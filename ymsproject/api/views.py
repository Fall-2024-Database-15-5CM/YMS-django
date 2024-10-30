from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User, Division, Yard, Slot, Structure, Driver, Transaction, Truck, Chassis, Container, Trailer, Maintenance, SlotUpdate
from .serializer import UserSerializer, DivisionSerializer, YardSerializer, SlotSerializer, StructureSerializer, DriverSerializer, TransactionSerializer, TruckSerializer, ChassisSerializer, ContainerSerializer, TrailerSerializer, MaintenanceSerializer, SlotUpdateSerializer
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import base64
from django.core.files.base import ContentFile
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
    order_by = request.query_params.get('order_by', 'name')  # 기본 정렬 필드
    page = request.query_params.get('page', 1)  # 기본 페이지 번호
    
    # Driver 쿼리셋 정렬 적용
    drivers = Driver.objects.all().order_by(order_by)

    # 페이지네이션 (8개씩 나누기)
    paginator = Paginator(drivers, 9)
    try:
        drivers_page = paginator.page(page)
    except PageNotAnInteger:
        drivers_page = paginator.page(1)
    except EmptyPage:
        drivers_page = paginator.page(paginator.num_pages)

    # 결과 직렬화 및 반환
    serializer = DriverSerializer(drivers_page, many=True)
    return Response({
        'page': int(page),  # 현재 페이지 번호 반환
        'total_pages': paginator.num_pages,  # 전체 페이지 수
        'total_drivers': paginator.count,  # 전체 드라이버 수
        'drivers': serializer.data  # 현재 페이지의 드라이버 데이터
    }, status=status.HTTP_200_OK)

@api_view(['POST'])
def create_driver(request):
    serializer = DriverSerializer(data=request.data)

    print(request)
    print(serializer)
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
