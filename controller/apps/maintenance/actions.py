from django.contrib import messages
from django.contrib.admin import helpers
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.utils.encoding import force_text

from controller.admin.utils import get_admin_link, get_modeladmin

from .forms import ExecutionForm
from .models import Operation, Instance


@transaction.commit_on_success
def execute_operation_changelist(modeladmin, request, queryset):
    if queryset.count() != 1:
        messages.warning(request, "One operation at a time")
        return
    operation = queryset.get()
    return redirect('admin:maintenance_operation_execute', operation.pk)
execute_operation_changelist.short_description = 'Execute operation'

@transaction.commit_on_success
def execute_operation(modeladmin, request, queryset):
    if not request.user.is_superuser:
        raise PermissionDenied
    
    opts = modeladmin.model._meta
    app_label = opts.app_label
    
    operation_id = request.path.split('/')[-3]
    operation = Operation.objects.get(pk=operation_id)
    
    if request.POST.get('post'):
        form = ExecutionForm(request.POST)
        if form.is_valid():
            include_new_nodes = form.cleaned_data['include_new_nodes']
        instances = operation.execute(queryset, include_new_nodes=include_new_nodes)
        for instance in instances:
            msg = 'Executed operation "%s"' % force_text(operation)
            modeladmin.log_change(request, operation, msg)
            instance_modeladmin = get_modeladmin(Instance)
            # AUTO_CREATE instances
            instance_modeladmin.log_addition(request, instance)
            modeladmin.message_user(request, "Successfully created %d instances." % len(instances))
            # Return None to display the change list page again.
            return redirect('admin:maintenance_operation_change', operation.pk)
    
    include_new_nodes = operation.executions.filter(include_new_nodes=True).exists()
    
    context = {
        "title": "Are you sure?",
        "operation": operation,
        "deletable_objects": [[ get_admin_link(node) for node in queryset ]],
        'queryset': queryset,
        "opts": opts,
        "app_label": app_label,
        'action_checkbox_name': helpers.ACTION_CHECKBOX_NAME,
        'form': ExecutionForm(initial={'include_new_nodes': include_new_nodes}),
    }
    
    return TemplateResponse(request, "admin/maintenance/operation/execute_operation_confirmation.html",
                            context, current_app=modeladmin.admin_site.name)


@transaction.commit_on_success
def revoke_instance(modeladmin, request, queryset):
    for instance in queryset:
        instance.revoke()
revoke_instance.url_name = 'revoke'
revoke_instance.verbose_name = 'revoke'


@transaction.commit_on_success
def run_instance(modeladmin, request, queryset):
    for instance in queryset:
        instance.run()
run_instance.url_name = 'run'
run_instance.verbose_name = 'run'
