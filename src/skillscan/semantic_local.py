from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from nltk.stem import PorterStemmer

from skillscan.models import Finding, Severity

_TOKEN_RE = re.compile(r"[a-zA-Z][a-zA-Z0-9_'-]{1,}")


@dataclass
class SemanticEvidence:
    confidence: float
    snippet: str


class LocalPromptInjectionClassifier:
    """Local, deterministic-features semantic prompt-injection classifier.

    Detects prompt-override / jailbreak / coercive-exfil patterns using stemmed
    feature scoring.  This classifier is additive to deterministic rules and does
    not call external models/APIs.
    """

    def __init__(self) -> None:
        self._stemmer = PorterStemmer()
        self._override_roots = {"ignor", "disregard", "forget", "overrid", "bypass", "jailbreak", "reset"}
        self._authority_roots = {"system", "develop", "prompt", "instruct", "polici", "guardrail", "safeti"}
        self._secrecy_roots = {"silent", "stealth", "covert", "hidden", "without", "conceal", "undetect"}
        self._data_roots = {
            "secret",
            "token",
            "credenti",
            "password",
            "cookie",
            "session",
            "apikey",
            "env",
            "ssh",
            "vault",
        }
        self._exfil_roots = {"send", "upload", "post", "transmit", "exfil", "webhook", "http", "request"}
        self._coercion_roots = {"must", "requir", "mandatori", "immedi", "now", "urgent", "cannot", "refus"}

    def _tokenize_and_stem(self, text: str) -> list[str]:
        return [self._stemmer.stem(t.lower()) for t in _TOKEN_RE.findall(text)]

    def classify(self, text: str) -> SemanticEvidence | None:
        tokens = self._tokenize_and_stem(text)
        if len(tokens) < 20:
            return None
        roots = set(tokens)

        override = len(roots & self._override_roots)
        authority = len(roots & self._authority_roots)
        secrecy = len(roots & self._secrecy_roots)
        data_access = len(roots & self._data_roots)
        exfil = len(roots & self._exfil_roots)
        coercion = len(roots & self._coercion_roots)

        score = 0.0
        score += min(override, 3) * 0.18
        score += min(authority, 3) * 0.1
        score += min(secrecy, 2) * 0.12
        score += min(data_access, 3) * 0.11
        score += min(exfil, 3) * 0.11
        score += min(coercion, 2) * 0.07

        # High-signal semantic conjunctions.
        if override > 0 and authority > 0:
            score += 0.12
        if (data_access > 0 and exfil > 0) or (secrecy > 0 and exfil > 0):
            score += 0.13
        if coercion > 0 and (override > 0 or secrecy > 0):
            score += 0.06

        confidence = min(round(score, 3), 0.95)
        if confidence < 0.62:
            return None

        lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
        keyword_re = re.compile(
            (
                r"ignore|override|system prompt|developer mode|"
                r"secret|token|credential|silent|without user|upload|send"
            ),
            re.IGNORECASE,
        )
        matched = [ln for ln in lines if keyword_re.search(ln)]
        snippet = (" | ".join(matched[:2]) if matched else lines[0])[:240]
        return SemanticEvidence(confidence=confidence, snippet=snippet)


