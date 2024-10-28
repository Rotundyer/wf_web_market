from fastapi import APIRouter, Request, Response
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from market_analysis.localization.localization import i18n
from market_analysis.db.session import sessionmanager
from market_analysis.db.dals.arcane_location_dal import ArcaneLocationDAL
from market_analysis.db.dals.item_dal import ItemDAL
from market_analysis.settings import API_HOST, API_PORT, API_VERSION

router = APIRouter(
    prefix='/admin',
    tags=['TradeWARF']
)

templates = Jinja2Templates(directory='templates/admin')


@router.get('/')
async def redirect(response: Response):
    return RedirectResponse('/admin/items')


@router.get('/items')
async def get_items_page(response: Response, request: Request):
    lng: dict = await i18n.get_language('ru')
    async with sessionmanager.session() as session:
        item_dal = ItemDAL(session)
        items = await item_dal.get_all_items()
        return templates.TemplateResponse('items.html', {'request': request,
                                                         'items': items,
                                                         "admin_items": lng.get('admin_items'),
                                                         'host': f'{API_HOST}:{API_PORT}/api/{API_VERSION}'})


@router.get('/approve_item')
async def get_approve_item_page(response: Response, request: Request):
    lng: dict = await i18n.get_language('ru')
    async with sessionmanager.session() as session:
        arcane_location_dal = ArcaneLocationDAL(session)
        locations = await arcane_location_dal.get_all_location()
        return templates.TemplateResponse('approve_item.html',
                                          {'request': request,
                                           'locations': locations,
                                           'admin_approve_location': lng.get('admin_approve_location'),
                                           'host': f'{API_HOST}:{API_PORT}/api/{API_VERSION}'})


@router.get('/approve_arcane_location')
async def get_approve_arcane_location(response: Response, request: Request):
    lng: dict = await i18n.get_language('ru')
    async with sessionmanager.session() as session:
        arcane_location_dal = ArcaneLocationDAL(session)
        locations = await arcane_location_dal.get_all_location()
        return templates.TemplateResponse('approve_arcane_location.html',
                                          {'request': request,
                                           'locations': locations,
                                           'admin_location': lng.get('admin_location'),
                                           'host': f'{API_HOST}:{API_PORT}/api/{API_VERSION}'})
