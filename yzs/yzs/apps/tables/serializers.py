from rest_framework import serializers

from .models import *


class TabInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TabInfo
        fields = '__all__'


class DBInfoSerializer(serializers.ModelSerializer):
    tabinfo_set = TabInfoSerializer(many=True, required=False)
    class Meta:
        model = DBInfo
        fields = '__all__'

        # extra_kwargs = {
        #     'schema_name': {'required': False}
        # }


class TabMetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TabMeta
        fields = '__all__'



class TabDDLSerializer(serializers.ModelSerializer):
    class Meta:
        model = TabDDL
        fields = '__all__'


class TabSampSerializer(serializers.ModelSerializer):
    class Meta:
        model = TabSamp
        fields = '__all__'


class TabMetaHisSerializer(serializers.ModelSerializer):
    class Meta:
        model = TabMetaHis
        fields = '__all__'


class TabDDLHisSerializer(serializers.ModelSerializer):
    class Meta:
        model = TabDDLHis
        fields = '__all__'