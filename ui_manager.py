"""
UI管理器和基础UI组件
"""
import os
import pygame
from config import *

# 获取字体的辅助函数
def get_font(size, bold=False, italic=False):
    """获取指定大小的字体"""
    try:
        font = pygame.font.SysFont(FONT_NAME, size, bold, italic)
    except:
        # 如果黑体不可用，回退到默认字体
        font = pygame.font.SysFont(None, size, bold, italic)
    return font

class Button:
    """按钮组件"""
    def __init__(self, x, y, width, height, text, 
                 normal_color=COLORS["BUTTON_NORMAL"],
                 hover_color=COLORS["BUTTON_HOVER"],
                 click_color=COLORS["BUTTON_CLICK"],
                 text_color=COLORS["TEXT"],
                 border_color=COLORS["BORDER"],
                 border_width=2,
                 font_size=FONT_MEDIUM,
                 multiline=False):  # 添加多行文本支持
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.normal_color = normal_color
        self.hover_color = hover_color
        self.click_color = click_color
        self.text_color = text_color
        self.border_color = border_color
        self.border_width = border_width
        self.font = get_font(font_size)
        self.is_hovered = False
        self.is_clicked = False
        self.multiline = multiline  # 是否多行显示
        
    def draw(self, screen):
        """绘制按钮"""
        # 根据状态选择颜色
        if self.is_clicked:
            color = self.click_color
        elif self.is_hovered:
            color = self.hover_color
        else:
            color = self.normal_color
            
        # 绘制按钮背景
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, self.border_color, self.rect, 
                        self.border_width, border_radius=10)
        
        # 绘制文本
        if self.multiline:
            # 多行文本处理
            lines = self.text.split('\n')
            total_height = len(lines) * self.font.get_linesize()
            start_y = self.rect.centery - total_height // 2
            
            for i, line in enumerate(lines):
                text_surf = self.font.render(line, True, self.text_color)
                text_rect = text_surf.get_rect(centerx=self.rect.centerx, 
                                             y=start_y + i * self.font.get_linesize())
                screen.blit(text_surf, text_rect)
        else:
            # 单行文本处理（保持原有逻辑）
            text_surf = self.font.render(self.text, True, self.text_color)
            text_rect = text_surf.get_rect(center=self.rect.center)
            screen.blit(text_surf, text_rect)
        
    def update(self, mouse_pos, mouse_pressed):
        """更新按钮状态"""
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        self.is_clicked = self.is_hovered and mouse_pressed[0]
        
    def is_clicked_now(self, mouse_pos, mouse_pressed, prev_mouse_pressed):
        """检查按钮是否被点击（当前帧）"""
        if self.rect.collidepoint(mouse_pos):
            if mouse_pressed[0] and not prev_mouse_pressed[0]:
                return True
        return False

class ImageButton(Button):
    """带图标的按钮"""
    def __init__(self, x, y, width, height, text, icon_path=None, **kwargs):
        super().__init__(x, y, width, height, text, **kwargs)
        self.icon = None
        if icon_path and os.path.exists(icon_path):
            try:
                self.icon = pygame.image.load(icon_path)
                # 缩放图标到合适大小
                icon_size = min(width, height) - 20
                self.icon = pygame.transform.scale(self.icon, (icon_size, icon_size))
            except:
                self.icon = None
                
    def draw(self, screen):
        """绘制带图标的按钮"""
        super().draw(screen)
        
        if self.icon:
            # 计算图标位置（在文字左侧）
            icon_rect = self.icon.get_rect()
            text_surf = self.font.render(self.text, True, self.text_color)
            text_rect = text_surf.get_rect(center=self.rect.center)
            
            # 将图标放在文字左侧
            icon_rect.centery = self.rect.centery
            icon_rect.right = text_rect.left - 10
            screen.blit(self.icon, icon_rect)

