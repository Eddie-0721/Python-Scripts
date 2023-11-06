import csv
import os

def remove_columns(input_dir, output_dir):
    csv_files = [file for file in os.listdir(input_dir) if file.endswith('.csv')]

    for file in csv_files:
        input_path = os.path.join(input_dir, file)
        output_path = os.path.join(output_dir, file)

        with open(input_path, 'r', encoding='utf-8', newline='') as input_file, open(output_path, 'w', newline='') as output_file:
            reader = csv.reader(input_file)
            writer = csv.writer(output_file)

            for row in reader:
                # 删除第一列和第二列
                del row[0]
                del row[0]

                # 写入新行
                writer.writerow(row)

# 使用示例
input_directory = r'E:\test'  # 输入目录
output_directory = r'E:\output'  # 输出目录

remove_columns(input_directory, output_directory)
