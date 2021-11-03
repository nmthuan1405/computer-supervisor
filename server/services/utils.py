from PIL import Image, ImageGrab
from datetime import datetime
import humanize
import win32api
import os
import magic
from getmac import get_mac_address as gma

def take_screenshot(size=None):
    image = ImageGrab.grab()
    if size is not None:
        image = image.resize(size, Image.ANTIALIAS)
    
    return image

def get_all_disk_letters():
    drives = win32api.GetLogicalDriveStrings()
    drives = drives.split('\000')[:-1]

    data_list = []
    for drive in drives:
        info = win32api.GetVolumeInformation(drive)
        data_list.append((drive, info[0], 'Disk drive', ''))
    return data_list

def get_dir(path):
    data_list = []
    if os.path.exists(path):
        with os.scandir(path) as it:
            for entry in it:
                try:
                    info = entry.stat()
                    modified = datetime.fromtimestamp(info.st_mtime).strftime('%d-%m-%Y %H:%M:%S')

                    if entry.is_file():
                        size = humanize.naturalsize(info.st_size)
                        type = magic.from_buffer(open(entry.path, "rb").read(2048))
                        data_list.append((entry.name, modified, type, size))
                    
                    if entry.is_dir():    
                        data_list.append((entry.name, modified, 'File folder', ''))
                except:
                    pass

    data_list.sort(key=lambda x: (x[2] != 'File folder', x[0].lower()))
    return data_list

def get_MAC():
    print(gma())
    return gma()