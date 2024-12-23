from PIL import Image
import plotille as plt


img = Image.open('./meteoblue/pictograms/png/iday/01_iday_new.png')

img = img.convert('L')

res = 5

img = img.resize((int(res*4), int(res*4)))
cvs = plt.Canvas(int(res*2), res)

cvs.braille_image(img.getdata())

with open("canvas_output.txt", "w") as file:
    file.write(cvs.plot())
