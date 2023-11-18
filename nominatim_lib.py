import json
import urllib.request
import server_pain as serv

NOMINATIM_HEADER = {'Referer' : 'https://www.ics.uci.edu/~thornton/ics32a/ProjectGuide/Project3/mmivanov'}

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
    
    stuff = serv.get_json(result, NOMINATIM_HEADER)
    return stuff

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

    stuff = serv.open_file(inp)

    return((stuff['lat'],stuff['lon']))

def rev_nominatim_search(long: float, lat: float):
    searchup = 'https://nominatim.openstreetmap.org/reverse?lat='+ long + '&lon=' + lat + '&format=json'
    
    stuff = serv.get_json(searchup, NOMINATIM_HEADER)
    return stuff['display_name']
    

def rev_nominatim_file(filepa: str) -> str:

    stuff = serv.open_file(filepa)
    return stuff['display_name']
