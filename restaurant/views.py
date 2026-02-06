# file: restaurant/views.py
# Author: Jerry Teixeira, jerrybt@bu.edu, 02/06/2026
# description: Views for the restaurant app, including main page, order page, and confirmation page.
# Create your views here.
from django.shortcuts import render
import random
from django.utils import timezone
from datetime import timedelta

# This view simply directs the application to display the main.html template
def main(request):
    '''main page view'''
    template_name = "restaurant/main.html"
    return render(request, template_name)


# list of daily specials (can be changed each time the page is loaded)
daily_specials = [
    {
        "key": "special",
        "name": "Spicy Tuna Bowl",
        "description": "Sushi rice, spicy tuna, cucumber, avocado, sesame",
        "price": 13.50,
    },
    {
        "key": "special",
        "name": "Truffle Mushroom Flatbread",
        "description": "Mushrooms, truffle oil, mozzarella, arugula",
        "price": 14,
    },
    {
        "key": "special",
        "name": "BBQ Chicken Wrap",
        "description": "BBQ chicken, cheddar, slaw, chipotle mayo",
        "price": 12.99,
    },
]

def order(request):
    '''order page view'''

    special = random.choice(daily_specials)

    context = {
        "daily_special": special,
    }
    template_name = "restaurant/order.html"
    return render(request, template_name, context)



def confirmation(request):
    """Process the form submission and generate a confirmation page of the order."""
    print(request.POST)
    template_name = "restaurant/confirmation.html"

    # Only accept POSTs from the form
    if request.POST:

        # Menu prices (use .get with defaults to avoid KeyError)
        prices = {
            "burger": 10,
            "salad": 8,
            "pizza": 12,
            "tacos": 11,
            "special": float(request.POST.get("special_price", "0") or 0), # Get the special price from the form, default to 0 if not provided or empty
        }
        # Menu item names
        names = {
            "burger": "Classic Burger",
            "salad": "Garden Salad",
            "pizza": "Build-Your-Own Pizza",
            "tacos": "Street Tacos (3)",
            "special": request.POST.get("special_name", "Daily Special"), # Get the special name from the form, default to "Daily Special" if not provided
        }

        ordered_items = [] # List to hold details of ordered items for the confirmation page
        total_price = 0.0 # Running total of the order price

        # Process selected items
        if request.POST.get("burger") == "on":
            ordered_items.append({"key": "burger", "name": names["burger"], "price": prices["burger"]})
            total_price += prices["burger"]

        if request.POST.get("salad") == "on":
            ordered_items.append({"key": "salad", "name": names["salad"], "price": prices["salad"]})
            total_price += prices["salad"]

        if request.POST.get("tacos") == "on":
            ordered_items.append({"key": "tacos", "name": names["tacos"], "price": prices["tacos"]})
            total_price += prices["tacos"]

        if request.POST.get("pizza") == "on":
            toppings = request.POST.getlist("pizza_toppings")
            details_parts = []
            if toppings:
                details_parts.append("Toppings: " + ", ".join(toppings))
            if request.POST.get("pizza_extra_cheese") == "on":
                details_parts.append("Extra cheese")

            ordered_items.append(
                {
                    "key": "pizza",
                    "name": names["pizza"],
                    "price": prices["pizza"],
                    "details": " | ".join(details_parts),
                }
            )
            total_price += prices["pizza"]

        if request.POST.get("special") == "on":
            ordered_items.append({"key": "special", "name": names["special"], "price": prices["special"]})
            total_price += prices["special"]

        # Customer info + instructions
        customer = {
            "name": request.POST.get("customer_name"),
            "phone": request.POST.get("customer_phone"),
            "email": request.POST.get("customer_email"),
        }
        special_instructions = request.POST.get("instructions")

        # Ready time: random 30–60 minutes from now
        minutes = random.randint(30, 60)
        ready_time = timezone.localtime(timezone.now() + timedelta(minutes=minutes))

        context = {
            "ordered_items": ordered_items,
            "total": f"{total_price:.2f}", # Format total price to 2 decimal places
            "customer": customer,
            "instructions": special_instructions,
            "ready_time": ready_time,
            "minutes": minutes,
        }
        return render(request, template_name, context)

    else:
        return render(request, template_name, {"error": "Please submit an order first."})
