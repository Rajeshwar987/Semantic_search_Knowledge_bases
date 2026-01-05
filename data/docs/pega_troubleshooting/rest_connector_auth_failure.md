# REST Connector Authentication Failure

## Symptoms
- REST connector returns authentication or authorization errors
- Integration calls fail with HTTP 401 or 403 responses
- External system is reachable but requests are rejected

## Root Cause
- Incorrect credentials configured for the REST connector
- Authentication profile is missing or misconfigured
- Token or credential has expired
- External system access policies have changed

## Resolution Steps
1. Verify credentials configured in the authentication profile
2. Confirm the REST connector references the correct authentication profile
3. Refresh or regenerate tokens if applicable
4. Validate endpoint access requirements with the external system
5. Retest the integration after updating credentials

## Best Practices
- Store credentials securely using authentication profiles
- Monitor token expiration and renewal policies
- Validate integration configurations in lower environments before promotion
