"""
各个歌手主题的展示内容定义
"""
from templates.show_templates import ThemeShow, SlideShowItem
import time

def create_adam_theme_show():
    """创建Adam Lambert主题的展示内容"""
    theme_show = ThemeShow("adam", "Adam Lambert")
    
    theme_show.add_slide(SlideShowItem(
        background_image="resources/backgrounds/adam/bg1.jpeg",
        audio_file="resources/sounds/adam/1.mp3",
        cover_image="temp/adam/cover_1.jpg",
        description="你在2009年推出了专辑《For Your Entertainment》，主打歌《Whataya Want From Me》唱出在情感索取中的自我捍卫与脆弱；这张专辑以绚丽的华丽摇滚舞台，奠定了你颠覆传统的巨星姿态。",
        display_duration=6000,
        music_duration=3000,
        animate_duration=5000
    ))
    
    theme_show.add_slide(SlideShowItem(
        background_image="resources/backgrounds/adam/bg2.jpeg",
        audio_file="resources/sounds/adam/2.mp3",
        cover_image="temp/adam/cover_2.jpg",
        description="你在2013年推出了专辑《Trespassing》，主打歌《Runnin'》演绎出对自由与界限的永不停歇的追逐；这张专辑以流畅的放克与流行节拍，构建了一场关于突破与身份认同的音乐宣言。",
        display_duration=6000,
        music_duration=3000,
        animate_duration=5000
    ))

    theme_show.add_slide(SlideShowItem(
        background_image="resources/backgrounds/adam/bg3.jpeg",
        audio_file="resources/sounds/adam/3.mp3",
        cover_image="temp/adam/cover_3.jpg",
        description="你在2016年推出了单曲《Welcome To The Show》，以史诗般的编曲向世界发出盛大邀约；这首歌曲以剧场般的磅礴层次，赞颂了现场演出的魔力与归属感。",
        display_duration=6000,
        music_duration=3000,
        animate_duration=5000
    ))

    theme_show.add_slide(SlideShowItem(
        background_image="resources/backgrounds/adam/bg4.jpeg",
        audio_file="resources/sounds/adam/4.mp3",
        cover_image="temp/adam/cover_4.jpg",
        description="你在2023年推出了专辑《High Drama》，主打歌《Chandelier》重新诠释了在耀眼高处摇摇欲坠的戏剧性坠落；这张以颠覆性翻唱为核心的专辑，淋漓尽致地展现了情感的张力和舞台人生的浮沉。",
        display_duration=6000,
        music_duration=3000,
        animate_duration=5000
    ))
    
    return theme_show

def create_angela_theme_show():
    """创建张韶涵主题的展示内容"""
    theme_show = ThemeShow("angela", "张韶涵")
    
    theme_show.add_slide(SlideShowItem(
        background_image="resources/backgrounds/angela/bg1.jpeg",
        audio_file="resources/sounds/angela/1.mp3",
        cover_image="temp/angela/cover_1.jpg",
        description="你在2004年初推出了专辑《Over The Rainbow》，凭借主打歌《寓语》唱出梦想的寓言与追索的勇气；这张专辑以缤纷多元的音乐风格，开启了一段如彩虹般绚烂的奇幻出道之旅。",
        display_duration=6000,
        music_duration=3000,
        animate_duration=5000
    ))

    theme_show.add_slide(SlideShowItem(
        background_image="resources/backgrounds/angela/bg2.jpeg",
        audio_file="resources/sounds/angela/2.mp3",
        cover_image="temp/angela/cover_2.jpg",
        description="你在2004年底推出了专辑《欧若拉》，以主打歌《欧若华》吟唱出极光般的神秘力量与希望之光；这张专辑融合空灵嗓音与电子节奏，勾勒出一幅充满能量与异想的神圣音乐画卷。",
        display_duration=6000,
        music_duration=3000,
        animate_duration=5000
    ))

    theme_show.add_slide(SlideShowItem(
        background_image="resources/backgrounds/angela/bg3.jpeg",
        audio_file="resources/sounds/angela/3.mp3",
        cover_image="temp/angela/cover_3.jpg",
        description="你在2007年初推出了专辑《梦里花》，凭借主打歌《梦花缘》低语那些如花绽放的纯真梦境与执着渴望；这张专辑用温暖细腻的抒情旋律，编织了一场如诗如画、不愿醒来的情感梦乡。",
        display_duration=6000,
        music_duration=3000,
        animate_duration=5000
    ))
    
    theme_show.add_slide(SlideShowItem(
        background_image="resources/backgrounds/angela/bg4.jpeg",
        audio_file="resources/sounds/angela/4.mp3",
        cover_image="temp/angela/cover_4.jpg",
        description="你在2007年底推出了专辑《Ang 5.0》，以主打歌《亲爱非情》剖白爱情的错觉与成长的释然；这张专辑通过更趋成熟的唱腔与多元曲风，宣告了你在音乐旅程中的一次华丽蜕变与自信突破。",
        display_duration=6000,
        music_duration=3000,
        animate_duration=5000
    ))
    
    return theme_show

