# ----------------------------------------------------------- #
# Installing and load all the required packages
# ----------------------------------------------------------- #

install.packages("pacman")
pacman::p_load(config, biomaRt, dplyr, rstudioapi)


# Optional: can be used to set the working dir to the directory where this R file lives

current_path = rstudioapi::getActiveDocumentContext()$path 
setwd(dirname(current_path ))
print( getwd() )

# ----------------------------------------------------------- #
# Load in the data
# ----------------------------------------------------------- #
config <- config::get() # The config file contains the location for all the traits


# ----------------------------------------------------------- #
# Function to convert gene symbols to ensembl gene IDs
# ----------------------------------------------------------- #

gene_symbols_to_ensembl <- function(netwas_data){
  # Convert gene symbols into ensembl gene IDs using the biomaRt package. 
  #
  # :parameter
  # ----------
  # netwas_data - table
  #   Netwas data in CSV format containing three columns: gene_symbol, training_label, and netwas_score
  #
  # :returns
  # --------
  # res - table
  #   A new table containing the original gene symbol, ensembl gene ID and netwas score
  
  mart <- useMart('ENSEMBL_MART_ENSEMBL')
  mart <- useDataset('hsapiens_gene_ensembl', mart)
  annotLookup <- getBM(
    mart = mart,
    attributes = c(
      'hgnc_symbol',
      'ensembl_gene_id',
      'gene_biotype'),
    uniqueRows = TRUE)
  
  # Define the result dataframe
  res <- data.frame(gene_symbol=character(),
                    ensemble_id=character(),
                    netwas_score=numeric(),
                    stringsAsFactors=FALSE)
  
  for (row in 1:nrow(netwas_data)) {
    symbol <- netwas_data[row, "gene_symbol"]
    df_mod <- filter(annotLookup, grepl(symbol, hgnc_symbol))
    ensembl_id <- df_mod[df_mod$hgnc_symbol == symbol,'ensembl_gene_id']
    
    # Works
    if (length(ensembl_id) != 0){
      if (length(ensembl_id) > 1){
        res[nrow(res) + 1, ] <- c(symbol, ensembl_id[1], netwas_data[row, "netwas_score"])
      } else if (length(ensembl_id) == 1){
        res[nrow(res) + 1, ] <- c(symbol, ensembl_id, netwas_data[row, "netwas_score"])}
    }
  }
  return(res)
}


# ----------------------------------------------------------- #
# Parse the data
# ----------------------------------------------------------- #

read_netwas <- function(file){
  # Read in data resulting from NetWAS. Data is tab seperated and contains three columns: gene_symbol, training_label, netwas_score.
  #
  # :parameter
  # ----------
  # file - file
  #   Netwas data in tab seperated format containing three columns: gene_symbol, training_label, and netwas_score
  #
  # :returns
  # --------
  # data - table
  #   NetWAS data
  data <- read.csv(file, sep="\t", header = FALSE, col.names=c("gene_symbol", "training_label", "netwas_score"))
  return(data)
}

write_data <- function(data, file_name){
  # Write out data to a CSV file.
  #
  # :parameter
  # ----------
  # data - table
  #   Data to write out to a CSV file
  # file_name - str
  #   Name and location of the output file
  write.csv(data, file_name, row.names = FALSE)
}

for (trait in config$traits){
  # Read in the data
  data <- read_netwas(file=trait)
  
  print(trait)
  print("Converting gene symbols to ensembl IDs, this might take a while...")
  # Converted gene symbols to ensembl IDs
  converted_data <- gene_symbols_to_ensembl(netwas_data = data)
  
  # Write the output file to a results file
  output_file <- paste(config$output_folder, basename(trait), sep="")
  
  write_data(converted_data, output_file)
}