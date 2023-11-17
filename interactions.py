import nominatim_lib as nomlib
import weather_lib as wlib
from datetime import datetime, timezone


def first_line_input() -> (str, int):
    '''
    (file or location, type)
    This will return the original phrase, as well as 
    whether the thing to handle is a filepath or a location.
    0 - ocation
    1 - filepath
    '''
    phrase_location = 'TARGET NOMINATIM '
    phrase_file = 'TARGET FILE '

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
    phrase_file = 'WEATHER FILE '

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

def first_line_brains(phrase: str, type: int) -> ({dict},str,str,bool):
    '''
    tells you what to do with the input. you input the phrase
    and the type and then you return the json dictionary of 
    the location
    '''
    used_nom = False
    if type == 0:
        lat, long = nomlib.nominatim_search(phrase)
        dict_to_return = wlib.weather_cords(lat, long)
        used_nom = True
    elif type == 1:
        lat, long = nomlib.nominatim_file(phrase)
        dict_to_return = phrase
    else:
        return None
    
    return(dict_to_return,lat ,long,used_nom)

def lat_long_target(lat: float, long: float)->str:
    '''
    so you can print it later
    '''
    latlongprint = 'TARGET '
    if float(lat) >= 0:
        latlongprint += lat + '/N '
    else:
        latlongprint += str((-1.0)*float(lat)) + '/S '

    if float(long) >= 0:
        latlongprint += long + '/E'
    else:
        latlongprint += str((-1.0)*float(long)) + '/W'

    return latlongprint

def second_line_brains(first_line_json: {dict}, type:int, possible_phrase:str) -> ({dict},bool):
    '''
    given the dictionary found from the first line(origin point)
    tells you what type of weather (file or nws) is required
    and returns the corresponding hourly info
    '''
    used_wsm = False
    if type == 0:
        ret = wlib.hour_info(first_line_json)
        used_wsm = True
    elif type == 1:
        ret = wlib.hour_get_file(possible_phrase)
    else:
        return None
    
    return (ret, used_wsm)

def third_line_loopy() -> ((str, int)):
    '''
    (follows, phrase value)
    returns whatever follows the chosen phrase
    as well as the value of the phrase. to be used
    in other functions
    0 - TEMPERATURE AIR 
    1 - TEMPERATURE FEELS 
    2 - HUMIDITY
    3 - WIND
    4 - PRECIPITATION
    5 - NO MORE QUERIES
    '''

    phrases = ['TEMPERATURE AIR ','TEMPERATURE FEELS ','HUMIDITY ','WIND ','PRECIPITATION ','NO MORE QUERIES']

    while True:
        inp = input().strip()
        upper_temp = inp.upper()
        for x in range(len(phrases)):
            phrase = phrases[x]
            if phrase in upper_temp:
                if phrase == phrases[5] and upper_temp == phrase:
                    return ('NO MORE QUERIES', 5)
                elif upper_temp.index(phrase) == 0:
                    return((inp[(len(phrase)):],x))


def which_function(json_file: {dict}, third_line_input: str, third_line_int: int) -> str:
    '''
    just runs the actual functions and puts them in a format that kind of keeps
    them for later. Also takes the timestamp and converts it to UTC and adds it 
    to waht needs to be printed

    '''
    #
    # i must say, the utc stuff is the worst. it's already in UTC (we can tell by the +00:00)
    # and to make it Z is a little bit extra, is it not?! all of it will end in 00Z anyways,
    # it all looks the same.

    parts = third_line_input.split(' ')
    # ind is index of the time
    # printy is the part i should be printing.
    match third_line_int:
        case 0:
            ind, printy = wlib.temperature_air(json_file, parts[0], int(parts[1]), parts[2])
        case 1:
            ind, printy = wlib.temperature_feels(json_file, parts[0], int(parts[1]), parts[2])
        case 2:
            ind, printy = wlib.humidity(json_file, int(parts[0]), parts[1])
            printy += '%'
        case 3:
            ind, printy = wlib.wind(json_file, int(parts[0]), parts[1])
            printy += ' mph'
        case 4:
            ind, printy = wlib.precip(json_file, int(parts[0]), parts[1])
            printy += '%'
        case 5:
            ind = -1
            printy = ''
    

    # PRINTS TIME. THIS TOOK ME AN HOUR
    time_portion = json_file[ind]['startTime']
    parsed_date = datetime.strptime(time_portion, "%Y-%m-%dT%H:%M:%S%z" ).timestamp()
    time_utc = datetime.fromtimestamp(parsed_date, timezone.utc).isoformat()
    print_time_utc = str(time_utc)[:-6]+'Z'
    

    toprint = print_time_utc + ' ' + printy

    return(toprint)


def reverse_end()-> (str, int):
    '''
    returns the request plus whether it is a file
    or a search request.
    0 - search
    1 - file
    '''
    phrase_location = 'REVERSE NOMINATIM'
    phrase_file = 'REVERSE FILE '

    while True:
        
        inp = input()
        upper_temp = inp.upper()
        
        if phrase_location in upper_temp:
            if upper_temp.index(phrase_location) == 0:
                return(inp[(len(phrase_location)):],0)
        
        if phrase_file in upper_temp:
            if upper_temp.index(phrase_file) == 0:
                try:
                    open(inp[len(phrase_file):], "r")
                    return(inp[len(phrase_file):],1)
                except IOError:
                    print('filepath not real')

def reverse_brains(type: int, phrase: str, lat: float, long: float) -> (str, bool):
    '''
    determines whether the reverse is a file or a link and gets the
    complementary display name.
    '''
    used_rev_nom = False
    if type == 0:
        disp = nomlib.rev_nominatim_search(lat, long)
        used_rev_nom = True
    elif type == 1:
        disp = nomlib.rev_nominatim_file(phrase)
    else:
        return None
    
    return(disp,used_rev_nom)

def attribution_messages(for_geo: bool, rev_geo: bool, nws_use: bool):
    '''
    wraps up output with attribution messages
    '''
    if for_geo:
        print('\t**Forward geocoding data from OpenStreetMap')
    if rev_geo:
        print('\t**Reverse geocoding data from OpenStreetMap')
    if nws_use:
        print('\t**Real-time weather data from National Weather Service, United States Department of Commerce')