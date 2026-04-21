# Security: non-interactive request forcing

| Field | Value |
|-------|-------|
| **Issue ID** | [40086171](https://issues.chromium.org/issues/40086171) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Cast |
| **Reporter** | [Deleted User] |
| **Assignee** | mf...@chromium.org |
| **Created** | 2016-12-07 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**

When a user starts the browser, it immediately sends a UDP multicast SSDP request to 239.255.255.250:1900. The purpose of this request is to gather info from other local network devices that Chrome could later use for screen casting.

The problem is that the effect of this functionality is that the browser asks the network to suggest a set of URLs that it should run HTTP GET requests on at startup. Then it runs the requests, all without any user interaction or awareness.

The HTTP connections persist cookies that come back in the responses. This could be used to force cookies on the user (and/or overwrite existing cookies).  

If a URL has the HTTP scheme, the browser will send, in the clear, persisted cookies not marked "secure" (for domains that are NOT in the HSTS preload list).  

This could be used to perform CSRF, as the victim user, against vulnerable sites (an attacker can specify a list of URLs that he would like the browser to visit).

Basically, this appears to be a LAN centered feature that does not properly limit what it will request, and it sends and sets too much data (e.g. cookies).  

A non-MITM attacker could use this to perform CSRF against a vulnerable site, without user interaction.  

A MITM attacker could use this to inspect cookies not marked secure, set/force/overwrite cookies, and all the other typical stuff available to a MITM attacker, but without requiring user initiated action, other than opening the browser.

When using incognito mode, the cookies used and set by this function are the cookies of non-incognito mode.  

I did not expect that non-incognito mode persistent cookies could be changed while running in incognito mode. That seems like a violation.

Even if a user has never navigated to a site, persistent cookies can be set for when they do actually navigate there.  

Even if a user uses incognito mode and types in https (or uses https bookmarks), a non-HSTS site is vulnerable to cookie forcing/injection with this enabled.

Disabling chrome://flags/#media-router stops this functionality from running at startup. Perhaps make this disabled by default until it's worked out (it is enabled by default right now).  

However, this same thing runs when "Cast..." is selected from the menu.

Here's the related code:  

<https://cs.chromium.org/chromium/src/chrome/browser/extensions/api/dial/dial_service.cc>

**VERSION**  

Chrome Version: 55.0.2883.75 (64-bit) stable  

Operating System: Ubuntu 16.04.1 LTS

**REPRODUCTION CASE**

The attached BadSSDP.java POC java program listens for such a multicast request and returns responses with URLs that it would like the browser to request.  

The attached poc.js is a small node.js HTTP server that sets cookies depending on the request received (a similarly configured local web server could be used instead for testing).

1. clear all cookies and close all google chrome processes
2. set example.com to resolve to 127.0.0.1 in /etc/hosts (this just makes testing easier. a real attacker could arpspoof to get MITM to be able to inspect, inject, modify etc...)
3. /opt/node-v7.2.1-linux-x64/bin/node ./poc.js &  
   
   4a) javac BadSSDP.java;  
   
   4b) java BadSSDP &
