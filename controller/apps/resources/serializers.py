from __future__ import absolute_import

from api import api, serializers
from nodes.models import Node

from . import ResourcePlugin
from .models import Resource, ResourceReq


class ResourceSerializer(serializers.ModelSerializer):
    unit = serializers.CharField(read_only=True)
    
    class Meta:
        model = Resource
        fields = ['name', 'max_sliver', 'dflt_sliver', 'unit']


class ResourceReqSerializer(serializers.ModelSerializer):
    unit = serializers.CharField(read_only=True)
    
    class Meta:
        model = ResourceReq
        fields = ['name', 'req', 'unit']


for producer_model in ResourcePlugin.get_producers_model():
    api.aggregate(producer_model, ResourceSerializer, name='resources')

for consumer_model in ResourcePlugin.get_consumers_model():
    api.aggregate(consumer_model, ResourceReqSerializer, name='resources')