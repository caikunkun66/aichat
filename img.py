from PIL import Image, ImageDraw, ImageFont

# 加载图像
image_path = '1.jpg'
image = Image.open(image_path)

# 将图像转换为RGB模式
image = image.convert('RGB')

# 创建一个可绘制对象
draw = ImageDraw.Draw(image)

# 尝试加载系统默认字体
try:
    font_path = 'SIMHEI.TTF'  # Windows系统默认字体路径
    font_size = 30
    font = ImageFont.truetype(font_path, font_size)
except IOError:
    print("默认字体加载失败")

# 尝试加载字体，用于突出显示部分文本
try:
    highlight_font_size = 50
    highlight_font = ImageFont.truetype(font_path, highlight_font_size)
except IOError:
    print("突出显示字体加载失败")

# 定义要添加的文本和位置
text_data = {
    "月租": ("29元", (260, 180)),
    "流量": ("80G（50G通用+30G定向）", (425, 310)),
    "通话": ("0.1元/分钟", (425, 365)),
    "福利": ("首充100元赠送240元", (100, 445)),
    "套餐外资费": ("定向流量5元/G，短彩信0.1元/条", (100, 475)),
    "办理年龄": ("18-65周岁", (100, 635)),
    "资费及发货说明": ("激活后首月9.9元权益包，次月起29元/月。专属渠道充值100元送240元。激活后赠送50G全国通用流量，流量有效期24个月。套餐内容按实际折算，次月起全月。京东上门配送激活。激活后插入手机并拨打一次电话进行实名验证。不发货地区：新疆、西藏、北京、云南、杭州、嘉兴、安阳、鹤壁、成都、常德、仙桃、吕梁、太原、阳泉、重庆、黑河、哈尔滨、保定市内蒙古（呼和浩特、赤峰、通辽、鄂尔多斯、呼伦贝尔、锡林郭勒、乌海）黑龙江、吉林、辽宁", (100, 715))
}

# 设置字体颜色
font_color = "black"
highlight_color = (0, 152, 250)  # 十六进制颜色 #0098fa 转换为 RGB

# 定义加粗的次数
boldness = 1  # 设置较小的加粗程度

def draw_bold_text(draw, position, text, font, color, boldness):
    x, y = position
    # 通过偏移绘制文本以模拟加粗效果
    for offset in range(-boldness, boldness + 1):
        draw.text((x + offset, y), text, font=font, fill=color)
        draw.text((x, y + offset), text, font=font, fill=color)

# 在图像上添加文本
for key, value in text_data.items():
    text, position = value
    
    if key == "月租":
        # 突出显示部分
        highlight_text = "29"
        rest_text = "元"
        
        # 计算突出显示部分的边界框
        highlight_bbox = draw.textbbox((0, 0), highlight_text, font=highlight_font)
        highlight_width = highlight_bbox[2] - highlight_bbox[0]
        highlight_height = highlight_bbox[3] - highlight_bbox[1]
        
        # 计算剩余部分的边界框
        rest_bbox = draw.textbbox((0, 0), rest_text, font=font)
        rest_height = rest_bbox[3] - rest_bbox[1]
        
        # 绘制突出显示部分并加粗
        draw_bold_text(draw, position, highlight_text, highlight_font, highlight_color, boldness)
        
        # 手动调整小字体的 y 位置
        y_adjusted = position[1] + highlight_height - rest_height + 5  # 手动增加5像素
        
        # 绘制剩余部分，使其底部与突出显示部分对齐
        draw.text((position[0] + highlight_width, y_adjusted), rest_text, font=font, fill=font_color)
    else:
        # 直接绘制其他文本
        draw.text(position, text, font=font, fill=font_color)

# 保存图像
output_path = 'output_image.jpg'
image.save(output_path)

# 显示图像（如果在本地运行）
image.show()
