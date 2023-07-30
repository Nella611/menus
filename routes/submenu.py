from typing import List
import uuid
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from .schemas.submenu import SubMenuChange, SubMenuShow
from models.submenu import SubMenu
from database import get_db

router = APIRouter()
db: Session = Depends(get_db)


@router.get(
        '/api/v1/menus/{menu_id}/submenus',
        response_model=List[SubMenuShow])
async def get_submenus(menu_id: str, db=db):
    submenus = db.query(SubMenu).filter(
        SubMenu.menu_id == menu_id).all()

    for submenu in submenus:
        submenu.dishes_count = submenu.dishes_count

    return submenus


@router.post('/api/v1/menus/{menu_id}/submenus', status_code=201)
async def create_submenu(menu_id: str,
                         submenu_data: SubMenuChange,
                         db=db):
    new_submenu = SubMenu(**submenu_data.dict(),
                          id=uuid.uuid4(),
                          menu_id=menu_id)
    db.add(new_submenu)
    db.commit()
    db.refresh(new_submenu)
    return new_submenu


@router.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}")
async def get_submenu(submenu_id: str,
                      menu_id: str,
                      db=db):
    submenu = db.query(SubMenu).filter(
        SubMenu.id == submenu_id, SubMenu.menu_id == menu_id).first()
    if not submenu:
        raise HTTPException(status_code=404, detail="submenu not found")
    return submenu


@router.patch('/api/v1/menus/{menu_id}/submenus/{submenu_id}')
async def update_submenu(submenu_id: str,
                         menu_id: str,
                         submenu_data: SubMenuChange,
                         db=db):
    submenu = db.query(SubMenu).filter(
        SubMenu.id == submenu_id, SubMenu.menu_id == menu_id).first()
    if not submenu:
        raise HTTPException(status_code=404, detail="submenu not found")

    for key, value in submenu_data.dict().items():
        setattr(submenu, key, value)

    db.commit()
    db.refresh(submenu)

    return submenu


@router.delete('/api/v1/menus/{menu_id}/submenus/{submenu_id}')
async def delete_submenu(menu_id: str, submenu_id: str,
                         db=db):
    submenu = db.query(SubMenu).filter(
        SubMenu.id == submenu_id, SubMenu.menu_id == menu_id).first()
    if not submenu:
        raise HTTPException(status_code=404, detail="submenu not found")

    db.delete(submenu)
    db.commit()
