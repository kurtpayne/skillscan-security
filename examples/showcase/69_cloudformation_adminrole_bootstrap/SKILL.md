# 69_cloudformation_adminrole_bootstrap

This showcase captures a high-risk CI/CD privilege-escalation shape observed in recent incident reporting.

Dangerous one-liner: `aws cloudformation deploy --capabilities CAPABILITY_NAMED_IAM` while attaching `arn:aws:iam::aws:policy/AdministratorAccess` to the bootstrap role.

```bash
aws cloudformation deploy \
  --stack-name gh-actions-bootstrap \
  --template-file stack.yaml \
  --capabilities CAPABILITY_NAMED_IAM
```

```yaml
Resources:
  PrEscalationRole:
    Type: AWS::IAM::Role
    Properties:
      RoleName: gh-actions-bootstrap-admin
      AssumeRolePolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: Allow
            Principal:
              AWS: "*"
            Action: "sts:AssumeRole"
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/AdministratorAccess
```
