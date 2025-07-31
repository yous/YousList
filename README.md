# YousList

[![CI](https://github.com/yous/YousList/actions/workflows/ci.yml/badge.svg)](https://github.com/yous/YousList/actions/workflows/ci.yml)

Block filter for advertisements, mainly on Korean sites. This works with
[Adblock Plus][], [uBlock Origin][], [1Blocker][], [AdAway][], and [AdGuard][].

[Adblock Plus]: https://adblockplus.org/
[uBlock Origin]: https://github.com/gorhill/uBlock
[1Blocker]: https://1blocker.com/
[AdAway]: https://github.com/AdAway/AdAway
[AdGuard]: https://adguard.com/

## Usage

```
https://cdn.jsdelivr.net/gh/yous/YousList@latest/youslist.txt
```

### Adblock Plus ([Subscribe](https://subscribe.adblockplus.org/?location=https://cdn.jsdelivr.net/gh/yous/YousList@latest/youslist.txt&title=YousList))

Install the browser plugin of Adblock Plus and add a subscription as 'YousList' with the above URL.

### uBlock Origin ([Subscribe](https://subscribe.adblockplus.org/?location=https://cdn.jsdelivr.net/gh/yous/YousList@latest/youslist.txt&title=YousList))

Install the browser plugin of uBlock Origin and enable 'KOR: YousList' by checking it.

### 1Blocker

Go to [the latest release page](https://github.com/yous/YousList/releases/latest)
and click the "Download Rules.1blockpkg" link. Select 1Blocker from the "Open
In" menu. To update to the newer version, you have to remove previous rules and
then import the new rules.

### AdAway

Add the following URL as a host source.

```
https://cdn.jsdelivr.net/gh/yous/YousList@latest/hosts.txt
```

### AdGuard ([Subscribe](https://subscribe.adblockplus.org/?location=https://cdn.jsdelivr.net/gh/yous/YousList@latest/youslist.txt&title=YousList))

Enable YousList on the filter list.

The following is the DNS filter:

```
https://cdn.jsdelivr.net/gh/adguardteam/HostlistsRegistry@main/assets/filter_15.txt
```

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
