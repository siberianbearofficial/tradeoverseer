from datetime import datetime
from calendar import isleap
# from subprocess import STDOUT, check_output
# from json import loads
from .screenshot_analyzer import analyze_screenshot

days_in_months = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def get_days_in_month(year: int, month: int) -> int:
    days_in_month = days_in_months[month - 1]
    return 29 if (isleap(year) and month == 2) else days_in_month


def get_period_boundaries(year: int | None, month: int | None, day: int | None, hour: int | None):
    if not year:
        raise ValueError(f'Invalid year. Integer expected but got {year} instead.')
    if not month:
        raise ValueError(f'Invalid month. Integer expected but got {month} instead.')

    if day and hour:
        return (datetime(year=year, month=month, day=day, hour=hour),
                datetime(year=year, month=month, day=day, hour=hour, minute=59, second=59, microsecond=999999))
    if day:
        return (datetime(year=year, month=month, day=day),
                datetime(year=year, month=month, day=day, hour=23, minute=59, second=59, microsecond=999999))
    return (datetime(year=year, month=month, day=1),
            datetime(year=year, month=month, day=get_days_in_month(year, month),
                     hour=23, minute=59, second=59, microsecond=999999))


def validate_year(year: int):
    if year < 1:
        raise ValueError(f'Invalid year. Expected integer in [1, +inf) but got {year} instead.')


def validate_month(month: int):
    if month < 1 or month > 12:
        raise ValueError(f'Invalid month. Expected integer in [1, 12] but got {month} instead.')


def validate_day(year: int, month: int, day: int):
    days_in_month = get_days_in_month(year, month)
    if day > days_in_month or day < 1:
        raise ValueError(f'Invalid day. Expected integer in [1, {days_in_month}] but got {day} instead.')


def validate_hour(hour: int):
    if hour < 0 or hour > 23:
        raise ValueError(f'Invalid hour. Expected integer in [0, 23] but got {hour} instead.')


def validate_price(price: str):
    price = price.strip().replace(',', '.')
    if len(price) > 10:
        raise ValueError('Invalid price. Should contain not more than 10 symbols.')
    if not price.replace('.', '').isdigit():
        raise ValueError('Invalid price. Should be a positive float (without "e").')
    float(price)
    return price


def parse_screenshot(screenshot: bytes):
    # script_path = '/cv/screenshot_analyzer.py'
    screenshot_path = './screenshot.png'

    try:
        with open(screenshot_path, 'wb') as f:
            f.write(screenshot)
        # result = check_output(['python3', script_path, screenshot_path], cwd='/cv', text=True)
        # print('Result:', result)
        # result = loads(result)
        
        result = analyze_screenshot(screenshot_path)
        # result = []
        
        return 0, result
    except PermissionError:
        return 3, None
    except Exception as ex:
        print(ex)
        return 2, None
