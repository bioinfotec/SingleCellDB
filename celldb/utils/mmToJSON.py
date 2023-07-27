import json

# 跳过前三行元数据
with open("matrix.mtx", "r") as f_in:
    for _ in range(3):
        f_in.readline()

    # 读取矩阵数据并转换为JSON格式
    matrix_data = {}
    for line in f_in:
        row, col, value = map(int, line.strip().split())
        # 假设矩阵中的行和列从1开始编号
        if row not in matrix_data:
            matrix_data[row] = []
        matrix_data[row].append({col: value})

# 将JSON格式的矩阵数据写入到文件中
with open("matrix.json", "w") as f_out:
    json.dump(matrix_data, f_out, separators=(",", ":"), indent=None)