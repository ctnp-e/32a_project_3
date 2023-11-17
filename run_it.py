import interactions as inter

if __name__ == '__main__':
    toprint = ''
    for_geo_open = False
    rev_geo_open = False
    nws_use = False
    first_phrase, type = inter.first_line_input()
    first_result, lat, long, for_geo_open = inter.first_line_brains(first_phrase, type)

    second_phrase, type = inter.second_line_input()
    second_result,nws_use = inter.second_line_brains(first_result, type, second_phrase)

    
    # print(wlib.temperature_air(second_result, 'C', 24, 'max'))
    # print(wlib.temperature_feels(second_result, 'F', 24, 'max'))
    # print(wlib.humidity(second_result,24,'max'))
    # print(wlib.wind(second_result,24,'max'))
    # print(wlib.precip(second_result,24,'max'))
    one, two = inter.third_line_loopy()
    while two!= 5:
        toprint += inter.which_function(second_result, one, two) + '\n'
        one, two = inter.third_line_loopy()
    
    
    rev_phrase, type = inter.reverse_end()
    rev_disp, rev_geo_open = inter.reverse_brains(type, rev_phrase, lat, long)
    print(inter.lat_long_target(lat,long) + '\n' +rev_disp)
    print(toprint)
    inter.attribution_messages(for_geo_open, rev_geo_open, nws_use)


    
