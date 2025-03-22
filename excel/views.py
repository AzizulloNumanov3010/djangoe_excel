from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import APIView
from .serializers import UserSerializer
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.views import View
import openpyxl
from .models import *




class ExportUsersExcel(View):
    """Foydalanuvchilarni Excel formatida yuklab beruvchi API"""

    def get(self, request, *args, **kwargs):
        # Excel fayl yaratamiz
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = 'Users'
        sheet.append(['fullname', 'Work', 'Date of Birth', 'Email', 'Phone Number', 'Created At'])

        # Foydalanuvchilarni bazadan olish
        users = User.objects.all()
        for i in users:
            sheet.append([
                i.fullname,
                i.work,
                i.date_of_birth.strftime('%Y-%m-%d'),
                i.email,
                i.phone_number,
                i.created_at.strftime('%Y-%m-%d %H:%M:%S')
            ])

        # Excel faylni HTTP Response sifatida qaytarish
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=users.xlsx'
        workbook.save(response)
        return response


class UserAPIVIEWriter(APIView):

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def put(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


