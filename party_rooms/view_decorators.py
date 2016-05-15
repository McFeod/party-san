from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template.loader import get_template

from party_rooms.models import Room


def find_room(view):
    """
    Декоратор, подменяющий room_id на объект room из бд
    В случае некорректного room_id возвращает 404 страницу
    :param view:
    :return:
    """
    def wrapper(request, room_id):
        try:
            current_room = Room.objects.get(pk=room_id)
        except Room.DoesNotExist:
            raise Http404
        return view(request, current_room)
    return wrapper


def get_rendered(path, context, request):
    """
    благодаря тому, что RequestContext стал deprecated, появилась эта функция,
    заменяющая render_to_response(path, request_context)
    :param path: путь к шаблону
    :param context:
    :param request:
    :return:
    """
    return HttpResponse(get_template(path).render(context, request))


def basic_view(template):
    """
    Декоратор, который должен применяться к функции, возвращающей контекст.
    :param template: путь к шаблону
    :return: view-функция, возвращающая готовый HttpResponse
    """
    def view_decorator(context_func):
        def wrapper(request, *args, **kwargs):
            context = context_func(request, *args, **kwargs)
            return get_rendered(template, context, request)
        return wrapper
    return view_decorator


def check_room_auth(view):
    """
    Проверка на наличие доступа у юзера к комнате.
    Перенаправление при необходимости на страницу входа в комнату
    :param view:
    :return:
    """
    def wrapper(request, room):
        if request.user in room.room_users.all():
            return view(request, room)
        else:
            return HttpResponseRedirect(reverse('party:room_auth', kwargs={'room_id': room.pk}))
    return wrapper
