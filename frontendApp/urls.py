from django.urls import path

from . import views, controllers

app_name = "frontendApp"
urlpatterns = [
    path("", views.login, name="Home"),
    path("view/login/", views.login, name="LoginView"),
    path("controller/login/", controllers.AccountControllers.login, name="LoginController"),
    path("controller/logout/", controllers.AccountControllers.logout, name="LogoutController"),
    path("view/register/", views.register, name="RegisterView"),
    path("controller/register/", controllers.AccountControllers.register, name="RegisterController"),
    path("view/tasks/", views.tasks, name="TasksView"),
    path("controller/newTask/", controllers.TaskControllers.newTask, name="NewTaskController"),
    path("controller/deleteTask/", controllers.TaskControllers.deleteTask, name="DeleteTaskController"),
    path("view/error/", views.error, name="ErrorView"),
]
