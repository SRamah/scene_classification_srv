from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict
from app.auth.auth_bearer import JWTBearer
from plugins.scenes.classifier import SceneClassification
from app import schemas

SC = SceneClassification()

router = APIRouter()

@router.get("/", response_model=Dict)
def root():
    return {"message": "Welcome to Scene Classification Service."}

@router.put("/label/", response_model=List[schemas.SceneClassifierOutput], dependencies=[Depends(JWTBearer())])
def scene_label(images: List[str]):
    results = SC.img_classification(images)
    return results