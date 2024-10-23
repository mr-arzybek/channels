
from django.shortcuts import render, reverse, get_object_or_404, redirect
from django.http import HttpResponseRedirect, JsonResponse
from .models import Room
from .form import RegistrationForm
from django.contrib import messages
from django.contrib.auth import authenticate
from .tokenizator import create_token



def index(request):
    if request.method == "POST":
        name = request.POST.get("name", None)
        if name:
            room = Room.objects.create(name=name, host=request.user)
            print(room.pk)
            return HttpResponseRedirect(reverse("room", kwargs={"pk": room.pk}))
    return render(request, 'chat/create_room.html')


def room(request, pk):
    room: Room = get_object_or_404(Room, pk=pk)
    return render(request, 'chat/room.html', {
        "room": room,
    })


def main(request):
    return render(request, 'chat/index.html')


def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Сохраняем пользователя
            messages.success(request, 'Регистрация прошла успешно!')  # Уведомление об успешной регистрации

            # Перенаправляем на страницу main
            return redirect(reverse('main'))
        else:
            messages.error(request, 'Ошибка регистрации. Пожалуйста, попробуйте снова.')
    else:
        form = RegistrationForm()

    return render(request, 'chat/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Успешная аутентификация, создаем токен
            token = create_token(user.id)
            messages.success(request, 'Вы успешно вошли в систему!')
            # Возвращаем токен клиенту в качестве JSON-ответа
            return JsonResponse(token)
        else:
            messages.error(request, 'Неверное имя пользователя или пароль.')

    return render(request, 'chat/login.html')

def choice(request):
    if request.method == 'POST':
        choice = request.POST.get('choice', None)
        if choice:
            return HttpResponseRedirect(reverse("room", kwargs={"pk": choice}))
    else:  # Можно использовать elif request.method == 'GET':, но else также приемлемо
        rooms = Room.objects.all()  # Получаем все комнаты
        return render(request, 'chat/choice.html', {
            "rooms": rooms,
        })
