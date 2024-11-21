from rest_framework import viewsets
from rest_framework import permissions
# from rest_framework.throttling import AnonRateThrottle
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from cats.models import Achievement, Cat, User
from cats.serializers import AchievementSerializer, CatSerializer, UserSerializer
from cats.permissions import OwnerOrReadOnly
from cats.throttling import WorkingHoursRateThrottle
from cats.pagination import CatsPagination


class CatViewSet(viewsets.ModelViewSet):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer
    permission_classes = (OwnerOrReadOnly,)
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    )
    # throttle_classes = (AnonRateThrottle,)
    # Если кастомный тротлинг-класс вернёт True - запросы будут обработаны
    # Если он вернёт False - все запросы будут отклонены
    throttle_classes = (WorkingHoursRateThrottle, ScopedRateThrottle)
    # А далее применится лимит low_request
    throttle_scope = 'low_request'
    # pagination_class = PageNumberPagination
    # pagination_class = LimitOffsetPagination
    # pagination_class = CatsPagination
    pagination_class = None
    filterset_fields = ('color', 'birth_year')
    search_fields = ('name',)
    ordering_fields = ('name', 'birth_year')
    ordering = ('birth_year',) 

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    # def get_permissions(self):
    #     # Если в GET-запросе требуется получить информацию об объекте
    #     if self.action == 'retrieve':
    #         # Вернём обновлённый перечень используемых пермишенов
    #         return (ReadOnly(),)
    #     # Для остальных ситуаций оставим текущий перечень пермишенов без изменений
    #     return super().get_permissions()

    # def get_queryset(self):
    #     queryset = Cat.objects.all()
    #     # color = self.kwargs['color']
    #     # # Через ORM отфильтровать объекты модели Cat
    #     # # по значению параметра color, полученного в запросе
    #     # queryset = queryset.filter(color=color)
    #     # Добыть параметр color из GET-запроса
    #     color = self.request.query_params.get('color')
    #     if color is not None:
    #         #  через ORM отфильтровать объекты модели Cat
    #         #  по значению параметра color, полученного в запросе
    #         queryset = queryset.filter(color=color)
    #     return queryset


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AchievementViewSet(viewsets.ModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
