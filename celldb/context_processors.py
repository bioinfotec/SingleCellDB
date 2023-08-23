from celldb_v2.models import literature_info, dataset_info, cell_type_info


def sidebar_data(request):
    pmids = literature_info.objects.all().values_list("pmid", flat=True).distinct()
    species = dataset_info.objects.all().values_list("species_name", flat=True).distinct()
    cell_types = cell_type_info.objects.all().values_list("cell_type_name", flat=True).distinct()
    context = {"pmids": pmids, "species": species, "cell_types": cell_types}
    return context