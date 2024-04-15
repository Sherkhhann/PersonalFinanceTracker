from django.db import models
from enum import Enum
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime

PAYMENT_METHOD = (
    ('Card', 'Card'),
    ('Cash', 'Cash'),
)

# now = datetime.now()
# local_time = timezone.localtime(now)
# local_date = local_time.date()


class Expense(models.Model):
    ExpenseCategory = (
        ('Food/Drinks', 'Food/Drinks'),
        ('Clothing', "Clothing"),
        ('Transportation', 'Transportation'),
        ('Entertainment', 'Entertainment'),
        ('Home', 'Home'),
        ('Family', 'Family'),
        ('Sport/Health', 'Sport/Health'),
        ('Pets', 'Pets'),
        ('Subscriptions', 'Subscriptions'),
        ('Bills/Utiliets', 'Bills and Utilietes'),
        ('Education', 'Education'),
        ('Groceries', 'Groceries'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='expenses')
    expense_category = models.CharField(max_length=50, choices=ExpenseCategory)
    expense_amount = models.IntegerField(default=0)
    expense_payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD)
    expense_date = models.DateField(default=timezone.now)
    expense_comment = models.TextField(null=False)


class Income(models.Model):
    IncomeCategory = (
        ('Financial income', 'Financial income'),
        ('Income', 'Income'),
        ('Other', 'Other')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='incomes')
    income_category = models.CharField(max_length=50, choices=IncomeCategory)
    income_amount = models.IntegerField(default=0)
    income_payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD)
    income_date = models.DateField(default=timezone.now)
    income_comment = models.TextField(null=False)  