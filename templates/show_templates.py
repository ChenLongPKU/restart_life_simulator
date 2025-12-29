"""
展示模板定义
"""

class SlideShowItem:
    """单次展示的内容模板"""
    def __init__(self, 
                 background_image: str,      # 背景图片路径
                 audio_file: str,            # 音频文件路径
                 cover_image: str,           # 专辑封面图片路径
                 description: str,          # 介绍文字
                 display_duration: int = 5000,  # 展示时长(毫秒)
                 music_duration: int = 1000,    # 音乐开始播放到动画开始的间隔
                 animate_duration: int = 2000): # 动画持续时间
        self.background_image = background_image
        self.audio_file = audio_file
        self.cover_image = cover_image
        self.description = description
        self.display_duration = display_duration
        self.music_duration = music_duration
        self.animate_duration = animate_duration

class ThemeShow:
    """一个风格对应的所有展示模板"""
    def __init__(self, theme_id: str, theme_name: str):
        self.theme_id = theme_id
        self.theme_name = theme_name
        self.slides = []  # SlideShowItem列表
        self.current_slide_index = 0
    
    def add_slide(self, slide_item: SlideShowItem):
        """添加一个展示项"""
        self.slides.append(slide_item)
    
    def get_current_slide(self):
        """获取当前展示项"""
        if self.slides and 0 <= self.current_slide_index < len(self.slides):
            return self.slides[self.current_slide_index]
        return None
    
    def next_slide(self):
        """切换到下一个展示项"""
        if self.current_slide_index < len(self.slides) - 1:
            self.current_slide_index += 1
            return True
        return False
    
    def reset(self):
        """重置到第一个展示项"""
        self.current_slide_index = 0