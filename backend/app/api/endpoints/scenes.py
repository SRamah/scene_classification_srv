from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict
from backend.app.auth.auth_bearer import JWTBearer
from backend.plugins.scenes.classifier import SceneClassification
from backend.app import schemas

SC = SceneClassification()

router = APIRouter()

@router.get("/", response_model=Dict)
def root():
    return {"message": "Welcome to Scene Classification Service."}

@router.put("/url/label/", response_model=List[schemas.SceneClassifierOutput], dependencies=[Depends(JWTBearer())])
async def scene_label_from_urls(images: List[str]):
    results = SC.img_urls_classification(images)
    return results

@router.put("/obj/label/", response_model=List[schemas.SceneClassifierOutput], dependencies=[Depends(JWTBearer())])
async def scene_label_from_img(image: object):
    results = SC.img_obj_classification(image)
    return results