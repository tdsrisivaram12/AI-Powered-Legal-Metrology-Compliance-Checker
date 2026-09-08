"""
Sends email notifications, e.g. "your product was flagged SUSPECTED
NON-COMPLIANCE" to a manufacturer, or a daily digest to an inspector.

Uses stdlib smtplib so no extra dependency is needed. In dev/test, pass
dry_run=True (default) so nothing actually goes over the network -- this
mirrors how CI should run it.
"""
from __future__ import annotations

import smtplib
from dataclasses import dataclass
from email.message import EmailMessage
from typing import List, Optional


@dataclass
class EmailConfig:
    smtp_host: str = "localhost"
    smtp_port: int = 587
    username: Optional[str] = None
    password: Optional[str] = None
    from_address: str = "no-reply@legal-metrology-checker.gov.in"
    use_tls: bool = True


@dataclass
class SentEmail:
    to: List[str]
    subject: str
    body: str
    dry_run: bool


class EmailSender:
    def __init__(self, config: Optional[EmailConfig] = None, dry_run: bool = True):
        self.config = config or EmailConfig()
        self.dry_run = dry_run
        self.outbox: List[SentEmail] = []  # populated in dry_run mode, useful for tests

    def send(self, to: List[str], subject: str, body: str) -> SentEmail:
        record = SentEmail(to=to, subject=subject, body=body, dry_run=self.dry_run)

        if self.dry_run:
            self.outbox.append(record)
            return record

        message = EmailMessage()
        message["From"] = self.config.from_address
        message["To"] = ", ".join(to)
        message["Subject"] = subject
        message.set_content(body)

        with smtplib.SMTP(self.config.smtp_host, self.config.smtp_port) as server:
            if self.config.use_tls:
                server.starttls()
            if self.config.username and self.config.password:
                server.login(self.config.username, self.config.password)
            server.send_message(message)

        return record

    def send_violation_alert(self, to: List[str], product_id: str, decision: str, findings_count: int) -> SentEmail:
        subject = f"Compliance Alert: {product_id} - {decision}"
        body = (
            f"Product {product_id} was evaluated with decision: {decision}.\n"
            f"{findings_count} finding(s) were recorded.\n"
            f"Please review in the Legal Metrology Compliance dashboard."
        )
        return self.send(to, subject, body)
