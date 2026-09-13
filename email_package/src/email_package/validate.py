from email_validator import validate_email, EmailNotValidError, EmailSyntaxError, EmailUndeliverableError

def validate_email_address(email_address: str) -> tuple[int, str]:
    """
    validate_email_address
    :param email_address:
    :return: (error, error_string)

    Will validate the email address.

    error return:
    0 if success
    -1 if error

    error string:
    Will describe the error such as missing @, invalid domain.
    """

    try:
        # validate_email performs syntax checks and a DNS MX record lookup by default
        email_info = validate_email(email_address)

        # Always use the normalized version returned by the library
        normalized_email = email_info.normalized
        #print(f"Success! Normalized email: {normalized_email}"                               )
        return 0, normalized_email

    except EmailSyntaxError as e:
        # Raised if the structure is wrong (e.g., missing '@', spaces, invalid characters)
        return -1, f"Syntax Error: {email_address} {e}"

    except EmailUndeliverableError as e:
        # Raised if the domain doesn't exist or has no MX records
        return -1, f"Deliverability Error: {email_address} {e}"

    except EmailNotValidError as e:
        # Catch-all for any other validation errors provided by the library
        return -1, f"Validation Error: {email_address} {e}"


