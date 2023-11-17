import nominatim_lib as nomlib
import weather_lib as wlib

def file_test():
    # inp = input('TARGET NOMINATIM ')
    # inp = ('donald bren hall, irvine')
    inp = 'nominatim_center.json'

    #lat, long = server.nominatim_search(inp)
    
    lat, long = nomlib.nominatim_file(inp)
    fart_noise = wlib.weather_cords(float(lat),float(long))

    wlib.hour_info(fart_noise)

def first_line_input() -> (str, int):
    '''
    (file or location, type)
    This will return the original phrase, as well as 
    whether the thing to handle is a filepath or a location.
    0 - ocation
    1 - filepath
    '''
    phrase_location = 'TARGET NOMINATIM'
    phrase_file = 'TARGET FILE'

    while True:
        
        inp = input()
        upper_temp = inp.upper()
        
        if phrase_location in upper_temp:
            if upper_temp.index(phrase_location) == 0:
                return((inp[17:],0))
        
        if phrase_file in upper_temp:
            if upper_temp.index(phrase_file) == 0:
                try:
                    open(inp[12:], "r")
                    return((inp[12:],1))
                except IOError:
                    print('filepath not real')
                
def second_line_input() -> (str, int):
    '''
    (file or location, type)
    This is the same as the first input essentially,
    but weather specific.

    0 - NWS is only way to go
    1 - filepath
    '''
    phrase_location = 'WEATHER NWS'
    phrase_file = 'WEATHER FILE'

    while True:
        
        inp = input()
        upper_temp = inp.upper()
        
        if phrase_location in upper_temp:
            if upper_temp.index(phrase_location) == 0:
                return(('nws_go_go_go',0)) # empty because nothing 
        
        if phrase_file in upper_temp:
            if upper_temp.index(phrase_file) == 0:
                try:
                    open(inp[13:], "r")
                    return((inp[13:],1))
                except IOError:
                    print('filepath not real')

def first_line_brains(phrase: str, type: int) -> {dict}:
    '''
    tells you what to do with the input
    '''
    if type == 0:
        lat, long = nomlib.nominatim_search(phrase)
    elif type == 1:
        lat, long = nomlib.nominatim_file(phrase)
    else:
        return None
    
    return(wlib.weather_cords(lat, long))

def second_line_brains(first_line_json: {dict}, type:int, possible_phrase:str) -> {dict}:
    if type == 0:
        ret = wlib.hour_info(first_line_json)
    elif type == 1:
        ret = wlib.hour_get_file(possible_phrase)
    else:
        return None
    
    return ret


