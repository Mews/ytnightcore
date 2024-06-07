from datetime import datetime

def log(section, info, include_time=True, *args, **kwargs):
    current_time = datetime.now().strftime("%H:%M:%S")
    print("( "+current_time+" ) " + "["+section+"] " + info, *args, **kwargs)