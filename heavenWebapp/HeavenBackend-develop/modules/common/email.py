# from apps.HWCheck.models import HWCheck
# from django.core.mail import EmailMessage
# from django.db.models.signals import post_delete, post_save
# from django.dispatch import receiver


# def send_email(title, content, to):
#     email = EmailMessage(
#         title,  # 이메일 제목
#         content,  # 내용
#         to=to,  # 받는 이메일
#     )
#     email.send()


# def apply_emailing(sender):
#     post_save.connect(send_email_on_model_change, sender=sender)
#     post_delete.connect(send_email_on_model_delete, sender=sender)


# @receiver(post_save, sender=HWCheck)
# def send_email_on_model_change(sender, instance, created, **kwargs):
#     if created:
#         # 새로운 인스턴스가 생성되었을 때
#         email_title = "New PlanSeries Created"
#         email_content = f"New PlanSeries with ID {instance.id} has been created."
#         recipients = ["mksong@intellicode.co.kr"]  # 이메일 수신자 지정
#     else:
#         # 인스턴스가 업데이트되었을 때
#         email_title = "PlanSeries Updated"
#         email_content = f"PlanSeries with ID {instance.id} has been updated."
#         recipients = ["mksong@intellicode.co.kr"]  # 이메일 수신자 지정

#     send_email(email_title, email_content, recipients)


# @receiver(post_delete, sender=HWCheck)
# def send_email_on_model_delete(sender, instance, **kwargs):
#     email_title = "PlanSeries Deleted"
#     email_content = f"PlanSeries with ID {instance.id} has been deleted."
#     recipients = ["mksong@intellicode.co.kr"]  # 이메일 수신자 지정

#     send_email(email_title, email_content, recipients)
