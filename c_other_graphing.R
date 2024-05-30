# Install and load required packages
if (!requireNamespace("rgl", quietly = TRUE)) {
  install.packages("rgl")
}
if (!requireNamespace("readxl", quietly = TRUE)) {
  install.packages("readxl")
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
library(readxl)
library(ggplot2)
# library(rprojroot) # Uncomment if needed
library(rstudioapi)
library(plotly)
library(stringr)
library(scatterplot3d)

# Define the addgrids3d function if not already defined
addgrids3d <- function(x, y = NULL, z = NULL, grid = c("xy", "xz", "yz"), ...) {
  if (!inherits(x, "scatterplot3d")) {
    if (is.null(y) || is.null(z)) {
      stop("If 'x' is not a scatterplot3d object, 'y' and 'z' must be provided")
    }
    s3d <- scatterplot3d(x, y, z, ...)
  } else {
    s3d <- x
    if (is.null(y) || is.null(z)) {
      y <- s3d$xyz.convert(y)
      z <- s3d$xyz.convert(z)
    }
  }
  
  if (any(grid == "xy")) {
    s3d$points3d(s3d$xyz.convert(x, y, 0), type = "h", col = "gray")
  }
  if (any(grid == "xz")) {
    s3d$points3d(s3d$xyz.convert(x, 0, z), type = "h", col = "gray")
  }
  if (any(grid == "yz")) {
    s3d$points3d(s3d$xyz.convert(0, y, z), type = "h", col = "gray")
  }
}

current_file_path <- rstudioapi::getActiveDocumentContext()$path
folderpath <- str_replace(current_file_path, basename(current_file_path), "")

# Read the data from the Excel file
testdata3 <- read_excel(file.path(folderpath, "test_filtered_data.xlsx"))

# Extract the columns for plotting
name <- testdata3$sample
monomer1 <- testdata3$mappedmonomer1
monomer2 <- testdata3$mappedmonomer2
mol <- testdata3$crosslinkermol

complete_cases <- complete.cases(name, monomer1, monomer2, mol)
name <- name[complete_cases]
monomer1 <- monomer1[complete_cases]
monomer2 <- monomer2[complete_cases]
mol <- mol[complete_cases]

# Function to generate a color value
string_to_color <- function(take) {
  print(take)
  return(sum(utf8ToInt(take)))
}

color_values <- sapply(name, string_to_color)

complete_color <- complete.cases(color_values)
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
