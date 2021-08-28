from django.shortcuts import redirect, render, HttpResponse
from django.contrib import messages
import bcrypt
from main.models import Users


def index(request):
    return render(request, 'index.html')


def signup(request):
    if request.method == 'GET':
        return render(request, 'form_user.html')
    else:
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']
        birth = request.POST['birthday']

        errors = Users.objects.basic_validator(request.POST)

        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/signup')
        else:
            new_user = Users.objects.create(
                name=name,
                email=email,
                password=bcrypt.hashpw(
                    password.encode(), bcrypt.gensalt()).decode(),
                birthday=birth
            )
            request.session['user'] = {
                'id': new_user.id,
                'name': new_user.name,
                'email': new_user.email
            }
            messages.success(request, 'Usuario creado con exito')
            return redirect('/home')


def login(request):
    email = request.POST['email']
    password = request.POST['password']

    try:
        user = Users.objects.get(email=email)
    except Users.DoesNotExist:
        messages.error(request, 'Usuario o contraseña incorrecta')
        return redirect('/signup')

    if not bcrypt.checkpw(password.encode(), user.password.encode()):
        messages.error(request, 'Usuario inexistente o contraseña incorrecta')
        return redirect('/signup')

    request.session['user'] = {
        'id': user.id,
        'name': user.name,
        'email': user.email,
    }
    messages.success(request, f'Hola {user.name}')
    return redirect('/home')

def logout(request):
    try:
        del request.session['user']
    except KeyError:
        messages.error(request,'Ooops algo sucedio')
    return redirect('/signup')
