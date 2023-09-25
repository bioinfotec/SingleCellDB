from celldb_v2.models import literature_info, dataset_info, cell_info, matrix_file


def sidebar_data(request):
    pmids = literature_info.objects.all().values_list("pmid", flat=True).distinct()
    dataset_ids = matrix_file.objects.all().values_list("data_id", flat=True).distinct()
    species = dataset_info.objects.all().values_list("species_name", flat=True).distinct()
    cell_types = cell_info.objects.all().values_list("cell_type", flat=True).distinct()
    context = {"pmids": pmids, "species": species, "cell_types": cell_types, "dataset_ids": dataset_ids,}
    return context