import numpy as np
from amlich_data import *

PI = np.pi

def getYearCode(yyyy):
    #yearCode;
    if (yyyy < 1300):
        yearCode = TK13[yyyy - 1200];
    elif (yyyy < 1400):
        yearCode = TK14[yyyy - 1300];
    elif (yyyy < 1500):
        yearCode = TK15[yyyy - 1400];
    elif (yyyy < 1600):
        yearCode = TK16[yyyy - 1500];
    elif (yyyy < 1700):
        yearCode = TK17[yyyy - 1600];
    elif (yyyy < 1800):
        yearCode = TK18[yyyy - 1700];
    elif (yyyy < 1900):
        yearCode = TK19[yyyy - 1800];
    elif (yyyy < 2000):
        yearCode = TK20[yyyy - 1900];
    elif (yyyy < 2100):
        yearCode = TK21[yyyy - 2000];
    else:
        yearCode = TK22[yyyy - 2100];
    #if debug: print(hex(yearCode))
    return yearCode

def jdFromDate(dd, mm, yy):
    '''
    Compute the (integral) Julian day number of day dd/mm/yyyy, i.e., the number 
    of days between 1/1/4713 BC (Julian calendar) and dd/mm/yyyy. 
    Formula from http://www.tondering.dk/claus/calendar.html
    '''
    #a, y, m, jd
    a = int((14 - mm) / 12)
    y = yy+4800-a
    m = mm+12*a-3
    jd = dd + int((153*m+2)/5) + 365*y + int(y/4) - int(y/100) + int(y/400) - 32045
    if (jd < 2299161):
        jd = dd + int((153*m+2)/5) + 365*y + int(y/4) - 32083
    
    return jd
    
    
def jdToDate(jd):
    '''
    Convert a Julian day number to day/month/year. Parameter jd is an integer
    '''
    #a, b, c, d, e, m, day, month, year
    if (jd > 2299160): # After 5/10/1582, Gregorian calendar
        a = jd + 32044
        b = int((4*a+3)/146097)
        c = a - int((b*146097)/4)
    else:
        b = 0
        c = jd + 32082
    
    d = int((4*c+3)/1461)
    e = c - int((1461*d)/4)
    m = int((5*e+2)/153)
    day = e - int((153*m+2)/5) + 1
    month = m + 3 - 12*int(m/10)
    year = b*100 + d - 4800 + int(m/10)
    return (day, month, year)


def NewMoon(k):
    '''
    Compute the time of the k-th new moon after the new moon of 1/1/1900 13:52 UCT 
    (measured as the number of days since 1/1/4713 BC noon UCT, e.g., 2451545.125 is 1/1/2000 15:00 UTC).
    Returns a floating number, e.g., 2415079.9758617813 for k=2 or 2414961.935157746 for k=-2
    Algorithm from: "Astronomical Algorithms" by Jean Meeus, 1998
    '''
    #T, T2, T3, dr, Jd1, M, Mpr, F, C1, deltat, JdNew
    T = k/1236.85 #Time in Julian centuries from 1900 January 0.5
    T2 = T * T
    T3 = T2 * T
    dr = PI/180
    Jd1 = 2415020.75933 + 29.53058868*k + 0.0001178*T2 - 0.000000155*T3
    Jd1 = Jd1 + 0.00033 * np.sin((166.56 + 132.87*T - 0.009173*T2)*dr) #Mean new moon
    M = 359.2242 + 29.10535608*k - 0.0000333*T2 - 0.00000347*T3 #Sun's mean anomaly
    Mpr = 306.0253 + 385.81691806*k + 0.0107306*T2 + 0.00001236*T3 #Moon's mean anomaly
    F = 21.2964 + 390.67050646*k - 0.0016528*T2 - 0.00000239*T3 #Moon's argument of latitude
    C1=(0.1734 - 0.000393*T)*np.sin(M*dr) + 0.0021*np.sin(2*dr*M)
    C1 = C1 - 0.4068*np.sin(Mpr*dr) + 0.0161*np.sin(dr*2*Mpr)
    C1 = C1 - 0.0004*np.sin(dr*3*Mpr)
    C1 = C1 + 0.0104*np.sin(dr*2*F) - 0.0051*np.sin(dr*(M+Mpr))
    C1 = C1 - 0.0074*np.sin(dr*(M-Mpr)) + 0.0004*np.sin(dr*(2*F+M))
    C1 = C1 - 0.0004*np.sin(dr*(2*F-M)) - 0.0006*np.sin(dr*(2*F+Mpr))
    C1 = C1 + 0.0010*np.sin(dr*(2*F-Mpr)) + 0.0005*np.sin(dr*(2*Mpr+M))
    if (T < -11):
        deltat= 0.001 + 0.000839*T + 0.0002261*T2 - 0.00000845*T3 - 0.000000081*T*T3
    else:
        deltat= -0.000278 + 0.000265*T + 0.000262*T2
    JdNew = Jd1 + C1 - deltat
    return JdNew


