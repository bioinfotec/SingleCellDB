library(RestRserve)
library(Seurat)
library(png)

app = Application$new()

pbmc.data <- Read10X(data.dir = "filtered_gene_bc_matrices/hg19/")
pbmc <- CreateSeuratObject(counts = pbmc.data, project = "pbmc3k", min.cells = 3, min.features = 200)
pbmc[["percent.mt"]] <- PercentageFeatureSet(pbmc, pattern = "^MT-")

img_VlnPlot  <- function() {
  png_file <- tempfile(fileext = ".png")
  png(png_file, width = 600, height = 400, res = 72)
  VlnPlot(pbmc, features = c("nFeature_RNA", "nCount_RNA", "percent.mt"), ncol = 3)
  dev.off()
  
  return(png_file)
}

img_VlnPlot_handler <- function(.req, .res) {
  png_file <- img_VlnPlot()
  
  # 将图像文件发送给前端
  img_data <- readBin("plot.png", "raw", n = file.info("plot.png")$size)
  .res$set_body(img_data)
  .res$set_content_type("image/png")
  .res$set_header("Content-Disposition", "inline")
  .res$set_header("Access-Control-Allow-Origin", "http://110.41.149.156:8000")
}

app$add_get(path = "/img-VlnPlot", FUN = img_VlnPlot_handler)

plot_line <- function() {
  # 准备数据
  x <- c(1, 2, 3, 4, 5)
  y <- c(3, 5, 4, 6, 8)
  
  # 生成直线图
  png_file <- tempfile(fileext = ".png")
  png(png_file, width = 800, height = 600, res = 96)
  plot(x, y, type = "l", main = "Line Plot", xlab = "X", ylab = "Y")
  dev.off()
  
  return(png_file)
}

line_handler <- function(.req, .res) {
  png_file <- plot_line()
  
  # 将图像文件发送给前端
  img_data <- readBin(png_file, "raw", n = file.info(png_file)$size)
  .res$set_body(img_data)
  .res$set_content_type("image/png")
  .res$set_header("Content-Disposition", "inline")
  .res$set_header("Access-Control-Allow-Origin", "http://110.41.149.156:8000")
}

app$add_get(path = "/line", FUN = line_handler)

# plot1 <- FeatureScatter(pbmc, feature1 = "nCount_RNA", feature2 = "percent.mt")
# plot2 <- FeatureScatter(pbmc, feature1 = "nCount_RNA", feature2 = "nFeature_RNA")

# img_FeatureScatter  <- function() {
#   png_file <- tempfile(fileext = ".png")
#   png(png_file, width = 600, height = 400, res = 72)
#   plot1+plot2
#   dev.off()
  
#   return(png_file)
# }

# img_FeatureScatter_handler <- function(.req, .res) {
#   png_file <- img_FeatureScatter()
  
#   # 将图像文件发送给前端
#   img_data <- readBin(png_file, "raw", n = file.info(png_file)$size)
#   .res$set_body(img_data)
#   .res$set_content_type("image/png")
#   .res$set_header("Content-Disposition", "inline")
#   .res$set_header("Access-Control-Allow-Origin", "http://110.41.149.156:8000")
# }

# app$add_get(path = "/img-FeatureScatter", FUN = img_FeatureScatter_handler)

backend = BackendRserve$new()
backend$start(app, http_port = 8080)
