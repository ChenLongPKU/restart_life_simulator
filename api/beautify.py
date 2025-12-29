"""
美颜算法API模块 - 基于dlib的人脸检测和美化算法
"""
import cv2
import numpy as np
import dlib
import os
from typing import Tuple, Dict, List, Optional

class FaceBeautifier:
    def __init__(self, predictor_path: str):
        """
        初始化美颜器
        Args:
            predictor_path: dlib人脸特征点检测模型路径
        """
        self.predictor_path = predictor_path
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(predictor_path)
        
    def detect_faces(self, image_path: str) -> Tuple[np.ndarray, List[Dict]]:
        """
        检测人脸并提取特征点
        Args:
            image_path: 图片路径
        Returns:
            (image_bgr, faces_data): 图片数据和检测到的人脸信息列表
        """
        # 读取图片
        image_bgr = cv2.imread(image_path)
        if image_bgr is None:
            raise ValueError(f"无法读取图片: {image_path}")
        
        # 转换为RGB进行检测
        image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
        faces_data = []
        
        # 检测人脸
        rects = self.detector(image_rgb, 1)
        
        for i, rect in enumerate(rects):
            # 获取68个特征点
            landmarks = np.array([[p.x, p.y] for p in self.predictor(image_rgb, rect).parts()])
            
            # 定义器官区域
            organs_points = {
                'jaw': list(range(0, 17)),
                'mouth': list(range(48, 61)),
                'nose': list(range(27, 35)),
                'left_eye': list(range(36, 42)),
                'right_eye': list(range(42, 48)),
                'left_brow': list(range(17, 22)),
                'right_brow': list(range(22, 27))
            }
            
            # 为每个器官生成遮罩
            organs_masks = {}
            for organ_name, points in organs_points.items():
                mask = self._create_organ_mask(image_bgr, landmarks[points])
                organs_masks[organ_name] = mask
            
            # 计算完整的额头区域
            mask_organs = self._combine_organ_masks(organs_masks, ['mouth', 'nose', 'left_eye', 'right_eye', 'left_brow', 'right_brow'])
            mask_nose = organs_masks['nose']
            forehead_landmarks = self._get_forehead_landmark(image_bgr, landmarks, mask_organs, mask_nose)
            
            organs_points['forehead'] = forehead_landmarks
            organs_masks['forehead'] = self._create_organ_mask(image_bgr, forehead_landmarks)
            
            # 整个脸部区域
            organs_points['face'] = list(range(0, 68))
            organs_masks['face'] = self._create_organ_mask(image_bgr, landmarks)
            
            face_data = {
                'index': i,
                'rect': rect,
                'landmarks': landmarks,
                'organs_points': organs_points,
                'organs_masks': organs_masks
            }
            
            faces_data.append(face_data)
        
        return image_bgr, faces_data
    
    def _combine_organ_masks(self, organs_masks, organ_names):
        """合并器官遮罩"""
        combined_mask = np.zeros(organs_masks[list(organs_masks.keys())[0]].shape, dtype=np.float64)
        for name in organ_names:
            if name in organs_masks:
                combined_mask = np.maximum(combined_mask, organs_masks[name])
        return combined_mask
    
    def _get_forehead_landmark(self, im_bgr: np.ndarray, face_landmark: np.ndarray, 
                              mask_organs: np.ndarray, mask_nose: np.ndarray) -> np.ndarray:
        """
        完整的额头区域检测（基于椭圆模型和肤色检测）
        """
        # 画椭圆定位额头大致区域
        radius = (np.linalg.norm(face_landmark[0] - face_landmark[16]) / 2).astype('int32')
        center_abs = tuple(((face_landmark[0] + face_landmark[16]) / 2).astype('int32'))
        
        angle = np.degrees(np.arctan((face_landmark[16] - face_landmark[0])[1] / 
                                   (face_landmark[16] - face_landmark[0])[0])).astype('int32')
        
        mask = np.zeros(mask_organs.shape[:2], dtype=np.float64)
        cv2.ellipse(mask, center_abs, (radius, radius), angle, 180, 360, 1, -1)
        
        # 剔除与五官重合部分
        mask[mask_organs > 0] = 0
        
        # 根据鼻子的肤色判断真正的额头面积
        index_bool = []
        for ch in range(3):
            nose_pixels = im_bgr[:, :, ch][mask_nose > 0]
            if len(nose_pixels) > 0:
                mean, std = np.mean(nose_pixels), np.std(nose_pixels)
                up, down = mean + 0.5 * std, mean - 0.5 * std
                index_bool.append((im_bgr[:, :, ch] < down) | (im_bgr[:, :, ch] > up))
            else:
                index_bool.append(np.zeros(im_bgr.shape[:2], dtype=bool))
        
        if index_bool:
            index_zero = ((mask > 0) & index_bool[0] & index_bool[1] & index_bool[2])
            mask[index_zero] = 0
        
        # 获取额头区域的凸包
        index_abs = np.array(np.where(mask > 0)[::-1]).transpose()
        if len(index_abs) > 0:
            landmark = cv2.convexHull(index_abs).squeeze()
        else:
            # 如果检测失败，使用简化方法作为备选
            points = face_landmark[[17, 18, 19, 20, 21, 22, 23, 24, 25, 26]]
            landmark = points.copy()
            landmark[:, 1] = landmark[:, 1] - (points[:, 1].max() - points[:, 1].min()) * 0.5
        
        return landmark.astype(np.int32)
    
    def _create_organ_mask(self, image_bgr: np.ndarray, points: np.ndarray) -> np.ndarray:
        """创建器官遮罩"""
        mask = np.zeros(image_bgr.shape[:2], dtype=np.uint8)
        
        if len(points) > 2:
            # 创建凸包
            hull = cv2.convexHull(points.astype(np.int32))
            cv2.fillConvexPoly(mask, hull, 255)
        
        # 高斯模糊使边缘柔和
        mask = cv2.GaussianBlur(mask, (15, 15), 0)
        return mask
    
    def apply_beautify(self, image_bgr: np.ndarray, faces_data: List[Dict], 
                      whitening: float = 0, smoothing: float = 0, 
                      bright_eyes: float = 0, red_lips: float = 0) -> np.ndarray:
        """
        应用美颜效果
        Args:
            image_bgr: 原始BGR图像
            faces_data: 人脸检测数据
            whitening: 美白程度 0-100
            smoothing: 磨皮程度 0-100  
            bright_eyes: 亮眼程度 0-100
            red_lips: 红唇程度 0-100
        Returns:
            美化后的BGR图像
        """
        result_image = image_bgr.copy()
        
        for face_data in faces_data:
            # 美白处理
            if whitening > 0:
                result_image = self._apply_whitening(result_image, face_data, whitening)
            
            # 磨皮处理
            if smoothing > 0:
                result_image = self._apply_smoothing(result_image, face_data, smoothing)
            
            # 亮眼处理
            if bright_eyes > 0:
                result_image = self._apply_bright_eyes(result_image, face_data, bright_eyes)
            
            # 红唇处理
            if red_lips > 0:
                result_image = self._apply_red_lips(result_image, face_data, red_lips)
        
        return result_image
    
    def _apply_whitening(self, image_bgr: np.ndarray, face_data: Dict, intensity: float) -> np.ndarray:
        """应用美白效果 - 修复额头和眉毛之间的黑线问题"""
        intensity = intensity / 100.0
        
        # 转换为HSV空间进行美白处理
        image_hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)
        
        # 获取脸部遮罩（包含额头）
        if 'face' in face_data['organs_masks']:
            mask_face = face_data['organs_masks']['face']
            
            # 获取额头遮罩（单独处理）
            mask_forehead = face_data['organs_masks'].get('forehead', np.zeros_like(mask_face))
            
            # 创建联合遮罩（脸部+额头）
            mask_combined = np.maximum(mask_face, mask_forehead)
            
            # 特别处理额头和眉毛交界处（修复黑线问题）
            if 'left_brow' in face_data['organs_masks'] and 'right_brow' in face_data['organs_masks']:
                mask_brows = np.maximum(
                    face_data['organs_masks']['left_brow'],
                    face_data['organs_masks']['right_brow']
                )
                
                # 在眉毛上方扩展5像素的区域
                kernel = np.ones((5, 5), np.uint8)
                mask_brows_extended = cv2.dilate(mask_brows, kernel, iterations=1)
                
                # 将这些区域加入美白区域
                mask_combined = np.maximum(mask_combined, mask_brows_extended)
            
            # 参考标准实现：在HSV空间调整V通道
            v_channel = image_hsv[:, :, 2].astype(np.float32)
            
            # 创建美白遮罩（更柔和的处理）
            whitening_mask = (mask_combined / 255.0 * intensity).astype(np.float32)
            
            # 应用美白：提高亮度，但保持自然过渡
            v_whitened = np.minimum(v_channel + v_channel * whitening_mask * 0.3, 255)
            
            # 根据遮罩混合原图和美白后的图像
            v_blended = v_channel * (1 - whitening_mask) + v_whitened * whitening_mask
            image_hsv[:, :, 2] = np.clip(v_blended, 0, 255).astype(np.uint8)
        
        return cv2.cvtColor(image_hsv, cv2.COLOR_HSV2BGR)
    
    def _apply_smoothing(self, image_bgr: np.ndarray, face_data: Dict, intensity: float) -> np.ndarray:
        """应用磨皮效果"""
        intensity = intensity / 100.0
        
        for organ_name in ['face', 'forehead']:
            if organ_name in face_data['organs_masks']:
                mask = face_data['organs_masks'][organ_name]
                # 双边滤波磨皮
                smoothed = cv2.bilateralFilter(image_bgr, 9, 75, 75)
                # 根据遮罩混合
                blend_mask = (mask / 255.0 * intensity).astype(np.float32)
                result = image_bgr.astype(np.float32) * (1 - blend_mask[..., None]) + \
                        smoothed.astype(np.float32) * blend_mask[..., None]
                image_bgr = np.clip(result, 0, 255).astype(np.uint8)
        
        return image_bgr
    
    def _apply_bright_eyes(self, image_bgr: np.ndarray, face_data: Dict, intensity: float) -> np.ndarray:
        """应用亮眼效果"""
        intensity = intensity / 100.0
        
        for eye_name in ['left_eye', 'right_eye']:
            if eye_name in face_data['organs_masks']:
                mask = face_data['organs_masks'][eye_name]
                # 提高眼睛区域对比度
                eye_region = image_bgr.copy()
                eye_region = cv2.convertScaleAbs(eye_region, alpha=1.0 + intensity * 0.3, beta=10 * intensity)
                # 根据遮罩混合
                blend_mask = (mask / 255.0 * intensity).astype(np.float32)
                result = image_bgr.astype(np.float32) * (1 - blend_mask[..., None]) + \
                        eye_region.astype(np.float32) * blend_mask[..., None]
                image_bgr = np.clip(result, 0, 255).astype(np.uint8)
        
        return image_bgr
    
    def _apply_red_lips(self, image_bgr: np.ndarray, face_data: Dict, intensity: float) -> np.ndarray:
        """应用红唇效果"""
        intensity = intensity / 100.0
        
        if 'mouth' in face_data['organs_masks']:
            mask = face_data['organs_masks']['mouth']
            # 增强红色通道
            b, g, r = cv2.split(image_bgr.astype(np.float32))
            r_enhanced = np.minimum(r * (1 + intensity * 0.5), 255)
            # 根据遮罩混合
            blend_mask = (mask / 255.0 * intensity).astype(np.float32)
            r_blended = r * (1 - blend_mask) + r_enhanced * blend_mask
            image_bgr = cv2.merge([b, g, r_blended]).astype(np.uint8)
        
        return image_bgr