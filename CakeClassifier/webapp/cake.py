from starlette.applications import Starlette
from starlette.responses import JSONResponse, HTMLResponse, RedirectResponse

from fastai.vision import (
    ImageDataBunch,
    load_learner,
    open_image,
)
from pathlib import Path
from io import BytesIO

import numpy as np
import uvicorn
import sys

app = Starlette()

cake_model_path = Path("./model")
cake_learner = load_learner(cake_model_path, "export.pkl")

classes = cake_learner.data.classes

@app.route("/predict", methods=["POST"])
async def predict(request):
    data = await request.form()
    bytes = await (data["file"].read())
    return predict_image_from_bytes(bytes)

def predict_image_from_bytes(bytes):
    img = open_image(BytesIO(bytes))
    preds, y, losses = cake_learner.predict(img)
    class_idx = np.argmax(losses).item()
    return JSONResponse({
        "prediction" : classes[class_idx]
    })

@app.route("/")
def form(request):
    return HTMLResponse(
    """
    <h1>Is it Cake?</h1>
    <form action="/predict" method="post" enctype="multipart/form-data">
        Select Image to Upload:
        <input type="file" name="file" />
        <input type="submit" value="Upload Image" />
    </form>
    """
    )

if __name__ == "__main__":
    if "serve" in sys.argv:
        uvicorn.run(app, host="0.0.0.0", port=8080)
