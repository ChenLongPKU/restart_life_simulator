"""
封面生成API调用 - 适配歌手主题
"""
import os
import cv2
import dlib
import numpy as np
from pathlib import Path
from templates.theme_shows import get_theme_show


def get_landmarks(im, detector, predictor):
    """返回 dlib landmarks（numpy.matrix，shape (68,2)），若未检测到或检测到多个脸会抛异常"""
    rects = detector(im, 1)
    # if len(rects) > 1:
    #     print("检测到多张人脸，无法处理")
    # if len(rects) == 0:
    #     print("未检测到人脸，无法处理")
    return np.matrix([[p.x, p.y] for p in predictor(im, rects[0]).parts()])

def transformation_from_points(points1, points2):
    """
    计算仿射变换矩阵（3x3）使 points1 对齐到 points2
    points1/points2: numpy.matrix 或 numpy.array (N,2)
    """
    points1 = points1.astype(np.float64)
    points2 = points2.astype(np.float64)

    c1 = np.mean(points1, axis=0)
    c2 = np.mean(points2, axis=0)
    points1 -= c1
    points2 -= c2

    s1 = np.std(points1)
    s2 = np.std(points2)
    points1 /= s1
    points2 /= s2

    # SVD
    U, S, Vt = np.linalg.svd(points1.T * points2)
    R = (U * Vt).T

    # 构造 3x3 仿射矩阵
    M = np.vstack([
        np.hstack(((s2 / s1) * R, c2.T - (s2 / s1) * R * c1.T)),
        np.matrix([0., 0., 1.])
    ])
    return M

def draw_convex_hull(im, points, color):
    points = cv2.convexHull(points)
    cv2.fillConvexPoly(im, points, color=color)

def get_face_mask(im, landmarks):
    """
    返回与 im 相同宽高的三通道 float mask，取值大致在 [0,1]
    landmarks: numpy.matrix (68,2)
    """

    feather_amount = 11

    # landmark 索引定义
    face_points = list(range(17, 68))
    mouth_points = list(range(48, 61))
    right_brow_points = list(range(17, 22))
    left_brow_points = list(range(22, 27))
    right_eye_points = list(range(36, 42))
    left_eye_points = list(range(42, 48))
    nose_points = list(range(27, 35))
    jaw_points = list(range(0, 17))

    # 用于生成 mask 的区域
    # overlay_points = [
    #     left_eye_points + right_eye_points + left_brow_points + right_brow_points,
    #     nose_points + mouth_points,
    # ]
    # overlay_points = [
    #     left_eye_points + right_eye_points,
    #     nose_points + mouth_points,
    # ]
    overlay_points = [
        left_eye_points,
        right_eye_points,
        nose_points,
        mouth_points,
    ]

    im_mask = np.zeros(im.shape[:2], dtype=np.float64)
    for group in overlay_points:
        draw_convex_hull(im_mask, np.array(landmarks[group], dtype=np.int32), color=1)
    im_mask = np.array([im_mask, im_mask, im_mask]).transpose((1, 2, 0))
    # feather / blur
    feather = feather_amount if feather_amount % 2 == 1 else feather_amount + 1
    im_mask = (cv2.GaussianBlur(im_mask, (feather, feather), 0) > 0) * 1.0
    im_mask = cv2.GaussianBlur(im_mask, (feather, feather), 0)
    return im_mask

def warp_im(im, M, dshape):
    """
    使用仿射 M 将 im warp 到 dshape（h,w,channels）
    M: 3x3 矩阵（numpy.matrix 或 array）
    """
    output_im = np.zeros(dshape, dtype=im.dtype)
    M2 = np.array(M[:2])  # warpAffine 需要 2x3 ndarray
    cv2.warpAffine(im, M2, (dshape[1], dshape[0]),
                   dst=output_im,
                   borderMode=cv2.BORDER_TRANSPARENT,
                   flags=cv2.WARP_INVERSE_MAP)
    return output_im

