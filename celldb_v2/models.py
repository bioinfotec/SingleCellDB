from django.db import models
from django.contrib.auth.models import User
# 文献信息表
class literature_info(models.Model):
    pmid = models.CharField(primary_key=True,max_length=25)
    publication = models.CharField(max_length=50, blank=True, null=True)
    release_time = models.DateField(blank=True, null=True)
    article_title = models.CharField(max_length=255, blank=True, null=True)
    article_url = models.URLField(max_length=200, blank=True, null=True)
    articel_abstract = models.TextField(blank=True, null=True)
    articel_content = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.pmid
    
# 数据集表
class dataset_info(models.Model):
    dataset_id = models.CharField(primary_key=True,max_length=25)
    dataset_url = models.URLField(max_length=200, blank=True, null=True)
    used_method = models.CharField(max_length=50, blank=True, null=True)
    species_name = models.CharField(max_length=50, blank=True, null=True)
    tissue_name = models.CharField(max_length=50, blank=True, null=True)
    cell_types = models.TextField(blank=True, null=True)
    num_cells = models.IntegerField(blank=True, null=True)
    markers_main = models.TextField(blank=True, null=True)
    markers_other = models.TextField(blank=True, null=True)
    literature = models.ManyToManyField(literature_info, through='literature_dataset', blank=True)

    def __str__(self):
        return self.dataset_id

# 文献-数据集中间表
class literature_dataset(models.Model):
    literature_info = models.ForeignKey(literature_info, default="PMID000", on_delete=models.SET_DEFAULT)
    dataset_info = models.ForeignKey(dataset_info, default="GSE000", on_delete=models.SET_DEFAULT)
    
# 细胞信息表
class cell_info(models.Model):
    id = models.AutoField(primary_key=True)
    dataset_info = models.ForeignKey(dataset_info, on_delete=models.SET_NULL, null=True)
    orig_ident = models.CharField(max_length=100, blank=True, null=True)
    barcode = models.CharField(max_length=100, blank=True, null=True)
    cell_type = models.CharField(max_length=100, blank=True, null=True)
    ncount_rna = models.FloatField(blank=True,null=True)
    nfeature_rna = models.FloatField(blank=True,null=True)
    percent_mt = models.FloatField(blank=True,null=True)
    umap_1 = models.FloatField(blank=True,null=True)
    umap_2 = models.FloatField(blank=True,null=True)
    def __str__(self) -> str:
        return self.barcode
    
# 基因表达量表
class gene_expression(models.Model):
    id = models.AutoField(primary_key=True)
    dataset_info = models.ForeignKey(dataset_info, on_delete=models.SET_NULL, null=True)
    gene_name = models.CharField(max_length=50, blank=True, null=True)
    expression = models.JSONField(blank=True, null=True)
    cell_types = models.CharField(max_length=255, blank=True, null=True)
    def __str__(self) -> str:
        return self.gene_name

# 基因信息表
class gene_info(models.Model):
    id = models.AutoField(primary_key=True)
    gene_name = models.CharField(max_length=50)
    gene_ensg = models.CharField(max_length=50, blank=True, null=True)
    gene_annotation = models.TextField(blank=True, null=True)
    def __str__(self) -> str:
        return self.gene_name

#细胞类型表
class cell_type_info(models.Model):
    cell_type_name = models.CharField(primary_key=True,max_length=50, default="Unknown")
    cell_type_alias = models.CharField(max_length=50, blank=True, null=True)
    cell_type_annotation = models.TextField(blank=True, null=True)
    cell_type = models.ManyToManyField(dataset_info, through="dataset_cell_type")
    def __str__(self) -> str:
        return self.cell_type_name

# 数据集-细胞类型中间表
class dataset_cell_type(models.Model):
    dataset_info = models.ForeignKey(dataset_info, default="GSE000", on_delete=models.SET_DEFAULT)
    cell_type_info = models.ForeignKey(cell_type_info, default="GSE000", on_delete=models.SET_DEFAULT)

# 文件上传
def user_directory_path(instance, filename):
    # 文件将会上传到 MEDIA_ROOT/user_<user_id>/<filename>
    return f'user_{instance.user.id}/{instance.data_id}/{filename}'
class matrix_file(models.Model):
    user = models.ForeignKey(User, default="user",on_delete=models.SET_DEFAULT)
    data_id = models.CharField(max_length=50)
    gene_file = models.FileField(upload_to=user_directory_path)
    cell_file = models.FileField(upload_to=user_directory_path)
    expression_file = models.FileField(upload_to=user_directory_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.data_id