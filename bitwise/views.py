from django.shortcuts import render
from .forms import NumberForm
from pymongo import MongoClient

def home(request):
    result = None
    warning = None
    form = NumberForm(request.POST or None)

    if request.method == "POST":
        try:
            # Get all 5 inputs
            a = float(request.POST.get("a"))
            b = float(request.POST.get("b"))
            c = float(request.POST.get("c"))
            d = float(request.POST.get("d"))
            e = float(request.POST.get("e"))

            numbers = [a, b, c, d, e]

            # Validation
            if any(n < 0 for n in numbers):
                warning = "Warning: Some numbers are negative."

            avg = sum(numbers) / len(numbers)
            avg_check = "Above 50" if avg > 50 else "50 or Below"
            positive_count = len([n for n in numbers if n > 0])
            bitwise = ["Even" if int(n) & 1 == 0 else "Odd" for n in numbers]
            greater_than_10 = sorted([n for n in numbers if n > 10])

            # MongoDB connection
            client = MongoClient("mongodb://admin:password@172.31.67.166:27017/")
            db = client["mydatabase"]
            col = db["results"]

            # Prepare safe stringified data
            data = {
                "original": [str(n) for n in numbers],
                "sorted": [str(n) for n in greater_than_10],
                "average": str(avg),
                "avg_check": avg_check,
                "positive_count": str(positive_count),
                "bitwise": bitwise
            }
            col.insert_one(data)

            # Send results to template
            result = {
                "original": numbers,
                "sorted": greater_than_10,
                "average": avg,
                "avg_check": avg_check,
                "positive_count": positive_count,
                "bitwise": bitwise
            }

        except ValueError:
            warning = "Please enter valid numeric values only."

    return render(request, "bitwise/home.html", {"form": form, "result": result, "warning": warning})
