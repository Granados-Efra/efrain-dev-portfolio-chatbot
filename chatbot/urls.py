from django.urls import path
from .views import make_question, reset_conversation, health_check

urlpatterns = [
    path('ask/', make_question, name='make_question'),
    path('reset/', reset_conversation, name='reset_conversation'),
]
