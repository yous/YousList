# Contributing

## Issue reporting

- Check that the issue has not already been reported.
- Check that the issue has not already been fixed in the latest code (`master`).
- Specify the problematic URL on which the issue can be reproduced.

## Pull requests

- Make sure that every entry follows [Adblock Plus filter rules](https://adblockplus.org/en/filters).
- Update the [checksum](https://adblockplus.org/en/filters#special-comments).
  If you use Vim, you can use [adblock-filter.vim](https://github.com/mojako/adblock-filter.vim).
  Also you can run `./bin/add_checksum.py youslist.txt > youslist.txt`.
  Validate the checksum by running `./bin/validate_checksum.py youslist.txt`.
- Update the version with the format `yyyyMMdd`.
- Alphabetically order every entry. Check it by running `./bin/check_sorted.py youslist.txt`.
- Do not add extra empty line.
- Make sure that `Rules.1blockpkg.json` is up to date when you add a filter for addresses.
  Use `./bin/generate_rules.py youslist.txt > Rules.1blockpkg.json` to update.
  You should install dependencies by running `pip install -r requirements.txt`.
  If you're using Python older than or equal to 2.6, than you should run `pip install -r requirements26.txt` too.
- After updating `Rules.1blockpkg.json`, update `Rules.1blockpkg` by running `./bin/minify_pkg.py`.
- To update `Rules.1blockpkg.json` with the content of `Rules.1blockpkg`, run `./bin/prettify_pkg.py`.
- Test `youslist.txt` and `Rules.1blockpkg.json` with `bin/test`.
- Build `Rules.1blockpkg.json` and `Rules.1blockpkg` from `youslist.txt` with `bin/release`.
