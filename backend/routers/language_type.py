from fastapi import APIRouter
from utils import is_regular

router = APIRouter(tags=["Language Type"],prefix="/language_type")



@router.get("/isregular/{string_to_test}")
async def is_regular(string_to_test: str):
    regular = is_regular(string_to_test)
    


