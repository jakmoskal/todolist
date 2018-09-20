from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.contrib import messages

from todolist_panel.forms import TodoListForm, TodoItemForm
from todolist_panel.models import TodoList, TodoItem


def index(request):
    return render(request, 'index.html', {
        'current_site': 'index'
    })


def about(request):
    return render(request, 'todolist_panel/about.html', {
        'current_site': 'about'
    })


@login_required
def todo_list(request):
    return render(request, 'todolist_panel/todo_list.html', {
        'current_site': 'todo',
        'todo_lists': TodoList.objects.filter(owner=request.user).order_by('name'),
        'add_todo_list_form': TodoListForm()
    })


@login_required
def todo_list_add(request):
    if request.method == 'POST':
        form = TodoListForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            messages.add_message(request, messages.INFO, 'Changed list description successfully')
            return redirect('panel:todo_list_view', form.instance.id)
    else:
        form = TodoListForm()

    return render(request, 'todolist_panel/todo_list_add.html', {
        'current_site': 'todo',
        'form': form
    })


@login_required
def todo_list_edit(request, id):
    obj = TodoList.objects.get(pk=id, owner=request.user)
    if request.method == 'POST':
        form = TodoListForm(request.POST, instance=obj)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()

            return redirect('panel:todo_list_view', obj.id)
    else:
        form = TodoListForm(instance=obj)

    return render(request, 'todolist_panel/todo_list_edit.html', {
        'current_site': 'todo',
        'form': form
    })


@login_required
def todo_list_view(request, id):
    obj = TodoList.objects.get(pk=id, owner=request.user)
    if obj is None:
        raise Http404()
    return render(request, 'todolist_panel/todo_list_view.html', {
        'current_site': 'todo',
        'todo': obj,
        'add_todo_item_form': TodoItemForm()
    })


@login_required
@require_POST
def todo_list_delete(request, id):
    obj = TodoList.objects.get(pk=id, owner=request.user)
    obj.delete()
    messages.add_message(request, messages.INFO, 'Removed list "%s"' % obj.name)
    return redirect('panel:todo_list')


@login_required
@require_POST
def todo_item_add(request, parent_id):

    form = TodoItemForm(request.POST)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.todolist = TodoList.objects.get(pk=parent_id)  # mozna podać samo id, ale niech sie waliduje
        obj.save()
        return redirect('panel:todo_list_view', parent_id)

    messages.add_message(request, messages.ERROR, str(form.errors))
    return redirect('panel:todo_list_view', parent_id)

@login_required
@require_POST
def todo_item_finish(request, id):
    obj = TodoItem.objects.select_related('todolist').get(pk=id, todolist__owner=request.user)
    obj.done = True
    obj.save()
    messages.add_message(request, messages.INFO, 'Finished working on "%s"' % obj.name)
    return redirect('panel:todo_list_view', obj.todolist.id)


@login_required
def todo_item_edit(request, id):
    obj = TodoItem.objects.select_related('todolist').get(pk=id, todolist__owner=request.user)
    if request.method == 'POST':
        form = TodoItemForm(data=request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, 'Changed item successfully')
            return redirect('panel:todo_list_view', obj.todolist.id)
    else:
        form = TodoListForm(instance=obj)

    return render(request, 'todolist_panel/todo_item_edit.html', {
        'current_site': 'todo',
        'form': form,
        'parent_id': obj.todolist.id,
        'item_id': obj.id
    })


@login_required
@require_POST
def todo_item_delete(request, id):
    obj = TodoItem.objects.select_related('todolist').get(pk=id, todolist__owner=request.user)
    todo_list = obj.todolist
    if todo_list.items_count == 1:
        todo_list.delete()  # usunie kaskadowo
        messages.add_message(request, messages.INFO, 'Removed item "%s" and whole list (was empty)' % obj.name)
        return redirect('panel:todo_list')

    obj.delete()
    messages.add_message(request, messages.INFO, 'Removed item "%s"' % obj.name)
    return redirect('panel:todo_list_view', todo_list.id)
