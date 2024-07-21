from django.urls import path
from .views import UserSignUpView, EmailVerifyView, LoginView, UploadFileView, ListFilesView, DownloadFileView, FileDownloadView

urlpatterns = [
    path('signup/', UserSignUpView.as_view(), name='signup'),
    path('verify-email/<uidb64>/<token>/', EmailVerifyView.as_view(), name='verify-email'),
    path('login/', LoginView.as_view(), name='login'),
    path('upload-file/', UploadFileView.as_view(), name='upload-file'),
    path('list-files/', ListFilesView.as_view(), name='list-files'),
    # path('download-file/<int:pk>/', DownloadFileView.as_view(), name='download-file'),
    path('download-link/<int:pk>/', DownloadFileView.as_view(), name='download-link'),
    path('download-file/<str:token>/', FileDownloadView.as_view(), name='download-file'),
]
