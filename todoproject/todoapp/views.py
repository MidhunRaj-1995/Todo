from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .models import Task
from .forms import  Todoform
from django.views.generic import ListView, DeleteView
from django.views.generic import DetailView
from django.views.generic import UpdateView

# Create your views here.
class TaskListView(ListView):
    model =Task
    template_name = "add.html"
    context_object_name = "task1"

class TaskDetailView(DetailView):
    model =Task
    template_name = "detail.html"
    context_object_name = "task2"

class TakUpdateView(UpdateView):
    model = Task
    template_name ="update_1.html"
    context_object_name= "task"
    fields = ("task","priority","date")

    def get_success_url(self):
        return reverse_lazy("cbvdetail",kwargs={'pk':self.object.id})

class TakDeleteView(DeleteView):
    model = Task
    template_name = "delete.html"
    success_url = reverse_lazy('cbvhome')
def add(request):
    task1 = Task.objects.all()
    if request.method == 'POST':
        task = request.POST.get('task')
        priority = request.POST.get('priority')
        date = request.POST.get('date')
        task = Task(task=task,priority=priority,date=date)
        task.save()
    return render(request,"add.html",{'task1':task1})


def delete(request,task_id):
    task = Task.objects.get(id=task_id)
    if request.method == 'POST':
        task.delete()
        return redirect('/')
    return render(request,"delete.html")

def update(request,task_id):
    task = Task.objects.get(id=task_id)
    f = Todoform(request.POST or None,instance=task)
    if f.is_valid():
        f.save()
        return redirect('/')
    return render(request,"update.html",{'f':f,"task":task})
