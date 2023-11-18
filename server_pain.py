
import json
import urllib.request, urllib.error

class NOT200Error(Exception):
    pass

class URLJsonFormatError(Exception):
    pass

class NetworkError(Exception):
    pass

class MissingFileError(Exception):
    pass

class FileJsonFormatError(Exception):
    pass

def get_json(url: str, header: str) -> dict:
    '''
    given the url and header, returns the dict
    and any posisble errors. 
    '''
    response = None
    status = None
    try:
        request = urllib.request.Request(url, None, header)
        response = urllib.request.urlopen(request)

        status = response.status
        if status != 200:
            print('FAILED')
            try: #prints status, only if it's an int
                status == int(status)
                print(status, url)
            except:
                print(url)
            print('NOT 200')
            raise NOT200Error
        
        possible_thing = response.read().decode(encoding = 'utf-8')
        
        try: 
            testing = json.loads(possible_thing)
        except json.JSONDecodeError:
            print('FAILED\n' + url)
            raise URLJsonFormatError
        json_it = json.loads(possible_thing)
        
        if type(json_it) == list:
            thingy = json_it[0]
        else:
            thingy = json_it

        return dict(thingy)
        
    except urllib.error.URLError:
        print('FAILED')
        print(url)
        raise NetworkError
    

    finally:
        if response != None:
            response.close()

def open_file(file_loc: str) -> {dict}:
    '''
    tries to open the given file or otherwise says
    the error thing. returns the file name
    '''
    open_file = None
    data_test = None
    try:
        open_file = open(file_loc, 'r')
        inside = json.load(open_file)
        if type(inside) == list:
            json_time = inside[0]
        else:
            json_time = inside
        data_test = json_time
    except FileNotFoundError:
        print('FAILED\n' + file_loc)
        raise MissingFileError
    except json.JSONDecodeError:
        print('FAILED\n' + file_loc)
        raise FileJsonFormatError
    finally:
        if open_file!= None and data_test != None:
            open_file.close()
            return data_test

