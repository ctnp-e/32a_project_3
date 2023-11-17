import json
import urllib.request

def nominatim_search(inp: str) -> (float, float):
    searchup = 'https://nominatim.openstreetmap.org/search?q='
    res = inp.strip()

    parts = ''

    it = ((res.replace(' ', '+')).replace(',', '%2C')).replace('\'', '%27')
    result = searchup + it + '&format=json'

    request = urllib.request.Request(result)
    response = urllib.request.urlopen(request)
    data = response.read()

    stuff = dict(json.loads(data.decode(encoding = 'utf-8')[1:-1]))
    
    for x in stuff:
        print(x + '\t\t' + str(stuff[x]))

    response.close()
    return((stuff['lat'],stuff['lon']))
    