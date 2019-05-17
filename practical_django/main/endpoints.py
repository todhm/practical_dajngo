from django.contrib.auth import get_user_model,authenticate
from rest_framework import serializers,viewsets
from rest_framework.decorators import (
    api_view,
    permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import TokenAuthentication
from rest_framework.settings import api_settings
from django.utils.translation import ugettext_lazy as _

from . import models 




class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')
        data = {"email":email,'password':password}
        user = authenticate(
            request=self.context.get('request'),
            email=email,
            password=password
        )

        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs

class OrderLineSerializer(serializers.HyperlinkedModelSerializer):
    product = serializers.StringRelatedField()

    class Meta: 
        model = models.OrderLine 
        fields = ('id','order','product','status')
        read_only_fields = ('id','order','product','status')

class PaidOrderLineViewSet(viewsets.ModelViewSet):
    queryset = models.OrderLine.objects.filter(order__status = models.Order.PAID).order_by('-order__date_added')
    serializer_class = OrderLineSerializer 
    filter_fields = ('order','status')

class OrderSerializer(serializers.HyperlinkedModelSerializer):

    class Meta: 
        model = models.Order
        fields = (
            "shipping_name",'shipping_address1','shipping_address2','shipping_zip_code','shipping_city','shipping_country','date_updated','date_added',
        )
    
class PaidOrderViewSet(viewsets.ModelViewSet):

    queryset = models.Order.objects.all().filter(
        status=models.Order.PAID
    ).order_by('-date_added')
    serializer_class = OrderSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def perform_create(self,serializer):
        serializer.save(user=self.request.user)

class OrderOrderLineSerializer(serializers.ModelSerializer):

    order = OrderSerializer(many=False)   
    class Meta: 
        model = models.OrderLine 
        fields = ('id','order','product','status')




class OrderOrderLineViewSet(viewsets.ModelViewSet):

    queryset = models.OrderLine.objects.filter(order__status = models.Order.PAID).order_by('-order__date_added')
    serializer_class = OrderOrderLineSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def perform_create(self,serializer):
        total_data = serializer.validated_data
        order_data = total_data.get("order")
        order = models.Order(**order_data,user=self.request.user)
        order.save()
        orderline = models.OrderLine(
            product=total_data["product"],
            status=total_data["status"],
            order=order
        )
        orderline.save()


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for the user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

# Create your views here.

@api_view()
@permission_classes((IsAuthenticated,))
def my_orders(request):
    user = request.user 
    orders = models.Order.objects.filter(user=user).order_by("-date_added")
    data = []
    for order in orders: 
        data.append(
            {
                "id":order.id, 
                "image":order.mobile_thumb_url, 
                "summary":order.summary, 
                "price":order.total_price, 
            }
        )
    return Response(data)