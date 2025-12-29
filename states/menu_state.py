"""
主菜单状态
"""
import pygame
import os
from config import *
from ui_manager import Button, get_font

class MenuState:
    def __init__(self):
        self.background = None
        self.title_font = get_font(FONT_TITLE)
        self.button_font = get_font(FONT_MEDIUM)
        self.just_entered = True  # 标记是否刚进入该状态
        
        # 加载背景图片
        if os.path.exists(RESOURCE_PATHS["menu_bg"]):
            try:
                self.background = pygame.image.load(RESOURCE_PATHS["menu_bg"])
                self.background = pygame.transform.scale(
                    self.background, (SCREEN_WIDTH, SCREEN_HEIGHT)
                )
            except:
                self.background = None
                
        # 创建按钮
        button_width = 300
        button_height = 70
        center_x = SCREEN_WIDTH // 2
        start_y = SCREEN_HEIGHT // 2
        
        self.start_button = Button(
            center_x - button_width // 2,
            start_y,
            button_width,
            button_height,
            "开始重启",
            normal_color=COLORS["BLUE"],
            hover_color=(0, 150, 255),
            click_color=(0, 100, 200)
        )
        
        self.quit_button = Button(
            center_x - button_width // 2,
            start_y + button_height + 20,
            button_width,
            button_height,
            "退出程序",
            normal_color=COLORS["BUTTON_NORMAL"],
            hover_color=COLORS["BUTTON_HOVER"],
            click_color=COLORS["BUTTON_CLICK"]
        )
        
    def handle_event(self, event, ui_manager):
        """处理事件，返回是否处理了事件"""
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            return True
            
        return False  # 事件未处理
        
    def update(self, ui_manager):
        """更新状态"""

        if self.just_entered:
            # 模拟一次鼠标释放，清除可能的按下状态
            pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONUP, 
                                               button=1, 
                                               pos=pygame.mouse.get_pos()))
            self.just_entered = False

        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        prev_mouse_pressed = ui_manager.current_state.prev_mouse_pressed if hasattr(ui_manager.current_state, 'prev_mouse_pressed') else (False, False, False)
        
        # 更新按钮状态
        self.start_button.update(mouse_pos, mouse_pressed)
        self.quit_button.update(mouse_pos, mouse_pressed)
        
        # 检查按钮点击
        if self.start_button.is_clicked_now(mouse_pos, mouse_pressed, prev_mouse_pressed):
            ui_manager.play_click_sound()
            ui_manager.change_state(STATE_UPLOAD)
            
        if self.quit_button.is_clicked_now(mouse_pos, mouse_pressed, prev_mouse_pressed):
            ui_manager.play_click_sound()
            pygame.quit()
            exit()
            
        # 更新静音按钮
        if ui_manager.mute_button.update(mouse_pos, mouse_pressed, prev_mouse_pressed):
            ui_manager.play_click_sound()
            
        # 保存当前鼠标状态
        ui_manager.current_state.prev_mouse_pressed = mouse_pressed
        
    def draw(self, screen):
        """绘制主菜单"""
        # 绘制背景
        if self.background:
            screen.blit(self.background, (0, 0))
        else:
            screen.fill(COLORS["BACKGROUND"])
            # 绘制背景图案
            for i in range(0, SCREEN_WIDTH, 50):
                for j in range(0, SCREEN_HEIGHT, 50):
                    pygame.draw.circle(screen, (40, 40, 60), (i, j), 2)
                    
        # 绘制标题
        title = self.title_font.render("重启人生模拟器", True, COLORS["WHITE"])
        title_shadow = self.title_font.render("重启人生模拟器", True, COLORS["BLUE"])
        
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2 + 3, SCREEN_HEIGHT//4 + 3))
        screen.blit(title_shadow, title_rect)
        
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//4))
        screen.blit(title, title_rect)
        
        # 绘制副标题（白色蓝剪影效果）
        subtitle_font = get_font(FONT_MEDIUM)
        subtitle_text = "你穿越到了过去，是时候重启命运，改写人生了！"
        subtitle = subtitle_font.render(subtitle_text, True, COLORS["WHITE"])
        subtitle_shadow = subtitle_font.render(subtitle_text, True, COLORS["BLUE"])
        
        subtitle_rect = subtitle_shadow.get_rect(center=(SCREEN_WIDTH//2 + 2, SCREEN_HEIGHT//4 + 62))
        screen.blit(subtitle_shadow, subtitle_rect)
        
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//4 + 60))
        screen.blit(subtitle, subtitle_rect)
        
        # 绘制按钮
        self.start_button.draw(screen)
        self.quit_button.draw(screen)