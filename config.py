"""
配置文件和常量定义
"""
import os
import pygame

# 颜色定义
COLORS = {
    "WHITE": (255, 255, 255),
    "BLACK": (0, 0, 0),
    "GRAY": (128, 128, 128),
    "LIGHT_GRAY": (200, 200, 200),
    "DARK_GRAY": (50, 50, 50),
    "RED": (255, 0, 0),
    "GREEN": (0, 255, 0),
    "BLUE": (0, 120, 255),
    "YELLOW": (255, 255, 0),
    "PURPLE": (128, 0, 128),
    "BACKGROUND": (25, 25, 40),
    "BUTTON_NORMAL": (70, 70, 100),
    "BUTTON_HOVER": (90, 90, 130),
    "BUTTON_CLICK": (50, 50, 80),
    "TEXT": (240, 240, 240),
    "BORDER": (100, 100, 150)
}

# 屏幕尺寸
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

# 资源路径
RESOURCE_PATHS = {
    "video": "resources/videos/openingAlt.mp4",  # 视频文件
    "menu_bg": "resources/images/dooropen.png",
    "upload_bg": "resources/images/face.png",
    "beautify_bg": "resources/images/face.png",
    "theme_bg": "resources/images/albums.png",
    "loading_bg": "resources/images/guitar.png",
    "speaker_on": "resources/icons/speaker_on.png",
    "speaker_off": "resources/icons/speaker_off.png",
    "upload_icon": "resources/icons/upload.png",
    "click_sound": "resources/sounds/click.wav"
}

# 状态常量
STATE_VIDEO = "video"
STATE_MENU = "menu"
STATE_UPLOAD = "upload"
STATE_BEAUTIFY = "beautify"
STATE_THEME = "theme"
STATE_LOADING = "loading"
STATE_COVER = "cover_display"

# 字体设置
FONT_SMALL = 20  # 稍微调小以适应多行文本
FONT_MEDIUM = 28
FONT_LARGE = 42
FONT_TITLE = 56

# 字体名称
FONT_NAME = "simhei"  # 使用黑体

# 歌手主题列表 - 更新为包含时代、地点、性别信息
THEMES = [
    {"id": "adam", "name": "Adam Lambert", "era": "2000年代", "location": "美国", "gender": "男", "color": (220, 0, 0)},
    {"id": "angela", "name": "张韶涵", "era": "2000年代初", "location": "台湾", "gender": "女", "color": (0, 150, 255)},
    {"id": "faye", "name": "王菲", "era": "80年代末", "location": "香港", "gender": "女", "color": (180, 0, 180)},
    {"id": "eason", "name": "陈奕迅", "era": "90年代", "location": "香港", "gender": "男", "color": (0, 200, 100)},
    {"id": "michael", "name": "郑钧", "era": "90年代", "location": "中国大陆", "gender": "男", "color": (255, 150, 0)},
    {"id": "mj", "name": "Michael Jackson", "era": "70年代", "location": "美国", "gender": "男", "color": (150, 100, 50)},
    {"id": "gem", "name": "邓紫棋", "era": "2000年代", "location": "香港", "gender": "女", "color": (255, 100, 180)},
    {"id": "vae", "name": "许嵩", "era": "2000年代末", "location": "中国大陆", "gender": "男", "color": (100, 200, 200)},
]