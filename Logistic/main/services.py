from django.contrib.auth.models import User

from .exception import UserExistException, InvalidFormatDetails, InvalidLoginDetails, ActionDoneException, \
    InvalidAdminException, RiderExistException, UnAuthorizedException
import re

from .exception import UserExistException, InvalidFormatDetails, InvalidLoginDetails, ActionDoneException, \
    InvalidAdminException
from .models import Customer, Administrator, Rider


def validate(email):
    list_customer = Customer.objects.all()
    for customer in list_customer:
        if customer.user.email == email:
            raise UserExistException("User already exist")


def validateEmail(email: str):
    email_format = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[a-z]{2,7}\b'
    if re.match(email_format, email):
        pass
    else:
        raise InvalidFormatDetails("Invalid format for email")


def validatePassword(password):
    password_path = r'\b[A-Z][A-Za-z0-9.-_%+-]{7,}\b'
    if re.match(password_path, password):
        pass
    else:
        raise InvalidFormatDetails("Invalid format for password")


def validatePhoneNumber(phone_number):
    phone_number_path = r'\b[0][7-9][0-9]{9}\b'
    if re.match(phone_number_path, phone_number):
        pass
    else:
        raise InvalidFormatDetails("Invalid format for phone number")


def register(first_name, phone_number, email, password, address, last_name=""):
    validateEmail(email)
    validatePassword(password)
    validatePhoneNumber(phone_number)
    validate(email)
    user: User = User(first_name=first_name, email=email, last_name=last_name, username=email, password=password)
    user.save()
    customer: Customer = Customer(phone_number=phone_number, address=address, user=user)
    customer.save()
    return customer.pk


def validateAdmin(company_name):
    admin_list: list = Administrator.objects.all()
    for admin in admin_list:
        if admin.company_name == company_name:
            raise UserExistException("Admin already taken")


def register_admin(first_name, email, password, phone_number, address, company_name):
    validateEmail(email)
    validatePassword(password)
    validatePhoneNumber(phone_number)
    validateAdmin(company_name)
    user: User = User(username=company_name, email=email, password=password, first_name=first_name)
    user.save()
    admin: Administrator = Administrator(phone_number=phone_number, company_name=company_name, address=address, user=user)
    admin.save()
    return admin.pk


def findAdmin(company_name):
    list_admin = Administrator.objects.all()
    for admin in list_admin:
        if admin.company_name == company_name:
            return admin
    return None


def login_admin(company_name, password):
    admin: Administrator = findAdmin(company_name)
    if admin is None:
        raise InvalidLoginDetails("Invalid login details")
    if admin.login_status:
        raise ActionDoneException("Login already")
    if admin.user.password != password:
        raise InvalidLoginDetails("Invalid login details")
    admin.login_status = True
    admin.save()


def findCustomer(email):
    list_customer = Customer.objects.all()
    for customer in list_customer:
        if customer.user.email == email:
            return customer
    return None


def login_customer(email, password):
    customer: Customer = findCustomer(email)
    if customer is None:
        raise InvalidLoginDetails("Invalid login details")
    if customer.login_status:
        raise ActionDoneException("Login already done")
    if customer.user.password != password:
        raise InvalidLoginDetails("Invalid login details")
    customer.login_status = True
    customer.save()


def findRider(plate_number):
    for rider in Rider.objects.all():
        if rider.plate_number == plate_number:
            return rider
    return None


def add_rider(company_name, rider_name, rider_email, password, phone_number, address, transport_type, plate_number,
              driver_license, color_of_transportation):
    Admin: Administrator = findAdmin(company_name)
    if Admin is None:
        raise InvalidAdminException("Unsuccessful Registration")
    if not Admin.login_status:
        raise InvalidAdminException("Unsuccessful Registration")
    validateEmail(rider_email)
    validatePassword(password)
    validatePhoneNumber(phone_number)
    rider: Rider = findRider(plate_number)
    if rider:
        raise RiderExistException("rider already exist")
    user: User = User(username=plate_number, email=rider_email, password=password, first_name=rider_name)
    user.save()
    rider: Rider = Rider(user=user, admin=Admin, phone_number=phone_number, address=address, transport_type=transport_type,
                         plate_number=plate_number, driver_license=driver_license,
                         color_of_transportation=color_of_transportation)
    rider.save()


def list_of_riders_for(company_name):
    admin: Administrator = findAdmin(company_name)
    if admin is None:
        raise UserExistException("Invalid admin")
    list_of_rider = []
    for rider in Rider.objects.all():
        if rider.admin == admin:
            list_of_rider.append(rider)
    return list_of_rider


def remove_rider_for(company_name, rider_plate_number):
    admin: Administrator = findAdmin(company_name)
    if admin is None:
        raise UserExistException("Invalid details")
    if not admin.login_status:
        raise InvalidLoginDetails("User not login")
    rider: Rider = findRider(rider_plate_number)
    if rider.admin != admin:
        raise UnAuthorizedException("Can not perform request")
    rider.delete()
