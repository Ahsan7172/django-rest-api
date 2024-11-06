from rest_framework import serializers
from .models import User
from django.utils.encoding import smart_str,force_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .utils import Utils
class RegistrationSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(max_length=50,style={'input_type':'password'})
    class Meta:
        model=User
        fields=['image','name','email','password','password2']
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    def validate(self, attrs):
        password=attrs.get('password')
        password2=attrs.get('password2')
        if password!=password2:
            raise serializers.ValidationError('password doesnot match!')
        return attrs
class LoginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=70)
    class Meta:
        model=User
        fields=['email','password']
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['name','email','image']
class ChangePasswordSerializer(serializers.Serializer):
    password=serializers.CharField(max_length=80, style={'input_type':'password'})
    password2=serializers.CharField(max_length=70, style={'input_type':'password'})
    # class Meta:
    #     fields=['password','password2']
    def validate(self, attrs):
        password=attrs.get('password')
        password2=attrs.get('password2')
        user=self.context.get('user')
        if password!=password2:
            raise serializers.ValidationError("your password are not match!")
        user.set_password(password)
        user.save()
        return attrs
class SendEmailSerializer(serializers.Serializer):
    email=serializers.EmailField(max_length=70)
    def validate(self, attrs):
        email=attrs.get('email')
        if User.objects.filter(email=email).exists():
            user=User.objects.get(email=email)
            uid=urlsafe_base64_encode(force_bytes(user.id))
            print('uid:',uid)
            token=PasswordResetTokenGenerator().make_token(user)
            link='http://127.0.0.1:8000/reset/'+uid+token
            body="click here to reset your password"+link
            print(body)
            data={
                'subject':'RESET Your Password',
                'body':body,
                'to_email':user.email
            }
            Utils.send_mail(data)
            return attrs
class PasswordResetSerializer(serializers.Serializer):
    
     password=serializers.CharField(max_length=80, style={'input_type':'password'})
     password2=serializers.CharField(max_length=70, style={'input_type':'password'})
    # class Meta:
    #     fields=['password','password2']
     def validate(self, attrs):
        password=attrs.get('password')
        password2=attrs.get('password2')
        uid=self.context.get('uid')
        token=self.context.get('token')
        if password!=password2:
            raise serializers.ValidationError("your password are not match!")
        id=smart_str(urlsafe_base64_decode(uid))
        user=User.objects.get(id=id)
        if not PasswordResetTokenGenerator().check_token(user,token):
            raise serializers.ValidationError('token is expired or not valid')
        user.set_password(password)
        user.save()
        return attrs
        