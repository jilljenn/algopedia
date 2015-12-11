from django.conf.urls import url
from algopedia.views import AlgoList, AlgoDetail, AlgoCreate

urlpatterns = [
    url(r'^algos/$', AlgoList.as_view(), name="algo-list"),
    url(r'^algo/(?P<pk>\d+)', AlgoDetail.as_view(), name="algo-detail"),
    url(r'^algos/add/', AlgoCreate.as_view(), name="algo-create")
]
