from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ViewSet, GenericViewSet, ReadOnlyModelViewSet, ModelViewSet
from .serializers import *
from rest_framework.permissions import IsAuthenticated
# Create your views here.


class DBInfoViewSet(ModelViewSet):
    #authentication_classes = []
    queryset = DBInfo.objects.all()
    serializer_class = DBInfoSerializer
    #permission_classes = []
    #def list(self, request, *args, **kwargs):


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

