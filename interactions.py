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
                

def first_line_brains(phrase: str, type: int) -> (int, int):
    '''
    tells you what to do with the input
    '''
    if type == 0:
        lat, long = nomlib.nominatim_search(phrase)
    elif type == 1:
        lat, long = nomlib.nominatim_file(phrase)
    else:
        return None
    
    return((lat, long))


if __name__ == '__main__':
    #print(first_line())
    file_test()