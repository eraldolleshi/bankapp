from rest_framework import viewsets, permissions
from .models import User, BankAccount, DebitCard, Transaction
from .serializers import UserSerializer, BankAccountSerializer, DebitCardSerializer, TransactionSerializer, TransferSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from core import permission

class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "username": user.username,
            "role": user.role,
        })


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response({"detail": "Logged out."})

class BankerViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, permission.IsAdmin]

    def get_queryset(self):
        return User.objects.filter(role='BANKER')

    def perform_create(self, serializer):
        serializer.save(role='BANKER')

class ClientViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, permission.IsBanker]

    def get_queryset(self):
        return User.objects.filter(role='CLIENT')

    def perform_create(self, serializer):
        serializer.save(role='CLIENT')

class BankAccountViewSet(viewsets.ModelViewSet):
    serializer_class = BankAccountSerializer
    queryset = BankAccount.objects.all()

    def get_permissions(self):
        if self.action in ['create']:
            return [permissions.IsAuthenticated(), permission.IsClient()]
        elif self.action in ['update', 'partial_update']:
            return [permissions.IsAuthenticated(), permission.IsBanker()]
        elif self.action == 'list':
            return [permissions.IsAuthenticated()]
        return super().get_permissions()

    def get_queryset(self):
        user = self.request.user
        if user.role == 'BANKER':
            return BankAccount.objects.all()
        return BankAccount.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        

class DebitCardViewSet(viewsets.ModelViewSet):
    serializer_class = DebitCardSerializer
    queryset = DebitCard.objects.all()

    def get_permissions(self):
        if self.action in ['create']:
            return [permissions.IsAuthenticated(), permission.IsClient()]
        elif self.action in ['update', 'partial_update']:
            return [permissions.IsAuthenticated(), permission.IsBanker()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'BANKER':
           return DebitCard.objects.all()
        elif user.role == 'CLIENT':
           # Return only cards linked to the client's own accounts
           return DebitCard.objects.filter(account__owner=user)
        return DebitCard.objects.none()



class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'CLIENT':
            return Transaction.objects.filter(bank_account__owner=user)
        elif user.role == 'BANKER':
            return Transaction.objects.all()
        return Transaction.objects.none()


class TransferView(APIView):
    permission_classes = [permissions.IsAuthenticated, permission.IsClient]

    def post(self, request):
        serializer = TransferSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        transaction = serializer.save()
        return Response({"detail": "Transfer successful."}, status=status.HTTP_201_CREATED)