def correct_colours(im1, im2, landmarks1):
    """
    颜色校正：把 im2 的颜色校正到 im1（使用 landmarks1 计算模糊尺度）
    返回 float64 图像
    """
    
    colour_correct_blur_frac = 0.6

    # landmark 索引定义
    face_points = list(range(17, 68))
    mouth_points = list(range(48, 61))
    right_brow_points = list(range(17, 22))
    left_brow_points = list(range(22, 27))
    right_eye_points = list(range(36, 42))
    left_eye_points = list(range(42, 48))
    nose_points = list(range(27, 35))
    jaw_points = list(range(0, 17))

    left_eye = np.mean(landmarks1[left_eye_points], axis=0)
    right_eye = np.mean(landmarks1[right_eye_points], axis=0)
    blur_amount = colour_correct_blur_frac * np.linalg.norm(left_eye - right_eye)
    blur_amount = int(blur_amount)
    if blur_amount % 2 == 0:
        blur_amount += 1
    # 防止 blur_amount 太小
    blur_amount = max(1, blur_amount)

    im1_blur = cv2.GaussianBlur(im1, (blur_amount, blur_amount), 0)
    im2_blur = cv2.GaussianBlur(im2, (blur_amount, blur_amount), 0)

    # 避免除零
    im2_blur = im2_blur.astype(np.float64)
    im2_blur += (128 * (im2_blur <= 1.0)).astype(im2_blur.dtype)

    return (im2.astype(np.float64) * im1_blur.astype(np.float64) /
            im2_blur.astype(np.float64))

def face_change(template_path, user_path, output_path, detector, predictor):
    """人脸替换函数"""
    scale_factor = 1

    # landmark 索引定义
    face_points = list(range(17, 68))
    mouth_points = list(range(48, 61))
    right_brow_points = list(range(17, 22))
    left_brow_points = list(range(22, 27))
    right_eye_points = list(range(36, 42))
    left_eye_points = list(range(42, 48))
    nose_points = list(range(27, 35))
    jaw_points = list(range(0, 17))

    # 用于对齐的关键点
    # align_points = (
    #     left_brow_points +
    #     right_eye_points +
    #     left_eye_points +
    #     right_brow_points +
    #     nose_points +
    #     mouth_points
    # )
    align_points = (
        right_eye_points +
        left_eye_points +
        nose_points +
        mouth_points
    )

    tpl_p = Path(template_path)
    user_p = Path(user_path)
    out_p = Path(output_path)

    im1 = cv2.imread(str(tpl_p), cv2.IMREAD_COLOR)
    im2 = cv2.imread(str(user_p), cv2.IMREAD_COLOR)

    if scale_factor != 1:
        im1 = cv2.resize(im1, (int(im1.shape[1] * scale_factor), int(im1.shape[0] * scale_factor)))
        im2 = cv2.resize(im2, (int(im2.shape[1] * scale_factor), int(im2.shape[0] * scale_factor)))

    landmarks1 = get_landmarks(im1, detector, predictor)
    landmarks2 = get_landmarks(im2, detector, predictor)

    # 计算仿射矩阵：把 user 对齐到 template
    M = transformation_from_points(landmarks1[align_points], landmarks2[align_points])

    # 生成 mask 并 warp 回 template 尺寸
    mask2 = get_face_mask(im2, landmarks2)
    warped_mask = warp_im(mask2, M, im1.shape)
    mask1 = get_face_mask(im1, landmarks1)
    combined_mask = np.max([mask1, warped_mask], axis=0)

    # warp user 图像并进行颜色校正
    warped_im2 = warp_im(im2, M, im1.shape)
    warped_corrected_im2 = correct_colours(im1, warped_im2, landmarks1)

    # 融合（按 mask 权重混合）
    output_im = im1 * (1.0 - combined_mask) + warped_corrected_im2 * combined_mask

    # 保存前把像素裁剪回 0-255 并转 uint8
    output_im = np.clip(output_im, 0, 255).astype(np.uint8)

    cv2.imwrite(str(out_p), output_im)
    # print(f"Saved {out_p}")
    return output_im

