"""
加载状态
"""
import pygame
import os
from config import *
from api.cover_generator import generate_covers

class LoadingState:
    """加载状态"""
    def __init__(self):
        self.loading_text = "正在创作歌曲..."
        self.background = None
        self.just_entered = True
        self.prev_mouse_pressed = (False, False, False)
        self.generated_theme_show = None
        
        # 加载背景图片
        if os.path.exists(RESOURCE_PATHS["loading_bg"]):
            try:
                self.background = pygame.image.load(RESOURCE_PATHS["loading_bg"])
                self.background = pygame.transform.scale(
                    self.background, (SCREEN_WIDTH, SCREEN_HEIGHT)
                )
            except:
                self.background = None
                
        # 创建字体
        self.font = pygame.font.SysFont(FONT_NAME, FONT_LARGE)
        
    def handle_event(self, event, ui_manager):
        """处理事件"""
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            return True
            
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            ui_manager.change_state(STATE_THEME)
            return True
            
        return False
        
    def update(self, ui_manager):
        """更新状态"""
        if self.just_entered:
            pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONUP, 
                                               button=1, 
                                               pos=pygame.mouse.get_pos()))
            self.just_entered = False
            
        # 生成数据
        if not self.generated_theme_show:
            # 调用API生成封面
            self.generated_theme_show = self.generate_cover_show(ui_manager)
            
        # 数据生成完成后进入展示状态
        if self.generated_theme_show:
            if "cover_display" in ui_manager.states:
                ui_manager.states["cover_display"].set_theme_show(self.generated_theme_show)
                self.generated_theme_show = None
                ui_manager.change_state("cover_display")
            else:
                ui_manager.change_state(STATE_THEME)
                
        # 更新静音按钮
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        ui_manager.mute_button.update(mouse_pos, mouse_pressed, self.prev_mouse_pressed)
        self.prev_mouse_pressed = mouse_pressed
        
    def generate_cover_show(self, ui_manager):
        """生成专辑封面展示数据"""
        # 获取当前选择的主题
        current_theme = None
        if hasattr(ui_manager.states[STATE_THEME], 'selected_theme'):
            current_theme = ui_manager.states[STATE_THEME].selected_theme
            
        # 获取美化后的图片路径
        beautified_image = None
        if hasattr(ui_manager.states[STATE_BEAUTIFY], 'beautified_image'):
            beautified_image = ui_manager.states[STATE_BEAUTIFY].beautified_image
            
        # 调用API生成封面
        return generate_covers(current_theme, beautified_image)
        
    def draw(self, screen):
        """绘制加载界面"""
        # 绘制背景
        if self.background:
            screen.blit(self.background, (0, 0))
        else:
            screen.fill(COLORS["BACKGROUND"])
            # 绘制背景图案
            for i in range(0, SCREEN_WIDTH, 50):
                for j in range(0, SCREEN_HEIGHT, 50):
                    pygame.draw.circle(screen, (40, 40, 60), (i, j), 2)
        
        # 绘制加载文本（白色蓝底效果，与menu_state一致）
        text = self.font.render(self.loading_text, True, COLORS["WHITE"])
        text_shadow = self.font.render(self.loading_text, True, COLORS["BLUE"])
        
        text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        shadow_rect = text_shadow.get_rect(center=(SCREEN_WIDTH//2 + 3, SCREEN_HEIGHT//2 + 3))
        
        screen.blit(text_shadow, shadow_rect)
        screen.blit(text, text_rect)