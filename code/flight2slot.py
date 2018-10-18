# -*- coding: UTF8 -*-

import re
import calendar
import datetime
import numpy as np
from num2words import num2words

'''
format

{
    “legs”:[{“origin_city”:”Hong Kong”, “dest_city”:”Taipei”, “origin_date”: “20181212”},
            {“origin_city”:”Taipei”, “dest_city”:”Seoul”, “origin_date”: “20181214”},
            {“origin_city”:”Seoul”, “dest_city”:”Hong Kong”, “origin_date”: “20181215”}],
    ”date“:[“20181212”, “20181214”, “20181215”]
    “city”: [“Hong Kong”, “Taipei”, “Seoul”],
    “class”:”Economy”,
    “flight”: “CX420”
    }
'''

'''
slot

{”city_name”, “flight_class”, “flgith_no”, “departure_date”}
'''

today = datetime.date.today()

yesterday = today - datetime.timedelta(days=1)
tomorrow = today + datetime.timedelta(days=1)

month_abb = [i for i in calendar.month_abbr][1:] # 'Jan\\.|Jan'
month_full = [i for i in calendar.month_name][1:] # January
month_all = [x + '|' + y for x, y in zip(month_full, month_abb)] # january|jan\\.|jan
month_name_pattern = '('+'|'.join(month_all)+')'
month_number_pattern = '(0[123356789]|1[012])'
day_number_pattern = '(0[123456789]|1[1234567890]|2[0123456789]|3[01])'
year_number_pattern = '([0-9]{4})'

flight_pattern = '[A-Z]{2}[0-9]{3}'

city_dic = {
    "HKG":"Hong Kong",
    "HK":"Hong Kong",
    "TPE":"Taipei",
    "ICN":"Seoul",
    "SEL":"Seoul",
    "SHA":"Shanghai",
    "PVG":"Shanghai",
    "CAN":"Guangzhou",
    "PEK":"Beijing",
    "BJS":"Beijing",
    "KIX":"Osaka",
    "OSA":"Osaka",
    "TYO":"Tokyo",
    "NRT":"Tokyo",
    "HND":"Tokyo"
}

class_dic = {
    "Premium Econ":"Premium Economy",
    "Econ":"Economy",
    "Y Class":"Economy",
    " PE":"Preimium Economy",
    "PEY":"Preimium Economy",
    "W Class":"Preimium Economy",
    "Biz":"Business",
    "Bus":"Business",
    "J Class":"Business",
    "F Class":"First Class"
}

# 12 Dec, 12-Dec, 12-December, 10/12/2018, 2018/12/10, the next day, tomorrow, a day earlier
date_pattern1 = day_number_pattern + ' ' + month_name_pattern
date_pattern2 = day_number_pattern + '-' + month_name_pattern
date_pattern3 = day_number_pattern + '/' + month_number_pattern + '/' + year_number_pattern
date_pattern4 = year_number_pattern + '/' + month_number_pattern + '/' + day_number_pattern
date_pattern5 = '(T|t)omorrow|(y|Y)esterday|(a|A) day earlier|(T|t)he next day'

date_patterns = [date_pattern1, date_pattern2, date_pattern3, date_pattern4, date_pattern5]

# datetime.datetime.today().strftime('%Y%m%d')

# the 1st/ first one, option 1,the 1st/first option
maximum_show_flights = 10

ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4])

choice_pattern = ''

for n in range(1, maximum_show_flights + 1):
    ordinal_number = ordinal(n)
    ordinal_word = num2words(n, ordinal=True)
    choice_pattern += '(t|T)he (' + ordinal_number + '|' + ordinal_word + ') ((O|o)ption|one)|'
    choice_pattern += '(O|o)ption ' + str(n)
    if n != maximum_show_flights:
        choice_pattern += '|'



