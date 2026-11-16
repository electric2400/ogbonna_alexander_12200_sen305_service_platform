from django.contrib import admin
from django.utils import timezone
from .models import Category, ServiceRequest


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)



class OverdueFilter(admin.SimpleListFilter):
    title = 'Overdue'
    parameter_name = 'overdue'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'Overdue'),
            ('no', 'Not overdue'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(
                due_at__lt=timezone.now()
            ).exclude(status__in=['RESOLVED', 'CLOSED'])

        if self.value() == 'no':
            return queryset.filter(
                due_at__gte=timezone.now()
            ) | queryset.filter(due_at__isnull=True)

        return queryset

@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'category',
        'status',
        'priority',
        'due_at',
        'resolved_at',
    )

    list_filter = ('status', 'priority', 'category', OverdueFilter)
    search_fields = ('title', 'description')

    def get_queryset(self, request):
        return super().get_queryset(request)