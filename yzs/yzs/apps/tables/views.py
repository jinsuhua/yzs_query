from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet, GenericViewSet, ReadOnlyModelViewSet, ModelViewSet
from .serializers import *
from rest_framework.permissions import IsAuthenticated
# Create your views here.


class BusInfoViewSet(ModelViewSet):
    queryset = BusInfo.objects.all()
    serializer_class = BusInfoSerializer
    permission_classes = []


class DBInfoViewSet(ModelViewSet):
    #authentication_classes = []
    queryset = DBInfo.objects.all()
    serializer_class = DBInfoSerializer
    permission_classes = []
    #def list(self, request, *args, **kwargs):

    # @action(methods=['delete'], detail=False)
    # def multiple_delete(self, request, *args, **kwargs):
    #     delete_id = request.query_params.get('deleteid', None)
    #     print(delete_id)
    #     if not delete_id:
    #         return Response(status=status.HTTP_404_NOT_FOUND)
    #     for i in delete_id.split(','):
    #         get_object_or_404(DBInfo, pk=int(i)).delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)



class TabInfoViewSet(ModelViewSet):
    queryset = TabInfo.objects.all()
    serializer_class = TabInfoSerializer



# class TableSearchView(APIView):
#     """根据表名过滤表"""
#
#     def get(self, request, tablename):
#         print(tablename)
#         # 查询user表
#         dbs = DBInfo.objects.filter(tabinfo__table_name__contains=tablename)
#         serializer =DBInfoSerializer(instance=dbs, many=True)
#
#         print(serializer.data)
#
#
#         return Response(serializer.data)


class TabMetaViewSet(ModelViewSet):
    queryset = TabMeta.objects.all()
    serializer_class = TabMetaSerializer
    #filter_class = TabMetaFilter
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['htab__id']


class TabDDLViewSet(ModelViewSet):
    queryset = TabDDL.objects.all()
    serializer_class = TabDDLSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['htab__id']



class TabSampViewSet(ModelViewSet):
    queryset = TabSamp.objects.all()
    serializer_class = TabSampSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['htab__id']

class TabMetaHisViewSet(ModelViewSet):
    queryset = TabMetaHis.objects.all()
    serializer_class = TabMetaHisSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['tab_id']


class TabDDLHisViewSet(ModelViewSet):
    queryset = TabDDLHis.objects.all()
    serializer_class = TabDDLHisSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['tab_id']

