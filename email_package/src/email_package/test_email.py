from email_package.validate import validate_email_address
from email_package.my_email import MyEmail
from dotenv import load_dotenv
import os
from email_package.error_codes import ErrorCodes as Ec

def main():

    load_dotenv()

    password = os.environ["SMTP_PASSWORD"]
    username = os.environ["SMTP_USERNAME"]
    smtp_server = os.environ["SMTP_SERVER"]
    port = int(os.environ["SMTP_PORT"])
    sender_email = os.environ["EMAIL_FROM"]

    email = MyEmail(password,username,smtp_server,port,sender_email)
    distro = {"To": ["rlynch3456@yahoo.com"], "Bcc": ["rich.lynch3456@comcast.net"]}
    error = email.create_message("greetings", "rlynch3456@yahoo.com", distro, "<H1>foobar!</H1>")
    if error != Ec.SUCCESS:
        print(error.name)
    else:
        ret, ret_string = email.send_message()
        print(f'Return Code: {ret}  {ret_string}')

    # Test cases
    print(validate_email_address(""))   # Valid
    print(validate_email_address("bad-format.com"))       # Invalid (Missing @ sign)
    print(validate_email_address("user@fake-domain-xyz.com")) # Invalid (Domain doesn't exist)
    print(validate_email_address("user@rjlsoftwareus.com")) # Invalid (Domain doesn't exist)



if __name__ == "__main__":
    main()