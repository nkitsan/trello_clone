from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from tasker.models import User
from tasker.libs.apis import (habit,
                              event,
                              public_task,
                              private_task,
                              list)
from tasker.libs.managers import (user_manager,
                                  weekly_task_manager,
                                  public_task_manager,
                                  habit_tracker_manager)
from tasker.libs.helpers import (task_helper,
                                 schedule_helper,
                                 remembers_helper)


def login(request):
    if request.session.get('username') is not None:
        return redirect('/profiles/{}'.format(request.session.get('username')))
    elif request.method == "GET":
        username = request.GET.get('username')
        password = request.GET.get('password')
        if username is not None and request is not None and user_manager.login_user(username, password):
            request.session['username'] = username
            return redirect('/profiles/{}'.format(username))
        else:
            return render(request, 'tasker/login.html')
    else:
        return render(request, 'tasker/login.html')


def signup(request):
    if request.session.get('username') is not None:
        return redirect('/profiles/{}'.format(request.session.get('username')))
    elif request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if user_manager.signup_user(username, email, password):
            request.session['username'] = username
            return redirect('/profiles/{}'.format(username))
    else:
        return render(request, 'tasker/signup.html')


@csrf_exempt
def logout(request):
    try:
        del request.session['username']
    except KeyError:
        pass
    return redirect('/signup')


@csrf_exempt
def user_board(request, username):
    user = User.objects.get(username=username)
    schedule_helper.check_updates(username)
    return render(request, 'tasker/index.html', {'api_key': user.api_key,
                                                 'tasks': user.week_list.all(),
                                                 'lists': user.lists.all(),
                                                 'public_tasks': task_helper.tasks_to_dict(username),
                                                 'username': username})


@csrf_exempt
def habit_api(request, api, habit_id):
    if not User.objects.filter(api_key=api).exists():
        return JsonResponse({'error': 'wrong api key'})
    username = user_manager.get_username(api)
    schedule_helper.check_updates(username)
    if request.method == 'GET':
        return JsonResponse(habit.get_habit(api, habit_id))
    if request.method == 'PUT':
        habit_name = request.PUT.get('habit_name')
        habit_status = request.PUT.get('habit_status')
        habit_timeline = request.PUT.get('habit_timeline')
        return JsonResponse(habit.put_habit(api, habit_id, habit_name, habit_status, habit_timeline))


@csrf_exempt
def event_api(request, api, event_id):
    if not User.objects.filter(api_key=api).exists():
        return JsonResponse({'error': 'wrong api key'})
    if request.method == 'GET':
        return JsonResponse(event.get_event(api, event_id))
    if request.method == 'POST':
        comment = request.POST.get('comment')
        remember = request.POST.get('remember')
        return JsonResponse(event.post_event_params(api, event_id, comment, remember))
    if request.method == 'PUT':
        event_date = request.PUT.get('event_date')
        event_name = request.PUT.get('event_name')
        return JsonResponse(event.put_event(api, event_id, event_name, event_date))
    if request.method == 'DELETE':
        comment_id = request.DELETE.get('comment_id')
        remember_id = request.DELETE.get('remember_id')
        return JsonResponse(event.delete_event_params(api, event_id, comment_id, remember_id))


