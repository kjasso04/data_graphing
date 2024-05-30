# Install and load required packages
if (!requireNamespace("scatterplot3d", quietly = TRUE)) {
  install.packages("scatterplot3d")
}
if (!requireNamespace("datasets", quietly = TRUE)) {
  install.packages("datasets")
}

library(scatterplot3d)
library(datasets)

# Define the addgrids3d function
addgrids3d <- function(s3d, xlim, ylim, zlim, grid = c("xy", "xz", "yz"), ...) {
  save <- par("xpd", "col.lab", "col.axis")
  on.exit(par(save))
  par(xpd = TRUE, col.lab = "gray", col.axis = "gray")
  
  if ("xy" %in% grid) {
    for (z in seq(from = zlim[1], to = zlim[2], length.out = 10)) {
      coords <- s3d$xyz.convert(cbind(xlim, ylim, z))
      segments(coords$x[,3], coords$y[,3], coords$x[,3], coords$y[,2], col = "gray")
    }
  }
  
  if ("xz" %in% grid) {
    for (y in seq(from = ylim[1], to = ylim[2], length.out = 10)) {
      coords <- s3d$xyz.convert(cbind(xlim, y, zlim))
      segments(coords$x[,1], coords$y[,1], coords$x[,2], coords$y[,2], col = "gray")
    }
  }
  
  if ("yz" %in% grid) {
    for (x in seq(from = xlim[1], to = xlim[2], length.out = 10)) {
      coords <- s3d$xyz.convert(cbind(x, ylim, zlim))
      segments(coords$x[,1], coords$y[,1], coords$x[,2], coords$y[,2], col = "gray")
    }
  }
}

# Load the iris dataset
data(iris)

# Ensure the data is a 3-column matrix
iris_matrix <- as.matrix(iris[, 1:3])

# Create an empty 3D scatter plot using pch=""
s3d <- scatterplot3d(iris_matrix, pch = "", grid = FALSE, box = FALSE)

# Define axis limits
xlim <- range(iris_matrix[,1])
ylim <- range(iris_matrix[,2])
zlim <- range(iris_matrix[,3])

# Add grids
addgrids3d(s3d, xlim, ylim, zlim, grid = c("xy", "xz", "yz"))

# Add points
s3d$points3d(iris_matrix, pch = 16)
