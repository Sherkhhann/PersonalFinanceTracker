import django_filters
from .models import Expense, Income

class ExpenseFilter(django_filters.FilterSet):
    class Meta:
        model = Expense
        fields = ['expense_category', 'expense_payment_method', 'expense_date', 'expense_date']


class IncomeFilter(django_filters.FilterSet):
    class Meta:
        model = Income
        fields = ['income_category', 'income_payment_method', 'income_date', 'income_date']