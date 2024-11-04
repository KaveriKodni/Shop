from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=100, default="User")
    mobile = models.CharField(max_length=15, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    class Meta:

        db_table = "customer"


class Address(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10)
    country = models.CharField(max_length=50)

    class Meta:
        db_table = "address"


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    class Meta:
        db_table = "category"


class Flower(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    stock = models.IntegerField()
    image_url = models.URLField(max_length=200, blank=True)

    class Meta:
        db_table = "flower"


class Order(models.Model):
    ordered_at = models.DateTimeField(auto_now_add=True)
    flower = models.ForeignKey(Flower, on_delete=models.CASCADE,)  # The flower being ordered
    quantity = models.IntegerField()  # Quantity of the flower
    price = models.DecimalField(max_digits=7, decimal_places=2)  # Price of the flower

    class Meta:
        db_table = "order"


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()

    class Meta:
        db_table = 'contact'
