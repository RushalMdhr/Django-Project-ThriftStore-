import os
from django.shortcuts import render
from .models import *
from django.views import View
import hashlib

class EsewaRequestView(View):
    def get(self, request, *args, **kwargs):
        # Retrieve the order data and other necessary information
        o_id = request.GET.get("o_id")
        order = Ordered.objects.get(id=o_id)  # Replace with your actual model and logic
        access_key = os.getenv("ESEWA_ACCESS_KEY")  # Access eSewa access key from environment variable
        secret_key = os.getenv("ESEWA_SECRET_KEY")
        # Prepare the data dictionary
        data = {
            "amount": "100",
            "tax_amount": "10",
            "total_amount": "110",
            "transaction_uuid": "ab14a8f2b02c3",
            "product_code": "EPAYTEST",
            
            "access_key": access_key,
            "signature": None, 
        }

        # Sort the data alphabetically by keys
        sorted_data = {k: data[k] for k in sorted(data)}

        # Concatenate the values into a single string
        concatenated_data = ''.join(sorted_data.values())

        # Append your eSewa API secret key
        concatenated_data_with_secret = concatenated_data + secret_key

        # Calculate the SHA-256 hash
        signature = hashlib.sha256(concatenated_data_with_secret.encode()).hexdigest()

        # Update the data dictionary with the calculated signature
        data["signature"] = signature

        context = {
            "order": order,
            "data": data,
        }
        return render(request, "app/esewarequest.html", context)