from django.utils.timezone import now
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User, Division, Yard, Slot, Structure, Driver, Transaction, Truck, Chassis, Container, Trailer, Maintenance, SlotUpdate
from .serializer import *
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.files.base import ContentFile
from django.conf import settings
from django.db import connection
from django.db.models import Min, Max, F
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from datetime import date, datetime
import base64,requests
import jwt
import psutil
from django.shortcuts import render
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from datetime import date

def home(request):
    return HttpResponse("YMS API")

# User
@api_view(['GET', 'POST'])
def get_users(request):
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Division
@api_view(['GET', 'POST'])
def get_divisions(request):
    if request.method == 'GET':
        divisions = Division.objects.all()
        serializer = DivisionSerializer(divisions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = DivisionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Yard
@api_view(['GET', 'POST'])
def get_yards(request):
    if request.method == 'GET':
        yards = Yard.objects.all()
        serializer = YardSerializer(yards, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = YardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Slot
@api_view(['GET', 'POST'])
def get_slots(request):
    if request.method == 'GET':
        slots = Slot.objects.all()
        serializer = SlotSerializer(slots, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = SlotSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Structure
@api_view(['GET', 'POST'])
def get_structures(request):
    if request.method == 'GET':
        structures = Structure.objects.all()
        serializer = StructureSerializer(structures, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = StructureSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Driver
@api_view(['GET', 'POST'])
def get_drivers(request):
    if request.method == 'GET':
        drivers = Driver.objects.all()
        serializer = DriverSerializer(drivers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = DriverSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
# sorted Driver
@api_view(['GET'])
def get_sorted_drivers(request):
    # Query parameters 받기
    order_by = request.query_params.get('order_by', 'name')  
    page = request.query_params.get('page', 1)  
    filter_param = request.query_params.get('filter', None)  

    # Driver 쿼리셋 초기화
    drivers = Driver.objects.all()

    if filter_param:
        drivers = drivers.filter(
            Q(driver_id__icontains=filter_param) |
            Q(name__icontains=filter_param) |
            Q(phone__icontains=filter_param) |
            Q(state__icontains=filter_param)
        )

    drivers = drivers.order_by(order_by)

    # 페이지네이션 (10개씩 나누기)
    paginator = Paginator(drivers, 10)
    try:
        drivers_page = paginator.page(page)
    except PageNotAnInteger:
        drivers_page = paginator.page(1)
    except EmptyPage:
        drivers_page = paginator.page(paginator.num_pages)

    # DriverSerializer 사용해 데이터 직렬화
    serializer = DriverSerializer(drivers_page, many=True, fields=['driver_id', 'name', 'phone', 'updated_at', 'state', 'thumbnail'])
    data = serializer.data

    # 각 드라이버의 'updated_at' 필드 변환
    for driver in data:
        iso_time_str = driver.get("updated_at", None)  # 예시로 'updated_at' 필드 사용
        if iso_time_str:
            dt = datetime.strptime(iso_time_str, '%Y-%m-%dT%H:%M:%SZ')
            readable_format = dt.strftime("%m월 %d일 %H:%M:%S")
            driver["updated_at"] = readable_format

    # Response 데이터 반환
    return Response({
        'page': int(page),  # 현재 페이지 번호 반환
        'total_pages': paginator.num_pages,  # 전체 페이지 수
        'total_drivers': paginator.count,  # 전체 드라이버 수
        'drivers': serializer.data  # 현재 페이지의 드라이버 데이터
    }, status=status.HTTP_200_OK)

# sorted transaction
@api_view(['GET'])
def get_sorted_transactions(request):
    order_by = request.query_params.get('order_by', 'transaction_id')  
    page = request.query_params.get('page', 1)  
    filter_param = request.query_params.get('filter', None)  

    transactions = Transaction.objects.all()

    if filter_param:
        transactions = transactions.filter(
            Q(transaction_id__icontains=filter_param) |
            Q(driver_id__driver_id__icontains=filter_param) |
            Q(truck_id__icontains=filter_param) |
            Q(equipment_id__icontains=filter_param) |
            Q(child_equipment_id__icontains=filter_param) |
            Q(source__yard_id__icontains=filter_param) |
            Q(destination__yard_id__icontains=filter_param) |
            Q(state__icontains=filter_param)
        )

    transactions = transactions.order_by(order_by)

    # 페이지네이션 (10개씩 나누기)
    paginator = Paginator(transactions, 10)
    try:
        transactions_page = paginator.page(page)
    except PageNotAnInteger:
        transactions_page = paginator.page(1)
    except EmptyPage:
        transactions_page = paginator.page(paginator.num_pages)

    serializer = TransactionSerializer(transactions_page, many=True)
    data = serializer.data

    # 각 트랜잭션의 'updated_at' 필드 변환
    for transaction in data:
        iso_time_str = transaction.get("updated_at", None)  
        if iso_time_str:
            dt = datetime.strptime(iso_time_str, '%Y-%m-%dT%H:%M:%SZ')
            readable_format = dt.strftime("%m월 %d일 %H:%M:%S")
            transaction["updated_at"] = readable_format

    return Response({
        'page': int(page),  # 현재 페이지 번호 반환
        'total_pages': paginator.num_pages,  # 전체 페이지 수
        'total_transactions': paginator.count,  # 전체 트랜잭션 수
        'transactions': serializer.data  # 현재 페이지의 트랜잭션 데이터
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_driver_details(request):
    # 쿼리 파라미터에서 driver_id 가져오기
    driver_id = request.query_params.get('driver_id')
    
    # driver_id가 없을 때의 처리
    if not driver_id:
        return Response({"error": "driver_id 파라미터가 필요합니다."}, status=status.HTTP_400_BAD_REQUEST)

    # driver_id로 드라이버 찾기 (존재하지 않으면 404 에러 발생)
    driver = get_object_or_404(Driver, pk=driver_id)
    
    # 직렬화 시 'thumbnail'을 제외한 필드만 포함
    serializer = DriverSerializer(driver, exclude_fields=['thumbnail'])
    
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def create_driver(request):
    serializer = DriverSerializer(data=request.data)
    if serializer.is_valid():
        try:
            # Base64 이미지와 썸네일 디코딩 후 저장
            image_data = request.data.get('image')
            thumbnail_data = request.data.get('thumbnail')
            
            if image_data:
                
                image_file = base64.b64decode(image_data)
                print("Decoded Image File:", image_file)  # 디버그: 디코딩 결과 확인
                serializer.validated_data['image'] = image_file

            if thumbnail_data:
                thumbnail_file = base64.b64decode(thumbnail_data)
                print("Decoded Thumbnail File:", thumbnail_file)  # 디버그: 디코딩 결과 확인
                serializer.validated_data['thumbnail'] = thumbnail_file

            print("Validated Data Before Save:", serializer.validated_data)  # 디버그: 저장 전 데이터 확인
            # 드라이버 데이터 저장
            driver = serializer.save()

            return Response({
                'message': 'Driver created successfully!',
                'driver': DriverSerializer(driver).data
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            print("Error during image decoding or saving:", e)  # 에러 출력
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    print("Serializer Errors:", serializer.errors)  # 유효성 검사 오류 출력
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Transaction
@api_view(['GET', 'POST'])
def get_transactions(request):
    if request.method == 'GET':
        transactions = Transaction.objects.all()
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

#GetUpdatedEquipments
@api_view(['GET'])
def get_updated_equipments(request):
    # try:
        # 쿼리 파라미터에서 yard_id와 updated_at 가져오기
        yard_id = request.query_params.get('yard_id')
        updated_at = request.query_params.get('updated_at', datetime(2000,1,1))
        
        if not yard_id:
            return Response({'error': 'yard_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Slot 테이블에서 주어진 yard_id에 해당하는 slot_id 가져오기
        slot_ids = list(Slot.objects.filter(yard_id=yard_id).values_list('slot_id', flat=True))

        # 각 테이블(Truck, Chassis, Container, Trailer)에서 해당 slot_id와 updated_at 이후의 레코드 조회
        trucks = Truck.objects.filter(slot_id__in=slot_ids)#, updated_at__gt=updated_at)
        chassis = Chassis.objects.filter(slot_id__in=slot_ids)#, updated_at__gt=updated_at)
        containers = Container.objects.filter(slot_id__in=slot_ids)#, updated_at__gt=updated_at)
        trailers = Trailer.objects.filter(slot_id__in=slot_ids)#, updated_at__gt=updated_at)

        # 각 시리얼라이저를 사용해 데이터를 직렬화
        truck_serializer = TruckSerializer(trucks, many=True)
        chassis_serializer = ChassisSerializer(chassis, many=True)
        container_serializer = ContainerSerializer(containers, many=True)
        trailer_serializer = TrailerSerializer(trailers, many=True)
        # 모든 slot_id 중에서 비어 있는 슬롯을 식별
        occupied_slot_ids = set()
        # print(truck_serializer.data)
        occupied_slot_ids.update([data['slot'] for data in truck_serializer.data])
        occupied_slot_ids.update([data['slot'] for data in chassis_serializer.data])
        occupied_slot_ids.update([data['slot'] for data in container_serializer.data])
        occupied_slot_ids.update([data['slot'] for data in trailer_serializer.data])

        empty_slot_ids = [slot_id for slot_id in slot_ids if slot_id not in occupied_slot_ids]
        empty_slots = [{"slot_id":slot_id} for slot_id in empty_slot_ids]

        # 각 시리얼라이저를 사용해 데이터를 직렬화
        truck_serializer_time = TruckSerializer(trucks.filter(updated_at__gt=updated_at), many=True)
        chassis_serializer_time = ChassisSerializer(chassis.filter(updated_at__gt=updated_at), many=True)
        container_serializer_time = ContainerSerializer(containers.filter(updated_at__gt=updated_at), many=True)
        trailer_serializer_time = TrailerSerializer(trailers.filter(updated_at__gt=updated_at), many=True)
        # print(empty_slots)

        # 업데이트된 시간 수집
        all_updated_times = []
        all_updated_times += [data['updated_at'] for data in truck_serializer_time.data]
        all_updated_times += [data['updated_at'] for data in chassis_serializer_time.data]
        all_updated_times += [data['updated_at'] for data in container_serializer_time.data]
        all_updated_times += [data['updated_at'] for data in trailer_serializer_time.data]

        # all_updated_times에서 가장 큰 값을 찾음
        max_updated_time = max(all_updated_times) if all_updated_times else None

        # 모든 데이터를 합쳐서 반환
        combined_data = {
            "count": len(truck_serializer_time.data) + len(chassis_serializer_time.data) + len(container_serializer_time.data) + len(trailer_serializer_time.data),
            "updated_time": max_updated_time,
            'data': {
                'trucks': truck_serializer.data,
                'chassis': chassis_serializer.data,
                'containers': container_serializer.data,
                'trailers': trailer_serializer.data,
                "empty" : empty_slots
            }
        }

        return Response(combined_data, status=status.HTTP_200_OK)
    
    # except Exception as e:
    #     return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Truck
@api_view(['GET', 'POST'])
def get_trucks(request):
    if request.method == 'GET':
        trucks = Truck.objects.all()
        serializer = TruckSerializer(trucks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = TruckSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Chassis
@api_view(['GET', 'POST'])
def get_chassis(request):
    if request.method == 'GET':
        chassis = Chassis.objects.all()
        serializer = ChassisSerializer(chassis, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = ChassisSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def execute_sql_query(query, params):
    """
    SQL 쿼리 실행하는 함수
    Args:
        query (str): 실행할 SQL 쿼리
        params (list): 쿼리에 전달할 파라미터

    Returns:
        None
    """
    with connection.cursor() as cursor:
        cursor.execute(query, params)

# chassis_flip_sql
@api_view(['POST'])
def chassis_flip_sql(request):
    """
    Args:
        chassis_id1 (str): The source chassis ID.
        chassis_id2 (str): The destination chassis ID.

    Returns:
        Response: A JSON response with a success message or an error.
    """
    # chassis_id1, chassis_id2 가져오기
    chassis_id1 = request.data.get('chassis_id1')
    chassis_id2 = request.data.get('chassis_id2')

    if not chassis_id1 or not chassis_id2:
        return Response({"error": "chassis_id1 and chassis_id2 are required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        query1 = """
            UPDATE api_chassis
            SET container_id = (
                SELECT t.container_id 
                FROM (SELECT container_id FROM api_chassis WHERE chassis_id = %s) AS t
            )
            WHERE chassis_id = %s;
        """
        execute_sql_query(query1, [chassis_id1, chassis_id2])

        query2 = """
            UPDATE api_chassis 
            SET container_id = NULL 
            WHERE chassis_id = %s;
        """
        execute_sql_query(query2, [chassis_id1])

        return Response({"message": "Chassis flip successfully executed."}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
# Container
@api_view(['GET', 'POST'])
def get_containers(request):
    if request.method == 'GET':
        containers = Container.objects.all()
        serializer = ContainerSerializer(containers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = ContainerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Trailer
@api_view(['GET', 'POST'])
def get_trailers(request):
    if request.method == 'GET':
        trailers = Trailer.objects.all()
        serializer = TrailerSerializer(trailers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = TrailerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Maintenance
@api_view(['GET', 'POST'])
def get_maintenances(request):
    if request.method == 'GET':
        maintenances = Maintenance.objects.all()
        serializer = MaintenanceSerializer(maintenances, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = MaintenanceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# SlotUpdate
@api_view(['GET', 'POST'])
def get_slot_updates(request):
    if request.method == 'GET':
        slot_updates = SlotUpdate.objects.all()
        serializer = SlotUpdateSerializer(slot_updates, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = SlotUpdateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# set_destination_slot
@api_view(['POST'])
def set_destination_slot(request):
    transaction_id = request.data.get('transaction_id')
    destination_slot = request.data.get('destination_slot')

    if not transaction_id or not destination_slot:
        return Response({"error": "transaction_id and destination_slot are required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        query = """
            UPDATE api_transaction
            SET destination_slot = %s
            WHERE transaction_id = %s;
        """
        execute_sql_query(query, [destination_slot, transaction_id])

        return Response({"message": "Destination slot updated successfully."}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# YardSlotInfo
@api_view(['GET'])
def get_yard_slot_info(request):
    try:
        # 쿼리 파라미터에서 yard_id 가져오기
        yard_id = request.query_params.get('yard_id')
        if not yard_id:
            return Response({'error': 'yard_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        # SQL 쿼리 작성 - min_x, min_y, max_x, max_y 계산
        sql = """
            SELECT LEAST(parking_min.min_x, structure_min.min_x) AS min_x,
                   LEAST(parking_min.min_y, structure_min.min_y) AS min_y,
                   GREATEST(parking_max.max_x, structure_max.max_x) AS max_x,
                   GREATEST(parking_max.max_y, structure_max.max_y) AS max_y
            FROM
                (SELECT MIN(x) AS min_x, MIN(y) AS min_y FROM api_slot WHERE yard_id = %s) AS parking_min,
                (SELECT MIN(x) AS min_x, MIN(y) AS min_y FROM api_structure WHERE yard_id = %s) AS structure_min,
                (SELECT MAX(x + w) AS max_x, MAX(y + h) AS max_y FROM api_slot WHERE yard_id = %s) AS parking_max,
                (SELECT MAX(x + w) AS max_x, MAX(y + h) AS max_y FROM api_structure WHERE yard_id = %s) AS structure_max;
        """

        # 데이터베이스 연결 및 쿼리 실행
        with connection.cursor() as cursor:
            cursor.execute(sql, [yard_id, yard_id, yard_id, yard_id])
            row = cursor.fetchone()

        # 결과가 존재하지 않을 때 처리
        if not row:
            return Response({'error': 'No data found for the given yard_id'}, status=status.HTTP_404_NOT_FOUND)

        # 응답 데이터 작성 (min/max 좌표 정보)
        response_data = {
            'min_x': row[0],
            'min_y': row[1],
            'max_x': row[2],
            'max_y': row[3]
        }

        # Slot 테이블에서 모든 데이터를 가져오기
        slot_data = Slot.objects.filter(yard_id=yard_id)
        slot_serializer = SlotSerializer(slot_data, many=True)
        response_data['slot_data'] = slot_serializer.data

        # Structure 테이블에서 모든 데이터를 가져오기
        structure_data = Structure.objects.filter(yard_id=yard_id)
        structure_serializer = StructureSerializer(structure_data, many=True)
        response_data['structure_data'] = structure_serializer.data

        return Response(response_data, status=status.HTTP_200_OK)

    except Exception as e:
        # 오류 발생 시 에러 메시지 반환
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
# get_equipment_details
@api_view(['GET'])
def get_equipment_details(request):
    # Retrieve equipment_id from query parameters
    equipment_id = request.query_params.get('equipment_id')
    
    # Handle missing equipment_id
    if not equipment_id:
        return Response({"error": "equipment_id 파라미터가 필요합니다."}, status=status.HTTP_400_BAD_REQUEST)

    # Search for the equipment based on equipment_id
    equipment1 = Truck.objects.filter(truck_id=equipment_id).first()
    equipment2 = Chassis.objects.filter(chassis_id=equipment_id).first()
    equipment3 = Container.objects.filter(container_id=equipment_id).first()
    equipment4 = Trailer.objects.filter(trailer_id=equipment_id).first()

    # Check each equipment type and serialize
    if equipment1:
        serializer = TruckSerializer(equipment1)  # No `many=True` for single instance
        return Response({"type": "truck", "data": serializer.data}, status=status.HTTP_200_OK)
    elif equipment2:
        serializer = ChassisSerializer(equipment2)
        # if serializer.data.get("container_id",None):
        container = ContainerSerializer(Container.objects.filter(container_id = serializer.data['container_id']).first()).data
        serializer.data['container']=container
        return Response({"type": "chassis", "data": serializer.data,'container':container}, status=status.HTTP_200_OK)
    elif equipment3:
        serializer = ContainerSerializer(equipment3)
        return Response({"type": "container", "data": serializer.data}, status=status.HTTP_200_OK)
    elif equipment4:
        serializer = TrailerSerializer(equipment4)
        return Response({"type": "trailer", "data": serializer.data}, status=status.HTTP_200_OK)
    
    # If no equipment is found, return a 404 response
    return Response({"error": "장비를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

# move equipment
@api_view(['POST'])
def move_equipment(request):
    """
    Yard 내부에서 Truck 또는 Trailer 등의 장비 이동
    """
    # 입력 파라미터 가져오기
    equipment_id = request.data.get('equipment_id')
    source_slot_id = request.data.get('source_slot_id')
    destination_slot_id = request.data.get('destination_slot_id')

    # 입력값 검증
    if not all([equipment_id, source_slot_id, destination_slot_id]):
        return Response({"error": "equipment_id, source_slot_id, and destination_slot_id are required."}, 
                        status=status.HTTP_400_BAD_REQUEST)

    try:
        # 장비 조회 (Truck 또는 Trailer)
        equipment = (Truck.objects.filter(truck_id=equipment_id).first() or
                     Trailer.objects.filter(trailer_id=equipment_id).first() or
                     Chassis.objects.filter(chassis_id=equipment_id).first() or
                     Container.objects.filter(container_id=equipment_id).first())
        
        if not equipment:
            return Response({"error": "Equipment not found."}, status=status.HTTP_404_NOT_FOUND)

        # 현재 슬롯 확인
        if str(equipment.slot_id) != str(source_slot_id):
            return Response({"error": f"Equipment is not located in source_slot_id: {source_slot_id}."}, 
                            status=status.HTTP_400_BAD_REQUEST)

        # 목표 슬롯 확인
        destination_slot = Slot.objects.filter(slot_id=destination_slot_id).first()
        if not destination_slot:
            return Response({"error": f"Destination slot {destination_slot_id} does not exist."}, 
                            status=status.HTTP_404_NOT_FOUND)
        
        if (Truck.objects.filter(slot_id=destination_slot_id).first() or
            Trailer.objects.filter(slot_id=destination_slot_id).first() or
            Chassis.objects.filter(slot_id=destination_slot_id).first() or
            Container.objects.filter(slot_id=destination_slot_id).first()):
        # if destination_slot.occupied:
            return Response({"error": f"Destination slot {destination_slot_id} is already occupied."}, 
                            status=status.HTTP_400_BAD_REQUEST)

        # 슬롯 이동
        equipment.slot_id = destination_slot_id
        equipment.updated_at = now()
        equipment.save()

        # 결과 반환
        return Response({
            "message": "Equipment moved successfully.",
            "equipment_id": equipment_id,
            "source_slot_id": source_slot_id,
            "destination_slot_id": destination_slot_id
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# SlotIsUpdated
@api_view(['GET'])
def get_slot_isupdated(request):
    # 쿼리 파라미터에서 yard_id와 updated_time 가져오기
    yard_id = request.query_params.get('yard_id')
    updated_time_str = request.query_params.get('updated_time', '2000-01-01T00:00:00Z')  # 기본값 설정

    # yard_id가 없는 경우 에러 반환
    if not yard_id:
        return Response({'error': 'yard_id is required'}, status=status.HTTP_400_BAD_REQUEST)

    # updated_time 파싱
    try:
        updated_time = datetime.strptime(updated_time_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    except ValueError:
        return Response({"error": "Invalid updated_time format. Use ISO format, e.g., 2024-11-01T10:00:00Z"}, status=status.HTTP_400_BAD_REQUEST)

    # yard_id와 updated_time 이후에 업데이트된 Slot 존재 여부 확인
    slots_updated = Slot.objects.filter(yard_id=yard_id, updated_at__gt=updated_time).exists()

    # yard_id에 해당하는 모든 슬롯의 updated_at 필드에서 가장 최근 시간 계산
    all_updated_times = Slot.objects.filter(yard_id=yard_id).values_list('updated_at', flat=True)
    max_updated_time = max(all_updated_times) if all_updated_times else None

    # 업데이트 여부를 result 필드로 반환
    return Response({
        "result": slots_updated,
        "last_time": max_updated_time
    }, status=status.HTTP_200_OK)


# CurrentSlotState
@api_view(['GET'])
def current_slot_state(request):
    # 쿼리 파라미터에서 yard_id 가져오기
    yard_id = request.query_params.get('yard_id')
    
    # yard_id가 없는 경우 에러 반환
    if not yard_id:
        return Response({'error': 'yard_id is required'}, status=status.HTTP_400_BAD_REQUEST)

    # Slot 테이블에서 주어진 yard_id에 해당하는 slot_id 가져오기
    slot_ids = list(Slot.objects.filter(yard_id=yard_id).values_list('slot_id', flat=True))

    # 각 테이블에서 해당 slot_id를 가진 모든 레코드 조회
    trucks = Truck.objects.filter(slot_id__in=slot_ids)
    chassis = Chassis.objects.filter(slot_id__in=slot_ids)
    containers = Container.objects.filter(slot_id__in=slot_ids)
    trailers = Trailer.objects.filter(slot_id__in=slot_ids)

    # 각 시리얼라이저를 사용해 데이터를 직렬화
    truck_serializer = TruckSerializer(trucks, many=True)
    chassis_serializer = ChassisSerializer(chassis, many=True)
    container_serializer = ContainerSerializer(containers, many=True)
    trailer_serializer = TrailerSerializer(trailers, many=True)

    # 모든 slot_id 중에서 비어 있는 슬롯을 식별
    occupied_slot_ids = set()
    occupied_slot_ids.update([data['slot'] for data in truck_serializer.data])
    occupied_slot_ids.update([data['slot'] for data in chassis_serializer.data])
    occupied_slot_ids.update([data['slot'] for data in container_serializer.data])
    occupied_slot_ids.update([data['slot'] for data in trailer_serializer.data])

    empty_slot_ids = [slot_id for slot_id in slot_ids if slot_id not in occupied_slot_ids]
    empty_slots = [{"slot_id": slot_id} for slot_id in empty_slot_ids]

    in_scheduled_equipment_slot_ids = Transaction.objects.filter(destination_equipment_slot__isnull=False)
    in_scheduled__child_slot_ids = Transaction.objects.filter(destination_child_equipment_slot__isnull=False)
    in_scheduled_slot_ids = Transaction.objects.filter(destination_slot__isnull=False)

    in_scheduled_slot_ids = set([transaction.destination_slot for transaction in in_scheduled_slot_ids]+[transaction.destination_equipment_slot for transaction in in_scheduled_equipment_slot_ids]+[transaction.destination_child_equipment_slot for transaction in in_scheduled__child_slot_ids])
    empty_slots = [{"slot_id": slot_id, "state":"In-Scheduled" if slot_id in in_scheduled_slot_ids else "empty"} for slot_id in empty_slot_ids]
    empty_slots = [{"slot_id": slot_id, "state":"In-Scheduled" if slot_id in in_scheduled_slot_ids else str(in_scheduled_slot_ids)} for slot_id in empty_slot_ids]
    
    # 모든 데이터를 합쳐서 반환
    combined_data = {
        "data": {
            "trucks": [
                {
                    "truck_id": truck["truck_id"],
                    "state": truck["state"],
                    "created_at": truck["created_at"],
                    "updated_at": truck["updated_at"],
                    "slot": truck["slot"],
                    "size": truck['size']
                }
                for truck in truck_serializer.data
            ],
            "chassis": [
                {
                    "chassis_id": chassis["chassis_id"],
                    "state": chassis["state"],
                    "container_id": chassis["container_id"],
                    "created_at": chassis["created_at"],
                    "updated_at": chassis["updated_at"],
                    "slot": chassis["slot"],
                    "size": chassis["size"]
                }
                for chassis in chassis_serializer.data
            ],
            "containers": [
                {
                    "container_id": container["container_id"],
                    "state": container["state"],
                    "size": container["size"],
                    "created_at": container["created_at"],
                    "updated_at": container["updated_at"],
                    "slot": container["slot"]
                }
                for container in container_serializer.data
            ],
            "trailers": [
                {
                    "trailer_id": trailer["trailer_id"],
                    "state": trailer["state"],
                    "size": trailer["size"],
                    "created_at": trailer["created_at"],
                    "updated_at": trailer["updated_at"],
                    "slot": trailer["slot"]
                }
                for trailer in trailer_serializer.data
            ],
            "empty": empty_slots
        }
    }

    return Response(combined_data, status=status.HTTP_200_OK)

# Sorted Equipment with validation
@api_view(['GET'])
def get_sorted_equipments(request):
    # Define common fields for validation

    # Retrieve query parameters
    order_by = request.query_params.get('order_by', 'updated_at')
    order_type = request.query_params.get('order_type', 'asc')
    
    page = int(request.query_params.get('page', 1))-1
    filter_param = request.query_params.get('filter', '') 
    with connection.cursor() as cursor:
            cursor.execute(f"""SELECT 
                                t.id, 
                                t.vehicle, 
                                t.slot_id,
                                t.size, 
                                CONCAT(api_slot.yard_id, '-', api_slot.slot_num) AS location,
                                t.connect,
                                t.state, 
                                t.updated_at
                           FROM (
                                SELECT chassis_id AS id, 'chassis' AS vehicle,size, slot_id, updated_at, state,container_id AS connect FROM api_chassis
                                UNION
                                SELECT trailer_id AS id, 'trailer' AS vehicle,size, slot_id, updated_at, state,Null AS connect FROM api_trailer
                                UNION
                                SELECT truck_id AS id, 'truck' AS vehicle,size, slot_id, updated_at, state,Null AS connect FROM api_truck
                                UNION
                                SELECT container_id AS id, 'container' AS vehicle,size, slot_id, updated_at, state,Null AS connect FROM api_container
                            ) as t
                            JOIN api_slot
                            ON t.slot_id = api_slot.slot_id
                            WHERE 
                                t.id LIKE '%{filter_param}%' OR
                                t.vehicle LIKE '%{filter_param}%' OR
                                t.slot_id LIKE '%{filter_param}%' OR
                                CONCAT(api_slot.yard_id, '-', api_slot.slot_num) LIKE '%{filter_param}%' OR
                                t.state LIKE '%{filter_param}%' OR
                                t.updated_at LIKE '%{filter_param}%'
                            order by {order_by} {order_type};
                            """)

            # rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            # 데이터 매핑 (딕셔너리로 변환)
            rows = [dict(zip(columns, row)) for row in cursor.fetchall()]

    # Validate order_by field
    # if order_by not in valid_order_fields:
    #     return Response({
    #         'error': f"Invalid order_by field. Allowed fields are: {', '.join(valid_order_fields)}"
    #     }, status=status.HTTP_400_BAD_REQUEST)

    # Combine equipment data from all models
    # all_equipments = [
    #     {"type": "truck", "data": truck} for truck in Truck.objects.all()
    # ] + [
    #     {"type": "chassis", "data": chassis} for chassis in Chassis.objects.all()
    # ] + [
    #     {"type": "container", "data": container} for container in Container.objects.all()
    # ] + [
    #     {"type": "trailer", "data": trailer} for trailer in Trailer.objects.all()
    # ]

    # if filter_param:
    #     all_equipments = [
    #         equipment for equipment in all_equipments
    #         if filter_param.lower() in str(equipment["data"]).lower()
    #     ]

    # # Apply sorting based on the provided order_by field
    # all_equipments.sort(key=lambda x: getattr(x["data"], order_by, None))

    # # Apply pagination
    total_equipments = len(rows)
    total_pages = total_equipments//10
    equipment = rows[10*page:10*page+10]
    return Response({
        'page': int(page),
        'total_pages': total_pages,
        'total_equipments': total_equipments,
        'equipments': equipment,
    }, status=status.HTTP_200_OK)

# driver-details-history
@api_view(['GET'])
def driver_transaction_history(request):
    # 쿼리 파라미터에서 driver_id 가져오기
    driver_id = request.query_params.get('driver_id')
    
    # driver_id 제공되지 않으면 에러
    if not driver_id:
        return Response({"error": "Please enter the Driver ID."}, status=status.HTTP_400_BAD_REQUEST)
    
    # driver_id에 해당하는 Transaction 조회
    transactions = Transaction.objects.filter(driver_id=driver_id).select_related('driver', 'source', 'destination').order_by('-created_at')
    
    # 조회된 Transaction 없으면 404
    if not transactions.exists():
        return Response({"error": "There are no transactions for that Driver ID."}, status=status.HTTP_404_NOT_FOUND)
    
    # 응답 데이터 생성
    transaction_list = []
    for txn in transactions:
        transaction_data = {
            "transaction_id": txn.transaction_id,
            "driver_id": txn.driver.driver_id,
            "driver_name": txn.driver.name,
            "truck_id": txn.truck_id,
            "equipment_id": txn.equipment_id,
            "child_equipment_id": txn.child_equipment_id,
            "source": {
                "yard_id": txn.source.yard_id if txn.source else None,
                "yard_name": txn.source.yard_name if txn.source else None
            } if txn.source else None,
            "destination": {
                "yard_id": txn.destination.yard_id if txn.destination else None,
                "yard_name": txn.destination.yard_name if txn.destination else None
            } if txn.destination else None,
            "datetime": txn.datetime.isoformat(),
            "created_at": txn.created_at.isoformat()
        }
        transaction_list.append(transaction_data)
    
    return Response(transaction_list, status=status.HTTP_200_OK)


@api_view(['GET'])
def equipment_transaction_history(request):
    # 쿼리 파라미터에서 driver_id 가져오기
    equipment_id = request.query_params.get('equipment_id')
    
    # driver_id 제공되지 않으면 에러
    if not equipment_id:
        return Response({"error": "Please enter the Equipment ID."}, status=status.HTTP_400_BAD_REQUEST)
    
    # driver_id에 해당하는 Transaction 조회
    transactions = (
    Transaction.objects.filter(
        Q(truck_id=equipment_id) |
        Q(equipment_id=equipment_id) |
        Q(child_equipment_id=equipment_id)
    )
    # .select_related('driver', 'source', 'destination')
    .order_by('-created_at')
)
    
    # 조회된 Transaction 없으면 404
    if not transactions.exists():
        return Response({"error": "There are no transactions for that Driver ID."}, status=status.HTTP_404_NOT_FOUND)
    
    # 응답 데이터 생성
    transaction_list = []
    for txn in transactions:
        transaction_data = {
            "transaction_id": txn.transaction_id,
            "driver_id": txn.driver.driver_id,
            "driver_name": txn.driver.name,
            "truck_id": txn.truck_id,
            "equipment_id": txn.equipment_id,
            "child_equipment_id": txn.child_equipment_id,
            "source": {
                "yard_id": txn.source.yard_id if txn.source else None,
                "yard_name": txn.source.yard_name if txn.source else None
            } if txn.source else None,
            "destination": {
                "yard_id": txn.destination.yard_id if txn.destination else None,
                "yard_name": txn.destination.yard_name if txn.destination else None
            } if txn.destination else None,
            "datetime": txn.datetime.isoformat(),
            "created_at": txn.created_at.isoformat()
        }
        transaction_list.append(transaction_data)
    
    return Response(transaction_list, status=status.HTTP_200_OK)


# 사용자 회원가입
@api_view(['POST'])
def user_signup(request):
    data = request.data.copy()
    try:
        # password 암호화
        data['password_hash'] = make_password(data['password'])
        
        del data['password']
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully!"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 사용자 로그인
@api_view(['POST'])
def user_login(request):
    try:
        id = request.data.get('id')
        password = request.data.get('pw')
        
        user = User.objects.filter(id=id).first()
        if not user:
            return Response({"error": "Invalid ID or password"}, status=status.HTTP_401_UNAUTHORIZED)

        # Check if the password matches
        if not check_password(password, user.password):
            return Response({"error": "Invalid ID or password"}, status=status.HTTP_401_UNAUTHORIZED)

        # Generate JWT Token
        token = jwt.encode({'id': user.id}, settings.SECRET_KEY, algorithm='HS256')
        
        return Response({"message": "Login successful", "token": token}, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def server_status(request):
    # CPU와 메모리 사용량 정보를 가져오기
    cpu_usage = psutil.cpu_percent(interval=1)  # 1초 동안 CPU 사용률 측정
    memory = psutil.virtual_memory()  # 메모리 정보 가져오기
    disk = psutil.disk_usage('/')  # 디스크 사용량 가져오기

    # 상태 정보를 JSON으로 응답
    context = {
        'cpu_usage': cpu_usage,
        'memory': {
            'total': memory.total,
            'available': memory.available,
            'percent': memory.percent,
            'used': memory.used,
            'free': memory.free
        },
        'disk': {
            'total': disk.total,
            'used': disk.used,
            'free': disk.free,
            'percent': disk.percent
        }
    }
    
    # HTML 페이지에 데이터를 전달
    return render(request, 'server_status.html', context)


#RecentTransaction
@api_view(['GET'])
def get_recent_transaction(request):
    # 쿼리 파라미터에서 가져올 트랜잭션 개수 가져오기 (기본값: 7)
    n = int(request.query_params.get('n', 7))

    # 지정된 yard_ids에서 source_id 또는 destination_id가 일치하는 최근 트랜잭션 n개를 필터링
    transactions = Transaction.objects.order_by('-datetime')[:n]
    data = TransactionSerializer(transactions, many=True).data

    return Response(data, status=status.HTTP_200_OK)


# TMS current_map
@api_view(['GET'])
def get_current_map(request):
    transaction_id = request.query_params.get('transaction_id', None)

    if not transaction_id:
        return Response({
            "error": "Required parameters are missing.: transaction_id"
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT yard_id, lat, lon
                FROM api_yard
                WHERE yard_id IN (
                    SELECT source_id 
                    FROM api_transaction 
                    WHERE transaction_id = %s
                    UNION
                    SELECT destination_id 
                    FROM api_transaction 
                    WHERE transaction_id = %s
                );
            """, [transaction_id, transaction_id])

            rows = cursor.fetchall()

        results = [{"yard_id": row[0], "lat": row[1], "lon": row[2]} for row in rows]

        if len(results) < 2:
            return Response({
                "error": "There is not enough data to calculate a midway point. At a minimum, a starting point and a destination are required."
            }, status=status.HTTP_400_BAD_REQUEST)

        # 중간 위치 계산 (위도, 경도 평균값)
        avg_lat = sum(float(item["lat"]) for item in results) / len(results)
        avg_lon = sum(float(item["lon"]) for item in results) / len(results)

        # "NOW"로 현재 차량 위치 추가
        results.append({
            "yard_id": "NOW",
            "lat": round(avg_lat, 6),
            "lon": round(avg_lon, 6)
        })

        return Response({"yards": results}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({
            "error": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def update_weather(request):
    # 요청 데이터에서 날씨 정보 추출
    yards = Yard.objects.all()
    for yard in yards:
        try:
            lat = yard.lat
            lon = yard.lon
            url = f"https://api.openweathermap.org/data/3.0/onecall?units=metric&lat={lat}&lon={lon}&appid=fddd33a3fcc06aa00b5efcc7163f95ca"
            weather_data = requests.get(url).json()
            print(weather_data)
            temperature = weather_data['current']['temp']
            weather = weather_data['current']['weather'][0]['icon']
            yard.weather = weather
            yard.temperature = temperature
            yard.save()
        except:
            pass
    return Response({'message': 'Weather data updated successfully'}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def get_weather(request):
    # icon을 내림차순해서 순서대로 4개만
    yards = Yard.objects.all().order_by('-weather')[:4]
    serializer = YardAllSerializer(yards, many=True)  
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_today_summary(request):
    # datetime 필드의 날짜가 오늘이거나 datetime_end 필드의 날짜가 오늘인 경우
    today_transactions = Transaction.objects.filter(Q(datetime__date=date.today()) | Q(datetime_end__date=date.today()))
    # 'Reservation','Processing','End'
    today_summery = {
        'Total': today_transactions.count(),
        'Reservation': today_transactions.filter(state='Reservation').count(),
        'Processing': today_transactions.filter(state='Processing').count(),
        'End': today_transactions.filter(state='End').count()
    }
    return Response(today_summery, status=status.HTTP_200_OK)



@api_view(['GET'])
def get_processing_transaction(request):
    # Define common fields for validation

    with connection.cursor() as cursor:
            cursor.execute(f"""select transaction_id, datetime,source_id, destination_id from api_transaction where state = 'Processing' order by datetime limit 6;
                            """)

            # rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            # 데이터 매핑 (딕셔너리로 변환)
            rows = [dict(zip(columns, row)) for row in cursor.fetchall()]

    return Response({'data':rows,}, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_livemap_not_end(request):
    # Define common fields for validation
    yard_id = request.query_params.get('yard_id')
    with connection.cursor() as cursor:
            cursor.execute(f"""select * from api_transaction where state !="End" and destination_id="{yard_id}" order by destination_slot asc;""")

            # rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            # 데이터 매핑 (딕셔너리로 변환)
            rows = [dict(zip(columns, row)) for row in cursor.fetchall()]

    return Response({'data':rows,}, status=status.HTTP_200_OK)
