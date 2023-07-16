library(RestRserve)
library(png)

app = Application$new()

plot_scatter <- function(x, y) {
  # 绘制散点图
  png_file <- tempfile(fileext = ".png")
  png(png_file, width = 600, height = 400, res = 72)
  plot(x, y, main = "Scatter Plot", xlab = "X", ylab = "Y")
  dev.off()
  
  return(png_file)
}

scatter_handler <- function(.req, .res) {
  # x <- as.numeric(unlist(.req$parameters_query[["x"]]))
  # y <- as.numeric(unlist(.req$parameters_query[["y"]]))

  # if (length(x) == 0L || length(y) == 0L || any(is.na(x)) || any(is.na(y))) {
  #   raise(HTTPError$bad_request())
  # }
  x  <- c(1, 2, 3, 4, 5)
  y  <- c(3, 5, 4, 6, 8)
  png_file <- plot_scatter(x, y)
  
  # 将图像文件发送给前端
  img_data <- readBin(png_file, "raw", n = file.info(png_file)$size)
  .res$set_body(img_data)
  .res$set_content_type("image/png")
  .res$set_header("Content-Disposition", "inline")
  .res$set_header("Access-Control-Allow-Origin", "http://110.41.149.156:8000")
}

app$add_get(path = "/scatter", FUN = scatter_handler)

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

calc_fib = function(n) {
  if (n < 0L) stop("n should be >= 0")
  if (n == 0L) return(0L)
  if (n == 1L || n == 2L) return(1L)
  x = rep(1L, n)
  
  for (i in 3L:n) {
   x[[i]] = x[[i - 1]] + x[[i - 2]] 
  }
  
  return(x[[n]])
}

fib_handler = function(.req, .res) {
  n = as.integer(.req$parameters_query[["n"]])
  if (length(n) == 0L || is.na(n)) {
    raise(HTTPError$bad_request())
  }
  .res$set_body(as.character(calc_fib(n)))
  .res$set_content_type("text/plain")
}

app$add_get(path = "/fib", FUN = fib_handler)

backend = BackendRserve$new()
backend$start(app, http_port = 8081)