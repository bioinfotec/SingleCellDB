from rest_framework import serializers
from celldb.models import TranMeta, DataSetMeta, LiteratureMeta,UploadedFile


class TranMetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TranMeta
        fields = "__all__"
    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

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