class SocialEngineeringClassifier:
    """Stemmed feature classifier for social-engineering credential-harvest instructions.

    Targets the attack pattern where a skill instructs the AI to solicit credentials,
    tokens, or secrets from users using persuasion, reassurance, or urgency — without
    any prompt-override language that would trigger the prompt-injection classifier.

    Detection axes:
      - imperative:   directive verbs aimed at the AI (request, ask, tell, instruct…)
      - solicit:      collection verbs (paste, provide, share, send, enter, give…)
      - credential:   target data types (token, api key, password, secret, ssh key…)
      - social_eng:   persuasion / reassurance / pretext language (reassure, hesitate,
                      temporary, verify, ownership, convince, legitimate…)
      - urgency:      pressure language (urgent, immediately, required, must, cannot…)

    A finding fires when imperative + solicit + credential co-occur (the core pattern)
    and the social_eng or urgency axis adds supporting signal.
    """

    def __init__(self) -> None:
        self._stemmer = PorterStemmer()
        # Directive verbs: the skill is telling the AI to do something to the user
        self._imperative_roots = {
            "request", "ask", "tell", "instruct", "direct", "have", "prompt",
            "convinc", "persuad", "encourag", "requir", "demand",
        }
        # Collection verbs: how the credential is obtained
        self._solicit_roots = {
            "past", "provid", "share", "send", "enter", "type", "give",
            "suppli", "submit", "collect", "retriev", "obtain", "input",
        }
        # Target data types
        self._credential_roots = {
            "token", "credenti", "password", "passphras", "secret",
            "apikey", "api", "key", "ssh", "privat", "access",
        }
        # Social engineering / pretext language
        self._social_eng_roots = {
            "reassur", "hesit", "temporari", "verifi", "ownership",
            "convinc", "legitim", "trust", "onboard", "setup", "confirm",
            "account", "authent", "identifi",
        }
        # Urgency / pressure language
        self._urgency_roots = {
            "urgent", "immedi", "must", "cannot", "requir", "mandatori",
            "now", "quickli", "asap", "critic",
        }

    def _tokenize_and_stem(self, text: str) -> list[str]:
        return [self._stemmer.stem(t.lower()) for t in _TOKEN_RE.findall(text)]

    def classify(self, text: str) -> SemanticEvidence | None:
        tokens = self._tokenize_and_stem(text)
        # Minimum token count: short snippets are handled by SE-001 static rule
        if len(tokens) < 8:
            return None
        roots = set(tokens)

        imperative = len(roots & self._imperative_roots)
        solicit = len(roots & self._solicit_roots)
        credential = len(roots & self._credential_roots)
        social_eng = len(roots & self._social_eng_roots)
        urgency = len(roots & self._urgency_roots)

        # Core pattern: imperative + solicit + credential must all be present
        if imperative == 0 or solicit == 0 or credential == 0:
            return None

        score = 0.0
        score += min(imperative, 2) * 0.20
        score += min(solicit, 2) * 0.18
        score += min(credential, 2) * 0.18
        score += min(social_eng, 3) * 0.10
        score += min(urgency, 2) * 0.08

        # Conjunction bonuses
        if imperative > 0 and credential > 0 and solicit > 0:
            score += 0.15  # all three axes present
        if social_eng > 0 and credential > 0:
            score += 0.08  # pretext + credential target
        if urgency > 0 and credential > 0:
            score += 0.06  # pressure + credential target

        confidence = min(round(score, 3), 0.92)
        if confidence < 0.62:
            return None

        lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
        keyword_re = re.compile(
            r"request|ask|tell|instruct|paste|provide|share|send|enter|give|"
            r"token|api.?key|password|credential|secret|passphrase|private.?key|"
            r"reassure|hesitate|temporary|verify|ownership|convince",
            re.IGNORECASE,
        )
        matched = [ln for ln in lines if keyword_re.search(ln)]
        snippet = (" | ".join(matched[:2]) if matched else lines[0])[:240]
        return SemanticEvidence(confidence=confidence, snippet=snippet)


def local_prompt_injection_findings(path: Path, text: str) -> list[Finding]:
    evidence = LocalPromptInjectionClassifier().classify(text)
    if evidence is None:
        return []

    severity = Severity.HIGH if evidence.confidence >= 0.82 else Severity.MEDIUM
    return [
        Finding(
            id="PINJ-SEM-001",
            category="prompt_injection_semantic",
            severity=severity,
            confidence=evidence.confidence,
            title="Local semantic prompt-injection intent pattern",
            evidence_path=str(path),
            snippet=evidence.snippet,
            mitigation=(
                "Remove prompt-override/coercive instructions and any "
                "secret-collection or hidden exfil intent. "
                "Treat repository prompt text as untrusted input."
            ),
        )
    ]


def local_social_engineering_findings(path: Path, text: str) -> list[Finding]:
    """Emit SE-SEM-001 findings for social-engineering credential-harvest patterns.

    This is complementary to the SE-001 static rule: the static rule catches
    obvious single-sentence patterns; this classifier catches multi-sentence
    or paraphrased variants where the imperative/solicit/credential axes are
    distributed across the text.
    """
    evidence = SocialEngineeringClassifier().classify(text)
    if evidence is None:
        return []

    severity = Severity.HIGH if evidence.confidence >= 0.80 else Severity.MEDIUM
    return [
        Finding(
            id="SE-SEM-001",
            category="social_engineering",
            severity=severity,
            confidence=evidence.confidence,
            title="Local semantic social-engineering credential-harvest pattern",
            evidence_path=str(path),
            snippet=evidence.snippet,
            mitigation=(
                "Remove instructions that direct the AI to solicit credentials, tokens, "
                "or secrets from users. Use OAuth, delegated auth flows, or "
                "environment-variable injection instead of collecting secrets in-chat."
            ),
        )
    ]
