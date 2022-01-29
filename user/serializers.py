from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(label=_('პაროლი'), write_only=True, style={'input_type': 'password'})
    password2 = serializers.CharField(label=_('გაიმეორეთ პაროლი'), write_only=True, style={'input_type': 'password'})
    token = serializers.CharField(label=_('ავტორიზაციის ტოკენი'), read_only=True)

    class Meta:
        model = User
        fields = ['password1', 'password2', 'first_name', 'last_name', 'username', 'email', 'token']

    def validate(self, attrs):
        password1 = attrs.get('password1')
        password2 = attrs.get('password2')
        if password2 and password1:
            if password2 != password1:
                raise serializers.ValidationError(_('პაროლი ერთმანეთს არ ემთხვევა'))
        else:
            raise serializers.ValidationError(_('პაროლის შეყვანა აუცილებელია'))
        return attrs

    def create(self, validated_data):
        password = validated_data.get('password1')
        user = User(
            username=validated_data.get('username'),
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            email=validated_data.get('email'),
            is_active=False
        )
        user.set_password(password)
        user.save()
        return user


class VerifyUser(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['is_active']


class LoginUser(serializers.ModelSerializer):
    password1 = serializers.CharField(label=_('პაროლი'), write_only=True, style={'input_type': 'password'})
    email = serializers.EmailField(label=_('მეილი'), write_only=True)
    token = serializers.CharField(label=_('token'), read_only=True)

    class Meta:
        model = User
        fields = ['password1', 'email', 'token']

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password1')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)
            if not user:
                error_message = 'მეილი ან პაროლი არასწორია'
                raise serializers.ValidationError(error_message)
        else:
            error_message = 'მეილის და პაროლის შევსება სავალდებულოა'
            raise serializers.ValidationError(error_message)

        attrs['user'] = user
        return attrs
