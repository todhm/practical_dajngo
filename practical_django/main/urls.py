from django.urls import path,include
from rest_framework import routers 
from main import endpoints
from django.views.generic.detail import DetailView 
from django.views.generic import TemplateView 
from django.contrib.auth import views as auth_views
from main import views,admin,models,forms
router = routers.DefaultRouter()

router.register(r'orderlines',endpoints.PaidOrderLineViewSet)
router.register(r'orders',endpoints.PaidOrderViewSet)
order_orderline_list = endpoints.OrderOrderLineViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
urlpatterns = [
    path(
        "product/<slug:slug>/",
        DetailView.as_view(model=models.Product),
        name="product",
    ),
    path(
        "products/<slug:tag>/",
        views.ProductListView.as_view(),
        name="products",
    ),
    path(
        "product_image_create/<slug:slug>/",
        views.ProductImageCreateView.as_view(),
        name="product_image_create",
    ),
    path(
        "contact-us/",
        views.ContactUsView.as_view(),
        name="contact_us"
    ),
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name='login.html',
            form_class=forms.AuthenticationForm,
        ),
        name="login"
    ),
    path(
        "signup/",
        views.SignupView.as_view(),
        name="signup"
    ),
    path(
        "about-us/",
        TemplateView.as_view(template_name="about_us.html"),
        name="about_us"
    ),
    path(
        "",
        TemplateView.as_view(template_name="home.html"),
        name="home",
    ),
    path(
        "address/",
        views.AddressListView.as_view(),
        name="address_list",
    ),
    path(
        "address/create/",
        views.AddressCreateView.as_view(),
        name="address_create",
    ),
    path(
        "address/<int:pk>/",
        views.AddressUpdateView.as_view(),
        name="address_update",
    ),
    path(
        "address/<int:pk>/delete/",
        views.AddressDeleteView.as_view(),
        name="address_delete",
    ),
    path(
        "add_to_basket/",
        views.add_to_basket,
        name="add_to_basket",
    ),
    path(
        'basket/',
        views.manage_basket,
        name="basket",   
    ),
    path(
        "order/done/",
        TemplateView.as_view(template_name="order_done.html"),
        name="checkout_done",
    ),
    path(
        "order/address_select/",
        views.AddressSelectionView.as_view(),
        name="address_select",
    ),
    path(
        "order-dashboard/",
        views.OrderView.as_view(),
        name="order_dashboard",
    ),
    path(
        'api/',
        include(router.urls),
    ),
    path(
        'api/order_orderline',
        order_orderline_list,
        name='order_orderline'
    ),
    path(
        'api/token/',
        endpoints.CreateTokenView.as_view(),
        name="token",
    ),
    path(
        "admin/",
        admin.main_admin.urls
    ),
    path(
        "office-admin/",
        admin.central_office_admin.urls
    ),
    path(
        "dispatch-admin/",
        admin.dispatchers_admin.urls
    ),
]