# Label Normalizer — cold example

This fully synthetic, dependency-free project shows the small starting point used
by the paired teaching example. It turns display labels into deterministic
comparison keys. Keep the original label for display because normalization is
intentionally destructive.

Run the native check from this directory:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
```

The paired project implements the same normalization rule with a package, CLI,
and concise project guidance. This folder contains no benchmark result.
