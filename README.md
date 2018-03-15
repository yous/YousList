# YousList

[![Build Status](https://travis-ci.org/yous/YousList.svg?branch=master)](https://travis-ci.org/yous/YousList)

Block filter for [Adblock Plus][], [uBlock Origin][], [uBlock][], [1Blocker][],
[AdAway][], and [AdGuard][].

[Adblock Plus]: https://adblockplus.org/
[uBlock Origin]: https://github.com/gorhill/uBlock
[uBlock]: https://github.com/chrisaljoudi/uBlock
[1Blocker]: http://1blocker.com/
[AdAway]: https://github.com/Free-Software-for-Android/AdAway
[AdGuard]: https://adguard.com/

## Usage

```
https://github.com/yous/YousList/raw/master/youslist.txt
```

### Adblock Plus

Install the browser plugin of Adblock Plus and add a subscription as 'YousList' with the above URL.

### uBlock Origin

Install the browser plugin of uBlock Origin and enable 'KOR: YousList' by checking it.

### uBlock

Install the browser plugin of uBlock and add a custom filter with the above URL.

### 1Blocker

Open [Rules.1blockpkg (v20180314)](https://cdn.rawgit.com/yous/YousList/v20180314/Rules.1blockpkg)
and select 1Blocker from the "Open In" menu. To update to the latest version,
you have to remove previous rules and then import the new rules.

### AdAway

Add the following URL as a host source.

```
https://github.com/yous/YousList/raw/master/hosts.txt
```

### AdGuard

Enable YousList on the filter list.

## Testing

For the tests of your filter, make a temporary subscription served by your local machine by:

``` sh
ruby -run -ehttpd . -p8000
```

Add a filter using `http://localhost:8000/youslist.txt`.

## Contributing

New issues and pull requests are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for further details.

## License

Content of the YousList is licensed under a [Creative Commons Attribution 4.0 International License](http://creativecommons.org/licenses/by/4.0/).
