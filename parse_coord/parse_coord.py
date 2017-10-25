import pandas as pd
import requests
import time

df = pd.read_csv('addresses.csv', sep=';')
coord = []
json_list = []
for i, (addr, atm) in enumerate(list(zip(df['ADDRESS'], df['ATM'])), 1):
    print (i)
    addresses = [
        ' '.join(['г. Алматы', atm, addr]),
        ' '.join(['г. Алматы', addr]),
        ' '.join([atm, addr]),
        addr
    ]

    for address in addresses:
        try:
            link = 'http://geocode-maps.yandex.ru/1.x/?format=json&geocode=' + address + '&results=1'
            r = requests.get(link).json()
            pair = r['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
            x, y = pair.split(' ')
            adm_name = r['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty']['GeocoderMetaData']['AddressDetails']['Country']['AdministrativeArea']['AdministrativeAreaName']
            coord.append( {
                    'address':address,
                    'x':x,
                    'y':y,
                    'adm_name': adm_name
                }
            )
            print ('\n'.join([address, pair, adm_name]))
            json_item =  {
                        "type": "Feature",
                        "id": i,
                        "geometry": {
                            "type": "Point",
                            "coordinates": [
                                float(y),
                                float(x)
                            ]
                        }
                    }
            json_list.append(json_item)
            time.sleep(1)
            break
        except:
            print ('Some error')
            time.sleep(1)
            pass

df_coord = pd.DataFrame(coord)
df_coord.to_csv('coord.csv', index=None)

import json
with open('json.txt', 'w') as outfile:
    json.dump(json_list, outfile)