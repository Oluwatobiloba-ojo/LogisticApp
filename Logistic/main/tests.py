from django.test import TestCase

# Create your tests here.
from .exception import UserExistException, InvalidFormatDetails, InvalidLoginDetails, ActionDoneException, \
    InvalidAdminException, RiderExistException, UnAuthorizedException
from .models import Customer
from .services import register, register_admin, login_admin, login_customer, add_rider, list_of_riders_for, \
    remove_rider_for


# Create your tests here.
class TestSomething(TestCase):
    def test_that_when_register_count_is_one(self):
        user_id = register(first_name="ope", email="oluwapo@gmail.com", password="Oluwashola123",
                           phone_number="08129810794", address="13 jubril")
        self.assertEqual("ope", Customer.objects.get(pk=user_id).user.first_name)

    def test_that_user_can_not_register_having_same_email_throws_exception(self):
        id_user = register(first_name="ope", email="oluwapo@gmail.com", password="Oluwashola123",
                           phone_number="08129810794", address="13 jubril")
        self.assertEqual('ope', Customer.objects.get(pk=id_user).user.first_name)
        with self.assertRaises(UserExistException):
            user_id = register(first_name="ope", email="oluwapo@gmail.com", password="Oluwashola123",
                               phone_number="08032389457", address="13 jubril")

    def test_that_when_user_want_to_get_register_with_wrong_email_format_throws_error(self):
        with self.assertRaises(InvalidFormatDetails):
            register(first_name="ope", email="wrong_email", password="Oluwashola123", phone_number="0857363",
                     address="13 jubril")

    def test_that_when_customer_tries_to_register_with_a_weak_password_throws_error(self):
        with self.assertRaises(InvalidFormatDetails):
            register(first_name="ope", email="oluwapo@gmail.com", password="weak_password", phone_number="0857363",
                     address="13 jubril")

    def test_that_when_customer_login_with_wrong_password_throws_exception(self):
        register(first_name="tobi", email="oluwapo@gmail.com", password="Oluwashola1",
                 phone_number="08129810794", address='13 wosilatu')
        with self.assertRaises(InvalidLoginDetails):
            login_customer(email="oluwapo@gmail.com", password="wrong_password")

    def test_that_when_customer_login_with_wrong_email_throws_exception(self):
        with self.assertRaises(InvalidLoginDetails):
            login_customer(email="email_not_register", password="Oluwashola1")

    def test_that_when_customer_login_twiceThrows_exception(self):
        register(first_name="tobi", email="oluwapo@gmail.com", password="Oluwashola1",
                 phone_number="08129810794", address='13 wosilatu')
        login_customer(email="oluwapo@gmail.com", password="Oluwashola1")
        with self.assertRaises(ActionDoneException):
            login_customer(email="oluwapo@gmail.com", password="Oluwashola1")

    def test_that_a_customer_can_book_the_delivery(self):
        user_id = register(first_name="ope", email="oluwapo@gmail.com", password="Oluwashola@",
                           phone_number="07032389457", address="13 jubril")
        # book_delivery(customer_id=user_id, receiver_name="olakunle", receiverAddress="13 agege",
        #               pickUpAddress="13 alimosho road", pickUpName="delight", package_description="A box of food", vehicle_type="Bike")


