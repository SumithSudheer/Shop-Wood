from rest_framework import serializers
from accounts.models import User,BranchAdmin

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'mobile','password']
        # fileds = '__all__'


    def get_name(self,obj):
        name=obj.username
        return name
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        instance.is_active = True
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['is_active']




class BranchAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = BranchAdmin
        fields = '__all__'
        # fields = ['email','password','superadmin']


