from rest_framework import serializers
from celldb_v2.models import literature_info, literature_dataset, dataset_info


class literature_info_serializer(serializers.ModelSerializer):
    class Meta:
        model = literature_info
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
                
class dataset_info_serializer(serializers.ModelSerializer):
    class Meta:
        model = dataset_info
        fileds = "__all__"

class literature_dataset_serializer(serializers.ModelSerializer):
    literature = literature_info_serializer(many=True, read_only=True)
    dataset = dataset_info_serializer(many=True, read_only=True)
    class Meta:
        model = literature_dataset
        fields = "__all__"

