# Brute Force Playbook

Brute force activity usually involves repeated authentication attempts against SSH, RDP, VPN, web login, or other access services.

Recommended response:

- Block or rate-limit the source IP when attempts exceed policy.
- Check whether any account had a successful login after repeated failures.
- Enforce MFA and strong password policy.
- Review authentication logs around the same time window.
- Map to MITRE ATT&CK technique T1110 where appropriate.
