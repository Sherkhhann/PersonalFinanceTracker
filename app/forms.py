# from django import forms


# class ExpenseForm(forms.Form):
#     expense_category = 
from django import forms
from .models import Expense

class ExpenseFilterForm(forms.Form):
    ExpenseCategory = (
        ('', 'All'),  
        ('Food/Drinks', 'Food/Drinks'),
        ('Clothing', "Clothing"),
        ('Transportation', 'Transportation'),
        ('Entertainment', 'Entertainment'),
        ('Home', 'Home'),
        ('Family', 'Family'),
        ('Sport/Health', 'Sport/Health'),
        ('Pets', 'Pets'),
        ('Subscriptions', 'Subscriptions'),
        ('Bills/Utilities', 'Bills and Utilities'),  # Fixed typo in category name
        ('Education', 'Education'),
        ('Groceries', 'Groceries'),
    )

    expense_category = forms.ChoiceField(choices=ExpenseCategory, required=False)
    expense_payment_method = forms.CharField(max_length=50, required=False)  # Assuming you have defined PAYMENT_METHOD elsewhere
    min_amount = forms.IntegerField(label='Min Amount', required=False)
    max_amount = forms.IntegerField(label='Max Amount', required=False)

    def clean(self):
        cleaned_data = super().clean()
        min_amount = cleaned_data.get('min_amount')
        max_amount = cleaned_data.get('max_amount')

        if min_amount is not None and max_amount is not None:
            if min_amount > max_amount:
                raise forms.ValidationError("Min amount cannot be greater than max amount.")
        return cleaned_data


class IncomeFilterForm(forms.Form):
    IncomeCategory = (
        ('', 'All'),  
        ('Financial income', 'Financial income'),
        ('Income', 'Income'),
        ('Other', 'Other')
    )

    income_category = forms.ChoiceField(choices=IncomeCategory, required=False)
    income_payment_method = forms.CharField(max_length=50, required=False)  # Assuming you have defined PAYMENT_METHOD elsewhere
    min_amount = forms.IntegerField(label='Min Amount', required=False)
    max_amount = forms.IntegerField(label='Max Amount', required=False)

    def clean(self):
        cleaned_data = super().clean()
        min_amount = cleaned_data.get('min_amount')
        max_amount = cleaned_data.get('max_amount')

        if min_amount is not None and max_amount is not None:
            if min_amount > max_amount:
                raise forms.ValidationError("Min amount cannot be greater than max amount.")
        return cleaned_data