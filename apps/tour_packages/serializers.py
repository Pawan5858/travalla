from rest_framework import serializers
from .models import *
from apps.masterentry.serializers import DestinationSerializer


class TourPackageItinerarySerializer(serializers.ModelSerializer):
    class Meta:
        model = TourPackageItinerary
        fields = '__all__'

class TourPackageSerializer(serializers.ModelSerializer):
    destination = DestinationSerializer(read_only=True, source='torp_destination') 
    start_location = DestinationSerializer(read_only=True, source='torp_start_location') 
    end_destination = DestinationSerializer(read_only=True, source='torp_end_destination') 
    itinerary = TourPackageItinerarySerializer(many=True, read_only=True, source='tourpackageitinerary_set')
    class Meta:
        model = TourPackage
        fields = '__all__'
        
        