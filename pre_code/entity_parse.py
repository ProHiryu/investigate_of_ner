# -*- coding: UTF8 -*-

import re
import calendar
import datetime
import numpy as np

month_abb = [i+'\.'+'|'+i for i in calendar.month_abbr][1:]
month_full = [i for i in calendar.month_name][1:]
month_all = [x.lower()+'|'+y.lower() for x, y in zip(month_full, month_abb)]
month_name_pattern = '('+'|'.join(month_all)+')'
month_name_pattern = month_name_pattern

half_month_pattern_1 = '(the )?(first|1st|second|2nd) (half|period) of (this|the) month'
half_month_pattern_2 = '(the )?(first|1st|second|2nd) (half|period) of ' + month_name_pattern + '(,? 201[0-9])?'

last_period_pattern = '(last|this|previous) (time )?(report|period)'
week_period_pattern = "(the )?period of (this|last|previous) week"

from_to_pattern_1_1 = "([0-3]?[0-9]-[0-3]?[0-9] )" + month_name_pattern + '(,? 201[0-9])?'
from_to_pattern_1_2 = month_name_pattern + "( [0-3]?[0-9]-[0-3]?[0-9])" + '(,? 201[0-9])?'

from_to_pattern_2_1 = "(from|between|from |between )?" + '([0-3]?[0-9](st|th|rd|nd)? )' + '(to|through|till|and|until)' + '( [0-3]?[0-9](st|th|rd|nd)? )' + month_name_pattern + '(,? 201[0-9])?'
from_to_pattern_2_2 = "(from|between|from |between )?" + month_name_pattern + '( [0-3]?[0-9](st|th|rd|nd)? )' + '(to|through|till|and|until)' + '( [0-3]?[0-9](st|th|rd|nd)?)' + '(,? 201[0-9])?'

from_to_pattern_3_1 = "(from|between|from |between )?" + '([0-3]?[0-9](st|th|rd|nd)? )' + month_name_pattern + " " + '(to|through|till|and|until)' + '( [0-3]?[0-9](st|th|rd|nd)? )' + month_name_pattern + '(,? 201[0-9])?'
from_to_pattern_3_2 = "(from|between|from |between )?" + month_name_pattern + '( [0-3]?[0-9](st|th|rd|nd)? )' + '(to|through|till|and|until)' + " " + month_name_pattern + '( [0-3]?[0-9](st|th|rd|nd)?)' + '(,? 201[0-9])?'

from_to_pattern_4_1 = "[0-1]?[0-9]\.[0-3]?[0-9]-[0-3]?[0-9]"
from_to_pattern_4_2 = "^[0-1]?[0-9]\.[0-3]?[0-9]-[0-3]?[0-9]$"

single_date_pattern_1 = '([0-3]?[0-9](st|th|rd|nd)? )' + month_name_pattern + '(,? 201[0-9])?'
single_date_pattern_2 = month_name_pattern + '( [0-3]?[0-9](st|th|rd|nd)?)' + '(,? 201[0-9])?'


date_pattern_1 = "(201[0-9])[-/.]?([0-1])?[0-9][-/.]?([0-3])?[0-9]"
date_pattern_2 = "([0-1])?[0-9][-/.]?([0-3])?[0-9][-/.]?(201[0-9])"
date_pattern_3 = "^(201[0-9])[-/.]?([0-1])?[0-9][-/.]?([0-3])?[0-9]$"
date_pattern_4 = "^([0-1])?[0-9][-/.]?([0-3])?[0-9][-/.]?(201[0-9])$"
date_pattern_5 = "^([0-1])?[0-9][-/.]([0-3])?[0-9]$"
date_pattern_6 = "([0-1])?[0-9][-/.]?([0-3])?[0-9]"

digit_pattern_from_to_1 = "(from|between|from |between )?" + date_pattern_1 + "( ?- ?| ?to ?| ?~ ?| ?till ?| ?and ?| | ?,|,? | ?until ?)" + date_pattern_1
digit_pattern_from_to_2 = "(from|between|from |between )?" + date_pattern_2 + "( ?- ?| ?to ?| ?~ ?| ?till ?| ?and ?| | ?,|,? | ?until ?)" + date_pattern_2
digit_pattern_from_to_3 = "(from|between|from |between )?" + date_pattern_6 + "( ?- ?| ?to ?| ?~ ?| ?till ?| ?and ?| | ?,|,? | ?until ?)" + date_pattern_6


def num_to_str(m):
    if m < 10:
        m = '0' + str(m)
    else:
        m = str(m)
    return m


