from django.core.paginator import Paginator
from django.shortcuts import render
from .models import TranMeta, LiteratureMeta
from celldb_v2.models import literature_info, literature_dataset, dataset_info, cell_type_info
from django.contrib.auth.decorators import login_required

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
    species_all = dataset_info.objects.all().values_list("species_name", flat=True).distinct()
    cell_types_all = cell_type_info.objects.all().values_list("cell_type_name", flat=True).distinct()
    selected_species = request.GET.get('species', None)
    selected_cell_type = request.GET.get('cell_type', None)
    queryset = literature_info.objects.all()
    if selected_species:
        queryset = queryset.filter(dataset_info__species_name=selected_species)
    if selected_cell_type:
        queryset = queryset.filter(dataset_info__cell_types__icontains=selected_cell_type).distinct()
    return render(request, "celldb/overview.html", {"literature_info":queryset, "species_all":species_all, "cell_types_all":cell_types_all, "selected_cell_type":selected_cell_type, "selected_species":selected_species})

def browse(request):
    # pmids = literature_info.objects.all().values_list("pmid", flat=True).distinct()
    # species = dataset_info.objects.all().values_list("species_name", flat=True).distinct()
    # cell_types = cell_type_info.objects.all().values_list("cell_type_name", flat=True).distinct()
    # context = {"pmids": pmids, "species": species, "cell_types": cell_types}
    return render(request, "celldb/browse.html")

def browseDataset(request):
    req_pmid = request.GET.get("pmid", None)
    pmids = literature_info.objects.all().values_list("pmid", flat=True).distinct()
    species = dataset_info.objects.all().values_list("species_name", flat=True).distinct()
    cell_types = cell_type_info.objects.all().values_list("cell_type_name", flat=True).distinct()
    res_dataset = None
    if req_pmid:
        res_dataset = literature_info.objects.get(pmid=req_pmid).dataset_info_set.all()
    return render(request, "celldb/browseDataset.html", {"res_dataset": res_dataset, "pmids":pmids, "species":species, "cell_types":cell_types})

def browseFeature(request):
    dataset_ids = dataset_info.objects.all().values_list("dataset_id", flat=True).distinct()
    req_pmid = request.GET.get("pmid", None)
    if req_pmid:
        res_dataset_id = literature_info.objects.get(pmid=req_pmid).dataset_info_set.all().values_list("dataset_id", flat=True).distinct()[0]
    else:
        res_dataset_id = None
    context = {'dataset_ids': dataset_ids, 'res_dataset_id': res_dataset_id}
    return render(request, "celldb/browseFeature.html", context)

def browseExpression(request):
    dataset_ids = dataset_info.objects.all().values_list("dataset_id", flat=True).distinct()
    pmid = request.GET.get("pmid", None)
    context = {'dataset_ids': dataset_ids,"pmid": pmid}
    return render(request, "celldb/browseExpression.html", context)

def download(request):
    data = TranMeta.objects.all()
    items_per_page = 10
    paginator = Paginator(data, items_per_page)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "celldb/download.html", {"page_obj": page_obj})

@login_required(login_url='/accounts/login/')
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
