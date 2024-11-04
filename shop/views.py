from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .models import Customer, Address, Flower
from django.core.mail import send_mail
from .serializers import *
from rest_framework.views import APIView
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from django.core.paginator import Paginator
from .forms import ContactForm


# views.py
def home_page(request):
    flowers = Flower.objects.all()
    return render(request, 'index.html', {'flowers': flowers})


class shop_page(APIView):
    def get(self, request):
        # Get the search query from the request
        get_name = request.query_params.get("name", "")
        flowers = Flower.objects.all().order_by('id')

        # If a search query is provided, filter the flowers based on the name
        if get_name:
            flowers = flowers.filter(name__icontains=get_name)

        paginator = Paginator(flowers, 3)  # adding limit on data
        page_num = request.query_params.get("page", 1)  # getting page number where u present
        final = paginator.get_page(page_num)  # it will show data based on page_num
        data = {
            "flowers": final,
            "get_name": get_name,
        }
        print(final)
        return render(request, "shop.html", data)


def blog_page(request):
    return render(request, "Blog.html")


def About_page(request):
    return render(request, "AboutUs.html")


def cart_page(request):
    return render(request, "cart.html")


class Order_view(APIView):
    def get(self, request, id=None):
        # get_id = request.query_params.get("id")
        # id = get_id or id

        # if id:
        #     try:
        #         order = Order.objects.select_related('flower').get(id=id)
        #         serialized_data = OrderSerializers(order).data
        #         # return render(request, "order.html", {'Order': [serialized_data]})
        #         return Response(serialized_data,status=status.HTTP_200_OK)
        #     except Order.DoesNotExist:
        #         raise NotFound(detail="order not found.")
        orders = Order.objects.select_related('flower').all()
        print(orders)
        serialized_data = OrderSerializers(orders, many=True).data
        print([serialized_data])
        return render(request, "order.html", )

    def post(self, request):
        # Expecting an array of items in the request
        order_data = request.data.get('items', [])
        created_orders, total_amount = [], 0

        for item in order_data:
            serializer = OrderSerializers(data={
                'flower': item['flower'],  # Use the ID from the cart item
                'quantity': item['quantity'],
                'price': item['price']
            })
            if serializer.is_valid():
                order = serializer.save()
                created_orders.append(order.id)
                total_amount += item['quantity'] * float(item['price'])
                created_orders.append(order.id)  # Keep track of created order IDs
            else:
                return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        # self._send_order_email(order_data, total_amount, request.data['address'], request.data['mobile_number'])
        send_mail(
            "Order request",
            "Order",
            "dummyforwork125@gmail.com",
            ['kaverikodni@gmail.com'],
        )
        return Response({
            "success": "Orders placed successfully!",
            "order_ids": created_orders
        }, status=status.HTTP_201_CREATED)

    # send_mail(
    #     "Order request",
    #     "Order",
    #     "dummyforwork125@gmail.com",
    #     ['kaverikodni@gmail.com'],
    # )
    # def _send_order_email(self, order_items, total_amount, address, mobile_number):
    #     """Helper method to send email after order is saved."""
    #     message = f"Dear Owner,\n\nNew order received:\n\nAddress: {address}\nMobile: {mobile_number}\n\n"
    #     message += "Order Details:\n"
    #     for item in order_items:
    #         flower = Flower.objects.get(id=item['flower'])
    #         message += f"- {flower.name} (Qty: {item['quantity']}) - Rs {item['price'] * item['quantity']}\n"
    #
    #     gst = total_amount * 0.05
    #     grand_total = total_amount + gst
    #     message += f"\nTotal: Rs {total_amount:.2f}\nGST: Rs {gst:.2f}\nGrand Total: Rs {grand_total:.2f}\n\nBest regards,\nFlower Shop"
    #
    #     send_mail(
    #         "New Order Confirmation",
    #         message,
    #         settings.DEFAULT_FROM_EMAIL,
    #         ['kaverikodni@gmail.com'],  # Replace with the shop owner's email
    #         fail_silently=False,
    #     )


def Submit_page(request):
    return HttpResponse("<h1>Your Message sent</h1>")


# class ContactView(APIView):
#     def get(self, request):
#         # Render the contact page with the form
#         return render(request, 'contact.html')
#
#     # Handle form submission
#     def post(self, request):
#         serializer = ContactSerializers(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return render(request, 'contact.html', {'success': 'Your message has been sent successfully!'})
#         else:
#             return render(request, 'contact.html', {'error': 'Please correct the errors below.'})

