import colorama
import datetime


def convert_date_format(date_string):
    '''
    Convert date format from dd/mm/yyyy to yyyy-mm-dd.
    
    Parameters:
    date_string : str
        Date string in the format dd/mm/yyyy.
        
    Returns:
    str
        Converted date string in the format yyyy-mm-dd.
    '''

    date_components = date_string.split("/")
    converted_date = f"{date_components[2]}-{date_components[1]}-{date_components[0]}"
    return converted_date


def convert_to_investment_period(time, is_yearly=True):
    '''
    Convert time from dd/mm/yyyy to a fixed investment period.

    Parameters:
    time : int
        Year or quarter value.
    is_yearly : bool, optional
        Specifies whether the input time is in years (True) or quarters (False). Default is True.

    Returns:
    tuple
        A tuple containing the start and end dates of the investment period.
    '''
    
    if is_yearly:
        start_date = datetime.datetime(time, 4, 1)
        end_date = datetime.datetime(time+1, 3, 1)
    else:
        start_date = datetime.datetime(
            2000+(time)//4,
            (time % 4)*3+2, 6
        )
        end_date = datetime.datetime(
            2000+(time)//4 + ((time % 4)*3+5)//12,
            ((time % 4)*3+5) % 12, 1
        )
    return start_date, end_date


def coverTime(str_time):
    '''
    Chuyển đổi thời gian từ dd/mm/yyyy sang yyyy-mm-dd
    '''
    time = str_time.split("/")
    return datetime.datetime(int(time[2]), int(time[1]), int(time[0]))


def progress_bar(cur, total, color=colorama.Fore.GREEN, text=""):
    '''
    Hiển thị thanh tiến trình'''
    percent = 100*(cur/float(total))*1/2
    bar = '█' * int(percent) + "-"*(50-int(percent))
    print(colorama.Fore.BLUE + f"\r |{bar}| {percent*2:.2f}% {text}", end="\r")
    if cur == total:
        print(colorama.Fore.RESET + f"|{text} Done!!!!| {percent*2:.2f}%")
