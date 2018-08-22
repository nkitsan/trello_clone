from django.shortcuts import render
from django.shortcuts import redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from tasker.models import User
from tasker.libs.apis import response_habit, response_event, response_public_task, response_private_task, response_list
from tasker.libs.managers import user_manager


def login(request):
    if request.session.get('username') is not None:
        return redirect('/profile/{}/'.format(request.session.get('username')))
    elif request.method == "GET":
        username = request.GET.get('username')
        password = request.GET.get('password')
        if username is not None and request is not None and user_manager.login_user(username, password):
            request.session['username'] = username
            return redirect('/profile/{}/'.format(username))
        else:
            return render(request, 'tasker/login.html')
    else:
        return render(request, 'tasker/login.html')


def signup(request):
    if request.session.get('username') is not None:
        return redirect('/profile/{}/'.format(request.session.get('username')))
    elif request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if user_manager.signup_user(username, email, password):
            request.session['username'] = username
            return redirect('/profile/{}/'.format(username))
    else:
        return render(request, 'tasker/signup.html')


@csrf_exempt
def user_board(request, username):
    user = User.objects.get(username=username)
    return render(request, 'tasker/index.html', {'api_key': user.api_key})


@csrf_exempt
def habit_api(request, api, habit_id):
    if not User.objects.filter(api_key=api).exists():
        return JsonResponse({'error': 'wrong api key'})


@csrf_exempt
def event_api(request, api, event_id):
    if not User.objects.filter(api_key=api).exists():
        return JsonResponse({'error': 'wrong api key'})


def private_task_api(request, api, task_id):
    if not User.objects.filter(api_key=api).exists():
        return JsonResponse({'error': 'wrong api key'})


def public_task_api(request, api, list_id, task_id):
    if not User.objects.filter(api_key=api).exists():
        return JsonResponse({'error': 'wrong api key'})


@csrf_exempt
def list_api(request, api, list_id):
    if not User.objects.filter(api_key=api).exists():
        return JsonResponse({'error': 'wrong api key'})


@csrf_exempt
def habits_api(request, api):
    if not User.objects.filter(api_key=api).exists():
        return JsonResponse({'error': 'wrong api key'})
    if request.method == 'POST':
        habit_name = request.POST.get('habit_name')
        return JsonResponse(response_habit.post_habit(api, habit_name))
    if request.method == 'GET':
        return JsonResponse(response_habit.get_habits(api))


@csrf_exempt
def events_api(request, api):
    if not User.objects.filter(api_key=api).exists():
        return JsonResponse({'error': 'wrong api key'})
    if request.method == 'POST':
        event_name = request.POST.get('event_name')
        event_date = request.POST.get('event_date')
        return JsonResponse(response_event.post_event(api, event_name, event_date))
    if request.method == 'GET':
        return JsonResponse(response_event.get_events(api))


@csrf_exempt
def private_tasks_api(request, api):
    if not User.objects.filter(api_key=api).exists():
        return JsonResponse({'error': 'wrong api key'})
    if request.method == 'POST':
        task_name = request.POST.get('task_name')
        return JsonResponse(response_private_task.post_task(api, task_name))
    if request.method == 'GET':
        return JsonResponse(response_private_task.get_tasks(api))


@csrf_exempt
def public_tasks_api(request, api, list_id):
    if not User.objects.filter(api_key=api).exists():
        return JsonResponse({'error': 'wrong api key'})
    if request.method == 'POST':
        task_name = request.POST.get('task_name')
        return JsonResponse(response_public_task.post_public_tasks(api, list_id, task_name))
    if request.method == 'GET':
        return JsonResponse(response_public_task.get_public_tasks(api, list_id))


@csrf_exempt
def lists_api(request, api):
    if not User.objects.filter(api_key=api).exists():
        return JsonResponse({'error': 'wrong api key'})
    if request.method == 'POST':
        list_name = request.POST.get('list_name')
        return JsonResponse(response_list.post_lists(api, list_name))
    if request.method == 'GET':
        return JsonResponse(response_list.get_lists(api))
