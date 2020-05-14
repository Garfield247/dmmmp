from dmp.utils.email import EmailBody, send_mail


class ValidationEmail():

    def __init__(self):
        self.confirm_url = 'http://localhost:7789/user/activate/'
        # self.change_pwd_url = 'http://localhost:7789/user/changepwd/'
        self.gettoken_url = 'http://localhost:7789/user/gettoken/'

    def activate_email(self, user, email):
        token = user.generate_activate_token().decode('utf-8')
        confirm_url = self.confirm_url + token
        text_body, html_body = EmailBody.email_body(user.dmp_username, confirm_url)
        send_mail.apply_async(args=[email, '账户激活', text_body, html_body])

    def reactivate_email(self, user, email):
        token = user.generate_activate_token().decode('utf-8')
        confirm_url = self.confirm_url + token
        text_body, html_body = EmailBody.resend_email(user.email, confirm_url)
        send_mail.apply_async(args=[email, '重新激活账户', text_body, html_body])

    def change_pwd(self, user, email):
        token = user.generate_activate_token().decode('utf-8')
        # change_pwd_url = self.change_pwd_url + token
        gettoken_url = self.gettoken_url + token
        text_body, html_body = EmailBody.change_pwd(user.email, gettoken_url)
        send_mail.apply_async(args=[email, '重置密码', text_body, html_body])

