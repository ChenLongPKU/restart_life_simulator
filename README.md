# Restart Life Simulator

该项目为2025秋《图像处理》课程大作业，由陈龙和王未完成。

## 运行步骤

1. 创建运行所需的环境：
```bash
conda create -n rls python=3.11
conda activate rls
pip install pygame opencv-python numpy Pillow
conda install -c conda-forge dlib
```

2. 下载资源文件：
   - 访问 https://disk.pku.edu.cn/link/AA3C1A74DDB6B5453AB98C1C5008F5D7F0 下载 `resources.zip`
   - 将 `resources.zip` 解压，并将解压后的 `resources` 文件夹放在项目主目录下

3. 运行程序：
   - 在项目主目录下，执行以下命令：
   ```bash
   python main.py
   ```

## 项目结构

```
restart_life_simulator/
│
├── api/                    # API相关代码
│
├── resources/              # 资源文件目录
│   ├── backgrounds/        # 背景资源
│   ├── images/            # 图片资源
│   ├── models/            # 模型文件
│   ├── sounds/            # 音频资源
│   ├── templates/         # 模板文件
│   └── videos/            # 视频资源
│
├── states/                 # 状态管理相关
├── templates/              # 展示模板相关
│
├── config.py              # 配置文件
├── main.py                # 主程序入口
└── ui_manager.py          # UI管理文件
```

## 注意事项

- 请确保按照上述步骤正确放置 `resources` 文件夹
- 如果遇到依赖库安装问题，请检查Python版本（建议使用Python 3.7+）

- 项目运行时需要确保所有资源文件完整且路径正确
