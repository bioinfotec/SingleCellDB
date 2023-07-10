library(RestRserve)
library(png)
library(Seurat)

app = Application$new()

pbmc.data <- Read10X(data.dir = "filtered_gene_bc_matrices/hg19/")
pbmc <- CreateSeuratObject(counts = pbmc.data, project = "pbmc3k", min.cells = 3, min.features = 200)
pbmc[["percent.mt"]] <- PercentageFeatureSet(pbmc, pattern = "^MT-")

img_VlnPlot  <- function() {
  png_file <- tempfile(fileext = ".png")
  png(png_file, width = 800, height = 600, res = 96)
  Vln = VlnPlot(pbmc, features = c("nFeature_RNA", "nCount_RNA", "percent.mt"), ncol = 3)
  print(Vln)
  dev.off()
  return(png_file)
}

img_VlnPlot_handler <- function(.req, .res) {
  png_file <- img_VlnPlot()
  # 将图像文件发送给前端
  img_data <- readBin(png_file, "raw", n = file.info(png_file)$size)
  .res$set_body(img_data)
  .res$set_content_type("image/png")
  .res$set_header("Content-Disposition", "inline")
  .res$set_header("Access-Control-Allow-Origin", "http://110.41.149.156:8000")
}

app$add_get(path = "/img-VlnPlot", FUN = img_VlnPlot_handler)

img_FeatureScatter  <- function() {
  plot1 <- FeatureScatter(pbmc, feature1 = "nCount_RNA", feature2 = "percent.mt")
  plot2 <- FeatureScatter(pbmc, feature1 = "nCount_RNA", feature2 = "nFeature_RNA")
  png_file <- tempfile(fileext = ".png")
  png(png_file, width = 600, height = 400, res = 72)
  print(plot1+plot2)
  dev.off()
  
  return(png_file)
}

img_FeatureScatter_handler <- function(.req, .res) {
  png_file <- img_FeatureScatter()
  
  # 将图像文件发送给前端
  img_data <- readBin(png_file, "raw", n = file.info(png_file)$size)
  .res$set_body(img_data)
  .res$set_content_type("image/png")
  .res$set_header("Content-Disposition", "inline")
  .res$set_header("Access-Control-Allow-Origin", "http://110.41.149.156:8000")
}

app$add_get(path = "/img-FeatureScatter", FUN = img_FeatureScatter_handler)

pbmc <- NormalizeData(pbmc, normalization.method = "LogNormalize", scale.factor = 10000)
pbmc <- NormalizeData(pbmc)

pbmc <- FindVariableFeatures(pbmc, selection.method = "vst", nfeatures = 2000)
top10 <- head(VariableFeatures(pbmc), 10)
pbmc <- ScaleData(pbmc, features = top10)

img_HighVarFeatures  <- function() {
  png_file <- tempfile(fileext = ".png")
  png(png_file, width = 600, height = 400, res = 72)
  plot1 <- VariableFeaturePlot(pbmc)
  plot2 <- LabelPoints(plot = plot1, points = top10, repel = TRUE)
  print(plot1+plot2)
  dev.off()
  
  return(png_file)
}

img_HighVarFeatures_handler <- function(.req, .res) {
  png_file <- img_HighVarFeatures()
  
  # 将图像文件发送给前端
  img_data <- readBin(png_file, "raw", n = file.info(png_file)$size)
  .res$set_body(img_data)
  .res$set_content_type("image/png")
  .res$set_header("Content-Disposition", "inline")
  .res$set_header("Access-Control-Allow-Origin", "http://110.41.149.156:8000")
}

app$add_get(path = "/img-HighVarFeatures", FUN = img_HighVarFeatures_handler)

all.genes <- rownames(pbmc)
pbmc <- ScaleData(pbmc, features = all.genes)
pbmc <- RunPCA(pbmc, features = VariableFeatures(object = pbmc))

txt_Examine_PCA  <- function() {
  output <- capture.output({
    print(pbmc[["pca"]], dims = 1:5, nfeatures = 5)
  })
}

