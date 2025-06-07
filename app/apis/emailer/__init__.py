from fastapi import APIRouter
from pydantic import BaseModel, EmailStr
import os
from datetime import datetime
import resend

from typing import Optional, List

# Create router
router = APIRouter()

# Pydantic models for API requests
class ContactFormRequest(BaseModel):
    name: str
    email: EmailStr
    subject: str
    message: str

class WelcomeEmailRequest(BaseModel):
    name: str
    email: EmailStr

class EmailResponse(BaseModel):
    success: bool
    message: str
    email_id: Optional[str] = None

class RecipientEmail(BaseModel):
    email: EmailStr
    name: Optional[str] = None

class GenericEmailRequest(BaseModel):
    from_email: str = "support@loufranktv.com"
    from_name: str = "LouFrank TV Support"
    to: List[RecipientEmail]
    subject: str
    html_content: str
    text_content: Optional[str] = None
    reply_to: Optional[str] = None

class TrialRequestRequest(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None

@router.post("/contact", response_model=EmailResponse)
def send_contact_form(request: ContactFormRequest):
    """
    Send a contact form submission email to the support team.
    """
    try:
        # Initialize Resend with API key
        api_key = os.environ.get("RESEND_API_KEY")
        if not api_key:
            return EmailResponse(
                success=False,
                message="Email service not configured. Please contact us directly.",
                email_id=None
            )
        
        # Set Resend API key
        resend.api_key = api_key
        
        # Prepare email content with premium styling and logo
        html_content = f"""
        <html>
            <head>
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <style>
                    body {{ font-family: 'Arial', sans-serif; line-height: 1.6; margin: 0; padding: 0; background-color: #f9f9f9; }}
                    .container {{ max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 0 20px rgba(0, 0, 0, 0.1); }}
                    .header {{ background: #17d1e0; padding: 20px; text-align: center; }}
                    .logo {{ height: 70px; width: auto; }}
                    .content {{ padding: 30px; color: #333333; font-size: 16px; }}
                    .footer {{ background-color: #f0f0f0; padding: 20px; text-align: center; font-size: 14px; color: #555555; border-top: 1px solid #e0e0e0; }}
                    h1, h2 {{ color: #222222; margin-top: 0; font-weight: bold; font-size: 24px; }}
                    h1 {{ font-size: 28px; letter-spacing: 0.5px; }}
                    p {{ margin-bottom: 16px; color: #333333; }}
                    strong {{ color: #0891b2; font-weight: bold; }}
                    .highlight {{ color: #0891b2; font-weight: bold; }}
                    .divider {{ height: 2px; background: linear-gradient(to right, #ffffff, #17d1e0, #ffffff); margin: 20px 0; }}
                    ul {{ padding-left: 20px; margin: 20px 0; }}
                    li {{ margin-bottom: 10px; padding-left: 5px; color: #333333; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <img class="logo" src="https://loufranktv.com/public/901661ac-f28e-4815-8069-61ae5363a100/logo-color.png" alt="LouFrank TV Logo">
                    </div>
                    <div class="content">
                        <h2>New Contact Form Submission</h2>
                        <div class="divider"></div>
                        <p><strong>From:</strong> {request.name} ({request.email})</p>
                        <p><strong>Subject:</strong> {request.subject}</p>
                        <p><strong>Message:</strong></p>
                        <p>{request.message}</p>
                    </div>
                    <div class="footer">
                        <p>© {datetime.now().year} LouFrank TV. All rights reserved.</p>
                        <p>Premium IPTV Service | 16,000+ Channels | Global Coverage</p>
                    </div>
                </div>
            </body>
        </html>
        """
        
        # Send email
        params = {
            "from": "LouFrank TV Contact <contact@loufranktv.com>",
            "to": ["loufranktv@gmail.com"],  # Using owner's email for testing, replace with support email after domain verification
            "subject": f"Contact Form: {request.subject}",
            "html": html_content,
            "reply_to": request.email
        }
        
        response = resend.Emails.send(params)
        
        return EmailResponse(
            success=True,
            message="Contact form submitted successfully",
            email_id=response.get("id")
        )
    
    except Exception as e:
        print(f"Error sending contact email: {str(e)}")
        return EmailResponse(
            success=False,
            message=f"Failed to send email: {str(e)}",
            email_id=None
        )

@router.post("/welcome", response_model=EmailResponse)
def send_welcome_email(request: WelcomeEmailRequest):
    """
    Send a welcome email to a newly registered user.
    """
    try:
        # Initialize Resend with API key
        api_key = os.environ.get("RESEND_API_KEY")
        if not api_key:
            return EmailResponse(
                success=False,
                message="Email service not configured",
                email_id=None
            )
        
        # Set Resend API key
        resend.api_key = api_key
        
        # Prepare email content with premium styling and logo
        html_content = f"""
        <html>
            <head>
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <style>
                    body {{ font-family: 'Arial', sans-serif; line-height: 1.6; color: #e2e8f0; margin: 0; padding: 0; background-color: #0f0f0f; }}
                    .container {{ max-width: 600px; margin: 0 auto; background-color: #0a0a0a; border-radius: 8px; overflow: hidden; }}
                    .header {{ background: linear-gradient(135deg, #000000, #1a1a1a); padding: 20px; text-align: center; border-bottom: 1px solid #333; }}
                    .logo {{ height: 60px; width: auto; }}
                    .content {{ padding: 30px; }}
                    .footer {{ background-color: #0a0a0a; padding: 20px; text-align: center; font-size: 12px; color: #6c7280; border-top: 1px solid #333; }}
                    h1, h2 {{ color: #ffffff; margin-top: 0; }}
                    .highlight {{ color: #17d1e0; }}
                    .divider {{ height: 1px; background: linear-gradient(to right, transparent, #333, transparent); margin: 20px 0; }}
                    .button {{ background: #17d1e0; color: #ffffff; text-decoration: none; padding: 14px 30px; border-radius: 5px; font-weight: bold; display: inline-block; margin: 25px 0; font-size: 16px; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1); }}
                    .button:hover {{ background: #0891b2; }}
                    a {{ color: #0891b2; text-decoration: underline; font-weight: bold; }}
                    a:hover {{ color: #066a82; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <img class="logo" src="https://loufranktv.com/public/901661ac-f28e-4815-8069-61ae5363a100/logo-color.png" alt="LouFrank TV Logo">
                    </div>
                    <div class="content">
                        <h1>Welcome to <span class="highlight">LouFrank TV</span>!</h1>
                        <div class="divider"></div>
                        
                        <p>Hello {request.name},</p>
                        <p>Thank you for joining LouFrank TV! We're excited to have you as part of our community of premium entertainment enthusiasts.</p>
                        
                        <p>With your new account, you now have access to:</p>
                        <ul>
                            <li>Over <strong>16,000 HD and FHD channels</strong> from more than 50 countries</li>
                            <li>Thousands of <strong>on-demand movies and TV series</strong></li>
                            <li><strong>Ultra-fast zapping</strong> with no freezing</li>
                            <li><strong>Global access</strong> from any device</li>
                        </ul>
                        
                        <div style="text-align: center;">
                            <a href="https://loufranktv.com/setup-guides" class="button">Set Up Your Devices</a>
                        </div>
                        
                        <p>If you have any questions or need assistance, don't hesitate to contact our support team at <a href="mailto:support@loufranktv.com" style="color: #17d1e0;">support@loufranktv.com</a>.</p>
                        
                        <p>Enjoy the premium experience!</p>
                        <p>The LouFrank TV Team</p>
                    </div>
                    <div class="footer">
                        <p>© {datetime.now().year} LouFrank TV. All rights reserved.</p>
                        <p>Premium IPTV Service | 16,000+ Channels | Global Coverage</p>
                    </div>
                </div>
            </body>
        </html>
        """
        
        # Plain text version
        text_content = f"""
        Welcome to LouFrank TV!
        
        Hello {request.name},
        
        Thank you for joining LouFrank TV! We're excited to have you as part of our community of premium entertainment enthusiasts.
        
        With your new account, you now have access to:
        - Over 16,000 HD and FHD channels from more than 50 countries
        - Thousands of on-demand movies and TV series
        - Ultra-fast zapping with no freezing
        - Global access from any device
        
        Set up your devices: https://loufranktv.com/setup
        
        If you have any questions or need assistance, don't hesitate to contact our support team at support@loufranktv.com.
        
        Enjoy the premium experience!
        
        The LouFrank TV Team
        """
        
        # Send email
        params = {
            "from": "LouFrank TV <welcome@loufranktv.com>",
            "to": [request.email],
            "subject": "Welcome to LouFrank TV - Your Premium Entertainment Awaits!",
            "html": html_content,
            "text": text_content
        }
        
        response = resend.Emails.send(params)
        
        return EmailResponse(
            success=True,
            message="Welcome email sent successfully",
            email_id=response.get("id")
        )
    
    except Exception as e:
        print(f"Error sending welcome email: {str(e)}")
        return EmailResponse(
            success=False,
            message=f"Failed to send welcome email: {str(e)}",
            email_id=None
        )

@router.post("/trial-request", response_model=EmailResponse)
def send_trial_request(request: TrialRequestRequest):
    """
    Send a trial request email to the support team.
    """
    try:
        # Initialize Resend with API key from environment variable
        api_key = os.environ.get("RESEND_API_KEY")
        if not api_key:
            return EmailResponse(
                success=False,
                message="Email service not configured. Please contact us directly.",
                email_id=None
            )
        resend.api_key = api_key
        # Compose a robust HTML body for the trial request email
        html_body = f"""
        <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
        <html xmlns="http://www.w3.org/1999/xhtml">
        <head>
            <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
            <title>New Trial Request for Lou Frank TV</title>
            <style type="text/css">
                body, table, td, a {{ -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; }}
                table, td {{ mso-table-lspace: 0pt; mso-table-rspace: 0pt; }}
                img {{ -ms-interpolation-mode: bicubic; }}
                body {{ margin: 0; padding: 0; }}
                table {{ border-collapse: collapse !important; }}
                .ExternalClass {{ width: 100%; }}
                .ExternalClass, .ExternalClass p, .ExternalClass span, .ExternalClass font, .ExternalClass td, .ExternalClass div {{ line-height: 100%; }}
                .apple-link a {{ color: inherit !important; text-decoration: none !important; }}
                .btn-link a {{ color: #ffffff !important; text-decoration: none !important; }}
                img {{ border: 0; height: auto; line-height: 100%; outline: none; text-decoration: none; display: block; }}
            </style>
        </head>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; margin: 0; padding: 0;">
            <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #f4f4f4;">
                <tr>
                    <td align="center" style="padding: 20px 0;">
                        <table width="600" cellpadding="0" cellspacing="0" border="0" style="background-color: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
                            <tr>
                                <td align="center" style="padding: 20px 0;">
                                    <a href="https://www.loufranktv.com" target="_blank" style="text-decoration: none;">
                                        <img src="https://www.loufranktv.com/logo-loufrank-crew.png" alt="Lou Frank TV Logo" style="display: block; width:200px; max-width:100%; height:auto; margin: 0 auto;" />
                                    </a>
                                </td>
                            </tr>
                            <tr>
                                <td style="padding: 0 30px 20px 30px;">
                                    <p style="font-size: 16px; color: #333333;">Hello Owner,</p>
                                    <p style="font-size: 16px; color: #333333;">Someone requested a free trial:</p>
                                    <ul style="font-size: 16px; color: #333333; list-style-type: none; padding: 0;">
                                        <li style="margin-bottom: 10px;"><strong>Name:</strong> {request.name}</li>
                                        <li style="margin-bottom: 10px;"><strong>Email:</strong> {request.email}</li>
                                        {f'<li style="margin-bottom: 10px;"><strong>Phone:</strong> {request.phone}</li>' if request.phone else ''}
                                    </ul>
                                    <p style="font-size: 16px; color: #333333;">Please follow up as soon as possible.</p>
                                </td>
                            </tr>
                            <tr>
                                <td align="center" style="padding: 20px; font-size: 12px; color: #999999; background-color: #eeeeee;">
                                    <p>&copy; {datetime.now().year} Lou Frank TV. All rights reserved.</p>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
            </table>
        </body>
        </html>
        """
        params = {
            "from": "LouFrank TV Trial Requests <trials@loufranktv.com>",
            "to": ["loufranktv@gmail.com"],
            "subject": "New Trial Request!",
            "html": html_body,
            "reply_to": request.email
        }
        response = resend.Emails.send(params)
        return EmailResponse(
            success=True,
            message="Trial request submitted successfully",
            email_id=response.get("id")
        )
    
    except Exception as e:
        print(f"Error sending trial request email: {str(e)}")
        return EmailResponse(
            success=False,
            message=f"Failed to send email: {str(e)}",
            email_id=None
        )

@router.post("/send", response_model=EmailResponse)
def send_generic_email(request: GenericEmailRequest):
    """
    Send a generic email with custom content.
    """
    try:
        # Initialize Resend with API key
        api_key = os.environ.get("RESEND_API_KEY")
        if not api_key:
            return EmailResponse(
                success=False,
                message="Email service not configured",
                email_id=None
            )
        
        # Set Resend API key
        resend.api_key = api_key
        
        # Prepare recipients list
        to_emails = [recipient.email for recipient in request.to]
        
        # If html_content doesn't contain our templated container, wrap it in our premium template
        if "<div class=\"container\">" not in request.html_content:
            wrapped_html = f"""
            <html>
                <head>
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <style>
                        body {{ font-family: 'Arial', sans-serif; line-height: 1.6; color: #e2e8f0; margin: 0; padding: 0; background-color: #0f0f0f; }}
                        .container {{ max-width: 600px; margin: 0 auto; background-color: #0a0a0a; border-radius: 8px; overflow: hidden; }}
                        .header {{ background: linear-gradient(135deg, #000000, #1a1a1a); padding: 20px; text-align: center; border-bottom: 1px solid #333; }}
                        .logo {{ height: 60px; width: auto; }}
                        .content {{ padding: 30px; }}
                        .footer {{ background-color: #0a0a0a; padding: 20px; text-align: center; font-size: 12px; color: #6c7280; border-top: 1px solid #333; }}
                        h1, h2 {{ color: #ffffff; margin-top: 0; }}
                        .highlight {{ color: #17d1e0; }}
                        .divider {{ height: 1px; background: linear-gradient(to right, transparent, #333, transparent); margin: 20px 0; }}
                    </style>
                </head>
                <body>
                    <div class="container">
                        <div class="header">
                            <img class="logo" src="https://loufranktv.com/public/901661ac-f28e-4815-8069-61ae5363a100/logo-color.png" alt="LouFrank TV Logo">
                        </div>
                        <div class="content">
                            {request.html_content}
                        </div>
                        <div class="footer">
                            <p>© {datetime.now().year} LouFrank TV. All rights reserved.</p>
                            <p>Premium IPTV Service | 16,000+ Channels | Global Coverage</p>
                        </div>
                    </div>
                </body>
            </html>
            """
            html_to_send = wrapped_html
        else:
            html_to_send = request.html_content
            
        # Send email
        params = {
            "from": f"{request.from_name} <{request.from_email}>",
            "to": to_emails,
            "subject": request.subject,
            "html": html_to_send,
        }
        
        # Add optional parameters if provided
        if request.text_content:
            params["text"] = request.text_content
            
        if request.reply_to:
            params["reply_to"] = request.reply_to
        
        response = resend.Emails.send(params)
        
        return EmailResponse(
            success=True,
            message="Email sent successfully",
            email_id=response.get("id")
        )
    
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return EmailResponse(
            success=False,
            message=f"Failed to send email: {str(e)}",
            email_id=None
        )
