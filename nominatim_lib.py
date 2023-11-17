import json
import urllib.request

def nominatim_info(inp:str) -> {dict}:
    '''
    takes a location and makes a valid link out of it.
    then reads the link, turns it into a dictionary
    '''
    searchup = 'https://nominatim.openstreetmap.org/search?q='
    res = inp.strip()

    parts = ''

    it = ((res.replace(' ', '+')).replace(',', '%2C')).replace('\'', '%27')
    result = searchup + it + '&format=json'
    try:
        request = urllib.request.Request(result)
        response = urllib.request.urlopen(request)
        data = response.read()

        stuff = dict(json.loads(data.decode(encoding = 'utf-8')[1:-1]))
        
        response.close()
        return stuff
    except:
        print('FAILED')

def nominatim_search(inp: str) -> (float, float):
    '''
    from the nominatim_info function, gets the lat and lon
    '''
    nom_dict = nominatim_info(inp)
    return((nom_dict['lat'],nom_dict['lon']))


def nominatim_file(inp:str ) -> (float, float):
    '''
    this is for debugging. serves the same purpose as 
    nominatim_search but for a specific file.
    '''
    f = open(inp, "r")
    stuff = dict(json.loads(f.read()[1:-1]))

    f.close()
    return((stuff['lat'],stuff['lon']))

def nominatim_display_search(inp: str) -> str:
    '''
    from the nominatim_info function, returns the display
    '''
    nom_dict = nominatim_info(inp)
    return(nom_dict['display_name'])

def nominatim_display_file(inp: str) -> str:
    '''
    from the nominatim_info function, returns the display
    '''
    f = open(inp, "r")
    stuff = dict(json.loads(f.read()[1:-1]))

    f.close()
    return(stuff['display_name'])