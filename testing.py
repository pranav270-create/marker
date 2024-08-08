import modal


def main():
    my_file = "file.pdf"
    file_bytes = open(my_file, "rb").read()
    file_bytes = [file_bytes] * 10
    cls = modal.Cls.lookup("document-parsing-modal", "Model")
    obj = cls()
    for ret in obj.parse_document.map(file_bytes, return_exceptions=True):
        pass


if __name__ == "__main__":
    main()
