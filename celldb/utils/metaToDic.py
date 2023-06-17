import csv

def get_data():
    data = []

    with open(r"/mnt/c/Users/86188/Desktop/WangJie/DB/singleCell/celldb/data/Single_cell_Meta_data.txt", 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            item = {
                "Cell_barcode": row["Cell_barcode"],
                "cell_type": row["cell_type"],
                "zone": row["zone"],
                "run_id": row["run_id"],
                "time_point": row["time_point"],
                "UMAP_X": row["UMAP_X"],
                "UMAP_Y": (row["UMAP_Y"])
            }
            data.append(item)
    return data

print(get_data())