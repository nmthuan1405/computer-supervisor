from services.Socket import Socket
import services.utils as utils
import socket
import threading
import queue
import humanize

PORT = 1234
MSG_SIZE = 1024 * 10**3

class Client(Socket, threading.Thread):
    def __init__(self, DELIM=b'\x00'):
        Socket.__init__(self, socket= None, DELIM=DELIM)
        threading.Thread.__init__(self, name='client')

        self.ui_queue = None
        self.socket_queue = queue.Queue()
        self.file_handle = None

    def add_ui_queue(self, ui_queue):
        self.ui_queue = ui_queue
    
    def ui_cmd(self, cmd, ext = None, ui = 'main'):
        self.ui_queue[ui].put((cmd, ext))

    def start_socket(self, SERVER):
        self.socket = socket.socket()
        self.socket.connect((SERVER, PORT))

    def stop_socket(self):
        try:
            self.socket.shutdown(socket.SHUT_RDWR)
            self.socket.close()
        except:
            pass

    # main GUI
    def task_start(self, ip):
        try:
            self.start_socket(ip)
        except:
            self.ui_cmd('start', 'er')
        else:
            self.ui_cmd('start', 'ok')

    def task_stop(self):
        try:
            self.send_str('close')
            self.stop_socket()
        finally:
            self.ui_cmd('stop')

    def task_get_MAC(self):
        self.send_str('get-MAC')
        self.ui_cmd('update-MAC', self.recv_str())

    def task_send_logout(self):
        self.send_str('logout')

    def task_send_shutdown(self):
        self.send_str('shutdown')

    def task_send_restart(self):
        self.send_str('restart')
    
    # screen GUI
    def task_update_stream(self, size):
        self.send_str('screen-stream')
        self.send_obj(size)

        img = self.recv_obj()
        self.ui_cmd('update-stream', img, 'screen')

    def task_capture_stream(self):
        self.send_str('screen-capture')

        img = self.recv_obj()
        self.ui_cmd('save-image', img, 'screen')

    # keyboard GUI
    def task_keyboard_start(self):
        self.send_str('listener-start')

    def task_keyboard_stop(self):
        self.send_str('listener-stop')

    def task_hook(self):
        self.send_str('listener-hook')

    def task_unhook(self):
        self.send_str('listener-unhook')

    def task_log_clear(self):
        self.send_str('listener-clear')

    def task_log_get(self):
        self.send_str('listener-get')
        self.ui_cmd('update-log', self.recv_str(), 'keyboard')

    def task_keyboard_block(self):
        self.send_str('listener-block')

    def task_keyboard_unblock(self):
        self.send_str('listener-unblock')

    # file GUI
    def task_update_dir(self, dir):
        self.send_str('get-dir')
        self.send_str(dir)

        self.ui_cmd('update-dir', self.recv_obj(),'file')

    def task_delete_file(self, path):
        self.send_str('delete-file')
        self.send_str(path)

        if self.recv_state():
            self.ui_cmd('delete-file', 'ok', 'file')
        else:
            self.ui_cmd('delete-file', 'err', 'file')

    # copy-file GUI
    def task_copy_file(self, path, des):
        self.file_handle = utils.FileDownloader(des)
        if self.file_handle.create_file():
            self.send_str('copy-file')
            self.send_str(path)

            name, size = self.recv_obj()
            if size is not None:
                self.file_handle.set_total_size(size)

                self.ui_cmd('get-info', (name, humanize.naturalsize(size)), 'copy-file')
            else:
                self.ui_cmd('get-info', 'err', 'copy-file')
                self.file_handle.delete_file()
                self.file_handle = None
        else:
            self.ui_cmd('create-file', 'err', 'copy-file')

    def task_continue_copy_file(self):
        def error_handler():
            self.file_handle.delete_file()
            self.file_handle = None
            self.ui_cmd('copy-file', 'err', 'copy-file')

        if self.file_handle is not None:
            self.send_str('continue-copy-file')
            self.send_str(MSG_SIZE)
            data = self.recv_obj()

            if data is not None:
                if self.file_handle.write_file(data):
                    size = humanize.naturalsize(self.file_handle.get_received_size()) + ' / ' + humanize.naturalsize(self.file_handle.get_total_size())
                    percent = self.file_handle.get_received_size() / self.file_handle.get_total_size() * 100
                    self.ui_cmd('copy-file', (size, percent), 'copy-file')

                    if percent >= 100:
                        self.ui_cmd('copy-file', 'done', 'copy-file')
                        self.send_str('close-file')
                        self.file_handle.close_file()
                        self.file_handle = None
                else:
                    self.send_str('close-file')
                    error_handler()
            else:
                error_handler()

    def task_cancel_copy_file(self):
        self.send_str('close-file')
        self.file_handle.delete_file()
        self.file_handle = None

    # registry GUI
    def task_merge_reg_file(self, file_data):
        self.send_str('merge-reg-file')
        self.send_str(file_data)

        if self.recv_state():
            self.ui_cmd('merge', 'ok', 'reg')
        else:
            self.ui_cmd('merge', 'err', 'reg')

    def task_query_reg_value(self, path, value):
        self.send_str('query-reg-value')
        self.send_str(path)
        self.send_str(value)

        self.ui_cmd('query', self.recv_obj(), 'reg')

    def task_set_reg_value(self, path, value, type, data):
        self.send_str('set-reg-value')
        self.send_str(path)
        self.send_str(value)
        self.send_str(type)
        self.send_obj(data)

        if self.recv_state():
            self.ui_cmd('set-value', 'ok', 'reg')
        else:
            self.ui_cmd('set-value', 'err', 'reg')

    def task_delete_reg_value(self, path, value):
        self.send_str('delete-reg-value')
        self.send_str(path)
        self.send_str(value)

        if self.recv_state():
            self.ui_cmd('delete-value', 'ok', 'reg')
        else:
            self.ui_cmd('delete-value', 'err', 'reg')

    def task_create_reg_key(self, path):
        self.send_str('create-reg-key')
        self.send_str(path)

        if self.recv_state():
            self.ui_cmd('create-key', 'ok', 'reg')
        else:
            self.ui_cmd('create-key', 'err', 'reg')

    def task_delete_reg_key(self, path):
        self.send_str('delete-reg-key')
        self.send_str(path)

        if self.recv_state():
            self.ui_cmd('delete-key', 'ok', 'reg')
        else:
            self.ui_cmd('delete-key', 'err', 'reg')

    # app GUI
    def task_get_running_app(self):
        self.send_str('get-running-app')
        process_list = self.recv_obj()
        self.ui_cmd('update-running', process_list, 'app')

    def task_get_app_list(self):
        self.send_str('get-app-list')
        process_list = self.recv_obj()
        self.ui_cmd('update-app', process_list, 'start-app')

    # process GUI
    def task_kill_process(self, uid, ui = 'process'):
        self.send_str('kill-process')
        self.send_str(uid)
        if self.recv_state():
            self.ui_cmd('kill', 'ok', ui)
        else:
            self.ui_cmd('kill', 'err', ui)

    def task_start_process(self, path, ui = 'process'):
        self.send_str('start-process')
        self.send_str(path)
        if self.recv_state():
            self.ui_cmd('start', 'ok', ui)
        else:
            self.ui_cmd('start', 'err', ui)

    def task_get_running_process(self):
        self.send_str('get-running-process')
        process_list = self.recv_obj()
        self.ui_cmd('update-running', process_list, 'process')


    def run(self):
        while True:
            cmd, args = self.socket_queue.get()
            self.DEBUG('task', cmd, args)

            if cmd == 'exit':
                break
            elif cmd == 'start':
                self.task_start(*args)
            elif cmd == 'stop':    
                self.task_stop()
            elif cmd == 'get-MAC':
                self.task_get_MAC()
            elif cmd == 'logout':
                self.task_send_logout()
            elif cmd == 'shutdown':
                self.task_send_shutdown()
            elif cmd == 'restart':
                self.task_send_restart()

            # screen
            elif cmd == 'update-stream':
                self.task_update_stream(*args)
            elif cmd == 'capture-stream':
                self.task_capture_stream()

            # keyboard
            elif cmd == 'listener-start':
                self.task_keyboard_start()
            elif cmd == 'listener-stop':
                self.task_keyboard_stop()
            elif cmd == 'listener-hook':
                self.task_hook()
            elif cmd == 'listener-unhook':
                self.task_unhook()
            elif cmd == 'listener-clear':
                self.task_log_clear()
            elif cmd == 'listener-get':
                self.task_log_get()
            elif cmd == 'listener-block':
                self.task_keyboard_block()
            elif cmd == 'listener-unblock':
                self.task_keyboard_unblock()
            
            # file
            elif cmd == 'update-dir':
                self.task_update_dir(*args)
            elif cmd == 'copy-file':
                self.task_copy_file(*args)
            elif cmd == 'continue-copy-file':
                self.task_continue_copy_file()
            elif cmd == 'delete-file':
                self.task_delete_file(*args)
            elif cmd == 'cancel-copy-file':
                self.task_cancel_copy_file()
            
            # registry
            elif cmd == 'merge-reg-file':
                self.task_merge_reg_file(*args)
            elif cmd == 'query-reg-value':
                self.task_query_reg_value(*args)
            elif cmd == 'set-reg-value':
                self.task_set_reg_value(*args)
            elif cmd == 'delete-reg-value':
                self.task_delete_reg_value(*args)
            elif cmd == 'create-reg-key':
                self.task_create_reg_key(*args)
            elif cmd == 'delete-reg-key':
                self.task_delete_reg_key(*args)

            # app
            elif cmd == 'get-running-app':
                self.task_get_running_app()
            elif cmd == 'get-app-list':
                self.task_get_app_list()

            # process
            elif cmd == 'kill-process':
                self.task_kill_process(*args)
            elif cmd == 'start-process':
                self.task_start_process(*args)
            elif cmd == 'get-running-process':
                self.task_get_running_process()
     

    def DEBUG(self, *args,**kwargs):
        print('Client:', *args,**kwargs)