txt_Examine_PCA_handler <- function(.req, .res) {
  output <- txt_Examine_PCA()
  output_text <- paste(output, collapse = "\n")
  .res$set_body(output_text)
  .res$set_content_type("text/plain")
  .res$set_header("Access-Control-Allow-Origin", "http://110.41.149.156:8000")
}

app$add_get(path = "/txt-Examine-PCA", FUN = txt_Examine_PCA_handler)

img_Examine_PCA  <- function() {
  png_file <- tempfile(fileext = ".png")
  png(png_file, width = 600, height = 400, res = 72)
  PCA_plot  <- VizDimLoadings(pbmc, dims = 1:2, reduction = "pca")
  print(PCA_plot)
  dev.off()
  
  return(png_file)
}

img_Examine_PCA_handler <- function(.req, .res) {
  png_file <- img_Examine_PCA()
  
  # 将图像文件发送给前端
  img_data <- readBin(png_file, "raw", n = file.info(png_file)$size)
  .res$set_body(img_data)
  .res$set_content_type("image/png")
  .res$set_header("Content-Disposition", "inline")
  .res$set_header("Access-Control-Allow-Origin", "http://110.41.149.156:8000")
}

app$add_get(path = "/img-Examine-PCA", FUN = img_Examine_PCA_handler)

img_PCA_DimPlot  <- function() {
  png_file <- tempfile(fileext = ".png")
  png(png_file, width = 600, height = 400, res = 72)
  PCA_plot  <- DimPlot(pbmc, reduction = "pca")
  print(PCA_plot)
  dev.off()
  
  return(png_file)
}

img_PCA_DimPlot_handler <- function(.req, .res) {
  png_file <- img_PCA_DimPlot()
  
  # 将图像文件发送给前端
  img_data <- readBin(png_file, "raw", n = file.info(png_file)$size)
  .res$set_body(img_data)
  .res$set_content_type("image/png")
  .res$set_header("Content-Disposition", "inline")
  .res$set_header("Access-Control-Allow-Origin", "http://110.41.149.156:8000")
}

app$add_get(path = "/img-PCA-DimPlot", FUN = img_PCA_DimPlot_handler)

img_PCA_Headtmap  <- function() {
  png_file <- tempfile(fileext = ".png")
  png(png_file, width = 600, height = 400, res = 72)
  PCA_plot  <- DimHeatmap(pbmc, dims = 1, cells = 500, balanced = TRUE)
  print(PCA_plot)
  dev.off()
  
  return(png_file)
}

img_PCA_Headtmap_handler <- function(.req, .res) {
  png_file <- img_PCA_Headtmap()
  
  # 将图像文件发送给前端
  img_data <- readBin(png_file, "raw", n = file.info(png_file)$size)
  .res$set_body(img_data)
  .res$set_content_type("image/png")
  .res$set_header("Content-Disposition", "inline")
  .res$set_header("Access-Control-Allow-Origin", "http://110.41.149.156:8000")
}

app$add_get(path = "/img_PCA_Headtmap", FUN = img_PCA_Headtmap_handler)

img_15_PCA_Headtmap  <- function() {
  png_file <- tempfile(fileext = ".png")
  png(png_file, width = 1200, height = 800, res = 72)
  PCA_plot  <- DimHeatmap(pbmc, dims = 1:15, cells = 500, balanced = TRUE)
  print(PCA_plot)
  dev.off()
  
  return(png_file)
}

img_15_PCA_Headtmap_handler <- function(.req, .res) {
  png_file <- img_15_PCA_Headtmap()
  
  # 将图像文件发送给前端
  img_data <- readBin(png_file, "raw", n = file.info(png_file)$size)
  .res$set_body(img_data)
  .res$set_content_type("image/png")
  .res$set_header("Content-Disposition", "inline")
  .res$set_header("Access-Control-Allow-Origin", "http://110.41.149.156:8000")
}

app$add_get(path = "/img_15_PCA_Headtmap", FUN = img_15_PCA_Headtmap_handler)

backend = BackendRserve$new()
backend$start(app, http_port = 8080)
