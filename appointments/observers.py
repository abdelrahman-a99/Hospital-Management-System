# appointments/observer.py

from abc import ABC, abstractmethod

# Abstract Observer
class Observer(ABC):
    @abstractmethod
    def update(self, message):
        pass

# Concrete Observer
class NotificationObserver(Observer):
    def __init__(self, user):
        self.user = user

    def update(self, message):
        # This will handle creating a notification for the user
        from .models import Notification  # Import here to avoid circular imports
        Notification.objects.create(user=self.user, content=message)

# Subject
class Subject:
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def notify(self, message):
        for observer in self._observers:
            observer.update(message)
