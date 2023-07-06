from rest_framework import serializers
from celldb.models import TranMeta, DataSetMeta, LiteratureMeta,UploadedFile


class TranMetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TranMeta
        fields = (
            "data_id",
            "cell_barcode",
            "cell_type",
            "zone",
            "run_id",
            "time_point",
            "umap_x",
            "umap_y",
        )


class DataSetMetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSetMeta
        fields = "__all__"
        
class LiteratureMetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = LiteratureMeta
        fields = "__all__"
        
class UploadedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = "__all__"