def create_faye_theme_show():
    """创建Faye Wong主题的展示内容"""
    theme_show = ThemeShow("faye", "王菲")
    
    theme_show.add_slide(SlideShowItem(
        background_image="resources/backgrounds/faye/bg1.jpeg",
        audio_file="resources/sounds/faye/1.mp3",
        cover_image="temp/faye/cover_1.jpg",
        description="你在1998年推出了专辑《唱游》，凭借主打歌《红米》唱出隽永的相思与淡然；这张专辑以充满玩心的音乐探索，呈现了爱情中百转千回的不同面貌。",
        display_duration=6000,
        music_duration=3000,
        animate_duration=5000
    ))
    
    theme_show.add_slide(SlideShowItem(
        background_image="resources/backgrounds/faye/bg2.jpeg",
        audio_file="resources/sounds/faye/2.mp3",
        cover_image="temp/faye/cover_2.jpg",
        description="你在2000年推出了专辑《寓言》，以主打歌《笑忘录》传递出一份通透的自我和解；专辑开篇的五首连贯之作，构建了一个充满哲学意味的宏大音乐寓言。",
        display_duration=6000,
        music_duration=3000,
        animate_duration=5000
    ))

    theme_show.add_slide(SlideShowItem(
        background_image="resources/backgrounds/faye/bg3.jpeg",
        audio_file="resources/sounds/faye/3.mp3",
        cover_image="temp/faye/cover_3.jpg",
        description="你在2001年推出了自己的同名专辑，主打歌《逝年》用诗意的笔触喟叹命运相遇的偶然与必然；这张作品以国际化的音乐元素，奠定了你新世纪的音乐风向。",
        display_duration=6000,
        music_duration=3000,
        animate_duration=5000
    ))
    
    theme_show.add_slide(SlideShowItem(
        background_image="resources/backgrounds/faye/bg4.jpeg",
        audio_file="resources/sounds/faye/4.mp3",
        cover_image="temp/faye/cover_4.jpg",
        description="在这张同名专辑中，单曲《光翼》以前卫的电子音效模拟网络世界的感官冲击；这首歌敏锐地捕捉了互联网时代初临的脉搏，成为跨越时代的先声。",
        display_duration=6000,
        music_duration=3000,
        animate_duration=5000
    ))
    
    return theme_show

