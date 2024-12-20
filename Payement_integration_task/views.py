from django.shortcuts import render
import razorpay
from django.http import JsonResponse
from django.conf import settings
import json


client = razorpay.Client(auth=(settings.KEY, settings.RAZORPAY_SECRET_KEY))


def home(request):
    return render(request, 'index.html')


def create_order(request):

    if request.method == "POST":
        try:

            data = json.loads(request.body)
            product_name = data.get("product_name", "Unknown Product")
            amount = int(data.get("price", 0))*100  

            print(amount) 

            

        
            order = client.order.create({
                "amount": amount,
                "currency": "INR",
                "receipt": f"receipt_{product_name}",
                "notes": {"Product": product_name},
            })

            return JsonResponse( {
                "id": order["id"],
                "amount": order["amount"],
                "currency": order["currency"],
                "product_name": product_name
            })
        
        except Exception as e:

            return JsonResponse({"error": str(e)}, status=500)
        

    return JsonResponse({"error": "Invalid request method"}, status=400)
