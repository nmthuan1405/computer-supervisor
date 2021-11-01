from PIL import Image, ImageGrab
import win32api

def take_screenshot(size=None):
    image = ImageGrab.grab()
    if size is not None:
        image = image.resize(size, Image.ANTIALIAS)
    
    return image

def get_all_disk_letters():
    drives = win32api.GetLogicalDriveStrings()
    drives = drives.split('\000')[:-1]

    return drives

# for drive in get_all_disk_letters():
#     print(win32api.GetVolumeInformation(drive))