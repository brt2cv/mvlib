import mvlib

# mvlib.set_backend("skimage")
im = mvlib.imread("sample.jpg")
# im2 = mvlib.rgb2gray(im)

#####################################################################

im2 = mvlib.resize(im, (100,150))





mvlib.imsave("save.jpg", im2)
