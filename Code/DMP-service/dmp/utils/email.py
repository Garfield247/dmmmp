#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020/5/6
# @Author  : SHTD 

from flask import current_app, render_template
from flask_mail import Message
from dmp.extensions import mail
from dmp.extensions import celery


class EmailBody():

    @staticmethod
    def email_body(name, url):

        text_body = '''
            Dear {},
            To confirm your account please click on the following link: {}
            Sincerely,
            Note: replies to this email address are not monitored.
            '''.format(name, url)
        html_body = '''
            <p>Dear {0},</p>
            <p>To confirm your account please <a href="{1}">click here</a>.</p>
            <p>Alternatively, you can paste the following link in your browser's address bar:</p>
            <p><b>{1}</b></p>
            <p>Sincerely,</p>
            <p><small>Note: replies to this email address are not monitored.</small></p>
            '''.format(name, url)
        return text_body, html_body

    @staticmethod
    def resend_email(email, url):
        text_body = '''
            Dear {} email user,
            Click here to reactivate your email: {}
            '''.format(email, url)
        html_body = '''
            <p>Dear {0} email user,</p>
            <p>Click here to reactivate your email <a href="{1}">click here</a>.</p>
            '''.format(email, url)
        return  text_body, html_body



    @staticmethod
    def change_pwd(email, url):

        text_body = '''
            Dear {} email user,
            Click here to reset your new password: {}
            '''.format(email, url)
        html_body = '''
            <p>Dear {0} email user,</p>
            <p>Click here to reset your new password, please <a href="{1}">click here</a>.</p>
            '''.format(email, url)
        return text_body, html_body


@celery.task
def send_mail(r, subject, text_body, html_body, **kwargs):
    app = current_app._get_current_object()
    msg = Message(
        subject=subject,
        recipients=[r],
        sender=app.config['MAIL_USERNAME']
    )
    msg.html = html_body
    msg.text = text_body
    mail.send(msg)