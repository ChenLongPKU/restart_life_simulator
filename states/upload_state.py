"""
上传图片状态 - 重新设计布局
"""
import pygame
import os
import math
from config import *
from ui_manager import Button, FileUploadBox, get_font

class UploadState:
    def __init__(self):
        self.background = None
        self.selected_file = None
        self.just_entered = True
        
        # 新增：载入中状态
        self.is_loading = False
        self.loading_text = "载入中..."
        
        # 加载背景图片
        if os.path.exists(RESOURCE_PATHS["upload_bg"]):
            try:
                self.background = pygame.image.load(RESOURCE_PATHS["upload_bg"])
                self.background = pygame.transform.scale(
                    self.background, (SCREEN_WIDTH, SCREEN_HEIGHT)
                )
            except:
                self.background = None
                
        # 创建合并的上传预览框 - 右侧
        upload_width = 400
        upload_height = 400
        upload_x = SCREEN_WIDTH - upload_width - 100  # 右侧留出100px边距
        upload_y = SCREEN_HEIGHT // 2 - upload_height // 2
        
        self.upload_box = FileUploadBox(
            upload_x,
            upload_y,
            upload_width,
            upload_height,
            "上传人像图片"
        )
        
        # 创建按钮 - 放在上传框下方
        button_width = 180
        button_height = 50
        button_y = self.upload_box.rect.bottom + 20
        button_spacing = 20
        
        # 返回按钮在左
        self.back_button = Button(
            upload_x + (upload_width - button_width*2 - button_spacing) // 2,
            button_y,
            button_width,
            button_height,
            "返回主菜单"
        )
        
        # 下一步按钮在右
        self.next_button = Button(
            upload_x + (upload_width - button_width*2 - button_spacing) // 2 + button_width + button_spacing,
            button_y,
            button_width,
            button_height,
            "下一步",
            normal_color=COLORS["BLUE"],
            hover_color=(0, 150, 255),
            click_color=(0, 100, 200)
        )
        
        # 保存按钮的初始状态
        self.next_button_normal_text = "下一步"
        self.next_button_disabled_text = "请先选择图片"
        self.next_button_disabled = True
        
        # 文字说明相关
        self.title_font = get_font(FONT_LARGE)
        self.subtitle_font = get_font(FONT_MEDIUM)
        self.info_font = get_font(FONT_SMALL)
        
        # 载入中字体
        self.loading_font = get_font(FONT_MEDIUM)
        
    def reset(self):
        """重置状态"""
        self.selected_file = None
        self.next_button_disabled = True
        self.upload_box.set_file(None)
        self.is_loading = False
        
    def handle_event(self, event, ui_manager):
        """处理事件，返回是否处理了事件"""
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            return True
            
        # 处理文件拖放
        elif event.type == pygame.DROPFILE:
            file_path = event.file
            if file_path and file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                self.selected_file = file_path
                self.upload_box.set_file(file_path)
                self.next_button_disabled = False
                ui_manager.play_click_sound()
                
                # 重要：文件拖放后重置鼠标状态
                if hasattr(ui_manager.current_state, 'prev_mouse_pressed'):
                    ui_manager.current_state.prev_mouse_pressed = (False, False, False)
                return True
                    
        return False

    def update(self, ui_manager):
        """更新状态"""
        # 如果正在载入中，切换到美颜状态
        if self.is_loading:
            # 将选择的文件传递给美化状态
            if hasattr(ui_manager.states[STATE_BEAUTIFY], 'set_original_image'):
                ui_manager.states[STATE_BEAUTIFY].set_original_image(self.selected_file)
            
            self.is_loading = False
            # 切换到美颜状态
            ui_manager.change_state(STATE_BEAUTIFY)
            return
        
        # 获取鼠标状态
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        
        # 获取上一帧的鼠标状态
        if hasattr(ui_manager.current_state, 'prev_mouse_pressed'):
            prev_mouse_pressed = ui_manager.current_state.prev_mouse_pressed
        else:
            prev_mouse_pressed = (False, False, False)
            ui_manager.current_state.prev_mouse_pressed = prev_mouse_pressed
        
        # 更新组件状态
        self.upload_box.update(mouse_pos)
        
        # 只有下一步按钮不禁用时，才更新其状态
        if not self.next_button_disabled:
            self.next_button.update(mouse_pos, mouse_pressed)
        else:
            # 如果按钮被禁用，重置其状态
            self.next_button.is_hovered = False
            self.next_button.is_clicked = False
            
        self.back_button.update(mouse_pos, mouse_pressed)
        
        # 检查上传框点击
        if self.upload_box.handle_click(mouse_pos, mouse_pressed, prev_mouse_pressed):
            ui_manager.play_click_sound()
            # 打开文件选择对话框
            import tkinter as tk
            from tkinter import filedialog
            
            try:
                root = tk.Tk()
                root.withdraw()
                file_path = filedialog.askopenfilename(
                    title="选择人像图片",
                    filetypes=[("图片文件", "*.jpg *.jpeg *.png *.bmp"), ("所有文件", "*.*")]
                )
                if file_path:
                    self.selected_file = file_path
                    self.upload_box.set_file(file_path)
                    self.next_button_disabled = False
                    
                    # 重要：文件选择对话框后重置鼠标状态
                    ui_manager.current_state.prev_mouse_pressed = (False, False, False)
            except Exception as e:
                print(f"文件选择对话框错误: {e}")
                file_path = input("请输入图片路径: ").strip('"').strip("'")
                if file_path and os.path.exists(file_path) and file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                    self.selected_file = file_path
                    self.upload_box.set_file(file_path)
                    self.next_button_disabled = False
                        
        # 检查下一步按钮点击
        if not self.next_button_disabled and self.next_button.is_clicked_now(mouse_pos, mouse_pressed, prev_mouse_pressed):
            if self.selected_file and os.path.exists(self.selected_file):
                ui_manager.play_click_sound()
                # print(f"选择的文件: {self.selected_file}")
                
                # 开始载入中状态
                self.is_loading = True
                
            else:
                # 文件不存在，重置状态
                self.selected_file = None
                self.upload_box.set_file(None)
                self.next_button_disabled = True
                print("文件不存在，请重新选择")
                
        # 检查返回按钮点击
        if self.back_button.is_clicked_now(mouse_pos, mouse_pressed, prev_mouse_pressed):
            ui_manager.play_click_sound()
            # 重置状态
            self.reset()
            ui_manager.change_state(STATE_MENU)
            
        # 更新静音按钮
        if ui_manager.mute_button.update(mouse_pos, mouse_pressed, prev_mouse_pressed):
            ui_manager.play_click_sound()
            
        # 保存当前鼠标状态
        ui_manager.current_state.prev_mouse_pressed = mouse_pressed
        
    def draw(self, screen):
        """绘制上传界面"""
        # 绘制背景
        if self.background:
            screen.blit(self.background, (0, 0))
        else:
            screen.fill(COLORS["BACKGROUND"])
            # 绘制深蓝色网格背景
            for i in range(0, SCREEN_WIDTH, 50):
                for j in range(0, SCREEN_HEIGHT, 50):
                    pygame.draw.circle(screen, (40, 40, 60), (i, j), 2)
        
        # 计算左侧文字区域 - 避开圆形问号图标
        # 假设问号图标在左侧中央偏上，我们将文字放在问号下方
        left_margin = 100
        left_width = SCREEN_WIDTH // 2 - 150
        left_center_x = left_margin + left_width // 2
        
        # 绘制左侧文字说明
        # 避免遮挡问号图标，从屏幕高度的一半开始
        start_y = SCREEN_HEIGHT * 0.6  # 从屏幕60%高度开始
        
        # 第一行：大标题（带蓝色剪影的白色文字）
        title_text = "在重启之前，请决定你的形象"
        title = self.title_font.render(title_text, True, COLORS["WHITE"])
        title_shadow = self.title_font.render(title_text, True, COLORS["BLUE"])
        
        # 先绘制蓝色剪影（偏移）
        title_rect = title.get_rect(center=(left_center_x + 3, start_y + 3))
        screen.blit(title_shadow, title_rect)
        
        # 再绘制白色文字
        title_rect = title.get_rect(center=(left_center_x, start_y))
        screen.blit(title, title_rect)
        
        # 第二行：介绍部分（使用蓝色）
        subtitle_y = title_rect.bottom + 30
        subtitle_texts = [
            "上传一张人像图片，",
            "支持格式: JPG, PNG, BMP",
            "建议使用正面角度的自拍照",
            "请确保五官在图片中清晰可见，无眼镜等配饰"
        ]
        
        for i, text in enumerate(subtitle_texts):
            # 绘制蓝色剪影
            subtitle_shadow = self.subtitle_font.render(text, True, COLORS["BLUE"])
            subtitle_shadow_rect = subtitle_shadow.get_rect(center=(left_center_x + 2, subtitle_y + i * 40 + 2))
            screen.blit(subtitle_shadow, subtitle_shadow_rect)
            
            # 绘制白色文字
            subtitle_white = self.subtitle_font.render(text, True, COLORS["WHITE"])
            subtitle_rect = subtitle_white.get_rect(center=(left_center_x, subtitle_y + i * 40))
            screen.blit(subtitle_white, subtitle_rect)
            
        # 绘制上传框
        self.upload_box.draw(screen)
        
        # 绘制返回按钮
        self.back_button.draw(screen)
        
        # 绘制下一步按钮
        if not self.next_button_disabled:
            # 正常按钮
            self.next_button.text = self.next_button_normal_text
            self.next_button.draw(screen)
        else:
            # 禁用状态的按钮
            disabled_rect = self.next_button.rect.copy()
            
            # 绘制灰色背景
            pygame.draw.rect(screen, (80, 80, 80), disabled_rect, border_radius=10)
            pygame.draw.rect(screen, (100, 100, 100), disabled_rect, 2, border_radius=10)
            
            # 绘制禁用文本
            text_surf = self.next_button.font.render(self.next_button_disabled_text, True, (150, 150, 150))
            text_rect = text_surf.get_rect(center=disabled_rect.center)
            screen.blit(text_surf, text_rect)
        
        # 绘制载入中提示（在右下角）
        if self.is_loading:
            loading_surface = self.loading_font.render(self.loading_text, True, COLORS["WHITE"])
            loading_rect = loading_surface.get_rect(bottomright=(SCREEN_WIDTH - 60, SCREEN_HEIGHT - 20))
            
            # 绘制半透明背景
            bg_rect = loading_rect.inflate(20, 10)
            bg_surface = pygame.Surface(bg_rect.size, pygame.SRCALPHA)
            bg_surface.fill((0, 0, 0, 180))  # 黑色半透明背景
            screen.blit(bg_surface, bg_rect)
            
            screen.blit(loading_surface, loading_rect)