from domain.repositories import RestaurantRepository, TerminalRepository, CustomerRepository

class GetRestaurantConfigUseCase:
    def __init__(self, repository: RestaurantRepository):
        self.repository = repository
    
    def execute(self, uri: str):
        restaurant = self.repository.get_by_uri(uri)
        if not restaurant:
            return None
        return {
            'uuid': restaurant.uuid,
            'name': restaurant.name,
            'uri_name': restaurant.uri_name,
            'logo': restaurant.logo,
            'favicon': restaurant.favicon,
            'welcome_image': restaurant.welcome_image,
            'primary_color': restaurant.primary_color,
            'secondary_color': restaurant.secondary_color
        }

class GetTerminalConfigUseCase:
    def __init__(self, terminal_repo: TerminalRepository, restaurant_repo: RestaurantRepository):
        self.terminal_repo = terminal_repo
        self.restaurant_repo = restaurant_repo
    
    def execute(self, terminal_uuid: str):
        terminal = self.terminal_repo.get_by_uuid(terminal_uuid)
        if not terminal:
            return None
        
        restaurant = self.restaurant_repo.get_by_uuid(terminal.restaurant_uuid)
        if not restaurant:
            return None
        
        return {
            'terminal': {
                'uuid': terminal.uuid,
                'name': terminal.name,
                'location': terminal.location
            },
            'restaurant': {
                'uuid': restaurant.uuid,
                'name': restaurant.name,
                'logo': restaurant.logo,
                'favicon': restaurant.favicon,
                'welcome_image': restaurant.welcome_image,
                'primary_color': restaurant.primary_color,
                'secondary_color': restaurant.secondary_color
            }
        }

class GetCustomerByLoyaltyCodeUseCase:
    def __init__(self, customer_repo: CustomerRepository, restaurant_repo: RestaurantRepository):
        self.customer_repo = customer_repo
        self.restaurant_repo = restaurant_repo
    
    def execute(self, restaurant_uuid: str, loyalty_code: str):
        customer = self.customer_repo.get_by_loyalty_code(loyalty_code, restaurant_uuid)
        if not customer:
            return None
        
        return {
            'uuid': customer.customer_id,
            'name': customer.name or customer.email.split('@')[0],
            'mail': customer.email,
            'loyaltyCode': customer.loyalty_code,
            'loyaltyPoints': customer.loyalty_points
        }
