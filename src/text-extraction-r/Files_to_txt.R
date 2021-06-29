
# This website gives good information on reading pdfs in R:
# https://data.library.virginia.edu/reading-pdf-files-into-r-for-text-mining/

# This website gives good information on reading word files in R:
# http://theautomatic.net/2020/07/21/how-to-read-and-create-word-documents-in-r/

# Load the required libraries.
# Note: you need to install these packages first using 
# install.packages("packagename").
library(pdftools)
library(officer)

# Define location of data. I'm using a relative path here.
# In order to do the same, make sure you create a folder called
# "data" in the directory of this script.
data_path <- "./data/"

# Also make a directory to write the .txt files into. 
# Name it 'txtdata'. 
txt_path <- "./txtdata/"



# ---------------------- PDF files ----------------------- #

# This gives you a list of the pdf files in your data directory.
pdf_files <- list.files(path = data_path, pattern = "pdf$")

# This gives a list with one element per word file. It has flat text,
# but it is very rudimentary.
pdf_reports <- lapply(paste0(data_path, pdf_files), pdf_text)

# Write into seperate .txt files
for (i in seq_len(length(pdf_files))) {
    writeLines(pdf_reports[[i]],
              paste0(txt_path,
              substr(pdf_files[i], 1, nchar(pdf_files[i]) - 4),
              ".txt"), useBytes = T)
}

# ---------------------- Word files ---------------------- #

# This gives you a list of the word files in your data directory.
word_files <- list.files(path = data_path, pattern = ".docx$")

# This gives a list with one element per word file. It needs further
# extraction and cleaning before it can be used.
word_reports <- lapply(paste0(data_path, word_files), read_docx)

# Read the contents of the word files using docx_summary().
word_contents <- lapply(word_reports, docx_summary)

# Write the text into seperate .txt files
for (i in seq_len(length(word_files))) {
    writeLines(word_contents[[i]]$text,
              paste0(txt_path,
              substr(word_files[i], 1, nchar(word_files[i]) - 5),
              ".txt"), useBytes = T)
}

# ---------------------------------------------------------- #

# Help with Orange:
# https://orange3-text.readthedocs.io/en/latest/
# https://orangedatamining.com/workflows/