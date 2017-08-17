#_*_ coding:utf-8 _*_

import urllib.request
import json
import datetime

# return date as list format in yyyymmdd format from specified start date and end date
def datestartend(startdate, enddate):
    start = datetime.datetime.strptime(startdate, '%Y%m%d')
    end = datetime.datetime.strptime(enddate, '%Y%m%d')
    daypassed = 0
    this_date = start + datetime.timedelta(days=daypassed)
    datelist = []
    while end > this_date:
        this_date = start + datetime.timedelta(days=daypassed)
        datelist.append(this_date.strftime('%Y%m%d'))
        daypassed = daypassed + 1
    return datelist

# file create with header and utf-8 encoding
def boxoffice_header_create(filename):
    f = open(filename, mode='w', encoding='utf-8')
    header = "date\trnum\trank\trankInten\trankOldAndNew\tmovieCd\tmovieNm\topenDt\tsalesAmt\tsalesShare\tsalesInten\tsalesChange\tsalesAcc\taudiCnt\taudiInten\taudiChange\taudiAcc\tscrnCnt\tshowCnt\n"
    f.write(header)
    f.close()

# need api key
def kofic_boxoffice_downloader(key, date, filename):
    print(date + "started")

    # url = ("http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json?key=%s&targetDt=%s" % (key, date))
    # 하루기준 10개 만 뽑을 수 있어서 상업영화여부와 한국영화여부를 넣어 하루 기준 40개를 뽑기로 했습니다.
    # 지역 코드도 있으니 필요하면 시군구별 통계도 뽑을 수 있어요
    urlA = (
        "http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json?multiMovieYn=Y&repNationCd=K&key=%s&targetDt=%s" % (
            key, date))
    urlB = (
        "http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json?multiMovieYn=N&repNationCd=K&key=%s&targetDt=%s" % (
            key, date))
    urlC = (
        "http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json?multiMovieYn=Y&repNationCd=F&key=%s&targetDt=%s" % (
            key, date))
    urlD = (
        "http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json?multiMovieYn=N&repNationCd=F&key=%s&targetDt=%s" % (
            key, date))
    urlList = [urlA, urlB, urlC, urlD]
    for url in urlList:
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)
        http_code = response.getcode()
        if http_code == 200:
            response_body = response.read()
            # print(response_body.decode('utf-8'))
            boxOfficeResults = json.loads(response_body.decode('utf-8'))
            # print(boxOfficeResults)
            for dailyBoxOffice in boxOfficeResults['boxOfficeResult']['dailyBoxOfficeList']:
                boxoffice_one_line = (
                    u"%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (
                        date, dailyBoxOffice['rnum'], dailyBoxOffice['rank'], dailyBoxOffice['rankInten'],
                        dailyBoxOffice['rankOldAndNew'], dailyBoxOffice['movieCd'], dailyBoxOffice['movieNm'],
                        dailyBoxOffice['openDt'], dailyBoxOffice['salesAmt'], dailyBoxOffice['salesShare'],
                        dailyBoxOffice['salesInten'], dailyBoxOffice['salesChange'], dailyBoxOffice['salesAcc'],
                        dailyBoxOffice['audiCnt'], dailyBoxOffice['audiInten'], dailyBoxOffice['audiChange'],
                        dailyBoxOffice['audiAcc'], dailyBoxOffice['scrnCnt'], dailyBoxOffice['showCnt']))
                f = open(filename, mode='a', encoding='utf-8')
                f.write(boxoffice_one_line)
                f.close()
        else:
            print("Error Code:" + http_code)
    print(date + "ocmpleted")

# main이죠
datestart = "20160324"
dateend = "20161231"
apikey = "x"
#boxoffice_header_create("boxoffice_%s_%s.txt" % (datestart, dateend))
#시작일 부터 끝나는 날 까지 다 모아서 적습니다.
for date in datestartend(datestart, dateend):
    kofic_boxoffice_downloader(apikey, date, "boxoffice.txt")


