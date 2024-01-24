from django.db.models import Sum
from rest_framework.response import Response
from .serializers import RegisterSerializer, LoginSerializers, ActivitySerializer, PurchaseSerializer
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .models import Activity, Package, PurchaseActivity
from collections import Counter

# Create your views here.
class ResgistrationsView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'Msg': 'User register Successfully!', 'status': status.HTTP_200_OK})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializers(data=request.data)
        if serializer.is_valid():
            username = serializer.data['username']
            password = serializer.data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                token = RefreshToken.for_user(user)
                return Response({'refresh': str(token), 'access': str(token.access_token)}, status=200)
            else:
                return Response({'Msg': 'User login successfully!', 'status': status.HTTP_200_OK})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ActivityView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ActivitySerializer

    def get(self, request):
        user = request.user
        activity = Activity.objects.filter(user=user)
        serializer = self.serializer_class(activity, many=True)
        return Response(serializer.data, status=200)

    def post(self, request):
        user = request.user
        serializer = self.serializer_class(data=request.data)
        package = PurchaseActivity.objects.all().last()
        if package == None:
            return Response({'Msg': 'Please purchase new package'}, status=200)

        packages = package.grandtotal
        activity = Activity.objects.filter(user=user).count()

        if packages == activity:
            return Response({'msg': 'Package limit has ended please purchase a new package'}, status=200)

        if serializer.is_valid():
            serializer.save(user=user)
            return Response({'msg': 'Activity created successfully', 'status': status.HTTP_200_OK})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PurchaseView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PurchaseSerializer

    def get(self, request):
        user = request.user
        purchases = PurchaseActivity.objects.filter(user=user)
        response = Counter(obj.package.package_name for obj in purchases)
        # gold = PurchaseActivity.objects.filter(package__package_name__startswith="gold",user=user).count()
        # silver = PurchaseActivity.objects.filter(package__package_name__startswith="silver",user=user).count()
        # bronze = PurchaseActivity.objects.filter(package__package_name__startswith="bronze",user=user).count()
        # response ={"gold":gold,"silver":silver,"bronze":bronze}        
        return Response(response,status=200)

    def post(self, request):
        user = request.user
        serializer = self.serializer_class(data=request.data)
        packages = request.data['package']
        try:
            package = Package.objects.get(id=packages)
        except package.DoesNotExist:
                return Response({'msg': f'This {package} dose not exist!'},status=200)
        package_activity = package.total_activity
        total_activity_sum = PurchaseActivity.objects.filter(user=user).aggregate(
            Sum('total_activity'))['total_activity__sum'] or 0

        totalactivity = package_activity + total_activity_sum
        if serializer.is_valid():
            serializer.save(user=user, total_activity=package_activity, grandtotal=totalactivity)
            return Response({'msg': 'Package purchase successfully!', 'status': status.HTTP_200_OK})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
