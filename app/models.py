from django.db import models
from enum import Enum
from django.urls import reverse
from django.contrib.auth.models import User
from django_enum_choices.fields import EnumChoiceField
from django.utils import timezone

# Create your models here.


class ExpenseCategory(Enum):
    ENTERTAINMENT = "Enterteinment"
    FOOD = "Food"
    TRANSPORT = "Transport"
    SHOPPING = "Shopping"
    FAMILY = "Family"
    OTHER = "Other"


class IncomeCategory(Enum):
    FINANCE = 'Financial income'
    INCOME = 'Income'
    OTHER = 'Other'


class PaymentMethod(Enum):
    WALLET = "Wallet"
    CARD = "Card"


class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='expenses')
    expense_category = EnumChoiceField(ExpenseCategory)
    expense_amount = models.IntegerField(default=0)
    expense_payment_method = EnumChoiceField(PaymentMethod)
    expense_date = models.DateTimeField(default=timezone.now)
    expense_comment = models.TextField(null=False)


class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='incomes')
    income_category = EnumChoiceField(IncomeCategory)
    income_amount = models.IntegerField(default=0)
    income_payment_method = EnumChoiceField(PaymentMethod)
    income_date = models.DateTimeField(default=timezone.now)
    income_comment = models.TextField(null=False)