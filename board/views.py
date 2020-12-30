from django.shortcuts import render

from rest_framework import generics

from board.serializers import BoardSerializer
from board.models import Board


class BoardApiView(generics.ListAPIView):
  queryset = Board.objects.all()
  serializer_class = BoardSerializer

  def get_queryset(self):
    queryset = super(BoardApiView, self).get_queryset()
    query = self.request.query_params.get('query', None)

    # queryset = queryset.filter(user=self.request.user)

    if query is not None:
      queryset = queryset.filter(name__icontains=query)

    queryset = queryset.order_by('name')
    return queryset
