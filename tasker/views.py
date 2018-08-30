from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from tasker.models import User
from tasker.libs.apis import (response_habit,
                              response_event,
                              response_public_task,
                              response_private_task,
                              response_list)
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
    if request.method == 'GET':
        return JsonResponse(response_habit.get_habit(api, habit_id))
    if request.method == 'PUT':
        habit_name = request.PUT.get('habit_name')
        habit_status = request.PUT.get('habit_status')
        habit_timeline = request.PUT.get('habit_timeline')
        return JsonResponse(response_habit.put_habit(api, habit_id, habit_name, habit_status, habit_timeline))


@csrf_exempt
def event_api(request, api, event_id):
    if not User.objects.filter(api_key=api).exists():
        return JsonResponse({'error': 'wrong api key'})
    if request.method == 'GET':
        return JsonResponse(response_event.get_event(api, event_id))
    if request.method == 'POST':
        comment = request.POST.get('comment')
        remember = request.POST.get('remember')
        return JsonResponse(response_event.post_event_params(api, event_id, comment, remember))
    if request.method == 'PUT':
        event_date = request.PUT.get('event_date')
        event_name = request.PUT.get('event_name')
        return JsonResponse(response_event.put_event(api, event_id, event_name, event_date))
    if request.method == 'DELETE':
        comment_id = request.DELETE.get('comment_id')
        remember_id = request.DELETE.get('remember_id')
        return JsonResponse(response_event.delete_event_params(api, event_id, comment_id, remember_id))


@csrf_exempt
def private_task_api(request, api, task_id):
    if not User.objects.filter(api_key=api).exists():
        return JsonResponse({'error': 'wrong api key'})
    if request.method == 'GET':
        return JsonResponse(response_private_task.get_task(api, task_id))
    if request.method == 'POST':
        repeat = request.POST.get('repeat')
        remember = request.POST.get('remember')
        subtask = request.POST.get('subtask')
        comment = request.POST.get('comment')
        return JsonResponse(response_private_task.post_task_params(api, task_id, repeat, remember, subtask, comment))
    if request.method == 'PUT':
        task_name = request.PUT.get('task_name')
        task_status = request.PUT.get('task_status')
        task_deadline = request.PUT.get('task_deadline')
        subtask_id = request.PUT.get('subtask_id')
        subtask_status = request.PUT.get('subtask_status')
        return JsonResponse(response_private_task.put_task(api, task_id, task_name, task_status, task_deadline,
                                                           subtask_id, subtask_status))
    if request.method == 'DELETE':
        repeat_id = request.DELETE.get('repeat_id')
        remember_id = request.DELETE.get('remember_id')
        subtask_id = request.DELETE.get('subtask_id')
        comment_id = request.DELETE.get('comment_id')
        return JsonResponse(response_private_task.delete_task_params(api, task_id, comment_id, subtask_id, repeat_id,
                                                                     remember_id))


@csrf_exempt
def public_task_api(request, api, list_id, task_id):
    if not User.objects.filter(api_key=api).exists():
        return JsonResponse({'error': 'wrong api key'})
    if request.method == 'GET':
        return JsonResponse(response_public_task.get_public_task(api, list_id, task_id))
    if request.method == 'POST':
        subtask = request.POST.get('subtask')
        comment = request.POST.get('comment')
        executor = request.POST.get('executor')
        return JsonResponse(response_public_task.post_public_task_params(api, list_id, task_id, comment, subtask,
                                                                         executor))
    if request.method == 'PUT':
        task_name = request.PUT.get('task_name')
        status = request.PUT.get('task_status')
        deadline = request.PUT.get('task_deadline')
        subtask_id = request.PUT.get('subtask_id')
        subtask_status = request.PUT.get('subtask_status')
        return JsonResponse(response_public_task.put_public_task(api, list_id, task_id, task_name, status, deadline,
                                                                 subtask_id, subtask_status))
    if request.method == 'DELETE':
        subtask_id = request.DELETE.get('subtask_id')
        comment_id = request.DELETE.get('comment_id')
        executor = request.DELETE.get('executor')
        return JsonResponse(response_public_task.delete_public_task_params(api, list_id, task_id, comment_id, subtask_id,
                                                                            executor))


@csrf_exempt
def list_api(request, api, list_id):
    if not User.objects.filter(api_key=api).exists():
        return JsonResponse({'error': 'wrong api key'})
    if request.method == 'POST':
        new_user = request.POST.get('new_user')
        print(new_user)
        return JsonResponse(response_list.post_list_params(api, list_id, new_user))
    if request.method == 'PUT':
        list_name = request.PUT.get('list_name')
        return JsonResponse(response_list.put_list(api, list_id, list_name))
    if request.method == 'DELETE':
        new_user = request.DELETE.get('new_user')
        return JsonResponse(response_list.delete_list_params(api, list_id, new_user))


@csrf_exempt
def habits_api(request, api):
    if not User.objects.filter(api_key=api).exists():
        return JsonResponse({'error': 'wrong api key'})
    if request.method == 'POST':
        habit_name = request.POST.get('habit_name')
        return JsonResponse(response_habit.post_habit(api, habit_name))
    if request.method == 'GET':
        return JsonResponse(response_habit.get_habits(api))
    if request.method == 'DELETE':
        habit_id = request.DELETE.get('habit_id')
        return JsonResponse(response_habit.delete_habit(api, habit_id))


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
    if request.method == 'DELETE':
        event_id = request.DELETE.get('event_id')
        return JsonResponse(response_event.delete_event(api, event_id))


@csrf_exempt
def private_tasks_api(request, api):
    if not User.objects.filter(api_key=api).exists():
        return JsonResponse({'error': 'wrong api key'})
    if request.method == 'POST':
        task_name = request.POST.get('task_name')
        return JsonResponse(response_private_task.post_task(api, task_name))
    if request.method == 'GET':
        return JsonResponse(response_private_task.get_tasks(api))
    if request.method == 'DELETE':
        task_id = request.DELETE.get('task_id')
        return JsonResponse(response_private_task.delete_task(api, task_id))


@csrf_exempt
def public_tasks_api(request, api, list_id):
    if not User.objects.filter(api_key=api).exists():
        return JsonResponse({'error': 'wrong api key'})
    if request.method == 'POST':
        task_name = request.POST.get('task_name')
        return JsonResponse(response_public_task.post_public_tasks(api, list_id, task_name))
    if request.method == 'GET':
        return JsonResponse(response_public_task.get_public_tasks(api, list_id))
    if request.method == 'DELETE':
        task_id = request.DELETE.get('task_id')
        return JsonResponse(response_public_task.delete_public_task(api, list_id, task_id))


@csrf_exempt
def lists_api(request, api):
    if not User.objects.filter(api_key=api).exists():
        return JsonResponse({'error': 'wrong api key'})
    if request.method == 'POST':
        list_name = request.POST.get('list_name')
        return JsonResponse(response_list.post_lists(api, list_name))
    if request.method == 'GET':
        return JsonResponse(response_list.get_lists(api))
    if request.method == 'DELETE':
        list_id = request.DELETE.get('list_id')
        return JsonResponse(response_list.delete_list(api, list_id))
