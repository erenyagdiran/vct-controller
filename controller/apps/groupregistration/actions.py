from django.contrib import messages
from django.db import transaction
from django.shortcuts import redirect

@transaction.commit_on_success
def approve_group(modeladmin, request, queryset):
    rows_updated = 0
    for group in queryset:
        group.approve()
        rows_updated+=1
        
    messages.info(request, "%s group(s) has been approved" % rows_updated)
    return redirect('admin:groupregistration_groupregistration_changelist')
approve_group.short_description = "Approve selected groups"

@transaction.commit_on_success
def reject_group(modeladmin, request, queryset):
    rows_updated = 0
    for group in queryset:
        group.reject()
        rows_updated+=1

    queryset.delete()
    messages.info(request, "%s group(s) has been rejected" % rows_updated)
    return redirect('admin:groupregistration_groupregistration_changelist')
reject_group.short_description = "Reject selected groups"
