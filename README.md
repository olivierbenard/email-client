# email-client

A lightweight, Python-based email client designed to simplify the process of composing and sending emails programmatically.

## Configuration

To configure the sending of automatic emails:

1. Go to your Google Account's [Security Page](https://myaccount.google.com/security).
2. Ensure that the 2-Step Verification is turned on.
3. Go to the [App Passwords](https://myaccount.google.com/apppasswords) page.
4. Create an App (or select an existing one).
5. You will get a 16-characters password. Copy this password - it's your app password.

Create or edit the `.env` environment variables file:

```
SMTP_HOST = "smtp.example.com"
SMTP_PORT = "587"
SMTP_USERNAME = "<username>"
SMTP_PASSWORD = "<password>"
SMTP_USE_TLS = "true"
```

## Usage

```python
client = EmailClient()

client.send_email(
    subject="your_subject",
    sender="sender@gmail.com",
    recipients=["recipient@gmail.com"],
    text_body="Napoléon",
)
```