def create_eason_theme_show():
    """创建陈奕迅主题的展示内容"""
    theme_show = ThemeShow("eason", "陈奕迅")
    
    theme_show.add_slide(SlideShowItem(
        background_image="resources/backgrounds/eason/bg1.jpeg",
        audio_file="resources/sounds/eason/1.mp3",
        cover_image="temp/eason/cover_1.jpg",
        description="你在1998年推出了专辑《我的快乐时代》，凭借主打歌《唯你无双》唱出对爱情极致而纯粹的礼赞；这张专辑以轻快旋律与真挚演绎，定格了青春岁月中那份无畏的快乐与憧憬。",
        display_duration=6000,
        music_duration=3000,
        animate_duration=5000
    ))

    theme_show.add_slide(SlideShowItem(
        background_image="resources/backgrounds/eason/bg2.jpeg",
        audio_file="resources/sounds/eason/2.mp3",
        cover_image="temp/eason/cover_2.jpg",
        description="你在2001年推出了专辑《Shall We Dance? Shall We Talk!》，以主打歌《可否畅言》叩问现代生活中疏离与沟通的隔阂；专辑通过舞曲节奏与深情叙事的结合，完成一场关于人际共鸣的音乐思辨。",
        display_duration=6000,
        music_duration=3000,
        animate_duration=5000
    ))

    theme_show.add_slide(SlideShowItem(
        background_image="resources/backgrounds/eason/bg3.jpeg",
        audio_file="resources/sounds/eason/3.mp3",
        cover_image="temp/eason/cover_3.jpg",
        description="你在2002年推出了专辑《五星级的家》，以主打歌《失群之子》低吟繁华表象下的孤独与漂泊感；这张专辑在看似奢华的基调中，层层剖开对家庭归属与内心空洞的深刻反思。",
        display_duration=6000,
        music_duration=3000,
        animate_duration=5000
    ))

    theme_show.add_slide(SlideShowItem(
        background_image="resources/backgrounds/eason/bg4.jpeg",
        audio_file="resources/sounds/eason/4.mp3",
        cover_image="temp/eason/cover_4.jpg",
        description="同年，你推出了专辑《The Line-Up》，凭借主打歌《来年今日》勾勒时光流转中绵长的怀念与期许；这张集结顶尖创作阵容的专辑，以多元曲风编织出一幅关于人生起落的情感航图。",
        display_duration=6000,
        music_duration=3000,
        animate_duration=5000
    ))
    
    return theme_show

def create_michael_theme_show():
    """创建郑钧主题的展示内容"""
    theme_show = ThemeShow("michael", "郑钧")
    
    theme_show.add_slide(SlideShowItem(
        background_image="resources/backgrounds/michael/bg1.jpeg",
        audio_file="resources/sounds/michael/1.mp3",
        cover_image="temp/michael/cover_1.jpg",
        description="你在1994年推出了专辑《赤裸裸》，凭借主打歌《归拉萨》唱出对雪域圣地的炽热向往与灵魂呼唤；这张专辑以粗糙而直接的摇滚质感，赤裸裸地展现了年轻世代的反叛激情与自由追寻。",
        display_duration=6000,
        music_duration=3000,
        animate_duration=5000
    ))

    theme_show.add_slide(SlideShowItem(
        background_image="resources/backgrounds/michael/bg2.jpeg",
        audio_file="resources/sounds/michael/2.mp3",
        cover_image="temp/michael/cover_2.jpg",
        description="你在1997年推出了专辑《第三只眼》，以主打歌《门扉》传递出一种内省而迷离的哲学思辨；这张专辑通过实验性的音乐编排，如同第三只眼般洞见了人性深层的矛盾与觉醒。",
        display_duration=6000,
        music_duration=3000,
        animate_duration=5000
    ))

    theme_show.add_slide(SlideShowItem(
        background_image="resources/backgrounds/michael/bg3.jpeg",
        audio_file="resources/sounds/michael/3.mp3",
        cover_image="temp/michael/cover_3.jpg",
        description="你在1999年推出了专辑《怒放》，凭借主打歌《盛放》呐喊出生命在压抑后的极致绽放与不屈斗志；这张专辑以充满张力的摇滚风暴，怒放着对存在意义的炽热追问。",
        display_duration=6000,
        music_duration=3000,
        animate_duration=5000
    ))

    theme_show.add_slide(SlideShowItem(
        background_image="resources/backgrounds/michael/bg4.jpeg",
        audio_file="resources/sounds/michael/4.mp3",
        cover_image="temp/michael/cover_4.jpg",
        description="你在2014年推出了单曲《无偿欢愉》，以轻快旋律与慵懒吟唱传递出一份随手馈赠的洒脱快乐；这首歌曲以简约编曲与真挚词作，在浮华时代里唤醒人们心底那份免费而简单的喜悦。",
        display_duration=6000,
        music_duration=3000,
        animate_duration=5000
    ))
    
    return theme_show

