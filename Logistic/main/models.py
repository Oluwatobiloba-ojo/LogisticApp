from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.
class common(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True)
    phone_number = models.CharField(max_length=230)
    address = models.TextField(max_length=235)
    login_status = models.BooleanField(default=False)

    class Meta:
        abstract = True


class Customer(common):

    def __str__(self):
        return self.user.name


class Administrator(common):
    company_name = models.CharField(max_length=235)

    def __str__(self):
        return self.company_name


class Rider(common):
    TRANSPORTATION_MEANS = {
        "BS": "BUS",
        "BE": "BIKE",
        "TK": "TRUCK",
        "ME": "MOTOR_BIKE"
    }
    transport_type = models.CharField(max_length=2, choices=TRANSPORTATION_MEANS)
    admin = models.ForeignKey(Administrator, on_delete=models.CASCADE)
    plate_number = models.CharField(max_length=200, unique=True)
    driver_license = models.CharField(max_length=235)
    color_of_transportation = models.CharField(max_length=200)
    location = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.admin


class Delivery(models.Model):
    rider = models.ForeignKey(Rider, on_delete=models.CASCADE)
    receiver_name = models.CharField(max_length=235)
    pick_up_name = models.CharField(max_length=200)
    pick_up_address = models.TextField(db_column='pick_up_location')
    receiver_address = models.TextField(db_column="receiver_location")
    package_description = models.TextField(db_column="description")
    vehicle_type = models.CharField(max_length=200)
    customer_email = models.EmailField(max_length=200, unique=True)

    def __str__(self):
        return self.rider
