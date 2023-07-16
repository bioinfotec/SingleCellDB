from rest_framework.decorators import api_view
from rest_framework.response import Response
import subprocess,os

@api_view(["POST"])
def execute_r_code(request):
    r_code = request.data.get("r_code")
    # 切换到当前路径
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    # 将 R 代码写入临时文件
    with open("tempCode/temp.R", "w") as file:
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