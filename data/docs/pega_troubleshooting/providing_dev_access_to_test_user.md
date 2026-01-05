# Providing Developer Access to a Test User

## Symptoms
- Test user is unable to access developer tools or Dev Studio
- User receives authorization or access denied errors
- Application rules are not visible to the test user
- User can log in but cannot perform development or configuration actions

## Root Cause
- Test user does not have a developer role assigned
- Required access group is missing or incorrectly configured
- Application rulesets are not available to the user’s access group
- User is associated with an end-user or operator-only role instead of a developer role

## Resolution Steps
1. Verify the operator record for the test user
2. Assign an appropriate developer access group to the user
3. Ensure the access group includes developer roles such as rule authoring or configuration roles
4. Confirm that required application rulesets are listed in the access group with correct versioning
5. Log out and log back in to refresh the user session
6. Validate that the user can now access developer tools and application rules

## Best Practices
- Use dedicated test user accounts for development and configuration activities
- Follow the principle of least privilege when assigning developer access
- Regularly review access groups and roles to prevent unauthorized access
- Document access changes to maintain auditability and traceability
