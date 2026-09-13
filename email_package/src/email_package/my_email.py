from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from email_package.validate import validate_email_address
from email_package.error_codes import ErrorCodes as Ec

class MyEmail:
    def __init__(self, password, username, server, port, sender_email):
        self.distro = {}
        self.msg = None

        self._password = password
        self._username = username
        self._smtp_server = server
        self._port = port
        self._sender_email = sender_email

    def create_message(self, subject, sender, distro, content):

        self.distro = distro
        self.msg = MIMEMultipart("alternative")
        self.msg["Subject"] = subject
        self.msg["From"] = sender
        if "To" in distro:
            self.msg["To"] = ", ".join(distro.get("To"))
        else:
            return Ec.MISSING_TO_RECIPIENT

        self.msg["Cc"] = ", ".join(distro.get("Cc", []))
        # Do not add Bcc to the header.  The addresses are in the recipient list though.
        #msg["Bcc"] = ", ".join(distro.get("Bcc", []))

        html_part = MIMEText(content, "html")
        self.msg.attach(html_part)
        return Ec.SUCCESS

    def send_message(self):

        debuglevel = True
        recipients = []
        if self.msg is None:
            return Ec.NO_MESSAGE_FOUND, "create_message method needs to be called first"

        to = self.distro.get("To", [])
        cc = self.distro.get("Cc", [])
        bcc = self.distro.get("Bcc", [])

        try:
            recipients = to
            if len(cc) >0:
                recipients.extend(cc)
            if len(bcc) >0:
                recipients.extend(bcc)

            error_list = []
            for address in recipients:
                error, string = validate_email_address(address)
                if error != 0:
                    error_list.append(string)

            if len(error_list) > 0:
                for error in error_list:
                    print(error)
                return Ec.BAD_EMAIL_ADDRESS, error_list

            with smtplib.SMTP(self._smtp_server, self._port) as server:
                server.set_debuglevel(debuglevel)
                server.starttls()
                server.login(self._username, self._password)

                server.sendmail(
                    self._sender_email,
                    recipients,
                    self.msg.as_string()
                )



        except smtplib.SMTPException as e:
            print(f"SMTP error occurred: {e}")

        return Ec.SUCCESS, recipients