def half_month_parse(string):
    this_year = datetime.date.today().year
    this_month = datetime.date.today().month
    # this_day = datetime.date.today().day
    month_end_date = calendar.monthrange(this_year, this_month)[1]

    match_obj = re.search(half_month_pattern_1, string)
    if match_obj:
        match_text = match_obj.group()
        if "first" in match_text or "1st" in match_text:
            return match_text, str(this_year) + num_to_str(this_month) + '01', str(this_year) + num_to_str(
                this_month) + '15'
        elif "second" in match_text or "2nd" in match_text:
            return match_text, str(this_year) + num_to_str(this_month) + '16', str(this_year) + num_to_str(
                this_month) + str(month_end_date)

    match_obj = re.search(half_month_pattern_2, string)
    if match_obj:
        from_year = None
        this_month = None

        match_text = match_obj.group()
        match_tmp = match_text.split()
        for m in match_tmp:
            m = m.replace(",", '')
            if re.search(month_name_pattern, m):
                word = re.search(month_name_pattern, m).group()
                for i, mon in enumerate(month_all):
                    if word in mon.replace("\\", ""):
                        this_month = i + 1
                        break
            if re.search("201[0-9]", m):
                from_year = re.search("201[0-9]", m).group()

        if not this_month:
            return None

        month_end_date = calendar.monthrange(int((from_year or this_year)), this_month)[1]

        if "first" in match_text or "1st" in match_text:
            return match_text, str(from_year or this_year) + num_to_str(this_month) + '01', str(
                from_year or this_year) + num_to_str(this_month) + '15'
        elif "second" in match_text or "2nd" in match_text:
            return match_text, str(from_year or this_year) + num_to_str(this_month) + '16', str(
                from_year or this_year) + num_to_str(this_month) + str(month_end_date)

    return None


def period_parse(string):
    this_year = datetime.date.today().year
    this_month = datetime.date.today().month
    this_day = datetime.date.today().day
    month_end_date = calendar.monthrange(this_year, this_month)[1]

    match_obj = re.search(last_period_pattern, string)
    if match_obj:
        match_text = match_obj.group()
        if 'last' in match_text:
            if this_day <= 15:
                # 跨年
                if this_month == 1:
                    this_year = this_year - 1
                    this_month = 12
                    month_end_date = calendar.monthrange(this_year, this_month)[1]
                    return match_text, str(this_year) + num_to_str(this_month) + '16', str(this_year) + num_to_str(
                        this_month) + str(month_end_date)
                else:
                    this_month = this_month - 1
                    month_end_date = calendar.monthrange(this_year, this_month)[1]
                    return match_text, str(this_year) + num_to_str(this_month) + '16', str(this_year) + num_to_str(
                        this_month) + str(month_end_date)
            else:
                return match_text, str(this_year) + num_to_str(this_month) + '01', str(this_year) + num_to_str(
                    this_month) + '15'

        elif 'this' in match_text:
            if this_day <= 15:
                return match_text, str(this_year) + num_to_str(this_month) + '01', str(this_year) + num_to_str(
                    this_month) + '15'
            else:
                return match_text, str(this_year) + num_to_str(this_month) + '16', str(this_year) + num_to_str(
                    this_month) + str(month_end_date)

    match_obj = re.search(week_period_pattern, string)
    if match_obj:
        match_text = match_obj.group()
        if 'last' in match_text:
            last_week_date = datetime.datetime.now() - datetime.timedelta(days=7)
            this_year = last_week_date.year
            this_month = last_week_date.month
            this_day = last_week_date.day
            month_end_date = calendar.monthrange(this_year, this_month)[1]
            if this_day <= 15:
                return match_text, str(this_year) + num_to_str(this_month) + '01', str(this_year) + num_to_str(
                    this_month) + '15'
            else:
                return match_text, str(this_year) + num_to_str(this_month) + '16', str(this_year) + num_to_str(
                    this_month) + str(month_end_date)
        elif 'this' in match_text:
            if this_day <= 15:
                return match_text, str(this_year) + num_to_str(this_month) + '01', str(this_year) + num_to_str(
                    this_month) + '15'
            else:
                return match_text, str(this_year) + num_to_str(this_month) + '16', str(this_year) + num_to_str(
                    this_month) + str(month_end_date)

    return None