def getNewMoonDay(k, timeZone):
    '''
    Compute the day of the k-th new moon in the given time zone.
    The time zone if the time difference between local time and UTC: 7.0 for UTC+7:00
    '''
    return int(NewMoon(k) + 0.5 + timeZone/24)


def SunLongitude(jdn):
    '''
    Compute the longitude of the sun at any time.
    Parameter: floating number jdn, the number of days since 1/1/4713 BC noon
    Algorithm from: "Astronomical Algorithms" by Jean Meeus, 1998
    '''
    #var T, T2, dr, M, L0, DL, ret, theta, omega;
    T = (jdn - 2451545.0 ) / 36525;     # Time in Julian centuries from 2000-01-01 12:00:00 GMT
    T2 = T*T;
    dr = PI/180   # degree to radian
    M = 357.52910 + 35999.05030*T - 0.0001559*T2 - 0.00000048*T*T2   # mean anomaly, degree
    L0 = 280.46645 + 36000.76983*T + 0.0003032*T2                    # mean longitude, degree
    DL = (1.914600 - 0.004817*T - 0.000014*T2)*np.sin(dr*M);
    DL = DL + (0.019993 - 0.000101*T)*np.sin(dr*2*M) + 0.000290*np.sin(dr*3*M);
    theta = L0 + DL; # true longitude, degree
    # obtain apparent longitude by correcting for nutation and aberration
    omega = 125.04 - 1934.136 * T;
    ret = theta - 0.00569 - 0.00478 * np.sin(omega * dr);
    # Convert to radians
    ret = ret*dr;
    ret = ret - PI*2*(int(ret/(PI*2))); # Normalize to (0, 2*PI)
    return ret;


def getSunLongitude(dayNumber, timeZone):
    '''
    Compute sun position at midnight of the day with the given Julian day number. 
    The time zone if the time difference between local time and UTC: 7.0 for UTC+7:00.
    The def returns a number between 0 and 11. 
    From the day after March equinox and the 1st major term after March equinox, 0 is returned. 
    After that, return 1, 2, 3 ...
    '''
    return int(SunLongitude(dayNumber - 0.5 - timeZone/24)/PI*6)



def getLunarMonth11(yy, timeZone):
    '''
    Find the day that starts the luner month 11 of the given year for the given time zone
    '''
    #k, off, nm, sunLong
    #off = jdFromDate(31, 12, yy) - 2415021.076998695
    off = jdFromDate(31, 12, yy) - 2415021
    k = int(off / 29.530588853)
    nm = getNewMoonDay(k, timeZone)
    sunLong = getSunLongitude(nm, timeZone) #sun longitude at local midnight
    if (sunLong >= 9):
        nm = getNewMoonDay(k-1, timeZone)
    return nm


def getLeapMonthOffset(a11, timeZone):
    '''
    Find the index of the leap month after the month starting on the day a11.
    '''
    #k, last, arc, i
    k = int((a11 - 2415021.076998695) / 29.530588853 + 0.5)
    last = 0
    i = 1 #We start with the month following lunar month 11
    arc = getSunLongitude(getNewMoonDay(k+i, timeZone), timeZone)
    while (arc != last and i < 14):
        last = arc
        i += 1
        arc = getSunLongitude(getNewMoonDay(k+i, timeZone), timeZone)
    return i-1


