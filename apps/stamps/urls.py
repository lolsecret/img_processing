from django.urls import path
from .views import DetectStampsView

urlpatterns = [
    path('detect_stamps/', DetectStampsView.as_view(), name='detect_stamps'),
]