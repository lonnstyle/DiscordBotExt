from datetime import datetime,timedelta

class time_info:
    def UTC_8():
        f = '[%Y-%m-%d %H:%M:%S]'
        time_delta = timedelta(hours=+8)
        utc_8_date_str = (datetime.utcnow()+time_delta).strftime(f) #時間戳記
        return utc_8_date_str
        
    def UTC_8_CH():
        time_delta = timedelta(hours=+8)
        str_time = (datetime.utcnow()+time_delta).strftime('%H:%M')
        hours, minutes = map(int, str_time.split(':'))
        am_or_pm = ['早上', '下午'][hours >= 12]
        return f"[{(datetime.utcnow()+time_delta).strftime('%Y-%m-%d')} {am_or_pm} {(hours-1) % 12+1}:{minutes:02}]"

    def convert(time):
        hour,minute = time.split(':')
        hour = int(hour)
        minute = int(minute)
        if hour < 12:
            return '早上 %d：%d'%(hour,minute)
        elif hour == 12:
            return '晚上 %d：%d'%(hour,minute)
        else:
            hour = hour-12
            return '晚上 %d：%d'%(hour,minute)