4. open chrome incognito window (packets #1-38 in attached packet capture)
5. wait a few seconds then close chrome incognito window (you actually don't have to wait long at all, but just to make sure you see what's going on...)
6. open chrome incognito window and notice that cookies are sent that were set automatically by step #5 (packets #39-76 in attached packet capture)
7. open new non-incognito window and navigate to <http://example.com:8080/> and notice that cookies are sent that were set automatically by step #5 (not included in the packet capture, just look at dev console etc...)

Note: While running this test, something that might trip you up are host-based firewall rules. If so, allow UDP port 1900 packets in and out. This functionality relies on that traffic being allowed for it to ever work, so the assumption must be that users allow that traffic already.

## Attachments

- [packets.pcap](attachments/packets.pcap) (application/octet-stream, 13.1 KB)
- [BadSSDP.java](attachments/BadSSDP.java) (text/plain, 1.8 KB)
- [poc.js](attachments/poc.js) (text/plain, 641 B)

## Timeline

### wr...@chromium.org (2016-12-09)

[Empty comment from Monorail migration]

### wr...@chromium.org (2016-12-09)

[Empty comment from Monorail migration]

### mf...@chromium.org (2016-12-09)

As an initial mitigation we should filter device description URL hosts to be RFC 1918 addresses.

Longer term, need to think about how to keep these requests independent from cookie store.


### el...@chromium.org (2016-12-09)

> how to keep these requests independent from cookie store.

Do we need to support cookies at all in this codepath? If not, can we do what IntranetRedirectDetector does?

    // We don't want these fetches to affect existing state in the profile.
    fetcher->SetLoadFlags(net::LOAD_DISABLE_CACHE |
                          net::LOAD_DO_NOT_SAVE_COOKIES |
                          net::LOAD_DO_NOT_SEND_COOKIES |
                          net::LOAD_DO_NOT_SEND_AUTH_DATA);

### sh...@chromium.org (2016-12-10)

[Empty comment from Monorail migration]

### mf...@chromium.org (2016-12-13)

No we don't need cookies.  To take advantage of the code path you suggest, we would need to plumb an extension API to call the IntranetRedirector, unless one already exists.


### el...@chromium.org (2016-12-13)

My proposal isn't that we should use the IntranetRedirector codepath directly. Instead, the question is whether we can, after the Dial API discovery phase obtains URLs, we fetch those discovered URLs using the Load Flags that suppress unwanted headers and caching behavior. 

### mf...@chromium.org (2016-12-13)

Yes, that makes complete sense.

### mb...@chromium.org (2016-12-15)

[Empty comment from Monorail migration]

[Monorail components: Internals>Cast]

### mf...@chromium.org (2016-12-21)

The issue pointed out by the original poster should be fixed in Chrome Canary running Media Router 5716.1220.0 or newer.  I am working on a more comprehensive fix, but it won't land for another few days.



### sh...@chromium.org (2016-12-22)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-01-03)

[Empty comment from Monorail migration]

### di...@chromium.org (2017-01-04)

Your change meets the bar and is auto-approved for M56 (branch: 2924)

### sh...@chromium.org (2017-01-09)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mf...@chromium.org (2017-01-09)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-01-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/90824416d3eeae5ec6013b250123df65e9d48032

commit 90824416d3eeae5ec6013b250123df65e9d48032
Author: mfoltz <mfoltz@chromium.org>
Date: Tue Jan 10 22:34:11 2017

Adds chrome.dial.fetchDeviceDecription API.

This API fetches the device description for a DIAL device, given a label for a device already discovered.

The request is configured to not send/receive cookies, ignore proxies, and ignore redirects.

Requests are retried with backoff on 5XX responses.

The response is validated in multiple ways:
- Valid Application-URL: header value
- Response body is a valid UTF-8 string
- Response body is <= 256kb

Additional validations are possible by following the DIAL spec closely at the risk of ignoring some devices.  See comments in device_description_fetcher.cc for details.

Note: The API function implementation is complicated by thread hopping.  See comments in dial_api.h for how this may be improved in the future.

BUG=671932
TESTED=Manually, unit tests, API test

Review-Url: https://codereview.chromium.org/2583853004
Cr-Commit-Position: refs/heads/master@{#442713}

[modify] https://crrev.com/90824416d3eeae5ec6013b250123df65e9d48032/chrome/browser/extensions/BUILD.gn
[add] https://crrev.com/90824416d3eeae5ec6013b250123df65e9d48032/chrome/browser/extensions/api/dial/device_description_fetcher.cc
[add] https://crrev.com/90824416d3eeae5ec6013b250123df65e9d48032/chrome/browser/extensions/api/dial/device_description_fetcher.h
[add] https://crrev.com/90824416d3eeae5ec6013b250123df65e9d48032/chrome/browser/extensions/api/dial/device_description_fetcher_unittest.cc
[modify] https://crrev.com/90824416d3eeae5ec6013b250123df65e9d48032/chrome/browser/extensions/api/dial/dial_api.cc
[modify] https://crrev.com/90824416d3eeae5ec6013b250123df65e9d48032/chrome/browser/extensions/api/dial/dial_api.h
[modify] https://crrev.com/90824416d3eeae5ec6013b250123df65e9d48032/chrome/browser/extensions/api/dial/dial_apitest.cc
[modify] https://crrev.com/90824416d3eeae5ec6013b250123df65e9d48032/chrome/browser/extensions/api/dial/dial_device_data.cc
[modify] https://crrev.com/90824416d3eeae5ec6013b250123df65e9d48032/chrome/browser/extensions/api/dial/dial_device_data.h
[modify] https://crrev.com/90824416d3eeae5ec6013b250123df65e9d48032/chrome/browser/extensions/api/dial/dial_registry.cc
[modify] https://crrev.com/90824416d3eeae5ec6013b250123df65e9d48032/chrome/browser/extensions/api/dial/dial_registry.h
[modify] https://crrev.com/90824416d3eeae5ec6013b250123df65e9d48032/chrome/common/extensions/api/dial.idl
[modify] https://crrev.com/90824416d3eeae5ec6013b250123df65e9d48032/chrome/test/BUILD.gn
[add] https://crrev.com/90824416d3eeae5ec6013b250123df65e9d48032/chrome/test/data/extensions/api_test/dial/experimental/fetch_device_description.html
[add] https://crrev.com/90824416d3eeae5ec6013b250123df65e9d48032/chrome/test/data/extensions/api_test/dial/experimental/fetch_device_description.js
[modify] https://crrev.com/90824416d3eeae5ec6013b250123df65e9d48032/extensions/browser/extension_function_histogram_value.h
[modify] https://crrev.com/90824416d3eeae5ec6013b250123df65e9d48032/tools/metrics/histograms/histograms.xml


### sh...@chromium.org (2017-01-12)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2017-01-12)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-12)

Congratulations! The panel decided to award $1,000 for this bug!

### [Deleted User] (2017-01-13)

Thanks! I signed up as a vendor a while back, do I need to do anything else?

### aw...@chromium.org (2017-01-13)

mike@ - in that case no, this will be included in the next payment run, so the money should be with you in a few weeks!

### aw...@chromium.org (2017-01-17)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-02-14)

[Empty comment from Monorail migration]

### [Deleted User] (2017-02-23)

This reward payment has been inprocess for over a month, is there something wrong? All my info is still the same. Thanks!

### aw...@chromium.org (2017-03-06)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-03-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-03-30)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@google.com (2017-08-11)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/671932?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086171)*
