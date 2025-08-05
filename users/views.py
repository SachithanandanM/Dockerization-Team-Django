from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate,logout
from django.contrib import messages
from .forms import SignUpForm, SignInForm
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "username": request.user.username,
            "email": request.user.email,
            "first_name": request.user.first_name,
        })


def home(request):
    return render(request, 'home.html')

def custom_logout(request):
    logout(request)
    return redirect('home')  # Redirect to home page after logout

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created successfully! Please sign in.')
            return redirect('home')  # Redirect to home page after signup
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken

def signin(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)  # keeps normal Django login

            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            # Prepare response
            response = JsonResponse({
                "refresh": refresh_token,
                "access": access_token,
                "message": "Login successful"
            })  

            return response
        else:
            return JsonResponse({"error": "Invalid credentials"}, status=400)

    return render(request, "signin.html")

