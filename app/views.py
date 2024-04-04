from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic 
from .models import Expense, Income
from app.formm import LoginForm, SignupForm
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Sum
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login



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
        total_expense = Expense.objects.filter(user=self.request.user).aggregate(total=Sum('expense_amount'))['total'] or 0
        context['total_expense'] = total_expense
        total_income = Income.objects.filter(user=self.request.user).aggregate(total=Sum('income_amount'))['total'] or 0
        context['total_income'] = total_income
        total_balance = total_income - total_expense
        context['total_balance'] = total_balance
        return context


class ExpenseListView(LoginRequiredMixin,generic.ListView):
    model = Expense
    template_name = 'list_expense.html'
    context_object_name = 'expenses'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['expenses'] = context['expenses'].filter(user=self.request.user)
        total_expense = Expense.objects.filter(user=self.request.user).aggregate(total=Sum('expense_amount'))['total'] or 0
        context['total_expense'] = total_expense
        return context


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
        return super(ExpenseView, self).form_valid(form)


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