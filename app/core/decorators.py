from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _

from django.contrib import messages
from django.shortcuts import redirect

from django.conf import settings
import jsonpickle


def anonymous_required(function):
    """
    Check either user registered or not. If it is already registered user will redirect to 'INDEX'.
    """

    def wrap(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated():
            messages.add_message(request, messages.ERROR, _('You are already registered and logged in.'))
            return redirect(reverse('index'))
        else:
            return function(request, *args, **kwargs)

    return wrap


def json(fn):
    """
    Gets view method response and returns it in JSON format.
    """

    def wrapper(request, *args, **kwargs):
        try:
            # Executing function itself
            fn_result = fn(request, *args, **kwargs)
            # Prepare JSON dictionary for successful result
            json_result = {'is_successful': True, 'message': None, 'data': fn_result}
        except Exception as e:
            # If AJAX_DEBUG is enabled raise Exception
            if settings.AJAX_DEBUG:
                raise e
            # Else prepare JSON result object with error message
            json_result = {'is_successful': False, 'message': e.message, 'data': None}
        # Wrap result with JSON HTTPResponse and return
        return HttpResponse(jsonpickle.encode(json_result, unpicklable=False), mimetype='application/json')

    return wrapper