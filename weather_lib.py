
import json
import urllib.request

def weather_file(lat: float,long: float):
    original_request = 'https://api.weather.gov/points/'+str(round(lat,4))+','+str(round(long,4))
    
    request = urllib.request.Request(original_request)
    response = urllib.request.urlopen(request)
    data = response.read()
    
    stuff = dict(json.loads(data.decode(encoding = 'utf-8')))
    
    # print(get+'\n'+got)

    location_properties = stuff['properties']
    input_grid_x = location_properties['gridX']
    input_grid_y = location_properties['gridY']
    input_grid_id = location_properties['gridId']

    inbe = input_grid_id + '/' + str(input_grid_x) + ',' + str(input_grid_y)
    specifics_link = 'https://api.weather.gov/gridpoints/'+ inbe+'/forecast'
    print(specifics_link)

    response.close()
