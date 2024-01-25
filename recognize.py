import cv2  # 导入OpenCV库，用于图像处理
import numpy as np  # 导入NumPy库，用于处理大型多维数组和矩阵
from os.path import isfile, join  # 用于路径操作，例如拼接路径


# 判断颜色是否在容差范围内
def is_color_match(center_color, target_color, tolerance):
    return all(abs(c - t) <= tolerance for c, t in zip(center_color, target_color))


# 输出裁剪后的图像，以便调试准确度
def draw_intervals(image, interval, color=(0, 0, 255), thickness=1):
    """
    在图像上按指定间隔画线。

    :param image: 裁剪后的图像。
    :param interval: 间隔大小。
    :param color: 线的颜色，默认为红色。
    :param thickness: 线的厚度，默认为1。
    :return: 带有间隔线的图像。
    """
    # 画水平线
    for y in range(0, image.shape[0], interval):
        cv2.line(image, (0, y), (image.shape[1], y), color, thickness)
    # 画垂直线
    for x in range(0, image.shape[1], interval):
        cv2.line(image, (x, 0), (x, image.shape[0]), color, thickness)
    return image


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


# 匹配图像模板
def match_template(image, template, threshold):
    # 使用OpenCV的matchTemplate功能进行模板匹配，这里选择了归一化的相关系数匹配方法
    result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
    # 从匹配结果中找到最大值及其位置
    try:
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        # 识别阈值
        if max_val >= threshold:
            return True
        return False
    except Exception as e:
        print(f"An error occurred: {e}")


# 定义一个函数来构建谜题矩阵
def build_puzzle_matrix(path, interval, color, tol, threshold):
    """
    识别谜题图片，并存储为矩阵

    :param path: 识别图片路径
    :param interval: 识别间距
    :param color: 视为填充的那张图片的颜色
    :param tol: 识别容差
    :param threshold: 识别的阈值比例
    """
    # 读取包含谜题答案的图片
    answer_image_full = cv2.imread(join(path, 'ans/answer.jpg'), cv2.IMREAD_COLOR)
    # 检查模板图片是否正确加载谜题答案的图片
    if answer_image_full is None:
        raise ValueError("The answer image did not load correctly. Please check the file path.\n"
                         "谜题答案的图片未正确加载。请检查文件路径。")

    # 定义裁剪坐标
    crop_start = (360, 850)
    crop_end = (1050, 1540)
    # 裁剪图片，因为默认读的图片是1080p的
    answer_image = answer_image_full[crop_start[0]:crop_end[0], crop_start[1]:crop_end[1]]
    # 请保证裁剪后的图片能被间隔整除
    print("Cropped image size:", answer_image.shape)
    # 在裁剪后的图像上按间隔画线
    answer_image_with_intervals = draw_intervals(answer_image.copy(), interval)

    # 创建一个空列表用来存放谜题的二维数组
    matrix = []
    # 通过滑动窗口的方式遍历答案图片
    for y in range(0, answer_image.shape[0], interval):
        row = []
        for x in range(0, answer_image.shape[1], interval):
            crop_img = answer_image[y:y + interval, x:x + interval]
            if crop_img.size == 0:
                raise ValueError(
                    f"Cropped image at position ({x}, {y}) is empty. Check the interval and image dimensions.\n "
                    f"({x}, {y}) 处的裁剪图像为空。检查间隔和图像尺寸。")

            # 获取裁剪图像的中心点颜色，便于调试
            center_color = crop_img[interval // 2, interval // 2]
            print(f"Cropped image center color at ({x}, {y}): {center_color}")  # 打印中心点颜色

            # 判断中心点颜色是否与目标颜色匹配
            cell_value = 0 if is_color_match(center_color, target_color, tolerance) else 1

            row.append(cell_value)
            # 绘制圆点
            draw_circle_on_cell(answer_image_with_intervals, (x, y), interval, cell_value)

        if row:
            matrix.append(row)

    # 循环结束后展示最终的图像
    cv2.imshow('Final Image with All Circles', answer_image_with_intervals)
    cv2.waitKey(0)  # 等待直到有键被按下
    cv2.destroyAllWindows()

    return matrix


# 定义目标颜色和容差
target_color = (152, 143, 145)  # 目标颜色RGB值
tolerance = 20  # 容差
threshold_ratio = 0.6  # 阈值比例

# 指定存放模板图片和答案图片的文件夹路径
folder_path = 'pic'
# 设置扫描间隔大小
cell_interval = 46
# 使用定义好的函数构建谜题矩阵
puzzle_matrix = build_puzzle_matrix(folder_path, cell_interval, target_color, tolerance, threshold_ratio)
# 打印谜题矩阵，以便查看和调试
print(np.array(puzzle_matrix))
