from django.test import TestCase
from django.views.decorators.cache import never_cache
import time
from .models import dataset_info,gene_expression

print("start")
t1 = time.perf_counter()
dataset_id = "GSE138002"
dataset_instance = dataset_info.objects.get(dataset_id=dataset_id)

# f = open("/home/zhupei/singleCell/SingleCellDB/media/user_admin/gse000/GSE000_cell.txt", "r")
# cell_number = 0
# cell_types = []

# for idx, line in enumerate(f):
#     if idx == 0:
#         continue
#     print("line: ", idx)
#     cell_number += 1
#     data = line.strip().split("\t")
#     print(data[0])
#     if data[3] not in cell_types:
#         cell_types.append(data[3])
    
#     barcode = data[0]
#     cell_type = data[3]
# f.close()
start_time = time.perf_counter()
f = open("/home/zhupei/data/GSE138002/GSE138002_Final_matrix.mtx", "r")
expression_data = {}
print("-"*10+"start")
for _ in range(2):
    next(f)
lines = f.readlines()
for idx, line in enumerate(lines):
    row, col, value = map(float, line.strip().split())
    row = int(row)
    col = int(col)
    if row not in expression_data:
        expression_data[row] = {}
    expression_data[row][col] = value
f.close()
print(time.perf_counter()-start_time)
# print("-"*10+"开始处理数据")
# f = open("/home/zhupei/data/GSE138002/gene_test.txt", "r")
# gene_exp_list = []

# for idx, line in enumerate(f, start=1):
#     data = line.strip().split("\t")
#     gene_ensg = data[0]
#     gene_name = data[1]
#     try:
#         gene_exp = expression_data[idx]
#         gene_exp_list.append(gene_expression(dataset_info=dataset_instance, gene_name=gene_name, expression=gene_exp))
#     except:
#         gene_exp_list.append(gene_expression(dataset_info=dataset_instance, gene_name=gene_name))
# f.close()
# print(time.perf_counter()-start_time)
# print("-"*10+"开始插入数据")
# for i in range(0, len(gene_exp_list), 2000):
#     print("开始插入", i)
#     gene_expression.objects.bulk_create(gene_exp_list[i:i+2000])
# print(time.perf_counter()-start_time)
# t2 = time.perf_counter()
# # 输出时间
# print(t2-t1)
        