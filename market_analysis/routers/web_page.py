from fastapi import APIRouter, Request, Response
from fastapi.templating import Jinja2Templates
from fastapi_cache.decorator import cache
from market_analysis.localization.localization import i18n
from market_analysis.db.session import sessionmanager
from market_analysis.db.dals.order_dal import OrderDAL
from market_analysis.feature.filter import filter_orders

router = APIRouter(
    tags=['TradeWARF']
)

templates = Jinja2Templates(directory='templates/web')


@router.get('/')
async def get_home_page(response: Response, request: Request):
    lng: dict = await i18n.get_language('ru')
    return templates.TemplateResponse('home.html', {'request': request,
                                                    'navigation': lng.get('navigation'),
                                                    'about': lng.get('about')})


@router.get('/arcane')
async def get_arcane_page(response: Response, request: Request):
    lng: dict = await i18n.get_language('ru')
    async with sessionmanager.session() as session:
        order_dal = OrderDAL(session)
        orders = await order_dal.get_all_orders()
        result = await filter_orders(orders)
        print(result)
        return templates.TemplateResponse('arcane.html', {'request': request,
                                                          'navigation': lng.get('navigation'),
                                                          'arcanes': result})


@router.get('/guns')
async def get_guns_page(response: Response, request: Request):
    lng: dict = await i18n.get_language('ru')
    return templates.TemplateResponse('guns.html', {'request': request,
                                                    'navigation': lng.get('navigation')})


@router.get('/primed_mods')
async def get_teshin_shop(response: Response, request: Request):
    lng: dict = await i18n.get_language('ru')
    return templates.TemplateResponse('primed_mods.html', {'request': request,
                                                           'navigation': lng.get('navigation')})


@router.get('/teshin_shop')
async def get_teshin_shop(response: Response, request: Request):
    lng: dict = await i18n.get_language('ru')
    return templates.TemplateResponse('teshin_shop.html', {'request': request,
                                                           'navigation': lng.get('navigation')})
