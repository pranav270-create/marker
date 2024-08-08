import modal

my_file = "file.pdf"
# send in bytes
file_bytes = open(my_file, "rb").read()
cls = modal.Cls.lookup("document-parsing-modal", "Model")
obj = cls()
obj.parse_document.remote(file_bytes)
