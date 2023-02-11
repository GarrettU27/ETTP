import base64
from enum import Enum
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from typing import Union
from pydantic import BaseModel
from dotenv import dotenv_values
from pymongo import MongoClient
from ecg_plot import plot, show, return_svg_bytes, return_png_bytes
from scipy.io import loadmat
import numpy as np

config = dotenv_values(".env")

app = FastAPI()

# Initialize to none. They will be given values at startup.
# This is mainly to get autocompletion on other functions
app.mongodb_client = None
app.database = None


# this deals with some security errors we'd have attempting to pull data from the backend in a dev environment
# for deployment, this permissive security policy would have to be dealt with
origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# https://fastapi.tiangolo.com/advanced/middleware/#gzipmiddleware
app.add_middleware(GZipMiddleware, minimum_size=1000)


@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(config["DB_URI"])
    app.database = app.mongodb_client[config["DB_NAME"]]
    print("Connected to the MongoDB database!")


@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()


@app.get("/")
async def root():
    return {"message": "Hello World"}


def convert_to_millivolts(microvolts: int):
    # the data is in microvolts, convert to millivolts
    return microvolts/1000


@app.get("/ecg-svg")
def get_ecg_svg():
    mat = loadmat("./JS00001.mat")
    data = mat["val"]
    ecg = []

    for ecg_lead in data:
        ecg.append([convert_to_millivolts(bits) for bits in ecg_lead])

    ecg = np.array(ecg)

    plot(ecg)
    return Response(content=return_svg_bytes(), media_type="application/xml")


@app.get("/ecg-png")
def get_ecg_png():
    mat = loadmat("./JS00001.mat")
    data = mat["val"]
    ecg = []

    for ecg_lead in data:
        ecg.append([convert_to_millivolts(bits) for bits in ecg_lead])

    ecg = np.array(ecg)

    plot(ecg)

    png_bytes = return_png_bytes()
    encoded_bytes = base64.b64encode(png_bytes)
    encoded_bytes_string = encoded_bytes.decode('ascii')
    base64_string = f"data:image/png;base64,{encoded_bytes_string}"

    return Response(content=base64_string, media_type="image/png")


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None


@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


@app.get("/db")
def get_database_name():
    return app.database.name
