import nominatim_lib as nomlib
import weather_lib as wlib

def file_test():
    # inp = input('TARGET NOMINATIM ')
    # inp = ('donald bren hall, irvine')
    inp = 'nominatim_center.json'
    #lat, long = server.nominatim_search(inp)
    
    lat, long = nomlib.nominatim_file(inp)
    wlib.weather_file(float(lat),float(long))
    print(lat + ' ' + long)


if __name__ == '__main__':
    file_test()