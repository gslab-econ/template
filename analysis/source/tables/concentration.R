library(tidyverse)
library(lfe)
library(stargazer)
library(starpolishr)
library(fst)
library(yaml)

D   <- yaml.load_file('config_global.yaml')
data <- D$build$data
out <- D$build$tables

write_models <- function(merge, type, cluster_state) {
  cs <- ifelse(cluster_state, "state", "0")
  cs_label <- ifelse(cluster_state, "state-clustering", "no-clustering")
  cs_note <- ifelse(cluster_state, "Standard errors clustered at the state level.", "Standard errors not clustered.")
  if (type == "logs") {
    merge$payments_per_capita <- (merge$payments_per_capita) * 10^(-6)
    bf <- "I(log(payments_per_capita)*10^6) ~ people_per_physician"
    title <- "Dependent variable: (Log payments per physician) $\\times 10^6$ "
  } else if (type == "levels") {
    bf <- "I(payments_per_capita*10^3) ~ people_per_physician"
    title <- "Dependent variable: (Payments per physician) $\\times 10^3$ "
  }

  model1 <- felm(formula(str_interp("${bf} | year | 0 | ${cs}")), weights = merge$total_physicians, data = merge)
  model2 <- felm(formula(str_interp("${bf} + income + population| year | 0 | ${cs}")), weights = merge$total_physicians, data = merge)
  model3 <- felm(formula(str_interp("${bf} | fips + year| 0 | ${cs} ")), weights = merge$total_physicians, data = merge)
  model4 <- felm(formula(str_interp("${bf} | primary_specialty + year| 0 | ${cs} ")), weights = merge$total_physicians, data = merge)
  model5 <- felm(formula(str_interp("${bf} | primary_specialty + fips + year | 0 | ${cs} ")), weights = merge$total_physicians, data = merge)

  output <- stargazer(list(model1, model2, model3, model4, model5),
    covariate.labels = c("Population per physician", "Income", "Population"),
    omit.stat = c("ser", "f", "rsq"),
    omit = c("Constant", "primary_specialty", "fips"),
    dep.var.labels.include = F,
    style = "aer", omit.table.layout = "n",
    star.cutoffs = c(0.1, 0.05, 0.01),
    add.lines = list(
      c("County FEs", "No", "No", "Yes", "No", "Yes"),
      c("Specialty FEs", "No", "No", "No", "Yes", "Yes"),
      c('Year FEs', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes')
    ),
    title = title
  ) %>%
    star_notes_tex(note.type = "threeparttable", note = str_interp("Regressions weighted by county population. ${cs_note}"))

  writeLines(output, con = str_interp("${out}/regressions-${type}-${cs_label}.tex"))
}

merge <- read_fst(str_interp('${data}/dataset-prepared.fst'))

write_models(merge, type = "logs", cluster_state = T)
write_models(merge, type = "logs", cluster_state = F)
write_models(merge, type = "levels", cluster_state = T)
write_models(merge, type = "levels", cluster_state = F)
