import modal
from modal import Function, Mount, asgi_app, Image
from modal import App, build, enter, method, web_endpoint, method

from marker.convert import convert_single_pdf
from marker.models import load_all_models
from marker.output import save_markdown


app = App("document-parsing-modal")
MINUTES = 60  # seconds
HOURS = 60 * MINUTES


# MODAL_TOKEN_ID
# MODAL_TOKEN_SECRET

image = (
    modal.Image.debian_slim(python_version="3.9")
    .apt_install(
        "build-essential",
        "curl",
        "libgl1-mesa-glx",
        "libglib2.0-0",
        "libsm6",
        "libxext6",
        "libxrender-dev",
        "git"
    )
    .pip_install(
        "scikit-learn>=1.3.2,<=1.4.2",
        "Pillow>=10.1.0",
        "pydantic>=2.4.2",
        "pydantic-settings>=2.0.3",
        "transformers>=4.36.2",
        "numpy>=1.26.1",
        "python-dotenv>=1.0.0",
        "torch>=2.2.2",
        "tqdm>=4.66.1",
        "tabulate>=0.9.0",
        "ftfy>=6.1.1",
        "texify>=0.1.10",
        "rapidfuzz>=3.8.1",
        "surya-ocr>=0.4.15",
        "filetype>=1.2.0",
        "regex>=2024.4.28",
        "pdftext>=0.3.10",
        "grpcio>=1.63.0",
    )
)

from pydantic import BaseModel
from typing import List

class ParseRequest(BaseModel):
    fname: str
    max_pages: int
    langs: List[str]
    batch_multiplier: int
    start_page: int


@app.cls(gpu="any", image=image, concurrency_limit=100, keep_warm=0, allow_concurrent_inputs=1, container_idle_timeout=5 * MINUTES, timeout=24 * HOURS)
class Model:
    model_list: List = None

    @build()
    @enter()
    def load_model(self):
        model_lst = load_all_models()
        self.model_list = model_lst

    # @web_endpoint(method="POST", docs=True)
    @method()
    def parse_document(self, fname: bytes) -> dict:
        # fname = request.fname
        # max_pages = request.max_pages
        # langs = request.langs
        # batch_multiplier = request.batch_multiplier
        # start_page = request.start_page

        full_text, images, out_meta = convert_single_pdf(fname, self.model_list, max_pages=100, langs=["English"], batch_multiplier=1, start_page=1)
        # subfolder_path = save_markdown("./output", fname, full_text, images, out_meta, image_cutoff=500)
        print("Result: ", full_text)
