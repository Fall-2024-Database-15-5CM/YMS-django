from django.db import models
from django.utils import timezone
import json

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    password_hash = models.CharField(max_length=30)
    username = models.CharField(max_length=30, unique=True)
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
    division_id = models.CharField(max_length=10, primary_key=True)
    division_name = models.CharField(max_length=30)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

class Yard(models.Model):
    yard_id = models.CharField(max_length=10, primary_key=True)
    division = models.ForeignKey(Division, on_delete=models.CASCADE)
    yard_name = models.CharField(max_length=30)
    capacity = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

class Slot(models.Model):
    slot_id = models.AutoField(primary_key=True)
    yard = models.ForeignKey(Yard, on_delete=models.CASCADE)
    slot_name = models.CharField(max_length=30)
    x = models.IntegerField()
    y = models.IntegerField()
    w = models.IntegerField()
    h = models.IntegerField()
    direction = models.IntegerField()
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
    driver_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30,null=False)
    license_number = models.CharField(max_length=30)
    phone = models.CharField(max_length=13,default='')
    adress = models.CharField(max_length=50,default='')
    email = models.CharField(max_length=30,default='')
    state = models.CharField(max_length=30,default='')
    status = models.CharField(max_length=50,default='')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    thumbnail = models.BinaryField(null=True, blank=True)  # 썸네일 필드 추가
    image = models.BinaryField(null=True, blank=True)  # 이미지 필드 추가

class Transaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    source = models.ForeignKey(Yard, related_name='source', on_delete=models.SET_NULL, null=True)
    destination = models.ForeignKey(Yard, related_name='destination', on_delete=models.SET_NULL, null=True)
    equipment_id = models.IntegerField()  # ForeignKey placeholder for dynamic relations
    in_out = models.CharField(max_length=50)
    datetime = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)

class Truck(models.Model):
    truck_id = models.AutoField(primary_key=True)
    slot = models.ForeignKey(Slot, on_delete=models.SET_NULL, null=True)
    state = models.CharField(max_length=30)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

class Chassis(models.Model):
    chassis_id = models.AutoField(primary_key=True)
    slot = models.ForeignKey(Slot, on_delete=models.SET_NULL, null=True)
    state = models.CharField(max_length=30)
    container_id = models.IntegerField(null=True)  # Placeholder for foreign key relation
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

class Container(models.Model):
    container_id = models.AutoField(primary_key=True)
    slot = models.ForeignKey(Slot, on_delete=models.SET_NULL, null=True)
    state = models.CharField(max_length=30)
    container_size = models.CharField(max_length=10)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

class Trailer(models.Model):
    trailer_id = models.AutoField(primary_key=True)
    slot = models.ForeignKey(Slot, on_delete=models.SET_NULL, null=True)
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
