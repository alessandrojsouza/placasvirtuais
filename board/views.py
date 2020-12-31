from django.shortcuts import render

from rest_framework import generics

from board.serializers import BoardSerializer
from board.models import Board


class BoardApiView(generics.ListAPIView, generics.RetrieveAPIView,
                  generics.CreateAPIView, generics.UpdateAPIView, generics.DestroyAPIView):
  queryset = Board.objects.all()
  serializer_class = BoardSerializer

  def get_queryset(self):
    pk = self.kwargs.get('pk')
    queryset = super(BoardApiView, self).get_queryset()
    query = self.request.query_params.get('query', None)

    if query is not None:
      queryset = queryset.filter(name__icontains=query)

    if pk:
      queryset = queryset.filter(pk=pk)

    queryset = queryset.order_by('name')
    return queryset
