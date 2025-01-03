# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class ApiChassis(models.Model):
    chassis_id = models.AutoField(primary_key=True)
    slot = models.ForeignKey('ApiSlot', models.DO_NOTHING, blank=True, null=True)
    container_id = models.IntegerField(blank=True, null=True)
    state = models.CharField(max_length=30)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'api_chassis'


class ApiContainer(models.Model):
    container_id = models.AutoField(primary_key=True)
    state = models.CharField(max_length=30)
    container_size = models.CharField(max_length=10)
    slot = models.ForeignKey('ApiSlot', models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'api_container'


class ApiDivision(models.Model):
    division_id = models.CharField(primary_key=True, max_length=10)
    division_name = models.CharField(max_length=30)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'api_division'


class ApiDriver(models.Model):
    driver_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    adress = models.CharField(max_length=50)
    email = models.CharField(max_length=30)
    phone = models.CharField(max_length=13)
    state = models.CharField(max_length=30)
    status = models.CharField(max_length=50)
    license_number = models.CharField(max_length=30)
    thumbnail = models.TextField(blank=True, null=True)
    image = models.TextField(blank=True, null=True)
    updated_at = models.DateTimeField()
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'api_driver'


class ApiMaintenance(models.Model):
    maintenance_id = models.AutoField(primary_key=True)
    equipment_id = models.IntegerField()
    maintenance_date = models.DateTimeField()
    details = models.TextField()
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'api_maintenance'


class ApiSlot(models.Model):
    slot_id = models.AutoField(primary_key=True)
    slot_num = models.IntegerField()
    slot_type = models.CharField(max_length=30)
    x = models.IntegerField()
    y = models.IntegerField()
    w = models.IntegerField()
    h = models.IntegerField()
    direction = models.CharField(max_length=11)
    yard = models.ForeignKey('ApiYard', models.DO_NOTHING)
    is_available = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'api_slot'


class ApiSlotupdate(models.Model):
    slot_id = models.IntegerField()
    parent_equipment_id = models.IntegerField()
    child_equipment_id = models.IntegerField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'api_slotupdate'


class ApiStructure(models.Model):
    structure_id = models.AutoField(primary_key=True)
    yard = models.ForeignKey('ApiYard', models.DO_NOTHING)
    structure_type = models.CharField(max_length=30)
    x = models.IntegerField()
    y = models.IntegerField()
    w = models.IntegerField()
    h = models.IntegerField()
    direction = models.CharField(max_length=10)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'api_structure'


class ApiTrailer(models.Model):
    trailer_id = models.AutoField(primary_key=True)
    state = models.CharField(max_length=30)
    slot = models.ForeignKey(ApiSlot, models.DO_NOTHING, blank=True, null=True)
    trailer_size = models.CharField(max_length=10)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'api_trailer'


class ApiTransaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    equipment_id = models.IntegerField()
    in_out = models.CharField(max_length=50)
    datetime = models.DateTimeField()
    destination = models.ForeignKey('ApiYard', models.DO_NOTHING, blank=True, null=True)
    driver = models.ForeignKey(ApiDriver, models.DO_NOTHING)
    source = models.ForeignKey('ApiYard', models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'api_transaction'


class ApiTruck(models.Model):
    truck_id = models.AutoField(primary_key=True)
    state = models.CharField(max_length=30)
    slot = models.ForeignKey(ApiSlot, models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'api_truck'


class ApiUser(models.Model):
    user_id = models.AutoField(primary_key=True)
    password_hash = models.CharField(max_length=30)
    username = models.CharField(unique=True, max_length=30)
    phone = models.CharField(unique=True, max_length=13)
    authority = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'api_user'


class ApiYard(models.Model):
    yard_id = models.CharField(primary_key=True, max_length=10)
    division = models.ForeignKey(ApiDivision, models.DO_NOTHING)
    yard_name = models.CharField(max_length=30)
    capacity = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'api_yard'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'
