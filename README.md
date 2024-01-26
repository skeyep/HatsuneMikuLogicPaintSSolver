# HatsuneMikuLogicPaintSSolver 😺🎶

![Header](https://github.com/skeyep/HatsuneMikuLogicPaintSSolver/blob/main/pic/header.jpg)

一个能自动完成《Hatsune Miku Logic Paint S》游戏中的解谜过程的脚本。

A script that automates the process of solving puzzles in the Hatsune Miku Logic Paint S game.

## 概述 / Overview

HatsuneMikuLogicPaintSSolver 是一个基于Python的自动化工具，旨在识别谜题图案并填充它们以完成《Hatsune Miku Logic Paint S》游戏中的谜题。该工具利用计算机视觉来处理图像并存储正确答案。

HatsuneMikuLogicPaintSSolver is a Python-based automation tool designed to recognize puzzle patterns and fill them in to complete puzzles from the Hatsune Miku Logic Paint S game. This tool utilizes computer vision techniques to process images and save the correct answers.

## 特点 / Features

- 图像识别谜题答案图片 📸
- - Image recognition for puzzle answer image 📸
- 自动化解谜逻辑 🧠
- - Automated puzzle solving logic 🧠
- 可定制参数，适应不同谜题大小和复杂性 🔧
- - Customizable parameters for different puzzle sizes and complexities 🔧
- 解题过程的可视化 🖼️
- - Visualization of the solving process 🖼️

## 先决条件 / Prerequisites

在开始之前，请确保您满足以下要求： 

Before you begin, ensure you have met the following requirements:

- Python 3.10.7 🐍
- OpenCV library 📚
- NumPy library 🔢
- Pynput library 🖱️
- Pygetwindow library 🪟

## 安装 / Installation

克隆仓库到您的本地机器：

Clone the repository to your local machine:

```bash
git clone https://github.com/your-github-username/HatsuneMikuLogicPaintSSolver.git
```

导航到克隆的目录并安装必要的Python包：

Navigate to the cloned directory and install the necessary Python packages:

```bash
pip install -r requirements.txt
```

## 使用方法 / Usage

要使用 HatsuneMikuLogicPaintSSolver，请按照以下步骤操作：

To use HatsuneMikuLogicPaintSSolver, follow these steps:

- 更新 `run.py` 文件，为您的谜题图像设置适当的参数。最重要的，就是更新`chapter`、`total_level`、`starting_level`.
- - Update the `run.py` file with the appropriate settings for your puzzle image. The most important thing is to update `chapter`、`total_level`、`starting_level`.
- 将游戏打开至`关卡答题页面`，即可自动化答题，请使用以下命令运行脚本：
- - Open the game to the `Level Answer Page` to automatically answer questions. Run the script with the following command:

```bash
python run.py
```
<div align="center">Level Answer Page</div>

![Level Answer Page](https://github.com/skeyep/HatsuneMikuLogicPaintSSolver/blob/main/pic/answer%20page.png)

## 贡献者 / Contributors

感谢以下为该项目做出贡献的人：

Thanks to the following people who have contributed to this project:

- Skeyep 🌟

## 联系方式 / Contact

如果您想联系我，可以通过 _skeyep@qq.com_ 找到我。 📧

If you want to contact me you can reach me at _skeyep@qq.com_. 📧