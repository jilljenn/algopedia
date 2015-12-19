from django.conf.urls import url
from django.views.generic.base import RedirectView
from . import views

urlpatterns = [
    url(r'^$', RedirectView.as_view(url="algos/", permanent=False), name="index"),
    url(r'^algos/$', views.AlgoList.as_view(), name="algo-list"),
    url(r'^algo/(?P<pk>\d+)', views.AlgoDetail.as_view(), name="algo-detail"),
    url(r'^algo/add/', views.AlgoCreate.as_view(), name="algo-create"),
    url(r'^category/(?P<pk>\d+)', views.categoryDetail, name="category-detail"),
    url(r'^categories/', views.CategoryList.as_view(), name="category-list"),
    url(r'^implementation/(?P<pk>\d+)', views.ImplementationDetail.as_view(), name="implementation-detail"),
    url(r'^implementation/add/(?P<algo>\d+)', views.ImplementationCreate.as_view(), name="implementation-create"),
    url(r'^implementation/diff/(?P<pk1>\d+)/(?P<pk2>\d+)', views.implementationDiff, name="implementation-diff"),
    url(r'^implementation/edit/(?P<pk>\d+)', views.ImplementationEdit.as_view(), name='implementation-edit'),

    url(r'^user/stars/', views.UserStars.as_view(), name='user-stars'),

    url(r'^ajax/implementation/(?P<pk>\d+)', views.ajaxImplementationDetail),
]
