
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
    print(specifics_link)

    
    request_hourly = urllib.request.Request(specifics_link)
    response_hourly = urllib.request.urlopen(request_hourly)
    hourly = response_hourly.read()

    hourly_json = dict(json.loads(hourly.decode(encoding = 'utf-8')))
    # print(hourly_json)
    response_hourly.close()
    return hourly_json


def hour_info(json_info: {dict}) -> {dict}:
    '''
    gets all the information provided for all the next 156 hours...
    its a lot of info.
    '''
    all_i_care_about = json_info['properties']['periods']
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

def convert(temp: float, desired_output: str) -> float:
    '''
    converts whatever value you want
    into the desired type (f or c)
    this works on the assumption that you do NOT have the
    type you currently want'''
    if desired_output == 'F':
        return(round((temp * 9.0 / 5.0 + 32.0),2))
    elif desired_output == 'C':
        return(round(((temp - 32.0) * 5.0 / 9.0),2))
    else:
        print('invalid desired output')
        return(None)

def minmaxxingthis(list_to_worry: [list], min_or_max: str) -> (int, float):
    '''
    my attempt at making this more efficient. I kept copy pasting
    this stupid part so i just made it more efficient, hence the
    name of "min maxxing." its a common tacting in mmorpgs to try
    to find the most optimal setup on a characer, every minimum and
    maximum possible. i love puns and i love mmorpgs. 
    '''
    index_to_record = 0
    if min_or_max.strip().lower() == 'min':
        ret = min(list_to_worry)
        index_to_record = find_min(list_to_worry)
    elif min_or_max.strip().lower() == 'max':
        ret = max(list_to_worry)
        index_to_record = find_max(list_to_worry)
    else:
        print('did not type min or max')
        return None
    
    return(index_to_record, ret)

def find_max(vals: [float]) -> int:
    '''
    finds index of max value
    '''
    max_index = 0
    for x in range(len(vals)):
        if vals[x] > vals[max_index]:
            max_index = x
    
    return max_index

def find_min(vals: [float]) -> int:
    '''
    finds index of min value
    '''
    min_index = 0
    for x in range(len(vals)):
        if vals[x] < vals[min_index]:
            min_index = x
    
    return min_index

def package_to_return(special_index: int, val) -> tuple:
    '''
    essentially packages up what i want to return in the
    general weather lib third line functions. makes it consistent
    and so i dont have to repeat the same thing over and over
    '''
    if type(val) == float or type(val) == int:
        return((special_index, format(val, '.4f')))
    else:
        return((special_index, val))

def temperature_air(json_file: {dict}, temp_type: str, time_length: int, min_or_max: str) -> int:
    '''
    finds the max or minimum temperature over the given
    timescale. goes into the periods given and pulls all
    temps and finds max or min, and adjusts the temp type
    according to what is desired.
    '''
    temps = []
    for x in range(time_length):
        val = json_file[x]['temperature']
        temps.append(val)
    
    index_to_record, ret = minmaxxingthis(temps, min_or_max)
    

    if(json_file[0]['temperatureUnit']) != temp_type:
        ret = convert(float(ret), temp_type.strip().upper())
    
    return package_to_return(index_to_record, ret)


def temperature_feels(json_file: {dict}, temp_type: str, time_length: int, min_or_max: str) -> float:
    '''
    given the periods, temp type, the time period, and max or min,
    applies the formula to each individual period to find what it
    would feel like. appends it to a list of all the feels like temps,
    and then finds either the min or max or the value (depending
    on waht the user wants)
    '''

    feels_like = []
    for x in range(time_length):
        res = 0
        period = json_file[x]
        temp = float(period['temperature'])
        if period['temperatureUnit'] != 'F':
            temp = convert(temp,'F')

        wind = float(period['windSpeed'].split(' ')[0])
        humidity = float(period['relativeHumidity']['value'])

        if temp >= 68:
            res = -42.379 \
            + (2.04901523) * temp               \
            + (10.14333127) * humidity          \
            + (-0.22475541)*temp*humidity       \
            + (-0.00683783)*temp**2             \
            + (-0.05481717)*humidity**2         \
            + (0.00122874)*(temp**2)*humidity   \
            + (0.00085282)*temp*(humidity**2)   \
            + (-0.00000199)*(temp**2)*(humidity**2)
        elif temp <= 50 and wind > 3:
            res = 35.74                         \
            + 0.6213 * temp                     \
            + (-35.75) * wind**0.16             \
            + (0.4275) * temp * wind**0.16      
        else:
            res = temp

        feels_like.append(res)

    index_to_record,ret = minmaxxingthis(feels_like, min_or_max)
    
    if(json_file[0]['temperatureUnit']) != temp_type:
        ret = convert(float(ret), temp_type.strip().upper())
    
    return package_to_return(index_to_record, ret)


def humidity(json_file: {dict}, time_length: int, min_or_max: str) -> str:
    '''
    collects all the humidity values in teh time length asked for
    and tehn finds either the minimum or maximum of the list.
    returns it as the value + % cause it looks nice
    '''
    humid_list = []
    index_to_record = 0
    for x in range(time_length):
        period = json_file[x]
        humid_list.append((period['relativeHumidity']['value']))
    
    index_to_record, ret = minmaxxingthis(humid_list, min_or_max)
    
    return package_to_return(index_to_record, (str(format(ret, '.4f')) + '%'))

