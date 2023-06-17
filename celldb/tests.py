from django.test import TestCase

#-----------------test-----------------
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def perform_analysis(data):
    # 创建UMAP图像
    sns.scatterplot(data=data, x='UMAP_X', y='UMAP_Y', hue='cell_type')

    cell_types = data['cell_type'].unique()

    for cell_type in cell_types:
        # 提取对应细胞类型的数据
        subset = data[data['cell_type'] == cell_type]
        # 在细胞类型的中心位置显示细胞类型文本
        x_center = subset['UMAP_X'].mean()
        y_center = subset['UMAP_Y'].mean()
        plt.text(x_center, y_center, cell_type, ha='center', va='center')

    # 设置图像标题和坐标轴标签
    plt.title('UMAP')
    plt.xlabel('UMAP_X')
    plt.ylabel('UMAP_Y')
    
    plt.legend(loc='upper right', fontsize=4)
    
    # 返回图像对象
    return plt.gcf()

def process_data():
    data = pd.read_csv(r"/mnt/c/Users/86188/Desktop/WangJie/DB/singleCell/celldb/data/Single_cell_Meta_data.txt")
    
    # 执行数据分析
    analysis_figure = perform_analysis(data)
    
    # 保存图像
    analysis_figure.savefig(r"/mnt/c/Users/86188/Desktop/WangJie/DB/singleCell/celldb/static/celldb/image.png", dpi=300)
    
process_data()