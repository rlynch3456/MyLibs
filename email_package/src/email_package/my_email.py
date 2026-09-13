from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from email_package.validate import validate_email_address
from email_package.error_codes import ErrorCode as Ec, ErrorCode

__all__ = ["MyEmail"]

class MyEmail:
    """
    MyEmail class

    Initialize the email system with username and password, etc

    :param username: email username
    :param password: email password
    :param sender_email: sender email address
    :param server: smtp server
    :param port: smtp port
    """
    def __init__(self, username, password, sender_email, server, port, ):
        self.distro = {}
        self.msg = None

        self._password = password
        self._username = username
        self._smtp_server = server
        self._port = port
        self._sender_email = sender_email

    def create_message(self, subject: str, sender: str, distro:dict[str, list[str]], content: str) -> ErrorCode:
        """
        create_message
        :param subject: subject line as a string
        :param sender:  sender email address
        :param distro:  recipients as a dictionary with "To", "Cc" and "Bcc" keys
        :param content: email content as a string, typically in HTML format
        :return: ErrorCode: SUCCESS or MISSING_TO_RECIPIENT
            (if disto does not at least contain "To").
        """
        self.distro = distro
        self.msg = MIMEMultipart("alternative")
        self.msg["Subject"] = subject
        self.msg["From"] = sender
        if "To" in distro:
            self.msg["To"] = ", ".join(distro["To"])
        else:
            return Ec.MISSING_TO_RECIPIENT

        self.msg["Cc"] = ", ".join(distro.get("Cc", []))
        # Do not add Bcc to the header.  The addresses are in the recipient list though.
        #msg["Bcc"] = ", ".join(distro.get("Bcc", []))

        html_part = MIMEText(content, "html")
        self.msg.attach(html_part)
        return Ec.SUCCESS

    def send_message(self) -> tuple[ErrorCode, list]:
        """
        send_message
        :return: Ec.SUCCESS, Ec.BAD_EMAIL_ADDRESS, or Ec.SEND_ERROR
        and list of either errors or recipient list if successful
        """
        debuglevel = True
        #recipients = []
        if self.msg is None:
            # Yes, it is odd that the string will be in a list, but the function return type is a
            # tuple [ErrorCode, list] where the list is typically a list of
            # recipients or errors.  This is just to keep the typedef happy.
            return Ec.NO_MESSAGE_FOUND, ["create_message method needs to be called first"]

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
                if error != Ec.SUCCESS:
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
            return Ec.MESSAGE_SEND_ERROR, [f"SMTP error occurred: {e}"]

        return Ec.SUCCESS, recipients