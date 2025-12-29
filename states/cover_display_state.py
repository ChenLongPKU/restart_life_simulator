"""
专辑封面展示状态
"""
import pygame
import os
from config import *
from ui_manager import Button, get_font

class CoverDisplayState:
    def __init__(self):
        self.theme_show = None
        self.background_surface = None
        self.cover_surface = None
        self.audio_channel = None
        self.animation_start_time = 0
        self.current_phase = "background"  # background, cover_animation, description, waiting
        self.just_entered = True
        self.prev_mouse_pressed = (False, False, False)
        
        # 创建按钮
        self.next_button = Button(
            SCREEN_WIDTH - 150, SCREEN_HEIGHT - 150, 
            120, 50, "下一张",
            normal_color=COLORS["BLUE"],
            hover_color=(0, 150, 255),
            click_color=(0, 100, 200)
        )
        
        # 字体
        self.title_font = get_font(FONT_LARGE)
        self.desc_font = get_font(FONT_SMALL)
        self.button_font = get_font(FONT_SMALL)
        
    def set_theme_show(self, theme_show):
        """设置主题展示数据"""
        self.theme_show = theme_show
        self.current_phase = "background"
        self.load_current_slide()
        
    def load_current_slide(self):
        """加载当前展示的资源"""
        if not self.theme_show:
            return
            
        slide = self.theme_show.get_current_slide()
        if not slide:
            return
            
        # 加载背景图
        try:
            if os.path.exists(slide.background_image):
                bg_img = pygame.image.load(slide.background_image)
                self.background_surface = pygame.transform.scale(bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
            else:
                self.background_surface = self.create_default_background()
        except:
            self.background_surface = self.create_default_background()
        
        # 加载封面图
        try:
            if os.path.exists(slide.cover_image):
                cover_img = pygame.image.load(slide.cover_image)
                self.cover_surface = cover_img
                self.cover_target_size = (400, 400)
                self.cover_start_size = (600, 600)
            else:
                self.cover_surface = None
        except:
            self.cover_surface = None
        
        # 加载音频
        try:
            if self.audio_channel:
                self.audio_channel.stop()
                
            if os.path.exists(slide.audio_file):
                pygame.mixer.init()
                self.audio_channel = pygame.mixer.Sound(slide.audio_file)
                self.audio_channel.play()
        except:
            print("音频播放失败")
            self.audio_channel = None
            
        # 重置动画状态
        self.animation_start_time = pygame.time.get_ticks()
        self.current_phase = "background"
        
    def create_default_background(self):
        """创建默认背景"""
        surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        for y in range(SCREEN_HEIGHT):
            color_value = int(30 + (y / SCREEN_HEIGHT) * 50)
            pygame.draw.line(surface, (color_value, color_value, color_value + 20), 
                           (0, y), (SCREEN_WIDTH, y))
        return surface
        
    def handle_event(self, event, ui_manager):
        """处理事件"""
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            return True
            
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.cleanup()
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
            
        if not self.theme_show:
            return
            
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.animation_start_time
        slide = self.theme_show.get_current_slide()
        
        if not slide:
            return
            
        # 更新动画阶段 - 使用slide中的music_duration和animate_duration
        if self.current_phase == "background" and elapsed_time > slide.music_duration:
            self.current_phase = "cover_animation"
            self.animation_start_time = current_time
            
        elif self.current_phase == "cover_animation" and elapsed_time > slide.animate_duration:
            self.current_phase = "description"
            
        elif self.current_phase == "description" and elapsed_time > slide.display_duration:
            self.current_phase = "waiting"
            
        # 更新按钮状态
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        
        if self.current_phase in ["description", "waiting"]:
            self.next_button.update(mouse_pos, mouse_pressed)
            
            # 更新按钮文字
            if self.theme_show.current_slide_index == len(self.theme_show.slides) - 1:
                self.next_button.text = "结束"
            else:
                self.next_button.text = "继续"
                
            # 检查按钮点击
            if self.next_button.is_clicked_now(mouse_pos, mouse_pressed, self.prev_mouse_pressed):
                ui_manager.play_click_sound()
                self.next_slide(ui_manager)
                
        # 更新静音按钮
        if ui_manager.mute_button.update(mouse_pos, mouse_pressed, self.prev_mouse_pressed):
            ui_manager.play_click_sound()
            if self.audio_channel:
                if ui_manager.mute_button.is_muted:
                    self.audio_channel.set_volume(0)
                else:
                    self.audio_channel.set_volume(1.0)
                    
        self.prev_mouse_pressed = mouse_pressed
        
    def next_slide(self, ui_manager):
        """切换到下一张或结束展示"""
        if self.theme_show.next_slide():
            self.load_current_slide()
        else:
            self.cleanup()
            ui_manager.states["loading"].generated_theme_show = None
            ui_manager.change_state(STATE_THEME)
            
    def cleanup(self):
        """清理资源"""
        if self.audio_channel:
            self.audio_channel.stop()
            
    def draw(self, screen):
        """绘制展示界面"""
        if not self.theme_show or not self.background_surface:
            return
            
        screen.blit(self.background_surface, (0, 0))
        
        slide = self.theme_show.get_current_slide()
        if not slide:
            return
            
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.animation_start_time
        
        # 绘制封面动画
        if self.cover_surface and self.current_phase in ["cover_animation", "description", "waiting"]:
            if self.current_phase == "cover_animation":
                progress = min(1.0, elapsed_time / slide.animate_duration)
            else:
                progress = 1.0
                
            current_width = int(self.cover_start_size[0] - (self.cover_start_size[0] - self.cover_target_size[0]) * progress)
            current_height = int(self.cover_start_size[1] - (self.cover_start_size[1] - self.cover_target_size[1]) * progress)
            alpha = int(255 * progress)
            
            scaled_cover = pygame.transform.scale(self.cover_surface, (current_width, current_height))
            scaled_cover.set_alpha(alpha)
            
            cover_rect = scaled_cover.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(scaled_cover, cover_rect)
            
        # 绘制描述文字 - 修改为白色文字加蓝色阴影效果
        if self.current_phase in ["description", "waiting"]:
            # 使用分号分割文案
            parts = slide.description.split('；')
            lines = []
            
            for part in parts:
                # 去除每部分前后的空格
                cleaned_part = part.strip()
                if cleaned_part:  # 确保不是空字符串
                    lines.append(cleaned_part)
            
            # 计算多行文字的总高度
            line_height = self.desc_font.get_linesize()
            total_height = len(lines) * line_height
            
            # 绘制每一行文字（白色文字加蓝色阴影效果）
            for i, line in enumerate(lines):
                # 创建阴影效果（蓝色）
                line_shadow = self.desc_font.render(line, True, COLORS["BLUE"])
                # 创建前景文字（白色）
                line_foreground = self.desc_font.render(line, True, COLORS["WHITE"])
                
                # 计算文字位置
                line_rect = line_foreground.get_rect()
                line_rect.centerx = SCREEN_WIDTH // 2
                line_rect.y = (SCREEN_HEIGHT // 2 + 310) - total_height // 2 + i * line_height
                
                # 先绘制阴影（偏移3像素）
                shadow_rect = line_shadow.get_rect()
                shadow_rect.centerx = SCREEN_WIDTH // 2 + 3
                shadow_rect.y = line_rect.y + 3
                screen.blit(line_shadow, shadow_rect)
                
                # 再绘制前景文字
                screen.blit(line_foreground, line_rect)
            
        # 绘制按钮
        if self.current_phase in ["description", "waiting"]:
            self.next_button.draw(screen)
            
        # 绘制标题 - 修改为白色文字加蓝色阴影效果
        title_text = f"重启人生 - {self.theme_show.theme_name}"
        title_foreground = self.title_font.render(title_text, True, COLORS["WHITE"])
        title_shadow = self.title_font.render(title_text, True, COLORS["BLUE"])
        
        # 先绘制阴影（偏移3像素）
        shadow_rect = title_shadow.get_rect(center=(SCREEN_WIDTH // 2 + 3, 53))
        screen.blit(title_shadow, shadow_rect)
        
        # 再绘制前景文字
        title_rect = title_foreground.get_rect(center=(SCREEN_WIDTH // 2, 50))
        screen.blit(title_foreground, title_rect)