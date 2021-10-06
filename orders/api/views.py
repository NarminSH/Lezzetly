from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from django.http.response import Http404, JsonResponse
from orders.api.serializers import OrderListSerializer, OrderSerializer
from rest_framework.generics import GenericAPIView, ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from orders.models import Order



class OrdersAPIView(ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderListSerializer
    lookup_url_kwarg = 'pk'

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OrderSerializer
        return super(OrdersAPIView, self).get_serializer_class()


class OrderAPIView(RetrieveUpdateDestroyAPIView):

    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Order.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return OrderListSerializer     # for swagger file
        return OrderSerializer

    # def get(self, *args, **kwargs):
    #     order = Order.objects.filter(pk=kwargs.get('pk')).first()
    #     if not order:
    #         raise Http404
    #     serializer = OrderListSerializer(
    #         order, context={'request': self.request})
    #     return JsonResponse(data=serializer.data, safe=False)

    # def put(self, *args, **kwargs):
    #     order = Order.objects.filter(pk=kwargs.get('pk')).first()
    #     if not order:
    #         raise Http404
    #     serializer = OrderSerializer(data=self.request.data,
    #                                    instance=order, context={'request': self.request})
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return JsonResponse(data=serializer.data, safe=False)

    # def delete(self, *args, **kwargs):
    #     order = Order.objects.filter(pk=kwargs.get('pk')).first()
    #     if not order:
    #         raise Http404
    #     serializer = OrderSerializer(order)
    #     order.delete()
    #     return JsonResponse(serializer.data, safe=False)

    # def patch(self, *args, **kwargs):
    #     order = Order.objects.filter(pk=kwargs.get('pk')).first()
    #     serializer = OrderSerializer(data=self.request.data, instance=order, 
    #                                 context={'request': self.request}, partial=True) # set partial=True to update a data partially
    #     if serializer.is_valid(raise_exception=True):
    #         serializer.save()
    #         return JsonResponse( data=serializer.data, safe=False)
    #     return JsonResponse( data="Wrong parameters")



class OrderItemAPIView(RetrieveUpdateDestroyAPIView):

    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    lookup_url_kwarg = 'pk'

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return OrderListSerializer
        return super(OrderItemAPIView, self).get_serializer_class()


class OrdersCompleteAPIView(GenericAPIView):
    serializer_class = OrderSerializer

    def get(self, *args, **kwargs):
        order = Order.objects.filter(complete=True).first()
        if not order:
            raise Http404
        serializer = OrderSerializer(
            order, context={'request': self.request})
        return JsonResponse(data=serializer.data, safe=False)

