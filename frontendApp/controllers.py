from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from .backendAccess import BackendAccess

class TaskControllers:
    @classmethod
    def newTask(self, request):
        """path("controller/newTask/", controllers.TaskControllers.newTask, name="NewTaskController")"""

        requiredMethod = "POST"
        if request.method != requiredMethod:
            return HttpResponseRedirect(reverse("frontendApp:ErrorView") + Utils.get405params(requiredMethod))

        username = request.session.get("currUser")
        taskText = request.POST.get("taskText")

        responseInfo = (200, "OK", "")
        if taskText:
            responseInfo = BackendAccess.addNewTask(username, taskText)

        return Utils.errorCheckRedirect(reverse("frontendApp:TasksView"), responseInfo)

    @classmethod
    def deleteTask(self, request):
        """path("controller/deleteTask/", controllers.TaskControllers.deleteTask, name="DeleteTaskController")"""

        requiredMethod = "POST"
        if request.method != requiredMethod:
            return HttpResponseRedirect(reverse("frontendApp:ErrorView") + Utils.get405params(requiredMethod))

        username = request.session.get("currUser")
        taskText = request.POST.get("taskText")

        responseInfo = BackendAccess.deleteTask(username, taskText)

        return Utils.errorCheckRedirect(reverse("frontendApp:TasksView"), responseInfo)

class AccountControllers:
    @classmethod
    def login(self, request):
        """path("controller/login/", controllers.AccountControllers.login, name="LoginController")"""

        requiredMethod = "POST"
        if request.method != requiredMethod:
            return HttpResponseRedirect(reverse("frontendApp:ErrorView") + Utils.get405params(requiredMethod))

        username = request.POST.get("username")
        password = request.POST.get("password")

        (status, desc, data) = BackendAccess.authenticate(username, password)

        if status == 200:
            request.session["currUser"] = username
        elif status == 401:
            request.session["loginError"] = "Wrong username or password"

        return Utils.errorCheckRedirect(reverse("frontendApp:TasksView"), resInfo = (status, desc, data))

    @classmethod
    def register(self, request):
        """path("controller/register/", controllers.AccountControllers.register, name="RegisterController"),"""

        requiredMethod = "POST"
        if request.method != requiredMethod:
            return HttpResponseRedirect(reverse("frontendApp:ErrorView") + Utils.get405params(requiredMethod))

        cancel = request.POST.get("cancel")
        if cancel:
            return HttpResponseRedirect(reverse("frontendApp:LoginView"))

        password = request.POST.get("password")
        confirmPassword = request.POST.get("confirmPassword")

        if password != confirmPassword:
            request.session["registerError"] = "Mismatched passwords"
            return HttpResponseRedirect(reverse("frontendApp:RegisterView"))

        name = request.POST.get("name")
        username = request.POST.get("username")

        (status, desc, data) = BackendAccess.register(name, username, password)

        if status == 200:
            request.session["currUser"] = username
        elif status == 409:
            request.session["registerError"] = "Please choose another username"
            return HttpResponseRedirect(reverse("frontendApp:RegisterView"))

        return Utils.errorCheckRedirect(reverse("frontendApp:TasksView"), resInfo = (status, desc, data))

    @classmethod
    def logout(self, request):
        """path("controller/logout/", controllers.AccountControllers.logout, name="LogoutController")"""

        requiredMethod = "POST"
        if request.method != requiredMethod:
            return HttpResponseRedirect(reverse("frontendApp:ErrorView") + Utils.get405params(requiredMethod))

        del request.session["currUser"]

        return HttpResponseRedirect(reverse("frontendApp:LoginView"))

class UpdateAPI:
    @classmethod
    def backendServerUpdate(self, request):
        """Should be called when a backend server becomes active"""

        if request.method != "post":
            return JsonResponse({"Error": "Only POST is allowed"}, status=405)

        data = json.loads(request.body)

        try:
            backendServerIP = data["backendServerIP"]
            protocol = data["protocol"]
            port = data["port"]
        except KeyError as e:
            return JsonResponse({"Error": "Missing server infos"}, status=404)

        BackendAccess.updateInfo(backendServerIP, port, protocol)
        return JsonResponse({"Message": "Successfully created account"}, status=200)

class Utils:
    @staticmethod
    def get405params(requiredMethod):
        return "?status={0}&desc={1}&msg={2}".format(405, "Method not allowed", "only {0} is allowed".format(requiredMethod))

    @staticmethod
    def errorCheckRedirect(url, resInfo):
        (status, desc, data) = resInfo
        if status < 400:
            return HttpResponseRedirect(url)
        else:
            return HttpResponseRedirect(reverse("frontendApp:ErrorView") + "?status={0}&desc={1}&msg={2}".format(status, desc, data["Error"]))
