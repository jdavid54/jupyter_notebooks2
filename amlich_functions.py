#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
['ABOUT', 'CAN', 'CHI', 'DAYNAMES', 'FONT_SIZES', 'GIO_HD', 'LunarDate', 'OutputOptions', 'PI', 'PRINT_OPTS',
'SunLongitude', 'TAB_WIDTHS', 'THANG', 'TIETKHI', 'TK13', 'TK14', 'TK15', 'TK16', 'TK17', 'TK18', 'TK19', 'TK20',
'TK21', 'TK22', 'TUAN', 'Tk_data', 'YEARLY_EVENTS', 'YearlyEvent', '__builtins__', '__cached__', '__doc__',
'__file__', '__loader__', '__name__', '__package__', '__spec__', 'alert', 'alertAbout', 'alertDayInfo',
'calendar', 'currentLunarDate', 'datetime', 'debug', 'decodeLunarYear', 'findLunarDate', 'getCanChi',
'getCanHour0', 'getCurrentTime', 'getDayName', 'getDayString', 'getGioHoangDao', 'getLunarDate', 'getMonth',
'getNextMonthLink', 'getNextYearLink', 'getPrevMonthLink', 'getPrevYearLink', 'getSelectedMonth', 'getSolarDate',
'getSolarTerm', 'getSunLongitude', 'getTodayString', 'getYearCanChi', 'getYearCode', 'getYearInfo', 'infoCellSelect',
'jdn', 'jdn2date', 'lunar_month', 'math', 'messagebox', 'month', 'month_cal', 'monthcalendar', 'monthrange',
'np', 'parseQuery', 'printCell', 'printEmptyCell', 'printFoot', 'printHead', 'printMonth', 'printSelectedMonth',
'printSelectedYear', 'printStyle', 'printTable', 'printYear', 'res', 'root', 'setOutputSize', 'showMonthSelect',
'showVietCal', 'showYearSelect', 'test_LunarDate', 'test_getSunlongitude', 'test_jdn', 'test_leap_month',
'test_longitude', 'test_solarDate', 'test_yearInfo', 'tkinter', 'today', 'today_info', 'weekday', 'write2file', 'year']
'''
debug = False

# imports
import numpy as np
import math
import datetime
from calendar import monthrange, monthcalendar, calendar
PI = np.pi
# https://docs.python.org/3/library/calendar.html#calendar.monthrange
# Python 3.x code
import tkinter
#https://docs.python.org/3/library/tkinter.html
from tkinter import messagebox

# include from files
from amlich_data import *

# This code is to hide the main tkinter window
root = tkinter.Tk()
root.withdraw()
# Message Box
# messagebox.showinfo("Title", "Message")

# functions
def jdn(dd, mm, yy):
    a = int((14 - mm) / 12);
    y = yy+4800-a;
    m = mm+12*a-3;
    jd = dd + int((153*m+2)/5) + 365*y + int(y/4) - int(y/100) + int(y/400) - 32045;
    return jd;
    #return 367*yy - int(7*(yy+int((mm+9)/12))/4) - int(3*(int((yy+(mm-9)/7)/100)+1)/4) + int(275*mm/9)+dd+1721029;

def jdn2date(jd):
    #Z, A, alpha, B, C, D, E, dd, mm, yyyy, F;
    Z = jd;
    if (Z < 2299161):
      A = Z;
    else:
      alpha = int((Z-1867216.25)/36524.25);
      A = Z + 1 + alpha - int(alpha/4);

    B = A + 1524;
    C = int( (B-122.1)/365.25);
    D = int( 365.25*C );
    E = int( (B-D)/30.6001 );
    dd = int(B - D - int(30.6001*E));
    if (E < 14):
      mm = E - 1;
    else:
      mm = E - 13;
    if (mm < 3):
      yyyy = C - 4715;
    else:
      yyyy = C - 4716;
    return (dd, mm, yyyy)

def decodeLunarYear(yy, k):
    # k = getYearCode(yy) from Tk tables  -- called by getYearInfo(yyyy)
    # monthLengths, regularMonths, offsetOfTet, leapMonth, leapMonthLength, solarNY, currentJD, j, mm;
    ly = [];
    monthLengths = [29, 30];
    regularMonths = ['']*12;
    if debug: print(bin(k))
    offsetOfTet = k >> 17;
    leapMonth = k & 0xf;
    leapMonthLength = monthLengths[k >> 16 & 0x1];
    solarNY = jdn(1, 1, yy);
    currentJD = solarNY + offsetOfTet;
    j = k >> 4;
    for i in range(12):                    
        regularMonths[12-i-1] = monthLengths[j & 0x1];
        j >>= 1;
     
    if (leapMonth == 0):
        for mm in range(1, 13):              
            ly.append(LunarDate(1, mm, yy, 0, currentJD));
            currentJD += regularMonths[mm-1];        
    else:  # create leapYear which begins at offsetTet after Solar new year
        # append ly first months to leapMonth
        for mm in range(1, leapMonth+1):
            ly.append(LunarDate(1, mm, yy, 0, currentJD));
            currentJD += regularMonths[mm-1];
        #insert a month with leapMontLenght after leapMonth with leap = 1
        ly.append(LunarDate(1, leapMonth, yy, 1, currentJD));
        currentJD += leapMonthLength;
        # append the months after leapMonth
        for mm in range(leapMonth+1,13):  #; mm <= 12; mm++):
            ly.append(LunarDate(1, mm, yy, 0, currentJD));
            currentJD += regularMonths[mm-1];
    return ly

def findLunarDate(jd, ly):
    FIRST_DAY = jdn(25, 1, 1800); ## Tet am lich 1800
    LAST_DAY = jdn(31, 12, 2199);

    if (jd > LAST_DAY or jd < FIRST_DAY or ly[0].jd > jd):
        return LunarDate(0, 0, 0, 0, jd);
    i = len(ly)-1;
    while (jd < ly[i].jd):
        i -= 1

    off = jd - ly[i].jd;
    ret = LunarDate(ly[i].day+ off, ly[i].month, ly[i].year, ly[i].leap, jd);
    return ret;

def SunLongitude(jdn):
    '''
    Compute the longitude of the sun at any time.
    Parameter: floating number jdn, the number of days since 1/1/4713 BC noon
    Algorithm from: "Astronomical Algorithms" by Jean Meeus, 1998
    '''
    #T, T2, dr, M, L0, DL, ret, theta, omega;
    T = (jdn - 2451545.0 ) / 36525;     # Time in Julian centuries from 2000-01-01 12:00:00 GMT
    T2 = T*T;
    dr = PI/180   # degree to radian
    M = 357.52910 + 35999.05030*T - 0.0001559*T2 - 0.00000048*T*T2   # mean anomaly, degree
    L0 = 280.46645 + 36000.76983*T + 0.0003032*T2                    # mean longitude, degree
    DL = (1.914600 - 0.004817*T - 0.000014*T2)*math.sin(dr*M);
    DL = DL + (0.019993 - 0.000101*T)*math.sin(dr*2*M) + 0.000290*math.sin(dr*3*M);
    theta = L0 + DL; # true longitude, degree
    # obtain apparent longitude by correcting for nutation and aberration
    omega = 125.04 - 1934.136 * T;
    lon = theta - 0.00569 - 0.00478 * math.sin(omega * dr);
    # Convert to radians
    lon = lon*dr;
    #ret = ret - PI*2*(int(ret/(PI*2))); # Normalize to (0, 2*PI)
    lon = lon%(2*PI)
    return lon

def lunar_month(month, year):  # solar month
    s = ''
    weekday_first, month_length = monthrange(year, month)  #weekday of the first day, length of month
    #print(mr)
    #firstday = mr[0]
    #print(weekday[firstday])
    d = datetime.datetime.today().day
    ld  = getLunarDate(d, month, year)
    #print('Th\u00E1ng ', THANG[ld.month-1], ld.year)
    s += 'Th\u00E1ng '+str(THANG[ld.month-1])+' '+str(ld.year)+'\n'      # solar month
    for wd in weekday:
        #print(wd, end='\t')
        s += str(wd)+'\t'
    #print()
    s += '\n'
    for d in range(weekday_first):
        #print(' ', end='\t')
        s += ' \t'        
    for d in range(1,month_length+1):
        ld = getLunarDate(d, month, year).day
        ld = str(d)+'/'+str(ld)
        #s += ld
        if d == datetime.datetime.today().day:
            ld = '('+str(ld)+')'
        s += ld + '\t'
        #print(ld, end='\t')
        if (weekday_first+d)%7 == 0 :
            #print()
            s += '\n'
    #print()
    return s

def alert(title, msg):
    #root = tkinter.Tk()
    #root.withdraw()
    messagebox.showinfo(title, msg)
    
def alertDayInfo(dd, mm, yy, leap, jd, sday, smonth, syear):
    lunar = LunarDate(dd, mm, yy, leap, jd);
    s = getDayString(lunar, sday, smonth, syear);
    s += " \u00E2m l\u1ECBch\n";
    s += getDayName(lunar)+'\n';
    s += "\nGi\u1EDD \u0111\u1EA7u ng\u00E0y: "+getCanHour0(jd)+" "+CHI[0]+'\n';
    s += "Ti\u1EBFt: "+TIETKHI[getSunLongitude(jd+1, 7.0)]+'\n';
    s += "Gi\u1EDD ho\u00E0ng \u0111\u1EA1o: "+getGioHoangDao(jd);
    #alert('Day info', s);
    tk_show(s, 'Today info')

def alertAbout():
    alert('About', ABOUT);

from tkinter import Tk, Text

def tk_show(s, title="Month calendar"):
    root = Tk()
    root.geometry("600x140")
    root.resizable(False, False)
    root.title(title)
    text = Text(root, height=8)
    text.pack()
    text.insert('1.0', s)
    #root.mainloop()

def today_info():
    today = datetime.datetime.today()
    ld = getLunarDate(today.day,today.month,today.year)       #-> class LunarDate(day=10, month=1, year=2021, leap=0, jd=2459267)
    yearname = getYearCanChi(ld.year)                         #->'Tân Sửu'
    dayname = getDayName(ld)                                  #'Ngày Canh Tý, tháng Canh Dần, năm Tân Sửu'
    #jd = jdn(today.day,today.month,today.year)
    daystr = getDayString(ld, today.day, today.month, today.year)  
#     print(daystr)                                             #'Chủ nhật 21/2/2021 -+- Ngày 10 tháng 1'
#     print(getCurrentTime())                                   #-> '11:03:04'
#     print(dayname)
#     print('Gi\u1EDD Ho\u00E0ng \u0110\u1EA1o : ',getGioHoangDao(ld.jd))    #-> 'Tý (23-1), Sửu (1-3), Mão (5-7), Ngọ (11-13), Thân (15-17)Dậu (17-19)'    
#     alertDayInfo(ld.day, ld.month, ld.year, ld.leap, ld.jd, today.day, today.month, today.year)
    return daystr

# month calendar
def month_cal(year, month):
    m_cal = monthcalendar(year, month)
    for k in range(len(m_cal)):
        for d in m_cal[k]:
            if d == 0 : d=' '
            print(d, end='\t')
        print()
    print()
#month_cal(year, month)
    
# ===================================================== get methods
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
    if debug: print(hex(yearCode))
    return yearCode

def getYearInfo(yyyy):  # same as decodeLunarYear(yy, k) using only year variable
    return decodeLunarYear(yyyy, getYearCode(yyyy));  

def getLunarDate(dd, mm, yyyy):
    #ly, jd;
    if (yyyy < 1800 or 2199 < yyyy):
        return LunarDate(0, 0, 0, 0, 0);
    ly = getYearInfo(yyyy);
    #if debug: print(ly)
    jd = jdn(dd, mm, yyyy);
    if (jd < ly[0].jd):
        ly = getYearInfo(yyyy - 1);
        #if debug: print(ly)
    return findLunarDate(jd, ly);

def getSolarTerm(dayNumber, timeZone):
    '''
    Compute the sun segment at start (00:00) of the day with the given integral Julian day number.
    The time zone if the time difference between local time and UTC: 7.0 for UTC+7:00.
    The def returns a number between 0 and 23.
    From the day after March equinox and the 1st major term after March equinox, 0 is returned.
    After that, return 1, 2, 3 ...
    '''
    return int(SunLongitude(dayNumber - 0.5 - timeZone/24.0) / PI * 12);

def getSunLongitude(dayNumber, timeZone):
    return int(SunLongitude(dayNumber - 0.5 - timeZone/24.0) / PI * 12);

def getSolarDate(dd, mm, yyyy):   # call getYearInfo(), jdn2date()
    if (yyyy < 1200 or 2199 < yyyy):
        return LunarDate(0, 0, 0, 0, 0);
    
    ly = getYearInfo(yyyy);
    if debug: print(ly, len(ly))
    lm = ly[mm-1];
    if debug: print(lm)
    if (lm.month != mm):
        lm = ly[mm];
    
    ld = lm.jd + dd - 1;
    return jdn2date(ld);

def getYearCanChi(year):
    return CAN[(year+6) % 10] + " " + CHI[(year+8) % 12];

def getSelectedMonth():
    query = window.location.search;
    arr = parseQuery(query);
    idx;
    for idx in range(len(arr)):       # = 0; idx < arr.length; idx++):
        if (arr[idx] == "mm"):
            currentMonth = parseInt(arr[idx+1]);
        elif (arr[idx] == "yy"):
            currentYear = parseInt(arr[idx+1]);
        
# rotation section
def getMonth(mm, yy):
    #ly1, ly2, tet1, jd1, jd2, mm1, yy1, result, i;
    if (mm < 12):
        mm1 = mm + 1;
        yy1 = yy;
    else:
        mm1 = 1;
        yy1 = yy + 1;

    jd1 = jdn(1, mm, yy);
    jd2 = jdn(1, mm1, yy1);
    ly1 = getYearInfo(yy);
    #alert('1/'+mm+'/'+yy+' = '+jd1+'; 1/'+mm1+'/'+yy1+' = '+jd2);
    tet1 = ly1[0].jd;
    result = [];
    if (tet1 <= jd1):                     # tet(yy) = tet1 < jd1 < jd2 <= 1.1.(yy+1) < tet(yy+1) */
        for i in range(jd1,jd2):          # = jd1; i < jd2; i++):
            result.append(findLunarDate(i, ly1));
        
    elif (jd1 < tet1 and jd2 < tet1):     # tet(yy-1) < jd1 < jd2 < tet1 = tet(yy) */
        ly1 = getYearInfo(yy - 1);
        for i in range(jd1,jd2):          # = jd1; i < jd2; i++):
            result.append(findLunarDate(i, ly1));
        
    elif (jd1 < tet1 and tet1 <= jd2):    # tet(yy-1) < jd1 < tet1 <= jd2 < tet(yy+1) */
        ly2 = getYearInfo(yy - 1);
        for i in range(jd1,tet1):         # = jd1; i < tet1; i++):
            result.append(findLunarDate(i, ly2));
        
        for i in range(tet1,jd2):         # = tet1; i < jd2; i++):
            result.append(findLunarDate(i, ly1));
    return result;

def getDayName(lunarDate):
    today = datetime.datetime.today()
    if (lunarDate.day == 0):
        return "";

    cc = getCanChi(lunarDate);
    s = "Ng\u00E0y " + cc[0] +", th\341ng "+cc[1] + ", n\u0103m " + cc[2];
    jd = jdn(today.day,today.month,today.year)
    s += ", Ti\u1EBFt: "+TIETKHI[getSunLongitude(jd+1, 7.0)]
    return s;

def getYearCanChi(year):
    return CAN[(year+6) % 10] + " " + CHI[(year+8) % 12];

'''
 * Can cua gio Chinh Ty (00:00) cua ngay voi JDN nay
