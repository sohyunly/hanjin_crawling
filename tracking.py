import requests
import csv
from bs4 import BeautifulSoup
import json
import os

# 특정 url에 접속하는 요청(request) 객체를 생성
while True:
    try:
        baseUrl = 'http://www.hanjin.co.kr/delivery_html/inquiry/result_waybill.jsp?wbl_num='
        plusUrl = input("송장번호를 입력하세요: ")
        real_url = baseUrl+plusUrl

        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
        # 접속한 이후의 웹사이트 소스코드를 추출
        r = requests.get(real_url, headers=headers)
        # html 소스코드를 파이썬 객체로 변환
        soup = BeautifulSoup(r.text, 'html.parser')
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))

        # 송장번호, 상품명, 주소 문자열 추출
        numbers = soup.select('strong')[0].text.strip()
        titles = soup.select('.bb')[1].text.strip()
        addresss = soup.select('.bb')[5].text.strip()

        # 상세 배송내역 추출
        tables = soup.find_all("table")[1]
        tbodys = tables.find("tbody")
        trs = tbodys.find_all("tr")
        del trs[-1]
        # 상세 배송내역 테이블 리스트 저장
        tds_list = []

        for tr in trs:
            tds = tr.find_all("td")
            td1 = tds[0]
            td2 = tds[1]
            td3 = tds[2]
            td4 = tds[3]
            
            newdict = dict(date = td1.get_text(), time = td2.get_text(), where = td3.get_text(), state = td4.get_text().replace(" ","").replace("\n","").replace("\t","").replace("\r","")  )
            tds_list.append(newdict)
    
        # 파일 저장 형태
        rows = {"운송장번호": numbers,
                "상품명": titles, 
                "주소": addresss,
                "상세내역": tds_list
                }

        # JSON 파일 저장
        with open(os.path.join(BASE_DIR, 'result.json'), 'a', encoding='utf-8-sig') as json_file:
            json.dump(rows, json_file, ensure_ascii=False, indent=4)
        print(numbers + " 배송정보가 성공적으로 저장되었습니다.")
        break

    except IndexError:
        print("송장번호가 잘못되었습니다. 다시 입력해주세요.")
    
        

