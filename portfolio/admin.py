from django.contrib import admin

# Register your models here.
from .models import PaidRequests
from django.contrib import messages

@admin.register(PaidRequests)
class PaidRequestsAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    search_fields = ('user__email', 'user__name')
    list_filter = ('created_at', 'user')
    ordering = ['-created_at']
    readonly_fields = ('created_at',)

    actions = ['make_users_paid']  # Add the custom action

    def make_users_paid(self, request, queryset):
        """Set is_paid = True for selected users."""
        users = set()  # To avoid duplicate updates

        for paid_request in queryset:
            user = paid_request.user
            if not user.is_paid:  # Check if the user is already paid
                user.is_paid = True
                user.save()
                users.add(user)
            paid_request.delete()
        # Provide feedback to the admin
        if users:
            messages.success(request, f'Successfully updated {len(users)} user(s) to paid.')
        else:
            messages.info(request, 'No users were updated; they might already be paid.')

    make_users_paid.short_description = "Mark selected users as paid"