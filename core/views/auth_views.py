from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def login_view(request):
    # Si el usuario ya inició sesión
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        matricula = request.POST.get("matricula")
        password = request.POST.get("password")

        user = authenticate(
            request,
            matricula=matricula,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("dashboard")

        messages.error(request, "La matrícula o la contraseña son incorrectas.")

    return render(request, "core/auth/login.html")


@login_required
def dashboard_view(request):
    """
    Redirige al dashboard correspondiente
    según el rol del usuario.
    """

    if request.user.rol == "ADMIN":
        return render(request, "core/admin/dashboard.html")

    elif request.user.rol == "DOCENTE":
        return render(request, "core/docente/dashboard.html")

    return render(request, "core/alumno/dashboard.html")


@login_required
def logout_view(request):
    logout(request)
    return redirect("login")