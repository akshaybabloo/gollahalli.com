---
title: "Retrieving Dns Records Using Python"
date: 2016-09-16T11:34:26+12:00
draft: false
categories: ["Tutorial"]
tags: ["Python"]
description: "Retrieving DNS records with Python 3."
relImage: ""
ads: true
author:
  prefix: "Mr."
  firstName: "Akshay Raj"
  lastName: "Gollahalli"
  honorarySuffix: "MCIS (FCH)"
  jobTitle: "Research Assistant"
  email: "akshay@gollahalli.com"
  addressCity: "Auckland"
  addressCountry: "New Zealand"
sitemap:
  priority: 0.8
  changeFreq: monthly
---

You can retrieve DNS records using `dnspython` package. You can install the package using `pip install dnspython`.

Gist can be found at [https://gist.github.com/akshaybabloo/2a1df455e7643926739e934e910cbf2e](https://gist.github.com/akshaybabloo/2a1df455e7643926739e934e910cbf2e)

The problem with this package is that you cannot retrieve all the records at a time so a quick and dirty alternative is to put them in `for` loop. Few record names in this list (`ids`) raise an exception, for example `ANY`, this is because there is no DNS record called `ANY`.

<!--adsense-->

## Things to know

1.  List of [DNS records](https://en.wikipedia.org/wiki/List_of_DNS_record_types)
2.  `dnspython` [docs](http://www.dnspython.org/docs/1.14.0/)

```python
#!/usr/bin/env python
# -*- coding utf-8 -*-
#
# Copyright 2016 Akshay Raj Gollahalli

import dns.resolver


def get_records(domain):
    """
    Get all the records associated to domain parameter.
    :param domain:
    :return:
    """
    ids = [
        'NONE',
        'A',
        'NS',
        'MD',
        'MF',
        'CNAME',
        'SOA',
        'MB',
        'MG',
        'MR',
        'NULL',
        'WKS',
        'PTR',
        'HINFO',
        'MINFO',
        'MX',
        'TXT',
        'RP',
        'AFSDB',
        'X25',
        'ISDN',
        'RT',
        'NSAP',
        'NSAP-PTR',
        'SIG',
        'KEY',
        'PX',
        'GPOS',
        'AAAA',
        'LOC',
        'NXT',
        'SRV',
        'NAPTR',
        'KX',
        'CERT',
        'A6',
        'DNAME',
        'OPT',
        'APL',
        'DS',
        'SSHFP',
        'IPSECKEY',
        'RRSIG',
        'NSEC',
        'DNSKEY',
        'DHCID',
        'NSEC3',
        'NSEC3PARAM',
        'TLSA',
        'HIP',
        'CDS',
        'CDNSKEY',
        'CSYNC',
        'SPF',
        'UNSPEC',
        'EUI48',
        'EUI64',
        'TKEY',
        'TSIG',
        'IXFR',
        'AXFR',
        'MAILB',
        'MAILA',
        'ANY',
        'URI',
        'CAA',
        'TA',
        'DLV',
    ]

    for a in ids:
        try:
            answers = dns.resolver.query(domain, a)
            for rdata in answers:
                print(a, ':', rdata.to_text())

        except Exception as e:
            print(e)  # or pass

if __name__ == '__main__':
    get_records('google.com')
```
