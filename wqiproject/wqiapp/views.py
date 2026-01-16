from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.messages import constants as messages
from django.contrib import messages
from django.db import IntegrityError
from .models import WaterData
# Create your views here.
def chemistry(request):
    return render(request,'chemistry.html')


def signin(request):
    if request.method == "POST":
        username = request.POST.get("username")   # username
        password = request.POST.get("password")
        print(username,password)
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("/main")
        else:
            messages.error(request, "inavlid credentials !try again")
            return render(request, "signin.html")

    return render(request, "signin.html")




def signup(request):
    if request.method == 'POST':
        name=request.POST.get('username')  
        email=request.POST.get('email')
        password=request.POST.get('password')
        try:
            user = User.objects.create_user(username=name, email=email, password=password)
            user.save()
            messages.success(request, "Sign up successfull")
        except IntegrityError:
            messages.error(request,"credentials already exixts")
            
    return render(request,'signup.html')

def main(request):
    if request.user.is_anonymous:
        return redirect("/signin")
        
    print("POST DATA:", request.POST)
  
    if request.method == 'POST':
        try:
            ph = float(request.POST.get('ph', 0))
            tds = float(request.POST.get('tds', 0))
            turbidity = float(request.POST.get('turbidity', 0))
            hardness = float(request.POST.get('hardness', 0))
            conductivity = request.POST.get('conductivity')
            conductivity = float(conductivity) if conductivity else None
        except ValueError:
            return render(request, 'main.html', {'error': 'Enter valid numbers'})
          # Save the data with the current user
        WaterData.objects.create(
            user=request.user,
            ph=ph,
            tds=tds,
            turbidity=turbidity,
            hardness=hardness,
            conductivity=conductivity,
            wqi = calculate_wqi(ph, tds, hardness, turbidity, conductivity)
        )
    return render(request,'main.html')

def logoutUser(request):
    logout(request)
    return render(request,"signin.html")



def display_data(request):
    if not request.user.is_authenticated:
        return redirect("/signin")

    data = WaterData.objects.filter(user=request.user).order_by("-created")

    return render(request, "display.html", {"data": data})

from django.shortcuts import redirect
from wqiapp.models import WaterData

def delete_record(request, record_id):
    if request.user.is_anonymous:
        return redirect("/signin")
    
    # Only delete if the record belongs to the logged-in user
    WaterData.objects.filter(id=record_id, user=request.user).delete()
    
    return redirect('/display')  # Redirect back to display page


def about(request):
    return render(request,'about.html')
# -------------------- WQI CALCULATION PYTHON VERSION ---------------------

# BIS / WHO Standard values for drinking water
standards = {
    "pH": 7.0,           # ideal
    "pH_max": 8.5,       # permissible
    "TDS": 500,
    "Hardness": 300,
    "Turbidity": 5,
    "Conductivity": 1500
}

# Weights used in WQI calculation
weights = {
    "pH": 0.22,
    "TDS": 0.28,
    "Hardness": 0.20,
    "Turbidity": 0.20,
    "Conductivity": 0.10
}


# -------------------- Qi FUNCTION --------------------
def compute_qi(measured, ideal, standard_limit):
    return ((measured - ideal) / (standard_limit - ideal)) * 100


# -------------------- MAIN WQI FUNCTION --------------------
def calculate_wqi(ph, tds, hardness, turbidity, conductivity=None):
    # Validate inputs (same as JS)
    if ph is None  or tds is None or hardness is None or turbidity is None:
        return {"error": "Missing required fields"}
    if ph>=14 and ph<0:
        return {"error":"ph out of range!"}
    qi = {}
    wiQi = 0
    sumWi = 0

    # pH
    qi["pH"] = compute_qi(ph, standards["pH"], standards["pH_max"])
    wiQi += qi["pH"] * weights["pH"]
    sumWi += weights["pH"]

    # TDS
    qi["TDS"] = compute_qi(tds, 0, standards["TDS"])
    wiQi += qi["TDS"] * weights["TDS"]
    sumWi += weights["TDS"]

    # Hardness
    qi["Hardness"] = compute_qi(hardness, 0, standards["Hardness"])
    wiQi += qi["Hardness"] * weights["Hardness"]
    sumWi += weights["Hardness"]

    # Turbidity
    qi["Turbidity"] = compute_qi(turbidity, 0, standards["Turbidity"])
    wiQi += qi["Turbidity"] * weights["Turbidity"]
    sumWi += weights["Turbidity"]

    # Conductivity (optional)
    if conductivity is not None and conductivity > 0:
        qi["Conductivity"] = compute_qi(conductivity, 0, standards["Conductivity"])
        wiQi += qi["Conductivity"] * weights["Conductivity"]
        sumWi += weights["Conductivity"]

    # Final WQI
    WQI = round(wiQi / sumWi, 2)
    return WQI



