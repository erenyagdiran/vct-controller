from django.conf import settings
from django.core.management.base import BaseCommand

from common.system import run, check_root


class Command(BaseCommand):
    help = 'Configures Apache2 to run with your controller instance.'
    
    @check_root
    def handle(self, *args, **options):
        username = run("ls -dl|awk {'print $3'}")
        project_name = settings.PROJECT_ROOT.split('/')[-1]
        apache_conf = (
            'WSGIScriptAlias / %(project_root)s/wsgi.py\n'
            'WSGIPythonPath %(site_root)s\n\n'
            '<Directory %(project_root)s>\n'
            '    <Files wsgi.py>\n'
            '        Order deny,allow\n'
            '        Allow from all\n'
            '    </Files>\n'
            '</Directory>\n\n'
            'Alias /media/ %(site_root)s/media/\n'
            'Alias /static/ %(site_root)s/static/\n'
            '<Directory /home/confine/controller/static/>\n'
            '    ExpiresActive On\n'
            '    ExpiresByType image/gif A1209600\n'
            '    ExpiresByType image/jpeg A1209600\n'
            '    ExpiresByType image/png A1209600\n'
            '    ExpiresByType text/css A1209600\n'
            '    ExpiresByType text/javascript A1209600\n'
            '    ExpiresByType application/x-javascript A1209600\n'
            '    <FilesMatch "\.(css|js|gz|png|gif|jpe?g|flv|swf|ico|pdf|txt|html|htm)$">\n'
            '        ContentDigest On\n'
            '        FileETag MTime Size\n'
            '    </FilesMatch>\n'
            '</Directory>\n'
            'RedirectMatch ^/$ /admin\n' % {'project_root': settings.PROJECT_ROOT,
                                            'site_root': settings.SITE_ROOT})
        
        run("echo '%s' > /etc/apache2/sites-available/%s.conf" % (apache_conf, project_name))
        run('a2ensite %s.conf' % project_name)
        # Give upload file permissions to apache
        run('adduser www-data %s' % username)
        run('chmod g+w %s/media/firmwares' % settings.SITE_ROOT)
        run('chmod g+w %s/media/templates' % settings.SITE_ROOT)
        run('chmod g+w %s/private/exp_data' % settings.SITE_ROOT)