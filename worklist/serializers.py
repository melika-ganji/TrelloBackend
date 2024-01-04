from rest_framework import serializers

from userprofile.serializers import UserSerializer
from worklist.models import Board, List, Card


class CardSerializer(serializers.ModelSerializer):
    users = UserSerializer(allow_null=True)

    class Meta:
        model = Card
        fields = '__all__'


class CardCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Card
        fields = '__all__'


class ListSerializer(serializers.ModelSerializer):
    cards = CardSerializer(many=True, allow_null=True)

    class Meta:
        model = List
        fields = '__all__'


class ListCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = List
        fields = '__all__'


class BoardDetailSerializer(serializers.ModelSerializer):
    lists = ListSerializer(many=True, allow_null=True)
    users = UserSerializer(many=True, allow_null=True)
    admin = UserSerializer(allow_null=True, read_only=True)

    class Meta:
        model = Board
        fields = '__all__'


class BoardSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True, read_only=True)
    admin = UserSerializer(allow_null=True, read_only=True)

    class Meta:
        model = Board
        fields = '__all__'


class BoardCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Board
        fields = '__all__'

    # def create(self, validated_data):
    #     users_data = validated_data.pop('users')
    #     board = Board.objects.create(**validated_data)
    #
    #     for user_data in users_data:
    #         user_id = user_data
    #         try:
    #             # user = User.objects.get(id=user_id)
    #             # print(user)
    #             board.users.add(user_id)
    #         except User.DoesNotExist:
    #             print(users_data)
    #             print("*****************")
    #             pass
    #
    #     return board

