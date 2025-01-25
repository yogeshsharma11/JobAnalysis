from .views import RoleAnalyticsView, JobRoleClusterView , RoleDistributionView,RoleDistributionPerStateView
from django.urls import path


urlpatterns = [
    path('job/roles/', RoleAnalyticsView.as_view(), name='role-analytics'),
    path('job/clusters/', JobRoleClusterView.as_view(), name='cluster-analytics'),
    path('job/roles-distribution/', RoleDistributionView.as_view(), name='roles-distribution'),
    path('job/roles-per-state/', RoleDistributionPerStateView.as_view(), name='roles-per-state'),
]