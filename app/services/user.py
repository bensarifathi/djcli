from django.db.models.query import QuerySet
from app.models import User
from django.shortcuts import get_object_or_404


class UserService:

    def get_all(self) -> QuerySet[User]:
        return User.objects.all()

    def get_by_id(self, id: int) -> User:
        return get_object_or_404(User, id)

    def create(self, **kwargs) -> User:
        return User.objects.create(**kwargs)
    
    def update(self, id: int, **kwargs) -> User:
        user = self.get_by_id(id)
        for k, v in kwargs.items():
            setattr(user, k, v)
        user.save()
        return user
    
    def delete(self, id: int) -> None:
        self.get_by_id(id).delete()