def generate_covers(theme_id, image_path):
    """
    生成专辑封面的主函数
    """
    # print(f"生成封面: 歌手={theme_id}, 图片={image_path}")
    
    predictor_path = "./resources/models/shape_predictor_68_face_landmarks.dat"
    
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(predictor_path)
    
    # 定义不同歌手的模板路径和输出目录
    singer_configs = {
        "adam": {
            "templates": [
                "resources/templates/adam/1.jpg",
                "resources/templates/adam/2.jpg",
                "resources/templates/adam/3.jpg",
                "resources/templates/adam/4.jpg",
            ],
            "output_dir": "temp/adam/"
        },
        "angela": {
            "templates": [
                "resources/templates/angela/1.jpg",
                "resources/templates/angela/2.jpg",
                "resources/templates/angela/3.jpg",
                "resources/templates/angela/4.jpg",
            ],
            "output_dir": "temp/angela/"
        },
        "faye": {
            "templates": [
                "resources/templates/faye/1.png",
                "resources/templates/faye/2.jpg",
                "resources/templates/faye/3.jpg",
                "resources/templates/faye/4.jpg",
            ],
            "output_dir": "temp/faye/"
        },
        "eason": {
            "templates": [
                "resources/templates/eason/1.jpg",
                "resources/templates/eason/2.jpg",
                "resources/templates/eason/3.jpg",
                "resources/templates/eason/4.jpg",
            ],
            "output_dir": "temp/eason/"
        },
        "michael": {
            "templates": [
                "resources/templates/michael/1.jpg",
                "resources/templates/michael/2.jpg",
                "resources/templates/michael/3.jpg",
                "resources/templates/michael/4.jpg",
            ],
            "output_dir": "temp/michael/"
        },
        "mj": {
            "templates": [
                "resources/templates/mj/1.jpg",
                "resources/templates/mj/2.jpg",
                "resources/templates/mj/3.jpg",
                "resources/templates/mj/4.jpg",
            ],
            "output_dir": "temp/mj/"
        },
        "gem": {
            "templates": [
                "resources/templates/gem/1.jpg",
                "resources/templates/gem/2.jpg",
                "resources/templates/gem/3.jpg",
                "resources/templates/gem/4.jpg",
            ],
            "output_dir": "temp/gem/"
        },
        "vae": {
            "templates": [
                "resources/templates/vae/1.png",
                "resources/templates/vae/2.jpg",
                "resources/templates/vae/3.jpg",
                "resources/templates/vae/4.jpg",
            ],
            "output_dir": "temp/vae/"
        }
    }
    
    # 获取当前歌手的配置
    config = singer_configs.get(theme_id)
    if not config:
        # print(f"未找到歌手 {theme_id} 的配置")
        return None
    
    # 确保输出目录存在
    os.makedirs(config["output_dir"], exist_ok=True)
    
    # 处理每个模板
    generated_covers = []
    for i, template_path in enumerate(config["templates"]):
        if not os.path.exists(template_path):
            # print(f"模板图片不存在: {template_path}")
            # 创建默认模板作为备用
            continue
            
        # 生成输出路径
        output_filename = f"cover_{i+1}.jpg"
        output_path = os.path.join(config["output_dir"], output_filename)
        
        try:
            # 调用人脸替换函数
            # print(f"正在为歌手 {theme_id} 生成封面 {i+1}/{len(config['templates'])}...")
            face_change(template_path, image_path, output_path, detector, predictor)
            
            # 记录生成的封面路径
            generated_covers.append(output_path)
            # print(f"封面生成成功: {output_path}")
            
        except Exception as e:
            # print(f"生成封面失败: {e}")
            # 创建默认封面作为备用
            try:
                # 复制用户图片作为默认封面
                import shutil
                default_output_path = os.path.join(config["output_dir"], f"default_{i+1}.jpg")
                shutil.copy2(image_path, default_output_path)
                generated_covers.append(default_output_path)
                # print(f"创建默认封面: {default_output_path}")
            except Exception as copy_error:
                print(f"创建默认封面失败: {copy_error}")
    
    # 获取主题展示数据
    theme_show = get_theme_show(theme_id)
    
    if theme_show and generated_covers:
        # 用实际生成的封面路径替换模板中的路径
        for i, slide in enumerate(theme_show.slides):
            if i < len(generated_covers):
                slide.cover_image = generated_covers[i]
                # print(f"设置幻灯片 {i+1} 封面: {generated_covers[i]}")
    
    return theme_show