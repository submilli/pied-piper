# @submilli/pied-piper-billing

Lists the charges on one customer's account, over fixed data. It stands
in for a real billing API in the Submilli book's examples, so it needs
no credential and makes no network call.

## Grant it

The package provides one operation, `pied-piper.example/charges.list`, with one
field a rule can test, `customerId`. Grant it for the customer the
session is for:

```yaml
variables:
  customerId:
    required: true
packages:
- '@submilli/pied-piper-billing'
permissions:
  main:
  - capability: pied-piper.example/charges.list
    filter: customerId == ${vars.customerId}
    action: allow
  '@submilli/pied-piper-billing': []
```

The package's own list is empty: it reads nothing and calls nothing.
