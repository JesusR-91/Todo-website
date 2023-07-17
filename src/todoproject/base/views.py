from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Todo


class Login(LoginView):
    template_name = "base/login.html"
    field = "__all__"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("todo-list")


class Signup(FormView):
    template_name = "base/signup.html"
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy("todo-list")

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(Signup, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("todo-list")
        return super(Signup, self).get(*args, ** kwargs)


class PendingList(LoginRequiredMixin, ListView):
    model = Todo
    context_object_name = "todo_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["todo_list"] = context["todo_list"].filter(user=self.request.user)
        context["count"] = context["todo_list"].filter(done=False).count

        found_value = self.request.GET.get("find-area")
        if found_value:
            context["todo_list"] = context["todo_list"].filter(title__icontains=found_value) or ""
        context["found_value"] = found_value or ""

        return context


class DetailsTodo(LoginRequiredMixin, DetailView):
    model = Todo
    context_object_name = "todo"
    template_name = "base/todo.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class CreateTodo(LoginRequiredMixin, CreateView):
    model = Todo
    fields = ["title", "description", "done"]
    success_url = reverse_lazy("todo-list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreateTodo, self).form_valid(form)


class UpdateTodo(LoginRequiredMixin, UpdateView):
    model = Todo
    fields = ["title", "description", "done"]
    success_url = reverse_lazy("todo-list")


class DeleteTodo(DeleteView):
    model = Todo
    context_object_name = "todo"
    success_url = reverse_lazy("todo-list")
