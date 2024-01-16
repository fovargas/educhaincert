import subprocess
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import Microcredencial
from .forms import LoginForm

def lista_microcredenciales(request):
    microcredenciales = Microcredencial.objects.all()
    context = {'microcredenciales': microcredenciales}
    return render(request, 'microcredenciales/microcredenciales.html', context)

def admin_microcredenciales(request):
    microcredenciales = Microcredencial.objects.all()
    return render(request, 'admin/microcredenciales.html', {'microcredenciales': microcredenciales})

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

def descargar_archivo(request, id_microcredencial):
    microcredencial = Microcredencial.objects.get(id=id_microcredencial)
    comando = subprocess.run(['ipfs', 'cat', microcredencial.ipfs_hash], stdout=subprocess.PIPE)
    response = HttpResponse(comando.stdout, content_type='application/octet-stream')
    response['Content-Disposition'] = 'attachment; filename="' + microcredencial.ipfs_hash + '.json"'
    return response