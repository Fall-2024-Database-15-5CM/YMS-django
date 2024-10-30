from rest_framework import serializers
from .models import User, Division, Yard, Slot, Structure, Driver, Transaction, Truck, Chassis, Container, Trailer, Maintenance, SlotUpdate

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class DivisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Division
        fields = '__all__'

class YardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Yard
        fields = '__all__'

class SlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slot
        fields = '__all__'

class StructureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Structure
        fields = '__all__'

class DriverSerializer(serializers.ModelSerializer):
    updated_at = serializers.DateTimeField(read_only=False)  # 읽기 전용 해제
    thumbnail = serializers.ModelField(model_field=Driver._meta.get_field('thumbnail'), read_only=False)
    image = serializers.ModelField(model_field=Driver._meta.get_field('image'), read_only=False)
    class Meta:
        model = Driver
        fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

class TruckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Truck
        fields = '__all__'

class ChassisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chassis
        fields = '__all__'

class ContainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Container
        fields = '__all__'

class TrailerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trailer
        fields = '__all__'

class MaintenanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maintenance
        fields = '__all__'

class SlotUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SlotUpdate
        fields = '__all__'
