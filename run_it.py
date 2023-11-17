import interactions as inter
import weather_lib as wlib

if __name__ == '__main__':
    first_phrase, type = inter.first_line_input()
    first_result = inter.first_line_brains(first_phrase, type)

    second_phrase, type = inter.second_line_input()
    second_result = inter.second_line_brains(first_result, type, second_phrase)

    
    print(wlib.temperature_air(second_result, 'F', 24, 'max'))
    print(wlib.temperature_feels(second_result, 'F', 24, 'max'))
    print(wlib.humidity(second_result,24,'max'))



    
