from pathlib import Path
import yaml
from fastapi import FastAPI

app = FastAPI(
    debug=True,
    openapi_url="/openapi/orders.json",
    docs_url="/docs/orders"
)

oas_doc_path = Path(__file__).parent / "../../api_docs/orders.yaml"
oas_doc = yaml.safe_load(oas_doc_path.read_text())
app.openapi = lambda: oas_doc

from orders.web.api import api