# AWS Config Notifier
This will be heavily based on IAM Sleuth. 

The goal of this will be to create a SNS topic notification that is a rollup report of AWS config compliance statuses.
ie:
```
:aws: you have $x total resources marked as non-compliant in $account
resource 1: non-compliant-r1
resource 2: non-compliant-r2
please continue to $link-to-config-dashboard
```