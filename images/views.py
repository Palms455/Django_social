from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import ImageCreateForm
from .models import Image
from common.decorators import ajax_required
from actions.utils import create_actions


@login_required
def image_create(request):
    if request.method == 'POST':
        # form is sent
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            # form data is valid
            cd = form.cleaned_data
            new_item = form.save(commit=False)

            # assign current user to the item
            new_item.user = request.user
            new_item.save()
            create_actions(request.user, 'добавил фото', new_item)
            messages.success(request, 'Изображение добавлено')

            # redirect to new created item detail view
            return redirect(new_item.get_absolute_url())
    else:
        # build form with data provided by the bookmarklet via GET
        form = ImageCreateForm(data=request.GET)

    return render(request,
                  'images/image/create.html',
                  {'section': 'images',
                   'form': form})

def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    return render(request, 'images/image/detail.html',
                  {'section': 'images', 'image': image})

@ajax_required
@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.users_like.add(request.user)
                create_actions(request.user, 'понравилось фото', image)
            else:
                image.users_like.remove(request.user)
            return JsonResponse({'status': ok})
        except:
            pass
    return JsonResponse({'status': ok})

@login_required
def image_list(request):
    images = Image.objects.all()
    paginator = Paginator(images, 3)
    page = request.GET.get('page')
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        # Если переданная страница не является числом, возвращаем первую
        images = paginator.page(1)
    except EmptyPage:
        if request.is_ajax:
            return HttpResponse('')
        # Если номер страницы больше, чем их количество, возвращаем последнюю.
        images = paginator.page(paginator.num_pages)
    if request.is_ajax:
        return render(request, 'images/image/list_ajax.html',
                      {'section':'images', 'images': images})
    return render(request, 'images/image/list.html',
                  {'section' :'images', 'images': images})