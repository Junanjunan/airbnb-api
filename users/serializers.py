from rest_framework import serializers
from .models import User

class RelatedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "avatar",
            "superhost"
        )
        # fields = ("username", "superhost")




class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)       # field에 password를 표기하지만(create 등 하기 위해서), read는 할 수 없게 write_only 설정

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "avatar",
            "superhost",
            "password"
        )
        read_only_fields = (
            "id",
            "superhost",
            "avatar"
        )

    # def validate_last_name(self, value):            # validate로 대문자로 저장해보기
    #     return value.upper()

    def create(self, validated_data):
        password = validated_data.get("password")
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user