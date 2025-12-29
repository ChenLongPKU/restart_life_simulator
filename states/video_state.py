"""
视频播放状态 - 改进的OpenCV音视频同步方案
"""
import pygame
import os
import cv2
import numpy as np
import threading
import time
from config import *
from ui_manager import Button, get_font

class VideoState:
    def __init__(self):
        self.video_ended = False
        self.skip_prompt_alpha = 0
        self.just_entered = True
        
        # 视频播放相关属性
        self.cap = None
        self.video_fps = 30
        self.last_frame_time = 0
        self.video_loaded = False
        self.video_path = None
        self.video_surface = None
        self.video_start_time = 0
        self.audio_started = False
        
        # 音频相关属性
        self.audio_loaded = False
        self.audio_playing = False
        self.audio_started = False
        self.audio_channel = None
        self.audio_sound = None
        
        # 同步控制
        self.frame_count = 0
        self.expected_frame_time = 0
        
        # 创建跳过按钮
        self.skip_button = Button(
            SCREEN_WIDTH - 150,
            20,
            120,
            40,
            "跳过",
            normal_color=(100, 100, 100),
            hover_color=(150, 150, 150),
            click_color=(80, 80, 80),
            text_color=COLORS["WHITE"],
            border_color=COLORS["BORDER"],
            font_size=FONT_SMALL
        )
        
        # 加载视频
        self.load_video()
    
    def load_video(self):
        """加载视频文件和音频"""
        video_path = RESOURCE_PATHS.get("video", "")
        
        if not video_path or not os.path.exists(video_path):
            print(f"视频文件不存在: {video_path}")
            return False
            
        try:
            # 使用OpenCV加载视频
            self.cap = cv2.VideoCapture(video_path)
            if not self.cap.isOpened():
                print("无法打开视频文件")
                return False
                
            # 获取视频属性
            self.video_fps = self.cap.get(cv2.CAP_PROP_FPS)
            self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            # 确保FPS有效
            if self.video_fps <= 0:
                self.video_fps = 30
                
            self.video_duration = int(self.total_frames / self.video_fps * 1000)
            self.video_path = video_path
            
            # print(f"视频加载成功: {video_path}")
            # print(f"FPS: {self.video_fps}, 总帧数: {self.total_frames}, 时长: {self.video_duration}ms")
            
            # 预加载第一帧
            ret, frame = self.cap.read()
            if ret:
                self.video_surface = self.convert_frame_to_surface(frame)
                self.video_loaded = True
                
                # 尝试加载音频
                self.load_audio(video_path)
                
                return True
            else:
                print("无法读取视频第一帧")
                return False
                
        except Exception as e:
            print(f"视频加载失败: {e}")
            if self.cap:
                self.cap.release()
                self.cap = None
            return False
    
    def load_audio(self, video_path):
        """尝试加载视频中的音频"""
        try:
            # 提取音频文件路径
            audio_path = video_path.replace('.mp4', '.wav')
            
            # 如果音频文件不存在，尝试从视频中提取
            if not os.path.exists(audio_path):
                # 使用ffmpeg从视频中提取音频
                import subprocess
                cmd = ['ffmpeg', '-i', video_path, '-q:a', '0', '-map', 'a', audio_path, '-y']
                subprocess.run(cmd, check=True, capture_output=True)
                # print(f"音频提取成功: {audio_path}")
            
            # 加载音频
            self.audio_sound = pygame.mixer.Sound(audio_path)
            self.audio_loaded = True
            # print("音频加载成功")
            
        except Exception as e:
            print(f"音频加载失败: {e}")
            self.audio_loaded = False
    
    def convert_frame_to_surface(self, frame):
        """将OpenCV帧转换为Pygame Surface"""
        try:
            # 转换BGR到RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # 调整尺寸
            frame_resized = cv2.resize(frame_rgb, (SCREEN_WIDTH, SCREEN_HEIGHT))
            # 转换为Pygame Surface
            return pygame.image.frombuffer(frame_resized.tobytes(), frame_resized.shape[1::-1], "RGB")
        except Exception as e:
            print(f"帧转换失败: {e}")
            return None
    
    def get_next_frame(self):
        """获取下一帧视频"""
        if self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                return self.convert_frame_to_surface(frame)
            else:
                # 视频播放结束
                self.video_ended = True
                self.cap.release()
                # 停止音频
                if self.audio_loaded and self.audio_playing:
                    self.audio_channel.stop()
                    self.audio_playing = False
        return None
    
    def start_audio(self):
        """开始播放音频"""
        if self.audio_loaded and not self.audio_playing and not self.audio_started:
            self.audio_channel = self.audio_sound.play()
            self.audio_playing = True
            self.audio_started = True
            # print("音频开始播放")
    
    def cleanup(self):
        """清理视频和音频资源"""
        if self.cap:
            self.cap.release()
            self.cap = None
        
        # 停止音频
        if self.audio_loaded and self.audio_playing:
            self.audio_channel.stop()
            self.audio_playing = False
    
    def handle_event(self, event, ui_manager):
        """处理事件"""
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            return True
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if self.skip_button.rect.collidepoint(mouse_pos):
                ui_manager.play_click_sound()
                self.cleanup()  # 确保清理音频
                ui_manager.change_state(STATE_MENU)
                return True
                
        return False
        
    def update(self, ui_manager):
        """更新状态"""
        current_time = pygame.time.get_ticks()
        
        if self.just_entered:
            # 模拟一次鼠标释放，清除可能的按下状态
            pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONUP, 
                                               button=1, 
                                               pos=pygame.mouse.get_pos()))
            self.just_entered = False
            self.video_start_time = current_time
            self.expected_frame_time = current_time
            self.frame_count = 0
        
        # 更新跳过按钮状态
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        prev_mouse_pressed = getattr(self, 'prev_mouse_pressed', (False, False, False))
        
        self.skip_button.update(mouse_pos, mouse_pressed)
        
        # 检查跳过按钮点击
        if self.skip_button.is_clicked_now(mouse_pos, mouse_pressed, prev_mouse_pressed):
            ui_manager.play_click_sound()
            self.cleanup()  # 确保清理音频
            ui_manager.change_state(STATE_MENU)
            
        # 更新视频帧
        if self.video_loaded and not self.video_ended:
            # 控制帧率，确保视频播放流畅
            frame_interval = 1000 / self.video_fps
            
            # 如果是前3帧之后，再开始音频（给视频缓冲时间）
            if not self.audio_started and self.frame_count >= 3:
                self.start_audio()
            
            # 基于时间戳的帧同步
            elapsed_time = current_time - self.video_start_time
            expected_frame = int(elapsed_time * self.video_fps / 1000)
            
            # 如果当前帧落后于预期帧，跳过一些帧
            if self.frame_count < expected_frame - 1:
                # 跳过落后的帧
                skip_frames = expected_frame - self.frame_count - 1
                for _ in range(skip_frames):
                    ret, _ = self.cap.read()
                    if not ret:
                        break
                    self.frame_count += 1
                # print(f"跳过 {skip_frames} 帧以追赶音频")
            
            # 获取当前帧
            if current_time >= self.expected_frame_time:
                frame = self.get_next_frame()
                if frame is not None:
                    self.video_surface = frame
                    self.frame_count += 1
                    self.expected_frame_time += frame_interval
                else:
                    # 视频播放结束
                    self.video_ended = True
        else:
            # 如果没有视频，直接结束
            if not self.video_loaded:
                self.video_ended = True
            
        # 检查视频是否结束
        if self.video_ended:
            # 直接切换到主菜单
            self.cleanup()  # 确保清理音频
            ui_manager.change_state(STATE_MENU)
                
        # 更新静音按钮
        if ui_manager.mute_button.update(mouse_pos, mouse_pressed, prev_mouse_pressed):
            ui_manager.play_click_sound()
            # 控制音频静音
            if self.audio_loaded and self.audio_playing:
                if ui_manager.mute_button.is_muted:
                    self.audio_channel.set_volume(0)
                else:
                    self.audio_channel.set_volume(1.0)
                    
        # 保存当前鼠标状态
        self.prev_mouse_pressed = mouse_pressed
            
    def draw(self, screen):
        """绘制视频界面"""
        # 绘制视频
        if self.video_loaded and self.video_surface:
            screen.blit(self.video_surface, (0, 0))
        else:
            # 显示加载中或错误信息
            screen.fill((0, 0, 0))
            font = get_font(FONT_MEDIUM)
            if self.video_loaded:
                text = font.render("视频播放中...", True, (255, 255, 255))
            else:
                text = font.render("视频加载失败", True, (255, 0, 0))
            text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            screen.blit(text, text_rect)
        
        # 绘制跳过按钮
        self.skip_button.draw(screen)