# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in Solar Cumulus Optimizer, please report it responsibly:

1. **DO NOT** open a public GitHub issue for security vulnerabilities
2. Email the details to: your-email@example.com
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

## Response Timeline

- **Initial Response**: Within 48 hours
- **Investigation**: Within 1 week
- **Fix Release**: Within 2 weeks (if applicable)
- **Public Disclosure**: After fix is released

## Security Best Practices

When using Solar Cumulus Optimizer:

- Keep Home Assistant updated to the latest version
- Use strong authentication for Home Assistant
- Keep your Linky credentials secure
- Review automations for unintended access
- Monitor logs for suspicious activity
- Enable Home Assistant backups

## Supported Versions

| Version | Supported          |
|---------|-------------------|
| 1.0.x   | ✅ Yes            |
| < 1.0   | ❌ No             |

## Known Limitations

- Component uses local Home Assistant only (no cloud)
- No external API calls (fully local)
- All data stays on your Home Assistant instance
- No telemetry or tracking

## Security Considerations

### Local Data Only
- ✅ All processing happens locally
- ✅ No data sent to external servers
- ✅ No telemetry or tracking

### Permissions
- Component only controls specified relay
- Cannot modify other entities without explicit setup
- Config flow validates entity selection

### Best Practices
1. Use strong Home Assistant passwords
2. Keep Home Assistant updated
3. Review automations for typos
4. Monitor unknown device access
5. Use network segmentation if possible

## Vulnerability Disclosure

If a vulnerability is reported:
1. Acknowledge receipt within 24 hours
2. Develop fix in private branch
3. Test thoroughly
4. Release patched version
5. Publish security advisory
6. Credit reporter (if desired)

## Questions?

For security questions (not vulnerability reports), use:
- GitHub Discussions
- Home Assistant Community Forum

---

**Last Updated**: 2024  
**Contact**: your-email@example.com
