from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Request
from loguru import logger
from datetime import datetime
from typing import Optional
from sqlalchemy import text
from pydantic import BaseModel
from sqlalchemy.orm import Session
from psycopg2.extras import RealDictCursor

from db.db import get_db, get_raw_db,SessionLocal
from db.models import Users

uapp=APIRouter()

@uapp.get("/get_users",tags=['Users'])
def get_users(request:Request,db:Session=Depends(get_db),rdb:Session=Depends(get_raw_db)):
    try:
        cursor=rdb.cursor(cursor=RealDictCursor)
        query='''select id,username,first_name,last_name,email from users'''
        cursor.execute(query)
        res=cursor.fetchall()
        return res
    except Exception as e :
        logger.error(e)
        raise e

