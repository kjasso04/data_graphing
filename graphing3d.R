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



library(rgl)
library(readxl)
#library(ggplot2)
library(plotly)
library(rstudioapi)
library(stringr)

current_file_path <- rstudioapi::getActiveDocumentContext()$path
folderpath <- str_replace(current_file_path, basename(current_file_path), "")


# Read the data from the Excel file
collData <- read.csv(file.path(folderpath, "rowFilter.csv"))

# getting columns for plotting

name <- collData$sample
monomer1 <- collData$monomer1
monomer2 <- collData$monomer2
mol <- collData$crosslinkermol

monomer1 <-as.factor(monomer1)
monomer2 <-as.factor(monomer2)
mol <-as.numeric(mol)

print(monomer1)

print(monomer1)

#making function and getting base colors 
string_to_color <- function(take) {
  print(take)
  return (sum(utf8ToInt(take)) )
  
}


color_values <- sapply(name, string_to_color)
color_values <- color_values[complete_cases]

#assign rgb
red <- (color_values %% 255)/255
blue <- ((color_values * length(name))  %% 255 )/255
green <- ((color_values * 8) %% 255)/255

print(red)
print(blue)
print(green)

print(color_values)

# Plot 3D
#install.packages("scatterplot3d")
library(plotly)
fig <- plot_ly(
  data, 
  x = monomer1, 
  y = monomer2, 
  z = mol, 
  type = "scatter3d", 
  mode = "markers",
  marker = list(size = 5, color = rgb(red, blue , green), colorscale = "Viridis")
)

fig <- fig %>% layout(
  scene = list(
    xaxis = list(title = 'monomer1'),
    yaxis = list(title = 'monomer2'),
    zaxis = list(title = 'mol%')
  )
)

fig