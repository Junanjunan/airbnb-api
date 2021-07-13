from rest_framework import serializers
from users.serializers import RelatedUserSerializer
from .models import Room


class ReadRoomSerializer(serializers.ModelSerializer):

    user = RelatedUserSerializer()

    class Meta:
        model = Room
        exclude = ("modified",)


class WriteRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        exclude = ("user", "modified", "created")

    
    def validate(self, data):
        if self.instance:                                               # update 할 때
            check_in = data.get('check_in', self.instance.check_in)     # update 할 때는 check_in, check_out을 수정하지 않을 수 있다. 그때는 self.instance.check_in 에 이미 있는 값을 default로 가져온다.
            check_out = data.get('check_out', self.instance.check_out)
        else:                                                           # create 할 때
            check_in = data.get('check_in')
            check_out = data.get('check_out')
        if check_in == check_out:
            raise serializers.ValidationError(
                "Not enough time between changes")
        return data