def from_to_parse(string):
    this_year = datetime.date.today().year
    # this_month = datetime.date.today().month
    # this_day = datetime.date.today().day
    # month_end_date = calendar.monthrange(this_year, this_month)[1]

    match_obj = (re.search(from_to_pattern_1_1, string) or re.search(from_to_pattern_1_2, string) or
                 re.search(from_to_pattern_2_1, string) or re.search(from_to_pattern_2_2, string) or
                 re.search(from_to_pattern_3_1, string) or re.search(from_to_pattern_3_2, string))

    from_year = None
    to_year = None
    from_month = None
    to_month = None
    from_day = None
    to_day = None
    month_tmp = 0

    if match_obj:
        match_text = match_obj.group()
        match_tmp = match_text.split()
        for m in match_tmp:
            m = m.replace(",", "")
            # from 后无空格 to后无空格 from可替换
            if re.search("(from|to|through)", m):
                continue
            if re.search("([0-3]?[0-9]-[0-3]?[0-9])", m):
                word = re.search("([0-3]?[0-9]-[0-3]?[0-9])", m).group().split('-')
                from_day = int(word[0])
                to_day = int(word[1])
            if re.search("(^[0-3]?[0-9]$)", m):
                if not from_day:
                    from_day = int(re.search("(^[0-3]?[0-9]$)", m).group())
                else:
                    to_day = int(re.search("(^[0-3]?[0-9]$)", m).group())

            if re.search("(^[0-3]?[0-9](st|th|rd|nd)$)", m):
                if not from_day:
                    from_day = int(re.search("(^[0-3]?[0-9](st|th|rd|nd)$)", m).group()[0:-2])
                else:
                    to_day = int(re.search("(^[0-3]?[0-9](st|th|rd|nd)$)", m).group()[0:-2])
            if re.search(month_name_pattern, m):
                word = re.search(month_name_pattern, m).group()
                for i, mon in enumerate(month_all):
                    if word in mon.replace("\\", ""):
                        month_tmp = i + 1
                        break
                if not from_month:
                    from_month = month_tmp
                else:
                    to_month = month_tmp
            if re.search("201[0-9]", m):
                if not from_year:
                    from_year = re.search("201[0-9]", m).group()
                else:
                    to_year = re.search("201[0-9]", m).group()

        if not (from_day and to_day and from_month):
            return None
        else:
            return match_text, str(from_year or this_year) + num_to_str(from_month) + num_to_str(from_day), \
                   str(to_year or from_year or this_year) + num_to_str(to_month or from_month) + num_to_str(to_day)

    else:
        return None


# for 3.1-15
def from_to_parse_2(string):
    this_year = datetime.date.today().year
    match_obj = re.search(from_to_pattern_4_1, string)

    if match_obj:
        # match_text = match_obj.group()
        # match_tmp = match_text.split()
        match_tmp = string.replace(",", " ").split()
        for m in match_tmp:
            m = m.replace(",", "")
            if re.search(from_to_pattern_4_2, m):
                tmp = m.replace(".", " ").replace("-", " ").split()
                from_month = to_month = num_to_str(int(tmp[0]))
                from_day = num_to_str(int(tmp[1]))
                to_day = num_to_str(int(tmp[2]))
                return m, str(this_year) + from_month + from_day, str(this_year) + to_month + to_day

    return None


def single_date_parse(string):
    this_year = datetime.date.today().year
    this_month = None
    this_day = None

    match_obj = (re.search(single_date_pattern_1, string) or re.search(single_date_pattern_2, string))
    if match_obj:
        match_text = match_obj.group()
        match_tmp = match_text.split()
        for m in match_tmp:
            m = m.replace(",", "")
            if re.search("(^[0-3]?[0-9]$)", m):
                this_day = int(re.search("(^[0-3]?[0-9]$)", m).group())

            if re.search("(^[0-3]?[0-9](st|th|rd|nd)$)", m):
                this_day = int(re.search("(^[0-3]?[0-9](st|th|rd|nd)$)", m).group()[0:-2])

            if re.search(month_name_pattern, m):
                word = re.search(month_name_pattern, m).group()
                for i, mon in enumerate(month_all):
                    if word in mon.replace("\\", ""):
                        this_month = i + 1
                        break

            if re.search("201[0-9]", m):
                this_year = int(re.search("201[0-9]", m).group())

        if not (this_month and this_day):
            return None

        return match_text, str(this_year) + num_to_str(this_month) + num_to_str(this_day), \
               str(this_year) + num_to_str(this_month) + num_to_str(this_day)

        # month_end_date = calendar.monthrange(this_year, this_month)[1]
        #
        # if this_day <= 15:
        #     return match_text, str(this_year) + num_to_str(this_month) + '01', str(this_year) + num_to_str(
        #         this_month) + '15'
        # else:
        #     return match_text, str(this_year) + num_to_str(this_month) + '16', str(this_year) + num_to_str(
        #         this_month) + str(month_end_date)

    return None


