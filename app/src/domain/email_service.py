from abc import ABC, abstractmethod


class EmailService(ABC):
    """Interface pour l'envoi d'emails"""
    
    @abstractmethod
    def send_loyalty_card(self, recipient_email: str) -> bool:
        """Envoie la carte de fidélité par email"""
        pass
