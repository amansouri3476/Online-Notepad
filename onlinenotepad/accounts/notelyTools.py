from django.core.mail import send_mail
from time import sleep


def email_reminder(email, first_name, note_name, time_left):
    while time_left > 0:
        sleep(5)
        time_left = time_left - 5
    send_mail("NoteLY Reminder!!!", first_name + ", Did you forget about " + note_name + "?", "sut25719test@gmail.com",
              [email])
