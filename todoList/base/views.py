from django.shortcuts import render, HttpResponse, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from base.models import Task
# from transformers import pipeline



# def foo():
#     summarizer = pipeline("summarization")
#
#     text = [
#         "My name is Karibay Sanzhar. I am 18 years old. I am from pavlodar. I am future data scientist. I have a family. My mom's name is Aisulu and sister's Assem."]
#     ARTICLE = ' '.join(text)
#
#     max_chunk = 500
#     ARTICLE = ARTICLE.replace('.', '.<eos>')
#     ARTICLE = ARTICLE.replace('?', '?<eos>')
#     ARTICLE = ARTICLE.replace('!', '!<eos>')
#
#     sentences = ARTICLE.split('<eos>')
#     current_chunk = 0
#     chunks = []
#     for sentence in sentences:
#         if len(chunks) == current_chunk + 1:
#             if len(chunks[current_chunk]) + len(sentence.split(' ')) <= max_chunk:
#                 chunks[current_chunk].extend(sentence.split(' '))
#             else:
#                 current_chunk += 1
#                 chunks.append(sentence.split(' '))
#         else:
#             print(current_chunk)
#             chunks.append(sentence.split(' '))
#
#     for chunk_id in range(len(chunks)):
#         chunks[chunk_id] = ' '.join(chunks[chunk_id])
#
#     res = summarizer(chunks, max_length=120, min_length=30, do_sample=False)
#     text = ' '.join([summ['summary_text'] for summ in res])
#     print(text)


def test():
    return HttpResponse("Hello World")

# --------------------------------------------------
class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')


class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')

        return super(RegisterPage,self).get(*args, **kwargs)


class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__startswith=search_input)

        context['search_input'] = search_input
        return context


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task.html'


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')


class DeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')




