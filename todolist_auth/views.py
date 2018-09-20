from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect


password_reset = auth_views.PasswordResetView.as_view(
    template_name='todolist_auth/password_reset_form.html',
    email_template_name = 'todolist_auth/password_reset_email.html',
    subject_template_name = 'todolist_auth/password_reset_subject.txt'
)


def register(request):

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = UserCreationForm()

    return render(request, 'todolist_auth/register.html', {
        'form': form,
        'current_site': 'register'
    })
