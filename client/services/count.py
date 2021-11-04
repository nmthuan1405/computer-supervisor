class Count:
    def __init__(self, default_count, function, *args, **kwargs):
        self.default_count = default_count
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.count = 0

    def run(self):
        self.function(*self.args, **self.kwargs)

    def count_up(self, count_up = None):
        if count_up is None:
            self.count += 1
        elif count_up == -1:
            self.count = self.default_count
        else:
            self.count += count_up

        if self.count >= self.default_count:
            self.run()
            self.count = 0