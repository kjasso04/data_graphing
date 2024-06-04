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
# library(rprojroot) # Uncomment if needed
library(rstudioapi)
library(plotly)
library(stringr)
library(scatterplot3d)

# Define the addgrids3d function if not already defined

current_file_path <- rstudioapi::getActiveDocumentContext()$path
folderpath <- str_replace(current_file_path, basename(current_file_path), "")

# Read the data from the CSV file
collData <- read.csv(file.path(folderpath, "rowFilter.csv"))

# Extract the columns for plotting
name <- collData$sample
monomer1 <- collData$mappedmonomer1
monomer2 <- collData$mappedmonomer2
mol <- collData$crosslinkermol


# Function to generate a color value
string_to_color <- function(take) {
  print(take)
  return(sum(utf8ToInt(take)))
}

color_values <- sapply(name, string_to_color)

color_values <- color_values[complete_color]

print(color_values)

# Assign rgb values
red <- (color_values %% 255) / 255
blue <- ((color_values * length(name)) %% 255) / 255
green <- ((color_values * 8) %% 255) / 255

# Plot 3D
s3d <- scatterplot3d(monomer1, monomer2, mol, color = rgb(red, blue, green),
                     pch = 16, type = "h", main = "3D Scatter Plot")

# Add grids

# Uncomment this line if you need interactive 3D plotting
# plot3d(monomer1, monomer2, mol, col = rgb(red, blue, green), size = 3)