def slot_filling(inputs):
    """
    Get slot_filling with input sentence.
    
    Parameters:
        inputs - sentence of user apply

    Returns:
        slots - dictionary of slots
        sentence - sentence replaced by slots
    """
    slots = {}
    sentence = inputs

    dates = date_parse(sentence)
    cities = city_parse(sentence)
    classes = class_parse(sentence)
    flights = flight_parse(sentence)
    choice = choice_parse(sentence)

    slots['city'] = []
    for city in cities:
        sentence = sentence.replace(city, 'city_name')
        if city in city_dic:
            city = city_dic[city]
        if city not in slots['city']:
            slots['city'].append(city)

    slots['class'] = ''
    if classes != '':
        sentence = sentence.replace(classes, 'flight_class')
        if classes in class_dic:
            classes = class_dic[classes]
        slots['class'] = classes
        
    slots['flight'] = ''
    if flights != '':
        slots['flight'] = flights
        sentence = sentence.replace(flights, 'flight_no')
    elif choice:
        sentence = sentence.replace(choice, 'flight_no')
        slots['flight'] = choice
    else:
        pass

    slots['date'] = []
    slots['legs'] = []
    for date in dates:
        sentence = sentence.replace(date, 'departure_date')
        if re.match(date_pattern1, date) or re.match(date_pattern2, date):
            day_num = date[:2]
            month_name = date[3:]
            if len(month_name) > 3:
                month_num = str(list(calendar.month_name).index(month_name))
            else:
                month_num = str(list(calendar.month_abbr).index(month_name))
            year_num = str(datetime.datetime.now().year)
            date = year_num + month_num + day_num
            if date not in slots['date']:
                slots['date'].append(date)
        
        elif re.match(date_pattern3, date):
            items = date.split('/')[::-1]
            date = ''.join(items)
            if date not in slots['date']:
                slots['date'].append(date)
        
        elif re.match(date_pattern4, date):
            items = date.split('/')
            date = ''.join(items)
            if date not in slots['date']:
                slots['date'].append(date)
        
        elif re.match(date_pattern5, date):
            if date == 'yesterday' or date == 'Yesterday':
                date = yesterday.strftime('%Y%m%d')
            elif date == 'tomorrow' or date == 'Tomorrow':
                date = tomorrow.strftime('%Y%m%d')
            
            if date not in slots['date']:
                slots['date'].append(date)
        else:
            pass
    
    if len(slots['date']) < 3 or len(slots['city']) < 3:
        pass
    else:
        slots['legs'].append({'origin_city':slots['city'][0], 'dest_city':slots['city'][1], 'origin_date': slots['date'][0]})
        slots['legs'].append({'origin_city':slots['city'][1], 'dest_city':slots['city'][2], 'origin_date': slots['date'][1]})
        slots['legs'].append({'origin_city':slots['city'][2], 'dest_city':slots['city'][0], 'origin_date': slots['date'][2]})
        slots['city'] = []
        slots['date'] = [] 
    
    return slots, sentence

def flight_parse(inputs):
    """
    Get flghts exist in input sentence.
    
    Parameters:
        inputs - sentence of user apply

    Returns:
        res - flghts exist in input sentence
    """
    res = ''

    if re.search(flight_pattern, inputs):
        res = re.search(flight_pattern, inputs).group()

    return res


def date_parse(inputs):
    """
    Get dates exist in input sentence.
    
    Parameters:
        inputs - sentence of user apply

    Returns:
        res - dates exist in input sentence
    """

    res = []
    for pattern in date_patterns:
        for m in re.finditer(pattern, inputs):
            res.append(m.group())

    return res
    

def city_parse(inputs):
    """
    Get cities exist in input sentence.
    
    Parameters:
        inputs - sentence of user apply

    Returns:
        res - cities exist in input sentence
    """
    cities = ["HongKong"]
    for k, v in city_dic.items():
        cities.append(k)
        cities.append(v)
    cities = list(set(cities))
    city_pattern = '(' + '|'.join(cities) + ')'

    res = []
    for m in re.finditer(city_pattern, inputs):
        res.append(m.group())

    return res
    
def choice_parse(inputs):
    """
    Get choice_pattern exist in input sentence.
    
    Parameters:
        inputs - sentence of user apply

    Returns:
        res - choice_pattern exist in input sentence
    """
    res = ''
    
    if re.search(choice_pattern, inputs):
        res = re.search(choice_pattern, inputs).group()
    
    return res


def class_parse(inputs):
    """
    Get classes of flight exists in input sentence.
    
    Parameters:
        inputs - sentence of user apply

    Returns:
        res - classes of flight exists in input sentence
    """
    classes = []
    for k, v in class_dic.items():
        classes.append(k)
        classes.append(v)
    classes = list(set(classes))
    classes.sort(key = lambda s : - len(s))

    res = ""
    for cl in classes:
        if re.search(cl, inputs):
            res = re.search(cl, inputs).group()
            break

    return res