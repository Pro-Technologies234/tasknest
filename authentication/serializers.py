from rest_framework import serializers
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username', 
                  'gender', 'birthdate', 'profile_image',
                  'created_at'
                  ]
        
    
class UserUpdateSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = CustomUser
        fields = [
            'email', 'username', 'gender', 
            'birthdate', 'profile_image',
        ]
        extra_kwargs = {
            'birthdate': {'required': False},
            'profile_image': {'required': False, 'allow_null': True},
            
        }

    def validate_profile_image(self, value):
        if value and not value.content_type.startswith('image/'):
            raise serializers.ValidationError("File type is not image.")
        return value
    

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'username', 'email', 'password',
            'gender', 'birthdate', 'profile_image',
        ]
        extra_kwargs = {
            'birthdate': {'required': False},
            'profile_image': {'required': False}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user
