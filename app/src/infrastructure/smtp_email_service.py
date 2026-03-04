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
    
    def send_loyalty_card(self, recipient_email: str) -> bool:
        """Envoie la carte de fidélité via SMTP Google"""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.smtp_user
            msg['To'] = recipient_email
            msg['Subject'] = 'Votre carte de fidélité Borne Appétit'
            
            body_text = "Voici votre carte de fidélité."
            msg.attach(MIMEText(body_text, 'plain'))
            
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)
            
            return True
        except Exception as e:
            print(f"Erreur envoi email: {e}")
            return False
