from django.db.models import Sum
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from .serializers import RegisterSerializer, LoginSerializers, ActivitySerializer, PurchaseSerializer
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .models import Activity, Package, PurchaseActivity


# Create your views here.
class ResgistrationsView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Success data created', 'status': status.HTTP_200_OK})
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
                user = RefreshToken.for_user(user)
                return Response({'refresh': str(user), 'access': str(user.access_token), })
            else:
                return Response({'msg': 'user is Login', 'status': status.HTTP_200_OK})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ActivityView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        activity = Activity.objects.all()
        serializer = ActivitySerializer(activity, many=True)
        return Response(serializer.data, status=200)

    def post(self, request):
        user = request.user
        serializer = ActivitySerializer(data=request.data)
        package = PurchaseActivity.objects.all().last()
        if package == None:
            return Response({'msg': 'please purchase package'})
        else:
            pass
        packages = package.grandtotal
        print('-----------packages------------', packages)
        activity = Activity.objects.filter(user=user).count()
        print('------------------activity------------', activity)

        if packages == activity:
            return Response({'msg': 'your package limit is closed please purchase a new package'})

        if serializer.is_valid():
            serializer.save(user=user)
            return Response({'msg': 'Activity created sucessfully', 'status': status.HTTP_200_OK})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PurchaseView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        serializer = PurchaseSerializer(data=request.data)
        packages = request.data['package']
        package = Package.objects.get(id=packages)
        package_activity = package.total_activity
        total_activity_sum = PurchaseActivity.objects.filter(user=user).aggregate(
            Sum('total_activity'))['total_activity__sum'] or 0

        totalactivity = package_activity + total_activity_sum
        if serializer.is_valid():
            serializer.save(
                user=user, total_activity=package_activity, grandtotal=totalactivity)

            return Response({'msg': 'your package purchase successfully !', 'status': status.HTTP_200_OK})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


