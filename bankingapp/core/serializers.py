from rest_framework import serializers
from .models import User, BankAccount, DebitCard, Transaction
from django.db import transaction

from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = ['id', 'iban', 'currency', 'balance', 'owner', 'is_approved']
        read_only_fields = ['owner'] 
        

class DebitCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = DebitCard
        fields = ['id', 'account', 'salary','is_approved', 'reject_reason']
        read_only_fields = ['reject_reason', 'is_approved'] 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.context['request'].user

        if user.role == 'BANKER':
            self.fields['is_approved'].read_only = False
            self.fields['reject_reason'].read_only = False
            
        else:
            self.fields['is_approved'].read_only = True
            self.fields['reject_reason'].read_only = True

    def validate(self, data):
        user = self.context['request'].user
        account = data.get('account')
        salary = data.get('salary')

        if self.instance is None and user.role != 'CLIENT':
            raise serializers.ValidationError("Only clients can request debit cards.")

        if self.instance is None:
            if not account.is_approved:
                raise serializers.ValidationError("Account must be approved to request a card.")
            if hasattr(account, 'debitcard'):
                raise serializers.ValidationError("This account already has a debit card.")
            if salary < 500:
                raise serializers.ValidationError("Salary must be at least 500€ to request a debit card.")

        return data

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'bank_account', 'amount', 'currency', 'type']
        read_only_fields = ['type', 'currency']

class TransferSerializer(serializers.Serializer):
    from_iban = serializers.CharField()
    to_iban = serializers.CharField()
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)

    def validate(self, data):
        from_iban = data['from_iban']
        to_iban = data['to_iban']
        amount = data['amount']
        user = self.context['request'].user

        try:
            from_account = BankAccount.objects.get(iban=from_iban)
        except BankAccount.DoesNotExist:
            raise serializers.ValidationError("Sender account not found.")

        try:
            to_account = BankAccount.objects.get(iban=to_iban)
        except BankAccount.DoesNotExist:
            raise serializers.ValidationError("Receiver account not found.")

        if from_account.owner != user:
            raise serializers.ValidationError("You do not own the sender account.")

        if from_account.balance < amount:
            raise serializers.ValidationError("Insufficient balance.")

        debit_card = getattr(from_account, 'debit_card', None)
        if not debit_card or not debit_card.is_approved:
            raise serializers.ValidationError("Sender account must have an approved debit card.")

        data['from_account'] = from_account
        data['to_account'] = to_account
        return data

    def create(self, validated_data):
        from_account = validated_data['from_account']
        to_account = validated_data['to_account']
        amount = validated_data['amount']

        with transaction.atomic():
            
            debit = Transaction.objects.create(
                bank_account=from_account,
                amount=-amount,
                type=Transaction.DEBIT,
            )
            from_account.balance -= amount
            from_account.save()

        
            credit = Transaction.objects.create(
                bank_account=to_account,
                amount=amount,
                type=Transaction.CREDIT,
            )
            to_account.balance += amount
            to_account.save()

        return debit
