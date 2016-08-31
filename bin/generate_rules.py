#!/usr/bin/env python
import os
import sys
import fileinput
import json
import collections
import re
import uuid
import six

pwd = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(pwd)

class FilterParser:
    DOMAIN_PREFIX = '^(?:[^:/?#]+:)?(?://(?:[^/?#]*\\.)?)?'

    def __init__(self, name='Generated Package', basepkg=None):
        self.pkg = collections.OrderedDict()
        self.id_dict = {}
        self.rules = []
        if basepkg:
            try:
                f = open(basepkg)
                obj = json.load(f, object_pairs_hook=collections.OrderedDict)
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
        for line in fileinput.input():
            self._parse_rule(line)
        self.pkg['rules'] = self.rules
        if six.PY2:
            sys.stdout.write(
                json.dumps([self.pkg], ensure_ascii=False,
                           indent=4, separators=(',', ': ')) \
                .encode('utf-8'))
        else:
            sys.stdout.write(
                json.dumps([self.pkg], ensure_ascii=False,
                           indent=4, separators=(',', ': ')))

    def _parse_rule(self, line):
        if six.PY2:
            line = line.strip().decode('utf-8')
        else:
            line = line.strip()
        if not line or line.startswith('!') or re.match('\[Adblock.*\]', line):
            return
        if '##' in line:
            # Element hiding rule
            self._parse_hiding_rule(line)
        else:
            # Blocking rule
            self._parse_blocking_rule(line)

    def _parse_hiding_rule(self, line):
        rule = collections.OrderedDict()
        name = line
        if name in self.id_dict:
            rule['id'] = self.id_dict[name]
        else:
            rule['id'] = str(uuid.uuid4())
        rule['name'] = name

        urls, css = line.split('##', 2)
        if ',' in urls:
            url_list = urls.split(',')
            for url in url_list:
                self._parse_hiding_rule(url + '##' + css)
            return
        url = urls
        trigger = collections.OrderedDict()
        if url:
            trigger['url-filter'] = self.DOMAIN_PREFIX + url.replace('.', '\\.')
        else:
            trigger['url-filter'] = '.*'
        trigger['load-type'] = []

        action = collections.OrderedDict()
        action['type'] = 'css-display-none'
        action['selector'] = css

        content = collections.OrderedDict()
        content['trigger'] = trigger
        content['action'] = action
        rule['content'] = content
        self.rules.append(rule)

    def _parse_blocking_rule(self, line):
        rule = collections.OrderedDict()
        splits = line.split('$', 2)
        if len(splits) < 2:
            splits.append('')
        url, options = splits
        name = url.lstrip('||').rstrip('^')
        url = url.rstrip('^').strip('*')
        if options:
            name += '$' + options
        if name in self.id_dict:
            rule['id'] = self.id_dict[name]
        else:
            rule['id'] = str(uuid.uuid4())
        rule['name'] = name

        trigger = {}
        if url.startswith('||'):
            trigger['url-filter'] = self.DOMAIN_PREFIX + url.lstrip('||') \
                .replace('.', '\\.') \
                .replace('*', '.*') \
                .replace('?', '\\?')
        else:
            trigger['url-filter'] = url \
                .replace('.', '\\.') \
                .replace('*', '.*') \
                .replace('?', '\\?')
        trigger['load-type'] = []

        opt_dict = self._parse_options(options)
        trigger.update(opt_dict)
        trigger_ordered_keys = ['url-filter',
                                'resource-type',
                                'load-type',
                                'if-domain',
                                'unless-domain']
        trigger_ordered_dict = collections.OrderedDict()
        for key in trigger_ordered_keys:
            if key in trigger:
                trigger_ordered_dict[key] = trigger[key]

        action = collections.OrderedDict()
        action['type'] = 'block'

        content = collections.OrderedDict()
        content['trigger'] = trigger_ordered_dict
        content['action'] = action
        rule['content'] = content
        self.rules.append(rule)

    def _parse_options(self, options):
        opt_dict = {}
        if options:
            options = options.split(',')
        else:
            options = []
        for option in options:
            splits = option.split('=', 2)
            if len(splits) < 2:
                splits.append('')
            opt_key, opt_val = splits
            if opt_key == 'domain':
                domains = opt_val.split('|')
                if_domain = []
                unless_domain = []
                for domain in domains:
                    if domain.startswith('~'):
                        unless_domain.append(domain.lstrip('~'))
                    else:
                        if_domain.append(domain)
                if len(if_domain) and len(unless_domain):
                    raise ValueError('Cannot handle this domains: ' + opt_val)
                elif len(if_domain):
                    opt_dict['if-domain'] = if_domain
                elif len(unless_domain):
                    opt_dict['unless-domain'] = unless_domain
            elif opt_key == 'script':
                opt_dict['resource-type'] = ['script']
            else:
                raise ValueError('Cannot handle this option: ' + opt_key)
        return opt_dict

orig_pkg = os.path.join(root, 'Rules.1blockpkg')
parser = FilterParser(basepkg=orig_pkg)
parser.parse()