class FileUploadBox:
    """文件上传框组件 - 合并了图片预览功能"""
    def __init__(self, x, y, width, height, label="上传人像图片"):
        self.rect = pygame.Rect(x, y, width, height)
        self.label = label
        self.file_path = None
        self.file_name = None
        self.image_preview = None
        self.is_hovered = False
        self.label_font = get_font(FONT_MEDIUM)
        self.hint_font = get_font(FONT_SMALL)
        
    def set_file(self, file_path):
        """设置选择的文件，并加载图片预览"""
        self.file_path = file_path
        if file_path:
            self.file_name = os.path.basename(file_path)
            # 加载图片预览
            try:
                image = pygame.image.load(file_path)
                # 计算缩放比例，保持纵横比
                image_width, image_height = image.get_size()
                
                # 计算缩放比例，使图片适应框的大小
                scale = min(
                    (self.rect.width - 40) / image_width,
                    (self.rect.height - 60) / image_height
                )
                new_width = int(image_width * scale)
                new_height = int(image_height * scale)
                
                # 缩放图片
                self.image_preview = pygame.transform.smoothscale(image, (new_width, new_height))
                
            except Exception as e:
                print(f"加载图片失败: {e}")
                self.image_preview = None
        else:
            self.file_name = None
            self.image_preview = None
        
    def draw(self, screen):
        """绘制上传框"""
        # 绘制背景
        bg_color = COLORS["DARK_GRAY"] if not self.is_hovered else COLORS["BUTTON_HOVER"]
        pygame.draw.rect(screen, bg_color, self.rect, border_radius=8)
        pygame.draw.rect(screen, COLORS["BORDER"], self.rect, 2, border_radius=8)
        
        # 绘制标签
        label_surf = self.label_font.render(self.label, True, COLORS["TEXT"])
        label_rect = label_surf.get_rect(center=(self.rect.centerx, self.rect.top - 20))
        screen.blit(label_surf, label_rect)
        
        if self.file_path and self.image_preview:
            # 显示图片预览
            preview_rect = self.image_preview.get_rect(center=self.rect.center)
            screen.blit(self.image_preview, preview_rect)
            
            # 显示文件名
            text = f"已选择: {self.file_name[:30]}"  # 限制显示长度
            text_color = COLORS["GREEN"]
            text_surf = self.hint_font.render(text, True, text_color)
            text_rect = text_surf.get_rect(center=(self.rect.centerx, self.rect.bottom - 20))
            screen.blit(text_surf, text_rect)
        else:
            # 显示上传提示
            hint_text = "点击选择图片文件"
            hint_surf = self.hint_font.render(hint_text, True, COLORS["LIGHT_GRAY"])
            hint_rect = hint_surf.get_rect(center=self.rect.center)
            screen.blit(hint_surf, hint_rect)
            
            # 绘制加号图标
            plus_size = 40
            plus_x = self.rect.centerx
            plus_y = self.rect.centery - 30
            
            # 绘制加号横线
            pygame.draw.rect(screen, COLORS["LIGHT_GRAY"], 
                           (plus_x - plus_size//2, plus_y - 2, plus_size, 4), 
                           border_radius=2)
            # 绘制加号竖线
            pygame.draw.rect(screen, COLORS["LIGHT_GRAY"], 
                           (plus_x - 2, plus_y - plus_size//2, 4, plus_size), 
                           border_radius=2)
            
    def update(self, mouse_pos):
        """更新状态"""
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
    def handle_click(self, mouse_pos, mouse_pressed, prev_mouse_pressed):
        """处理点击事件，返回是否被点击"""
        if self.rect.collidepoint(mouse_pos):
            if mouse_pressed[0] and not prev_mouse_pressed[0]:
                return True
        return False

class MuteButton:
    """静音按钮组件 - 位于左下角"""
    def __init__(self, screen_width, screen_height, size=40, padding=20):
        self.size = size
        # 修改为左下角位置
        self.rect = pygame.Rect(
            padding,  # 左边距
            screen_height - size - padding,  # 底边距
            size, size
        )
        self.is_muted = False
        self.icon_on = None
        self.icon_off = None
        
        # 加载图标
        if os.path.exists(RESOURCE_PATHS["speaker_on"]):
            self.icon_on = pygame.image.load(RESOURCE_PATHS["speaker_on"])
            self.icon_on = pygame.transform.scale(self.icon_on, (size, size))
        if os.path.exists(RESOURCE_PATHS["speaker_off"]):
            self.icon_off = pygame.image.load(RESOURCE_PATHS["speaker_off"])
            self.icon_off = pygame.transform.scale(self.icon_off, (size, size))
            
    def draw(self, screen):
        """绘制静音按钮"""
        if self.is_muted and self.icon_off:
            screen.blit(self.icon_off, self.rect)
        elif not self.is_muted and self.icon_on:
            screen.blit(self.icon_on, self.rect)
        else:
            # 如果没有图标，绘制默认图形
            if self.is_muted:
                # 绘制带红叉的喇叭
                pygame.draw.rect(screen, COLORS["GRAY"], self.rect, border_radius=5)
                # 绘制喇叭
                pygame.draw.polygon(screen, COLORS["BLACK"], [
                    (self.rect.left + 20, self.rect.top + 10),     # 右上
                    (self.rect.left + 20, self.rect.bottom - 10),  # 右下
                    (self.rect.left + 10, self.rect.bottom - 20),  # 左下
                    (self.rect.left + 10, self.rect.top + 20)      # 左上
                ])
                # 绘制红叉
                pygame.draw.line(screen, COLORS["RED"], 
                                (self.rect.left + 5, self.rect.top + 5),
                                (self.rect.right - 5, self.rect.bottom - 5), 3)
                pygame.draw.line(screen, COLORS["RED"],
                                (self.rect.left + 5, self.rect.bottom - 5),
                                (self.rect.right - 5, self.rect.top + 5), 3)
            else:
                # 绘制喇叭背景
                pygame.draw.rect(screen, COLORS["LIGHT_GRAY"], self.rect, border_radius=5)
                
                # 绘制右侧三角形（喇叭主体，开口朝左）
                pygame.draw.polygon(screen, COLORS["BLACK"], [
                    (self.rect.left + 20, self.rect.top + 10),     # 右上
                    (self.rect.left + 20, self.rect.bottom - 10),  # 右下
                    (self.rect.left + 10, self.rect.bottom - 20),  # 左下
                    (self.rect.left + 10, self.rect.top + 20)      # 左上
                ])
                
                # 绘制右侧三个竖条（从小到大）
                bar_width = 2
                bar_spacing = 1
                
                # 第一个竖条（最小）
                bar1_height = 10
                bar1_x = self.rect.left + 22
                bar1_y = self.rect.centery - bar1_height // 2
                pygame.draw.rect(screen, COLORS["BLACK"], 
                                (bar1_x, bar1_y, bar_width, bar1_height))
                
                # 第二个竖条（中等）
                bar2_height = 16
                bar2_x = bar1_x + bar_width + bar_spacing
                bar2_y = self.rect.centery - bar2_height // 2
                pygame.draw.rect(screen, COLORS["BLACK"], 
                                (bar2_x, bar2_y, bar_width, bar2_height))
                
                # 第三个竖条（最大）
                bar3_height = 22
                bar3_x = bar2_x + bar_width + bar_spacing
                bar3_y = self.rect.centery - bar3_height // 2
                pygame.draw.rect(screen, COLORS["BLACK"], 
                                (bar3_x, bar3_y, bar_width, bar3_height))
                
    def update(self, mouse_pos, mouse_pressed, prev_mouse_pressed):
        """更新按钮状态，返回是否被点击"""
        if self.rect.collidepoint(mouse_pos):
            if mouse_pressed[0] and not prev_mouse_pressed[0]:
                self.is_muted = not self.is_muted
                return True
        return False

class UIManager:
    """UI管理器"""
    def __init__(self, screen):
        self.screen = screen
        self.current_state = None
        self.states = {}
        self.mute_button = MuteButton(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.click_sound = None
        self.prev_state = None  # 记录前一个状态
        
        # 加载音效
        if os.path.exists(RESOURCE_PATHS["click_sound"]):
            try:
                pygame.mixer.init()
                self.click_sound = pygame.mixer.Sound(RESOURCE_PATHS["click_sound"])
            except:
                self.click_sound = None
                
    def register_state(self, state_name, state):
        """注册状态"""
        self.states[state_name] = state
        
    def change_state(self, state_name):
        """切换状态"""
        if state_name in self.states:
            # 重置前一个状态的标志（如果有）
            if self.current_state and hasattr(self.current_state, 'just_entered'):
                self.current_state.just_entered = False
                
            # 设置新状态的标志
            new_state = self.states[state_name]
            if hasattr(new_state, 'just_entered'):
                new_state.just_entered = True
                
            self.current_state = new_state
            return True
        return False
        
    def handle_event(self, event):
        if self.current_state:
            # 保存当前状态的引用
            old_state = self.current_state
            
            # 处理事件
            result = self.current_state.handle_event(event, self)
            
            # 检查状态是否发生变化
            if old_state != self.current_state:
                return True  # 状态已变化
                
            return result
        return False
        
    def update(self):
        """更新UI"""
        if self.current_state:
            self.current_state.update(self)
            
    def draw(self):
        """绘制UI"""
        if self.current_state:
            self.current_state.draw(self.screen)
            
        # 始终绘制静音按钮
        self.mute_button.draw(self.screen)
        
    def play_click_sound(self):
        """播放点击音效"""
        if self.click_sound and not self.mute_button.is_muted:
            self.click_sound.play()
            
    def toggle_mute(self):
        """切换静音状态"""
        self.mute_button.is_muted = not self.mute_button.is_muted