from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', UserLoginView.as_view(), name='login'),
    path('home/', BaseListView.as_view(), name='home'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('signup/', UserSignup.as_view(), name='signup'),
    path('showexpense/', ExpenseListView.as_view(), name='show_ex'),
    path('showincome/', IncomeListView.as_view(), name='show_in'),
    path('createexpense/', ExpenseView.as_view(), name='create_ex'),
    path('createincome/', IncomeView.as_view(), name='create_in'),
    path('updateexpense/<int:pk>/', ExpenseUpdate.as_view(), name='update_ex'),
    path('updateincome/<int:pk>/', IncomeUpdate.as_view(), name='update_in'),
    path('deleteexpense/<int:pk>/', DeleteExpense.as_view(), name='delete_ex'),
    path('deleteincome/<int:pk>/', DeleteIncome.as_view(), name='delete_in'),
    path('search-expense/', expense_list, name='search_expense'),
    path('search-income/', income_list, name='search_income'),
]
