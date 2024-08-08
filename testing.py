import modal
import asyncio


async def parse_document(file_bytes):
    cls = modal.Cls.lookup("document-parsing-modal", "Model")
    obj = cls()
    return obj.parse_document.remote(file_bytes)


async def main():
    my_file = "file.pdf"
    file_bytes = open(my_file, "rb").read()

    tasks = [parse_document(file_bytes) for _ in range(10)]
    results = await asyncio.gather(*tasks)
    for result in results:
        print(result)


if __name__ == "__main__":
    asyncio.run(main())
