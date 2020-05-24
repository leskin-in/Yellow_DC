from django.http import HttpRequest, HttpResponse, HttpResponseNotFound, HttpResponseRedirect, HttpResponseNotAllowed, HttpResponseServerError, HttpResponseBadRequest
from django.template.loader import render_to_string
from django.views.generic import TemplateView
from django.views.decorators.cache import never_cache

from .api_picture import upload, result

import logging


class IndexView(TemplateView):
    template_name = 'index.html'


def fp_upload(request: HttpRequest):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    try:
        file = request.FILES.get('photo')
        if file is None:
            return HttpResponseBadRequest('A photo must be provided (as a \'photo\' file)')
        result_id = upload(file)
        return HttpResponseRedirect('/photo/{}/'.format(result_id))
    except Exception as e:
        logging.getLogger().exception(e)
        return HttpResponseServerError()


@never_cache
def fp_photo(request: HttpRequest, id: str):
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])

    r = result(id)
    if r is None:
        return HttpResponseNotFound()
    
    return HttpResponse(render_to_string('photo.html', r))