@csrf_exempt
def private_task_api(request, api, task_id):
    if not User.objects.filter(api_key=api).exists():
        return JsonResponse({'error': 'wrong api key'})
    username = user_manager.get_username(api)
    schedule_helper.check_updates(username)
    if request.method == 'GET':
        return JsonResponse(private_task.get_task(api, task_id))
    if request.method == 'POST':
        repeat = request.POST.get('repeat')
        remember = request.POST.get('remember')
        subtask = request.POST.get('subtask')
        comment = request.POST.get('comment')
        return JsonResponse(private_task.post_task_params(api, task_id, repeat, remember, subtask, comment))
    if request.method == 'PUT':
        task_name = request.PUT.get('task_name')
        task_status = request.PUT.get('task_status')
        task_deadline = request.PUT.get('task_deadline')
        subtask_id = request.PUT.get('subtask_id')
        subtask_status = request.PUT.get('subtask_status')
        return JsonResponse(private_task.put_task(api, task_id, task_name, task_status, task_deadline,
                                                  subtask_id, subtask_status))
    if request.method == 'DELETE':
        repeat_id = request.DELETE.get('repeat_id')
        remember_id = request.DELETE.get('remember_id')
        subtask_id = request.DELETE.get('subtask_id')
        comment_id = request.DELETE.get('comment_id')
        return JsonResponse(private_task.delete_task_params(api, task_id, comment_id, subtask_id, repeat_id,
                                                            remember_id))


@csrf_exempt
def public_task_api(request, api, list_id, task_id):
    if not User.objects.filter(api_key=api).exists():
        return JsonResponse({'error': 'wrong api key'})
    if request.method == 'GET':
        return JsonResponse(public_task.get_public_task(api, list_id, task_id))
    if request.method == 'POST':
        subtask = request.POST.get('subtask')
        comment = request.POST.get('comment')
        executor = request.POST.get('executor')
        return JsonResponse(public_task.post_public_task_params(api, list_id, task_id, comment, subtask,
                                                                executor))
    if request.method == 'PUT':
        task_name = request.PUT.get('task_name')
        status = request.PUT.get('task_status')
        deadline = request.PUT.get('task_deadline')
        subtask_id = request.PUT.get('subtask_id')
        subtask_status = request.PUT.get('subtask_status')
        return JsonResponse(public_task.put_public_task(api, list_id, task_id, task_name, status, deadline,
                                                        subtask_id, subtask_status))
    if request.method == 'DELETE':
        subtask_id = request.DELETE.get('subtask_id')
        comment_id = request.DELETE.get('comment_id')
        executor = request.DELETE.get('executor')
        return JsonResponse(public_task.delete_public_task_params(api, list_id, task_id, comment_id, subtask_id,
                                                                  executor))


@csrf_exempt
def list_api(request, api, list_id):
    if not User.objects.filter(api_key=api).exists():
        return JsonResponse({'error': 'wrong api key'})
    if request.method == 'POST':
        new_user = request.POST.get('new_user')
        print(new_user)
        return JsonResponse(list.post_list_params(api, list_id, new_user))
    if request.method == 'PUT':
        list_name = request.PUT.get('list_name')
        return JsonResponse(list.put_list(api, list_id, list_name))
    if request.method == 'DELETE':
        new_user = request.DELETE.get('new_user')
        return JsonResponse(list.delete_list_params(api, list_id, new_user))


@csrf_exempt
def habits_api(request, api):
    if not User.objects.filter(api_key=api).exists():
        return JsonResponse({'error': 'wrong api key'})
    username = user_manager.get_username(api)
    schedule_helper.check_updates(username)
    if request.method == 'POST':
        habit_name = request.POST.get('habit_name')
        return JsonResponse(habit.post_habit(api, habit_name))
    if request.method == 'GET':
        return JsonResponse(habit.get_habits(api))
    if request.method == 'DELETE':
        habit_id = request.DELETE.get('habit_id')
        return JsonResponse(habit.delete_habit(api, habit_id))


@csrf_exempt
def events_api(request, api):
    if not User.objects.filter(api_key=api).exists():
        return JsonResponse({'error': 'wrong api key'})
    if request.method == 'POST':
        event_name = request.POST.get('event_name')
        event_date = request.POST.get('event_date')
        return JsonResponse(event.post_event(api, event_name, event_date))
    if request.method == 'GET':
        return JsonResponse(event.get_events(api))
    if request.method == 'DELETE':
        event_id = request.DELETE.get('event_id')
        return JsonResponse(event.delete_event(api, event_id))


