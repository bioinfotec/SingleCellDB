from rest_framework import serializers
from celldb_v2.models import literature_info, dataset_info, cell_info, gene_expression, gene_info, cell_type_info, matrix_file


# 文献信息
class LiteratureInfoSerializer(serializers.ModelSerializer):
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

# 数据信息
class DatasetInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = dataset_info
        fields = ('dataset_id','dataset_url', 'used_method', 'species_name', 'tissue_name', 'cell_types',
                  'num_cells', 'markers_main', 'markers_other')
    
# 数据集-文献信息
class DatasetLiteratureSerializer(serializers.ModelSerializer):
    literature = LiteratureInfoSerializer(many=True)
    class Meta:
        model = dataset_info
        fields = ('dataset_id','dataset_url','used_method','species_name','tissue_name','cell_types','num_cells','markers_main','markers_other', 'literature',)

# 文献-数据集信息
class LiteratureDatasetSerializer(serializers.ModelSerializer):
    dataset_info_set = DatasetInfoSerializer(many=True)
    class Meta:
        model = literature_info
        fields = ('pmid','article_title','article_url','articel_abstract','articel_content', 'publication','release_time', 'dataset_info_set',)

# 细胞信息
class CellInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = cell_info
        fields = ('barcode','cell_type','orig_ident','ncount_rna','nfeature_rna','percent_mt','umap_1','umap_2',)

# 基因表达量表
class GeneExpressionSerializer(serializers.ModelSerializer):
    class Meta:
        model = gene_expression
        fields = ('gene_name','expression', 'dataset_info_id',)

# 基因信息表
class GeneInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = gene_info
        fields = ('gene_name','gene_ensg', 'gene_annotation',)
        
# 细胞类型信息
class CellTypeInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = cell_type_info
        fields = ('cell_type_name','cell_type_alias','cell_type_annotation',)
 
       
# 数据集-文献-基因表
class DatasetLiteratureGeneSerializer(serializers.ModelSerializer):
    literature = serializers.SerializerMethodField()
    gene_expression_set = serializers.SerializerMethodField()
    
    class Meta:
        model = dataset_info
        fields = ("dataset_id","species_name","literature","gene_expression_set",)
        
    def get_literature(self, obj):
        literature_pmid = obj.literature.values("pmid")
        return literature_pmid

    def get_gene_expression_set(self, obj):
        gene_name = self.context.get('gene_name')
        cell_type = self.context.get('cell_type')
        if gene_name is not None:
            gene_expression_data = obj.gene_expression_set.filter(gene_name=gene_name).values("gene_name", "cell_types")
        else:
            gene_expression_data = obj.gene_expression_set.values("cell_types")
        if cell_type is not None:
            gene_expression_data = gene_expression_data.filter(cell_types__icontains=cell_type)
        return gene_expression_data
    
# 文件上传
class UploadedMatrixFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = matrix_file
        fields = "__all__"