'''
def getCanHour0(jdn):
    return CAN[(jdn-1)*2 % 10];

def getCanChi(lunar):  #-> Lunar name of the year
    #dayName, monthName, yearName;
    dayName = CAN[(lunar.jd + 9) % 10] + " " + CHI[(lunar.jd+1)%12];
    monthName = CAN[(lunar.year*12+lunar.month+3) % 10] + " " + CHI[(lunar.month+1)%12];
    if (lunar.leap == 1):
        monthName += " (nhu\u1EADn)";

    yearName = getYearCanChi(lunar.year);
    return (dayName, monthName, yearName);

def getDayString(lunar, solarDay, solarMonth, solarYear):
    #s;
    dayOfWeek = TUAN[(lunar.jd + 1) % 7];
    s = str(dayOfWeek) + " " + str(solarDay) + "/" + str(solarMonth) + "/" + str(solarYear);
    s += " -+- ";
    s = s + "Ng\u00E0y " + str(lunar.day) +" th\341ng "+ str(lunar.month);
    if (lunar.leap == 1):
        s = s + " nhu\u1EADn";
    return s;

def getTodayString():
    today = datetime.datetime.today()
    #print(today.day, today.month, today.year)
    currentLunarDate = getLunarDate(today.day, today.month, today.year);
    #print(currentLunarDate)
    #currentMonth = currentLunarDate.month+1;
    #currentYear = currentLunarDate.year;
    s = getDayString(currentLunarDate, today.day, today.month+1, today.year);
    s += " n\u0103m " + getYearCanChi(currentLunarDate.year);
    return s;

def getCurrentTime():
    today = datetime.datetime.today()   
    Std = today.hour;
    Min = today.minute;
    Sec = today.second;
    s1  = ("0" + str(Std) if (Std < 10) else str(Std));
    s2  = ("0" + str(Min) if (Min < 10) else str(Min));
    s3  = ("0" + str(Sec) if (Sec < 10) else str(Sec));
    #s3  = ((Sec < 10) ? "0" + Sec : Sec);
    #return s1 + ":" + s2 + ":" + s3;
    return s1 + ":" + s2 + ":" + s3;

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
            #if (count == 3): ret += ''
    return ret;

# changing month
def getPrevMonthLink(mm, yy):
    mm1 = mm-1 if mm > 1 else 12;
    yy1 = yy if mm > 1 else yy-1;
    #return '<a href="'+window.location.pathname+'?yy='+yy1+'&mm='+mm1+'"><img src="left1.gif" width=8 height=12 alt="PrevMonth" border=0></a>';
    return '<a href="'+window.location.pathname+'?yy='+yy1+'&mm='+mm1+'">&lt;</a>';

def getNextMonthLink(mm, yy):
    mm1 = mm+1 if mm < 12 else 1;
    yy1 = yy if mm < 12 else yy+1;
    #return '<a href="'+window.location.pathname+'?yy='+yy1+'&mm='+mm1+'"><img src="right1.gif" width=8 height=12 alt="NextMonth" border=0></a>';
    return '<a href="'+window.location.pathname+'?yy='+yy1+'&mm='+mm1+'">&gt;</a>';

# changing year
def getPrevYearLink(mm, yy):
    #return '<a href="'+window.location.pathname+'?yy='+(yy-1)+'&mm='+mm+'"><img src="left2.gif" width=16 height=12 alt="PrevYear" border=0></a>';
    return '<a href="'+window.location.pathname+'?yy='+(yy-1)+'&mm='+mm+'">&lt;&lt;</a>';

def getNextYearLink(mm, yy):
    #return '<a href="'+window.location.pathname+'?yy='+(yy+1)+'&mm='+mm+'"><img src="right2.gif" width=16 height=12 alt="NextYear" border=0></a>';
    return '<a href="'+window.location.pathname+'?yy='+(yy+1)+'&mm='+mm+'">&gt;&gt;</a>';

#============================================================= Test des méthodes
def test_jdn():
    print('111 jdn - jdn2date')
    jd = jdn(20,2,2021)
    print(jd)
    dat = jdn2date(jd)
    print(dat)

def test_yearInfo():
    print('163 getYearInfo - decodeLunarYear')
    info = getYearInfo(2021)
    print(info)     #call __repr__()
    for evt in info:
        print(evt)  # call __str__()

def test_longitude():
    print('SunLongitude(jdn)')
    print(SunLongitude(jd))

def test_getSunlongitude():
    print('getSunLongitude(jdn)')
    print(SunLongitude(jd))

def test_solarDate():
    print('getSolarDate()')
    sol_date =getSolarDate(20, 2, 2021)
    print(sol_date)

def test_LunarDate():
    print('getLunarDate - findLunarDate')
    info = getLunarDate(20, 2, 2021)
    print(info)     #call __repr__() return day, month, year, leap, jd
    # return 9, 0, 2021, 0, 2459266
    #showDayInfo(20,9,1,2021,0,29,2459266,20,2,2021);
    today = datetime.datetime.today()
    if debug: print(today.day, today.month, today.year)
    currentLunarDate = getLunarDate(today.day, today.month, today.year);
    if debug: print(currentLunarDate)
    currentMonth = currentLunarDate.month+1;
    currentYear = currentLunarDate.year;
    print(currentLunarDate.day, currentMonth,currentYear)
    print('OK')

# test leapmonth number
def test_leap_month():
    leapmonth = ((1995,8),(1998,5),(2001,4),(2004,2),
                 (2006,7),(2009,5), (2012,4),
                 (2014,9),(2017,6),(2020,4),(2023,2),
                 (2025,6),(2028,5),(2031,3))

    print(2017, Tk_data(getYearCode(2017)).leapMonth)    #-> leapmonth=6
    print(1995, Tk_data(getYearCode(1995)).leapMonth)    #-> leapmonth=8
    
    print(Tk_data(getYearCode(2021))) #-> Tk_data(offset Tet=42,
                                        #leap month number=0,
                                        #leap month lenght=29,
                                        #regular months lenght=[29, 30, 30, 29, 30, 29, 30, 29, 30, 29, 30, 29]),

#=============================================================================
# for html use
#=============================================================================
def parseQuery(q):
    ret = [];
    if (q.length < 2): return ret;
    s = q.substring(1, q.length);
    arr = s.split("&");
    #i, j;
    
    for i in range(len(arr)):       #= 0; i < arr.length; i++):
        a = arr[i].split("=");
        for j in range(len(a)):     # = 0; j < a.length; j++):
            ret.append(a[j]);
    return ret;

'''
DAYNAMES = ("CN", "T2", "T3", "T4", "T5", "T6", "T7");
PRINT_OPTS = new OutputOptions();
FONT_SIZES = ("9pt", "13pt", "17pt");
TAB_WIDTHS = ("180px", "420px", "600px");