def create_mj_theme_show():
    """创建Michael Jackson主题的展示内容"""
    theme_show = ThemeShow("mj", "Michael Jackson")
    
    theme_show.add_slide(SlideShowItem(
        background_image="resources/backgrounds/mj/bg1.jpeg",
        audio_file="resources/sounds/mj/1.mp3",
        cover_image="temp/mj/cover_1.jpg",
        description="你在1982年推出了专辑《Thriller》，凭借主打歌《Billie Jean》唱出对媒体骚扰与亲子争议的深刻反思；这张专辑以融合放克、摇滚与流行乐的开创性制作，重新定义了现代音乐产业的标准，成为史上最畅销的唱片。",
        display_duration=6000,
        music_duration=3000,
        animate_duration=5000
    ))
    
    theme_show.add_slide(SlideShowItem(
        background_image="resources/backgrounds/mj/bg2.jpeg",
        audio_file="resources/sounds/mj/2.mp3",
        cover_image="temp/mj/cover_2.jpg",
        description="在专辑《Thriller》中，单曲《P.Y.T.》以轻快的放克节奏和浪漫歌词，捕捉了年轻爱情的欢愉与活力；这首歌的合成器音效与动感旋律，成为派对音乐的经典之作，展现了专辑的多元娱乐氛围。",
        display_duration=6000,
        music_duration=3000,
        animate_duration=5000
    ))
    
    theme_show.add_slide(SlideShowItem(
        background_image="resources/backgrounds/mj/bg3.jpeg",
        audio_file="resources/sounds/mj/3.mp3",
        cover_image="temp/mj/cover_3.jpg",
        description="你在1987年推出了专辑《Bad》，主打歌《Smooth Criminal》用强劲的节拍和悬疑叙事，刻画了都市犯罪故事的紧张氛围；这张作品以更坚韧的摇滚与放克元素，展现了你在音乐与舞蹈上的巅峰创新，巩固了流行之王的地位。",
        display_duration=6000,
        music_duration=3000,
        animate_duration=5000
    ))
    
    theme_show.add_slide(SlideShowItem(
        background_image="resources/backgrounds/mj/bg4.jpeg",
        audio_file="resources/sounds/mj/4.mp3",
        cover_image="temp/mj/cover_4.jpg",
        description="在专辑《Bad》中，单曲《Liberian Girl》以温柔的旋律和非洲节奏，歌颂了跨越文化的浪漫爱情；这首歌的世界音乐风情与深情演唱，体现了你对全球音乐融合的敏锐洞察，为专辑注入了异国情调的魅力。",
        display_duration=6000,
        music_duration=3000,
        animate_duration=5000
    ))
    
    return theme_show

def create_gem_theme_show():
    """创建邓紫棋主题的展示内容"""
    theme_show = ThemeShow("gem", "邓紫棋")
    
    theme_show.add_slide(SlideShowItem(
        background_image="resources/backgrounds/gem/bg1.jpeg",
        audio_file="resources/sounds/gem/1.mp3",
        cover_image="temp/gem/cover_1.jpg",
        description="你在2015年推出了专辑《新的心跳》，凭借主打歌《天涯共此时》唱出跨越千山万水的执着眷恋；这张专辑以鲜活节奏与情感迸发，演绎了爱情中重启心跳的蜕变与复苏。",
        display_duration=6000,
        music_duration=3000,
        animate_duration=5000
    ))
    
    theme_show.add_slide(SlideShowItem(
        background_image="resources/backgrounds/gem/bg2.jpeg",
        audio_file="resources/sounds/gem/2.mp3",
        cover_image="temp/gem/cover_2.jpg",
        description="你在2016年推出了单曲《星河之约》，以浩瀚编曲与炽热声线倾诉穿越宇宙的永恒爱意；这首歌曲借科幻诗境与激昂旋律，在无垠时空里铭刻下灵魂相拥的浪漫传奇。",
        display_duration=6000,
        music_duration=3000,
        animate_duration=5000
    ))

    theme_show.add_slide(SlideShowItem(
        background_image="resources/backgrounds/gem/bg3.jpeg",
        audio_file="resources/sounds/gem/3.mp3",
        cover_image="temp/gem/cover_3.jpg",
        description="你在2018年推出了专辑《睡皇后》，凭借主打歌《岩心花开》歌颂了绝境中破土而出的坚韧守望；这张专辑以迷幻音景与内在力量，寓言了沉睡心灵苏醒后直面现实的勇气之旅。",
        display_duration=6000,
        music_duration=3000,
        animate_duration=5000
    ))

    theme_show.add_slide(SlideShowItem(
        background_image="resources/backgrounds/gem/bg4.jpeg",
        audio_file="resources/sounds/gem/4.mp3",
        cover_image="temp/gem/cover_4.jpg",
        description="你在2021年推出了单曲《双面镜》，以对立声部与诡谲编曲揭露内心矛盾自我的撕扯与共生；这首歌曲通过分裂与和解的音乐对话，在当代情感迷雾中映照出人性幽微的双重真相。",
        display_duration=6000,
        music_duration=3000,
        animate_duration=5000
    ))

    return theme_show

