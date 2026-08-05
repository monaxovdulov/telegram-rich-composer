# Security policy

## Supported version

Security fixes are applied to the latest release and the `main` branch.

## Reporting

Do not open a public issue for a bot token, recipient-routing flaw, path traversal, SSRF, secret leak, or duplicate-delivery vulnerability. Use GitHub private vulnerability reporting when enabled on the repository.

Do not include real tokens, chat IDs, user data, private media, or production request logs in a report. Use synthetic values and the smallest safe reproduction.

## Boundary

`CompositionSpec` is untrusted model output. The adapter owns authorization, recipient context, topic and reply IDs, capability truth, token access, local media roots, network policy, outbound secret scanning, and unknown-delivery reconciliation.