@csrf_exempt
def private_tasks_api(request, api):
    if not User.objects.filter(api_key=api).exists():
        return JsonResponse({'error': 'wrong api key'})
    username = user_manager.get_username(api)
    schedule_helper.check_updates(username)
    if request.method == 'POST':
        task_name = request.POST.get('task_name')
        return JsonResponse(private_task.post_task(api, task_name))
    if request.method == 'GET':
        return JsonResponse(private_task.get_tasks(api))
    if request.method == 'DELETE':
        task_id = request.DELETE.get('task_id')
        return JsonResponse(private_task.delete_task(api, task_id))


@csrf_exempt
def public_tasks_api(request, api, list_id):
    if not User.objects.filter(api_key=api).exists():
        return JsonResponse({'error': 'wrong api key'})
    if request.method == 'POST':
        task_name = request.POST.get('task_name')
        return JsonResponse(public_task.post_public_tasks(api, list_id, task_name))
    if request.method == 'GET':
        return JsonResponse(public_task.get_public_tasks(api, list_id))
    if request.method == 'DELETE':
        task_id = request.DELETE.get('task_id')
        return JsonResponse(public_task.delete_public_task(api, list_id, task_id))


@csrf_exempt
def lists_api(request, api):
    if not User.objects.filter(api_key=api).exists():
        return JsonResponse({'error': 'wrong api key'})
    if request.method == 'POST':
        list_name = request.POST.get('list_name')
        return JsonResponse(list.post_lists(api, list_name))
    if request.method == 'GET':
        return JsonResponse(list.get_lists(api))
    if request.method == 'DELETE':
        list_id = request.DELETE.get('list_id')
        return JsonResponse(list.delete_list(api, list_id))


def remembers_api(request, api):
    if not User.objects.filter(api_key=api).exists():
        return JsonResponse({'error': 'wrong api key'})
    username = user_manager.get_username(api)
    schedule_helper.check_updates(username)
    if request.method == 'GET':
        remembers_events = event.check_remembers(api)
        remembers_tasks = private_task.check_remembers(api)
        return JsonResponse({'events': remembers_events, 'tasks': remembers_tasks})


@csrf_exempt
def task_info(request, username, task_id):
    task = weekly_task_manager.find_user_task(username, task_id)
    return render(request, 'tasker/task.html', {'name': task.task.name,
                                                'deadline': ' '.join(str(task.task.deadline)[0:-9].split('T')),
                                                'subtasks': task.task.subtasks.all(),
                                                'status': task.task.status,
                                                'task_id': task_id,
                                                'comments': task.task.comments.all(),
                                                'remembers': task.remember.all(),
                                                'repeats': task_helper.task_repeats(username, task_id),
                                                'username': username})


@csrf_exempt
def create_task(request, username):
    task_name = request.POST.get('title')
    if request.method == 'POST' and request.session.get('username') == username and task_name != '':
        weekly_task_manager.add_weeklytask(username, task_name)
    return redirect('/profiles/{}'.format(username))


@csrf_exempt
def change_task(request, username, task_id):
    if request.method == 'GET' and request.session.get('username') == username:
        task = weekly_task_manager.find_user_task(username, task_id)
        return render(request, 'tasker/task_change.html', {'username': username,
                                                           'task_id': task_id,
                                                           'task_name': task.task.name})
    if request.method == 'POST' and request.session.get('username') == username:
        name = request.POST.get('title')
        date = request.POST.get('date')
        time = request.POST.get('time')
        status = request.POST.get('status')
        if name != '':
            weekly_task_manager.change_weeklytask_name(username, task_id, name)
        if date != '':
            if time == '':
                time = "00:00"
            deadline = date + ' ' + time
            weekly_task_manager.change_weeklytask_deadline(username, task_id, deadline)
        if status != '':
            weekly_task_manager.change_weeklytask_status(username, task_id, status)
    return redirect('/profiles/{}/tasks/{}'.format(username, task_id))


