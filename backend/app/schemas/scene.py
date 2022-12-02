from typing import List, Optional
#from datetime import datetime
from pydantic import BaseModel
from typing import List, Dict

# Shared properties
class SceneClassifierBase(BaseModel):
    image_url: str

# Properties to return to client
class SceneClassifierOutput(SceneClassifierBase):
    scene_label: str
    scores: Dict
    #classified_at: datetime