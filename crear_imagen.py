from PIL import Image

size= (2705 , 4384)
image_text= "ahuevo"
img = Image.new('RGB' ,size)
im_logo = Image.open('cartas/Armades_Cuidador_de_Limites.png')
im_logo2 = Image.open('cartas/Dragon_de_la_Rosa_Negra.png')
im_logo3 = Image.open('cartas/HEROE_Elemental_Stratos.png')
im_logo4 = Image.open('cartas/Caballeria_Oscura.png')
im_logo5 = Image.open('cartas/Dragon_de_Chispas_de_Polvo_de_Estrellas.png')
fondo1= Image.open('con extra.png')
fondo=fondo1.resize((2705 , 4384))
img.paste(fondo,(0,0))
img.paste(im_logo, (100,100))
img.paste(im_logo2, (621,100))
img.paste(im_logo3, (1142,100))
img.paste(im_logo4, (1663,100))
img.paste(im_logo5, (2184,100))

img.paste(im_logo, (100,814))
img.paste(im_logo2, (621,814))
img.paste(im_logo3, (1142,814))
img.paste(im_logo4, (1663,814))
img.paste(im_logo5, (2184,814))

img.paste(im_logo, (100,1528))
img.paste(im_logo2, (621,1528))
img.paste(im_logo3, (1142,1528))
img.paste(im_logo4, (1663,1528))
img.paste(im_logo5, (2184,1528))

img.paste(im_logo, (100,2242))
img.paste(im_logo2, (621,2242))
img.paste(im_logo3, (1142,2242))
img.paste(im_logo4, (1663,2242))
img.paste(im_logo5, (2184,2242))

img.paste(im_logo, (100,2956))
img.paste(im_logo2, (621,2956))
img.paste(im_logo3, (1142,2956))
img.paste(im_logo4, (1663,2956))
img.paste(im_logo5, (2184,2956))

img.paste(im_logo, (100,3670))
img.paste(im_logo2, (621,3670))
img.paste(im_logo3, (1142,3670))
img.paste(im_logo4, (1663,3670))
img.paste(im_logo5, (2184,3670))

img.save('image33.png')

#image = Image.open('unsplash_01.jpg')

greyscale_image = fondo1.convert('L')
greyscale_image.save('greyscale_image.jpg')