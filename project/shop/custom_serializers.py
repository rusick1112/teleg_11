# project/shop/custom_serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from .models import CustomerProfile


class CustomUserCreateSerializer(BaseUserCreateSerializer):
    """Custom user creation serializer that also creates customer profile"""
    phone_number = serializers.CharField(max_length=20, required=False, allow_blank=True, write_only=True)
    address = serializers.CharField(required=False, allow_blank=True, write_only=True)
    
    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'password', 'phone_number', 'address')
    
    def validate(self, attrs):
        # Remove profile fields from user validation
        self.profile_data = {
            'phone_number': attrs.pop('phone_number', ''),
            'address': attrs.pop('address', '')
        }
        return super().validate(attrs)
    
    def create(self, validated_data):
        # Create user with only User model fields
        user = super().create(validated_data)
        
        # Create customer profile with the stored profile data
        CustomerProfile.objects.create(
            user=user,
            phone_number=self.profile_data.get('phone_number', ''),
            address=self.profile_data.get('address', '')
        )
        
        return user


class CustomUserSerializer(serializers.ModelSerializer):
    """Custom user serializer with profile information"""
    profile = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'profile')
        read_only_fields = ('id',)
    
    def get_profile(self, obj):
        try:
            profile = obj.profile
            return {
                'phone_number': profile.phone_number,
                'address': profile.address
            }
        except CustomerProfile.DoesNotExist:
            return {
                'phone_number': '',
                'address': ''
            }