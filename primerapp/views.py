from django.shortcuts import render, redirect
from .models import Usuario
from .forms import UsuarioForm, BusquedaUsuarioForm
from django.http import HttpResponse
from django.contrib import messages

from django.shortcuts import render
from .forms import UsuarioForm

def registro_usuario(request):
    mensaje = None

    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            mensaje = "Usuario creado correctamente"
            form = UsuarioForm() #limpiar form
    else:
        form = UsuarioForm()
    
    return render(request, "registro_usuario.html", {'form': form, 'mensaje': mensaje} )

def buscar_usuario(request):
    usuarios = None
    if request.method == 'POST':
        form = BusquedaUsuarioForm(request.POST)
        if form.is_valid():
            nombre_busqueda = form.cleaned_data['nombre_busqueda']
            usuarios = Usuario.objects.filter(nombre__icontains=nombre_busqueda)
            return render(request, 'buscar_usuario.html', {'form': form, 'usuarios': usuarios})
    else: 
        form = BusquedaUsuarioForm()

    return render(request, 'buscar_usuario.html', {'form': form, 'usuarios': usuarios})

from django.contrib.auth import authenticate, login
from django.contrib import messages

def inicio_sesion(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        contraseña = request.POST.get('contrasena')
        
        try:
            usuario = Usuario.objects.get(nombre=nombre, contraseña=contraseña)
            # Realizar acciones necesarias para el inicio de sesión exitoso
            messages.success(request, 'Sesión iniciada')
            # return redirect('inicio')  # Redirigir a la página de inicio después del inicio de sesión exitoso
        except Usuario.DoesNotExist:
            # Usuario no encontrado en la base de datos o credenciales inválidas
            messages.error(request, 'El usuario no se encuentra registrado')
    
    return render(request, 'inicio_sesion.html')