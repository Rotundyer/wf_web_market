import os
import json
from fastapi_cache.decorator import cache


class Localization:
    def __init__(self):
        self.path: str = f'{os.path.dirname(os.path.abspath(__file__))}\\lngs'
        self.languages = {}

    async def get_language(self, language: str = 'en') -> dict:
        match language:
            case 'en':
                if self.languages.get('en') is None:
                    return await self._get_en()
                return self.languages.get('en')
            case 'ru':
                if self.languages.get('ru') is None:
                    return await self._get_ru()
                return self.languages.get('ru')

    async def _get_en(self) -> dict:
        try:
            with open(f'{self.path}\\en.json', 'r', encoding='utf8') as json_lng:
                lng: dict = json.load(json_lng)
                json_lng.close()
                self.languages.update({'en': lng})
                return lng
        finally:
            json_lng.close()

    async def _get_ru(self) -> dict:

        try:
            with open(f'{self.path}\\ru.json', 'r', encoding='utf8') as json_lng:
                lng: dict = json.load(json_lng)
                self.languages.update({'ru': lng})
                return lng
        finally:
            json_lng.close()


i18n = Localization()
