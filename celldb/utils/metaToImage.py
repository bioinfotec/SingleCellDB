import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import io


def process_data(uploaded_file):
    # 将上传的文件读取为DataFrame
    data = pd.read_csv(uploaded_file)
    
    # 执行数据分析
    analysis_figure = perform_analysis(data)
    
    # 将图像保存为二进制数据
    image_buffer = io.BytesIO()
    analysis_figure.savefig(image_buffer, format='png')
    image_buffer.seek(0)
    
    # 返回图像数据
    return image_buffer.getvalue()

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

    # 返回图像对象
    return plt.gcf()
