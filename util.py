import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class EmailUser:
    """
    Email User class
    """

    def __init__(self, login, password):
        self.login = login
        self.password = password


class WorkOrder:
    """
    Work Order class
    """

    def __init__(self, name, email, phone_number,
        work_type, subject, page_count,
        work_topic, work_term, add_info):
        self.name = name
        self.email = email
        self.phone_number = phone_number
        self.work_type = work_type
        self.subject = subject
        self.page_count = page_count
        self.work_topic = work_topic
        self.work_term = work_term
        self.add_info = add_info


def generate_order_text(order):
    """
    Generate order text
    """
    text = 'Имя: {!s}\n'.format(order.name)
    text += 'E-mail: {!s}\n'.format(order.email)
    text += 'Номер телефона: {!s}\n'.format(order.phone_number)
    text += 'Вид работы: {!s}\n'.format(order.work_type)
    text += 'Предмет: {!s}\n'.format(order.subject)
    text += 'Кол-во страниц: {!s}\n'.format(order.page_count)
    text += 'Тема работы: {!s}\n'.format(order.work_topic)
    text += 'Срок выполнения: {!s}\n'.format(order.work_term)
    text += 'Дополнительная информация: {!s}\n'.format(order.add_info)
    return text


def send_email(email_user, receiver, subject, text=''):
    """
    Send email message
    """
    msg = MIMEMultipart()
    msg['From'] = email_user.login
    msg['To'] = receiver
    msg['Subject'] = subject
    msg.attach(MIMEText(text, 'plain'))

    server = smtplib.SMTP('smtp.mail.ru', 587)
    server.starttls()
    server.login(email_user.login, email_user.password)
    text = msg.as_string()
    server.sendmail(email_user.login, receiver, text)
    server.quit()
