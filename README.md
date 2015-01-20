# YousList

Block filter for [Adblock Plus][] and [µBlock][].

[Adblock Plus]: https://adblockplus.org/
[µBlock]: https://github.com/gorhill/uBlock

## Usage

```
https://github.com/yous/YousList/raw/master/youslist.txt
```

### Adblock Plus

Install the browser plugin of Adblock Plus and add a subscription as 'YousList' with the above URL.

### µBlock

Install the browser plugin of µBlock and add a custom filter with the above URL.

## Testing

For the tests of your filter, make a temporary subscription served by your local machine by:

``` sh
ruby server.rb
```

Add a filter using `http://localhost:8000/youslist.txt`.

## Contributing

New issues and pull requests are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for further details.

## License

Content of the YousList is licensed under a [Creative Commons Attribution 4.0 International License](http://creativecommons.org/licenses/by/4.0/).
