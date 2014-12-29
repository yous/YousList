# YousList

[Adblock Plus][] filter.

[Adblock Plus]: https://adblockplus.org/

## Usage

Install its browser plugin of Adblock Plus and add a subscription as 'YousList' with the url:

```
https://github.com/yous/YousList/raw/master/youslist.txt
```

## Testing

For the tests of your filter, make a temporary subscription served by your local machine by:

``` sh
ruby server.rb
```

Add a subscription using `http://localhost:8000/youslist.txt`.

## Contributing

New issues and pull requests are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for further details.

## License

Content of the YousList is licensed under a [Creative Commons Attribution 4.0 International License](http://creativecommons.org/licenses/by/4.0/).
