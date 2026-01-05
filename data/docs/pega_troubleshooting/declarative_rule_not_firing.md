# Declarative Rule Not Firing as Expected

## Symptoms
- Declarative rule does not update target properties
- Expected calculations or updates do not occur
- No errors are displayed, but results are incorrect

## Root Cause
- Declarative rule conditions are not met
- Source or target properties are incorrectly configured
- Rule is not in the correct ruleset or version
- Conflicting rules override the expected behavior

## Resolution Steps
1. Verify the declarative rule conditions and trigger events
2. Confirm source and target property references are correct
3. Ensure the rule is available in the application ruleset stack
4. Check for conflicting rules affecting the same properties
5. Test the rule using controlled input data

## Best Practices
- Keep declarative logic simple and well-scoped
- Avoid overlapping rules that update the same properties
- Document declarative dependencies for maintainability
