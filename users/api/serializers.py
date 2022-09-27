from django.contrib.auth.models import User 
from rest_framework import serializers
from django.contrib.auth.hashers import make_password

class AccountSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)
    
    class Meta:
        model = User 
        fields = ["email", "username", "password", "password2"]
        extra_kwargs = {
            "password": {"write_only": True}
        }
        
    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError("The two passwords do not match !")
        return data 

    def create(self, validated_data):
        username = validated_data["username"]
        user_email = validated_data["email"] 
        password = make_password(validated_data["password"])
        confirm_account = User.objects.filter(email=user_email)
        if confirm_account.exists():
            raise serializers.ValidationError("An account already exists with this email")
        new_account = User.objects.create(email=user_email, username=username, password=password)
        return new_account