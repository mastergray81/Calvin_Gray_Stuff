import datetime

def endTime(time):
    endtime = datetime.datetime.now()
    timeElapsed = endtime - time
    return print('\nTotal time elapsed:',timeElapsed,'\n')