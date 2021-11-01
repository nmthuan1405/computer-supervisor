from services.client import Client
from ui.ui_main import UI_main

if __name__ == "__main__":
    root_ui = UI_main()
    client = Client()

    root_ui.add_socket_queue(client.socket_queue)
    client.add_ui_queue(root_ui.ui_queues)

    client.start()
    root_ui.mainloop()
    