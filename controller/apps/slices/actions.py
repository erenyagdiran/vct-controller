from django.contrib import messages
from django.contrib.admin import helpers
from django.core.exceptions import PermissionDenied
from django.db import router, transaction
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy

from common.admin import get_admin_link, get_modeladmin

from .forms import SliverIfaceBulkForm
from .models import Slice, Sliver, SliverIface
from .settings import SLICES_SLICE_EXP_INTERVAL


@transaction.commit_on_success
def renew_selected_slices(modeladmin, request, queryset):
    # TODO queryset.renew() ?
    for obj in queryset:
        if not modeladmin.has_change_permission(request, obj=obj):
            raise PermissionDenied
        obj.renew()
        msg = "Renewed for %s" % SLICES_SLICE_EXP_INTERVAL
        modeladmin.log_change(request, obj, msg)
    msg = "%s selected slices has been renewed for %s on" % (queryset.count(), \
        SLICES_SLICE_EXP_INTERVAL)
    modeladmin.message_user(request, msg)


@transaction.commit_on_success
def reset_selected(modeladmin, request, queryset):
    # TODO queryset.reset() ?
    for obj in queryset:
        if not modeladmin.has_change_permission(request, obj=obj):
            raise PermissionDenied
        obj.reset()
        modeladmin.log_change(request, obj, "Instructed to reset")
    verbose_name_plural = force_text(obj._meta.verbose_name_plural)
    msg = "%s selected %s has been reseted" % (queryset.count(), verbose_name_plural)
    modeladmin.message_user(request, msg)
reset_selected.short_description = ugettext_lazy("Reset selected %(verbose_name_plural)s")


@transaction.commit_on_success
def create_slivers(modeladmin, request, queryset):
    """ Create slivers in selected nodes """
    opts = modeladmin.model._meta
    app_label = opts.app_label
    
    slice_id = request.path.split('/')[-3]
    slice = Slice.objects.get(pk=slice_id)
    
    if not modeladmin.has_change_permission(request, obj=slice):
        raise PermissionDenied
    
    n = queryset.count()
    if n == 1:
        node = queryset.get()
        return redirect('admin:slices_slice_add_sliver', slice_id, node.pk)
    
    if request.POST.get('post'):
        form = SliverIfaceBulkForm(request.POST)
        if form.is_valid():
            optional_ifaces = form.cleaned_data
            requested_ifaces = [ field for field, value in optional_ifaces.iteritems() if value ]
            
            for node in queryset:
                sliver = Sliver(slice=slice, node=node)
                if not request.user.has_perm('slices.add_sliver', sliver):
                    raise PermissionDenied
                sliver.save()
                for iface_type in requested_ifaces:
                    iface = Sliver.get_registred_iface(iface_type)
                    SliverIface.objects.create(sliver=sliver, name=iface.DEFAULT_NAME, type=iface_type)
                slice_modeladmin = get_modeladmin(Slice)
                msg = 'Added sliver "%s"' % force_text(sliver)
                slice_modeladmin.log_change(request, slice, msg)
                sliver_modeladmin = get_modeladmin(Sliver)
                # AUTO_CREATE SliverIfaces
                sliver_modeladmin.log_addition(request, sliver)
            
            modeladmin.message_user(request, "Successfully created %d slivers." % n)
            # Return None to display the change list page again.
            return None
    
    context = {
        "title": "Are you sure?",
        "slice": slice,
        "deletable_objects": [[ get_admin_link(node) for node in queryset ]],
        'queryset': queryset,
        "opts": opts,
        "app_label": app_label,
        'action_checkbox_name': helpers.ACTION_CHECKBOX_NAME,
        'form': SliverIfaceBulkForm(),
    }
    
    return TemplateResponse(request, "admin/slices/slice/create_slivers_confirmation.html",
                            context, current_app=modeladmin.admin_site.name)
create_slivers.short_description = "Create slivers on selected nodes"