@csrf_exempt
def delete_task(request, username, task_id):
    if request.method == 'POST' and request.session.get('username') == username:
        weekly_task_manager.delete_weeklytask(username, task_id)
    return redirect('/profiles/{}'.format(username))


@csrf_exempt
def add_subtask(request, username, task_id):
    subtask_name = request.POST.get('title')
    if request.method == 'POST' and request.session.get('username') == username and subtask_name != '':
        weekly_task_manager.add_weeklytask_subtask(username, task_id, subtask_name)
    return redirect('/profiles/{}/tasks/{}'.format(username, task_id))


@csrf_exempt
def change_subtask(request, username, task_id, subtask_id):
    subtask_status = request.POST.get('subtask_status')
    if request.method == 'POST' and request.session.get('username') == username:
        if subtask_status is None:
            weekly_task_manager.change_weeklytask_subtask_status(username, task_id, subtask_id, 'NS')
        else:
            weekly_task_manager.change_weeklytask_subtask_status(username, task_id, subtask_id, 'F')
    return redirect('/profiles/{}/tasks/{}'.format(username, task_id))


@csrf_exempt
def delete_subtask(request, username, task_id, subtask_id):
    if request.method == 'POST' and request.session.get('username') == username:
        weekly_task_manager.delete_weeklytask_subtask(username, task_id, subtask_id)
    return redirect('/profiles/{}/tasks/{}'.format(username, task_id))


@csrf_exempt
def add_comment(request, username, task_id):
    comment = request.POST.get('text')
    if request.method == 'POST' and request.session.get('username') == username and comment != '':
        weekly_task_manager.add_weeklytask_comment(username, task_id, comment)
    return redirect('/profiles/{}/tasks/{}'.format(username, task_id))


@csrf_exempt
def delete_comment(request, username, task_id, comment_id):
    if request.method == 'POST' and request.session.get('username') == username:
        weekly_task_manager.delete_weeklytask_comment(username, task_id, comment_id)
    return redirect('/profiles/{}/tasks/{}'.format(username, task_id))


@csrf_exempt
def add_remember(request, username, task_id):
    if request.method == 'POST' and request.session.get('username') == username:
        date = request.POST.get('date')
        time = request.POST.get('time')
        print(time)
        print(date)
        if date != '':
            if time == '':
                time = '00:00'
            remember = date + ' ' + time
            weekly_task_manager.add_weeklytask_remember(username, task_id, remember)
    return redirect('/profiles/{}/tasks/{}'.format(username, task_id))


@csrf_exempt
def delete_remember(request, username, task_id, remember_id):
    if request.method == 'POST' and request.session.get('username') == username:
        weekly_task_manager.delete_weeklytask_remember(username, task_id, remember_id)
    return redirect('/profiles/{}/tasks/{}'.format(username, task_id))


@csrf_exempt
def add_repeat(request, username, task_id):
    if request.method == 'POST' and request.session.get('username') == username:
        repeat = request.POST.get('repeat')
        if repeat != '':
            weekly_task_manager.add_weeklytask_repeat(username, task_id, repeat)
    return redirect('/profiles/{}/tasks/{}'.format(username, task_id))


@csrf_exempt
def delete_repeat(request, username, task_id, repeat_id):
    if request.method == 'POST' and request.session.get('username') == username:
        weekly_task_manager.delete_weeklytask_repeat(username, task_id, repeat_id)
    return redirect('/profiles/{}/tasks/{}'.format(username, task_id))


@csrf_exempt
def create_list(request, username):
    list_name = request.POST.get('title')
    if request.method == 'POST' and request.session.get('username') == username and list_name != '':
        public_task_manager.create_public_list(username, list_name)
    return redirect('/profiles/{}'.format(username))


