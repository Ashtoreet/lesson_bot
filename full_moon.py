import ephem
import datetime
import re


def moon_full(day):
    try:        
        result = re.search(r'\d{4}\-\d{2}\-\d{2}|\d{4}\/\d{2}\/\d{2}|\d{4}\.\d{2}\.\d{2}', day)
        date = ephem.next_full_moon(result.group(0)).datetime().strftime('%d %b %Y %H:%M:%S')
                
        return date
    except AttributeError as e:
        return 'Вы забыли написать дату'
    except ValueError as e:
        return e


if __name__ == '__main__':
    day = 'Когда ближайшее полнолуние после 2016-10-01?'
    # day = ' полнолуние?'
    # day = 'Когда ближайшее полнолуние после 2016-10-01'
    print(moon_full(day))
