import smtplib
import pytest
from unittest.mock import MagicMock
from email_client.client import (
    EmailConfig,
    EmailClient,
)


@pytest.fixture(params=[True, False], ids=["with_tls", "no_tls"])
def test_config(request):
    """
    Fixture to create a test EmailConfig instance with known values.

    The fixture will run twice:
      - Once with use_tls=True
      - Once with use_tls=False
    """
    return EmailConfig(
        host_server="smtp.test.com",
        port=587,
        username="test_user",
        password="test_pass",
        use_tls=request.param,
    )


@pytest.fixture
def email_client(test_config):
    """
    Fixture to create an EmailClient instance using the parametrized test configuration.
    """
    return EmailClient(test_config)


@pytest.fixture
def mock_smtp(monkeypatch):
    """
    Fixture to patch smtplib.SMTP and provide a mock SMTP instance.
    """
    # Create a mock SMTP instance.
    smtp_instance = MagicMock()

    # Create a mock context manager that returns smtp_instance on __enter__.
    smtp_context = MagicMock()
    smtp_context.__enter__.return_value = smtp_instance

    # Monkey-patch smtplib.SMTP to always return our context manager.
    monkeypatch.setattr(smtplib, "SMTP", lambda *args, **kwargs: smtp_context)

    return smtp_instance


def test_send_email_success(email_client, mock_smtp, capsys):
    """
    Test that send_email successfully calls SMTP methods when everything works as expected.
    """
    subject = "Test Subject"
    sender = "sender@test.com"
    recipients = ["recipient@test.com"]
    text_body = "This is a test email."
    html_body = "<p>This is a test email.</p>"

    # Ensure the mock SMTP instance has the necessary methods.
    mock_smtp.starttls = MagicMock()
    mock_smtp.login = MagicMock()
    mock_smtp.sendmail = MagicMock()

    # Call the send_email method.
    email_client.send_email(subject, sender, recipients, text_body, html_body)

    # Verify that starttls, login, and sendmail were called as expected.
    if email_client.config.use_tls:
        mock_smtp.starttls.assert_called_once()
    else:
        # Verify that starttls() was NOT called.
        mock_smtp.starttls.assert_not_called()

    mock_smtp.login.assert_called_once_with(
        email_client.config.username, email_client.config.password
    )

    mock_smtp.sendmail.assert_called_once_with(
        sender, recipients, mock_smtp.sendmail.call_args[0][2]
    )

    # Optionally, capture the output and check for the success message.
    captured = capsys.readouterr().out
    assert "Email sent successfully." in captured


def test_send_email_failure(email_client, mock_smtp, capsys):
    """
    Test that send_email handles SMTP exceptions and prints an error message.
    """
    subject = "Test Failure"
    sender = "sender@test.com"
    recipients = ["recipient@test.com"]
    text_body = "This will simulate a failure."

    # Ensure the mock SMTP instance has the necessary methods.
    mock_smtp.starttls = MagicMock()
    mock_smtp.login = MagicMock()
    # Raise an exception when sendmail is called.
    mock_smtp.sendmail.side_effect = smtplib.SMTPException("Simulated failure")

    # Call send_email; the exception should be caught.
    email_client.send_email(subject, sender, recipients, text_body)

    # Capture output and verify that the error message is printed.
    captured = capsys.readouterr().out
    assert "Error sending email:" in captured
    assert "Simulated failure" in captured
