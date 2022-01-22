# -*- coding=utf-8 -*-
import codecs
import io
import json
import os
import re
import sys
import uuid
from collections import OrderedDict

pwd = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(pwd)


class FilterParser:
    # For scheme, see Appendix A of http://www.ietf.org/rfc/rfc2396.txt
    # See https://webkit.org/blog/4062/targeting-domains-with-content-blockers/
    DOMAIN_PREFIX = '^[^:]+://+([^:/]+\\.)?'
    TRIGGER_ORDERED_KEYS = ['url-filter',
                            'url-filter-is-case-sensitive',
                            'resource-type',
                            'load-type',
                            'if-domain',
                            'unless-domain']

    def __init__(self, name='Generated Package', basepkg=None):
        self.pkg = OrderedDict()
        self.id_dict = {}
        self.rules = []
        if basepkg:
            try:
                # For cross-platform development, expecially for Windows
                f = io.open(basepkg)
                obj = json.load(f, object_pairs_hook=OrderedDict)
                orig_pkg = obj[0]
                self.pkg['id'] = orig_pkg['id']
                self.pkg['name'] = orig_pkg['name']
                for rule in orig_pkg['rules']:
                    self.id_dict[rule['name']] = rule['id']
            finally:
                f.close()
        if 'id' not in self.pkg:
            self.pkg['id'] = str(uuid.uuid4())
        if 'name' not in self.pkg:
            self.pkg['name'] = name

    def parse(self):
        # For the purpose of a cross-platform expecially for Windows
        # Windows consoles does not use 'utf-8' by default.
        with io.open(sys.argv[1], encoding='utf-8') as f:
            for line in f.readlines():
                self._parse_rule(line)
        self.pkg['rules'] = self.rules
        json_string = json.dumps([self.pkg], ensure_ascii=False,
                                 indent=4, separators=(',', ': '))
        self._print(json_string)

    def _print(self, line):
        # Objects:
        # 1. Use UTF-8 as default in Python 2 and Python 3
        # 2. Support cross-plarform script
        #
        # Note that sys.stdout.encoding is involved with console you use, not
        # with Python interpreter. The default encoding called code page of
        # Windows terminal is NOT set up for utf-8. Please refer to this page:
        # https://stackoverflow.com/a/24104423
        #
        # In case this script runs in Python 3 on Linux.
        if sys.stdout.encoding == 'UTF-8':
            sys.stdout.write(line)

        # Otherwise,
        else:
            # Python 3
            if sys.version_info.major >= 3:
                sys.stdout.buffer.write(bytes(line.encode('utf-8')))

            # Python 2
            else:
                # On Windows, the output ends with CRLF.
                if sys.platform == "win32":
                    import msvcrt
                    msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)
                codecs.getwriter('utf-8')(sys.stdout).write(line)

    def _parse_rule(self, line):
        line = line.strip()
        if (not line or line.startswith('!') or
                re.match(r'\[Adblock.*\]', line)):
            return
        if '##' in line:
            # Element hiding rule
            self._parse_hiding_rule(line)
        elif line.startswith('#@#'):
            # Skip global element hiding exception rule
            return
        elif '#@#' in line:
            # Element hiding exception rule
            self._parse_hiding_exception_rule(line)
        elif '#?#' in line:
            # Adblock Plus specific extended CSS selectors
            pass
        elif line.startswith('@@'):
            # Exception rule
            self._parse_exception_rule(line)
        else:
            # Blocking rule
            self._parse_blocking_rule(line)

    def _parse_hiding_rule(self, line):
        # Handle rule with multiple URLs
        urls, css = line.split('##', 1)
        if ',' in urls:
            url_list = urls.split(',')
            for url in url_list:
                self._parse_hiding_rule(url + '##' + css)
            return
        url = urls

        rule = OrderedDict()
        if url:
            if url.startswith('~'):
                name = '##' + css
            else:
                name = url + '##'
        else:
            name = line
        rule['id'] = self._get_rule_id(name)
        rule['name'] = name

        if url.startswith('~'):
            # Element hiding exception rule
            url = url[1:]
            for prev_rule in self.rules:
                content = prev_rule['content']
                trigger = content['trigger']
                action = content['action']

                url_filter = trigger['url-filter']
                if_domain = trigger.get('if-domain')
                unless_domain = trigger.get('unless-domain')

                if (action['type'] == 'css-display-none' and
                        action['selector'] == css and
                        url_filter == '.*' and
                        not if_domain):
                    if unless_domain is None:
                        unless_domain = ['*' + url]
                    else:
                        unless_domain.append('*' + url)
                    trigger['unless-domain'] = unless_domain
                    return

            # There is no global hiding rule
            trigger = OrderedDict()
            trigger['url-filter'] = '.*'
            trigger['unless-domain'] = ['*' + url]

            action = OrderedDict()
            action['type'] = 'css-display-none'
            action['selector'] = css

            content = OrderedDict()
            content['trigger'] = trigger
            content['action'] = action
            rule['content'] = content
            self.rules.append(rule)
            return

        trigger = OrderedDict()
        if url:
            trigger['url-filter'] = \
                self.DOMAIN_PREFIX + url.replace('.', '\\.')

            for prev_rule in reversed(self.rules):
                prev_content = prev_rule['content']
                prev_trigger = prev_content['trigger']
                prev_action = prev_content['action']
                prev_url_filter = prev_trigger['url-filter']

                if (prev_action['type'] == 'css-display-none' and
                        prev_url_filter == trigger['url-filter']):
                    prev_action['selector'] += ',' + css
                    return
        else:
            trigger['url-filter'] = '.*'

        action = OrderedDict()
        action['type'] = 'css-display-none'
        action['selector'] = css

        content = OrderedDict()
        content['trigger'] = trigger
        content['action'] = action
        rule['content'] = content
        self.rules.append(rule)

    def _parse_hiding_exception_rule(self, line):
        # Handle rule with multiple URLs
        urls, css = line.split('#@#', 1)
        if ',' in urls:
            url_list = urls.split(',')
            for url in url_list:
                self._parse_hiding_exception_rule(url + '#@#' + css)
            return
        url = urls

        if url.startswith('~'):
            # Element hiding exception rule
            raise Exception('Cannot handle this rule: ' + line)
        for rule in self.rules:
            content = rule['content']
            trigger = content['trigger']
            action = content['action']

            url_filter = trigger['url-filter']
            if_domain = trigger.get('if-domain')
            unless_domain = trigger.get('unless-domain')

            if (action['type'] == 'css-display-none' and
                    action['selector'] == css and
                    url_filter == '.*' and
                    not if_domain):
                if unless_domain is None:
                    unless_domain = ['*' + url]
                else:
                    unless_domain.append('*' + url)
                trigger['unless-domain'] = unless_domain
                return
        raise Exception('Cannot handle this rule: ' + line)

    def _parse_exception_rule(self, line):
        rule = self._parse_url_filter(line[2:])
        name = '@@' + rule['name']
        rule['id'] = self._get_rule_id(name)
        rule['name'] = name
        rule['content']['action']['type'] = 'ignore-previous-rules'
        self.rules.append(rule)

    def _parse_blocking_rule(self, line):
        rule = self._parse_url_filter(line)
        name = rule['name']
        rule['id'] = self._get_rule_id(name)
        rule['content']['action']['type'] = 'block'
        self.rules.append(rule)

    def _parse_url_filter(self, line):
        """rule['id'], rule['content']['action']['type'] should be set."""
        rule = OrderedDict()
        rule['id'] = None
        trigger = {}

        splits = line.rsplit('$', 1)
        if len(splits) < 2:
            splits.append('')
        url, options = splits
        if line.startswith('/'):
            # Regular expression blocking rule
            regex = url
            if not regex.endswith('/'):
                raise Exception('Cannot handle this rule: ' + line)
            regex = regex[1:-1]
            regex = re.sub(r'\\/', '/', regex)

            name = '/'
            if regex.startswith(self.DOMAIN_PREFIX):
                name += regex[len(self.DOMAIN_PREFIX):]
            else:
                name += regex
            name += '/'
            if options:
                name += '$' + options
            rule['name'] = name

            trigger['url-filter'] = regex
        else:
            # General blocking rule
            name = self._strip_url(url)
            url = url.rstrip('^').strip('*')
            if options:
                name += '$' + options
            rule['name'] = name

            # * Adblock Plus' filterToRegExp:
            #   https://github.com/adblockplus/adblockpluscore/blob/master/lib/common.js
            # * uBlock Origin's restrFromGenericPattern:
            #   https://github.com/gorhill/uBlock/blob/master/src/js/static-net-filtering.js
            url_regex = url
            for search, replace in [[r'\*+', '*'],
                                    [r'[.+?${}()|[\]\\]', r'\\\g<0>'],
                                    [r'\*', '.*'],
                                    [r'^\\\|\\\|', self.DOMAIN_PREFIX],
                                    [r'^\\\|', '^'],
                                    [r'\\\|$', '$']]:
                url_regex = re.sub(search, replace, url_regex)
            trigger['url-filter'] = url_regex

        trigger['url-filter-is-case-sensitive'] = False

        opt_dict = self._parse_options(options)
        trigger.update(opt_dict)
        trigger_ordered_dict = OrderedDict()
        for key in self.TRIGGER_ORDERED_KEYS:
            if key in trigger:
                trigger_ordered_dict[key] = trigger[key]

        action = OrderedDict()
        action['type'] = None

        content = OrderedDict()
        content['trigger'] = trigger_ordered_dict
        content['action'] = action
        rule['content'] = content
        return rule

    def _parse_options(self, options):
        opt_dict = {}
        if options:
            options = options.split(',')
        else:
            options = []
        for option in options:
            splits = option.split('=', 1)
            if len(splits) < 2:
                splits.append('')
            opt_key, opt_val = splits
            if opt_key == 'domain':
                domains = opt_val.split('|')
                if_domain = []
                unless_domain = []
                for domain in domains:
                    if domain.startswith('~'):
                        unless_domain.append('*' + domain.lstrip('~'))
                    else:
                        if_domain.append('*' + domain)
                if len(if_domain) and len(unless_domain):
                    raise Exception('Cannot handle these domains: ' + opt_val)
                elif len(if_domain):
                    opt_dict['if-domain'] = if_domain
                elif len(unless_domain):
                    opt_dict['unless-domain'] = unless_domain
            elif opt_key == 'image' or opt_key == 'script':
                if 'resource-type' not in opt_dict:
                    opt_dict['resource-type'] = []
                opt_dict['resource-type'].append(opt_key)
            elif opt_key == 'third-party':
                opt_dict['load-type'] = ['third-party']
            elif opt_key == 'match-case':
                opt_dict['url-filter-is-case-sensitive'] = True
            else:
                raise Exception('Cannot handle this option: ' + opt_key)
        return opt_dict

    def _get_rule_id(self, name):
        if name in self.id_dict:
            return self.id_dict[name]
        else:
            return str(uuid.uuid4())

    def _strip_url(self, url):
        result = url.rstrip('^')
        if result.startswith('||'):
            result = result[2:]
        elif result.startswith('|'):
            result = result[1:]
        return result


orig_pkg = os.path.join(root, 'Rules.1blockpkg')
parser = FilterParser(basepkg=orig_pkg)
parser.parse()
