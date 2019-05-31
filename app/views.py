from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ExpenseRequestForm


Employee = get_user_model()


def show_emp_points(request, pk):
    query = request.GET.get('name')
    if query:
        result = get_object_or_404(Employee, pk=pk)
        return render(request, 'app/points.html', {'result': result})
    return render(request, 'app/emp_profile.html')


@login_required
def show_my_points(request):
    points = request.user.points
    return render(request, 'app/my_points.html', {'points': points})


@login_required
def make_expense_request(request):
    if request.method == 'POST':
        form = ExpenseRequestForm(request.POST)
        if form.is_valid():
            exp_req = form.save(commit=False)
            exp_req.is_approved = False
            exp_req.save()
            return redirect('app:my_expense_requests')
    else:
        form = ExpenseRequestForm()
    return render(request, 'app/expense_request_form.html', {'form': form})
