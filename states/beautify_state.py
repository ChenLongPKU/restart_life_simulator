"""
图片美化状态
"""
import pygame
import os
import cv2
from config import *
from ui_manager import Button, get_font
from api.beautify import FaceBeautifier

class BeautifyState:
    def __init__(self):
        self.original_image = None
        self.beautified_image = None
        self.just_entered = True
        self.background = None
        
        # 加载背景图片
        if os.path.exists(RESOURCE_PATHS["beautify_bg"]):
            try:
                self.background = pygame.image.load(RESOURCE_PATHS["beautify_bg"])
                self.background = pygame.transform.scale(
                    self.background, (SCREEN_WIDTH, SCREEN_HEIGHT)
                )
            except:
                self.background = None
        
        # 美颜参数
        self.whitening = 0
        self.smoothing = 0
        self.bright_eyes = 0
        self.red_lips = 0
        
        # 初始化美颜器（dlib模型作为属性）
        predictor_path = "./resources/models/shape_predictor_68_face_landmarks.dat"
        self.beautifier = FaceBeautifier(predictor_path)
        self.faces_data = None  # 存储检测到的人脸数据
        
        # 创建滑块
        self.sliders = []
        self.slider_labels = ["美白", "磨皮", "亮眼", "红唇"]
        self.slider_values = [self.whitening, self.smoothing, self.bright_eyes, self.red_lips]
        
        # 调整滑块位置和宽度
        slider_width = 250  # 宽度从300减小到250
        slider_height = 20
        slider_x = 900  # 从800调整到900，向右移动100像素
        slider_start_y = 200
        slider_spacing = 80
        
        for i in range(4):
            slider_rect = pygame.Rect(
                slider_x, 
                slider_start_y + i * slider_spacing,
                slider_width, 
                slider_height
            )
            self.sliders.append(slider_rect)
        
        # 创建按钮
        button_width = 150
        button_height = 50
        button_y = 650
        
        # 调整按钮布局
        self.back_button = Button(
            100, button_y, button_width, button_height, "返回"
        )
        
        self.next_button = Button(
            SCREEN_WIDTH - button_width - 50, button_y, button_width, button_height, "下一步",
            normal_color=COLORS["BLUE"],
            hover_color=(0, 150, 255),
            click_color=(0, 100, 200)
        )
        
        self.reset_button = Button(
            SCREEN_WIDTH//2 - button_width - 10, button_y, button_width, button_height, "重置"
        )
        
        # 修改美颜按钮为蓝色
        self.beautify_button = Button(
            SCREEN_WIDTH//2 + 10, button_y, button_width, button_height, "美颜",
            normal_color=COLORS["BLUE"],  # 改为蓝色
            hover_color=(0, 150, 255),    # 蓝色悬停效果
            click_color=(0, 100, 200)     # 蓝色点击效果
        )
        
        # 加载字体
        self.title_font = get_font(FONT_LARGE)
        self.label_font = get_font(FONT_MEDIUM)
        self.value_font = get_font(FONT_SMALL)
        
    def set_original_image(self, image_path):
        """设置原始图片并立即进行人脸检测"""
        self.original_image = image_path
        self.beautified_image = image_path
        try:
            # 加载图片用于显示
            img = pygame.image.load(image_path)
            display_width, display_height = 350, 350
            img_width, img_height = img.get_size()
            
            scale = min(display_width / img_width, display_height / img_height)
            new_width = int(img_width * scale)
            new_height = int(img_height * scale)
            
            self.original_image_display = pygame.transform.smoothscale(img, (new_width, new_height))
            self.beautified_image_display = self.original_image_display.copy()
            
            # 立即进行人脸检测（优化关键步骤）
            if os.path.exists(image_path):
                self.faces_data = self.beautifier.detect_faces(image_path)
                # print(f"检测到 {len(self.faces_data[1])} 张人脸")
            else:
                print("图片文件不存在")
                
        except Exception as e:
            print(f"加载图片或人脸检测失败: {e}")
            self.original_image = None
            self.faces_data = None
    
    def handle_event(self, event, ui_manager):
        """处理事件"""
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            return True
        return False
    
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
        prev_mouse_pressed = getattr(self, 'prev_mouse_pressed', (False, False, False))
        
        # 更新按钮状态
        self.back_button.update(mouse_pos, mouse_pressed)
        self.next_button.update(mouse_pos, mouse_pressed)
        self.reset_button.update(mouse_pos, mouse_pressed)
        self.beautify_button.update(mouse_pos, mouse_pressed)
        
        # 检查按钮点击
        if self.back_button.is_clicked_now(mouse_pos, mouse_pressed, prev_mouse_pressed):
            ui_manager.play_click_sound()
            ui_manager.change_state(STATE_UPLOAD)
            
        if self.next_button.is_clicked_now(mouse_pos, mouse_pressed, prev_mouse_pressed):
            ui_manager.play_click_sound()
            ui_manager.change_state(STATE_THEME)
            
        if self.reset_button.is_clicked_now(mouse_pos, mouse_pressed, prev_mouse_pressed):
            ui_manager.play_click_sound()
            self.reset_beautify()
            
        if self.beautify_button.is_clicked_now(mouse_pos, mouse_pressed, prev_mouse_pressed):
            ui_manager.play_click_sound()
            self.apply_beautify()
        
        # 更新滑块
        if mouse_pressed[0]:
            for i, slider in enumerate(self.sliders):
                if slider.collidepoint(mouse_pos):
                    # 计算滑块位置对应的值
                    relative_x = mouse_pos[0] - slider.x
                    value = max(0, min(100, int(relative_x / slider.width * 100)))
                    self.slider_values[i] = value
        
        # 更新美颜参数
        self.whitening = self.slider_values[0]
        self.smoothing = self.slider_values[1]
        self.bright_eyes = self.slider_values[2]
        self.red_lips = self.slider_values[3]
        
        # 更新静音按钮
        if ui_manager.mute_button.update(mouse_pos, mouse_pressed, prev_mouse_pressed):
            ui_manager.play_click_sound()
            
        # 保存当前鼠标状态
        self.prev_mouse_pressed = mouse_pressed
    
    def reset_beautify(self):
        """重置美颜效果"""
        if self.original_image_display:
            self.beautified_image_display = self.original_image_display.copy()
        self.beautified_image = self.original_image
    
    def apply_beautify(self):
        """应用美颜效果 - 使用优化后的API"""
        if self.original_image and self.faces_data:
            try:
                # 调用美颜API，传入预先检测的人脸数据
                image_bgr, faces_data_list = self.faces_data
                result_image = self.beautifier.apply_beautify(
                    image_bgr, 
                    faces_data_list,
                    whitening=self.whitening,
                    smoothing=self.smoothing,
                    bright_eyes=self.bright_eyes,
                    red_lips=self.red_lips
                )
                
                # 保存临时结果并加载显示
                temp_path = "temp/beautified_temp.jpg"
                os.makedirs("temp", exist_ok=True)
                cv2.imwrite(temp_path, result_image)
                
                # 加载美化后的图片用于显示
                img = pygame.image.load(temp_path)
                display_width, display_height = 350, 350
                img_width, img_height = img.get_size()
                
                scale = min(display_width / img_width, display_height / img_height)
                new_width = int(img_width * scale)
                new_height = int(img_height * scale)
                
                self.beautified_image_display = pygame.transform.smoothscale(img, (new_width, new_height))
                self.beautified_image = temp_path
                
                # print("美颜效果应用成功")
                
            except Exception as e:
                print(f"美颜处理失败: {e}")
                # 备用方案
                self._apply_simulated_beautify()
        else:
            print("未检测到人脸，无法应用美颜")
    
    def _apply_simulated_beautify(self):
        """模拟美颜效果（备选方案）"""
        if self.original_image_display:
            self.beautified_image_display = self.simulate_beautify(
                self.original_image_display,
                self.whitening,
                self.smoothing,
                self.bright_eyes,
                self.red_lips
            )
    
    def simulate_beautify(self, image, whitening, smoothing, bright_eyes, red_lips):
        """
        模拟美颜效果（当真实API不可用时使用）
        """
        # ... 原有的模拟代码保持不变 ...
        surface = image.copy()
        
        if whitening > 0:
            white_surface = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
            white_value = min(255, whitening * 2)
            white_surface.fill((white_value, white_value, white_value, int(whitening * 1.5)))
            surface.blit(white_surface, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
        
        if red_lips > 0:
            red_surface = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
            red_value = min(255, red_lips * 2)
            for y in range(surface.get_height() // 2, surface.get_height()):
                for x in range(surface.get_width()):
                    current_color = surface.get_at((x, y))
                    new_red = min(255, current_color[0] + red_value // 3)
                    new_green = max(0, current_color[1] - red_value // 10)
                    new_blue = max(0, current_color[2] - red_value // 10)
                    surface.set_at((x, y), (new_red, new_green, new_blue, current_color[3]))
        
        return surface
    
    def draw(self, screen):
        """绘制美化界面"""
        # 绘制背景
        if self.background:
            screen.blit(self.background, (0, 0))
        else:
            screen.fill(COLORS["BACKGROUND"])
            # 绘制深蓝色网格背景
            for i in range(0, SCREEN_WIDTH, 50):
                for j in range(0, SCREEN_HEIGHT, 50):
                    pygame.draw.circle(screen, (40, 40, 60), (i, j), 2)
        
        # 绘制标题 - 修改为"美化形象"，白字蓝剪影效果
        title_text = "美化形象"
        title = self.title_font.render(title_text, True, COLORS["WHITE"])
        title_shadow = self.title_font.render(title_text, True, COLORS["BLUE"])
        
        # 先绘制蓝色剪影（偏移）
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2 + 3, 80 + 3))
        screen.blit(title_shadow, title_rect)
        
        # 再绘制白色文字
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 80))
        screen.blit(title, title_rect)
        
        # 绘制副标题 - 修改为指定文字，白字蓝剪影效果
        subtitle_text = "在正式重启之前，你可以对自己的形象做一些美化"
        subtitle = self.label_font.render(subtitle_text, True, COLORS["WHITE"])
        subtitle_shadow = self.label_font.render(subtitle_text, True, COLORS["BLUE"])
        
        # 先绘制蓝色剪影（偏移）
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH//2 + 2, 120 + 2))
        screen.blit(subtitle_shadow, subtitle_rect)
        
        # 再绘制白色文字
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH//2, 120))
        screen.blit(subtitle, subtitle_rect)
        
        # 绘制图片预览区域
        if hasattr(self, 'original_image_display') and self.original_image_display:
            # 原图预览
            orig_x = 100
            orig_y = 180
            pygame.draw.rect(screen, COLORS["DARK_GRAY"], 
                           (orig_x-10, orig_y-10, 370, 370), border_radius=5)
            screen.blit(self.original_image_display, (orig_x, orig_y))
            
            # 原图标签
            orig_label = self.label_font.render("原图", True, COLORS["WHITE"])
            orig_label_rect = orig_label.get_rect(center=(orig_x+175, orig_y+370))
            screen.blit(orig_label, orig_label_rect)
            
            # 美化后预览
            beaut_x = 450
            beaut_y = 180
            pygame.draw.rect(screen, COLORS["DARK_GRAY"], 
                           (beaut_x-10, beaut_y-10, 370, 370), border_radius=5)
            if hasattr(self, 'beautified_image_display') and self.beautified_image_display:
                screen.blit(self.beautified_image_display, (beaut_x, beaut_y))
            
            # 美化后标签
            beaut_label = self.label_font.render("美化后", True, COLORS["WHITE"])
            beaut_label_rect = beaut_label.get_rect(center=(beaut_x+175, beaut_y+370))
            screen.blit(beaut_label, beaut_label_rect)
        else:
            # 如果没有图片，显示提示
            no_image_text = self.label_font.render("请先上传图片", True, COLORS["LIGHT_GRAY"])
            no_image_rect = no_image_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            screen.blit(no_image_text, no_image_rect)
        
        # 绘制滑块和标签
        for i, slider in enumerate(self.sliders):
            # 绘制滑块背景
            pygame.draw.rect(screen, COLORS["DARK_GRAY"], slider, border_radius=10)
            
            # 绘制滑块填充（根据当前值）
            fill_width = int(slider.width * self.slider_values[i] / 100)
            fill_rect = pygame.Rect(slider.x, slider.y, fill_width, slider.height)
            pygame.draw.rect(screen, COLORS["BLUE"], fill_rect, border_radius=10)
            
            # 绘制滑块手柄
            handle_x = slider.x + fill_width - 5
            handle_rect = pygame.Rect(handle_x-5, slider.y-5, 10, slider.height+10)
            pygame.draw.rect(screen, COLORS["WHITE"], handle_rect, border_radius=5)
            
            # 绘制标签
            label = self.label_font.render(self.slider_labels[i], True, COLORS["WHITE"])
            label_rect = label.get_rect(midright=(slider.x - 10, slider.centery))
            screen.blit(label, label_rect)
            
            # 绘制数值
            value_text = self.value_font.render(f"{self.slider_values[i]}%", True, COLORS["LIGHT_GRAY"])
            value_rect = value_text.get_rect(midleft=(slider.x + slider.width + 10, slider.centery))
            screen.blit(value_text, value_rect)
        
        # 绘制按钮
        self.back_button.draw(screen)
        self.next_button.draw(screen)
        self.reset_button.draw(screen)
        self.beautify_button.draw(screen)