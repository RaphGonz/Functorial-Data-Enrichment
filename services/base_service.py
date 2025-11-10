from abc import ABC, abstractmethod

class BaseService(ABC):
    """Interface commune à tous les modules d'enrichissement."""

    name: str = "base"
    enabled: bool = True

    @abstractmethod
    def run(self, *args, **kwargs):
        """Méthode principale appelée par le routeur."""
        pass