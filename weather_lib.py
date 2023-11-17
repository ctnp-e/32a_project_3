
import json
import urllib.request

def weather_cords(lat: float,long: float) -> {dict}:
    '''
    given the coords, finds the link that tells me the 
    station it uses. given the station and the station coords,
    finds the hourly forecast for that particular place. 

    returns the json info to work with, so that the other
    hourly information function can work for both files and
    online requests
    '''
    original_request = 'https://api.weather.gov/points/'+str(round(float(lat),4))+','+str(round(float(long),4))
    
    request_points = urllib.request.Request(original_request)
    response_points = urllib.request.urlopen(request_points)
    data_points = response_points.read()
    
    points_json = dict(json.loads(data_points.decode(encoding = 'utf-8')))
    
    # print(get+'\n'+got)

    location_properties = points_json['properties']
    input_grid_x = location_properties['gridX']
    input_grid_y = location_properties['gridY']
    input_grid_id = location_properties['gridId']

    response_points.close()

    inbe = input_grid_id + '/' + str(input_grid_x) + ',' + str(input_grid_y)
    specifics_link = 'https://api.weather.gov/gridpoints/'+ inbe+'/forecast/hourly'
    # print(specifics_link)

    
    request_hourly = urllib.request.Request(specifics_link)
    response_hourly = urllib.request.urlopen(request_hourly)
    hourly = response_hourly.read()

    hourly_json = dict(json.loads(hourly.decode(encoding = 'utf-8')))

    response_hourly.close()
    return hourly_json


def hour_info(json_info: {dict}) -> {dict}:
    '''
    gets all the information provided for the most recent hour.
    this only uses the json stuff provided.
    '''
    all_i_care_about = json_info['properties']['periods'][0]
    return all_i_care_about

def hour_get_file(file_loc: str) -> {dict}:
    '''
    opens the file and turns it into a form that can actually be
    compatible with the hour_info function, so I can use this for
    testing my file instead of only online usability
    '''
    f = open(file_loc, "r")
    stuff = dict(json.loads(f.read()))
    return hour_info(stuff)