from django import forms

from todolist_panel.models import TodoItem, TodoList


class TodoListForm(forms.ModelForm):
    class Meta:
        model = TodoList
        fields = ('name',)


class TodoItemForm(forms.ModelForm):
    class Meta:
        model = TodoItem
        fields = ('name',)
