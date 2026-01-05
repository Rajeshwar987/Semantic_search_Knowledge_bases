# Obj-Save Failed Error During Case Processing

## Symptoms
- Error message: "Obj-Save failed"
- Case save or commit operation fails
- Transaction is rolled back unexpectedly

## Root Cause
- Mandatory property values are missing
- Property data types are incompatible
- Database constraints are violated
- Incorrect declarative or activity logic modifies data during save

## Resolution Steps
1. Review logs to identify the property causing the save failure
2. Validate required fields are populated before save
3. Check data types and property definitions
4. Review declarative rules or activities executed during commit
5. Correct the data issue and retry the transaction

## Best Practices
- Validate data before performing save operations
- Minimize complex logic during commit processing
- Use appropriate error handling to capture save failures
