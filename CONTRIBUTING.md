# Contributing

## Issue reporting

- Check that the issue has not already been reported.
- Check that the issue has not already been fixed in the latest code (`master`).

## Pull requests

- Make sure that every entry follows [Adblock Plus filter rules](https://adblockplus.org/en/filters).
- Update the [checksum](https://adblockplus.org/en/filters#special-comments). If you use Vim, you can use [adblock-filter.vim](https://github.com/mojako/adblock-filter.vim).
- Update the version with the format `yyyyMMdd`.
- Alphabetically order every entry.
- Do not add extra empty line.
- Make sure that `Rules.1blockpkg` is up to date when you add a filter for addresses. Use <http://my.1blocker.com> for editing.
- After updating `Rules.1blockpkg`, update `Rules.1blockpkg.json`, to make easy to see diff, by running `./bin/prettify_pkg.py`
