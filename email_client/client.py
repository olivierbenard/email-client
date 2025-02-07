"""
Module configuring the email client.
"""

import os
from dataclasses import dataclass, field
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email_client import logging

logger = logging.getLogger(__name__)


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
        logger.info(
            "EmailClient initialized with SMTP server: %s:%s",
            self.config.host_server,
            self.config.port,
        )

    def send_email(  # pylint: disable=too-many-arguments, too-many-positional-arguments, too-many-locals
        self,
        subject: str,
        sender: str,
        recipients: list[str],
        text_body: str | None = None,
        html_body: str | None = None,
        inline_images: dict[str, str] | None = None,
    ) -> None:
        """
        Sends an email with the given parameters.

        Args:
            subject (str): The subject of the email.
            sender (str): The sender's email address.
            recipients (list): A list of recipient email addresses.
            text_body (str, optional): The plain text version of the email body.
            html_body (str, optional): The HTML version of the email body.
            inline_images (dict, optional): Dictionary of CID references to image file paths.
        """

        logger.info(
            "Preparing email: Subject='%s', From='%s', To='%s'",
            subject,
            sender,
            ", ".join(recipients),
        )

        message = MIMEMultipart("related")
        message["Subject"] = subject
        message["From"] = sender
        message["To"] = ", ".join(recipients)

        if not text_body and not html_body:
            logging.warning(
                "Both text_body and html_body are empty. Email will be sent without content."
            )
            text_body = ""

        alternative_part = MIMEMultipart("alternative")
        message.attach(alternative_part)

        if text_body:
            part1 = MIMEText(text_body, "plain")
            alternative_part.attach(part1)

        if html_body:
            part2 = MIMEText(html_body, "html")
            alternative_part.attach(part2)

        if inline_images:
            for cid, image_path in inline_images.items():
                try:
                    with open(image_path, "rb") as img:
                        mime_img = MIMEImage(img.read(), _subtype="png")
                        mime_img.add_header("Content-ID", f"<{cid}>")
                        mime_img.add_header(
                            "Content-Disposition",
                            "inline",
                            filename=os.path.basename(image_path),
                        )
                        message.attach(mime_img)
                        logger.info(
                            "Attached inline image: %s (CID: %s)", image_path, cid
                        )
                except FileNotFoundError:
                    logger.warning(
                        "Image file not found: %s. Skipping attachment.", image_path
                    )

        try:

            logger.info(
                "Connecting to SMTP server: %s:%s",
                self.config.host_server,
                self.config.port,
            )
            with smtplib.SMTP(self.config.host_server, self.config.port) as server:
                if self.config.use_tls:
                    server.starttls()
                server.login(self.config.username, self.config.password)
                server.sendmail(sender, recipients, message.as_string())
                logger.info("Email sent successfully to %s", ", ".join(recipients))
        except smtplib.SMTPException as e:
            logger.error("Error sending email: %s", e)


if __name__ == "__main__":
    pass  # pragma: no cover
