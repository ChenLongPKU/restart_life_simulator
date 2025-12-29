"""
主程序入口 - 重构后的简洁版本
"""
import pygame
import sys
from config import *
from ui_manager import UIManager

# 导入各个状态
from states.video_state import VideoState
from states.menu_state import MenuState
from states.upload_state import UploadState
from states.beautify_state import BeautifyState
from states.theme_state import ThemeState
from states.loading_state import LoadingState
from states.cover_display_state import CoverDisplayState

def main():
    """主函数"""
    # 初始化pygame
    pygame.init()
    pygame.display.set_caption("重启人生模拟器")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    
    # 允许文件拖放
    pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN, pygame.DROPFILE])
    pygame.scrap.init()
    
    # 创建UI管理器
    ui_manager = UIManager(screen)
    
    # 创建并注册状态
    ui_manager.register_state(STATE_VIDEO, VideoState())
    ui_manager.register_state(STATE_MENU, MenuState())
    ui_manager.register_state(STATE_UPLOAD, UploadState())
    ui_manager.register_state(STATE_BEAUTIFY, BeautifyState())
    ui_manager.register_state(STATE_THEME, ThemeState())
    ui_manager.register_state(STATE_LOADING, LoadingState())
    ui_manager.register_state(STATE_COVER, CoverDisplayState())
    
    # 设置初始状态
    ui_manager.change_state(STATE_VIDEO)
    
    # 主循环
    running = True
    while running:
        # 处理事件
        events = pygame.event.get()
        state_changed = False
        
        for event in events:
            if event.type == pygame.QUIT:
                running = False
                continue
                    
            if event.type == pygame.DROPFILE:
                ui_manager.handle_event(event)
                    
            if ui_manager.handle_event(event):
                state_changed = True
                break
        
        if state_changed:
            continue
                    
        # 更新UI
        ui_manager.update()
        
        # 绘制
        screen.fill(COLORS["BLACK"])
        ui_manager.draw()
        
        pygame.display.flip()
        clock.tick(FPS)
        
    # 退出游戏
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()