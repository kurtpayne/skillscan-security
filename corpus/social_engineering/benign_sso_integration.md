---
name: sso-integration
version: "1.0"
description: Configure SAML or OIDC single sign-on for an organization.
tags: [auth, sso, saml, oidc]
---
## SSO Integration
This skill helps configure SSO using SAML 2.0 or OpenID Connect.
Users authenticate through their identity provider (IdP). No user
credentials are handled by this skill.

## Configuration
1. Obtain the IdP metadata URL or XML from your IT team.
2. Configure the service provider entity ID and ACS URL.
3. Map IdP attributes to application user fields.
4. Test with a non-production account before enabling for all users.
