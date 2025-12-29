"""
选择歌手主题状态
"""
import pygame
import os
from config import *
from ui_manager import Button, get_font

class ThemeState:
    def __init__(self):
        self.background = None
        self.selected_theme = None
        self.just_entered = True  # 标记是否刚进入该状态
        
        # 加载背景图片
        if os.path.exists(RESOURCE_PATHS["theme_bg"]):
            try:
                self.background = pygame.image.load(RESOURCE_PATHS["theme_bg"])
                self.background = pygame.transform.scale(
                    self.background, (SCREEN_WIDTH, SCREEN_HEIGHT)
                )
            except:
                self.background = None
                
        # 创建歌手主题按钮
        self.theme_buttons = []
        button_width = 280  # 稍微加宽以适应多行文本
        button_height = 180  # 增加高度以适应更大的字体
        padding = 20
        
        # 计算布局 - 改为4列2行，占满整个屏幕
        cols = 4
        rows = 2
        grid_width = cols * button_width + (cols - 1) * padding
        grid_height = rows * button_height + (rows - 1) * padding
        start_x = (SCREEN_WIDTH - grid_width) // 2
        start_y = 170  # 降低起始位置，为标题留出更多空间
        
        for i, theme in enumerate(THEMES):
            row = i // cols
            col = i % cols
            
            x = start_x + col * (button_width + padding)
            y = start_y + row * (button_height + padding)
            
            # 创建多行文本内容
            button_text = f"{theme['era']}\n{theme['location']}\n{theme['gender']}"
            
            button = Button(
                x, y, button_width, button_height, button_text,
                normal_color=theme["color"],
                hover_color=tuple(min(c + 30, 255) for c in theme["color"]),
                click_color=tuple(max(c - 30, 0) for c in theme["color"]),
                text_color=COLORS["WHITE"],
                font_size=FONT_MEDIUM,  # 使用中号字体，使文字更大
                multiline=True  # 启用多行文本
            )
            self.theme_buttons.append(button)
            
        # 创建返回按钮
        self.back_button = Button(
            SCREEN_WIDTH//2 - 100,
            SCREEN_HEIGHT - 80,
            200, 50,
            "返回"
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
        
        # 更新歌手主题按钮
        for i, button in enumerate(self.theme_buttons):
            button.update(mouse_pos, mouse_pressed)
            
            if button.is_clicked_now(mouse_pos, mouse_pressed, prev_mouse_pressed):
                ui_manager.play_click_sound()
                self.selected_theme = THEMES[i]["id"]
                # print(f"选择的歌手: {THEMES[i]['name']} ({self.selected_theme})")
                
                # 这里应该调用后端生成图片
                # 临时：显示加载状态
                ui_manager.change_state("loading")
                
        # 更新返回按钮
        self.back_button.update(mouse_pos, mouse_pressed)
        if self.back_button.is_clicked_now(mouse_pos, mouse_pressed, prev_mouse_pressed):
            ui_manager.play_click_sound()
            ui_manager.change_state(STATE_UPLOAD)
            
        # 更新静音按钮
        if ui_manager.mute_button.update(mouse_pos, mouse_pressed, prev_mouse_pressed):
            ui_manager.play_click_sound()
            
        # 保存当前鼠标状态
        ui_manager.current_state.prev_mouse_pressed = mouse_pressed
        
    def draw(self, screen):
        """绘制歌手主题选择界面"""
        # 绘制背景
        if self.background:
            screen.blit(self.background, (0, 0))
        else:
            screen.fill(COLORS["BACKGROUND"])
            # 绘制渐变背景
            for i in range(SCREEN_HEIGHT):
                color_value = int(25 + (i / SCREEN_HEIGHT) * 30)
                pygame.draw.line(screen, (color_value, color_value, 40), 
                               (0, i), (SCREEN_WIDTH, i))
                
        # 绘制大标题 - 白色蓝剪影效果（参考MenuState）
        title_font = get_font(FONT_LARGE)
        title_text = "选择出身"
        title = title_font.render(title_text, True, COLORS["WHITE"])
        title_shadow = title_font.render(title_text, True, COLORS["BLUE"])
        
        # 先绘制阴影（偏移3像素），再绘制主文本
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2 + 3, 60 + 3))
        screen.blit(title_shadow, title_rect)
        
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 60))
        screen.blit(title, title_rect)
        
        # 绘制第一行小标题 - 白色蓝剪影效果
        subtitle_font = get_font(FONT_MEDIUM)
        subtitle1_text = "你发现自己穿越回了一个伟大歌手们尚未发迹的时代，也许可以借此机会一举成名！"
        subtitle1 = subtitle_font.render(subtitle1_text, True, COLORS["WHITE"])
        subtitle1_shadow = subtitle_font.render(subtitle1_text, True, COLORS["BLUE"])
        
        subtitle1_rect = subtitle1_shadow.get_rect(center=(SCREEN_WIDTH//2 + 2, 100 + 2))
        screen.blit(subtitle1_shadow, subtitle1_rect)
        
        subtitle1_rect = subtitle1.get_rect(center=(SCREEN_WIDTH//2, 100))
        screen.blit(subtitle1, subtitle1_rect)
        
        # 绘制第二行小标题 - 白色蓝剪影效果
        subtitle2_text = "选择你所重启的时代、地点以及重启后的性别"
        subtitle2 = subtitle_font.render(subtitle2_text, True, COLORS["WHITE"])
        subtitle2_shadow = subtitle_font.render(subtitle2_text, True, COLORS["BLUE"])
        
        subtitle2_rect = subtitle2_shadow.get_rect(center=(SCREEN_WIDTH//2 + 2, 130 + 2))
        screen.blit(subtitle2_shadow, subtitle2_rect)
        
        subtitle2_rect = subtitle2.get_rect(center=(SCREEN_WIDTH//2, 130))
        screen.blit(subtitle2, subtitle2_rect)
        
        # 绘制歌手主题按钮
        for button in self.theme_buttons:
            button.draw(screen)
            
        # 绘制返回按钮
        self.back_button.draw(screen)