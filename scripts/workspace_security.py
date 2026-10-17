"""Local data boundaries and redaction; no shell, network or model execution."""
import re
import hashlib
import unicodedata
from pathlib import Path

if __package__:
    from .check_workspace import local_path, linked_path
else:
    from check_workspace import local_path, linked_path

MAX_DOCUMENT = 1024 * 1024
TRUST = "UNTRUSTED_DATA"
SECRET_PATTERNS = (
    ("PRIVATE_KEY", r"-----BEGIN (?:RSA |EC |OPENSSH |DSA |ENCRYPTED )?PRIVATE KEY-----[\s\S]*?(?:-----END [A-Z ]*PRIVATE KEY-----|$)"),
    ("PROVIDER_TOKEN", r"\b(?:sk-(?:proj-|svcacct-)?[A-Za-z0-9_-]{20,}|gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|AKIA[A-Z0-9]{16})\b"),
    ("BEARER_TOKEN", r"(?i)\bBearer\s+[A-Za-z0-9._~+/-]{16,}"),
    ("CREDENTIAL_ASSIGNMENT", r"""(?i)\b(?:api[_-]?key|access[_-]?token|client[_-]?secret|password)\s*["']?\s*[:=]\s*["']?[A-Za-z0-9/+_.-]{12,}"""),
    ("URL_CREDENTIAL", r"(?i)https?://[^\s/@:]+:[^\s/@]+@[^\s]+"),
    ("URL_TOKEN", r"(?i)[?&](?:token|api_key|access_token)=[A-Za-z0-9._~-]{12,}"),
    ("LABELED_IDENTITY", r"""(?i)\b(?:national_id|passport_number|bank_account|ssn|date_of_birth)\s*[:=]\s*["']?[A-Za-z0-9_-]{6,}"""),
)
INJECTION_PATTERNS = (
    ("OVERRIDE", r"(?is)\b(?:ignore|override|disregard)\b.{0,65}\b(?:previous|system|developer|instructions|polic(?:y|ies)|AGENTS\.md)\b"),
    ("ROLE_SPOOF", r"(?im)(?:<\|(?:im_start|start_header_id)\|>\s*(?:system|developer)|</?(?:system|developer)>|^\s*(?:\[|#{1,6}\s*)?(?:SYSTEM|DEVELOPER)\s*(?:\]|:))"),
    ("EXFILTRATION", r"(?is)\b(?:reveal|exfiltrate|print|send|upload|read)\b.{0,80}(?:\.env\b|private.?key|credentials|secrets|environment variables)"),
    ("POLICY_CHANGE", r"(?is)\b(?:edit|modify|overwrite|replace|delete|disable)\b.{0,60}(?:AGENTS\.md|SCHEMA\.md|permissions|security rules)"),
    ("TOOL_SPOOF", r"(?im)(?:^\s*(?:TOOL_RESULT|TOOL_OUTPUT|assistant to=)|<tool_result>|<function_call>)"),
    ("SOURCE_COMMAND", r"(?is)(?:execute|run)\s+(?:this\s+)?(?:shell|powershell|bash|command)|(?:call|invoke)\s+(?:the\s+)?(?:exec_command|apply_patch|tools\.)"),
    ("ACTIVE_MARKUP", r"(?is)<script\b|javascript\s*:|<iframe\b|<img\b[^>]*\bonerror\s*="),
)


class SecurityError(ValueError):
    """Fixed code only; do not embed attacker-controlled text in exceptions."""


def secret_codes(text):
    return sorted({code for code, pattern in SECRET_PATTERNS if re.search(pattern, text)})


def redact(value):
    if isinstance(value, str):
        for _, pattern in SECRET_PATTERNS:
            value = re.sub(pattern, "[REDACTED]", value)
        return value
    if isinstance(value, dict):
        return {redact(str(key)): redact(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [redact(item) for item in value]
    return value


def inspect_data(text):
    if not isinstance(text, str) or len(text.encode("utf-8")) > MAX_DOCUMENT:
        raise SecurityError("DOCUMENT_LIMIT")
    # Normalization is only for detection, never for rewriting source bytes.
    normalized = unicodedata.normalize("NFKC", text)
    normalized = "".join(c for c in normalized if unicodedata.category(c) != "Cf")
    return sorted({code for code, pattern in INJECTION_PATTERNS if re.search(pattern, normalized)})


def require_safe_data(text):
    if secret_codes(text):
        raise SecurityError("SENSITIVE_CONTENT")
    if inspect_data(text):
        raise SecurityError("UNTRUSTED_CONTENT")


def read_data(root, relative):
    root = Path(root).absolute()
    if linked_path(root):
        raise SecurityError("LINKED_ROOT")
    path = local_path(root, root, relative)
    if path.suffix.lower() not in {".md", ".txt"} or not any(
            path.is_relative_to(root / folder) for folder in ("sources/raw", "wiki", "decisions")):
        raise SecurityError("READ_DENIED")
    if path.stat().st_size > MAX_DOCUMENT:
        raise SecurityError("DOCUMENT_LIMIT")
    data = path.read_bytes()
    if len(data) > MAX_DOCUMENT:
        raise SecurityError("DOCUMENT_LIMIT")
    text = data.decode("utf-8-sig")
    require_safe_data(text)
    return {"trust": TRUST, "origin": relative, "text": text,
            "content_hash": "sha256:" + hashlib.sha256(data).hexdigest()}


def audit_security(root):
    """Scan only approved public documentation; never open suspected secret files."""
    root = Path(root).absolute()
    issues = []
    if linked_path(root):
        return ["ERROR LINKED_ROOT .: security scan refused."]
    folders = ("wiki", "projects", "decisions", "handoffs", "prompts", "templates", "experiments", "reports")

    def visit(path):
        try:
            path = local_path(root, root, path.relative_to(root).as_posix())
        except (ValueError, OSError):
            issues.append("WARNING SENSITIVE_LOCATION [REDACTED_PATH]: contents not opened.")
            return
        if path.is_dir():
            for child in sorted(path.iterdir()):
                yield from visit(child)
        elif path.suffix.lower() in {".md", ".json", ".csv"}:
            yield path

    try:
        candidates = list(root.glob("*.md"))
        for folder in folders:
            path = root / folder
            if path.exists() or linked_path(path):
                candidates.append(path)
        # Filename-only inventory of root environment/key locations; no contents.
        for path in root.iterdir():
            try:
                local_path(root, root, path.name)
            except ValueError:
                if path.name not in {".git", ".obsidian", ".gitignore"}:
                    issues.append("WARNING SENSITIVE_LOCATION [REDACTED_PATH]: contents not opened.")
        for candidate in candidates:
            for path in visit(candidate):
                if path.stat().st_size > MAX_DOCUMENT:
                    issues.append("WARNING SCAN_LIMIT [REDACTED_PATH]: contents not scanned.")
                    continue
                codes = secret_codes(path.read_text(encoding="utf-8-sig"))
                if codes:
                    issues.append("ERROR SENSITIVE_CONTENT [REDACTED_PATH]: " + ",".join(codes) + ".")
    except (OSError, UnicodeError):
        issues.append("ERROR SECURITY_SCAN .: a permitted document could not be scanned.")
    return sorted(set(issues))
