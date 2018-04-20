"""
    Choose right icons for each day and
    background picture for current weather.
"""
from collections import Counter
from typing import List


def choose_the_icon(lst: List) -> str:
    """
    Choose relevant weather icon

    :param lst:
    :return: str
    """
    result = ''
    if len(lst) == 1:
        return lst[0] + '.svg'

    if 'Thunderstorm' in lst:
        if 'Drizzle' in lst:
            result = 'thunder-drizzle.svg'
        elif 'Rain' in lst:
            result = 'thunder-rain.svg'
        elif 'Snow' in lst:
            result = 'thunder-snow.svg'
        elif 'Atmosphere' in lst:
            result = 'thunder-fog.svg'
        elif 'Clear' in lst:
            result = 'thunder-clear.svg'
        elif 'Clouds' in lst:
            result = 'thunder-clouds.svg'
        elif 'Extreme' in lst:
            result = 'thunder-extreme.svg'
        else:
            result = 'Additional.svg'

    elif 'Drizzle' in lst:
        if 'Rain' in lst:
            result = 'drizzle-rain.svg'
        elif 'Snow' in lst:
            result = 'drizzle-snow.svg'
        elif 'Atmosphere' in lst:
            result = 'drizzle-fog.svg'
        elif 'Clear' in lst:
            result = 'drizzle-clear.svg'
        elif 'Clouds' in lst:
            result = 'drizzle-clouds.svg'
        elif 'Extreme' in lst:
            result = 'drizzle-extreme.svg'
        else:
            result = 'Additional.svg'

    elif 'Rain' in lst:
        if 'Snow' in lst:
            result = 'rain-snow.svg'
        elif 'Atmosphere' in lst:
            result = 'rain-fog.svg'
        elif 'Clear' in lst:
            result = 'rain-clear.svg'
        elif 'Clouds' in lst:
            result = 'rain-clouds.svg'
        elif 'Extreme' in lst:
            result = 'rain-extreme.svg'
        else:
            result = 'Additional.svg'

    elif 'Snow' in lst:
        if 'Atmosphere' in lst:
            result = 'snow-fog.svg'
        elif 'Clear' in lst:
            result = 'snow-clear.svg'
        elif 'Clouds' in lst:
            result = 'snow-clouds.svg'
        elif 'Extreme' in lst:
            result = 'snow-extreme.svg'
        else:
            result = 'Additional.svg'

    elif 'Atmosphere' in lst:
        if 'Clear' in lst:
            result = 'atmosphere-clear.svg'
        elif 'Clouds' in lst:
            result = 'atmosphere-clouds.svg'
        elif 'Extreme' in lst:
            result = 'atmosphere-extreme.svg'
        else:
            result = 'Additional.svg'

    elif 'Clear' in lst:
        if 'Clouds' in lst:
            result = 'clear-clouds.svg'
        elif 'Extreme' in lst:
            result = 'clear-extreme.svg'
        else:
            result = 'Additional.svg'

    elif 'Clouds' in lst:
        if 'Extreme' in lst:
            result = 'clouds-extreme.svg'
        else:
            result = 'Additional.svg'

    else:
        result = 'Additional.svg'
    return result


def choose_background(condition: int) -> str:
    """
    Check the number to determine which background to return

    :param condition:
    :return: str
    """
    result = ''
    num = int(condition / 100)
    if condition == 800 or condition == 801:
        result = 'Clear'
    elif num == 2:
        result = 'Thunderstorm'
    elif num == 3:
        result = 'Drizzle'
    elif num == 5:
        result = 'Rain'
    elif num == 6:
        result = 'Snow'
    elif num == 7:
        result = 'Atmosphere'
    elif num == 8:
        result = 'Clouds'
    elif condition < 907:
        result = 'Extreme'
    else:
        result = 'Additional'
    return result


def choose_icon(df: 'dataFrame') -> 'dataFrame':
    """
    Check the number of occurrence of weather type in df.
    If occurs more than 2 times, keep it.

    :param df:
    :return:
    """
    i = 0
    while i < len(df):
        value = df['weather'][i]
        count = Counter(value)
        k = []
        for x in count:
            if count[x] > 1:
                k.append(x)
        icon = choose_the_icon(k)
        df.at[i, 'weather'] = icon
        i += 1
    return df
