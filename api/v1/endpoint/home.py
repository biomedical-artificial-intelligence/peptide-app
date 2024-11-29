from fastapi import APIRouter, Depends, HTTPException


router = APIRouter()


@router.get("")
async def homepage():
    return {"message": "H O M E P A G E"}