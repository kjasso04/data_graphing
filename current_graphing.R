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
testdata3 <- read_excel(paste( str_replace(current_file_path, basename(current_file_path), ""), "/test_filtered_data.xlsx",sep = ""))


# getting columns for plotting

name <- testdata3$sample
monomer1 <- testdata3$monomer1
monomer2 <- testdata3$monomer2
mol <- testdata3$crosslinkermol

monomer1 <-as.factor(monomer1)
monomer2 <-as.factor(monomer2)
mol <-as.numeric(mol)

print(monomer1)

complete_cases <- complete.cases( monomer1, monomer2, mol)
monomer1 <- monomer1[complete_cases]
monomer2 <- monomer2[complete_cases]
mol <- mol[complete_cases]

print(monomer1)

#making function and getting base colors 
string_to_color <- function(take) {
  print(take)
  return (sum(utf8ToInt(take)) )
  
}


color_values <- sapply(name, string_to_color)

complete_color <- complete.cases(color_values)
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