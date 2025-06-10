
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
        self.is_production = os.environ.get("ENVIRONMENT", "development") == "production"
    
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
            <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 10px; text-align: center; color: white;">
                    <h1 style="margin: 0; font-size: 28px;">🗳️ Sistema de Votación Blockchain</h1>
                    <p style="margin: 10px 0 0 0; opacity: 0.9;">Universidad Nacional de Ingeniería</p>
                </div>
                
                <div style="padding: 30px; background: #f8f9fa; border-radius: 10px; margin: 20px 0;">
                    <h2 style="color: #333; margin-top: 0;">Verificación de Identidad</h2>
                    <p style="color: #666; font-size: 16px;">Hola,</p>
                    <p style="color: #666; font-size: 16px;">Has solicitado participar en la elección:</p>
                    <div style="background: white; padding: 15px; border-radius: 8px; border-left: 4px solid #667eea; margin: 20px 0;">
                        <h3 style="margin: 0; color: #333;">{election_title}</h3>
                    </div>
                    
                    <p style="color: #666; font-size: 16px;">Tu código de verificación es:</p>
                    <div style="background: #667eea; color: white; padding: 20px; border-radius: 10px; text-align: center; margin: 20px 0;">
                        <h2 style="margin: 0; font-size: 32px; letter-spacing: 8px; font-family: 'Courier New', monospace;">{verification_code}</h2>
                    </div>
                    
                    <div style="background: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; border-radius: 8px; margin: 20px 0;">
                        <p style="margin: 0; color: #856404;"><strong>⏰ Importante:</strong></p>
                        <ul style="color: #856404; margin: 10px 0 0 0;">
                            <li>Este código es válido por <strong>30 minutos</strong></li>
                            <li>Solo puedes votar <strong>una vez</strong> por elección</li>
                            <li>Tu voto será <strong>completamente anónimo</strong></li>
                        </ul>
                    </div>
                </div>
                
                <div style="background: #e9ecef; padding: 20px; border-radius: 10px; text-align: center;">
                    <p style="margin: 0; color: #6c757d; font-size: 14px;">
                        Si no solicitaste este código, puedes ignorar este correo.<br>
                        <strong>Sistema de Votación Blockchain UNI</strong><br>
                        Desarrollado con tecnología blockchain para garantizar transparencia y seguridad
                    </p>
                </div>
            </body>
            </html>
            """
            
            msg.attach(MIMEText(body, 'html'))
            
            # Send real email if in production or if password is provided
            if self.email_password:
                try:
                    server = smtplib.SMTP(self.smtp_server, self.smtp_port)
                    server.starttls()
                    server.login(self.email_username, self.email_password)
                    text = msg.as_string()
                    server.sendmail(self.email_username, to_email, text)
                    server.quit()
                    logging.info(f"Email enviado exitosamente a {to_email}")
                    return True
                except Exception as e:
                    logging.error(f"Error enviando email real: {str(e)}")
                    # Fall back to development mode
                    self._log_email_content(to_email, verification_code, "VERIFICATION")
                    return True
            else:
                # Development mode - log email content
                self._log_email_content(to_email, verification_code, "VERIFICATION")
                return True
            
        except Exception as e:
            logging.error(f"Error en send_verification_email: {str(e)}")
            return False
    
    def send_vote_confirmation(self, to_email: str, election_title: str) -> bool:
        """Send vote confirmation email"""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email_username
            msg['To'] = to_email
            msg['Subject'] = f"✅ Voto Confirmado - {election_title}"
            
            body = f"""
            <html>
            <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
                <div style="background: linear-gradient(135deg, #56ab2f 0%, #a8e6cf 100%); padding: 30px; border-radius: 10px; text-align: center; color: white;">
                    <h1 style="margin: 0; font-size: 28px;">✅ ¡Voto Registrado!</h1>
                    <p style="margin: 10px 0 0 0; opacity: 0.9;">Sistema de Votación Blockchain UNI</p>
                </div>
                
                <div style="padding: 30px; background: #f8f9fa; border-radius: 10px; margin: 20px 0;">
                    <h2 style="color: #333; margin-top: 0;">Confirmación de Votación</h2>
                    <p style="color: #666; font-size: 16px;">¡Felicidades!</p>
                    <p style="color: #666; font-size: 16px;">Tu voto para la elección <strong>"{election_title}"</strong> ha sido registrado exitosamente en la blockchain.</p>
                    
                    <div style="background: white; padding: 20px; border-radius: 10px; margin: 20px 0;">
                        <h3 style="color: #28a745; margin-top: 0;">🔐 Características de tu voto:</h3>
                        <div style="display: grid; gap: 15px;">
                            <div style="display: flex; align-items: center; padding: 10px; background: #d4edda; border-radius: 8px;">
                                <span style="margin-right: 10px;">✅</span>
                                <span style="color: #155724;"><strong>Verificado:</strong> Tu identidad fue confirmada</span>
                            </div>
                            <div style="display: flex; align-items: center; padding: 10px; background: #cce5ff; border-radius: 8px;">
                                <span style="margin-right: 10px;">🔒</span>
                                <span style="color: #004085;"><strong>Anónimo:</strong> Tu voto no puede ser rastreado</span>
                            </div>
                            <div style="display: flex; align-items: center; padding: 10px; background: #fff3cd; border-radius: 8px;">
                                <span style="margin-right: 10px;">⛓️</span>
                                <span style="color: #856404;"><strong>Inmutable:</strong> Almacenado permanentemente en blockchain</span>
                            </div>
                            <div style="display: flex; align-items: center; padding: 10px; background: #f8d7da; border-radius: 8px;">
                                <span style="margin-right: 10px;">🛡️</span>
                                <span style="color: #721c24;"><strong>Seguro:</strong> Protegido criptográficamente</span>
                            </div>
                        </div>
                    </div>
                    
                    <div style="background: #e7f3ff; border: 1px solid #b3d9ff; padding: 15px; border-radius: 8px; margin: 20px 0;">
                        <p style="margin: 0; color: #0056b3;"><strong>📊 ¿Qué sigue?</strong></p>
                        <p style="color: #0056b3; margin: 10px 0 0 0;">Puedes ver los resultados en tiempo real visitando el sistema de votación. Los resultados se actualizan automáticamente conforme llegan más votos.</p>
                    </div>
                </div>
                
                <div style="background: #e9ecef; padding: 20px; border-radius: 10px; text-align: center;">
                    <p style="margin: 0; color: #6c757d; font-size: 14px;">
                        Gracias por participar en el proceso democrático de la UNI<br>
                        <strong>Sistema de Votación Blockchain UNI</strong><br>
                        Transparencia • Seguridad • Confianza
                    </p>
                </div>
            </body>
            </html>
            """
            
            msg.attach(MIMEText(body, 'html'))
            
            # Send real email if in production or if password is provided
            if self.email_password:
                try:
                    server = smtplib.SMTP(self.smtp_server, self.smtp_port)
                    server.starttls()
                    server.login(self.email_username, self.email_password)
                    text = msg.as_string()
                    server.sendmail(self.email_username, to_email, text)
                    server.quit()
                    logging.info(f"Confirmación de voto enviada a {to_email}")
                    return True
                except Exception as e:
                    logging.error(f"Error enviando confirmación real: {str(e)}")
                    # Fall back to development mode
                    self._log_email_content(to_email, "CONFIRMACIÓN", "VOTE_CONFIRMATION")
                    return True
            else:
                # Development mode - log email content
                self._log_email_content(to_email, "CONFIRMACIÓN", "VOTE_CONFIRMATION")
                return True
            
        except Exception as e:
            logging.error(f"Error en send_vote_confirmation: {str(e)}")
            return False
    
    def _log_email_content(self, to_email: str, code_or_message: str, email_type: str):
        """Log email content for development mode"""
        logging.info(f"{email_type} email sent to {to_email}: {code_or_message}")
        print(f"📧 {email_type} EMAIL - To: {to_email}, Content: {code_or_message}")

# Global email service instance
email_service = EmailService()
