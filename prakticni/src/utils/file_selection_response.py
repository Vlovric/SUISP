class FileSelectionResponse:
    def __init__(self, path):
        self.path = path
        self.filename = path.split("/").pop()
        self.content = None
        self.is_binary = False
        self.successful = False

        try:
            try:
                with open(path, "r", encoding="utf-8") as f:
                    self.content = f.read()
                    self.is_binary = False
                    self.successful = True
            except:
                with open(path, "rb") as f:
                    self.content = f.read()
                    self.is_binary = True
                    self.successful = True
        except:
            raise Exception("Nije moguće otvoriti datoteku")