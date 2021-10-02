from django.utils.translation import gettext as _  # noqa
from django.template.response import TemplateResponse
from dashboard.models import Models3D
from django.shortcuts import redirect
from django.http import Http404
import os
from django.conf import settings

TEXTURES = {
    'wood': '/static/threejs/textures/woods/wood_default/wood_default.jpg',
    'wood_default': '/static/threejs/textures/wood-kitchen-face/wood-default/default.jpg',
    'stone': '/static/threejs/textures/stones/stone2/stone_2.jpg',
    'black-stone': '/static/threejs/textures/black-stone/black/black-stone.jpg',
}


def index(request):
    models3d = Models3D.objects().order_by('-id')
    context = {
        'models3d': models3d
    }

    return TemplateResponse(request, 'wagtailadmin/3d/index.html', context)


def show(request, models3d_id):
    context = {}
    if not models3d_id:
        raise Http404
    models3d = Models3D.objects(id=models3d_id).first()

    context['models3d'] = models3d
    context['textures'] = TEXTURES

    if request.method == 'POST':
        try:
            file = request.FILES['file_glb']
        except Exception as e:
            print('Errors upload file: {}'.format(e))
            file = None

        if file:
            new_path = os.path.join(settings.BASE_DIR, 'static', 'threejs', 'models')
            new_file = os.path.join(new_path, '{}.glb'.format(models3d_id))
            path = '{}/{}'.format('/static/threejs/models', '{}.glb'.format(models3d_id))
            if not os.path.exists(os.path.dirname(new_file)):
                os.makedirs(os.path.dirname(new_file))

            with open(new_file, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

            models3d.path_3d = path

        name_jp = request.POST.get('name_jp', models3d.name_jp)
        name_en = request.POST.get('name_en', models3d.name_en)
        price = request.POST.get('price', models3d.price)

        material_index = request.POST.getlist('material_index', [])
        material_name = request.POST.getlist('material_name', [])
        material_color = request.POST.getlist('material_color', [])
        material_image = request.POST.getlist('material_image', [])

        material = []

        for i in range(0, len(material_index)):
            data = {}
            data['index'] = int(material_index[i])
            data['name'] = material_name[i]
            data['color'] = material_color[i]
            data['image'] = material_image[i]
            material.append(data)

        rotation_x = request.POST.get('rotation_x', '')
        rotation_y = request.POST.get('rotation_y', '')
        rotation_z = request.POST.get('rotation_z', '')
        models3d.rotation = {'x': rotation_x, 'y': rotation_y, 'z': rotation_z}

        scale_x = request.POST.get('scale_x', '')
        scale_y = request.POST.get('scale_y', '')
        scale_z = request.POST.get('scale_z', '')
        models3d.scale = {'x': scale_x, 'y': scale_y, 'z': scale_z}

        models3d.name_jp = name_jp
        models3d.name_en = name_en
        models3d.price = float(price)
        models3d.mesh = material
        models3d.save()

    return TemplateResponse(request, 'wagtailadmin/3d/show.html', context)


def add(request):
    if request.method == 'POST':
        name_jp = request.POST.get('name_jp', '')
        name_en = request.POST.get('name_en', '')
        price = request.POST.get('price', '')
        if name_jp and name_jp and price:
            models3d = Models3D()
            models3d.name_jp = name_jp
            models3d.name_en = name_en
            models3d.price = float(price)
            models3d.save()
            return redirect('3d_show', models3d.id)

    return TemplateResponse(request, 'wagtailadmin/3d/add.html', {})
