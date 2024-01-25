import cv2  # 导入OpenCV库，用于图像处理
import numpy as np  # 导入NumPy库，用于处理大型多维数组和矩阵
import os
from os.path import isfile, join  # 用于路径操作，例如拼接路径


# 判断颜色是否在容差范围内
def is_color_match(_center_color, _target_color, _tolerance):
    return all(abs(c - t) <= _tolerance for c, t in zip(_center_color, _target_color))


# 输出裁剪后的图像，以便调试准确度
def draw_intervals(_image, _cell_interval, _color=(0, 0, 255), _thickness=1):
    """
    在图像上按指定间隔画线。

    :param _image: 裁剪后的图像。
    :param _cell_interval: 间隔大小。
    :param _color: 线的颜色，默认为红色。
    :param _thickness: 线的厚度，默认为1。
    :return: 带有间隔线的图像。
    """
    # 画水平线
    for y in range(0, _image.shape[0], _cell_interval):
        cv2.line(_image, (0, y), (_image.shape[1], y), _color, _thickness)
    # 画垂直线
    for x in range(0, _image.shape[1], _cell_interval):
        cv2.line(_image, (x, 0), (x, _image.shape[0]), _color, _thickness)
    return _image


# 输出后的图像依次绘制圆点
def draw_circle_on_cell(image, cell_center, cell_size, value, color_map={0: (0, 0, 255), 1: (255, 0, 0)}):
    """
    在指定的单元格中心绘制一个圆点。
    蓝色点为应该填充的
    红色点为不应填充的

    :param image: 要在其上绘制的图像。
    :param cell_center: 单元格的中心坐标。
    :param cell_size: 单元格的大小(宽度和高度)。
    :param value: 单元格的值，根据该值选择颜色。
    :param color_map: 值到颜色的映射。
    """
    # 计算单元格中心的坐标
    center_x = int(cell_center[0] + cell_size / 2)
    center_y = int(cell_center[1] + cell_size / 2)
    # 从映射中获取颜色
    color = color_map.get(value, (0, 255, 0))  # 默认为绿色圆点
    # 绘制圆点
    cv2.circle(image, (center_x, center_y), 5, color, -1)


# 定义一个函数来构建谜题矩阵
def build_puzzle_matrix(_image_path, _cell_interval, _target_color, _tolerance):
    """
    识别谜题图片，并存储为矩阵

    :param _image_path: 识别图片路径
    :param _cell_interval: 识别间距
    :param _target_color: 视为填充的那张图片的颜色
    :param _tolerance: 识别容差
    """
    # 读取包含谜题答案的图片
    answer_image_full = cv2.imread(_image_path, cv2.IMREAD_COLOR)
    # 检查模板图片是否正确加载谜题答案的图片
    if answer_image_full is None:
        raise ValueError("The answer image did not load correctly. Please check the file path.\n"
                         "谜题答案的图片未正确加载。请检查文件路径。")

    # 定义裁剪坐标
    crop_start = (360, 852)
    crop_end = (1050, 1540)
    # 裁剪图片，因为默认读的图片是1080p的
    answer_image = answer_image_full[crop_start[0]:crop_end[0], crop_start[1]:crop_end[1]]
    # 请保证裁剪后的图片能被间隔整除
    # print("Cropped image size:", answer_image.shape)
    # 在裁剪后的图像上按间隔画线
    answer_image_with_intervals = draw_intervals(answer_image.copy(), _cell_interval)

    # 创建一个空列表用来存放谜题的二维数组
    matrix = []
    # 通过滑动窗口的方式遍历答案图片
    for y in range(0, answer_image.shape[0], _cell_interval):
        row = []
        for x in range(0, answer_image.shape[1], _cell_interval):
            crop_img = answer_image[y:y + _cell_interval, x:x + _cell_interval]
            if crop_img.size == 0:
                raise ValueError(
                    f"Cropped image at position ({x}, {y}) is empty. Check the interval and image dimensions.\n "
                    f"({x}, {y}) 处的裁剪图像为空。检查间隔和图像尺寸。")

            # 获取裁剪图像的中心点颜色，便于调试
            center_color = crop_img[_cell_interval // 2, _cell_interval // 2]
            # print(f"Cropped image center color at ({x}, {y}): {center_color}")  # 打印中心点颜色

            # 判断中心点颜色是否与目标颜色匹配
            cell_value = 0 if is_color_match(center_color, _target_color, _tolerance) else 1

            row.append(cell_value)
            # 绘制圆点
            draw_circle_on_cell(answer_image_with_intervals, (x, y), _cell_interval, cell_value)

        if row:
            matrix.append(row)

    # 循环结束后展示最终的图像
    '''cv2.imshow('Final Image with All Circles', answer_image_with_intervals)
    cv2.waitKey(0)  # 等待直到有键被按下
    cv2.destroyAllWindows()'''

    return matrix


# 遍历图片并保存结果
def process_images_and_save_results(_folder_path, _image_prefix, _image_count, _cell_interval, _target_color, _tolerance):
    for i in range(1, _image_count + 1):
        # 构建文件名
        filename = f"{_image_prefix}{str(i).zfill(3)}.jpg"
        # 完整的文件路径
        image_path = join(_folder_path, filename)
        # 调用 build_puzzle_matrix 函数处理图片
        matrix = build_puzzle_matrix(image_path, _cell_interval, _target_color, _tolerance)
        # 将列表转换为 NumPy 数组
        matrix_array = np.array(matrix)
        # 将结果保存到文件中
        result_filename = f"{_image_prefix}{str(i).zfill(3)}.txt"
        result_path = join(_folder_path, result_filename)
        # 使用 numpy 保存数组到文本文件
        np.savetxt(result_path, matrix_array, fmt='%d')


# 定义目标颜色和容差
target_color = (152, 143, 145)  # 目标颜色RGB值
tolerance = 30  # 容差
# 指定存放模板图片和答案图片的文件夹路径
folder_path = 'pic\\lv2'
# 设置扫描间隔大小
cell_interval = 46
# 图片数量
image_count = 150
# 前缀
image_prefix = 'Lv2 - '

# 处理图片并保存结果
process_images_and_save_results(folder_path, image_prefix, image_count, cell_interval, target_color, tolerance)
