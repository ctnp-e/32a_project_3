import json
import urllib.request

def nominatim_search(inp: str) -> (float, float):
    '''
    takes a location and makes a valid link out of it.
    then reads the link, turns it into a dictionary
    and (in debug prints out the whole thing) then returns
    the latitude and longitude.
    '''
    searchup = 'https://nominatim.openstreetmap.org/search?q='
    res = inp.strip()

    parts = ''

    it = ((res.replace(' ', '+')).replace(',', '%2C')).replace('\'', '%27')
    result = searchup + it + '&format=json'

    request = urllib.request.Request(result)
    response = urllib.request.urlopen(request)
    data = response.read()

    stuff = dict(json.loads(data.decode(encoding = 'utf-8')[1:-1]))
    
    # for x in stuff:
    #     print(x + '\t\t' + str(stuff[x]))

    response.close()
    return((stuff['lat'],stuff['lon']))

def nominatim_file(inp:str ) -> (float, float):
    '''
    this is for debugging. serves the same purpose as 
    nominatim_search but for a specific file.
    '''
    f = open(inp, "r")
    stuff = dict(json.loads(f.read()[1:-1]))
    for x in stuff:
        print(x + '\t\t' + str(stuff[x]))

    f.close()
    return((stuff['lat'],stuff['lon']))