def OutputOptions():
    this.fontSize = "13pt";
    this.tableWidth = "420px";
'''
#print(PRINT_OPTS)

def setOutputSize(size):
    if size == "small":
        idx = 0;
    elif size == "big":
        idx = 2;
    else:
        idx = 1;

    PRINT_OPTS.fontSize = FONT_SIZES[idx]
    PRINT_OPTS.tableWidth = TAB_WIDTHS[idx]
    return PRINT_OPTS

# ============================================ print
def printSelectedMonth():
    getSelectedMonth();
    return printMonth(currentMonth, currentYear);


def printSelectedYear():
    getSelectedMonth();
    return printYear(currentYear);
    
def printStyle():
    fontSize = PRINT_OPTS.fontSize;
    res = "";
    res += '<style type="text/css">\n';
    res += '<!--';
    #res += '  body:margin:0\n';
    res += '  .mois {padding-right : 10px;padding-left : 10px;}\n';
    res += '  .tennam {text-align:center; font-size:150%; line-height:120%; font-weight:bold; color:#000000; background-color:#FFD400}\n';
    res += '  .thang {font-size: '+fontSize+'; padding:1; line-height:100%; font-family:Tahoma,Verdana,Arial; table-layout:fixed}\n';
    res += '  .tenthang {text-align:center; font-size:125%; line-height:100%; font-weight:bold; color:#330033; background-color: #CCFFCC}\n';
    res += '  .navi-l {text-align:center; font-size:75%; line-height:100%; font-family:Verdana,Times New Roman,Arial; font-weight:bold; color:red; background-color: #CCFFCC}\n';
    res += '  .navi-r {text-align:center; font-size:75%; line-height:100%; font-family:Verdana,Arial,Times New Roman; font-weight:bold; color:#330033; background-color: #CCFFCC}\n';
    res += '  .ngaytuan {width:14%; text-align:center; font-size:125%; line-height:100%; color:#330033; background-color: #FFFFCC}\n';
    res += '  .ngaythang {background-color:#FDFDF0}\n';
    res += '  .homnay {background-color:#FFF000}\n';
    res += '  .tet {background-color:#FFCC99}\n';
    res += '  .am {text-align:right;font-size:75%;line-height:100%;color:blue}\n';
    res += '  .am2:text-align:right;font-size:75%;line-height:100%;color:#004080}\n';
    res += '  .t2t6 {text-align:left;font-size:125%;color:black}\n';
    res += '  .t7 {text-align:left;font-size:125%;line-height:100%;color:green}\n';
    res += '  .cn {text-align:left;font-size:125%;line-height:100%;color:red}\n';
    res += '-->\n';
    res += '</style>\n';
    
    return res;

def printHead(mm, yy):
    res = "";
    monthName = str(mm)+"/"+ str(yy);
    #print(monthName)
    #res += ('<tr><td colspan="7" class="tenthang" onClick="showMonthSelect();">'+monthName+'</td></tr>');
    #res += ('<tr><td colspan="2" class="navi-l">'+getPrevYearLink(mm, yy)+' &nbsp;'+getPrevMonthLink(mm, yy)+'</td>');
    #res += ('<td colspan="1" class="navig"><a href="'+getPrevMonthLink(mm, yy)+'"><img src="left1.gif" alt="Prev"></a></td>');
    res += ('<td colspan="3" class="tenthang" onClick="showMonthSelect();">'+monthName+'</td>\n');
    #res += ('<td colspan="1" class="navi-r"><a href="'+getNextMonthLink(mm, yy)+'"><img src="right1.gif" alt="Next"></a></td>');
    #res += ('<td colspan="2" class="navi-r">'+getNextMonthLink(mm, yy)+' &nbsp;'+getNextYearLink(mm, yy)+'</td></tr>');
    #res += ('<tr><td colspan="7" class="tenthang"><a href="'+getNextMonthLink(mm, yy)+'"><img src="right.gif" alt="Next"></a></td></tr>');
    res += ('<tr onClick="alertAbout();">\n');
    for i in range(7):    #(i=0;i<=6;i++):
        res += ('<td class=ngaytuan>'+DAYNAMES[i]+'</td>');

    res += ('</tr>');
    return res;

def printEmptyCell():
    return '<td class=ngaythang><div class=cn>&nbsp;</div> <div class=am>&nbsp;</div></td>\n';


def printCell(lunarDate, solarDate, solarMonth, solarYear):
    today = datetime.datetime.today()
    #cellClass, solarClass, lunarClass, solarColor;
    cellClass = "ngaythang";
    solarClass = "t2t6";
    lunarClass = "am";
    solarColor = "black";
    dow = (lunarDate.jd + 1) % 7;
    if (dow == 0):
        solarClass = "cn";
        solarColor = "red";
    elif (dow == 6):
        solarClass = "t7";
        solarColor = "green";

    

    if solarDate == today.day and solarMonth== today.month:
        cellClass = "homnay";
        # print('day',solarDate,today.day)
        # print('month',solarMonth,today.month)
        # print('printCell',cellClass)
        
    if (lunarDate.day == 1 and lunarDate.month == 1):
        cellClass = "tet";

    if (lunarDate.leap == 1):
        lunarClass = "am2";

    lunar = lunarDate.day;
    if (solarDate == 1 or lunar == 1):
        lunar = str(lunarDate.day) + "/" + str(lunarDate.month);

    res = "";
    args = str(lunarDate.day) + "," + str(lunarDate.month) + "," + str(lunarDate.year) + "," + str(lunarDate.leap);
    args += ("," + str(lunarDate.jd) + "," + str(solarDate) + "," + str(solarMonth) + "," + str(solarYear));
    res += ('<td class="'+ str(cellClass)+'"');
    if (lunarDate != None):
        res += (' title="'+getDayName(lunarDate)+'" onClick="alertDayInfo('+args+');"');
    res += (' <div style=color:'+str(solarColor)+' class="'+str(solarClass)+'">'+str(solarDate)+'</div> <div class="'+str(lunarClass)+'">'+str(lunar)+'</div></td>\n');
    return res;

def printFoot():
    res = "";
    res += '<script language="JavaScript" src="amlich-hnd.js"></script>\n';
    return res;

def printTable(mm, yy):
    #i, j, k, solar, lunar, cellClass, solarClass, lunarClass;
    currentMonth = getMonth(mm, yy);
    #print(currentMonth)
    if (len(currentMonth) == 0): return
    ld1 = currentMonth[0]
    emptyCells = (ld1.jd + 1) % 7
    MonthHead = str(mm) + "/" + str(yy)
    LunarHead = getYearCanChi(ld1.year)
    res = "";
    res += ('<table class="thang" border="2" cellpadding="1" cellspacing="1" width="'+PRINT_OPTS.tableWidth+'">\n');
    res += printHead(mm, yy);
    for i in range(6):     # = 0; i < 6; i++):
        res += ("<tr>");
        for j in range(7):    # = 0; j < 7; j++):
            k = 7 * i + j;
            if (k < emptyCells or k >= emptyCells + len(currentMonth)):
                res += printEmptyCell();
            else:
                solar = k - emptyCells +1
                
                ld1 = currentMonth[k - emptyCells]
                # print('solar',solar,mm,'-',ld1)
                res += printCell(ld1, solar, mm, yy)        
        res += ("</tr>\n")
    res += ('</table>\n')
    return res;

# ==================================================== return html code
def printMonth(mm, yy):
    res = "";
    res += printStyle()
    res += printTable(mm, yy)
    res += printFoot()
    return res;

printTable(9,2023)


def printYear(yy, by=3):
    yearName = "N&#x103;m " + getYearCanChi(yy) + " " + str(yy);
    res = "";
    res += printStyle();
    res += '<table align=center>';
    res += ('<tr><td colspan='+str(by)+' class="tennam" onClick="showYearSelect();">'+str(yearName)+'</td></tr>');
    for i in range(1,13):     # = 1; i<= 12; i++):
        if (i % by == 1): res += '<tr>';
        res += '<td class="mois">';
        res += printTable(i, yy);
        res += '</td>';
        if (i % by == 0): res += '</tr>';
    res += '<table>';
    res += printFoot();
    return res;

def write2file(file, res):
    with open(file,'wb') as f:
        f.write(res.encode('utf-8'))

# ===================================================== open html page
def showMonthSelect():
    #home = "http:#www.ifis.uni-luebeck.de/~duc/amlich/JavaScript/";
    home = "http://www.dacluc.com/amlich-js/index.html"
    window.open(home, "win2702", "menubar=yes,scrollbars=yes,status=yes,toolbar=yes,resizable=yes,location=yes");
    #window.location = home;
    #alertAbout();
#=========================================== windows os methods
def showYearSelect():
    #window.open("selectyear.html", "win2702", "menubar=yes,scrollbars=yes");
    window.print();

def infoCellSelect(id):
    if (id == 0):
        pass

def showVietCal():
    window.status = getCurrentTime() + " -+- " + getTodayString()
    window.window.setTimeout("showVietCal()",5000)
 