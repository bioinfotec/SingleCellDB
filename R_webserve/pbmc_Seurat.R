library(RestRserve)
library(png)
library(Seurat)

app = Application$new()

CommonPngFile <- function(plot_func, width, height, res) {
  png_file <- tempfile(fileext = ".png")
  png(png_file, width = width, height = height, res = res)
  plot_func()
  dev.off()
  
  return(png_file)
}

CommonHandler <- function(.req, .res, png_function, width = 600, height = 400, res=72) {
  png_file <- CommonPngFile(plot_func = png_function, width = width, height = height, res=res)
  # 将图像文件发送给前端
    img_data <- readBin(png_file, "raw", n = file.info(png_file)$size)
    .res$set_body(img_data)
    .res$set_content_type("image/png")
    .res$set_header("Content-Disposition", "inline")
    .res$set_header("Access-Control-Allow-Origin", "http://110.41.149.156:8000")
    unlink(png_file)
}

pbmc.data <- Read10X(data.dir = "filtered_gene_bc_matrices/hg19/")
pbmc <- CreateSeuratObject(counts = pbmc.data, project = "pbmc3k", min.cells = 3, min.features = 200)
pbmc[["percent.mt"]] <- PercentageFeatureSet(pbmc, pattern = "^MT-")


img_VlnPlot <- function() {
  print(VlnPlot(pbmc, features = c("nFeature_RNA", "nCount_RNA", "percent.mt"), ncol = 3))
}
app$add_get(path = "/img-vlnplot", FUN = function(.req, .res) {
  CommonHandler(.req, .res, img_VlnPlot)
})

img_FeatureScatter <- function() {
  plot1 <- FeatureScatter(pbmc, feature1 = "nCount_RNA", feature2 = "percent.mt")
  plot2 <- FeatureScatter(pbmc, feature1 = "nCount_RNA", feature2 = "nFeature_RNA")
  print(plot1+plot2)
}
app$add_get(path = "/img-feature-scatter", FUN = function(.req, .res) {
  CommonHandler(.req, .res, img_FeatureScatter)
})

pbmc <- subset(pbmc, subset = nFeature_RNA > 200 & nFeature_RNA < 2500 & percent.mt < 5)
# pbmc <- NormalizeData(pbmc, normalization.method = "LogNormalize", scale.factor = 10000)
pbmc <- NormalizeData(pbmc)

pbmc <- FindVariableFeatures(pbmc, selection.method = "vst", nfeatures = 2000)
top10 <- head(VariableFeatures(pbmc), 10)
pbmc <- ScaleData(pbmc, features = top10)

img_HighVarFeatures <- function() {
  plot1 <- VariableFeaturePlot(pbmc)
  plot2 <- LabelPoints(plot = plot1, points = top10, repel = TRUE)
  print(plot1+plot2)
}
app$add_get(path = "/img-highVar-features", FUN = function(.req, .res) {
  CommonHandler(.req, .res, img_HighVarFeatures)
})

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
app$add_get(path = "/txt-examine-pca", FUN = txt_Examine_PCA_handler)

img_Examine_PCA <- function() {
  print(VizDimLoadings(pbmc, dims = 1:2, reduction = "pca"))
}
app$add_get(path = "/img-examine-pca", FUN = function(.req, .res) {
  CommonHandler(.req, .res, img_Examine_PCA)
})

img_PCA_DimPlot <- function() {
  print(DimPlot(pbmc, reduction = "pca"))
}
app$add_get(path = "/img-pca-dimplot", FUN = function(.req, .res) {
  CommonHandler(.req, .res, img_PCA_DimPlot)
})

img_PCA_Headtmap <- function() {
  print(DimHeatmap(pbmc, dims = 1, cells = 500, balanced = TRUE))
}
app$add_get(path = "/img-pca-headtmap", FUN = function(.req, .res) {
  CommonHandler(.req, .res, img_PCA_Headtmap)
})

img_15_PCA_Headtmap <- function() {
  print(DimHeatmap(pbmc, dims = 1:15, cells = 500, balanced = TRUE))
}
app$add_get(path = "/img-15-pca-headtmap", FUN = function(.req, .res) {
  CommonHandler(.req, .res, img_15_PCA_Headtmap, width = 1200, height = 1000, res=95)
})

app$add_post(path = "/choose-data", FUN = function(.req, .res) {
  # 从请求中获取选择的数据
  selectedData <- .req$post_body$selectedData
  print(selectedData)
})

backend = BackendRserve$new()
backend$start(app, http_port = 8080)


# # 设置定时器，每隔一段时间执行清理内存函数
# timer <- Sys.time()
# interval <- 60  # 每隔60秒执行一次
# while (TRUE) {
#   if (difftime(Sys.time(), timer, units = "secs") >= interval) {
#     gc()
#     timer <- Sys.time()
#   }
#   Sys.sleep(1)
# }


