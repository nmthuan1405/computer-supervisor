from PIL import Image, ImageGrab

def take_screenshot(size=None):
    image = ImageGrab.grab()
    if size:
        image = image.resize(size, Image.ANTIALIAS)
    
    return image