@csrf_exempt
def change_list(request, username, list_id):
    if request.method == 'GET' and request.session.get('username') == username:
        public_list = public_task_manager.get_user_list(username, list_id)
        return render(request, 'tasker/list_change.html', {'public_list': public_list, 'username': username})
    if request.method == 'POST' and request.session.get('username') == username:
        title = request.POST.get('title')
        new_user = request.POST.get('new_user')
        if title != '':
            public_task_manager.change_public_list_name(username, list_id, title)
        if new_user != '':
            public_task_manager.add_public_list_user(username, new_user, list_id)
    return redirect('/profiles/{}'.format(username))


@csrf_exempt
def delete_list(request, username, list_id):
    if request.method == 'POST' and request.session.get('username') == username:
        public_task_manager.delete_public_list(username, list_id)
    return redirect('/profiles/{}'.format(username))


@csrf_exempt
def create_public_task(request, username, list_id):
    task_name = request.POST.get('title')
    if request.method == 'POST' and request.session.get('username') == username and task_name != '':
        public_task_manager.create_public_task(username, list_id, task_name)
    return redirect('/profiles/{}'.format(username))


@csrf_exempt
def public_task_info(request, username, list_id, task_id):
    task = public_task_manager.get_list_task(username, list_id, task_id)
    return render(request, 'tasker/public_task.html', {'name': task.task.name,
                                                       'deadline': ' '.join(str(task.task.deadline)[0:-9].split('T')),
                                                       'subtasks': task.task.subtasks.all(),
                                                       'comments': task.task.comments.all(),
                                                       'status': task.task.status,
                                                       'task_id': task_id,
                                                       'list_id': list_id,
                                                       'username': username,
                                                       'executors': task.executors.all()})


@csrf_exempt
def change_public_task(request, username, list_id, task_id):
    if request.method == 'GET' and request.session.get('username') == username:
        task = public_task_manager.get_list_task(username, list_id, task_id)
        public_list = public_task_manager.get_user_list(username, list_id)
        return render(request, 'tasker/public_task_change.html', {'username': username,
                                                                  'list_id': list_id,
                                                                  'task_id': task_id,
                                                                  'public_list': public_list,
                                                                  'task_name': task.task.name})
    if request.method == 'POST' and request.session.get('username') == username:
        name = request.POST.get('title')
        date = request.POST.get('date')
        time = request.POST.get('time')
        status = request.POST.get('status')
        user = request.POST.get('user')
        if name != '':
            public_task_manager.change_public_task_name(username, list_id, task_id, name)
        if date != '':
            if time == '':
                time = "00:00"
            deadline = date + ' ' + time
            public_task_manager.change_public_task_deadline(username, list_id, task_id, deadline)
        if status != '':
            public_task_manager.change_public_task_status(username, list_id, task_id, status)
        if user != '':
            public_task_manager.add_task_executor(username, user, list_id, task_id)
    return redirect('/profiles/{}/lists/{}/tasks/{}'.format(username, list_id, task_id))


@csrf_exempt
def delete_public_task(request, username, list_id, task_id):
    if request.method == 'POST' and request.session.get('username') == username:
        public_task_manager.delete_public_task(username, list_id, task_id)
    return redirect('/profiles/{}'.format(username))


@csrf_exempt
def add_public_subtask(request, username, list_id, task_id):
    subtask_name = request.POST.get('title')
    if request.method == 'POST' and request.session.get('username') == username and subtask_name != '':
        public_task_manager.add_public_task_subtask(username, list_id, task_id, subtask_name)
    return redirect('/profiles/{}/lists/{}/tasks/{}'.format(username, list_id, task_id))


@csrf_exempt
def change_public_subtask(request, username, list_id, task_id, subtask_id):
    subtask_status = request.POST.get('subtask_status')
    if request.method == 'POST' and request.session.get('username') == username:
        if subtask_status is None:
            public_task_manager.change_public_task_subtask_status(username, list_id, task_id, subtask_id, 'NS')
        else:
            public_task_manager.change_public_task_subtask_status(username, list_id, task_id, subtask_id, 'F')
    return redirect('/profiles/{}/lists/{}/tasks/{}'.format(username, list_id, task_id))


