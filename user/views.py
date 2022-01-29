from rest_framework import generics, status
from django.contrib.auth import get_user_model
from . import serializers
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .email import Mail


User = get_user_model()


class RegisterUser(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        context = {'result': 'verify your email address', 'token': token.key}
        Mail.send_verify_email_token(to=user.email, user=user, request=request)
        return Response(context, status=status.HTTP_201_CREATED)


class VerifyUser(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.VerifyUser
    lookup_field = 'id'


class LoginUser(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.LoginUser

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(context={'request': request}, data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get('user')
        token, _ = Token.objects.get_or_create(user=user)
        context = {'token': token.key}
        return Response(context, status=status.HTTP_201_CREATED)
