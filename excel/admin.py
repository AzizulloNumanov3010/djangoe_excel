from http.client import responses

from django.contrib import admin
from .models import User
import openpyxl
from django.http import HttpResponse


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('fullname', 'work','date_of_birth','email','phone_number','created_at')
    search_fields = ('fullname', 'work')
    list_filter = ('work', 'date_of_birth')

    actions = ['export_to_excel']

# Register your models here.
    def export_to_excel(self, request, queryset):
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = 'Users'
        sheet.append(['fullname', 'work','date_of_birth','email','phone_number','created_at'])

        for i in queryset:
            sheet.append([i.fullname, i.work, i.date_of_birth, i.email, i.phone_number,i.created_at.strftime('%Y-%m-%d %H:%M %S %p')])

        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename=users.xlsx'
        workbook.save(response)
        return response
    export_to_excel.short_description = 'Export to Excel'



