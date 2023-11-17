import interactions as inter
import weather_lib as wlib
import nominatim_lib as nomlib

if __name__ == '__main__':
    toprint = ''
    for_geo_open = False
    rev_geo_open = False
    nws_use = False
    first_phrase, type = inter.first_line_input()
    first_result, latlong, disp, for_geo_open = inter.first_line_brains(first_phrase, type)

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
    
    print(latlong + '\n' + disp)
    print(toprint)
    print(str(for_geo_open) + '\n' + str(rev_geo_open) + '\n' + str(nws_use))


    
