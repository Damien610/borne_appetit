from domain.email_service import EmailService
from domain.repositories import CustomerRepository, RestaurantRepository
from domain.customer import Customer


class SendLoyaltyCardUseCase:
    """Cas d'usage : Envoyer la carte de fidélité par email"""
    
    def __init__(self, email_service: EmailService, customer_repository: CustomerRepository, restaurant_repository: RestaurantRepository, wallet_service):
        self.email_service = email_service
        self.customer_repository = customer_repository
        self.restaurant_repository = restaurant_repository
        self.wallet_service = wallet_service
    
    def execute(self, restaurant_id: str, recipient_email: str) -> dict:
        """Exécute l'envoi de la carte de fidélité"""
        if not recipient_email or '@' not in recipient_email:
            raise ValueError("Email invalide")
        
        if not restaurant_id:
            raise ValueError("Restaurant ID requis")
        
        # Récupérer config restaurant
        restaurant = self.restaurant_repository.get_by_uuid(restaurant_id)
        if not restaurant:
            raise ValueError("Restaurant introuvable")
        
        restaurant_config = {
            'name': restaurant.name,
            'logo': restaurant.logo,
            'favicon': restaurant.favicon,
            'primary_color': restaurant.primary_color,
            'secondary_color': restaurant.secondary_color,
            'uri_name': restaurant.uri_name,
            'welcome_image': restaurant.welcome_image
        }
        
        # Récupérer ou créer le client
        customer = self.customer_repository.get_by_email(restaurant_id, recipient_email)
        
        if not customer:
            customer = Customer(
                restaurant_id=restaurant_id,
                customer_id="",
                email=recipient_email,
                loyalty_code="",
                loyalty_points=0
            )
            customer = self.customer_repository.create(customer)
        
        # Générer le pass Google Wallet
        wallet_url = self.wallet_service.create_loyalty_pass(
            customer.customer_id,
            customer.loyalty_code,
            customer.loyalty_points,
            restaurant_config
        )
        
        # Envoyer l'email avec le lien du pass
        success = self.email_service.send_loyalty_card(recipient_email, wallet_url, restaurant_config)
        
        return {
            'success': success,
            'customer_id': customer.customer_id,
            'loyalty_code': customer.loyalty_code,
            'wallet_url': wallet_url
        }
