from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from PIL import Image
from typing import List, Dict
from app.auth.auth_bearer import JWTBearer
from plugins.scenes.classifier import SceneClassification
from app import schemas

SC = SceneClassification()

router = APIRouter()

@router.get("/", response_model=Dict)
def root():
    return {"message": "Welcome to Scene Classification Service."}

@router.put("/url/label/", response_model=List[schemas.SceneClassifierOutput], dependencies=[Depends(JWTBearer())])
async def scene_label_from_urls(images: List[str]):
    results = SC.img_urls_classification(images)
    return results

# @router.put("/obj/label/", response_model=List[schemas.SceneClassifierOutput], dependencies=[Depends(JWTBearer())])
# async def scene_label_from_img(image):
#     results = SC.img_obj_classification(image)
#     return results

@router.post("/obj/label/", response_model=List[schemas.SceneClassifierOutput], dependencies=[Depends(JWTBearer())])
async def scene_label_from_img(img: UploadFile):
    image = Image.open(img.file)
    result = SC.img_obj_classification(image, "./"+img.filename)
    return result