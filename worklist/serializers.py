from rest_framework import serializers

from userprofile.serializers import UserSerializer
from worklist.models import Board, List, Card, Comment


class CommentCreateSerializer(serializers.ModelSerializer):
    def get_replies(self, comment):
        replies = Comment.objects.filter(parent_comment=comment)
        serializer = CommentSerializer(replies, many=True)
        return serializer.data

    class Meta:
        model = Comment
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()
    user = UserSerializer(allow_null=True)

    def get_replies(self, comment):
        replies = Comment.objects.filter(parent_comment=comment)
        serializer = CommentSerializer(replies, many=True)
        return serializer.data

    class Meta:
        model = Comment
        fields = '__all__'


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

