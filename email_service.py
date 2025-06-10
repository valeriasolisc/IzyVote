import smtplib
import os
import random
import string
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

class EmailService:
    """Service for sending verification and notification emails"""
    
    def __init__(self):
        self.smtp_server = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.environ.get("SMTP_PORT", "587"))
        self.email_username = os.environ.get("EMAIL_USERNAME", "sistemadevotacionblockchain@gmail.com")
        self.email_password = os.environ.get("EMAIL_PASSWORD")
    
    def generate_verification_code(self) -> str:
        """Generate a 6-digit verification code"""
        return ''.join(random.choices(string.digits, k=6))
    
    def send_verification_email(self, to_email: str, verification_code: str, election_title: str) -> bool:
        """Send verification code email"""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email_username
            msg['To'] = to_email
            msg['Subject'] = f"Código de Verificación - {election_title}"
            
            body = f"""
            <html>
            <body>
                <h2>Verificación de Votación</h2>
                <p>Hola,</p>
                <p>Tu código de verificación para la elección "<strong>{election_title}</strong>" es:</p>
                <h3 style="color: #007bff; font-size: 24px; letter-spacing: 3px;">{verification_code}</h3>
                <p>Este código es válido por 30 minutos.</p>
                <p>Si no solicitaste este código, puedes ignorar este correo.</p>
                <br>
                <p>Saludos,<br>Sistema de Votación Blockchain</p>
            </body>
            </html>
            """
            
            msg.attach(MIMEText(body, 'html'))
            
            # Send real email if credentials are provided
            if self.email_password:
                server = smtplib.SMTP(self.smtp_server, self.smtp_port)
                server.starttls()
                server.login(self.email_username, self.email_password)
                text = msg.as_string()
                server.sendmail(self.email_username, to_email, text)
                server.quit()
                logging.info(f"Verification email sent to {to_email}")
            else:
                # For development, just log the email content
                logging.info(f"Development mode - Verification email to {to_email}: Code {verification_code}")
                print(f"VERIFICATION EMAIL - To: {to_email}, Code: {verification_code}")
            
            return True
            
        except Exception as e:
            logging.error(f"Error sending verification email: {str(e)}")
            return False
    
    def send_vote_confirmation(self, to_email: str, election_title: str) -> bool:
        """Send vote confirmation email"""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email_username
            msg['To'] = to_email
            msg['Subject'] = f"Voto Confirmado - {election_title}"
            
            body = f"""
            <html>
            <body>
                <h2>¡Voto Registrado Exitosamente!</h2>
                <p>Hola,</p>
                <p>Tu voto para la elección "<strong>{election_title}</strong>" ha sido registrado exitosamente en la blockchain.</p>
                <p>Características de tu voto:</p>
                <ul>
                    <li>✅ Verificado y válido</li>
                    <li>🔒 Completamente anónimo</li>
                    <li>⛓️ Almacenado en blockchain</li>
                    <li>🛡️ Inmutable y seguro</li>
                </ul>
                <p>Gracias por participar en el proceso democrático.</p>
                <br>
                <p>Saludos,<br>Sistema de Votación Blockchain</p>
            </body>
            </html>
            """
            
            msg.attach(MIMEText(body, 'html'))
            
            # Send real email if credentials are provided
            if self.email_password:
                server = smtplib.SMTP(self.smtp_server, self.smtp_port)
                server.starttls()
                server.login(self.email_username, self.email_password)
                text = msg.as_string()
                server.sendmail(self.email_username, to_email, text)
                server.quit()
                logging.info(f"Vote confirmation sent to {to_email}")
            else:
                # For development, just log the email content
                logging.info(f"Development mode - Vote confirmation to {to_email}")
                print(f"VOTE CONFIRMATION EMAIL - To: {to_email}")
            
            return True
            
        except Exception as e:
            logging.error(f"Error sending vote confirmation: {str(e)}")
            return False

# Global email service instance
email_service = EmailService()
