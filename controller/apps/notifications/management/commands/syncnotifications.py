from optparse import make_option

from django.core.management.base import BaseCommand, CommandError

from notifications.models import Notification as NotificationModel
from notifications import Notification


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.option_list = BaseCommand.option_list
    
    option_list = BaseCommand.option_list
    help = 'Sync existing notifiactions with the database'
    
    def handle(self, *args, **options):
        existing_pks = []
        for notification in Notification.plugins:
            label = notification.__name__
            module = notification.__module__
            obj, created = NotificationModel.objects.get_or_create(label=label, module=module)
            if created:
                obj.subject=notification.default_subject
                obj.message=notification.default_message
                obj.save()
            existing_pks.append(obj.pk)
            self.stdout.write('Found %s (%s)' % (label, module))
        # Delete unused notifications
        NotificationModel.objects.exclude(pk__in=existing_pks).delete()