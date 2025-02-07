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

### Send an email without content

```python
client = EmailClient()

client.send_email(
    subject="Text Only Email",
    sender="your_email@example.com",
    recipients=["recipient@gmail.com"],
)
```

### Send an email with only a text body (html_body omitted)

```python
client = EmailClient()

client.send_email(
    subject="Text Only Email",
    sender="your_email@example.com",
    recipients=["recipient@gmail.com"],
    text_body="Napoléon",
)
```

### Send an email with only an HTML body (text_body omitted)

```python
client_email = EmailClient()

client_email.send_email(
    subject="HTML Only Email",
    sender="your_email@example.com",
    recipients=["recipient@example.com"],
    html_body="<h2>Only HTML Content</h2><p>This email has no plain text body.</p>",
)
```

### Send an email with both text and HTML

```python
client_email = EmailClient()

client_email.send_email(
    subject="Text & HTML Email",
    sender="your_email@example.com",
    recipients=["recipient@example.com"],
    text_body="This is the plain text version.",
    html_body="<h2>This is the HTML version</h2><p>It has formatting.</p>",
)
```

### Send an email with an inline image (CID-based)L

```python
client_email = EmailClient()

client_email.send_email(
    subject="Email with Inline Image",
    sender="your_email@example.com",
    recipients=["recipient@example.com"],
    html_body='<h2>Image Example</h2><img src="cid:example_image">',
    inline_images={"example_image": "path/to/image.png"},
)
```
