from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Request
from loguru import logger
from datetime import datetime
from typing import Optional
from sqlalchemy import text
from pydantic import BaseModel
from sqlalchemy.orm import Session
from psycopg2.extras import DictCursor

from db.db import get_db, get_raw_db,SessionLocal
from db.models import Notes

napp=APIRouter()

@napp.get("/get_notes",tags=['Notes App'])
def get_notes(request:Request,db:Session=Depends(get_db),rdb:Session=Depends(get_raw_db)):
    try :
        # cursor=rdb.cursor(cursor=DictCursor) ## for pymysql not for postgresql
        cursor=rdb.cursor(cursor_factory=DictCursor)
        query='''select * from notes'''
        cursor.execute(query)
        res=cursor.fetchone()
        logger.info(res["title"])
        return res
        
    except Exception as e :
        logger.error(e)
        # raise e
    
class ADDNOTE(BaseModel):
    title:str
    note:str=None
    important:bool=False
    archive:bool=False
@napp.post("/add_note",tags=['Notes App'])
def add_note(request:Request,new_note:ADDNOTE,db:Session=Depends(get_db),rdb:Session=Depends(get_raw_db)):
    try:
        add_note=Notes(
            title=new_note.title,
            note=new_note.note,
            important=new_note.important,
            archive=new_note.archive
        )
        db.add(add_note)
        db.commit()
        
        return {
            "status code":200,
            "data":"Note Added Successfully"
        }
    
    except Exception as e :
        logger.error(e)
        raise e

class EDITNOTE(BaseModel):
    id:int
    title:str
    note:str=None
    important:bool
    archive:bool
@napp.put("/edit_notes",tags=["Notes App"])
def edit_note(request:Request,edit:EDITNOTE,db:Session=Depends(get_db),rdb:Session=Depends(get_raw_db)):
    try:
        upd_note=db.query(Notes).filter_by(id=edit.id).update({
            "title":edit.title,
            "note":edit.note,
            "important":edit.important,
            "archive":edit.archive
        })
        db.commit()
        
        return {
            "status code":200,
            "data":"Note Updated Successfully"
        }    
    except Exception as e:
        logger.error(e)
        raise e
    
@napp.delete("/delete_note",tags=['Notes App'])
def delete_note(request:Request,note_id:int,db:Session=Depends(get_db),rdb:Session=Depends(get_raw_db)):
    try:
        cursor=rdb.cursor(cursor_factory=DictCursor)
        query=f'''delete from notes where id={note_id}'''
        cursor.execute(query)
        
        return {
            "status code":200,
            "data":"Note Deleted Successfully"
        }
    except Exception as e :
        logger.error(e)
        raise e