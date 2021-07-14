from rest_framework import serializers
from users.serializers import RelatedUserSerializer
from .models import Room


class RoomSerializer(serializers.ModelSerializer):

    user = RelatedUserSerializer()
    is_fav = serializers.SerializerMethodField()

    class Meta:
        model = Room
        exclude = ("modified",)
        read_only_fields = ("user", "id", "created", "updated")         # 중복되는 serializer를 하나로 합치고, room을 create, update 등을 할 때 user가 수정되지 않도록(즉, user를 validate하지 않도록) 해준다.
                                                                        # read_only_fields는 ModelSerializer에서만 작동한다 함
    
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

    def get_is_fav(self, obj):
        request = self.context.get("request")
        if request:
            user = request.user
            if user.is_authenticated:
                return obj in user.favs.all()
        return False
