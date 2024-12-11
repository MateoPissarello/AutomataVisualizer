from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from .utils import check_language

router = APIRouter(tags=["Language Type"], prefix="/language_type")


# Definir un modelo para recibir el lenguaje
class LanguageRequest(BaseModel):
    language: List[str] | str


@router.post("/isregular")
async def is_regular(request: LanguageRequest):
    results, is_regular = check_language(request.language)
    return {"results": results, "is_regular": is_regular}
