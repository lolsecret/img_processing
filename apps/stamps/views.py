import json
import logging

from django.views.generic import TemplateView

from django.http import JsonResponse
from django.views.generic.edit import FormView
from .forms import DetectStampsImageForm
from .utils import detect_stamps

logger = logging.getLogger(__name__)


class DetectStampsView(FormView):
    template_name = 'detect_stamps.html'
    form_class = DetectStampsImageForm

    def form_valid(self, form):
        logger.info("detect_stamps_request")
        image = form.cleaned_data['image']
        stamp_coordinates = detect_stamps(image)
        res = {
            'stamps': len(stamp_coordinates),
            'stamp_coordinates': json.dumps(stamp_coordinates.tolist()),
        }
        logger.info(f"detect_stamps_request img: {image}; response: {res}")

        return JsonResponse({'result': res})

    def form_invalid(self, form):
        logger.error(f"detect_stamps_request form_invalid: {form.errors}")

        return JsonResponse({
            'error': form.errors,
        }, status=400)


class IndexView(TemplateView):
    template_name = 'index.html'
