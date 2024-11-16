import os
import uuid

import app.keras_flowers as kf
from fastapi import FastAPI, UploadFile
from starlette.staticfiles import StaticFiles
from starlette.responses import FileResponse

app = FastAPI()
app.mount("/assets", StaticFiles(directory="frontend/dist/assets"), name="static")
app.mount("/img", StaticFiles(directory="frontend/public/img"), name="static")

@app.get("/")
async def read_index():
    return FileResponse('frontend/dist/index.html')


@app.post("/process")
async def process(image_file: UploadFile):
    filename = f"/tmp/{uuid.uuid4()}{os.path.splitext(image_file.filename)[1]}"
    with open(filename, "wb") as f:
        f.write(await image_file.read())

    predicted, score = max(kf.predict_name_by_path(filename), key=lambda it: it[1])
    os.unlink(filename)

    return {"label": predicted, "score": float(score)}
