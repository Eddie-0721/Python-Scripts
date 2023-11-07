# Python-Scripts 20231103
about python

# sftp_wget.sh 20231103
使用wget获取sftp文件服务器中的指定文件。

# remove_columns.py 20231106
处理csv中的列（删除目录下所有csv中的第一列和第二列）。
1. os.listdir(input_dir)：使用 os 模块的 listdir 函数列出指定目录 input_dir 中的所有文件和文件夹。
2. file.endswith('.csv')：对于列出的每个文件名 file，使用 endswith 方法检查它是否以 .csv 结尾。如果是，则返回 True，否则返回 False。
3. [file for file in os.listdir(input_dir) if file.endswith('.csv')]：使用列表推导式，将满足条件的文件名添加到列表中，形成一个包含所有以 .csv 结尾的文件名的列表。
4. 因此，csv_files 变量将包含指定目录 input_dir 中所有以 .csv 结尾的文件的文件名列表。


