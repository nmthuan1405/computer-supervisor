import ctypes
user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

WINDOW_BORDER_PADDING = 10

UPDATE_TIME = {}
UPDATE_TIME['main'] = 200

FRAME_WIDTH = 800
FRAME_HEIGHT = int(FRAME_WIDTH * (screensize[1]/screensize[0]))