import env
import time, sys
from main import Headless, HeadlessChrome

# checking if it close to the time for registration to open at 8AM ET or 1PM GMT
def checkTime():
    check = False

    current = time.gmtime()
    if current.tm_hour == 8+5 and current.tm_min >= 0:
        if current.tm_sec < 20:
            time.sleep(20-current.tm_sec)

        check = True

    return check

if __name__ == '__main__':
    print(time.gmtime())
    env.park = 'Nathan Phillips Square'
    if time.strftime("%A") == 'Saturday' or time.strftime("%A") == 'Sunday':
        env.time="4:00PM"
    else:
        env.time="6:00PM"

    chrome = any('--chrome' == arg for arg in sys.argv)

    if chrome:
        reserve = HeadlessChrome(env)
    else:
        reserve = Headless(env)

    reserve.setup()
    reserve.login()
    reserve.skatePage()
    reserve.selectPark()

    #logic for maintain an active session (checks every 15 seconds)
    lastPage = False
    while True:
        if lastPage is not True:
            reserve.lastPage()
        else:
            reserve.prevPage()

        lastPage = not lastPage

        if checkTime() is True:
            break
        else:
            time.sleep(15)

    #conduct one last page refresh by going to the prev page and then last page, then run select time algorithm
    print('Algorithm triggered')
    startTime = time.time();
    reserve.prevPage()
    time.sleep(2)
    reserve.lastPage()
    reserve.selectTime()
    reserve.registerAll()
    reserve.complete()
    print("Algorithm completed in (s):", time.time()-startTime)
    reserve.close()
