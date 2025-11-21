# app/api/routes/dropbox_routes.py
from fastapi import APIRouter, HTTPException

from app.dropbox import service as dropbox_service

router = APIRouter()


@router.get("/wise4051/co2/all", summary="ดึง CO2 จาก WISE-4051 ทั้งหมด")
def wise4051_co2_all():
    try:
        return dropbox_service.get_co2_all()
    except Exception as e:
        # log จริง ๆ ควรใช้ logger แต่เอาง่าย ๆ ก่อน
        print("ERROR in wise4051_co2_all:", e)
        raise HTTPException(status_code=500, detail="Dropbox CO2 error")


@router.get("/wise4012/all", summary="ดึง Temperature + Humidity จาก WISE-4012 ทั้งหมด")
def wise4012_all():
    try:
        return dropbox_service.get_temp_humid_all()
    except Exception as e:
        print("ERROR in wise4012_all:", e)
        raise HTTPException(status_code=500, detail="Dropbox temp/humid error")
