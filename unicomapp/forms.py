from django import forms
from .models import Member, StudyBoard, Member, Study, StudyMember

class MemberCreationForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['name', 'university_code', 'email', 'password', 'phone_number']

class StudyForm(forms.ModelForm):
    class Meta:
        model = Study
        fields = ['study_name', 'days', 'time_start', 'duration', 'frequency', 'start_date', 'retention_period', 'study_description', 'bank_account', 'max_participant']
        labels = {
            'study_name': '스터디 이름',
            'days': '스터디 요일',
            'time_start': '스터디 시작 시간',
            'duration': '스터디 시간',
            'frequency': '스터디 주기',
            'start_date': '시작 날짜',
            'retention_period': '스터디 기간',
            'max_participant': '최대 스터디 인원',
            'study_description': '스터디 설명',
            'bank_account': '정산 계좌',
        }

class StudyBoardForm(forms.ModelForm):
    class Meta:
        model = StudyBoard
        fields = ['title', 'content']
        labels = {
            'title': '게시글 제목',
            'content': '게시글 내용',
        }