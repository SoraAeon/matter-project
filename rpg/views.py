from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import ActionLog, UserStatus
from .forms import ActionLogForm

@login_required
def dashboard(request):
    return render(request, 'rpg/dashboard.html')

@login_required
def status_view(request):
    status, _ = UserStatus.objects.get_or_create(user=request.user)
    return render(request, 'rpg/status.html', {'status': status})

@login_required
def log_action(request):
    if request.method == 'POST':
        form = ActionLogForm(request.POST)
        if form.is_valid():
            log = form.save(commit=False)
            log.user = request.user
            log.exp = 10  # 仮に10固定（後で拡張できる）
            log.save()

            status = UserStatus.objects.get(user=request.user)
            current_exp = getattr(status, log.parameter, 0)
            setattr(status, log.parameter, current_exp + log.exp)
            status.exp += log.exp
            status.save()

            return redirect('status_view')
    else:
        form = ActionLogForm()

    return render(request, 'rpg/log_action.html', {'form': form})