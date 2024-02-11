# -*- coding: utf-8 -*-
"""
Created on Sat Feb 10 22:29:16 2024

@author: USER
"""

import requests
import sqlite3
from bs4 import BeautifulSoup
import datetime

#def scrape_university_reviews(university_name, admission_season):
def scrape_university_reviews(university_name):
    base_url = f"https://cafe.naver.com/suhui"
    response = requests.get(base_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # 스크래핑한 데이터를 데이터베이스에 저장하고 Postman에 전송
        #save_to_database_and_postman(university_name, admission_season, soup)
        save_to_database_and_postman(university_name, soup)
    else:
        print(f"Error: {response.status_code}")

#def save_to_database_and_postman(university_name, admission_season, soup):
def save_to_database_and_postman(university_name, soup):
    # 데이터베이스 연결
    conn = sqlite3.connect('university_reviews.db')
    cursor = conn.cursor()

    # 테이블 생성
    cursor.execute('''CREATE TABLE IF NOT EXISTS university_reviews (university_name TEXT, review_title TEXT, review_content TEXT, date TEXT)''')
                      #(university_name TEXT, admission_season TEXT, review_title TEXT, review_content TEXT, date TEXT)''')

    # 스크래핑한 제목과 내용 가져오기
    titles = soup.find_all('h2', class_='title')
    contents = soup.find_all('div', class_='content')
    dates = soup.find_all('span', class_='date')

    # 데이터베이스에 저장할 데이터 구성
    data_to_save = []
    for title, content, date in zip(titles, contents, dates):
        title_text = title.get_text(strip=True)
        content_text = content.get_text(strip=True)
        date_str = date.get_text(strip=True)
        #data_to_save.append((university_name, admission_season, title_text, content_text, date_str))
        data_to_save.append((university_name, title_text, content_text, date_str))

    # 데이터베이스에 데이터 저장
    #cursor.executemany("INSERT INTO university_reviews VALUES (?, ?, ?, ?, ?)", data_to_save)
    cursor.executemany("INSERT INTO university_reviews VALUES (?, ?, ?, ?)", data_to_save)
    conn.commit()

    # Postman에 데이터 전송
    for data in data_to_save:
        payload = {
            "university_name": data[0],
            #"admission_season": data[1],
            "review_title": data[1],
            "review_content": data[2],
            "date": data[3]
        }
        post_data_to_postman(payload)

    # 연결 종료
    conn.close()

def post_data_to_postman(payload):
    # Postman API 엔드포인트 URL
    postman_url = "https://api.postman.com/collections/32847908-2ec81940-bb48-47c7-8e05-6941b7f1a715?"

    # Postman API 키
    postman_api_key = "PMAT-01HP9MD8TF2FH7QAST06SEFBXP"

    # API 요청 헤더 설정
    headers = {
        "Content-Type": "application/json",
        "X-Api-Key": postman_api_key
    }

    try:
        # POST 요청 보내기
        response = requests.post(postman_url, headers=headers, json=payload)
        
        # 응답 확인
        if response.status_code == 200:
            print("Data saved to Postman successfully!")
        else:
            print(f"Failed to save data to Postman. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred while sending data to Postman: {e}")

def main():
    university_name = input("대학교 이름을 입력하세요: ")
    #admission_season = input("입학 시즌을 입력하세요 (수험시즌, 수시입시, 정시입시, 입학시즌): ")
    
    # 대학교 평판 스크래핑
    scrape_university_reviews(university_name)# admission_season)

if __name__ == "__main__":
    main()
