# app/api/routes/carbon_routes.py
from fastapi import APIRouter, Query

from app.dropbox import service as dropbox_service

router = APIRouter(prefix="/dropbox", tags=["dropbox"])


@router.get("/wise4051/co2/all", name="co2all")
def co2_all():
    return dropbox_service.get_co2_all()


@router.get("/wise4051/co2/daily", name="co2daily")
def co2_daily(date: str = Query(..., description="วันที่รูปแบบ YYYYMMDD")):
    return dropbox_service.get_co2_daily(date)


@router.get("/wise4012/temp/all", name="tempall")
def temp_all():
    return dropbox_service.get_temp_all()


@router.get("/wise4012/temp/daily", name="tempdaily")
def temp_daily(date: str = Query(..., description="วันที่รูปแบบ YYYYMMDD")):
    return dropbox_service.get_temp_daily(date)


@router.get("/wise4012/humid/all", name="humidall")
def humid_all():
    return dropbox_service.get_humid_all()


@router.get("/wise4012/humid/daily", name="humiddaily")
def humid_daily(date: str = Query(..., description="วันที่รูปแบบ YYYYMMDD")):
    return dropbox_service.get_humid_daily(date)
