import cv2  # 导入OpenCV库，用于图像处理
import numpy as np  # 导入NumPy库，用于处理大型多维数组和矩阵
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
def build_puzzle_matrix(_image_path, _cell_interval, _target_color, _tolerance,
                        _crop_coord, _show_final_image, _size):
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

    # 使用传入的裁剪坐标
    crop_start = (_crop_coord[0], _crop_coord[1])
    crop_end = (_crop_coord[2], _crop_coord[3])
    # 裁剪图片，因为默认读的图片是1080p的
    answer_image = answer_image_full[crop_start[0]:crop_end[0], crop_start[1]:crop_end[1]]
    # print(f"Cropped image size is {answer_image.shape}")
    # 在裁剪后的图像上按间隔画线
    answer_image_with_intervals = draw_intervals(answer_image.copy(), _cell_interval)

    # 创建一个空列表用来存放谜题的二维数组
    matrix = []
    # 通过滑动窗口的方式遍历答案图片
    for y in range(0, answer_image.shape[0], _cell_interval):
        if len(matrix) >= _size:  # 如果已经达到指定的行数，停止添加新行
            break
        row = []
        for x in range(0, answer_image.shape[1], _cell_interval):
            if len(row) >= _size:  # 如果已经达到指定的列数，停止添加新列
                break
            # 确保裁剪区域不会超出图像边界
            crop_img = answer_image[y:min(y + _cell_interval, answer_image.shape[0]),
                                    x:min(x + _cell_interval, answer_image.shape[1])]
            if crop_img.size == 0:
                raise ValueError(
                    f"Cropped image at position ({x}, {y}) is empty. Check the interval and image dimensions.\n "
                    f"({x}, {y}) 处的裁剪图像为空。检查间隔和图像尺寸。")

            # 获取裁剪图像的中心点颜色，便于调试
            # 获取裁剪图像的合法中心点颜色
            center_x = min(_cell_interval // 2, crop_img.shape[1] - 1)
            center_y = min(_cell_interval // 2, crop_img.shape[0] - 1)
            center_color = crop_img[center_y, center_x]
            # print(f"Cropped image center color at ({x}, {y}): {center_color}")  # 打印中心点颜色

            # 判断中心点颜色是否与目标颜色匹配
            cell_value = 0 if is_color_match(center_color, _target_color, _tolerance) else 1

            row.append(cell_value)
            # 绘制圆点
            draw_circle_on_cell(answer_image_with_intervals, (x, y), _cell_interval, cell_value)

        if row:
            matrix.append(row)

    # 循环结束后展示最终的图像
    if _show_final_image:
        cv2.imshow('Final Image with All Circles', answer_image_with_intervals)
        cv2.waitKey(0)  # 等待直到有键被按下
        cv2.destroyAllWindows()

    # 如果矩阵的行数少于指定的size，补齐剩余的行
    while len(matrix) < _size:
        matrix.append([0] * _size)  # 由0填充
        print("The matrix's size is less than given size.")

    return matrix


# 遍历图片并保存结果
def process_images_and_save_results(_chapter, _total_level, _cell_interval,
                                    _target_color, _tolerance, _crop_coord, _show_final_image, _size):
    for level in range(1, _total_level + 1):
        # 构建图片文件名
        image_filename = f"{_chapter} - {str(level).zfill(3)}.jpg"
        # 构建图片完整的文件路径
        image_path = join(f'pic\\{_chapter}', image_filename)
        # 调用 build_puzzle_matrix 函数处理图片
        matrix = build_puzzle_matrix(image_path, _cell_interval, _target_color, _tolerance,
                                     _crop_coord, _show_final_image, _size)
        # 将列表转换为 NumPy 数组
        matrix_array = np.array(matrix)

        # 构建结果文本文件的文件名
        file_name = f"txt\\{_chapter}\\{_chapter} - {str(level).zfill(3)}.txt"
        # 使用 numpy 保存数组到文本文件
        np.savetxt(file_name, matrix_array, fmt='%d')

