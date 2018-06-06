import ephem
import datetime

# Когда ближайшее полнолуние после 2016-10-01?

def moon_full(day):
    if 'полнолуние' in day:
        dates = day.split(' ')
        for item in dates:
            if '?' in item:
                item = item.replace('?', '')
                date = ephem.next_full_moon(item).datetime().strftime('%d %b %Y %H:%M:%S')
                
                return date


if __name__ == '__main__':
    day = 'Когда ближайшее полнолуние после 2016-10-01?'
    print(moon_full(day))
