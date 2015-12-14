from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^algos/$', views.AlgoList.as_view(), name="algo-list"),
    url(r'^algo/(?P<pk>\d+)', views.AlgoDetail.as_view(), name="algo-detail"),
    url(r'^algo/add/', views.AlgoCreate.as_view(), name="algo-create"),
    url(r'^category/(?P<pk>\d+)', views.categoryDetail, name="category-detail"),
    url(r'^implementation/(?P<pk>\d+)', views.ImplementationDetail.as_view(), name="implementation-detail"),
    url(r'^implementation/add/(?P<algo>\d+)', views.ImplementationCreate.as_view(), name="implementation-create"),
]
