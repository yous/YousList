# Contributing

## Issue reporting

- Check that the issue has not already been reported.
- Check that the issue has not already been fixed in the latest code (`master`).
- Specify the problematic URL on which the issue can be reproduced.

## Pull requests

- Make sure that every entry follows [Adblock Plus filter rules](https://adblockplus.org/en/filters).
- Update the version with the format `yyyyMMdd`.
- Alphabetically order every entry.
- Do not add extra empty line.
- Build `Rules.1blockpkg.json` and `Rules.1blockpkg` from `youslist.txt` with `bin/release`.
- Test `youslist.txt` and `Rules.1blockpkg.json` with `bin/test`.

## Scripts

### `bin/install_pkg`

Install `Rules.1blockpkg` on macOS.

### `bin/release`

Build `Rules.1blockpkg.json` and `Rules.1blockpkg` from `youslist.txt`.

``` sh
bin/release
```

### `bin/test`

Test `youslist.txt` and `Rules.1blockpkg.json`.

``` sh
bin/test
```

### `bin/check_sorted.py`

Check whether every entry is ordered alphabetically.

``` sh
python bin/check_sorted.py youslist.txt
```

### `bin/checked_sorted_hosts.py`

Check whether every host is ordered alphabetically.

``` sh
python bin/checked_sorted_hosts.py hosts.txt
```

### `bin/generate_rules.py`

Update `Rules.1blockpkg.json` based on the filter.

``` sh
python bin/generate_rules.py youslist.txt > Rules.1blockpkg.json
```

### `bin/minify_pkg.py`

Update `Rules.1blockpkg` based on the `Rules.1blockpkg.json`.

``` sh
python bin/minify_pkg.py
```

### `bin/prettify_pkg.py`

Update `Rules.1blockpkg.json` based on the `Rules.1blockpkg`

``` sh
python bin/prettify_pkg.py
```
