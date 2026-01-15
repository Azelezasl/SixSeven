from abc import ABC, abstractmethod

class Observer(ABC):
    """Abstract Observer Interface for the Observer Pattern."""
    
    @abstractmethod
    def update(self, subject, data: any) -> None:
        """Receive update from subject."""
        pass

class Subject(ABC):
    """Abstract Subject Interface."""

    def __init__(self):
        self._observers = []

    def attach(self, observer: Observer) -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        try:
            self._observers.remove(observer)
        except ValueError:
            pass

    def notify(self, data: any = None) -> None:
        for observer in self._observers:
            observer.update(self, data)