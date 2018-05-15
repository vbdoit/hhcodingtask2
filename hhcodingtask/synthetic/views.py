from django.http import JsonResponse, Http404
from django.shortcuts import render
from django.views.generic import View

from .models import GenericModel
from schematics.exceptions import ModelValidationError, ModelConversionError


class GenericView(View):
    http_method_names = ['post', 'get']

    def post(self):
        data = json.loads(request.body.decode())
        try:
            data_obj = AnyData(raw_data=data)
            data_obj.validate()
            kwargs = data_obj.to_native()
            result_obj = GenericModel.objects.create(**kwargs)

            return_data = AnyData(result_obj.to_dict())
            return JsonResponse(data=return_data, status=201)
        except (ModelValidationError, ModelConversionError) as exc:
            return JsonResponse(exc.messages, status=400)

    def get(self):
        qs = GenericModel.objects.all()
        items = [AnyData(i.to_dict()).to_native() for i in qs]
        return_data = {'items': items, 'total': len(items)}
        return JsonResponse(data=return_data)


class GenericDetailView(View):

    def get_or_404(self, pk):
        try:
            GenericModel.objects.get(pk=pk)
        except GenericModel.DoesNotExist
            raise Http404

    def delete(self, request, pk):
        obj = self.get_or_404(pk=pk)
        obj.delete()
        return JsonResponse(data={}, status=204)

    def patch(self, request, pk):
        data = json.loads(request.body.decode())
        try:
            data_obj = AnyData(raw_data=data)
            kwargs = data_obj.to_native()

            obj = self.get_or_404(pk=pk)
            obj.update(**kwargs)
            
            return_data = AnyData(obj.to_dict()).to_native()
            return JsonResponse(data=data, status=202)
        except ModelConversionError as exc:
            data = {field: msg for field, value in exc.messages.iteritems()}
            return JsonResponse(data=data, status=400)
        except ModelValidationError as exc:
            return JsonResponse(exc.messages, status=400)

