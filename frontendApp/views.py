from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .backendAccess import BackendAccess

# Create your views here.

def login(request):
    """path("view/login/", views.login, name="LoginView")
       path("", views.login, name="Home")"""

    username = request.session.get("currUser", "")
    if username:
        return HttpResponseRedirect(reverse("frontendApp:TasksView"))

    error = request.session.get("loginError", "")
    context = {"loginError": error}

    if error:
        del request.session["loginError"]

    return render(request, "todoList/login.html", context)

def register(request):
    """path("view/register/", views.register, name="RegisterView"),"""

    username = request.session.get("currUser", "")
    if username:
        return HttpResponseRedirect(reverse("frontendApp:TasksView"))

    error = request.session.get("registerError", "")
    context = {"registerError": error}

    if error:
        del request.session["registerError"]
    return render(request, "todoList/register.html", context)

def tasks(request):
    """path("view/tasks/", views.tasks, name="TasksView")"""

    username = request.session.get("currUser", "")
    if not username:
        return HttpResponseRedirect(reverse("frontendApp:LoginView"))

    (status, msg, data) = BackendAccess.getTasksOf(username)

    context = {}
    if status == 200:
        taskList = data["task"]
        name = data["name"]
        context["taskList"] = taskList
        context["name"] = name
    else:
        return HttpResponseRedirect(reverse("frontendApp:ErrorView") + "?status={0}&desc={1}&msg={2}".format(status, msg, data["Error"]))

    return render(request, "todoList/tasks.html", context)

def error(request):
    """path("view/error/", views.error, name="ErrorView")"""

    status = request.GET.get("status")
    desc = request.GET.get("desc")
    msg = request.GET.get("msg")
    context = {"status": status, "desc": desc, "msg": msg}
    return render(request, "todoList/error.html", context)
