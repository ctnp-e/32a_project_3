import interactions as inter
import server_pain as serv

def run():

    line_1 = input()
    line_2 = input()
    line_3 = input()
    possible_inputs = []

    while line_3.strip().upper() != 'NO MORE QUERIES':
        possible_inputs.append(line_3)
        line_3 = input()
    
    possible_inputs.append('NO MORE QUERIES')
    line_rev = input()

    toprint = ''
    for_geo_open = False
    rev_geo_open = False
    nws_use = False
    first_phrase, type = inter.first_line_input(line_1)
    first_result, lat, long, for_geo_open = inter.first_line_brains(first_phrase, type)

    second_phrase, type = inter.second_line_input(line_2)
    second_result,nws_use = inter.second_line_brains(first_result, type, second_phrase)

    going = 0

    one, two = inter.third_line_loopy(possible_inputs[going])
    while two!= 5:
        going +=1
        toprint += inter.which_function(second_result, one, two) + '\n'
        one, two = inter.third_line_loopy(possible_inputs[going])
    
    
    rev_phrase, type = inter.reverse_end(line_rev)
    rev_disp, rev_geo_open = inter.reverse_brains(type, rev_phrase, lat, long)
    print(inter.lat_long_target(lat,long) + '\n' +rev_disp)
    print(toprint)
    inter.attribution_messages(for_geo_open, rev_geo_open, nws_use)

if __name__ == '__main__':
    error = []
    try:
        run()
    except serv.NOT200Error:
        print('NOT 200')
    except serv.URLJsonFormatError:
        print('FORMAT')
    except serv.NetworkError:
        print('NETWORK')
    except serv.MissingFileError:
        print('MISSING')
    except serv.FileJsonFormatError:
        print('FORMAT')
    # except Exception as e:
    #     print(e)


    
