"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from core.views import protected_view
from django.urls import path
from apps.score.views import ScoreListView, RoundHistoryCreateView
from apps.signals.views import SignalsListView
from rest_framework.routers import DefaultRouter
from apps.signals.views import UnitViewSet, LessonsListView, ULessonViewSet, UUnitViewSet
from apps.user.views import RegisterView, UserReportListView, CustomTokenObtainPairView
from apps.signals.view_d import DiagnosticLessonsView, SubmitResponseView, DiagnosticResponsesView

router = DefaultRouter()
router.register(r'units', UnitViewSet)
router.register(r'lessons', LessonsListView)
router.register(r'my_lesson', ULessonViewSet)
router.register(r'my_unit', UUnitViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('games/', include('apps.games.urls')),
    path('api/protected/', protected_view, name='protected_view'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/scores/', ScoreListView.as_view(), name='score_list'),
    path('api/round-history/', RoundHistoryCreateView.as_view(), name='round_history_create'),
    path('api/signals/', SignalsListView.as_view(), name='signals_list'),
    path('api/', include(router.urls)),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/diagnostic/', DiagnosticLessonsView.as_view(), name='diagnostic_lessons'),
    path('api/submit-response/', SubmitResponseView.as_view(), name='submit_response'),
    path('api/users/reports/', UserReportListView.as_view(), name='user-report-list'),
    path('api/response/', DiagnosticResponsesView.as_view(), name='user-report-list'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)