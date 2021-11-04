from services.client import Client
from ui.ui_main import UI_main

if __name__ == "__main__":
    ui_queue = {}
    root_ui = UI_main(ui_queue)
    client = Client()

    root_ui.add_socket_queue(client.socket_queue)
    client.add_ui_queue(ui_queue)

    client.start()
    root_ui.mainloop()
    