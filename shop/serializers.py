from .models import *
from rest_framework import serializers
import re


class CustomerSerializers(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"

    def validate_name(self, value):
        if re.fullmatch(r"[a-zA-Z ]+", value) and len(value) >= 2:
            return value
        else:
            raise serializers.ValidationError('This field must contain only alphabetic characters.')

    def validate_mobile(self, value):
        if re.fullmatch(r"\d{10,15}", value):
            return value
        raise serializers.ValidationError("Mobile number must be between 10 and 15 digits.")


class AddressSerializers(serializers.ModelSerializer):
    # The PrimaryKeyRelatedField will convert ID into the corresponding
    # Customer object by querying the database.
    customer = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all(),
        write_only=True
    )

    customer_details = CustomerSerializers(source="customer", read_only=True)

    class Meta:
        model = Address
        fields = ["id", "customer", "street", "city", "postal_code", "country", "customer_details"]


class FlowerSerializers(serializers.ModelSerializer):
    class Meta:
        model = Flower
        fields = ['id', 'name', 'description', 'price', 'stock', 'image_url', 'category']


class OrderSerializers(serializers.ModelSerializer):
    flower = serializers.PrimaryKeyRelatedField(
        queryset=Flower.objects.all(),
        write_only=True
    )

    flower_details = FlowerSerializers(source="flower", read_only=True)

    class Meta:
        model = Order
        fields = ["flower", "flower_details", "ordered_at", "quantity", "price"]


class ContactSerializers(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ["id", "name", "email", "message"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
