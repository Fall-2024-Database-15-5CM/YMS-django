from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User, Division, Yard, Slot, Structure, Driver, Transaction, Truck, Chassis, Container, Trailer, Maintenance, SlotUpdate
from .serializer import UserSerializer, DivisionSerializer, YardSerializer, SlotSerializer, StructureSerializer, DriverSerializer, TransactionSerializer, TruckSerializer, ChassisSerializer, ContainerSerializer, TrailerSerializer, MaintenanceSerializer, SlotUpdateSerializer
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import base64
from datetime import datetime
from django.core.files.base import ContentFile
from django.db.models import Min, Max, F
from django.db import connection
from django.shortcuts import get_object_or_404


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
# Slot


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
    order_by = request.query_params.get('order_by', 'name')  # 기본 정렬 필드
    page = request.query_params.get('page', 1)  # 기본 페이지 번호
    # Driver 쿼리셋 정렬 적용
    drivers = Driver.objects.all().order_by(order_by)

    # 페이지네이션 (8개씩 나누기)
    paginator = Paginator(drivers, 12)
    try:
        drivers_page = paginator.page(page)
    except PageNotAnInteger:
        drivers_page = paginator.page(1)
    except EmptyPage:
        drivers_page = paginator.page(paginator.num_pages)
    

    serializer = DriverSerializer(drivers_page, many=True, fields=['driver_id', 'name', 'phone', 'updated_at', 'state', 'thumbnail'])
    data = serializer.data

    # 각 드라이버의 'created_at' 필드 변환
    for driver in data:
        iso_time_str = driver.get("updated_at", None)  # 예시로 'updated_at' 필드 사용
        if iso_time_str:
            dt = datetime.strptime(iso_time_str, "%Y-%m-%dT%H:%M:%S.%fZ")
            readable_format = dt.strftime("%m월 %d일 %H:%M:%S")
            driver["updated_at"] = readable_format


    return Response({
        'page': int(page),  # 현재 페이지 번호 반환
        'total_pages': paginator.num_pages,  # 전체 페이지 수
        'total_drivers': paginator.count,  # 전체 드라이버 수
        'drivers': serializer.data  # 현재 페이지의 드라이버 데이터
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
        return Response({"type": "chassis", "data": serializer.data}, status=status.HTTP_200_OK)
    elif equipment3:
        serializer = ContainerSerializer(equipment3)
        return Response({"type": "container", "data": serializer.data}, status=status.HTTP_200_OK)
    elif equipment4:
        serializer = TrailerSerializer(equipment4)
        return Response({"type": "trailer", "data": serializer.data}, status=status.HTTP_200_OK)
    
    # If no equipment is found, return a 404 response
    return Response({"error": "장비를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)


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
        updated_time = datetime.strptime(updated_time_str, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        return Response({"error": "Invalid updated_time format. Use ISO format, e.g., 2024-11-01T10:00:00Z"}, status=status.HTTP_400_BAD_REQUEST)

    # yard_id와 updated_time 이후에 업데이트된 Slot 존재 여부 확인
    slots_updated = Slot.objects.filter(yard_id=yard_id, updated_at__gt=updated_time).exists()

    # 업데이트 여부를 result 필드로 반환
    return Response({"result": slots_updated}, status=status.HTTP_200_OK)