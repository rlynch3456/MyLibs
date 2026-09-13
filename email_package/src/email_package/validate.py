from email_validator import validate_email, EmailNotValidError, EmailSyntaxError, EmailUndeliverableError
from email_package.error_codes import ErrorCode as Ec, ErrorCode

__all__ = ["validate_email_address"]

def validate_email_address(email_address: str) -> tuple[ErrorCode, str]:
    """
    validate_email_address
    :param email_address:
    :return: (error, error_string)

    Will validate the email address.

    error return:
    Ec.SUCCESS if success
    Ec.BAD_EMAIL_ADDRESS

    error string:
    Will describe the error such as missing @, invalid domain.
    """

    try:
        # validate_email performs syntax checks and a DNS MX record lookup by default
        email_info = validate_email(email_address)

        # Always use the normalized version returned by the library
        normalized_email = email_info.normalized
        #print(f"Success! Normalized email: {normalized_email}"                               )
        return Ec.SUCCESS, normalized_email

    except EmailSyntaxError as e:
        # Raised if the structure is wrong (e.g., missing '@', spaces, invalid characters)
        return Ec.BAD_EMAIL_ADDRESS, f"Syntax Error: {email_address} {e}"

    except EmailUndeliverableError as e:
        # Raised if the domain doesn't exist or has no MX records
        return Ec.BAD_EMAIL_ADDRESS, f"Deliverability Error: {email_address} {e}"

    except EmailNotValidError as e:
        # Catch-all for any other validation errors provided by the library
        return Ec.BAD_EMAIL_ADDRESS, f"Validation Error: {email_address} {e}"


