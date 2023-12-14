from django.db import models
from django.core.validators import RegexValidator

class University(models.Model):
    university_code = models.AutoField(primary_key=True)
    university_name = models.CharField(max_length=100)

    class Meta:
        db_table = 'university'

class Member(models.Model):
    member_id = models.AutoField(primary_key=True)
    university_code = models.ForeignKey(University, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)

    class Meta:
        db_table = 'member'
        

class Study(models.Model):
    study_id = models.AutoField(primary_key=True)
    study_name = models.CharField(max_length=100)
    days = models.CharField(max_length=50, null=True)
    time_start = models.IntegerField()  
    duration = models.CharField(max_length=50, null=True)
    frequency = models.CharField(max_length=50)
    start_date = models.CharField(max_length=50, null=True)
    retention_period = models.CharField(max_length=100, null=True)
    current_members = models.IntegerField(default=1)
    study_description = models.CharField(max_length=200, null=True)
    bank_account_validator = RegexValidator(regex=r'^\d{6}$', message="Bank account must be 6 digits.")
    bank_account = models.CharField(
        max_length=6,
        validators=[bank_account_validator],
        default = 0
    )
    max_participant = models.IntegerField()

    class Meta:
        db_table = 'study' 
        
class StudyBoard(models.Model):
    study_board_post_id = models.AutoField(primary_key=True)
    study = models.ForeignKey(Study, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    posting_date = models.DateField(auto_now_add=True) 

    class Meta:
        db_table = 'study_board'
        
class StudyComment(models.Model):
    study_board_comment_id = models.AutoField(primary_key=True)
    study_board_post = models.ForeignKey(StudyBoard, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    comment_date = models.DateField(auto_now_add=True)
    content = models.TextField()

    class Meta:
        db_table = 'study_comment'
        
class StudyMember(models.Model):
    study_member_id = models.AutoField(primary_key=True)
    study = models.ForeignKey('Study', on_delete=models.CASCADE)
    member = models.ForeignKey('Member', on_delete=models.CASCADE)
    role = models.CharField(max_length=50)

    class Meta:
        db_table = 'study_member'

class StudyCafe(models.Model):
    cafe_id = models.AutoField(primary_key=True)
    cafe_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    link = models.URLField()

    class Meta:
        db_table = 'study_cafe'

class StudyCafeRoom(models.Model):
    study_cafe_room_id = models.AutoField(primary_key=True)
    room_id = models.IntegerField()
    cafe = models.ForeignKey(StudyCafe, on_delete=models.CASCADE, related_name='rooms')
    room_name = models.CharField(max_length=100)
    hourly_price = models.DecimalField(max_digits=10, decimal_places=2)
    room_capacity = models.IntegerField()

    class Meta:
        db_table = 'study_cafe_room'
        
class StudyCafeRoomReservation(models.Model):
    reservation_id = models.AutoField(primary_key=True)
    study = models.ForeignKey('Study', on_delete=models.CASCADE)
    study_cafe_room = models.ForeignKey(StudyCafeRoom, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    billing_date = models.DateField()

    class Meta:
        db_table = 'study_cafe_room_reservation'
