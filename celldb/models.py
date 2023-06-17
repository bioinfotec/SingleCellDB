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
    zone = models.IntegerField()
    run_id = models.CharField(max_length=255)
    time_point = models.IntegerField()
    umap_x = models.FloatField()
    umap_y = models.FloatField()

    def __str__(self):
        return self.cell_barcode
