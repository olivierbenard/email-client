"""
Module configuring the email client.
"""

import os
from dataclasses import dataclass, field
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv


load_dotenv()


@dataclass
class EmailConfig:
    """
    Configuration for the EmailClient.
    Loads SMTP settings from environment variables with default values.
    """

    host_server: str = os.getenv("SMTP_HOST_SERVER", "smtp.example.com")
    port: int = int(os.getenv("SMTP_PORT", "587"))
    username: str = os.getenv("SMTP_USERNAME", "<username>")
    password: str = os.getenv("SMTP_PASSWORD", "<password>")
    use_tls: bool = field(
        default_factory=lambda: os.getenv("SMTP_USE_TLS", "True").lower()
        in ("true", "1", "yes")
    )


class EmailClient:  # pylint: disable=too-few-public-methods
    """
    A simple email client to send emails via SMTP.
    """

    def __init__(self, config: EmailConfig | None = None) -> None:
        """
        Initializes the EmailClient with the given configuration.
        """
        self.config = config or EmailConfig()

    def send_email(  # pylint: disable=too-many-arguments, too-many-positional-arguments
        self,
        subject: str,
        sender: str,
        recipients: list[str],
        text_body: str,
        html_body: str | None = None,
    ) -> None:
        """
        Sends an email with the given parameters.

        Args:
            subject (str): The subject of the email.
            sender (str): The sender's email address.
            recipients (list): A list of recipient email addresses.
            text_body (str): The plain text version of the email body.
            html_body (str, optional): The HTML version of the email body.
        """

        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = sender
        message["To"] = ", ".join(recipients)

        part1 = MIMEText(text_body, "plain")
        message.attach(part1)

        if html_body:
            part2 = MIMEText(html_body, "html")
            message.attach(part2)

        try:

            with smtplib.SMTP(self.config.host_server, self.config.port) as server:
                if self.config.use_tls:
                    server.starttls()
                server.login(self.config.username, self.config.password)
                server.sendmail(sender, recipients, message.as_string())
                print("Email sent successfully.")
        except smtplib.SMTPException as e:
            print(f"Error sending email: {e}")


if __name__ == "__main__":
    pass  # pragma: no cover
