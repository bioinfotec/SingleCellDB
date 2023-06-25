from rest_framework import serializers
from celldb.models import TranMeta, DataSetMeta


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
