import re
import pandas as pd
import numpy as np
from datetime import datetime
f = open('group_chat.txt', 'r', encoding= 'utf=8')
data = f.read()
def preprocess(data):
    pattern='\d{1,2}/\d{1,2}/\d{2}, \d{1,2}:\d{2}:\d{2} [APap][Mm]:\s'
    # pattern = r'\[(\d{2}/\d{2}/\d{2}, \d{2}:\d{2}:\d{2} [APap][Mm])\] (.?):\s(.?)$'
    message =  re.split(pattern,data)[1:]
    dates = re.findall(pattern,data)
    df = pd.DataFrame({'user_message': message, 'message_date': dates})
    df['date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %I:%M:%S %p: ')
    df.drop(columns=['message_date'], inplace=True)
    users = []
    message = []
    for message_text in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message_text)
        if entry[1:]:
            users.append(entry[1])
            message.append(entry[2])
        else:
            users.append('group_notification')
            message.append(entry[0])
    df['user']=users
    df['message']= message
    df.drop(columns=['user_message'],inplace=True)
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['only_date'] = df['date'].dt.date
    df['day_name']=df['date'].dt.day
    df['hour']=df['date'].dt.hour
    df['minute']=df['date'].dt.minute
    period=[]
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))
    df['period'] = period
    return df