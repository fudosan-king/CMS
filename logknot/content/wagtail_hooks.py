from wagtail.core import hooks
from django.http import HttpResponseRedirect
from content.models import ContentDetailPage


@hooks.register('after_create_page')
def redirect_after_page_create(request, page):
    building_id = request.POST.get('building_id')
    if building_id:
        page_content = ContentDetailPage.objects.get(building_id=building_id)
    if page_content and page.depth == 4 and page_content.link:
        return HttpResponseRedirect(page_content.link)


@hooks.register('after_edit_page')
def redirect_after_page_edit(request, page):
    building_id = request.POST.get('building_id')
    if building_id:
        page_content = ContentDetailPage.objects.get(building_id=building_id)
    if page_content and page.depth == 4 and page_content.link:
        return HttpResponseRedirect(page_content.link)


@hooks.register('after_delete_page')
def redirect_after_page_delete(request, page):
    link = request.POST.get('link')
    print(link)
    if link:
        return HttpResponseRedirect(link)
