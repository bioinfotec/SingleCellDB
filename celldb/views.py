from django.core.paginator import Paginator
from django.shortcuts import render
from .models import TranMeta, LiteratureMeta
from celldb_v2.models import literature_info

def home(request):
    logs = [
        {"date": "5.24~5.31", "content": "使用Django框架建立网站的雏形"},
        {"date": "6.1", "content": "实现了在后端对Single_cell_Meta_data.txt中的数据进行绘制，并传回前端页面"},
        {"date": "6.3", "content": "学习使用JavaScript，以便处理数据格式"},
        {"date": "6.4~6.6", "content": "使用echarts.js绘图"},
        {"date": "6.7~6.10", "content": "分页功能实现"},
        {"date": "6.11~15", "content": "尝试前后端分离"},
        {"date": "6.16~6.20", "content": "完善搜索功能和分页按钮"},
        {"date": "6.21~6.27", "content": "使用Databales插件;增加了下载数据功能;Plot增加了筛选功能;上传了summary文件中的数据"},
        {"date": "6.28~7.5", "content": "对数据过滤，允许对数据进行添加或删除"},
    ]
    return render(request, "celldb/home.html", {"logs": logs})

def overview(request):
    literature = literature_info.objects.all()
    return render(request, "celldb/overview.html", {"literature_info":literature})

def browseFeature(request):
    # 根据参数浏览数据
    pmid = request.GET.get("pmid", None)
    context = {"pmid": pmid}
    return render(request, "celldb/browseFeature.html", context)

def browseExpression(request):
    # 根据参数浏览数据
    pmid = request.GET.get("pmid", None)
    context = {"pmid": pmid}
    return render(request, "celldb/browseExpression.html", context)

def download(request):
    # restframework暂时未能实现
    # response = requests.get("http://127.0.0.1:8000/api/tran/", params=request.GET)
    # if response.status_code == 200:
    #     data = response.json()
    #     results = data['results']
    #     paginator = Paginator(results, 10)
    #     page_number = request.GET.get('page',1)
    #     page_data = paginator.get_page(page_number)
    # else:
    #     page_data = Paginator([], 10).get_page(1)
    # return render(request, 'celldb/data.html', {'data': page_data})

    # 直接使用内置API
    data = TranMeta.objects.all()
    items_per_page = 10
    paginator = Paginator(data, items_per_page)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "celldb/download.html", {"page_obj": page_obj})

def upload(request):
    return render(request, "celldb/upload.html")

def plotScatter(request):
    # 根据参数绘制散点图
    pmid = request.GET.get("pmid", None)
    context = {"pmid": pmid}
    return render(request, "celldb/plotScatter.html", context)

def plotLocal(request):
    return render(request, "celldb/plotLocal.html")

def plotR(request):
    return render(request, "celldb/plotR.html")

def runCode(request):
    return render(request, "celldb/runCode.html")

def analyse(request):
    # 根据参数分析数据
    pmid = request.GET.get("pmid", None)
    context = {"pmid": pmid}
    return render(request, "celldb/analyse.html", context)

def test(request):
    return render(request, "celldb/test.html")

def test2(request):
    return render(request, "celldb/test2.html")
