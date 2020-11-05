from rest_framework.routers import SimpleRouter
from accounts import views

router = SimpleRouter()
router.register(r'accounts', views.AccountsViewSet, basename='accounts')

urlpatterns = router.urls