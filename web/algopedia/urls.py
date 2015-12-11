from django.conf.urls import url
from algopedia.views import AlgoList, AlgoDetail

urlpatterns = [
    url(r'^algos/', AlgoList.as_view(), name="algos"),
    url(r'^algo/(?P<pk>\d+)', AlgoDetail.as_view(), name="algo")
]
