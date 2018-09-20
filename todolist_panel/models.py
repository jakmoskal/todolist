from django.contrib.auth.models import User
from django.db import models


class TodoList(models.Model):
    name = models.CharField(max_length=150)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def items(self):
        return TodoItem.objects.filter(todolist=self).order_by('ordering')

    @property
    def items_count(self):
        return self.items.count()


class TodoItem(models.Model):
    name = models.CharField(max_length=250)
    done = models.BooleanField(default=False)
    ordering = models.PositiveIntegerField(default=1)
    todolist = models.ForeignKey(TodoList, on_delete=models.CASCADE)

    def save(self, **kwargs):
        last_item = TodoItem.objects.filter(todolist=self.todolist).order_by('ordering').last()
        self.ordering = (last_item.ordering if last_item else 0) + 1
        super().save(**kwargs)

    def mark_finished(self):
        self.done = True
        self.save(update_fields=('done',))
