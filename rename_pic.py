import os


def rename_files(directory, prefix, start_number=1):
    # 获取指定目录下的所有文件
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

    # 初始化计数器
    count = start_number

    # 遍历所有文件
    for filename in files:
        # 构造新的文件名
        new_filename = f"{prefix}{str(count).zfill(3)}.jpg"
        # 构造旧文件的完整路径
        old_file = os.path.join(directory, filename)
        # 构造新文件的完整路径
        new_file = os.path.join(directory, new_filename)
        # 重命名文件
        os.rename(old_file, new_file)
        # 打印出更改后的文件名，这一步是可选的
        print(f'Renamed "{filename}" to "{new_filename}"')
        # 增加计数器
        count += 1


# 在这里修改需要重命名的图片文件名
rename_files('pic/Special', 'Special - ', 1)