def create_vae_theme_show():
    """创建许嵩主题的展示内容"""
    theme_show = ThemeShow("vae", "许嵩")
    
    theme_show.add_slide(SlideShowItem(
        background_image="resources/backgrounds/vae/bg1.jpeg",
        audio_file="resources/sounds/vae/1.mp3",
        cover_image="temp/vae/cover_1.jpg",
        description="你在2012年推出了专辑《梦游计》，凭借主打歌《幻声》吟唱出爱情消逝后萦绕不散的听觉幻觉与缱绻执念；这张专辑以迷离的电子音色与诗意的意识流词作，带领听众潜入梦境与现实交错的朦胧地带，映射出情感中那些虚实难辨的怅惘与沉溺。",
        display_duration=6000,
        music_duration=3000,
        animate_duration=5000
    ))

    theme_show.add_slide(SlideShowItem(
        background_image="resources/backgrounds/vae/bg2.jpeg",
        audio_file="resources/sounds/vae/2.mp3",
        cover_image="temp/vae/cover_2.jpg",
        description="你在2017年推出了单曲《破关》，以激昂的节奏与充满斗志的演唱传递出迎战人生关卡时的不屈信念；这首歌曲借用游戏闯关的隐喻与鼓舞人心的编曲，在喧嚣时代中唤醒人们直面挑战、解锁自我极限的勇气与热忱。",
        display_duration=6000,
        music_duration=3000,
        animate_duration=5000
    ))

    theme_show.add_slide(SlideShowItem(
        background_image="resources/backgrounds/vae/bg3.jpeg",
        audio_file="resources/sounds/vae/3.mp3",
        cover_image="temp/vae/cover_3.jpg",
        description="你在2018年推出了单曲《如期而来》，以温暖的吉他旋律与柔和声线诉说着跨越时间洪流的守候与重逢之喜；这首歌曲通过简约而真挚的抒情叙事，在浮躁生活里勾勒出一份历经岁月依旧笃定的浪漫约定，唤起人们对永恒陪伴的向往。",
        display_duration=6000,
        music_duration=3000,
        animate_duration=5000
    ))

    theme_show.add_slide(SlideShowItem(
        background_image="resources/backgrounds/vae/bg4.jpeg",
        audio_file="resources/sounds/vae/4.mp3",
        cover_image="temp/vae/cover_4.jpg",
        description="你在2023年推出了单曲《意料外》，以轻快的节奏与诙谐的歌词戏谑描绘生活中猝不及防的转折与意外馈赠；这首歌曲凭借幽默的叙事视角与松弛的编曲，在充满不确定的世界里提醒人们以坦然之心拥抱未知，品味每一场不期而遇的惊喜与成长。",
        display_duration=6000,
        music_duration=3000,
        animate_duration=5000
    ))
    
    return theme_show

# 歌手主题展示创建函数的映射
THEME_SHOW_CREATORS = {
    "adam": create_adam_theme_show,
    "angela": create_angela_theme_show,
    "faye": create_faye_theme_show,
    "eason": create_eason_theme_show,
    "michael": create_michael_theme_show,
    "mj": create_mj_theme_show,
    "gem": create_gem_theme_show,
    "vae": create_vae_theme_show
}

def get_theme_show(theme_id):
    """根据歌手ID获取对应的展示内容"""
    creator = THEME_SHOW_CREATORS.get(theme_id)
    if creator:
        return creator()
    return None