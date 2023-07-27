# library(RestRserve)

# app = Application$new()
# selectedData <- "APAP"
# app$add_post(path = "/choose-data", FUN = function(.req, .res) {
#   # 从请求中获取选择的数据
#   selectedData <- .req$get_param_query("data")
#   .res$set_body(paste("成功选择数据：",selectedData, "\n请等待服务器加载后点击下列按钮生成相应的图"))
#   .res$set_content_type("text/plain")
#   .res$set_header("Access-Control-Allow-Origin", "*")
# })

# backend = BackendRserve$new()
# backend$start(app, http_port = 8080)

library(RestRserve)
# 创建一个新的 RestRserve 应用程序
app <- Application$new()

# 添加一个 POST 路由，用于设置 selectedData 的值
app$add_post(path = "/choose-data", FUN = function(.req, .res) {
  # 从请求中获取 selectedData 的值
  selectedData <- .req$get_param_query("selectedData")
  source("plot_serve.R")
  # 打印 selectedData 的值
  .res$set_status_code(200)
  .res$set_content_type("text/plain")
  .res$set_body(paste("成功设置 selectedData 的值为：", selectedData, "\n请等待服务器加载后点击下列按钮生成相应的图"))
  .res$set_header("Access-Control-Allow-Origin", "*")
})

# 启动父进程的 RestRserve 服务器
backend <- BackendRserve$new()
backend$start(app, http_port = 8081)

