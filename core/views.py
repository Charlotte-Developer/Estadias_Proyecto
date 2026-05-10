from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def login_view(request):
    # Si el usuario ya inició sesión, lo mandamos directo al dashboard
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        matricula = request.POST.get('matricula')
        password = request.POST.get('password')
        
        # Authenticate verifica en PostgreSQL si los datos coinciden
        user = authenticate(request, matricula=matricula, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Matrícula o contraseña incorrectos.')

    # Si no es POST (es decir, solo entró a la página), le mostramos el HTML del login
    return render(request, 'core/login.html')

def dashboard_view(request):
    # Por ahora solo cargará un HTML vacío, luego le pondremos la lógica del 70%
    return render(request, 'core/dashboard.html')