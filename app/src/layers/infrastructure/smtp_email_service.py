import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from domain.email_service import EmailService


class SMTPEmailService(EmailService):
    """Implémentation SMTP pour l'envoi d'emails"""
    
    def __init__(self):
        self.smtp_user = os.environ.get('SMTP_USER')
        self.smtp_password = os.environ.get('SMTP_PASSWORD')
        
        if not self.smtp_user or not self.smtp_password:
            raise ValueError("Configuration SMTP manquante")
    
    def send_loyalty_card(self, recipient_email: str, wallet_url: str, restaurant_config: dict) -> bool:
        """Envoie le lien de la carte de fidélité Google Wallet"""
        try:
            name = restaurant_config.get('name', 'Restaurant')
            logo = restaurant_config.get('logo', '')
            
            html = f"""
<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"></head>
<body style="font-family: Arial; text-align: center; padding: 20px;">
    <img src="{logo}" alt="{name}" style="max-width: 200px; margin-bottom: 20px;">
    <h1>Votre carte de fidélité {name}</h1>
    <p>Ajoutez votre carte de fidélité à Google Wallet :</p>
    <a href="{wallet_url}" style="display: inline-block; background: #4285f4; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; margin: 20px 0;">Ajouter à Google Wallet</a>
</body>
</html>
"""
            
            msg = MIMEMultipart('alternative')
            msg['From'] = self.smtp_user
            msg['To'] = recipient_email
            msg['Subject'] = f"Votre carte de fidélité {name}"
            
            msg.attach(MIMEText(html, 'html'))
            
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)
            
            return True
        except Exception as e:
            print(f"Erreur envoi email: {e}")
            return False
