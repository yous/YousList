# Contributing

## Issue reporting

- Check that the issue has not already been reported.
- Check that the issue has not already been fixed in the latest code (`master`).
- Specify the problematic URL on which the issue can be reproduced.

## Pull requests

- Make sure that every entry follows [Adblock Plus filter rules](https://adblockplus.org/en/filters).
- Update the version with the format `yyyyMMdd`.
- Alphabetically order every entry. You can check with `bin/check_sorted.py youslist.txt`.
- Do not add extra empty line.
- Build `Rules.1blockpkg.json` and `Rules.1blockpkg` from `youslist.txt` with `bin/release`.
- Test `youslist.txt` and `Rules.1blockpkg.json` with `bin/test`.

## Scripts

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

Check whether every entry entry is ordered alphabetically.

``` sh
bin/check_sorted.py youslist.txt
```

### `bin/generate_rules.py`

Update `Rules.1blockpkg.json` based on the filter.

``` sh
bin/generate_rules.py youslist.txt > Rules.1blockpkg.json
```

If you're using Python older than or equal to 2.6, you should install
dependencies by running `pip install -r requirements26.txt`.

### `bin/minify_pkg.py`

Update `Rules.1blockpkg` based on the `Rules.1blockpkg.json`.

``` sh
bin/minify_pkg.py
```

### `bin/prettify_pkg.py`

Update `Rules.1blockpkg.json` based on the `Rules.1blockpkg`

``` sh
bin/prettify_pkg.py
```
