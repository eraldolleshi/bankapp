from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views import BankerViewSet, ClientViewSet, BankAccountViewSet, DebitCardViewSet, TransactionViewSet, TransferView,UserInfoView
from .views import LogoutView
from rest_framework.authtoken.views import obtain_auth_token


router = DefaultRouter()
router.register('bankers', BankerViewSet, basename='banker')
router.register('clients', ClientViewSet, basename='client')
router.register('bankaccounts', BankAccountViewSet, basename='bankaccount')
router.register('debitcards', DebitCardViewSet, basename='debitcard')
router.register('transactions', TransactionViewSet, basename='transaction')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/login/', obtain_auth_token, name='api_token_auth'),
    path('api/logout/', LogoutView.as_view(), name='api_logout'),
    path('api/transfer/', TransferView.as_view(), name='transfer'),
    path('api/user/', UserInfoView.as_view(), name='user_info'),
]
