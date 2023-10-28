from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import Microcredencial

def lista_microcredenciales(request):
    microcredenciales = Microcredencial.objects.all()
    return HttpResponse(', '.join([m.titulo for m in microcredenciales]))

def admin_microcredenciales(request):
    microcredenciales = Microcredencial.objects.all()
    return render(request, 'admin/microcredenciales.html', {'microcredenciales': microcredenciales})

def emitir_microcredencial(request, microcredencial_id):
    # Aquí iría el código para emitir la microcredencial
    return redirect('admin_microcredenciales')