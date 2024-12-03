from django.db import models
from django.utils import timezone
import json

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    password_hash = models.CharField(max_length=255)
    username = models.CharField(max_length=30, unique=False)
    phone = models.CharField(max_length=13, unique=True)
    authority = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if isinstance(self.authority, dict):
            self.authority = json.dumps(self.authority)
        super().save(*args, **kwargs)

    def get_authority(self):
        try:
            return json.loads(self.authority)
        except (TypeError, json.JSONDecodeError):
            return {}

class Division(models.Model):
    # ID 형식: 2 Letters (예: "LA", "PHX")
    division_id = models.CharField(
        max_length=3,
        primary_key=True,
        validators=[RegexValidator(r'^[A-Z]{2}$', 'Division ID must consist of 2 uppercase letters.')],
    )
    division_name = models.CharField(max_length=30)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

class Yard(models.Model):
    # ID 형식: Division + 2 Digits (예: "LA01")
    yard_id = models.CharField(
        max_length=5,
        primary_key=True,
        validators=[RegexValidator(r'^[A-Z]{2}\d{2}$', 'Yard ID must follow the format: 2 letters + 2 digits.')],
    )
    division = models.ForeignKey(Division, on_delete=models.CASCADE)
    yard_name = models.CharField(max_length=30)
    capacity = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

class Slot(models.Model):
    slot_id = models.AutoField(primary_key=True)
    yard = models.ForeignKey(Yard, on_delete=models.CASCADE)
    slot_num = models.IntegerField()
    slot_type = models.CharField(null=False, max_length=30)
    x = models.IntegerField()
    y = models.IntegerField()
    w = models.IntegerField()
    h = models.IntegerField()
    direction = models.CharField(max_length=11, default='')
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

class Structure(models.Model):
    structure_id = models.AutoField(primary_key=True)
    yard = models.ForeignKey(Yard, on_delete=models.CASCADE)
    structure_type = models.CharField(max_length=30)
    x = models.IntegerField()
    y = models.IntegerField()
    w = models.IntegerField()
    h = models.IntegerField()
    direction = models.CharField(max_length=10)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

class Driver(models.Model):
    # ID 형식: 6 Letters + 2 Digits (예: "DRIVER01")
    driver_id = models.CharField(
        max_length=8,
        primary_key=True,
        validators=[RegexValidator(r'^[A-Z]{6}\d{2}$', 'Driver ID must follow the format: 6 letters + 2 digits.')],
    )
    name = models.CharField(max_length=30, null=False)
    license_number = models.CharField(max_length=30)
    phone = models.CharField(max_length=13, default='')
    address = models.CharField(max_length=50, default='')
    email = models.CharField(max_length=30, default='')
    state = models.CharField(max_length=30, default='')
    status = models.CharField(max_length=50, default='')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

class Transaction(models.Model):
    transaction_id = models.CharField(max_length=16, primary_key=True)
    truck_id = models.CharField(max_length=14)
    equipment_id = models.CharField(max_length=14)  # ForeignKey placeholder for dynamic relations
    child_equipment_id = models.CharField(max_length=14)  # ForeignKey placeholder for dynamic relations
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    source = models.ForeignKey(Yard, related_name='source', on_delete=models.SET_NULL, null=True)
    destination = models.ForeignKey(Yard, related_name='destination', on_delete=models.SET_NULL, null=True)
    datetime = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)

class Truck(models.Model):
    truck_id = models.CharField(max_length=16, primary_key=True)
    slot = models.ForeignKey(Slot, on_delete=models.SET_NULL, null=True)
    state = models.CharField(max_length=30)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

class Chassis(models.Model):
    # ID 형식: 4 Letters (예: "TRAX")
    chassis_id = models.CharField(
        max_length=4,
        primary_key=True,
        validators=[RegexValidator(r'^[A-Z]{4}$', 'Chassis ID must consist of 4 uppercase letters.')],
    )
    slot = models.ForeignKey(Yard, on_delete=models.SET_NULL, null=True)
    state = models.CharField(max_length=30)
    container_id = models.CharField(max_length=16, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

class Container(models.Model):
    # ID 형식: 4 Letters + 7 Digits (예: "CONT1234567")
    container_id = models.CharField(
        max_length=11,
        primary_key=True,
        validators=[RegexValidator(r'^[A-Z]{4}\d{7}$', 'Container ID must follow the format: 4 letters + 7 digits.')],
    )
    slot = models.ForeignKey(Yard, on_delete=models.SET_NULL, null=True)
    state = models.CharField(max_length=30)
    container_size = models.CharField(max_length=10)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

class Trailer(models.Model):
    # ID 형식: 4 Letters + 6 Digits (예: "TRAI123456")
    trailer_id = models.CharField(
        max_length=10,
        primary_key=True,
        validators=[RegexValidator(r'^[A-Z]{4}\d{6}$', 'Trailer ID must follow the format: 4 letters + 6 digits.')],
    )
    slot = models.ForeignKey(Yard, on_delete=models.SET_NULL, null=True)
    state = models.CharField(max_length=30)
    trailer_size = models.CharField(max_length=10)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

class Maintenance(models.Model):
    maintenance_id = models.AutoField(primary_key=True)
    equipment_id = models.IntegerField()  # Placeholder for foreign key relation
    maintenance_date = models.DateTimeField(default=timezone.now)
    details = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

class SlotUpdate(models.Model):
    id = models.AutoField(primary_key=True)
    slot_id = models.IntegerField()  # ForeignKey placeholder for Slot
    parent_equipment_id = models.IntegerField()  # Placeholder for foreign key relation
    child_equipment_id = models.IntegerField()  # Placeholder for foreign key relation
    updated_at = models.DateTimeField(default=timezone.now)
