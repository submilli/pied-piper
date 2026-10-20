# Pied Piper example packages

The example packages the [Submilli](https://github.com/submilli/submilli-runtime)
book uses. Pied Piper is the fictional company whose support agent the book
follows. The packages remain scoped `@submilli/` because a package's scope
must be the GitHub owner it is installed from; the `acme-` package prefix is
part of the published compatibility name and remains unchanged.

| Package | What it is |
| --- | --- |
| `@submilli/acme-billing` | A charge lookup over fixed data, standing in for a billing API. No credential needed. |

Install one into your local store:

```sh
submilli install submilli/acme @submilli/acme-billing
```

Build and test from a checkout:

```sh
submilli build test
submilli build publish-local
```
