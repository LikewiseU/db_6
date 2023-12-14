from django.contrib.auth.backends import BaseBackend
from .models import Member

class MemberAuthenticationBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None):
        try:
            member = Member.objects.get(email=email)
            if member.password == password:
                # last_login 업데이트 로직 제거
                return member
        except Member.DoesNotExist:
            return None

    def get_user(self, member_id):
        try:
            return Member.objects.get(pk=member_id)
        except Member.DoesNotExist:
            return None
