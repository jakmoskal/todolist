from django.urls import path

from todolist_panel import views

app_name = 'todolist_panel'
urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('panel/list/', views.todo_list, name='todo_list'),
    path('panel/list/add', views.todo_list_add, name='todo_list_add'),
    path('panel/list/<int:id>/view/', views.todo_list_view, name='todo_list_view'),
    path('panel/list/<int:id>/delete/', views.todo_list_delete, name='todo_list_delete'),
    path('panel/list/<int:id>/edit/', views.todo_list_edit, name='todo_list_edit'),

    path('panel/item/<int:parent_id>/add/', views.todo_item_add, name='todo_item_add'),
    path('panel/item/<int:id>/edit/', views.todo_item_edit, name='todo_item_edit'),
    path('panel/item/<int:id>/finish/', views.todo_item_finish, name='todo_item_finish'),
    path('panel/item/<int:id>/delete/', views.todo_item_delete, name='todo_item_delete'),
]
