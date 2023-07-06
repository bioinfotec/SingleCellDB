from django.db import models


# class GseInfo(models.Model):
#     gse_number = models.CharField(max_length=20)
#     gse_date = models.DateField()
#     gse_title = models.CharField(max_length=200)
#     gse_organism = models.CharField(max_length=100)
#     gse_exper = models.CharField(max_length=100)
#     gse_sum = models.TextField()
#     gse_design = models.TextField()

#     def __str__(self):
#         return self.gse_number


class TranMeta(models.Model):
    data_id = models.AutoField(primary_key=True)
    cell_barcode = models.CharField(max_length=255)
    cell_type = models.CharField(max_length=255)
    zone = models.CharField(max_length=255)
    run_id = models.CharField(max_length=255)
    time_point = models.IntegerField()
    umap_x = models.FloatField()
    umap_y = models.FloatField()

    def __str__(self):
        return self.cell_barcode


class DataSetMeta(models.Model):
    dataset_id = models.CharField(primary_key=True, max_length=100)
    subdata_id = models.CharField(max_length=100, blank=True, null=True)
    dataset_design = models.TextField(blank=True, null=True)
    dataset_citation = models.TextField(blank=True, null=True)
    data_platform = models.CharField(max_length=100, blank=True, null=True)
    data_model = models.CharField(max_length=100, blank=True, null=True)
    data_library = models.CharField(max_length=100, blank=True, null=True)
    dataset_sample = models.TextField(blank=True, null=True)

    def __self__(self):
        return self.dataset_id


class LiteratureMeta(models.Model):
    Liter_pmid = models.CharField(primary_key=True, max_length=100)
    Liter_title = models.CharField(max_length=1000, blank=True, null=True)
    Liter_abstract = models.TextField(blank=True, null=True)
    Liter_publication = models.TextField(blank=True, null=True)
    Liter_content = models.TextField(blank=True, null=True)
    Liter_data = models.TextField(blank=True, null=True)
    Sample_info = models.TextField(blank=True, null=True)
    Species = models.CharField(max_length=1000, blank=True, null=True)
    Tissue = models.CharField(max_length=1000, blank=True, null=True)
    Number_cells = models.CharField(max_length=100, blank=True, null=True)
    Cell_types = models.TextField(blank=True, null=True)
    Method = models.CharField(max_length=1000, blank=True, null=True)
    Markers = models.TextField(blank=True, null=True)
    Note = models.TextField(blank=True, null=True)

    def __self__(self):
        return self.Liter_pmid


class UploadedFile(models.Model):
    file = models.FileField(upload_to='data')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    size = models.CharField(max_length=20)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    def __self__(self):
        return self.name