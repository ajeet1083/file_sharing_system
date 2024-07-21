from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import File, User
from .serializers import UserSerializer, FileSerializer, EmailVerificationSerializer
from django.http import FileResponse
import os
from file_sharing_system.settings import MEDIA_ROOT
from pathlib import Path


class UserSignUpView(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        link = f"http://localhost:8000/verify-email/{uid}/{token}"
        send_mail('Verify your email', f'Click the link to verify your email: {link}', 'ravan2763@gmail.com', [user.email])

class EmailVerifyView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({'message': 'Email verified successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid token or user'}, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({'refresh': str(refresh), 'access': str(refresh.access_token)}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request):
        return Response({'message': 'This is the login endpoint. Please use POST to log in.'}, status=status.HTTP_200_OK)

class UploadFileView(CreateAPIView):
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # Log to ensure we're receiving the file
        file = request.FILES.get('file')
        if not file:
            return Response({'message': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if the user is an 'ops' user
        if request.user.user_type != 'ops':
            return Response({'message': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        # Proceed with the normal creation process
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
class ListFilesView(ListAPIView):
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return File.objects.filter(user=self.request.user)

class DownloadFileView(RetrieveAPIView):
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        file_id = kwargs['pk']
        try:
            file = File.objects.get(pk=file_id)
            if request.user.user_type != 'client':
                return Response({'message': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
            
            download_link = self.generate_download_link(file)
            return Response({'download-link': download_link, 'message': 'success'}, status=status.HTTP_200_OK)
        except File.DoesNotExist:
            return Response({'message': 'File not found'}, status=status.HTTP_404_NOT_FOUND)

    def generate_download_link(self, file):
        # Implement your encryption logic here
        token = urlsafe_base64_encode(force_bytes(file.pk))
        return f"/download-file/{token}/"

class FileDownloadView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        token = kwargs.get('token')
        try:
            file_id = force_str(urlsafe_base64_decode(token))
            file = File.objects.get(pk=file_id)

            # Ensure the user has permission to download the file
            if request.user.user_type != 'client':
                return Response({'message': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
            
            # Generate file response
            file_path = file.file.path
            response = FileResponse(open(file_path, 'rb'), as_attachment=True, filename=file.file.name)

            # Save a copy of the file to the system default download directory
            self.save_file_locally(file_path, file.file.name)

            return response
        
        except File.DoesNotExist:
            return Response({'message': 'File not found'}, status=status.HTTP_404_NOT_FOUND)
        except (ValueError, TypeError, OverflowError, UnicodeDecodeError):
            return Response({'message': 'Invalid link'}, status=status.HTTP_400_BAD_REQUEST)

    def save_file_locally(self, file_path, file_name):
        # Determine the default download directory
        download_dir = self.get_default_download_directory()

        # Ensure the directory exists
        if not download_dir.exists():
            download_dir.mkdir(parents=True, exist_ok=True)

        # Define the path to save the file
        file_path_to_save = download_dir / file_name

        # Save the file to the default download directory
        try:
            with open(file_path, 'rb') as original_file:
                with open(file_path_to_save, 'wb') as new_file:
                    new_file.write(original_file.read())
            print(f"File saved to {file_path_to_save}")
        except FileNotFoundError:
            print(f"Error: File not found at {file_path}")
        except Exception as e:
            print(f"Unexpected error occurred: {e}")

    def get_default_download_directory(self):
        home = Path.home()
        if os.name == 'nt':  # Windows
            download_dir = home / 'Downloads'
        else:  # macOS and Linux
            download_dir = home / 'Downloads'
            
        return download_dir