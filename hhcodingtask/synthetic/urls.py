from django.conf.urls import url
from django.urls import path

from . import views

app_name = 'synthetic'

urlpatterns = [
    url(regex=r"^$", view=views.GenericView.as_view(), name="list"),
    url(regex=r"^form/", view=views.GenericFormView.as_view()),
    url(regex=r"^detail/(?P<pk>\d+)/$", view=views.GenericDetailView.as_view(),
        name="detail"),
]
