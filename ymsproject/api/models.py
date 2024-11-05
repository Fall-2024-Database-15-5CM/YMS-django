from django.db import models
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from PIL import Image
import json
import io


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    password = models.CharField(max_length=128)  # password 필드 길이 수정
    username = models.CharField(max_length=30, unique=True)
    phone = models.CharField(max_length=13, unique=True)
    authority = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # password hashing 로직
        if not self.pk:  # 새로운 객체일 때만 해싱
            self.password = make_password(self.password)

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
    image = models.BinaryField(default=b'') # 이미지 없으면 빈 바이너리로 채움
    state = models.CharField(max_length=30)
    phone = models.CharField(max_length=13)
    adress = models.CharField(max_length=50)
    email = models.CharField(max_length=30)
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    thumbnail = models.BinaryField(null=True, blank=True)  # 썸네일 필드 추가
    image = models.BinaryField(null=True, blank=True)  # 이미지 필드 추가
    new_temp_field = models.BinaryField(null=True, blank=True)  # 임시 필드 추가

    def save(self, *args, **kwargs):
        # 이미지 크기 조정
        if self.image:
            image = Image.open(io.BytesIO(self.image))
            image = image.resize((40, 40)) # 40x40 픽셀
            # 이미지를 바이너리로 변환
            image_io = io.BytesIO()
            image.save(image_io, format='PNG') # 일단 png로 해뒀는데 변경 가능
            self.image = image_io.getvalue()

        super().save(*args, **kwargs)

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
