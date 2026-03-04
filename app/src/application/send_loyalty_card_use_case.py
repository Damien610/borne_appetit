from domain.email_service import EmailService
from domain.repositories import CustomerRepository
from domain.customer import Customer


class SendLoyaltyCardUseCase:
    """Cas d'usage : Envoyer la carte de fidélité par email"""
    
    def __init__(self, email_service: EmailService, customer_repository: CustomerRepository):
        self.email_service = email_service
        self.customer_repository = customer_repository
    
    def execute(self, restaurant_id: str, recipient_email: str) -> dict:
        """Exécute l'envoi de la carte de fidélité"""
        if not recipient_email or '@' not in recipient_email:
            raise ValueError("Email invalide")
        
        if not restaurant_id:
            raise ValueError("Restaurant ID requis")
        
        # Récupérer ou créer le client
        customer = self.customer_repository.get_by_email(restaurant_id, recipient_email)
        
        if not customer:
            # Créer un nouveau client
            customer = Customer(
                restaurant_id=restaurant_id,
                customer_id="",  # Sera généré
                email=recipient_email,
                loyalty_code="",  # Sera généré
                loyalty_points=0
            )
            customer = self.customer_repository.create(customer)
        
        # Envoyer l'email
        success = self.email_service.send_loyalty_card(recipient_email)
        
        return {
            'success': success,
            'customer_id': customer.customer_id,
            'loyalty_code': customer.loyalty_code
        }
