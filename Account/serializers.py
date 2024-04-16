from rest_framework import serializers
from .models import Account, Report, Credentials

import string
import secrets


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id_card', 'first_name', 'last_name',
                'role']
        

        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
            instance.make_password(password)
        instance.save()
        return instance



class AccountSerializer(serializers.ModelSerializer):
    role = serializers.CharField(
        source='role.role_descripction', read_only=True)

    class Meta:
        model = Account
        fields = '__all__'


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'

class CredentialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Credentials
        exclude = ['password']
