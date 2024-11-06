from django.shortcuts import render
from .models import User
from .serializers import RegistrationSerializer,LoginSerializer,ProfileSerializer,ChangePasswordSerializer,SendEmailSerializer,PasswordResetSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login,logout,authenticate
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from .renderers import UserRenderer
from rest_framework .generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView,ListAPIView,DestroyAPIView
from rest_framework import viewsets
# Create your views here.
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
class RegistrationView(APIView):
    def post(self,request):
        serializer=RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.save()
            token=get_tokens_for_user(user)
            return Response({'msg':'successfully signup','token':token},status.HTTP_200_OK)
        return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)
class LoginView(APIView):
    def post(self,request):
        serializer=LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email=serializer.data.get('email')
            password=serializer.data.get('password')
            user=authenticate(email=email,password=password)
            if user is not None:
                token=get_tokens_for_user(user)
                return Response({"msg":"login successfully!",'token':token},status=status.HTTP_200_OK)
            else:
                
                return Response({'errors':'password or email doesnot exits'},status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors)
class ProfileView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        serializer=ProfileSerializer(request.user)
        return Response(serializer.data,status=status.HTTP_200_OK)
class ChangePasswordView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        serializer=ChangePasswordSerializer(data=request.data,context={'user':request.user})
        if serializer.is_valid(raise_exception=True):
            
            return Response({'msg':'password change sucessfully!'})
class SendEmailView(APIView):
    def post(self,request):
        serializer=SendEmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password Reset link send. Please check your Email'}, status=status.HTTP_200_OK) 
class PasswordResetView(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request,uid,token):
        serializer=PasswordResetSerializer(data=request.data,context={'uid':uid,'token':token})
        serializer.is_valid()
        return Response({'msg':'password reset successfully!'})

class CRUD(viewsets.ModelViewSet):
    queryset=User.objects.all()
    serializer_class=ProfileSerializer
    def get_permissions(self):
        if self.action in['list']:
            permission_classes=[IsAdminUser]
        elif self.action in ['retrieve','update','partial_update','destroy']:
            permission_classes=[IsAuthenticated]
        else:
            permission_classes=[IsAuthenticated]
        return [permission() for permission in permission_classes]
    def retrieve(self, request, *args, **kwargs):
        user=self.get_object()
        if request.user==user or request.user.is_staff:
            serializer=self.get_serializer(user)
            return Response(serializer.data)
        return Response({"error":"user not authenticated"})
    def update(self, request, *args, **kwargs):
        user=self.get_object()
        if request.user==user or request.user.is_staff:
            serializer=ProfileSerializer(user,data=request.data,partial=True)
            if serializer.is_valid(raise_exception=True):
                self.partial_update(serializer)
                return Response({"msg":"updated successfully"})
    def destroy(self, request, *args, **kwargs):
        user=self.get_object()
        if request.user==user or request.user.is_staff:
            self.perform_destroy(user)
            return Response({'msg':"user deleted successfully"})

            
 

    
           
        
            