class TestAdministrator(TestCase):
    def test_that_administrator_when_register_with_wrong_email_format_throw_exception(self):
        with self.assertRaises(InvalidFormatDetails):
            register_admin(first_name="tobi", email="wrong_email", password="Oluwapo",
                           phone_number="08129810794", address='13 wosilatu', company_name="SunShine")

    def test_that_when_an_administrator_register_with_a_weak_password_throws_exception(self):
        with self.assertRaises(InvalidFormatDetails):
            register_admin(first_name="tobi", email="oluwapo@gmail.com", password="weak_password",
                           phone_number="08129810794", address='13 wosilatu', company_name="SunShine")

    def test_that_when_an_admin_register_with_wrong_phone_number_format_throws_exception(self):
        with self.assertRaises(InvalidFormatDetails):
            register_admin(first_name="tobi", email="oluwapo@gmail.com", password="Oluwashola1",
                           phone_number="08129", address='13 wosilatu', company_name="SunShine")

    def test_that_when_user_register_with_same_username_throws_exception(self):
        register_admin(first_name="tobi", email="oluwapo@gmail.com", password="Oluwashola1",
                       phone_number="08129810794", address='13 wosilatu', company_name="SunShine")
        with self.assertRaises(UserExistException):
            register_admin(first_name="tobi", email="oluwapo@gmail.com", password="Oluwashola1",
                           phone_number="08129810794", address='13 wosilatu', company_name="SunShine")

    def test_that_when_admin_want_to_login_with_wrong_password_throws_invalid_login_details(self):
        register_admin(first_name="tobi", email="oluwapo@gmail.com", password="Oluwashola1",
                       phone_number="08129810794", address='13 wosilatu', company_name="SunShine")
        with self.assertRaises(InvalidLoginDetails):
            login_admin(company_name="SunShine", password="wrong_password")

    def test_that_when_admin_want_to_login_with_wrong_company_name_throw_exception(self):
        register_admin(first_name="tobi", email="oluwapo@gmail.com", password="Oluwashola1",
                       phone_number="08129810794", address='13 wosilatu', company_name="SunShine")
        with self.assertRaises(InvalidLoginDetails):
            login_admin(company_name="wrong_company", password="Oluwashola1")

    def test_that_when_admin_login_when_he_already_have_login_throw_exception(self):
        register_admin(first_name="tobi", email="oluwapo@gmail.com", password="Oluwashola1",
                       phone_number="08129810794", address='13 wosilatu', company_name="SunShine")
        login_admin(company_name="SunShine", password="Oluwashola1")
        with self.assertRaises(ActionDoneException):
            login_admin(company_name="SunShine", password="Oluwashola1")

    def test_that_when_admin_want_to_add_a_rider_but_wrong_email_format_throws_exception(self):
        register_admin(first_name="tobi", email="oluwapo@gmail.com", password="Oluwashola1",
                       phone_number="08129810794", address='13 wosilatu', company_name="SunShine")
        login_admin(company_name="SunShine", password="Oluwashola1")
        with self.assertRaises(InvalidFormatDetails):
            add_rider(company_name="SunShine", rider_name="Qudus", rider_email="wrong_email", password="Qudus123",
                      phone_number="08032389457", address="17, jubrila", transport_type="BS",
                      plate_number="ABC 123EF", driver_license="Qudus12358769", color_of_transportation="Red")

    def test_that_when_admin_want_to_add_rider_and_admin_company_name_does_not_exist(self):
        with self.assertRaises(InvalidAdminException):
            add_rider(company_name="SunShine", rider_name="Qudus", rider_email="qudus12@gmail.com",
                      password="Qudus123", phone_number="08032389457", address="17, jubrila", transport_type="BS",
                      plate_number="ABC 123EF", driver_license="Qudus12358769", color_of_transportation="Red")

    def test_that_when_admin_add_rider_with_weak_password_throws_exception(self):
        register_admin(first_name="tobi", email="oluwapo@gmail.com", password="Oluwashola1",
                       phone_number="08129810794", address='13 wosilatu', company_name="SunShine")
        login_admin(company_name="SunShine", password="Oluwashola1")
        with self.assertRaises(InvalidFormatDetails):
            add_rider(company_name="SunShine", rider_name="Qudus", rider_email="qudus@gmail.com",
                      password="weak_password",
                      phone_number="08032389457", address="17, jubrila", transport_type="BS",
                      plate_number="ABC 123EF", driver_license="Qudus12358769", color_of_transportation="Red")

    def test_that_when_admin_register_rider_with_a_wrong_phone_number_format_throws_exception(self):
        register_admin(first_name="tobi", email="oluwapo@gmail.com", password="Oluwashola1",
                       phone_number="08129810794", address='13 wosilatu', company_name="SunShine")
        login_admin(company_name="SunShine", password="Oluwashola1")
        with self.assertRaises(InvalidFormatDetails):
            add_rider(company_name="SunShine", rider_name="Qudus", rider_email="qudus@gmail.com",
                      password="Olakule123", phone_number="08032", address="17, jubrila", transport_type="BS",
                      plate_number="ABC 123EF", driver_license="Qudus12358769", color_of_transportation="Red")

    def test_that_when_admin_has_not_login_and_want_to_register_rider_throws_exception(self):
        register_admin(first_name="tobi", email="oluwapo@gmail.com", password="Oluwashola1",
                       phone_number="08129810794", address='13 wosilatu', company_name="SunShine")
        with self.assertRaises(InvalidAdminException):
            add_rider(company_name="SunShine", rider_name="Qudus", rider_email="qudus@gmail.com",
                      password="Olakule123", phone_number="08032389457", address="17, jubrila", transport_type="BS",
                      plate_number="ABC 123EF", driver_license="Qudus12358769", color_of_transportation="Red")

    def test_that_when_admin_register_a_rider_the_list_of_rider_belonging_to_the_admin_increase_by_one(self):
        register_admin(first_name="tobi", email="oluwapo@gmail.com", password="Oluwashola1",
                       phone_number="08129810794", address='13 wosilatu', company_name="SunShine")
        login_admin(company_name="SunShine", password="Oluwashola1")
        add_rider(company_name="SunShine", rider_name="Qudus", rider_email="qudus@gmail.com",
                  password="Olakule123", phone_number="08032389457", address="17, jubrila", transport_type="BS",
                  plate_number="ABC 123EF", driver_license="Qudus12358769", color_of_transportation="Red")
        self.assertEqual(1, len(list_of_riders_for("SunShine")))

    def test_that_admin_can_not_register_a_rider_with_same_plate_number(self):
        register_admin(first_name="tobi", email="oluwapo@gmail.com", password="Oluwashola1",
                       phone_number="08129810794", address='13 wosilatu', company_name="SunShine")
        login_admin(company_name="SunShine", password="Oluwashola1")
        add_rider(company_name="SunShine", rider_name="Qudus", rider_email="qudus@gmail.com",
                  password="Olakule123", phone_number="08032389457", address="17, jubrila", transport_type="BS",
                  plate_number="ABC 123EF", driver_license="Qudus12358769", color_of_transportation="Red")
        with self.assertRaises(RiderExistException):
            add_rider(company_name="SunShine", rider_name="Qudus", rider_email="qudus@gmail.com",
                      password="Olakule123", phone_number="08032389457", address="17, jubrila", transport_type="BS",
                      plate_number="ABC 123EF", driver_license="Qudus12358769", color_of_transportation="Red")
        self.assertEqual(1, len(list_of_riders_for("SunShine")))

    def test_that_admin_when_has_register_rider_can_remove_the_rider_from_the_list(self):
        register_admin(first_name="tobi", email="oluwapo@gmail.com", password="Oluwashola1",
                       phone_number="08129810794", address='13 wosilatu', company_name="SunShine")
        login_admin(company_name="SunShine", password="Oluwashola1")
        add_rider(company_name="SunShine", rider_name="Qudus", rider_email="qudus@gmail.com",
                  password="Olakule123", phone_number="08032389457", address="17, jubrila", transport_type="BS",
                  plate_number="ABC 123EF", driver_license="Qudus12358769", color_of_transportation="Red")
        add_rider(company_name="SunShine", rider_name="Qudus", rider_email="qudus@gmail.com",
                  password="Olakule123", phone_number="08032389457", address="17, jubrila", transport_type="BS",
                  plate_number="BCD 123 678", driver_license="Qudus12358769", color_of_transportation="Red")
        self.assertEqual(2, len(list_of_riders_for("SunShine")))
        remove_rider_for("SunShine", "ABC 123EF")
        self.assertEqual(1, len(list_of_riders_for("SunShine")))

    def test_that_when_the_wrong_admin_want_to_remove_rider_throw_exception(self):
        register_admin(first_name="tobi", email="oluwapo@gmail.com", password="Oluwashola1",
                       phone_number="08129810794", address='13 wosilatu', company_name="SunShine")
        login_admin(company_name="SunShine", password="Oluwashola1")
        add_rider(company_name="SunShine", rider_name="Qudus", rider_email="qudus@gmail.com",
                  password="Olakule123", phone_number="08032389457", address="17, jubrila", transport_type="BS",
                  plate_number="ABC 123EF", driver_license="Qudus12358769", color_of_transportation="Red")
        self.assertEqual(1, len(list_of_riders_for("SunShine")))
        with self.assertRaises(UserExistException):
            remove_rider_for("wrong_company_name", "ABC 123EF")

    def test_that_when_the_admin_want_to_remove_a_rider_with_the_driver_license_which_does_not_belong_to_him(self):
        register_admin(first_name="tobi", email="oluwapo@gmail.com", password="Oluwashola1",
                       phone_number="08129810794", address='13 wosilatu', company_name="SunShine")
        register_admin(first_name="tobi", email="oluwapo@gmail.com", password="Oluwashola1",
                       phone_number="08129810794", address='13 wosilatu', company_name="SunMaking")
        login_admin(company_name="SunShine", password="Oluwashola1")
        login_admin(company_name="SunMaking", password="Oluwashola1")
        add_rider(company_name="SunShine", rider_name="Qudus", rider_email="qudus@gmail.com",
                  password="Olakule123", phone_number="08032389457", address="17, jubrila", transport_type="BS",
                  plate_number="ABC 123EF", driver_license="Qudus12358769", color_of_transportation="Red")
        self.assertEqual(1, len(list_of_riders_for("SunShine")))
        with self.assertRaises(UnAuthorizedException):
            remove_rider_for("SunMaking", "ABC 123EF")
        self.assertEqual(1, len(list_of_riders_for("SunShine")))






