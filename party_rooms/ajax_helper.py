import django
from django.db.utils import IntegrityError
from django.http import JsonResponse
from party_rooms.models import Room, MeetingPlace, MeetingTime


def contains(request_type, *decorator_args):
    """
    Декоратор, добавляющий в параметры функции параметр data, следующий за request,
    и содержащий GET- либо POST-данные, в зависимости от параметров декоратора.
    Производится проверка ajax-запроса на соответствие формату.
    :param request_type: строка 'GET' или 'POST'
    :param decorator_args: ключи полей, наличие которых в запросе необходимо проверить
    """
    def content_decorator(func):
        def wrapper(request, *args, **kwargs):
            if request.method != request_type:
                return send_response(False)
            ajax_data = request.POST if request.method == 'POST' else request.GET
            for elem in decorator_args:
                if not (elem in ajax_data):
                    return send_response(False)
            return func(request, ajax_data, *args, **kwargs)
        return wrapper
    return content_decorator


def needs_auth(func):
    """
    Аналог requires_auth, посылающий JsonResponse в случае ошибки
    :param func:
    """
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated():
            return send_response(False)
        return func(request, *args, **kwargs)
    return wrapper


def integrity(func):
    """
    Декоратор для проверки IntegrityError (дублирование записей)
    :param func:
    :return:
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except django.db.utils.IntegrityError:
            return send_response(False)
    return wrapper


def specify_room(func):
    """
    Аналог @find_room из view_decorators, информирующий об ошибке с помощью json
    :param func:
    """
    def wrapper(request, data, room_id):
        try:
            room = Room.objects.get(pk=room_id)
        except Room.DoesNotExist:
            return send_response(False)
        return func(request, data, room)
    return wrapper


def specify_scenario(func):
    """
    Получаем по данным из словаря data нужный объект MeetingPlace или MeetingTime
    """
    def wrapper(request, data, room):
        types = {"place": MeetingPlace, "time": MeetingTime}
        try:
            scenario = types[data["option_type"]].objects.get(pk=data["option_id"])
        except (MeetingPlace.DoesNotExist, MeetingTime.DoesNotExist, KeyError):
            return send_response(False)
        return func(request, data, room, scenario)
    return wrapper


def need_admin(func):
    """
    Ограничение доступа к url, требующее прав модератора
    """
    def wrapper(request, data, room):
        if room.admin_id != request.user.pk:
            return send_response(False)
        return func(request, data, room)
    return wrapper


def check_permissions(func):
    """
    Проверяем, имеет ли право данный пользователь на редактирование/удаление места/времени встречи
    """
    def wrapper(request, data, room, scenario):
        if (request.user.pk == room.admin_id) or (request.user.pk == scenario.author_id):
            return func(request, data, room, scenario)
        return send_response(False)
    return wrapper


def send_response(success=True, data=None):
    """
    Обёртка для JsonResponse
    :param success: установленный в False, сигнализирует об ошибке
    :param data: дополнительная информация для отправки (dict)
    """
    if data is None:
        return JsonResponse({'success': success})
    else:
        data['success'] = success
        return JsonResponse(data)


def save_vote(target_model):
    """
    Декоратор, производящий основную работу по добавлению результатов голосования в бд
    Подменяет сигнатуру (request, data, room) на (request, target), где target - объект target_model
    :param target_model: MeetingPlace либо MeetingTime, т.е. та сущность, за которую голосуют
    Декорируемая функция должна возвращать объект, унаследованный от models.Vote !!!
    """
    def save_decorator(creation_func):
        def wrapper(request, data, room):
            try:
                target = target_model.objects.get(pk=request.GET['id'])
            except target_model.DoesNotExist:
                return send_response(False)
            if target.room != room:
                return send_response(False)
            vote = creation_func(request, target)
            if data['type'] == 'rating':
                vote.rating = data['choice']
            else:
                vote.possibility = data['choice']
            vote.save()
            return send_response(data={'id': vote.pk})
        return wrapper
    return save_decorator
