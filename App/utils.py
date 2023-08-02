def format_datetime_sent(time_sent:str):
    #remove 0 padded hour
    if time_sent[0] == '0':
        time_sent = time_sent[1:]

    if 'AM' in time_sent:
        time_sent = time_sent.replace('AM', 'a.m.')
    else:
        time_sent = time_sent.replace('PM', 'p.m.')
    return time_sent