from rest_framework import serializers
from .models import WatchList, StreamingPlatform, Review

class ReviewSerializers(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only = True)
    class  Meta:
        model = Review
        exclude = ['watchlist']
        # fields = '__all__'

class WatchListSerializers(serializers.ModelSerializer):
    # reviews = ReviewSerializers(many = True, read_only = True)
    platform = serializers.CharField(source='platform.streamplatform')
    class Meta:
        model = WatchList
        fields = '__all__'
    
    def validate(self, value):
        if value['tittle'] == value['description']:
            return serializers.ValidationError("Title and description should be different")
        else:
            return value 
        
class StreamingPlatformSerializer(serializers.ModelSerializer):
    watchlist = WatchListSerializers(many=True, read_only=True)
    class Meta:
        model = StreamingPlatform
        fields = '__all__'
        










    
    
    """field level validation ex
    def validate_tittle(self, value):
        if len(value) < 2:
            return serializers.ValidationError("Title is too short")
        else:
            return value
            
    object level validation:
    def validate(self, value):
        if value['tittle] == value['description]:
            return serializers.ValidationError("Title and description should be different")
        else:
            return value
            
    
    
    """