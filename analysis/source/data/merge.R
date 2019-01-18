library(tidyverse)
library(stringr)
library(data.table)
library(fst)
library(yaml)

D   <- yaml.load_file('config_global.yaml')
compare <- D$build$raw$compare
data <- D$build$data
auxiliary <- D$build$raw$auxiliary

month_dict <- c(1, 3, 4, 6, 7, 9, 10, 11, 12)
names(month_dict) <- c("january", "march", "april", "june", "july", "september", "october", "november", "december")

variables_to_select <- c(
  "NPI", "Professional Enrollment ID", "Last Name", "First Name", "Middle Name",
  "Gender", "Medical school name", "Graduation year", "Primary specialty", "Secondary specialty 1",
  "Secondary specialty 2", "Secondary specialty 3", "Secondary specialty 4", "Group Practice PAC ID", "Number of Group Practice members",
  "Line 1 Street Address", "Line 2 Street Address", "Marker of address line 2 suppression",
  "City", "State", "Zip Code", "Claims based hospital affiliation LBN 1", "Claims based hospital affiliation LBN 2",
  "Claims based hospital affiliation LBN 3", "Claims based hospital affiliation LBN 4", "Claims based hospital affiliation LBN 5"
)

names_40 <- c(
  "NPI", "PAC ID", "Professional Enrollment ID", "Last Name",
  "First Name", "Middle Name", "Suffix", "Gender", "Credential",
  "Medical school name", "Graduation year", "Primary specialty",
  "Secondary specialty 1", "Secondary specialty 2", "Secondary specialty 3",
  "Secondary specialty 4", "All secondary specialties", "Organization legal name",
  "Group Practice PAC ID", "Number of Group Practice members",
  "Line 1 Street Address", "Line 2 Street Address", "Marker of address line 2 suppression",
  "City", "State", "Zip Code",
  "Claims based hospital affiliation CCN 1",
  "Claims based hospital affiliation LBN 1", "Claims based hospital affiliation CCN 2",
  "Claims based hospital affiliation LBN 2", "Claims based hospital affiliation CCN 3",
  "Claims based hospital affiliation LBN 3", "Claims based hospital affiliation CCN 4",
  "Claims based hospital affiliation LBN 4", "Claims based hospital affiliation CCN 5",
  "Claims based hospital affiliation LBN 5", "Professional accepts Medicare Assignment",
  "Participating in eRx", "Participating in PQRS", "Participating in EHR"
)

read_and_format <- function(path) {
  print(path)
  month <- month_dict[str_match(path, "_(.+)?_")[, 2]] %>% str_pad(2, pad = "0")
  year <- str_match(path, "201[4-9]") %>% as.character()
  if (str_detect(path, 'march_2014') | str_detect(path, 'june_2014') {
    data <- read_csv(path, col_names = F)
    names(data) <- names_40
  }
  else if (str_detect(path, ".csv") & !(str_detect(path, 'march_2014') & !str_detect(path, 'june_2014') {
    data <- read_csv(path)
  } else {
    data <- read_tsv(path)
  }
  data <- data %>% select(one_of(variables_to_select)) %>% mutate(month = month, year = year)
  return(data)
}

files <- list.files(compare, full.names = T)
csvs <- list()
for (f in files) {
  csvs[[length(csvs) + 1]] <- read_and_format(f)
}

compare <- rbindlist(csvs, fill = T)
write_fst(compare, str_interp("${data}/compare_all.fst"))
rm(csvs)

years <- list()
for (year in 2013:2017) {
  data <- read_csv(str_interp("${year}/OP_DTL_GNRL_PGYR${year}_P06292018.csv")) %>%
    select(
      Teaching_Hospital_ID, Physician_Profile_ID, Physician_First_Name, Physician_Last_Name, 
      Physician_Middle_Name, Recipient_Zip_Code, Recipient_State, Nature_of_Payment_or_Transfer_of_Value,
      Applicable_Manufacturer_or_Applicable_GPO_Making_Payment_ID, Total_Amount_of_Payment_USDollars, Date_of_Payment,
    ) %>%
    mutate(year = year)
  years[[length(years) + 1]] <- data
}
payments <- rbindlist(years, fill = T)
write_fst(payments, str_interp("${data}/payments_all.fst"))
rm(years)

zip2fips <- read_csv(str_interp("${auxiliary}/zip2fips.csv"), col_types = cols(.default = "c"))
compare <- compare %>% mutate(`Zip Code` = substring(`Zip Code`, 1, 5), year = as.numeric(year)) %>% group_by(year) %>% filter(month == min(month)) %>% ungroup()

population <- read_csv(str_interp("${auxiliary}/population_acs17.csv"), col_types = cols(.default = "c")) %>%
  slice(2:n()) %>%
  select(GEO.id2, HD01_VD01) %>%
  rename(fips = GEO.id2, population = HD01_VD01) %>%
  mutate(population = as.numeric(population))

income <- read_csv(str_interp("${auxiliary}/income_acs17.csv"), col_types = cols(.default = "c")) %>%
  slice(2:n()) %>%
  select(GEO.id2, HC01_EST_VC01) %>%
  rename(fips = GEO.id2, income = HC01_EST_VC01) %>%
  mutate(income = as.numeric(income))

zip_level <- compare %>%
  inner_join(zip2fips, by = c("Zip Code" = "zip")) %>%
  select(contains("specialty"), fips, year) %>%
  mutate(count = 1) %>%
  gather(specialty, primary_specialty, -c("fips", "year")) %>%
  select(-specialty) %>%
  group_by(fips, primary_specialty, year) %>%
  summarise(total_physicians = n())

merge <- payments %>%
  inner_join(compare, by = c("Physician_Last_Name" = "Last Name", "Physician_Middle_Name" = "Middle Name", "Physician_First_Name" = "First Name", "Recipient_State" = "State", "year" = "year")) %>%
  rename(primary_specialty = `Primary specialty`, state = Recipient_State, zip = Recipient_Zip_Code) %>%
  mutate(zip = substring(zip, 1, 5)) %>%
  inner_join(zip2fips, by = 'zip') %>%
  group_by(fips, primary_specialty, state, year) %>%
  summarise(total_payments = sum(Total_Amount_of_Payment_USDollars)) %>%
  inner_join(zip_level, by = c("fips", "primary_specialty", "year")) %>%
  inner_join(population, by = "fips") %>%
  inner_join(income, by = "fips") %>%
  mutate(payments_per_capita = total_payments / total_physicians, people_per_physician = population / total_physicians)

write_fst(merge, str_interp('${data}/dataset-prepared.fst'))
