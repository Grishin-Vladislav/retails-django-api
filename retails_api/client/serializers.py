from rest_framework import serializers


class HelloWorldSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=255)

    def validate_message(self, v):
        if v != 'Hello world':
            raise serializers.ValidationError('Must be "Hello world"')
        return v
