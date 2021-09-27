from rest_framework import serializers

from .models import Stream, Department


class DepartmentSerializer(serializers.ModelSerializer):

    class Meta:

        model = Department
        fields = ("id", "department_name",)


class StreamSerializer(serializers.ModelSerializer):

    department_name = DepartmentSerializer(read_only=True, many=True)
    class Meta:

        model = Stream
        fields = ("id", "stream_name", "department_name",)
