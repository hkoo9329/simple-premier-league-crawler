# 파이썬으로 만든 프리미어리그 경기 일정 및 결과 api

프리미어리그 경기 결과를 알려주는 rest api가 있으면 좋지 않을까? 해서 만들어본 토이 프로젝트 입니다. 
웹 크롤링을 통해서 프리미어리그의 정보를 가져오고, DB에 저장 및 업데이트 합니다. 그리고 그 데이터를 rest api를 통해서 json의 형태로 전달합니다.
현재 aws ec2서버를 통해서 배포하고 있습니다.(주소 : http://ec2-15-165-113-72.ap-northeast-2.compute.amazonaws.com/)

## API 사용법
  - (api 주소)/matchs/all
    - 19/20 시즌 프리미어리그 전체 경기 정보를 반환합니다.
  - /matchs/all/{team}
    - 19/20 시즌 해당 팀의 모든 경기 정보를 반환합니다.
    - team라는 파라미터 값을 한글로 해야합니다.
      > 역시 url은 영어로 해야하나, 한글로 하는게 사용자 입장에서는 편하지 않을까? 하는 생각에서 일단은 한글로 하기로 결정했습니다. 사용하다가 문제가 발생하거나 생각이 바뀌면 영어로 변경할 것입니다.
   - /matchs/recency
    - 19/20 시즌 최근 8경기 ( 현재 날짜 이전 3경기 이후 5경기) 정보를 반환합니다.
   - /matchs/recency/{team}
    - 19/29 시즌 해당 팀의 최근 8경기 ( 현재 날짜 이전 3경기 이후 5경기) 정보를 반환합니다.
    - /matchs/all/{team} 에서와 같이 한글을 사용합니다.

사용법의 위 사이트에서 Swagger를 통해서도 확인할 수 있습니다.

## 서버 및 사용 모듈 환경
- Ubuntu Server 18.04
- Python 3.6
- Flask version 1.1.1
- BeautifulSoup4 version 4.8.2
- Selenium version 3.141.0
- aws rds mariaDB version 10.2.21
- chromium browser version 79.0.3945.79

