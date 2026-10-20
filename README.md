# Pied Piper example packages

Fixed-data billing packages for the [Submilli](https://github.com/submilli/submilli-runtime)
book. Pied Piper (`pied_piper`) has two charges totaling 6,150 cents. Hooli
(`hooli`) has one charge. No credential or network call is needed.

## Install

```sh
submilli install submilli/pied-piper @submilli/pied-piper-billing
```

For a reproducible installation, pin this repository release:

```sh
submilli install submilli/pied-piper@v0.1.1 @submilli/pied-piper-billing
```

The package scope is `@submilli` because Submilli requires it to match the
GitHub owner. Version 0.1.0 provides `pied-piper.example/charges.list`.
See [the package guide](packages/pied-piper-billing/README.md) for its Blueprint.

## Compatibility

`@submilli/acme-billing` version 0.1.1 remains available with its original
`acme.com/charges.list` capability. The old `submilli/acme` repository URL
redirects to this repository. Existing pinned commits remain available.

```sh
submilli install submilli/acme @submilli/acme-billing
```

Both packages accept `pied_piper` and `hooli`, plus the historical IDs
`cus_northwind` and `cus_initech`. Results preserve the ID supplied by the
caller. Each package checks its own capability against that exact supplied
ID before resolving aliases. A grant for one package's capability does not
grant the other capability, and an alias does not broaden a customer filter.

## Build and verify

```sh
submilli build test
submilli build publish-local
python3 tests/verify_install.py --cli /path/to/submilli
```

The integration check uses a temporary package store and tests both package
identities, customer aliases, denied customer access and separate capability
grants. To verify published source installation through both repository names:

```sh
python3 tests/verify_install.py --cli /path/to/submilli --published
```
