library(RestRserve)
library(ggplot2)
library(jsonlite)
library(RMySQL)

app <- Application$new()

plot_scatter <- function(filepath, expression) {
  data <- read.table(filepath, header = TRUE, sep = "\t")
  data$expression <- expression
  png_file <- tempfile(fileext = ".png")
  png(png_file, width = 500, height = 350, res = 96)
  plotfile <- ggplot(data, aes(x = UMAP_1, y = UMAP_2, color = expression)) +
    geom_point(size = 1) +
    scale_color_gradient(low = "grey", high = "red") +
    labs(color = "Expression")
    theme_minimal()
  print(plotfile)
  dev.off()
  return(png_file)
}
scatter_handler <- function(.req, .res) {
  con <- dbConnect(MySQL( ), 
                 user = "admin", 
                 password = "China123", 
                 dbname = "scdb", 
                 host = "aswmysqlsap.ceswkpd53vds.ap-southeast-1.rds.amazonaws.com")
  if (!is.null(con)) {
  tryCatch({
    # 获取参数
    genename <- .req$get_param_query("genename")
    dataset_id <- .req$get_param_query("dataset_id")
    
    # 从数据库获取文件路径
    filepath_query <- dbGetQuery(con, paste0("SELECT cell_file FROM celldb_v2_matrix_file WHERE data_id = '", dataset_id, "'"))
    filepath <- as.character(filepath_query)
    filepath <- paste0("../media/", filepath)
    
    # 从数据库获取数据
    query <- paste0("SELECT * FROM celldb_v2_gene_expression WHERE dataset_info_id = '", dataset_id, "' and gene_name='", genename,"'")
    print(query)
    result <- dbGetQuery(con, query)[1,]
    
    # 断开与数据库的连接
    dbDisconnect(con)
    
    # 处理结果数据
    result <- as.character(result[['expression']])
    if(is.na(result)) {
      .res$set_body("error")
      .res$set_content_type("application/json")
      .res$set_header("Access-Control-Allow-Origin", "*")
    }
    else {
    data <- read.table(filepath, header = TRUE, sep = "\t")
    expression <- numeric(nrow(data))
    parsed_data <- fromJSON(result)
    names(expression) <- as.character(1:nrow(data))
    expression[names(parsed_data)] <- as.numeric(parsed_data)
    
    # 创建散点图
    png_file <- plot_scatter(filepath, expression)
    
    # 读取图像数据并设置响应
    img_data <- readBin(png_file, "raw", n = file.info(png_file)$size)
    
    print(png_file)
    # 删除图片
    file.remove(png_file)

    # 传输
    .res$set_body(img_data)
    .res$set_content_type("image/png")
    .res$set_header("Content-Disposition", "inline")
    .res$set_header("Access-Control-Allow-Origin", "*")
    }
  }, error = function(e) {
    # 处理异常
    cat("发生错误：", conditionMessage(e), "\n")
    # 可以添加适当的错误响应
  })
} else {
  # 连接未成功建立，可以执行适当的处理
  cat("数据查询中发生错误\n")
  # 可以添加适当的错误响应
}
}
app$add_get(path = "/plot", FUN = scatter_handler)

backend <- BackendRserve$new()
backend$start(app, http_port = 8081)

