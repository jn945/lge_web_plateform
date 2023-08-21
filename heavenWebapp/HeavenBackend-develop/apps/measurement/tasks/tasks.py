from datetime import datetime, timedelta

from django.core.mail import EmailMessage

from ..models import MeasurementRequest


def update_request_status(request_id):
    # Request 가져오기
    request = MeasurementRequest.objects.get(id=request_id)

    # Request 상태 및 실행 시간 변경
    if request.status == "Confirmed":
        request.executed_time = datetime.now()
        request.status = "In Progress"
        request.save()

    elif request.status == "In Progress":
        # 이메일 보내기
        pass


def send_email(text):
    email = EmailMessage(
        "Title입니다",  # 이메일 제목
        "Content입니다",  # 내용
        to=["mksong@intellicode.co.kr"],  # 받는 이메일
    )
    email.send()
