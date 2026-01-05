# Flow Action Rule Not Found Error

## Symptoms
- Error message: "Flow Action Rule Not Found"
- Assignment submission fails
- Case processing stops at a specific step

## Root Cause
- Flow action rule is missing or renamed
- Rule is not included in the application ruleset
- Incorrect ruleset version is referenced in the flow
- Cache contains outdated rule references

## Resolution Steps
1. Verify that the flow action rule exists in the application ruleset
2. Check that the correct ruleset version is available to the application
3. Confirm the flow references the correct flow action name
4. Clear the rule cache if recent changes were made
5. Retry the assignment submission

## Best Practices
- Avoid deleting or renaming rules used in active flows
- Use consistent ruleset versioning across environments
- Validate flows after rule changes before deployment
