#coding: utf-8
import urllib
import urllib2

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse

from common import LOG


def send_register_code_by_email(email, code):
    subject = u'注册校验码-唯杰VR+'
    text_content = u'您好：\n您正在注册唯杰VR+！您的校验码是【%(code)s】。\n15分钟内有效，请勿泄露。\n\n敬上，\n唯杰VR+'
    html_content = u'<p>您好：</p><p>您正在注册唯杰VR+！您的校验码是&nbsp;<strong style="color:green;">%(code)s</strong></p><p>该校验码15分钟内有效，请勿泄露。</p><br><p>敬上，</p><p>唯杰VR+</p>'
    data = {'code': code}
    msg = EmailMultiAlternatives(subject, text_content % data, u'唯杰VR+<%s>' % settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content % data, 'text/html')
    msg.send()


def send_register_code_by_mobile(mobile, code):
    # content = u'您的注册验证码是%s。15分钟内有效，请勿泄露。' % code
    content = u'【唯杰VR+】欢迎注册唯杰VR+，您的校验码是%s。（请勿向任何人提供校验码）' % code
    send_sms(mobile, content)

def send_edit_code_by_email(email, code):
    subject = u'账户更改校验码-唯杰VR+'
    text_content = u'您好：\n您正在修改唯杰VR+账户的信息，您的校验码是【%(code)s】。\n15分钟内有效，请勿泄露。\n\n敬上，\n唯杰VR+'
    html_content = u'<p>您好：</p><p>您正在修改唯杰VR+账户的信息，您的校验码是&nbsp;<strong style="color:green;">%(code)s</strong></p><p>该校验码15分钟内有效，请勿泄露。</p><br><p>敬上，</p><p>唯杰VR+</p>'
    data = {'code': code}
    msg = EmailMultiAlternatives(subject, text_content % data, u'唯杰VR+<%s>' % settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content % data, 'text/html')
    msg.send()


def send_edit_code_by_mobile(mobile, code):
    content = u'【唯杰VR+】您正在修改唯杰VR+的账户信息，校验码是%s。（请勿向任何人提供校验码）' % code
    send_sms(mobile, content)


def send_sms(mobile, content):
    if not mobile:
        LOG.debug('ERROR for mobile %s', mobile)
        return

    req = urllib2.Request(settings.SMS_ZZ_URL)

    data = {'UserName': settings.SMS_ZZ_ACCOUNT,
            'UserPass': settings.SMS_ZZ_KEY,
            'Mobile': mobile,
            'Content': content.encode('utf-8'),
            'Subid': '01'
            }
    req.add_data(urllib.urlencode(data))

    res = urllib2.urlopen(req)
    result = res.read()
    res.close()

    if not result.startswith('00') and not result.startswith('03'):
        LOG.debug('ERROR for sms %s', result)
        return True


def get_erp_email_connection():
    from django.core.mail import get_connection
    return get_connection(username=settings.ERP_EMAIL_ACCOUNT, password=settings.ERP_EMAIL_PASSWORD, fail_silently=True)