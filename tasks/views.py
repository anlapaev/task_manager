from django.shortcuts import render, get_object_or_404, redirect
from .models import Task
from .forms import TaskForm

from django.contrib.auth.decorators import login_required


@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)

    status_filter = request.GET.get('status')
    priority_filter = request.GET.get('priority')
    sort_by = request.GET.get('sort_by')

    if status_filter and status_filter in dict(Task.STATUS_CHOICES).keys():
        tasks = tasks.filter(status=status_filter)

    if priority_filter and priority_filter in dict(Task.PRIORITY_CHOICES).keys():
        tasks = tasks.filter(priority=priority_filter)

    if sort_by and sort_by in ['due_date', 'priority']:
        tasks = tasks.order_by(sort_by)

    return render(request, 'tasks/task_list.html', {'tasks': tasks})


@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, "tasks/task_detail.html", {"task": task})


@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('task_list')
        else:
            print(form.errors)  # Вывод ошибок формы в консоль
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form})



@login_required
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("task_list")
    else:
        form = TaskForm(instance=task)
    return render(request, "tasks/task_form.html", {"form": form})


@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        task.delete()
        return redirect("task_list")
    return render(request, "tasks/task_confirm_delete.html", {"task": task})
