from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'role', 'phone', 'national_id')
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 6},
            'email': {'required': False, 'allow_blank': True},
            'phone': {'required': False, 'allow_blank': True},
            'national_id': {'required': False, 'allow_blank': True},
            'role': {'required': False},
        }

    def create(self, validated_data):
        # Extract password to hash it properly via create_user
        password = validated_data.pop('password')
        
        # Ensure default role if not provided or to prevent unauthorized role escalation
        validated_data.setdefault('role', 'GUEST')
        
        # create_user handles hashing and assigns all remaining validated fields
        user = User.objects.create_user(
            password=password,
            **validated_data
        )
        return user

# Add this at the bottom of serializers.py
class LogoutSerializer(serializers.Serializer):
    confirm = serializers.BooleanField(
        default=True,
        help_text="Check this box to confirm logout"
    )


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)
    password = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True,
        required=True
    )
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'role', 'phone', 'national_id')
        read_only_fields = ('id',)