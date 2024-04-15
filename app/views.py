from django.db.models.query import QuerySet
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic 
from .models import Expense, Income, PAYMENT_METHOD
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Sum
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from datetime import timedelta
from django.utils import timezone
from .filters import ExpenseFilter
from .forms import ExpenseFilterForm, IncomeFilterForm


class UserLoginView(LoginView):
    template_name = 'login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('home')
    

class UserSignup(generic.FormView):
    template_name = 'signup.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(UserSignup, self).form_valid(form)
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home')
        else:
            return super(UserSignup, self).get(*args, **kwargs)


class BaseListView(LoginRequiredMixin,generic.ListView):
    model = Expense
    template_name = 'main_detail.html'
    context_object_name = 'main'
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['main'] = context['main'].filter(user=self.request.user)
        
        expense = Expense.objects.filter(user=self.request.user)
        income = Income.objects.filter(user=self.request.user)

        ####################
        today = timezone.now().date()
        start_of_month = timezone.datetime(today.year, today.month, 1)
        end_of_month = timezone.datetime(today.year, today.month, today.day)
        last_month_end = start_of_month - timedelta(days=1)
        last_month_start = timezone.datetime(last_month_end.year, last_month_end.month, 1)
        
        #Total expense
        total_expense = Expense.objects.filter(user=self.request.user).aggregate(total=Sum('expense_amount'))['total'] or 0
        
        #Tottal income
        total_income = Income.objects.filter(user=self.request.user).aggregate(total=Sum('income_amount'))['total'] or 0
        
        #Total balance
        total_balance = total_income - total_expense
        self.request.session['total_balance'] = total_balance

        #Procents
        procecnt_of_income = (total_income * 100) // (total_income + total_balance)

        #Total expense this month
        expense_this_month = expense.filter(expense_date__range=(start_of_month, end_of_month)).aggregate(total=Sum('expense_amount'))['total'] or 0

        #Total expense last month
        expense_last_month = expense.filter(expense_date__range=(last_month_start, last_month_end)).aggregate(total=Sum('expense_amount'))['total'] or 0
        
        #Total income this month
        income_this_month = income.filter(income_date__range=(last_month_start, last_month_end)).aggregate(total=Sum('income_amount'))['total'] or 0

        #Total income last month
        income_last_month = income.filter(income_date__range=(start_of_month, end_of_month)).aggregate(total=Sum('income_amount'))['total'] or 0

        procecnt_of_income = (income_this_month * 100) // (expense_this_month + income_this_month)
        
        #Card Total balance
        card_income = income.filter(income_payment_method='Card').aggregate(total=Sum('income_amount'))['total'] or 0
        card_expense = expense.filter(expense_payment_method='Card').aggregate(total=Sum('expense_amount'))['total'] or 0
        card_balance = card_income - card_expense
        
        #Wallet Total balance
        wallet_income = income.filter(income_payment_method='Cash').aggregate(total=Sum('income_amount'))['total'] or 0
        wallet_expense = expense.filter(expense_payment_method='Cash').aggregate(total=Sum('expense_amount'))['total'] or 0
        wallet_balance = wallet_income - wallet_expense

        #Contexts
        context['expense_this_month'] = expense_this_month
        context['expense_last_month'] = expense_last_month
        context['income_this_month'] = income_this_month
        context['income_last_month'] = income_last_month
        context['total_expense'] = total_expense
        context['total_income'] = total_income
        context['total_balance'] = total_balance
        context['card_balance'] = card_balance
        context['wallet_balance'] = wallet_balance
        context['procent_of_income'] = procecnt_of_income

        return context


class ExpenseListView(LoginRequiredMixin,generic.ListView):
    model = Expense
    filterset_class = ExpenseFilter
    template_name = 'list_expense.html'
    context_object_name = 'expenses'

    def get_queryset(self):

        queryset = super().get_queryset()
        self.filterset = ExpenseFilter(self.request.GET, queryset=queryset)
        
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_expense = Expense.objects.filter(user=self.request.user).aggregate(total=Sum('expense_amount'))['total'] or 0

        context['form'] = self.filterset.form
        context['total_expense'] = total_expense
        context['expenses'] = context['expenses'].filter(user=self.request.user)
        return context
    

