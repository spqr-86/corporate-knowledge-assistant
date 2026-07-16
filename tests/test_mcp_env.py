"""The MCP subprocess must receive only the env vars it needs, not the whole
parent environment — a security assistant that spawns a child process should
not hand it unrelated secrets (AWS keys, tokens) it never uses."""

from agents.hr_domain_agent import _mcp_subprocess_env


def test_whitelists_needed_vars_and_drops_unrelated_secrets(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    monkeypatch.setenv("CKA_MODEL_ID", "openai/gpt-4o-mini")
    monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "should-not-leak")

    env = _mcp_subprocess_env()

    assert env["OPENAI_API_KEY"] == "sk-test"
    assert env["CKA_MODEL_ID"] == "openai/gpt-4o-mini"  # CKA_* overrides pass through
    assert "AWS_SECRET_ACCESS_KEY" not in env
    assert "PATH" in env  # needed so the child resolves the venv interpreter


def test_whitelists_tls_and_locale_vars(monkeypatch):
    """The MCP child makes HTTPS calls (OpenAI embeddings). Custom CA bundles
    and locale are configured via env in conda/Nix/corporate-proxy setups —
    stripping them silently breaks TLS/encoding in prod though it works on a
    dev box with system certs."""
    monkeypatch.setenv("SSL_CERT_FILE", "/etc/ssl/custom-ca.pem")
    monkeypatch.setenv("LANG", "en_US.UTF-8")

    env = _mcp_subprocess_env()

    assert env["SSL_CERT_FILE"] == "/etc/ssl/custom-ca.pem"
    assert env["LANG"] == "en_US.UTF-8"
