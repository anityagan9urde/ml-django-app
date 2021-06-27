from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

# Create your views here.
from .models import *
from .forms import LoanForm, CreateUserForm
from .filters import LoanFilter
from .decorators import unauthenticated_user, allowed_users, admin_only


@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name='name')
            user.groups.add(group)

            messages.success(request, 'Account was created for ' + username)

            return redirect('login')

    context = {'form': form}
    return render(request, 'api/register.html', context)


@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username OR password is incorrect')

    context = {}
    return render(request, 'api/login.html', context)


@login_required(login_url='login')
def home(request):
    loan = LoanApplication.objects.all()
    new = loan.filter(status=1).count()
    rejected = loan.filter(status=2).count()
    approved = loan.filter(status=3).count()

    context = {'loans': loan,
               'rejected': rejected,
               'approved': approved}

    return render(request, 'api/dashboard.html', context)


def userPage(request):
    context = {}
    return render(request, 'api/user.html', context)


@login_required(login_url='login')
@admin_only
def loans(request):
    loan = LoanApplication()
    myFilter = LoanFilter(request.GET, queryset=loan)
    orders = myFilter.qs

    context = {'applicants': loan.id, 'loans': loan, 'loan_count': loan.count(),
               'myFilter': myFilter}
    return render(request, 'api/customer.html', context)


@login_required(login_url='login')
@admin_only
def createLoan(request, pk):
    LoanFormSet = inlineformset_factory(LoanApplication, fields=('loans', 'status'), extra=10)
    applicant = LoanApplication.get(id=pk)
    formset = LoanFormSet(queryset=loans.objects.none(), instance=applicant)
    # form = OrderForm(initial={'customer':customer})
    if request.method == 'POST':
        # print('Printing POST:', request.POST)
        form = LoanForm(request.POST)
        formset = LoanFormSet(request.POST, instance=applicant)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {'form': formset}
    return render(request, 'api/order_form.html', context)


@login_required(login_url='login')
@admin_only
def updateInfo(request, pk):
    loan = LoanApplication.objects.get(id=pk)
    form = LoanForm(instance=loan)

    if request.method == 'POST':
        form = LoanForm(request.POST, instance=loan)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'api/order_form.html', context)


@login_required(login_url='login')
@admin_only
def deleteLoan(request, pk):
    loan = LoanApplication.objects.get(id=pk)
    if request.method == "POST":
        loan.delete()
        return redirect('/')

    context = {'item': loan}
    return render(request, 'api/delete.html', context)
