from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

from decimal import Decimal
from .models import Wallet
from .serializers import WalletSerializer


class WalletBalanceView(APIView):
    def get(self, request, wallet_uuid):
        try:
            wallet = Wallet.objects.get(uuid=wallet_uuid)
            serializer = WalletSerializer(wallet)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Wallet.DoesNotExist:
            return Response({'error': 'Wallet not found'}, status=status.HTTP_404_NOT_FOUND)


class WalletOperationView(APIView):
    def post(self, request, wallet_uuid):
        try:
            with transaction.atomic():

                wallet = Wallet.objects.select_for_update().get(uuid=wallet_uuid)

                operation_type = request.data.get('operationType')
                amount = request.data.get('amount')

                if not operation_type or not amount:
                    return Response({"error": "Invalid request data"}, status=status.HTTP_400_BAD_REQUEST)
                if operation_type not in ['DEPOSIT', 'WITHDRAW']:
                    return Response({"error": "Invalid operation type"}, status=status.HTTP_400_BAD_REQUEST)

                try:
                    amount = Decimal(amount)
                    if amount <= 0:
                        raise ValueError
                except ValueError:
                    return Response({"error": "Amount must be a positive number"}, status=status.HTTP_400_BAD_REQUEST)

                if operation_type == 'WITHDRAW' and wallet.balance < amount:
                    return Response({"error": "Insufficient funds"}, status=status.HTTP_400_BAD_REQUEST)

                if operation_type == 'DEPOSIT':
                    wallet.balance += amount
                elif operation_type == 'WITHDRAW':
                    wallet.balance -= amount

                wallet.save()
            return Response({"message": "Operation successful", "new_balance": wallet.balance}, status=status.HTTP_200_OK)
        except Wallet.DoesNotExist:
            return Response({'error': 'Wallet not found'}, status=status.HTTP_404_NOT_FOUND)



