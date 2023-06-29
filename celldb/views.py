from django.core.paginator import Paginator
from django.shortcuts import render
from .models import TranMeta, LiteratureMeta
import requests
from django.views import View
from django.http import HttpResponse


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
    ]
    return render(request, "celldb/home.html", {"logs": logs})


def plotScatter(request):
    return render(request, "celldb/plotScatter.html")


def search(request):
    liter = LiteratureMeta.objects.all()
    # query = request.GET.get("query", "")
    data = ""
    # if query:
    #     response = requests.get(f"http://127.0.0.1:8000/api/tran/{query}.json")
    #     data = response.json()
    return render(request, "celldb/search.html", {"data": data, "liter":liter})


def data(request):
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
    return render(request, "celldb/data.html", {"page_obj": page_obj})


def test(request):
    return render(request, "celldb/test.html")
