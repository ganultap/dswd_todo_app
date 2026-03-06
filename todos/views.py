from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, ListView, TemplateView, UpdateView

from .forms import SignUpForm, TodoForm
from .models import Todo


class LandingView(TemplateView):
    template_name = 'landing.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('todo-list')
        return super().dispatch(request, *args, **kwargs)


class BrandedLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for field in form.fields.values():
            field.widget.attrs.update({'class': 'text-input'})
        form.fields['username'].widget.attrs.update({'placeholder': 'Username'})
        form.fields['password'].widget.attrs.update({'placeholder': 'Password'})
        return form

    def form_valid(self, form):
        messages.success(self.request, 'Welcome back.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Check your username and password and try again.')
        return super().form_invalid(form)


class SignUpView(CreateView):
    template_name = 'registration/signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('todo-list')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('todo-list')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, 'Account created. Start adding your tasks.')
        return response


class TodoListView(LoginRequiredMixin, ListView):
    model = Todo
    template_name = 'todos/todo_list.html'
    context_object_name = 'todos'

    def get_queryset(self):
        queryset = Todo.objects.filter(owner=self.request.user)
        status = self.request.GET.get('status', 'all')
        query = self.request.GET.get('q', '').strip()

        if status == 'open':
            queryset = queryset.filter(is_completed=False)
        elif status == 'done':
            queryset = queryset.filter(is_completed=True)

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            )

        return queryset.order_by('is_completed', 'due_date', '-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        base_queryset = Todo.objects.filter(owner=self.request.user)
        context['status'] = self.request.GET.get('status', 'all')
        context['query'] = self.request.GET.get('q', '').strip()
        context['total_count'] = base_queryset.count()
        context['open_count'] = base_queryset.filter(is_completed=False).count()
        context['done_count'] = base_queryset.filter(is_completed=True).count()
        return context


class TodoCreateView(LoginRequiredMixin, CreateView):
    model = Todo
    form_class = TodoForm
    template_name = 'todos/todo_form.html'
    success_url = reverse_lazy('todo-list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, 'Task created successfully.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Create a new task'
        context['submit_label'] = 'Save task'
        return context


class TodoUpdateView(LoginRequiredMixin, UpdateView):
    model = Todo
    form_class = TodoForm
    template_name = 'todos/todo_form.html'
    success_url = reverse_lazy('todo-list')

    def get_queryset(self):
        return Todo.objects.filter(owner=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Task updated successfully.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Update task'
        context['submit_label'] = 'Save changes'
        return context


class TodoDeleteView(LoginRequiredMixin, DeleteView):
    model = Todo
    template_name = 'todos/todo_confirm_delete.html'
    success_url = reverse_lazy('todo-list')

    def get_queryset(self):
        return Todo.objects.filter(owner=self.request.user)

    def form_valid(self, form):
        title = self.object.title
        response = super().form_valid(form)
        messages.success(self.request, f'"{title}" deleted successfully.')
        return response


class TodoToggleStatusView(LoginRequiredMixin, View):
    def post(self, request, pk):
        todo = get_object_or_404(Todo, pk=pk, owner=request.user)
        todo.is_completed = not todo.is_completed
        todo.save()

        status_label = 'completed' if todo.is_completed else 'marked as open'
        messages.success(request, f'"{todo.title}" {status_label}.')

        next_url = request.POST.get('next')
        if next_url and next_url.startswith('/'):
            return redirect(next_url)
        return redirect('todo-list')


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.info(request, 'You have been logged out.')
    return redirect('landing')
