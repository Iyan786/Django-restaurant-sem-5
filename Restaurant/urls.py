"""
URL configuration for Restaurant project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from homeapp import views as hv
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/',include('homeapp.urls')),
    path('',hv.SignupPage,name='signup'),
    path('login/',hv.LoginPage,name='login'),
    path('home/',hv.home,name='home'),
     path('about/',hv.about,name='about'),
     path('orders/',hv.orders,name='orders'),
    path('menu/',hv.menu,name='menu'),
    path('productdetail/<int:id>/',hv.productdetail,name='productdetail'),
    path('download-bill/<int:order_id>/', hv.download_bill, name='download_bill'),
     #path('order/',hv.order,name='order'),
     path('book_table/',hv.book_table,name='book_table'), 
     path('contact/',hv.contact,name='contact'),
     path('logout/',hv.LogoutPage,name='logout'),
    # path('user/',hv.user,name="user"),
    path('display_user/',hv.display_user,name='display_user'),
    path('tables/',hv.tables,name='tables'),
    path('aorder/',hv.aorder,name='aorder'),
    path('update_order_status/<int:id>/', hv.update_order_status, name='update_order_status'),
    path('update_table_status/<int:id>/', hv.update_table_status, name='update_table_status'),
    path('add-empty-table/', hv.add_empty_table, name='add_empty_table'),
    path('cancel_order/<int:id>/', hv.cancel_order, name='cancel_order'),
    path('display_category/',hv.display_category,name='display_category'),
    path('display_product/',hv.display_product,name='display_product'),
    path('table_manage/',hv.table_manage,name='table_manage'),
    path('add_category/',hv.add_category,name='add_category'),
    path('add_product/',hv.add_product,name='add_product'),
    path('category_confirm_delete/<int:id>/', hv.cat_delete, name='category_confirm_delete'),
    path('edit_category/<int:id>/', hv.edit_category, name='edit_category'),
    path('product_confirm_delete/<int:id>/', hv.pro_delete, name='product_confirm_delete'),
    path('table_delete/<int:id>/', hv.table_delete, name='table_delete'),
    path('edit_product/<int:id>/', hv.edit_product, name='edit_product'),
     
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)