def check_num_letter(word):
    alphabet = list("abcdefghijklmnopqrstuvwxyz")
    numbers = list("0123456789")
    letters = list(word)
    if len(letters) < 5 or len(letters) > 10:
        return False
    if (len(np.intersect1d(letters, alphabet)) > 0) and (len(np.intersect1d(letters, numbers)) > 0) \
            and (letters[-1] in numbers) and letters[0] not in ['t', 'f', 'c']:  # 避免charge/from/to20180218被识别成wbs_code
        return True

    return False


def code_parse(string):
    string = re.sub("[,.?!:']", " ", string)
    words = string.split()
    for w in words:
        if check_num_letter(w):
            return w
    return None


def hours_parse(string):
    if re.search("[1-9]( ?hours?| ?hrs?|hs?|rs)(/day|/d)?", string):
        match_text = re.search("[1-9]( ?hours?| ?hrs?|hs?|rs)(/day|/d)?", string).group()
        for i in match_text:
            if i in '0123456789':
                return match_text, i

    string = re.sub("[-,.?!:\'\"]", " ", string)
    words = string.split()
    for i in range(len(words)):
        if re.search("^[1-9]$", words[i]):
            return words[i], words[i]

    return None


# 2018228 7位数字或者2018/2/3替换为仅剩6位数字
def seven_digits_date_parse(string):
    string = re.sub("[-/.]", "", string)
    year = re.search("201[0-9]", string).group()
    string = re.sub(year, "", string)
    if len(string) == 4:
        return year + string
    elif len(string) == 3:
        return year + "0" + string
    else:
        return year + "0" + string[0] + "0" + string[1]


# 有人变态地写20180000
def parse_period_from_date(string):
    try:
        dt = datetime.datetime.strptime(string,  "%Y%m%d")
    except:
        return "NULL", "NULL"
    year = dt.year
    month = dt.month
    day = dt.day
    return str(year) + num_to_str(month) + num_to_str(day), str(year) + num_to_str(month) + num_to_str(day)

    # month_end_date = calendar.monthrange(year, month)[1]
    # if day <= 15:
    #     return str(year) + num_to_str(month) + "01", str(year) + num_to_str(month) + "15"
    # else:
    #     return str(year) + num_to_str(month) + "16", str(year) + num_to_str(month) + str(month_end_date)


def digit_date_parse(string):
    dates = []

    if re.search(digit_pattern_from_to_1, string):
        match_text = re.search(digit_pattern_from_to_1, string).group()
        for m in re.finditer(date_pattern_1, match_text):
            dates.append(m.group())

        if len(dates) < 2:
            return None

        return match_text, seven_digits_date_parse(dates[0]), seven_digits_date_parse(dates[1])

    if re.search(digit_pattern_from_to_2, string):
        match_text = re.search(digit_pattern_from_to_2, string).group()
        for m in re.finditer(date_pattern_2, match_text):
            dates.append(m.group())

        if len(dates) < 2:
            return None

        return match_text, seven_digits_date_parse(dates[0]), seven_digits_date_parse(dates[1])

    if re.search(digit_pattern_from_to_3, string):
        match_text = re.search(digit_pattern_from_to_3, string).group()
        for m in re.finditer(date_pattern_6, match_text):
            dates.append(m.group())

        if len(dates) < 2:
            return None

        this_year = str(datetime.date.today().year)
        return match_text, seven_digits_date_parse(this_year+dates[0]), seven_digits_date_parse(this_year+dates[1])

    # . / - 暂时保留
    string = re.sub("[,?!:\'\"]", " ", string)
    words = string.split()
    for w in words:
        if re.search(date_pattern_3, w):
            match_text = re.search(date_pattern_3, w).group()
            the_date = seven_digits_date_parse(match_text)
            from_time, to_time = parse_period_from_date(the_date)
            return match_text, from_time, to_time

        if re.search(date_pattern_4, w):
            match_text = re.search(date_pattern_4, w).group()
            the_date = seven_digits_date_parse(match_text)
            from_time, to_time = parse_period_from_date(the_date)
            return match_text, from_time, to_time

        if re.search(date_pattern_5, w):
            match_text = re.search(date_pattern_5, w).group()
            this_year = str(datetime.date.today().year)
            the_date = seven_digits_date_parse(this_year+str(match_text))
            from_time, to_time = parse_period_from_date(the_date)
            return match_text, from_time, to_time

    return None







