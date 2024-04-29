from rest_framework import serializers
from .models import Account, Report, Credentials, Permissions

class CredentialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Credentials
        exclude = ['password']

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'

class AccountSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source='role.role_descripction', read_only=True)
    credentials = CredentialsSerializer(source='credentials_set', many=True, read_only=True)
    reports = ReportSerializer(source='report_set',many=True, read_only=True)


    class Meta:
        model = Account
        fields = '__all__'

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model.objects.create(**validated_data)
        if password is not None:
            instance.set_password(password)
            instance.save()
        return instance

class PermissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permissions
        fields = '__all__'

class PermissionsSerializerLogIn(serializers.ModelSerializer):
    module_name = serializers.CharField(source='idModule.description')

    class Meta:
        model = Permissions
        fields = ['module_name', 'can_view', 'can_modify']
