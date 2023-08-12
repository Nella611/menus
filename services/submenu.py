from uuid import UUID

from fastapi import Depends
from fastapi.responses import JSONResponse

from repositories.submenu import SubMenuRepository
from schemas.submenu import BaseSubMenu, SubMenuShow
from services.cache import MENU_CACHE_NAME, SUBMENU_CACHE_NAME, CacheRepositorySubMenu


class SubMenuService:
    def __init__(self, submenu_repository=Depends(SubMenuRepository)):
        self.submenu_repository = submenu_repository
        self._redis = CacheRepositorySubMenu()

    async def create(self,
                     menu_id: UUID,
                     submenu_data: BaseSubMenu) -> SubMenuShow:
        new_submenu = await self.submenu_repository.create(
            menu_id,
            submenu_data)
        self._redis.create_update(menu_id=menu_id,
                                  submenu_id=new_submenu.id,
                                  data=new_submenu)
        return new_submenu

    async def update(self,
                     menu_id: UUID,
                     submenu_id: UUID,
                     submenu_data: BaseSubMenu) -> SubMenuShow:
        update_submenu = await self.submenu_repository.update(submenu_id,
                                                              submenu_data)
        self._redis.create_update(menu_id=menu_id,
                                  submenu_id=submenu_id,
                                  data=update_submenu)
        return update_submenu

    async def get_all(self, menu_id: UUID) -> list[SubMenuShow]:
        key_submenus = f'{MENU_CACHE_NAME}{menu_id}{SUBMENU_CACHE_NAME}'
        if self._redis.exists(key_submenus):
            return self._redis.get(key_submenus)
        submenus = await self.submenu_repository.get_all(menu_id)
        self._redis.set_all(key=key_submenus, data=submenus)
        return submenus

    async def get_by_id(self,
                        menu_id: UUID,
                        submenu_id: UUID) -> SubMenuShow:
        key_submenu = f'{MENU_CACHE_NAME}{menu_id}' \
                      f'{SUBMENU_CACHE_NAME}{submenu_id}'
        if self._redis.exists(key_submenu):
            return self._redis.get(key_submenu)
        submenu = await self.submenu_repository.get_by_id(submenu_id)
        self._redis.set(key=key_submenu, data=submenu)
        return submenu

    async def delete(self, menu_id: UUID, submenu_id: UUID) -> JSONResponse:
        response = await self.submenu_repository.delete(submenu_id)
        self._redis.delete(menu_id=menu_id, submenu_id=submenu_id)
        return response
