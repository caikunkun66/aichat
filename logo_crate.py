from PIL import Image, ImageDraw, ImageFont

class ImageTextEditor:
    def __init__(self, image_path):
        # 初始化时打开图片
        self.image = Image.open(image_path)
        self.draw = ImageDraw.Draw(self.image)
# (207, -8)
    def add_text(self, text, position=(207, -5), font_path='AlibabaPuHuiTi-3-105-Heavy.ttf', font_size=48, text_color='261a18'):
        # 加载字体
        try:
            font = ImageFont.truetype(font_path, font_size)
        except IOError:
            # 如果指定的字体不存在，使用默认字体
            font = ImageFont.load_default()

        # 将颜色从十六进制转换为Pillow可以理解的格式
        text_color = tuple(int(text_color[i:i+2], 16) for i in (0, 2, 4))

        # 在图片上添加文字
        self.draw.text(position, text, fill=text_color, font=font)

    def save_image(self, output_path):
        # 保存图片到指定路径
        self.image.save(output_path)

    def show_image(self):
        # 显示图片
        self.image.show()

# titles = ['浙江星', '河南星','湖北星','山东星','湖南星','广东星','北京星','福建星','黑龙江星','安徽星']
# titles = ['百双卡','乐学卡','皇冠卡','福兔卡','灵龙卡']
titles = ['菜鸟宝','流量王']
# 使用示例
for title in titles:
    image_path = '站群网站logo20240623-联通-1-文字留空.png'
    output_path = f'联通_{title}_logo.png'
    text = title
    # 创建图像编辑器对象
    editor = ImageTextEditor(image_path)
    # 添加文字
    editor.add_text(text)
    # # 显示图片
    # editor.show_image()
    # 保存图片
    editor.save_image(output_path)


