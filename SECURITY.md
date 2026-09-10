# Security Policy

## ⚠️ Critical Warnings

This engine handles financial data and may execute trades or simulations.

**All agents, users, and developers MUST read and understand this document before using this engine.**

---

## Developer Responsibilities

You **MUST** ensure:

### 1. Explicit Consent
Always obtain explicit, informed consent before:
- Executing any real trades (not simulations)
- Making API calls that may incur costs
- Accessing user credentials or personal data
- Modifying financial data
- Performing actions with financial implications

**Consent must be:**
- Clear and unambiguous
- Specific to the action being taken
- Given by the account owner or authorized user
- Documented/logged for audit purposes

### 2. Input Validation
All user inputs must be validated before processing:

**Stock Symbols:**
- Validate format (letters, dots, hyphens only)
- Reject if length > 10 characters
- Sanitize to prevent injection attacks
- Validate against known exchanges

**Numeric Inputs:**
- Validate range constraints
- Check for reasonable values (e.g., price > 0)
- Reject NaN or infinity values
- Validate precision limits

**All Text Inputs:**
- Strip HTML tags
- Remove script tags
- Validate length constraints
- Check for malicious patterns
- Sanitize SQL injection attempts

### 3. Credential Handling

**NEVER:**
- Store credentials in plain text
- Log API keys, tokens, or passwords
- Transmit credentials over insecure channels
- Hardcode credentials in source code
- Commit credentials to version control

**ALWAYS:**
- Use secure credential stores (vaults, environment variables)
- Mask sensitive data in logs and outputs
- Rotate credentials regularly
- Limit credential scope and permissions
- Use .env files with .gitignore

### 4. Rate Limiting

Implement proper rate limiting:
- Respect data provider rate limits (usually 5-30 requests/minute)
- Implement exponential backoff on rate limit errors
- Cache responses where appropriate
- Don't hammer APIs with rapid retries
- Queue requests to avoid bursts

**Recommended backoff strategy:**
```
Attempt 1: Immediate
Attempt 2: Wait 1 second
Attempt 3: Wait 2 seconds
Attempt 4: Wait 4 seconds
Max attempts: 3-5
```

### 5. Error Handling

Properly handle all error scenarios:
- Network failures
- API timeouts
- Authentication errors
- Rate limit errors
- Invalid input errors
- Data format errors
- Exchange closed errors

**All errors must:**
- Be logged securely (without sensitive data)
- Provide clear, actionable messages to users
- Not expose internal system details
- Trigger appropriate retry or fallback logic
- Maintain system stability

### 6. Financial Data Integrity

- Validate all financial calculations
- Verify data sources
- Cross-check critical data
- Handle missing data gracefully
- Maintain audit trails
- Ensure data consistency

---

## User Warnings

**Before using this engine, be aware that:**

1. **Financial Responsibility**: All trades and actions are your responsibility. You are accountable for all financial outcomes.

2. **Paper Trading First**: Always test with simulated data before using real money.

3. **API Keys**: API keys are sensitive credentials. Protect them like passwords. Anyone with your API key can act as you and incur costs.

4. **Financial Impact**: Data providers may charge for usage, storage, or API calls. You are responsible for all costs incurred.

5. **Data Accuracy**: Financial data may be delayed, incomplete, or inaccurate. Always verify critical data.

6. **Market Risk**: All investments carry risk. This engine does not guarantee profits or prevent losses.

7. **Compliance**: Ensure your use complies with all applicable laws, regulations, and data provider terms of service.

---

## Data Provider-Specific Security Notes

### Alpha Vantage
- Rate limit: 5 requests per minute (free tier)
- Premium tier: 30 requests per minute
- Use API keys from environment variables
- Cache responses to avoid rate limits

### Yahoo Finance
- No API key required
- Rate limited by IP
- Respect robots.txt
- Use with caution in production

### Finnhub
- Rate limit: 60 requests per second (paid)
- Sandbox available for testing
- Requires API key
- WebSocket connections available

### Polygon
- Rate limits vary by plan
- Sandbox available
- Requires API key
- Real-time and historical data

### General Financial APIs
- Always check rate limits
- Use sandbox when available
- Never expose API keys in frontend
- Respect terms of service
- Cache data where possible

---

## Incident Response

### If You Discover a Security Vulnerability

**DO NOT:**
- Open a public GitHub issue
- Discuss in public forums
- Wait to report

**DO:**
1. Email immediately: security@stijnman.com
2. Include:
   - Steps to reproduce the vulnerability
   - Impact assessment (what could an attacker do?)
   - Suggested fix (if you have one)
3. Wait for acknowledgment before disclosing to others
4. Give maintainers reasonable time to fix before public disclosure

### If Your Credentials Are Compromised

1. **Immediately revoke** all compromised API keys/tokens
2. **Rotate** all credentials that may have been exposed
3. **Audit** all recent API calls for suspicious activity
4. **Report** to the data provider's security team
5. **Update** your engine's credential store
6. **Investigate** how the compromise occurred
7. **Document** the incident and response

### If Incorrect Data Was Used

1. **Stop** all automated trading immediately
2. **Verify** all data sources
3. **Check** for any executed trades
4. **Review** all recent decisions
5. **Correct** any errors
6. **Document** the incident

---

## Compliance Considerations

### Financial Regulations
- Comply with all applicable financial regulations
- Understand licensing requirements for data
- Respect exchange rules and restrictions
- Maintain proper records for audits

### Data Protection
- User data may be subject to privacy regulations
- Handle personal data according to GDPR/CCPA
- Anonymize data where possible
- Respect user privacy preferences

### Platform Terms of Service
- All actions must comply with data provider TOS
- Automated access may be restricted
- Check platform's automation/robot policies
- Some platforms prohibit AI-driven trading

### Acceptable Use Policies
- Don't use for spam or abuse
- Don't create accounts for illegal purposes
- Don't bypass platform protections
- Don't use for market manipulation
- Respect all platform policies
- Don't engage in front-running

---

## Security Checklist for Developers

Before deploying or using this engine:

- [ ] All API credentials stored securely
- [ ] Input validation implemented for all user inputs
- [ ] Explicit consent obtained before sensitive operations
- [ ] Rate limiting configured
- [ ] Error handling implemented
- [ ] Sensitive data masked in logs
- [ ] Security warnings displayed to users
- [ ] Platform TOS reviewed and complied with
- [ ] Incident response plan documented
- [ ] All calculations verified
- [ ] Data sources validated

---

## Security Best Practices

### Code Security
- Use type hints for better code clarity
- Validate all function inputs
- Use context managers for resource handling
- Implement proper exception handling
- Use logging instead of print statements
- Keep dependencies updated

### Data Security
- Encrypt sensitive data at rest
- Use HTTPS for all communications
- Validate SSL certificates
- Sanitize all outputs
- Use parameterized queries
- Implement data validation

### Network Security
- Use firewalls and network segmentation
- Limit exposure of APIs
- Implement authentication for all endpoints
- Use rate limiting at the network level
- Monitor for suspicious activity

---

## Contact

**Security Issues**: security@stijnman.com  
**General Questions**: Open a GitHub issue  
**Maintainer**: [Stijnman](https://github.com/Stijnman)

---

*Last updated: September 11, 2026*
