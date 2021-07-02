from wagtail.images.views.multiple import AddView


class UploadImages(AddView):
    template_name = 'wagtailimages/upload/add.html'

    def save_object(self, form):
        image = form.save(commit=False)
        image.uploaded_by_user = self.request.user
        image.file_size = image.file.size
        image.file.seek(0)
        image._set_file_hash(image.file.read())
        image.building_id = self.request.POST.get('building_id', '')
        image.file.seek(0)
        image.save()
        return image
