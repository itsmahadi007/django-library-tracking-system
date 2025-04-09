from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from .models import Loan


@shared_task
def send_loan_notification(loan_id):
    try:
        loan = Loan.objects.get(id=loan_id)
        member_email = loan.member.user.email
        book_title = loan.book.title
        send_mail(
            subject='Book Loaned Successfully',
            message=f'Hello {loan.member.user.username},\n\nYou have successfully loaned "{book_title}".\nPlease return it by the due date.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[member_email],
            fail_silently=False,
        )
    except Loan.DoesNotExist:
        pass


@shared_task(name="check_overdue_loans")
def check_overdue_loans():
    loan_list = Loan.objects.filter(
        is_returned=False,
        due_date__lt=timezone.now().date()
    )

    for loan in loan_list:
        member_email = loan.member.user.email
        book_title = loan.book.title
        send_mail(
            subject='Notification for Book Loaned over due',
            message=f'Hello {loan.member.user.username},\n\nYour book titled: {book_title} loaned is overdue. Please return it as soon as possible.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[member_email],
            fail_silently=False,
        )
