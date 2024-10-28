import requests
import json

response = requests.get(
    url='https://api.warframe.market/v1/items/rolling_guard/orders',
    params={
        'include': 'item'
    }).json()

first = response['include']
# first['item'].pop('items_in_set')

second = response['include']
list = []

# print(json.dumps(first, indent=4))

# print(json.dumps(second, indent=4))

for i in first['item']['items_in_set']:
    i.pop('en')
    i.pop('ru')
    i.pop('ko')
    i.pop('sv')
    i.pop('de')
    i.pop('zh-hant')
    i.pop('zh-hans')
    i.pop('pt')
    i.pop('es')
    i.pop('pl')
    i.pop('cs')
    i.pop('uk')
    i.pop('fr')

    list.append(i)

first['item'].update({'items_in_set': list})
print(json.dumps(first, indent=4))
