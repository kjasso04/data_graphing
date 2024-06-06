# Install and load required packages
if (!requireNamespace("rgl", quietly = TRUE)) {
  install.packages("rgl")
}
if (!requireNamespace("rstudioapi", quietly = TRUE)) {
  install.packages("rstudioapi")
}
if (!requireNamespace("plotly", quietly = TRUE)) {
  install.packages("plotly")
}
if (!requireNamespace("scatterplot3d", quietly = TRUE)) {
  install.packages("scatterplot3d")
}

library(rgl)
library(ggplot2)
library(rstudioapi)
library(plotly)
library(stringr)
library(scatterplot3d)

# Define the addgrids2d function if not already defined
# Assuming the function is defined elsewhere if needed

current_file_path <- rstudioapi::getActiveDocumentContext()$path
folderpath <- str_replace(current_file_path, basename(current_file_path), "")

# Read the data from the csv file
collData <- read.csv(file.path(folderpath, "rowFilter.csv"))

# Extract the columns for plotting
name <- collData$sample
monomer1 <- collData$monomer1mapped
monomer2 <- collData$monomer2mapped
mol <- collData$crosslinkermol

# Function to generate a color value
string_to_color <- function(take) {
  return(sum(utf8ToInt(take)))
}

# Generate color values and remove NAs
color_values <- sapply(name, string_to_color)
color_values <- na.omit(color_values)

# Assign rgb values
red <- (color_values %% 255) / 255
blue <- ((color_values * length(name)) %% 255) / 255
green <- ((color_values * 8) %% 255) / 255

# Plot 3D
s3d <- scatterplot3d(monomer1, monomer2, mol, color = rgb(red, green, blue),
                     pch = 16, type = "h", main = "3D Scatter Plot")

# Uncomment this line if you need interactive 3D plotting
# plot3d(monomer1, monomer2, mol, col = rgb(red, green, blue), size = 3)
