import json
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from rest_framework.generics import CreateAPIView

from ads.models import Category
from ads.serializer import CategorySerializer


class CategoryCreateView(CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


@method_decorator(csrf_exempt, name='dispatch')
class CategoryListCreateView(View):

    def get(self, request):
        categories = Category.objects.all()
        response = []
        for cat in categories:
            response.append({'id': cat.pk,
                             'name': cat.name,
                             'slug': cat.slug})
        return JsonResponse(response, safe=False)

    def post(self, request):
        data = json.loads(request.body)
        cat = Category.objects.create(**data)

        return JsonResponse({'id': cat.pk,
                             'name': cat.name,
                             'slug': cat.slug},
                            safe=False)


class CategoryDetailView(DetailView):
    model = Category

    # queryset = Category.objects.all()

    def get(self, request, *args, **kwargs):
        cat = self.get_object()
        return JsonResponse({'id': cat.pk, 'name': cat.name}, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryUpdateView(UpdateView):
    model = Category
    fields = ['name']

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        data = json.loads(request.body)

        if 'name' in data:
            self.object.name = data['name']
        self.object.save()

        return JsonResponse({'id': self.object.pk,
                             'name': self.object.name},
                            safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryDeleteView(DeleteView):
    model = Category
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({'status': 'OK'}, status=204)
