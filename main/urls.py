from django.urls import path
from . import views

urlpatterns = [
    path('', views.VlogsGetView.as_view(), name="main"),
    path('post/', views.VlogsPostView.as_view(), name="post-vlogs"),
    path('<int:pk>/', views.VlogsView.as_view(), name="vlog-view"),
    path('<int:pk>/update/', views.VlogsUpdateView.as_view(), name="vlog-update"),
    path('<int:pk>/delete/', views.VlogsDeleteView.as_view(), name="vlog-delete"),
    path('<int:vlog_pk>/image/<int:pk>/', views.VlogImageUpdateDeleteView.as_view(), name="vlog-image-update"),
    path('<int:vlog_pk>/video/<int:pk>/', views.VlogVideoUpdateDeleteView.as_view(), name="vlog-image-update"),
    path('<int:vlog_pk>/document/<int:pk>/', views.VlogDocumentUpdateDeleteView.as_view(), name="vlog-image-update"),
    path('<int:pk>/post-comment/', views.CommentsPostView.as_view(), name='post-comment'),
    path('<int:vlog_id>/update-comment/', views.CommentsUpdateView.as_view(), name="delete-comment"),
    path('<int:vlog_id>/delete-comment/', views.CommentsDeleteView.as_view(), name="delete-comment"),
    path('<int:vlog_id>/like/', views.LikeVlogView.as_view(), name='like-vlog'),
    path('<int:vlog_id>/drop-like/', views.DropLikeView.as_view(), name="drop-like-vog"),
]
