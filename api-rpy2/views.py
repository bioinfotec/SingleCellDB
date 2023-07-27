from rest_framework.decorators import api_view
from rest_framework.response import Response
import subprocess,os, signal,uuid
from django.http import HttpResponse
import rpy2.robjects as robjects
import rpy2.robjects.packages as rpackages
import rpy2.robjects.vectors as rvectors
from rpy2.robjects import conversion, default_converter

@api_view(["POST"])
def execute_r_code(request):
    r_code = request.data.get("r_code")
    # 将 R 代码写入临时文件
    with open("api-test/tempCode/temp.R", "w") as file:
        file.write(r_code)
    try:
        # 执行 R 代码并获取输出
        output = subprocess.check_output(["Rscript", "tempCode/temp.R"], stderr=subprocess.STDOUT)
        result = output.decode("utf-8")
        return Response({"result": result})
    except subprocess.CalledProcessError as e:
        error = e.output.decode("utf-8")
        return Response({"error": error})
    finally:
        subprocess.call(["rm", "tempCode/temp.R"])

current_process = None
def anaylse(request):
    print(os.getcwd())
    data_id = request.GET.get("data_id", None)
    global current_process
    if current_process is not None:
        os.kill(current_process.pid, signal.SIGTERM)
        current_process = None
    if data_id == "APAP":
        print(current_process)
        # Start the new subprocess and store its PID
        current_process = subprocess.Popen(["Rscript", "R_webserve/APAP_Seurat.R"])
        return HttpResponse("APAP")
    elif data_id == "pbmc":
        print(current_process)
        # Start the new subprocess and store its PID
        current_process = subprocess.Popen(["Rscript", "R_webserve/pbmc_Seurat.R"])
        return HttpResponse("pbmc")
    else:
        print(current_process)
        return HttpResponse("Invalid data_id")
    
    
# 定义要在 R 中执行的函数
def r_function(x,y,filename):
    try:
        r_code = f"""
        library(ggplot2)
        p <- ggplot(data.frame(x={x}, y={y}), aes(x=x, y=y)) +
            geom_point() +
            labs(title="R Plot")
        ggsave(p, filename="{filename}", width=4, height=3, dpi=300)
        """
        robjects.r(r_code)
        return "success"
    except Exception as e:
        error_message = str(e)
        return error_message
        
def test(request):
    x = request.GET.get("x", "c(1,2,3,4,5)")
    y = request.GET.get("y", "c(2,4,6,8,10)")
    filename = f"{uuid.uuid4()}_plot.png"
    with conversion.localconverter(default_converter):
        res = r_function(x, y, filename)
        if res != "success":
            return HttpResponse(res)
        with open(f"{filename}", "rb") as f:
            response = HttpResponse(f.read(), content_type="image/png")
            response["Content-Disposition"] = f"inline; filename={filename}"
        # 删除临时文件
        os.remove(filename)
    return response