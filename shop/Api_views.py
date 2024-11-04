from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .models import Customer, Address, Flower
from django.core.mail import send_mail
from .serializers import *
from rest_framework.views import APIView
from rest_framework import status
from .forms import ContactForm


# class contactView(APIView):
#     class ContactView(APIView):
#         def get(self, request):
#             # Render the contact form
#             form = ContactForm()
#             return render(request, 'contact.html', {'form': form})
#
#     # def post(self, request):
#     #     data = CustomerSerializers(data=request.data)
#     #     if data.is_valid():
#     #         data.save()
#     #         return Response(data.data, status=status.HTTP_200_OK)
#     #     return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)
#     def post(self, request):
#         # Handle form submission via POST request
#         form = ContactForm(request.POST)
#         if form.is_valid():
#             form.save()  # Save the form data to the database
#             # After saving, redirect or render a success message (e.g., the same contact page with a message)
#             return render(request, 'contact.html',
#                           {'form': ContactForm(), 'success': 'Your message has been sent successfully!'})
#         else:
#             # If the form is not valid, re-render the form with validation errors
#             return render(request, 'contact.html', {'form': form, 'error': 'Please correct the errors below.'})

class CustomerView(APIView):
    def get(self, request, id=None, name=None):
        get_id = request.query_params.get("id")
        get_name = request.query_params.get("name")

        id = get_id or id
        name = get_name or name

        if id:
            try:
                data = Customer.objects.get(id=id)
                return Response(CustomerSerializers(data).data)
            except Customer.DoesNotExist:
                raise NotFound(detail="Customer not found.")

        if name:
            data = Customer.objects.filter(name__icontains=name)
            if data.exists():
                return Response(CustomerSerializers(data, many=True).data)
            raise NotFound(detail="Customer not found.")

        return Response(CustomerSerializers(Customer.objects.all(), many=True).data)

    def post(self, request):
        serializer = CustomerSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_objects(self, id):
        try:
            return Customer.objects.get(id=id)
        except Customer.DoesNotExist:
            raise NotFound(detail="Customer Not Found")

    def put(self, request, id):
        customer = self.get_objects(id)
        serializer = CustomerSerializers(customer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id):
        customer = self.get_objects(id)
        serializer = CustomerSerializers(customer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddressView(APIView):
    def get(self, request, id=None):
        get_id = request.query_params.get("id")
        id = get_id or id

        if id:
            try:
                data = Address.objects.get(id=id)
                return Response(AddressSerializers(data).data)
            except Address.DoesNotExist:
                raise NotFound(detail="Address not found.")

        return Response(AddressSerializers(Address.objects.all(), many=True).data)

    def post(self, request):
        serializer = AddressSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_objects(self, id):
        try:
            return Address.objects.get(id=id)
        except Address.DoesNotExist:
            raise NotFound(detail="Address Not Found")

    def put(self, request, id):
        address = self.get_objects(id)
        serializer = AddressSerializers(address, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id):
        address = self.get_objects(id)
        serializer = AddressSerializers(address, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FlowerView(APIView):
    def get(self, request, id=None, name=None):
        get_id = request.query_params.get("id")
        get_name = request.query_params.get("name")

        id = get_id or id
        name = get_name or name

        if id:
            try:
                data = Flower.objects.get(id=id)
                flower = FlowerSerializers(data, many=True).data
                return Response(flower, status=status.HTTP_200_OK)

            except Flower.DoesNotExist:
                raise NotFound(detail="Flower not found.")

        if name:
            data = Flower.objects.filter(name__icontains=name)

            if data.exists():
                flower = FlowerSerializers(data, many=True).data
                return Response(flower, status=status.HTTP_200_OK)
            raise NotFound(detail="Flower not found.")

        return Response(FlowerSerializers(Flower.objects.all(), many=True).data)

    def post(self, request):
        serializer = FlowerSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_objects(self, id):
        try:
            return Flower.objects.get(id=id)
        except Flower.DoesNotExist:
            raise NotFound(detail="Flower not found.")

    def put(self, request, id):
        flower = self.get_objects(id)
        serializer = FlowerSerializers(flower, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id):
        flower = self.get_objects(id)
        serializer = FlowerSerializers(flower, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoriesView(APIView):
    def get(self, request, id=None, name=None):
        get_id = request.query_params.get("id")
        get_name = request.query_params.get("name")

        id = get_id or id
        name = get_name or name

        if id:
            try:
                data = Category.objects.get(id=id)
                return Response(CategorySerializer(data).data, status=status.HTTP_200_OK)
            except Category.DoesNotExist:
                raise NotFound(detail="Category not found.")

        if name:
            data = Category.objects.filter(name__icontains=name)
            if data.exists():
                return Response(CategorySerializer(data, many=True).data, status=status.HTTP_200_OK)
            raise NotFound(detail="Category not found.")

        return Response(CategorySerializer(Category.objects.all(), many=True).data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_objects(self, id):
        try:
            return Category.objects.get(id=id)
        except Category.DoesNotExist:
            raise NotFound(detail="Category not found.")

    def put(self, request, id):
        category = self.get_objects(id)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        category = self.get_objects(id)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class Orders(APIView):
    def get(self, request, id=None):
        get_id = request.query_params.get("id")
        id = get_id or id

        if id:
            try:
                order = Order.objects.get(id=id)
                serialized_data = OrderSerializers(order).data
                return Response(serialized_data,status=status.HTTP_200_OK)
            except Order.DoesNotExist:
                raise NotFound(detail="order not found.")

        orders = Order.objects.select_related('flower').all()
        serialized_data = OrderSerializers(orders, many=True).data
        return Response(serialized_data,status=status.HTTP_200_OK)



# class OrderView(APIView):
#     def post(self, request):
#         serializer = OrderSerializers(data=request.data)
#         if serializer.is_valid():
#             order = serializer.save()
#
#             # Send notification to the shop owner
#             flower_names = ", ".join([item['flower'] for item in request.data['items']])
#             total_price = sum(
#                 [Flower.objects.get(id=item['flower']).price * item['quantity'] for item in request.data['items']])
#             send_mail(
#                 subject='New Flower Order',
#                 message=f'You have received a new order for {flower_names}. Total price: ${total_price:.2f}.',
#                 from_email='your_email@gmail.com',
#                 recipient_list=['shop_owner_email@example.com'],
#             )
#
#             # Send confirmation email to the customer
#             send_mail(
#                 subject='Order Confirmation',
#                 message=f'Thank you for your order! You ordered {flower_names}. Total price: ${total_price:.2f}.',
#                 from_email='your_email@gmail.com',
#                 recipient_list=[order.customer_email],
#             )
#
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
