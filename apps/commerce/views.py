from logging import getLogger

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ViewSet
from rest_framework.mixins import ListModelMixin

from apps.commerce.choices import TransactionStatuses
from apps.commerce.exceptions import ProductNotFoundError, InsufficientProductQuantityError, InsufficientFundsError
from apps.commerce.models import Product
from apps.commerce.serializers import ProductListSerializer, TransactionRequestSerializer, TransactionResponseSerializer
from apps.commerce.services import VendingMachineService


logger = getLogger('commerce')


class ProductListView(ListModelMixin, GenericViewSet):
    queryset = Product.objects.filter(quantity__gt=0)
    serializer_class = ProductListSerializer


class TransactionViewSet(ViewSet):
    @action(methods=['post'], detail=False)
    def purchase(self, request, *args, **kwargs):
        serializer = TransactionRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'error': 'Невалидные данные', 'details': serializer.errors},
                      status=status.HTTP_400_BAD_REQUEST
            )
        data = serializer.validated_data
        product_id = data.get('product_id')
        money = data.get('money')
        quantity = data.get('quantity')

        try:
            transaction = VendingMachineService.purchase_product(product_id, quantity, money)
            response_serializer = TransactionResponseSerializer(data=transaction)
            response_serializer.is_valid(raise_exception=True)
            logger.info(f'SUCCESS transaction: {response_serializer}')
            return Response(response_serializer.data)
        except ProductNotFoundError as e:
            return Response({'error': str(e)},
                            status=status.HTTP_404_NOT_FOUND)
        except InsufficientProductQuantityError as e:
            logger.error(f'ERROR: {repr(e)}')
            return Response({'error': str(e),'status': TransactionStatuses.ERROR},
                            status=status.HTTP_400_BAD_REQUEST)
        except InsufficientFundsError as e:
            logger.error(f'ERROR: {repr(e)}')
            return Response({'error': str(e), 'status': TransactionStatuses.ERROR},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({'error': 'Нерпедвиденная ошибка! Просим попробовать позже!'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
