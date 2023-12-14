from django.shortcuts import render, redirect, get_object_or_404
from .models import Member, University
from .models import Study
from .models import StudyBoard
from .models import StudyComment
from django.utils import timezone
from django.http import HttpResponseRedirect
from .forms import StudyForm, StudyBoardForm
from .models import Study, StudyBoard, StudyMember, StudyCafeRoomReservation
from .models import StudyCafe, StudyCafeRoom
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime

# 기존의 login_register 함수 내부의 로그인 처리 부분을 별도의 함수로 분리
def login_member(request, email, password):
    member = Member.objects.get(email=email)
    if member.password == password:
        # Django의 login 함수를 사용하지 않고, 세션을 직접 관리
        request.session['member_id'] = member.pk
        # 필요한 경우 여기에 추가 세션 관리 로직을 추가
        return True
    return False

def is_member_logged_in(request):
    return 'member_id' in request.session

def login_register(request):
    error_message = None

    if request.method == 'POST':
        if 'register_submit' in request.POST:
            # 회원가입 처리
            name = request.POST.get('name')
            university_code = request.POST.get('university_code')
            email = request.POST.get('email')
            password = request.POST.get('password')
            phone_number = request.POST.get('phone_number')

            # 대학 코드 유효성 검사 및 처리
            try:
                university = University.objects.get(pk=university_code)
            except University.DoesNotExist:
                error_message = "유효하지 않은 대학 코드입니다."
                return render(request, 'login_register.html', {'error_message': error_message})

            # 회원 객체 생성 및 저장
            member = Member(name=name, university_code=university, email=email, password=password, phone_number=phone_number)
            member.save()

            return redirect('study_board')

        elif 'login_submit' in request.POST:
            email = request.POST.get('email')
            password = request.POST.get('password')
            try:
                member = Member.objects.get(email=email)
                if member.password == password:
                    request.session['member_id'] = member.pk
                    return redirect('study_board')
                else:
                    error_message = "비밀번호가 틀렸습니다."
            except Member.DoesNotExist:
                error_message = "존재하지 않는 계정입니다."

    return render(request, 'login_register.html', {'error_message': error_message})

def study_board(request):
    study_boards = StudyBoard.objects.all().order_by('-posting_date').select_related('study')
    return render(request, 'study_board.html', {'study_boards': study_boards})


def study_create(request):
    if request.method == 'POST':
        study_board_form = StudyBoardForm(request.POST)
        study_form = StudyForm(request.POST)

        if study_board_form.is_valid() and study_form.is_valid():
            # Member Verification
            member_id = request.session.get('member_id')
            if not member_id:
                return redirect('login_register')

            member = Member.objects.get(pk=member_id)

            # Create and save the Study object first
            study = study_form.save()

            # Create StudyBoard, link it with Study and Member, and save
            study_board = study_board_form.save(commit=False)
            study_board.study = study
            study_board.member = member
            study_board.save()

            # Create a StudyMember object for the member who created the study
            # and assign a role (e.g., 'Leader', 'Member', etc.)
            study_member = StudyMember(study=study, member=member, role='회장')
            study_member.save()

            return redirect('study_board')
    else:
        study_form = StudyForm()
        study_board_form = StudyBoardForm()

    return render(request, 'study_create.html', {'study_form': study_form, 'study_board_form': study_board_form})


def study_detail(request, study_board_post_id):
    study_board = get_object_or_404(StudyBoard, pk=study_board_post_id)
    comments = StudyComment.objects.filter(study_board_post=study_board)

    if request.method == 'POST':
        if is_member_logged_in(request):
            member_id = request.session.get('member_id')  # 세션에서 member_id 가져오기
            content = request.POST.get('content')
            member = Member.objects.get(pk=member_id)
            StudyComment.objects.create(
                study_board_post=study_board,
                member=member,
                content=content,
                comment_date=timezone.now()
            )
            return HttpResponseRedirect(request.path_info)
        else:
            return redirect('login_register')

    return render(request, 'study_detail.html', {'study_board': study_board, 'comments': comments})

@require_POST
def join_study(request, study_id):
    if 'member_id' in request.session:
        member_id = request.session['member_id']
        member = get_object_or_404(Member, pk=member_id)
        study = get_object_or_404(Study, pk=study_id)

        # 이미 가입한 경우 체크
        if StudyMember.objects.filter(study=study, member=member).exists():
            return JsonResponse({'status': 'already_member'})

        # 새로운 StudyMember 객체 생성
        StudyMember.objects.create(study=study, member=member, role='회원')

        # Study의 current_members 필드 업데이트
        study.current_members += 1
        study.save()

        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error'}, status=403)


def study_list(request):
    if 'member_id' in request.session:
        member_id = request.session['member_id']
        studies = Study.objects.filter(studymember__member_id=member_id)
        return render(request, 'study_list.html', {'studies': studies})
    else:
        # 사용자가 로그인하지 않았을 경우
        return redirect('login_register')
    
def study_home(request, study_id):
    study = get_object_or_404(Study, pk=study_id)
    return render(request, 'study_home.html', {'study': study})

def study_home(request, study_id):
    study = get_object_or_404(Study, pk=study_id)
    reservations = StudyCafeRoomReservation.objects.filter(study=study)
    return render(request, 'study_home.html', {'study': study, 'reservations': reservations})

def study_cafe_reservation(request):
    cafes = StudyCafe.objects.prefetch_related('rooms').all()
    return render(request, 'study_cafe_reservation.html', {'cafes': cafes})

@require_POST
@csrf_exempt
def settle_reservation(request, reservation_id):
    try:
        data = json.loads(request.body)
        reservation = StudyCafeRoomReservation.objects.get(pk=reservation_id)
        member_count = data.get('memberCount', 1)
        individual_share = reservation.total_amount / member_count
        reservation.total_amount -= individual_share
        reservation.save()
        return JsonResponse({
            'status': 'success', 
            'new_amount': reservation.total_amount,
            'reservation_date': reservation.billing_date.strftime('%Y-%m-%d')
        })
    except StudyCafeRoomReservation.DoesNotExist:
        return JsonResponse({'status': 'error'}, status=404)
    
@require_POST
@csrf_exempt
def create_reservation(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            study_id = data['studyId']
            room_id = data['roomId']
            cafe_id = data['cafeId']
            billing_date = data['billingDate']
            hourly_price = data['hourlyPrice']

            study = Study.objects.get(pk=study_id)
            room = StudyCafeRoom.objects.get(study_cafe_room_id=room_id, cafe_id=cafe_id)

            total_amount = hourly_price  # Assuming hourly_price is already in the correct format

            reservation = StudyCafeRoomReservation.objects.create(
                study=study,
                study_cafe_room=room,
                total_amount=total_amount,
                billing_date=billing_date
            )

            return JsonResponse({'status': 'success', 'message': '예약이 완료되었습니다.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


def my_view(request, study_id):
    # 스터디 객체를 가져오는 로직
    study = get_object_or_404(Study, pk=study_id)
    
    # 컨텍스트에 스터디 ID 추가
    context = {
        'study': study,
        'current_study_id': study.id
    }
    return render(request, 'my_template.html', context)

def study_home(request, study_id):
    study = get_object_or_404(Study, pk=study_id)
    reservations = StudyCafeRoomReservation.objects.filter(study=study)
    return render(request, 'study_home.html', {'study': study, 'reservations': reservations})