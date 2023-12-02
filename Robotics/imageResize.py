from PIL import Image

image = Image.open('VEXOverUnder.png')
new_image = image.resize((1700, 1700))
new_image.save('VEXOverUnder_1800.png')