def convertSolar2Lunar(dd, mm, yy, timeZone):
    '''
    Comvert solar date dd/mm/yyyy to the corresponding lunar date
    '''
    #k, dayNumber, monthStart, a11, b11, lunarDay, lunarMonth, lunarYear, lunarLeap
    dayNumber = jdFromDate(dd, mm, yy)
    k = int((dayNumber - 2415021.076998695) / 29.530588853)
    monthStart = getNewMoonDay(k+1, timeZone)
    if (monthStart > dayNumber):
        monthStart = getNewMoonDay(k, timeZone)
    #alert(dayNumber+" -> "+monthStart)
    a11 = getLunarMonth11(yy, timeZone)
    b11 = a11
    if (a11 >= monthStart):
        lunarYear = yy
        a11 = getLunarMonth11(yy-1, timeZone)
    else:
        lunarYear = yy+1
        b11 = getLunarMonth11(yy+1, timeZone)
    lunarDay = dayNumber-monthStart+1
    diff = int((monthStart - a11)/29)
    lunarLeap = 0
    lunarMonth = diff+11
    if (b11 - a11 > 365):
        leapMonthDiff = getLeapMonthOffset(a11, timeZone)
        if (diff >= leapMonthDiff):
            lunarMonth = diff + 10
            if (diff == leapMonthDiff):
                lunarLeap = 1
    if (lunarMonth > 12):
        lunarMonth = lunarMonth - 12

    if (lunarMonth >= 11 and diff < 4):
        lunarYear -= 1
    return (lunarDay, lunarMonth, lunarYear, lunarLeap)


def convertLunar2Solar(lunarDay, lunarMonth, lunarYear, lunarLeap, timeZone):
    '''
    Convert a lunar date to the corresponding solar date
    '''
    #k, a11, b11, off, leapOff, leapMonth, monthStart
    if (lunarMonth < 11):
        a11 = getLunarMonth11(lunarYear-1, timeZone)
        b11 = getLunarMonth11(lunarYear, timeZone)
    else:
        a11 = getLunarMonth11(lunarYear, timeZone)
        b11 = getLunarMonth11(lunarYear+1, timeZone)
    k = int(0.5 + (a11 - 2415021.076998695) / 29.530588853)
    off = lunarMonth - 11
    if (off < 0):
        off += 12

    if (b11 - a11 > 365):
        leapOff = getLeapMonthOffset(a11, timeZone)
        leapMonth = leapOff - 2
        if (leapMonth < 0):
            leapMonth += 12
        
        if (lunarLeap != 0 and lunarMonth != leapMonth):
            return (0, 0, 0)
        elif (lunarLeap != 0 or off >= leapOff):
            off += 1
    monthStart = getNewMoonDay(k+off, timeZone)
    return jdToDate(monthStart+lunarDay-1)

def findEvents(dd, mm):
    ret = []
    for evt in YEARLY_EVENTS:
        #evt = YEARLY_EVENTS[$i];
        if (evt.day == dd and evt.month == mm):
            ret.append(evt)
    return ret


def getDayInfo(dd, mm):
    events = findEvents(dd, mm)
    #print(events)
    #echo count($events);
    ret = ''
    for evt in events:
        ret += evt.info + ' '
    ret += ' '
    return ret


def getYearCanChi(year):
    return CAN[(year+6) % 10] + " " + CHI[(year+8) % 12];


def getCanHour0(jdn):
    '''
    Can cua gio Chinh Ty (00:00) cua ngay voi JDN nay
    '''
    return CAN[(jdn-1)*2 % 10];



def getSolarTerm(dayNumber, timeZone):
    '''
    Compute the sun segment at start (00:00) of the day with the given integral Julian day number.
    The time zone if the time difference between local time and UTC: 7.0 for UTC+7:00.
    The function returns a number between 0 and 23.
    From the day after March equinox and the 1st major term after March equinox, 0 is returned.
    After that, return 1, 2, 3 ...
    '''
    return int(SunLongitude(dayNumber - 0.5 - timeZone/24.0) / PI * 12);


