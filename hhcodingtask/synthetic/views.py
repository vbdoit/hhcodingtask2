import json

from django.http import JsonResponse, Http404
from django.shortcuts import render
from django.views.generic import View, TemplateView

from .models import GenericModel, AnyData
from schematics.exceptions import ModelValidationError, ModelConversionError


class GenericView(View):
    http_method_names = ['post', 'get']

    def post(self, request):
        data = json.loads(request.body.decode())
        try:
            data_obj = AnyData(raw_data=data)
            data_obj.validate()
            response = data_obj.serialize()
            result_obj = GenericModel.objects.create(
                any_data=json.dumps(response))

            response['id'] = result_obj.pk
            return JsonResponse(data=response, status=201)
        except (ModelValidationError, ModelConversionError) as exc:
            result = {}
            for field, messages in exc.messages.items():
               result[field] = exc.messages[field].to_primitive()
            return JsonResponse(result, status=400)

    def get(self, request):
        qs = GenericModel.objects.all()
        items = {}
        for bits in qs.values_list('pk', 'any_data'):
            pk = bits[0]
            data = AnyData(raw_data=json.loads(bits[1])).to_native()
            items[pk] = data
        return_data = {'items': items, 'total': len(items)}
        return JsonResponse(data=return_data)


class GenericDetailView(View):

    def get_or_404(self, pk):
        try:
            return GenericModel.objects.get(pk=pk)
        except GenericModel.DoesNotExist:
            raise Http404

    def delete(self, request, pk):
        obj = self.get_or_404(pk=pk)
        obj.delete()
        return JsonResponse(data={}, status=204)

    def patch(self, request, pk):
        data = json.loads(request.body.decode())
        try:
            obj = self.get_or_404(pk=pk)
            data_obj = AnyData(raw_data=data)
            data_obj.validate()
            response = data_obj.serialize()
            obj.any_data = json.dumps(response)
            obj.save()
            response['id'] = obj.pk
            return JsonResponse(data=response, status=202)
        except (ModelValidationError, ModelConversionError) as exc:
            result = {}
            for field, messages in exc.messages.items():
               result[field] = exc.messages[field].to_primitive()
            return JsonResponse(result, status=400)


class GenericFormView(TemplateView):
    template_name = 'synthetic/form.html'