@csrf_exempt
def delete_public_subtask(request, username, list_id, task_id, subtask_id):
    if request.method == 'POST' and request.session.get('username') == username:
        public_task_manager.delete_public_task_subtask(username, list_id, task_id, subtask_id)
    return redirect('/profiles/{}/lists/{}/tasks/{}'.format(username, list_id, task_id))


@csrf_exempt
def add_public_comment(request, username, list_id, task_id):
    comment = request.POST.get('text')
    if request.method == 'POST' and request.session.get('username') == username and comment != '':
        public_task_manager.add_public_task_comment(username, list_id, task_id, comment)
    return redirect('/profiles/{}/lists/{}/tasks/{}'.format(username, list_id, task_id))


@csrf_exempt
def delete_public_comment(request, username, list_id, task_id, comment_id):
    if request.method == 'POST' and request.session.get('username') == username:
        public_task_manager.delete_public_task_comment(username, list_id, task_id, comment_id)
    return redirect('/profiles/{}/lists/{}/tasks/{}'.format(username, list_id, task_id))


@csrf_exempt
def delete_task_executor(request, username, list_id, task_id, new_user):
    if request.method == 'POST' and request.session.get('username') == username:
        public_task_manager.delete_task_executor(username, new_user, list_id, task_id)
    return redirect('/profiles/{}/lists/{}/tasks/{}'.format(username, list_id, task_id))


@csrf_exempt
def habits_info(request, username):
    schedule_helper.check_updates(username)
    habits = habit_tracker_manager.get_user_habits(username)
    return render(request, 'tasker/habit_tracker.html', {'habits': habits,
                                                         'username': username})


@csrf_exempt
def add_habit(request, username):
    habit_name = request.POST.get('title')
    if request.method == 'POST' and request.session.get('username') == username and habit_name != '':
        habit_tracker_manager.create_habit(username, habit_name)
    return redirect('/profiles/{}/habits'.format(username))


@csrf_exempt
def change_habit(request, username, habit_id):
    habit_name = request.POST.get('title')
    habit_timeline = request.POST.get('timeline')
    if request.method == 'GET' and request.session.get('username') == username:
        habit = habit_tracker_manager.get_user_habit(username, habit_id)
        return render(request, 'tasker/habit_change.html', {'habit': habit,
                                                            'username': username})
    if request.method == 'POST' and request.session.get('username') == username:
        habit = habit_tracker_manager.get_user_habit(username, habit_id)
        if habit_name != '':
            habit_tracker_manager.change_habit_name(username, habit_id, habit_name)
        if habit_timeline != '' and habit_timeline.isdigit() and int(habit_timeline) >= habit.count:
            habit_tracker_manager.change_habit_timeline(username, habit_id, habit_timeline)
    return redirect('/profiles/{}/habits'.format(username))


@csrf_exempt
def delete_habit(request, username, habit_id):
    if request.method == 'POST' and request.session.get('username') == username:
        habit_tracker_manager.delete_habit(username, habit_id)
    return redirect('/profiles/{}/habits'.format(username))


@csrf_exempt
def change_habit_status(request, username, habit_id):
    habit_status = request.POST.get('habit_status')
    if request.method == 'POST' and request.session.get('username') == username:
        if habit_status is None:
            habit_tracker_manager.change_habit_status(username, habit_id, 'NS')
        else:
            habit_tracker_manager.change_habit_status(username, habit_id, 'F')
    return redirect('/profiles/{}/habits'.format(username))


@csrf_exempt
def remember_info(request, username):
    remembers = remembers_helper.check_remembers(username)
    return render(request, 'tasker/remembers.html', {'remembers': remembers,
                                                         'username': username})
