# 대학생 스터디-동아리 커뮤니티

## 현재 상황 : 스터디쪽 기능만 구현함.

## 공지

사실 스터디 쪽만 구현하고 내도 될 것 같더라구요, 제가 시간이 좀 부족하기도 하고..

그래서 스터디만 구현하고 영상찍어서 내면 될 것 같아요. 한 번 확인해보세요

---

### 여기서 추가로 구현 해주시면 좋겠는 기능:

- 스터디에서 “예약하기” 버튼을 추가로 넣었는데 미구현이에요 이 부분 해결해주시면 좋겠어요.
- 동아리가 스터디 구조보다 쉬우니까 스터디 코드 구조 보고 비슷하게 짜서 동아리 모집 게시판 정도 구현하면 좋을 듯 해요.

→ 구현 못해도 되니까 시도는 다들 해봐주세요!

---

## 실행 방법

1. **Python 설치**

https://www.python.org/downloads/

1. ****Django 설치****

`pip install django`

1. **git 프로젝트 clone**

`git clone https://github.com/LikewiseU/db_6.git`

1. **프로젝트 설정**

unicom >settings.py에 

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join("C:\\Users\\user\\Downloads", 'test1.db'),
    }
}
```

경로를 알맞게 설정합니다.

### DB 관련 내용 업데이트 프로젝트에 적용하는 법

프로젝트 디렉토리에서 `python [manage.py](http://manage.py/) makemigrations` (models.py, [views.py](http://views.py) 수정 시)

### 내용 수정 프로젝트에 업데이트하는 법

프로젝트 디렉토리에서 `python [manage.py](http://manage.py/) migrate` (매 실행 수정 후 실행 시 한번씩 하는게 나음)

### 서버 실행하는 법

프로젝트 디렉토리에서 `python [manage.py](http://manage.py/) runserver` 실행 후

웹 창 열고 → **`http://localhost:8000/register/` 주소 입력**

---

p.s. 안의 구현된 내용이랑 방식, 구조를 한 번 보시고, Django가 어떤건지, HTML 어떻게 작성하는지, DB랑 연동하는 법 등등 독학도 하면서, 모르는 부분 찾아가면서 감을 잡으셨으면 좋겠어요. 

한번 수정하려고 노력해보시면 공부 많이 될 겁니다!

++ 챗GPT 사용하면서 공부하면 더 편하심!
