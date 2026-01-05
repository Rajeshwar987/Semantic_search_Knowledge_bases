# Adding a Report to the Insights Tab in a Constellation Application

## Symptoms
- Report does not appear in the Insights tab of a Constellation application
- Insights tab is visible but shows no reports
- Newly created report is available in Dev Studio but not accessible to users
- Users receive errors or see empty content when accessing the Insights tab

## Root Cause
- Report is not configured for Constellation-compatible presentation
- Report is not associated with the correct application or access group
- Required Insights configuration or category is missing
- User does not have sufficient privileges to view the report
- Report definition is not included in the ruleset available to the application

## Resolution Steps
1. Verify that the report definition is compatible with Constellation UI
2. Ensure the report is associated with the correct application context
3. Assign the report to the appropriate Insights category or configuration
4. Confirm that the report’s ruleset and version are included in the application stack
5. Validate that the user’s access group has permission to view the report
6. Refresh the application or log out and log back in to apply configuration changes
7. Reopen the Insights tab and confirm that the report is visible and accessible

## Best Practices
- Validate report compatibility with Constellation before deployment
- Use consistent naming and categorization for Insights reports
- Limit report visibility based on user roles to maintain security
- Test Insights configuration changes using a non-production user
- Document report additions to support maintainability and audit requirements