def getGioHoangDao(jd):
    chiOfDay = (jd+1) % 12;
    gioHD = GIO_HD[chiOfDay % 6];   # same values for Ty' (1) and Ngo. (6), for Suu and Mui etc.
    ret = ""
    count = 0
    for i in range(12):  
        if (gioHD[i] == '1'):
            ret += CHI[i]
            ret += ' (' + str((i*2+23)%24) + '-'+ str((i*2+1)%24) + ')'
            count += 1
            if (count < 5): ret += ', '
            #if (count == 3): ret += '\n'
    return ret;


def showDayInfo(cell, dd, mm, yy, leap, length, jd, sday, smonth, syear):  # sday : solar day (DL), dd : moon day (AL)
    tz = 1.0
    #selectCell($cellId);
    #alert('Cell '+cellId+': '+dd+'/'+mm+'/'+yy+" AL = "+sday+"/"+smonth+"/"+$syear);
    #document.NaviForm.$dd.value = $dd;
    #document.getElementById("thangduong").innerHTML =
    print('Ngày ' + str(sday) + ' Tháng '+ str(smonth) +' năm '+ str(syear))
    #document.getElementById("ngayduong").innerHTML =
    #print(sday)
    dayOfWeek = TUAN[(jd + 1) % 7]
    #document.getElementById("thuduong").innerHTML =
    print(dayOfWeek)
    #document.getElementById("ngayam").innerHTML = $
    print(dd, end=' ')  # jour lunaire
    #nhuan = (leap == 1) ? ' nhu\u1EADn' : ''
    nhuan = ' nhu\u1EADn' if leap == 1 else ''
    tenthang = 'Th\u00E1ng ' + THANG[mm-1] + nhuan + (' (\u0110)' if length == 30 else ' (T)');
    #document.getElementById("thangam").innerHTML = $
    print(tenthang, end=' ')
    #document.getElementById("namam").innerHTML =
    print('N\u0103m '+ getYearCanChi(yy))
    thang = CAN[(yy*12+mm+3) % 10] + " " + CHI[(mm+1)%12]
    #document.getElementById("canchithang").innerHTML =
    print('Th\u00E1ng '+ thang)
    ngay = CAN[(jd + 9) % 10] + " " + CHI[(jd+1)%12]
    #document.getElementById("canchingay").innerHTML =
    print('Ng\u00E0y '+ ngay)
    #document.getElementById("canchigio").innerHTML =
    print('Gi\u1EDD '+ getCanHour0(jd)+' '+ CHI[0])
    #document.getElementById("tietkhi").innerHTML =
    print('Ti\u1EBFt '+ TIETKHI[getSolarTerm(jd+1, tz)])
    #document.getElementById("dayinfo").innerHTML =
    print(getDayInfo(dd, mm))
    #document.getElementById("hoangdao").innerHTML =
    print('Gi\u1EDD ho\u00E0ng \u0111\u1EA1o: '+ getGioHoangDao(jd))
    #document.NaviForm.submit(); 


def leap(year):
    '''7 fois en 19 ans'''
    sequence = (0,3,6,9,11,14,17)
    if year%19 in sequence : return True
    else : return False


tropic_year = 365.2421898    #jours
synodic_period = 29.530588853  #jours

def div_euclid(n,m):   # n>m
    ent = n//m
    ret = int(n/m)
    frac = n-(m*ent)
    return ent, frac, ret


def frac_cont(n,m):
    ret = ''
    fc = []
    while m != 1 and m > 0.0:
        #print(n,m, ret)
        old = m
        n, m, ret = div_euclid(n,m)
        n = old
        fc.append(ret)
    return fc


def dev_frac(fc, rang):
    if rang == 1 : return fc[0]
    fs = fc[0:rang]
    print(fs)
    s = 0 
    for r in range(1,rang):
        s = 1/(fs[-r]+s)
    return s + fs[0]