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
    
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        exclude_fields = kwargs.pop('exclude_fields', None)
        super(DriverSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)
        if exclude_fields is not None:
            for field_name in exclude_fields:
                if field_name in self.fields:
                    self.fields.pop(field_name)

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
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        exclude_fields = kwargs.pop('exclude_fields', None)
        super(TruckSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)
        if exclude_fields is not None:
            for field_name in exclude_fields:
                if field_name in self.fields:
                    self.fields.pop(field_name)

class ChassisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chassis
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        exclude_fields = kwargs.pop('exclude_fields', None)
        super(ChassisSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)
        if exclude_fields is not None:
            for field_name in exclude_fields:
                if field_name in self.fields:
                    self.fields.pop(field_name)

class ContainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Container
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        exclude_fields = kwargs.pop('exclude_fields', None)
        super(ContainerSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)
        if exclude_fields is not None:
            for field_name in exclude_fields:
                if field_name in self.fields:
                    self.fields.pop(field_name)

class TrailerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trailer
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        exclude_fields = kwargs.pop('exclude_fields', None)
        super(TrailerSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)
        if exclude_fields is not None:
            for field_name in exclude_fields:
                if field_name in self.fields:
                    self.fields.pop(field_name)

class MaintenanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maintenance
        fields = '__all__'

class SlotUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SlotUpdate
        fields = '__all__'

class GenericEquipmentSerializer(serializers.Serializer):
    type = serializers.CharField()
    data = serializers.SerializerMethodField()

    def get_data(self, obj):
        equipment = obj['data']
        if obj['type'] == 'truck':
            return TruckSerializer(equipment).data
        elif obj['type'] == 'chassis':
            return ChassisSerializer(equipment).data
        elif obj['type'] == 'container':
            return ContainerSerializer(equipment).data
        elif obj['type'] == 'trailer':
            return TrailerSerializer(equipment).data
        else:
            return None
