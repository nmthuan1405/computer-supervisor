from services.server import Server
from ui.ui_main import UI_main

if __name__ == "__main__":
    root_ui = UI_main()
    server = Server()

    root_ui.add_socket_queue(server.socket_queue)
    server.add_ui_queue(root_ui.ui_queue)

    server.start()
    root_ui.mainloop()