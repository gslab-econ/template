set more off

program main
    say_hello
    first_letters
end

program say_hello
    display "Hello world! This is a test Stata script."
end

program first_letters
     import delimited ../../output/data/stopWords_Fox_lengths.csv
	 generate first_letter = substr(word, 1, 1)
	 generate count = 1
	 collapse (count) count (mean) len, by(first_letter)
	 rename len mean_letter_count
	 save ../../output/analysis/first_letters.dta
end

main