class ContactView(APIView):
    def get(self, request):
        form = ContactForm()  # Initialize an empty form
        return render(request, 'contact.html', {'form': form})

    # Handle form submission
    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'contact.html', {'form': ContactForm(), 'success': 'Your message has been sent successfully!'})
        else:
            return render(request, 'contact.html', {'form':form,'error': 'Please correct the errors below.'})


# class AddressView(APIView):
#     def get(self, request, id=None):
#         get_id = request.query_params.get("id")
#         id = get_id or id
#
#         if id:
#             try:
#                 data = Address.objects.get(id=id)
#                 return Response(AddressSerializers(data).data)
#             except Address.DoesNotExist:
#                 raise NotFound(detail="Address not found.")
#
#         return Response(AddressSerializers(Address.objects.all(), many=True).data)
#
#     def post(self, request):
#         serializer = AddressSerializers(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def get_objects(self, id):
#         try:
#             return Address.objects.get(id=id)
#         except Address.DoesNotExist:
#             raise NotFound(detail="Address Not Found")
#
#     def put(self, request, id):
#         address = self.get_objects(id)
#         serializer = AddressSerializers(address, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def patch(self, request, id):
#         address = self.get_objects(id)
#         serializer = AddressSerializers(address, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class FlowerView(APIView):
#     def get(self, request, id=None, name=None):
#         get_id = request.query_params.get("id")
#         get_name = request.query_params.get("name")
#
#         id = get_id or id
#         name = get_name or name
#
#         if id:
#             try:
#                 data = Flower.objects.get(id=id)
#                 flower = FlowerSerializers(data, many=True).data
#                 return render(request, "shop.html", {'flowers': flower})
#
#             except Flower.DoesNotExist:
#                 raise NotFound(detail="Flower not found.")
#
#         if name:
#             data = Flower.objects.filter(name__icontains=name)
#
#             if data.exists():
#                 flower = FlowerSerializers(data, many=True).data
#                 return render(request, "shop.html", {'flowers': flower})
#             raise NotFound(detail="Flower not found.")
#
#         return Response(FlowerSerializers(Flower.objects.all(), many=True).data)
#
#     def post(self, request):
#         serializer = FlowerSerializers(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def get_objects(self, id):
#         try:
#             return Flower.objects.get(id=id)
#         except Flower.DoesNotExist:
#             raise NotFound(detail="Flower not found.")
#
#     def put(self, request, id):
#         flower = self.get_objects(id)
#         serializer = FlowerSerializers(flower, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def patch(self, request, id):
#         flower = self.get_objects(id)
#         serializer = FlowerSerializers(flower, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class CategoriesView(APIView):
#     def get(self, request, id=None, name=None):
#         get_id = request.query_params.get("id")
#         get_name = request.query_params.get("name")
#
#         id = get_id or id
#         name = get_name or name
#
#         if id:
#             try:
#                 data = Category.objects.get(id=id)
#                 return Response(CategorySerializer(data).data, status=status.HTTP_200_OK)
#             except Category.DoesNotExist:
#                 raise NotFound(detail="Category not found.")
#
#         if name:
#             data = Category.objects.filter(name__icontains=name)
#             if data.exists():
#                 print(data.data)
#                 return Response(CategorySerializer(data, many=True).data, status=status.HTTP_200_OK)
#             raise NotFound(detail="Category not found.")
#
#         return Response(CategorySerializer(Category.objects.all(), many=True).data)
#
#     def post(self, request):
#         serializer = CategorySerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def get_objects(self, id):
#         try:
#             return Category.objects.get(id=id)
#         except Category.DoesNotExist:
#             raise NotFound(detail="Category not found.")
#
#     def put(self, request, id):
#         category = self.get_objects(id)
#         serializer = CategorySerializer(category, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, id):
#         category = self.get_objects(id)
#         category.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#
#
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

class flower_view(APIView):
    def get(self, request, id=None, name=None):
        # Get query parameters from the request
        get_id = request.query_params.get("id")
        get_name = request.query_params.get("name")

        id = get_id or id
        name = get_name or name

        if id:
            try:
                flower = Flower.objects.get(id=id)
                serialized_data = FlowerSerializers(flower).data
                return render(request, "shop.html", {'flowers': [serialized_data]})
            except Flower.DoesNotExist:
                raise NotFound(detail="Flower not found.")

        if name:
            flowers = Flower.objects.filter(name__icontains=name)
            if flowers.exists():
                serialized_data = FlowerSerializers(flowers, many=True).data
                return render(request, "shop.html", {'flowers': serialized_data})
            raise NotFound(detail="Flower not found.")

        # If no specific ID or name, return all flowers
        flowers = Flower.objects.all()
        serialized_data = FlowerSerializers(flowers, many=True).data
        return render(request, "shop.html", {'flowers': serialized_data})
