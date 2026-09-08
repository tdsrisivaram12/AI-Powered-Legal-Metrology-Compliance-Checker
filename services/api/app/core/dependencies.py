"""
Process-wide singletons wiring services/rules, services/compliance,
services/evidence, services/search, and services/notifications into the
API layer. In-memory state (search index, audit log, email outbox) is fine
for the MVP; swap for a real DB/queue when services/api/app/repositories
grows beyond stubs.
"""
from __future__ import annotations

from services.compliance.evaluator.evaluator import ComplianceEvaluator
from services.evidence.audit.audit_log import AuditLog
from services.evidence.storage.storage import EvidenceStorage
from services.notifications.email.email_sender import EmailSender
from services.notifications.push.push_sender import PushSender
from services.rules.engine.rules_engine import RulesEngine
from services.rules.versions.version_manager import VersionManager
from services.search.similarity.similarity import ViolationHistoryIndex

version_manager = VersionManager()
rules_engine = RulesEngine(version_manager)
compliance_evaluator = ComplianceEvaluator(version_manager)

evidence_storage = EvidenceStorage(base_dir="evidence_store")
audit_log = AuditLog()

violation_history = ViolationHistoryIndex()

# dry_run=True by default: no real email/push goes out until wired to real
# SMTP/FCM creds via environment config in services/api/app/core/config.py
email_sender = EmailSender(dry_run=True)
push_sender = PushSender()
