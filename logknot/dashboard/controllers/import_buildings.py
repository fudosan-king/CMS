from django.http import HttpResponse
from django.template import loader
from importer.import_csv import import_csv
import os
from django.conf import settings
import datetime

# 1MB - 1048576
# 2MB - 2097152
# 2.5MB - 2621440
# 5MB - 5242880
# 10MB - 10485760
# 20MB - 20971520
# 50MB - 5242880
# 100MB 104857600
# 250MB - 214958080
# 500MB - 429916160
MAX_UPLOAD_SIZE = 2097152


def index(request):
    errors = []
    done = {}
    ignore = {}
    fail = []
    if request.method == 'POST':
        try:
            file = request.FILES['files']
        except Exception as e:
            errors.append('ファイルcsvを確認してください: {}'.format(e))
            file = None

        if file:
            if file.size > MAX_UPLOAD_SIZE:
                errors.append('非常に大きなファイル: {}Bytes（必要とする <2MB）'.format(file.size))
            else:
                now = datetime.datetime.now()
                time = '{}{}{}_{}{}{}'.format(
                    now.year,
                    format(now.month, '02d'),
                    format(now.day, '02d'),
                    format(now.hour, '02d'),
                    format(now.minute, '02d'),
                    format(now.second, '02d')
                )
                new_path = os.path.join(settings.IMPORT_ROOT, time)
                new_file = os.path.join(new_path, 'import.csv')
                if not os.path.exists(os.path.dirname(new_file)):
                    os.makedirs(os.path.dirname(new_file))

                with open(new_file, 'wb+') as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)
                try:
                    dry_run = request.POST.get('dry_run')
                    if not dry_run:
                        dry_run = False
                        import_csv(new_path, dry_run=dry_run)
                    else:
                        dry_run = True
                        done, ignore, fail = import_csv(new_path, dry_run=dry_run)
                except Exception as e:
                    errors.append('インポートできません: {}'.format(e))

    template = loader.get_template('wagtailadmin/import_buildings/index.html')
    print(type(ignore))
    context = {
        'errors': errors,
        'done': done,
        'ignore': ignore,
        'fail': fail
    }
    return HttpResponse(template.render(context, request))
