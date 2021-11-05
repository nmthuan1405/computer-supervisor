class FileDownloader():
    def __init__(self, file_path):
        self.file_path = file_path
        self.file = None
        self.total_size = 0
        self.received_size = 0
    
    def create_file(self):
        try:
            self.file = open(self.file_path, 'wb')
        except:
            return False
        else:
            return True
    
    def write_file(self, data):
        try:
            if self.received_size < self.total_size:
                self.file.write(data)
                self.received_size += len(data)
        except:
            return False
        else:
            return True

    def close_file(self):
            self.file.close()

    def set_total_size(self, size):
        self.total_size = size

    def get_total_size(self):
        return self.total_size
    
    def get_received_size(self):
        return self.received_size

