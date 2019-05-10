class Uploader:

    def __init__(self):
        self.queue = Queue()

    def enqueue(self, file):
        raise NotImplementedError

    def flush(self):
        raise NotImplementedError

    def uploaded_files(self):
        raise NotImplementedError
