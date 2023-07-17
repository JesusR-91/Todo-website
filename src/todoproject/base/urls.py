from django.urls import path
from .views import PendingList, DetailsTodo, CreateTodo, UpdateTodo, DeleteTodo, Login, Signup
from django.contrib.auth.views import LogoutView

urlpatterns = [path("", PendingList.as_view(), name="todo-list"),
               path("login/", Login.as_view(), name="login"),
               path("signup/", Signup.as_view(), name="signup"),
               path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
               path("todo/<int:pk>", DetailsTodo.as_view(), name="todo"),
               path("create-todo/", CreateTodo.as_view(), name="create-todo"),
               path("update-todo/<int:pk>", UpdateTodo.as_view(), name="update-todo"),
               path("delete-todo/<int:pk>", DeleteTodo.as_view(), name="delete-todo")]
