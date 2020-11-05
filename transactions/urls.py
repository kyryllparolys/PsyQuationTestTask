from django.urls import path
from rest_framework.routers import SimpleRouter
from transactions import views

router = SimpleRouter()
router.register(r'transactions', views.TransactionsViewSet, basename='transactions')

urlpatterns = router.urls