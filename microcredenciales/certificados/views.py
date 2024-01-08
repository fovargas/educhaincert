from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import Microcredencial

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import LoginForm

def lista_microcredenciales(request):
    microcredenciales = Microcredencial.objects.all()
    return HttpResponse(', '.join([m.titulo for m in microcredenciales]))

def admin_microcredenciales(request):
    microcredenciales = Microcredencial.objects.all()
    return render(request, 'admin/microcredenciales.html', {'microcredenciales': microcredenciales})

def emitir_microcredencial(request, microcredencial_id):
    # Aquí iría el código para emitir la microcredencial
    return redirect('admin_microcredenciales')

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('lista_microcredenciales')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})