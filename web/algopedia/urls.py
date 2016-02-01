from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.Index.as_view(), name="index"),
    url(r'^algos/$', views.AlgoList.as_view(), name="algo-list"),
    url(r'^algo/(?P<pk>\d+)', views.AlgoDetail.as_view(), name="algo-detail"),
    #url(r'^algo/add/', views.AlgoCreate.as_view(), name="algo-create"),
    url(r'^algo/edit/(?P<pk>\d+)', views.AlgoEdit.as_view(), name="algo-edit"),
    url(r'^category/(?P<pk>\d+)', views.CategoryDetail.as_view(), name="category-detail"),
    url(r'^categories/', views.CategoryList.as_view(), name="category-list"),
    url(r'^implementation/(?P<pk>\d+)', views.ImplementationDetail.as_view(), name="implementation-detail"),
    url(r'^implementation/add/(?P<algo>\d+)', views.ImplementationCreate.as_view(), name="implementation-create"),
    url(r'^implementation/diff/(?P<pk1>\d+)/(?P<pk2>\d+)', views.ImplementationDiff.as_view(), name="implementation-diff"),
    url(r'^implementation/edit/(?P<pk>\d+)', views.ImplementationEdit.as_view(), name='implementation-edit'),

    url(r'^user/profile/', views.UserProfile.as_view(), name='user-profile'),
    url(r'^user/notebook/$', views.NotebookParams.as_view(), name='user-notebook'),
    url(r'^user/notebook/(?P<format>pdf|tex)/', views.NotebookGen.as_view(), name='user-notebook-gen'),

    url(r'^ajax/implementation/(?P<pk>\d+)', views.ImplementationDetailAjax.as_view()),
    url(r'^ajax/star/(?P<action>add|remove)/(?P<pk>\d+)', views.StarAjax.as_view()),
    url(r'^star/(?P<action>add|remove)/(?P<pk>\d+)', views.StarRedirect.as_view(), name='star-redirect'),
]
