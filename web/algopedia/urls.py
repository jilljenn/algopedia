from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^algos/$', views.AlgoList.as_view(), name="algo-list"),
    url(r'^algo/(?P<pk>\d+)', views.AlgoDetail.as_view(), name="algo-detail"),
    url(r'^algos/add/', views.AlgoCreate.as_view(), name="algo-create"),
    url(r'^category/(?P<pk>\d+)/', views.categoryDetail, name="category-detail")
]
