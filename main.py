from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
import warnings
import pickle
from datetime import datetime
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from sms_model_prep import sms_predictor
warnings.filterwarnings('ignore')
from feature import FeatureExtraction
from fastapi.responses import JSONResponse
from datetime import datetime

app = FastAPI()

file = open(r"pickle/model.pkl","rb")
gbc = pickle.load(file)
file.close()

with open(r'sms\archive\pickle\sms_model2.pkl', 'rb') as f:
    classifier = pickle.load(f)
with open(r'sms\archive\pickle\vectorizer.pkl', 'rb') as f:
    cv = pickle.load(f)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB connection URL
MONGO_URL = "mongodb+srv://saifmohamedsv:KsrIoeUzVVZi0zw8@cluster0.bq297d9.mongodb.net/"
client = AsyncIOMotorClient(MONGO_URL)
database = client["graduation"]
collection = database["phishing-payloads"]

class RequestBody(BaseModel):
    payload: str
    model: str
    uid: str

class ResponseBody(BaseModel):
    id:str
    payload: str
    model: str
    created_at: datetime
    status: int
    uid: str


@app.get("/user-payloads/{uid}")
async def get_user_payloads(uid: str):
    payloads = []
    async for document in collection.find({"uid": uid}):
        document["_id"] = str(document["_id"])
        document["created_at"] = document["created_at"].isoformat()
        payloads.append(document)

    return JSONResponse(content=payloads)


async def save_payload(payload: str, model: str, status: np.int64, uid: str) -> ResponseBody:
    ts = datetime.now()
    status_int = int(status)
    payload_dict = {"payload": payload, "model": model, "status": status_int, "created_at": ts, "uid": uid}
    result = await collection.insert_one(payload_dict)
    inserted_id = str(result.inserted_id)
    return ResponseBody(id=inserted_id, payload=payload, model=model, created_at=ts, status=status, uid=uid)

@app.post("/extract-features", response_model=ResponseBody)
async def root(item: RequestBody):
    if item.model == "url":
        features = np.array(FeatureExtraction(item.payload).getFeaturesList()).reshape(1, 30)
        y_pred = gbc.predict(features)[0]
        if y_pred == 0:
            saved_payload = await save_payload(item.payload, item.model, y_pred, item.uid)
            return saved_payload
        else:
            return ResponseBody(id='', payload=item.payload, model=item.model, created_at=datetime.now(), status=y_pred, uid=item.uid)
    else:
        print(item.payload)
        return ResponseBody(id='', payload=item.payload, model=item.model, created_at=datetime.now(), status= sms_predictor(classifier,cv).predict_spam(item.payload), uid=item.uid)