def expense_list(request):
    form = ExpenseFilterForm(request.GET)
    expenses = Expense.objects.all()

    if form.is_valid():
        if form.cleaned_data['expense_category']:
            expenses = expenses.filter(expense_category=form.cleaned_data['expense_category'])
        if form.cleaned_data['expense_payment_method']:
            expenses = expenses.filter(expense_payment_method=form.cleaned_data['expense_payment_method'])
        if form.cleaned_data['min_amount']:
            expenses = expenses.filter(expense_amount__gte=form.cleaned_data['min_amount'])
        if form.cleaned_data['max_amount']:
            expenses = expenses.filter(expense_amount__lte=form.cleaned_data['max_amount'])


    return render(request, 'expense_list.html', {'form': form, 'expenses': expenses})


def income_list(request):
    form = IncomeFilterForm(request.GET)
    incomes = Income.objects.all()  # Changed 'expenses' to 'incomes'

    if form.is_valid():
        if form.cleaned_data['income_category']:
            incomes = incomes.filter(income_category=form.cleaned_data['income_category'])  # Changed 'expenses' to 'incomes'
        if form.cleaned_data['income_payment_method']:
            incomes = incomes.filter(income_payment_method=form.cleaned_data['income_payment_method'])  # Changed 'expenses' to 'incomes'
        if form.cleaned_data['min_amount']:
            incomes = incomes.filter(income_amount__gte=form.cleaned_data['min_amount'])
        if form.cleaned_data['max_amount']:
            incomes = incomes.filter(income_amount__lte=form.cleaned_data['max_amount'])

    return render(request, 'income_list.html', {'form': form, 'incomes': incomes})  # Changed 'expenses' to 'incomes', and 'expense_list.html' to 'income_list.html'



class IncomeListView(LoginRequiredMixin, generic.ListView):
    model = Income
    template_name = 'list_income.html'
    context_object_name = 'incomes'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['incomes'] = context['incomes'].filter(user=self.request.user)
        total_income = Income.objects.filter(user=self.request.user).aggregate(total=Sum('income_amount'))['total'] or 0
        context['total_income'] = total_income
        return context
    
    

class ExpenseView(LoginRequiredMixin, generic.CreateView):
    model = Expense
    template_name = 'expense.html'
    fields = ['expense_category', 'expense_amount', 'expense_payment_method', 'expense_date', 'expense_comment']
    success_url = reverse_lazy('show_ex')

    def form_valid(self, form):
        form.instance.user = self.request.user
        total_balance = self.request.session.get('total_balance', 0)
        if form.cleaned_data['expense_amount'] > total_balance:
            form.add_error('expense_amount', 'Sorry! But you dont have enough money!')
            return self.form_invalid(form)

        return super().form_valid(form)


class IncomeView(LoginRequiredMixin, generic.CreateView):
    model = Income
    template_name = 'income.html'
    fields = ['income_category', 'income_amount', 'income_payment_method', 'income_date', 'income_comment']
    success_url = reverse_lazy('show_in')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(IncomeView, self).form_valid(form)


class ExpenseUpdate(LoginRequiredMixin, generic.UpdateView):
    model = Expense
    template_name = 'update_expense.html'
    fields = ['expense_category', 'expense_amount', 'expense_payment_method', 'expense_date', 'expense_comment']
    success_url = reverse_lazy('show_ex')


class IncomeUpdate(LoginRequiredMixin, generic.UpdateView):
    model = Income
    template_name = 'update_income.html'
    fields = ['income_category', 'income_amount', 'income_payment_method', 'income_date', 'income_comment']
    success_url = reverse_lazy('show_in')


class DeleteExpense(LoginRequiredMixin, generic.DeleteView):
    model = Expense
    template_name = 'delete.html'
    success_url = reverse_lazy('show_ex')


class DeleteIncome(LoginRequiredMixin, generic.DeleteView):
    model = Income
    template_name = 'delete.html'
    success_url = reverse_lazy('show_in')