def countobjects(img):
    pylab.imshow(img)
    pylab.gray()

    imgf = ndimage.gaussian_filter(img, 4.5)
    T = mahotas.thresholding.otsu(imgf)
    #pylab.imshow(img > T)
    #pylab.show()

    labeled, nr_objects = ndimage.label(imgf > T)
    pylab.imshow(labeled)
    #pylab.jet()
    #pylab.show()
    return nr_objects

# This is the main entry point of the program
if __name__ == "__main__":
    import scipy
    from scipy import misc
    import pylab
    import skimage.filter as skif
    import mahotas
    from scipy import ndimage

    circles = mahotas.imread('circles.png')
    objects = mahotas.imread('objects.png')
    peppers = mahotas.imread('peppers.png')

    print 'Number of Circles: ' + str(countobjects(circles))
    print 'Number of Objects: ' + str(countobjects(objects))
    print 'Number of Pepper: ' + str(countobjects(peppers))

