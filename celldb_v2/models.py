from django.db import models

# 文献信息表
class literature_info(models.Model):
    pmid = models.CharField(primary_key=True,max_length=25)
    publication = models.CharField(max_length=50, blank=True, null=True)
    release_time = models.DateField(blank=True, null=True)
    article_title = models.CharField(max_length=255, blank=True, null=True)
    article_url = models.URLField(max_length=200, blank=True, null=True)
    articel_abstract = models.TextField(blank=True, null=True)
    articel_content = models.TextField(blank=True, null=True)
    has_usefull_dataset = models.BooleanField(blank=True, null=True)

    def __str__(self):
        return self.pmid
    
# 数据集信息表
class dataset_info(models.Model):
    dataset_id = models.CharField(primary_key=True,max_length=25)
    literature = models.ManyToManyField(literature_info, through='literature_dataset', blank=True)

    def __str__(self):
        return self.dataset_id

# 文献与数据集关系表
class literature_dataset(models.Model):
    literature_info = models.ForeignKey(literature_info, on_delete=models.CASCADE)
    dataset_info = models.ForeignKey(dataset_info, on_delete=models.CASCADE)
    dataset_url = models.URLField(max_length=200, blank=True, null=True)
    dataset_path = models.FilePathField(blank=True, null=True)
    used_method = models.CharField(max_length=50, blank=True, null=True)
    species_name = models.CharField(max_length=50, blank=True, null=True)
    tissue_name = models.CharField(max_length=50, blank=True, null=True)
    cell_types = models.TextField(blank=True, null=True)
    num_cells = models.IntegerField(blank=True, null=True)
    markers_main = models.TextField(blank=True, null=True)
    markers_other = models.TextField(blank=True, null=True)

# 细胞信息表
class cell_info(models.Model):
    id = models.AutoField(primary_key=True)
    dataset_info_id = models.ForeignKey(dataset_info, on_delete=models.CASCADE)
    barcode = models.CharField(max_length=100, blank=True, null=True)
    cell_type = models.CharField(max_length=100, blank=True, null=True)
    ncount_rna = models.FloatField(blank=True,null=True)
    nfeature_rna = models.FloatField(blank=True,null=True)
    percent_mt = models.FloatField(blank=True,null=True)
    umap_1 = models.FloatField(blank=True,null=True)
    umap_2 = models.FloatField(blank=True,null=True)
    
# 基因表达量表
class gene_expression(models.Model):
    id = models.AutoField(primary_key=True)
    dataset_info = models.ForeignKey(dataset_info, on_delete=models.CASCADE)
    gene_name = models.CharField(max_length=50, blank=True, null=True)
    expression = models.JSONField(blank=True, null=True)

# 基因信息表
class gene_info(models.Model):
    id = models.AutoField(primary_key=True)
    gene_name = models.CharField(max_length=50)
    gene_ensg = models.CharField(max_length=50, blank=True, null=True)
    gene_annotation = models.TextField(blank=True, null=True)
    
    