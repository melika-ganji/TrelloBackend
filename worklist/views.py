import django_filters
from django.http import JsonResponse, Http404
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView
from rest_framework import permissions, status
from django_filters import rest_framework as filters

from worklist.models import Board, Card, List, Comment
from worklist.serializers import BoardSerializer, ListSerializer, CardSerializer, BoardDetailSerializer, \
    BoardCreateSerializer, ListCreateSerializer, CardCreateSerializer, CommentSerializer, CommentCreateSerializer

filter_backends = (filters.DjangoFilterBackend,)


class TagFilter(django_filters.FilterSet):
    class Meta:
        model = Card
        fields = ['tag']


class BoardAPIView(ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BoardSerializer

    def get_queryset(self):
        users = self.request.user
        return Board.objects.filter(users__id=users.id)


class BoardCreateAPIView(ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BoardCreateSerializer

    def get_queryset(self):
        users = self.request.user
        return Board.objects.filter(users__id=users.id)

    def post(self, request, *args, **kwargs):
        data_copy = request.data.copy()
        data_copy['admin'] = request.user.id

        serializer = BoardCreateSerializer(data=data_copy, context={"request": request})

        flag = False
        for user in data_copy["users"]:
            if request.user.id == user:
                flag = True
                break

        if not flag:
            return Response(status=status.HTTP_403_FORBIDDEN)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BoardDetailAPIView(ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BoardDetailSerializer

    def get_queryset(self):
        users = self.request.user
        return Board.objects.filter(users__id=users.id)


class ListAPIView(ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ListSerializer

    def get_queryset(self):
        board = self.request.board.id
        return List.objects.filter(board__id=board)


class ListCreateAPIView(ListCreateAPIView):
    serializer_class = ListCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        board = self.request.board.id
        return List.objects.filter(board__id=board)

    def post(self, request, *args, **kwargs):
        board = self.request.data["board"]
        board_info = Board.objects.get(id=board)
        admin = board_info.admin
        print(admin)
        if admin.id != request.user.id:
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = ListCreateSerializer(data=request.data, context={"request": request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CardAPIView(ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CardSerializer
    filterset_class = TagFilter

    def get_queryset(self):
        users = self.request.user
        return Card.objects.filter(users__id=users.id)


class CardCreateAPIView(ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CardSerializer

    def get_queryset(self):
        users = self.request.user
        return Card.objects.filter(users__id=users.id)

    def post(self, request, *args, **kwargs):
        # print(request.data)
        # lst = self.request.data["list"]   #id hast
        # list_info = List.objects.get(id=lst)
        # board = Board.objects.get(id=list_info.board.id)  #title hast
        # board_id = getBoardId(board)
        # print("boardid", board_id)
        # users = Board.objects.get(id=board_id).users
        # print(users)

        # flag = False
        # for user in users:
        #     if request.data["users"] == user:
        #         flag = True
        #         break
        #
        # if not flag:
        #     return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = CardCreateSerializer(data=request.data, context={"request": request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # print(admin)
        # if list_info.id != request.user.id:
        #     return Response(status=status.HTTP_403_FORBIDDEN)


class CommentAPIView(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CommentSerializer

    def get_queryset(self):
        card_id = self.kwargs.get('id')
        print(card_id)
        if card_id:
            return Comment.objects.filter(card=card_id, parent_comment=None)
        # else:
        #     return Comment.objects.filter(parent_comment=None)


class CommentCreateAPIView(ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CommentCreateSerializer

    def get_queryset(self):
        card_id = self.kwargs.get('card_id')
        if card_id:
            return Comment.objects.filter(card=card_id, parent_comment=None)
        else:
            return Comment.objects.filter(parent_comment=None)

    def post(self, request, *args, **kwargs):
        card_id = self.request.data.get('card', None)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if card_id:
            card = Card.objects.get(pk=card_id)
            serializer.save(card=card)
        else:
            serializer.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


# def post(self, request, *args, **kwargs):
   #     card_id = self.request.data.get('card', None)
   #     # if card_id:
   #     #     card = Card.objects.get(pk=card_id)
   #     #     serializer.save(card=card)
   #     # else:
   #     #     serializer.save()
   #     serializer = self.get_serializer(data=request.data)
   #     serializer.is_valid(raise_exception=True)
   #
   #     # Associate the comment with the specified card
   #     if card_id:
   #         card = Card.objects.get(pk=card_id)
   #         serializer.save(card=card)
   #     else:
   #         serializer.save()
   #
   #     headers = self.get_success_headers(serializer.data)
   #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)



def getBoardId(request, name):
    board = Board.objects.get(title=name)
    if board:
        return JsonResponse({'id': board.id})
    else:
        return Http404


def getListId(request, name):
    lst = List.objects.get(title=name)
    if lst:
        return JsonResponse({'id': lst.id})
    else:
        return Http404
