from user_package.user import User
from user_package.appuser import AppUser
from icecream import ic

def main():
    usr1 = User('Rich')
    print(f'__str__: usr1: {usr1}')

    usr2 = AppUser('Rich', 'Admin', "rlynch3456@yahoo.com")
    usr2.generate_id()
    ic(usr2)
    print(f'__str__: {str(usr2)}')
    print(f'__repr__: {repr(usr2)}')
    print(f'is Admin? {usr2.is_admin()}')
    usr3 = AppUser('Rich', 'guest')
    ic(usr2 == usr3)

if __name__ == "__main__":
    main()
