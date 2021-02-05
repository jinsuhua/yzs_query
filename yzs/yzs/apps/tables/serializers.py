from rest_framework import serializers

from .models import *


class TabInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TabInfo
        exclude = ['create_date', 'update_date']


class DBInfoSerializer(serializers.ModelSerializer):
    tabinfo_set = TabInfoSerializer(many=True, required=False)
    #businfo = serializers.StringRelatedField(many=True)

    class Meta:
        model = DBInfo
        #fields = '__all__'
        exclude = ['businfo', 'create_date', 'update_date']
        # extra_kwargs = {
        #     'schema_name': {'required': False}
        # }


class BusInfoSerializer(serializers.ModelSerializer):
    dbinfo_set = DBInfoSerializer(many=True, required=False)

    class Meta:
        model = BusInfo
        fields = '__all__'


class TabMetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TabMeta
        exclude = ['create_date', 'update_date']


class TabDDLSerializer(serializers.ModelSerializer):
    class Meta:
        model = TabDDL
        exclude = ['create_date', 'update_date']


class TabSampSerializer(serializers.ModelSerializer):
    class Meta:
        model = TabSamp
        exclude = ['create_date', 'update_date']


class TabMetaHisSerializer(serializers.ModelSerializer):
    class Meta:
        model = TabMetaHis
        exclude = ['create_date', 'update_date']


class TabDDLHisSerializer(serializers.ModelSerializer):
    class Meta:
        model = TabDDLHis
        exclude = ['create_date', 'update_date']