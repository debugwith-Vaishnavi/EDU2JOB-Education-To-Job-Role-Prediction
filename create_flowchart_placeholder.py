from PIL import Image, ImageDraw, ImageFont

# create white image
img = Image.new('RGB', (600, 400), color='white')
d = ImageDraw.Draw(img)
text = "Flowchart placeholder"
# default font
font = ImageFont.load_default()
bbox = d.textbbox((0,0), text, font=font)
text_w = bbox[2] - bbox[0]
text_h = bbox[3] - bbox[1]
d.text(((600 - text_w) / 2, (400 - text_h) / 2), text, fill='black', font=font)
img.save('f:/edu2job/flowchart.png')
print('flowchart.png created')
