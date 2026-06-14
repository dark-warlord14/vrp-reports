# Security: OpenSearch description files can be loaded from file:// URLs

| Field | Value |
|-------|-------|
| **Issue ID** | [40080786](https://issues.chromium.org/issues/40080786) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Omnibox, UI>Browser>Search |
| **Reporter** | ja...@googlemail.com |
| **Assignee** | me...@chromium.org |
| **Created** | 2014-11-03 |
| **Bounty** | $500.00 |

## Description

Security: OpenSearch description files can be loaded from file:// URLs

**VULNERABILITY DETAILS**  

When a webpage uses <link rel="search" type="application/opensearchdescription+xml" href="{url}" ...> to point to an OpenSearch description file, the renderer will give the URI to the privileged browser process using a ChromeViewHostMsg\_PageHasOSDD message. SearchEngineTabHelper::OnPageHasOSDD will then download the XML file from the given URL and use it to configure a search engine, even if the webpage comes from an http origin and the URL points to the local filesystem.

I can think of some ways in which this might be usable for an attacker:

- If an attacker can cause secret information to be embedded in a file with an attacker-controlled structure, he might be able to create a search engine that, when used, transfers the secret to the attacker when the search engine is used for the first time. This seems pretty unlikely to me though.
- An attacker might be able to use this in order to track users more invasively: If he can place a search description file with a unique tracking identifier on a user's computer, e.g. by triggering a file download, he could later use the path to the file to add the search engine, giving him the unique tracking token the next time the user performs a search. This tracking token would persist across browser profiles.
- It might be possible to use this to detect the existence of files on the local filesystem using timing. (Or, depending on the size of the file, by detecting that the browser is suddenly gone - attempting to parse a 692MB file causes the browser to kill itself with a "mov BYTE PTR ds:0x0,0x0".) Maybe I'll try to find out whether this works in the following days.

**VERSION**  

Chrome Version: 38.0.2125.104 stable  

Operating System: Debian Jessie

**REPRODUCTION CASE**  

Put this into the webroot of a webserver:

<!DOCTYPE html>
<html>
<head>
<link rel="search" type="application/opensearchdescription+xml" href="file:///tmp/quark" title="quark" />
</head>
<body></body>
</html>

Then save something like this as /tmp/quark:

<?xml version="1.0"?>
<OpenSearchDescription xmlns="http://a9.com/-/spec/opensearch/1.1/">
<ShortName>foobarbaz</ShortName>
<Description>foo bar baz</Description>
<Url type="text/html" method="get" template="http://quark/search?q={searchTerms}"/>
</OpenSearchDescription>

Now navigate to the root of the webserver, then look at the search engine list in the settings. You should see a new entry with "foobarbaz" in the first column and [http://quark/search?q=%s](javascript:void(0);) in the third one.

## Attachments

- [loader.html](attachments/loader.html) (text/html, 3.4 KB)
- [start.html](attachments/start.html) (text/html, 1.2 KB)
- [server.js](attachments/server.js) (text/javascript, 2.4 KB)

## Timeline

### ja...@googlemail.com (2014-11-03)

The "kill the browser with a big file" thing could be used to bruteforce the user's name - try different values for $user in /home/$user/Downloads/bigfilename until the browser crashes, then you know that the attempt that caused a crash is correct.

### me...@chromium.org (2014-11-05)

Thanks for the report. Looks like there is no check for local files in SearchEngineTabHelper::OnPageHasOSDD. I'm marking this medium severity as it allows enumerating the file system. 

sky: Are you the right person for open search bugs?

### cl...@chromium.org (2014-11-05)

[Empty comment from Monorail migration]

### ja...@googlemail.com (2014-11-05)

Made a nicer PoC. :)

If you want to run it from my server, you'll have to add "37.221.195.125 dyryawtajek.thejh.net" to your hostsfile first - as far as I can tell, AUTODETECTED_PROVIDER only works on the main page of a domain or something like that, and I didn't want to put the PoC in the root of a domain that's listed in my provider's DNS server.

This is it: http://dyryawtajek.thejh.net:38145/start , login credentials are user:Rashefyigov1.
Some of the paths tested by default should exist on Linux boxes - if you use a different OS, you'll probably have to enter different ones. Note that files under 1MB probably can't be detected and that files that are a few hundred MB big will crash the browser. Folders also work though, as long as they have enough entries. (A few hundred entries seem to be sufficient, I haven't played around with what the lower limit is.)
Click "start", wait for it to finish (should take about a minute), and you should see a list of paths that were tested. Green ones probably exist on your system, gray ones probably don't (or the files/folders are too small).

This is how it works:
When a search provider is added via autodetect, the request is dropped if another request is already pending. Therefore, if a filesystem URL is specified as a search provider and an http URL is specified as search provider immediately afterwards, the http request will only happen if the filesystem request finished very quickly. This PoC uses that: For every path that was entered, five times, it loads the path as search provider description and loads a URL on the server as search provider description immediately afterwards. The server logs the requests and provides the list of requests that reached it to the client afterwards. If most of the requests failed, the file probably exists, if most of the requests got through, the file probably doesn't exist or is very small.

I've also attached the PoC's source.

### cl...@chromium.org (2014-11-09)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-11-10)

[Empty comment from Monorail migration]

### me...@chromium.org (2014-11-10)

sky: Can you please take a look or reassign as appropriate?

### mb...@chromium.org (2014-11-11)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-11-18)

sky@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-11-25)

sky@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-12-03)

sky@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-12-10)

sky@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-12-17)

sky@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-12-18)

sky@: Uh oh! This issue is still open and hasn't been updated in the last 44 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-12-19)

sky@: Uh oh! This issue is still open and hasn't been updated in the last 44 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### in...@chromium.org (2015-01-07)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-01-09)

sky@: Uh oh! This issue is still open and hasn't been updated in the last 66 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### dc...@chromium.org (2015-01-22)

CCing owners of components/search_engines and people who have contributed non-maintenance patches to it in hopes of getting some action on this bug.

### th...@chromium.org (2015-01-22)

meacer: Is all that's needed to check the schema (and origin?) of |ossd_url| in SearchEngineTabHelper::OnPageHasOSDD?

### me...@chromium.org (2015-01-22)

Hmm, I just looked at the code very briefly at the time and that was what looked interesting, but it's possible there is more to this bug than that check.

### pk...@chromium.org (2015-01-22)

Note that a page should probably be allowed to specify an OSDD from a different scheme or origin (e.g. http://static.foo.com/osdd.xml from https://search.foo.com/), but it probably shouldn't be able to specify a file: URL unless the referencing page itself is a local file.

### cl...@chromium.org (2015-02-12)

sky@: Uh oh! This issue is still open and hasn't been updated in the last 21 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### me...@chromium.org (2015-02-12)

Here is a patch to get this going: https://codereview.chromium.org/917313004/

Needs tests but I couldn't find any existing ones. 

### cl...@chromium.org (2015-02-20)

[Empty comment from Monorail migration]

### me...@chromium.org (2015-02-20)

jln: Any opinions about file:// urls referring to other file:// urls as search descriptors? (https://codereview.chromium.org/917313004/)

### bu...@chromium.org (2015-02-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/c4b8fd74e67dfb23ef150c6aa313cb506746f06f

commit c4b8fd74e67dfb23ef150c6aa313cb506746f06f
Author: meacer <meacer@chromium.org>
Date: Tue Feb 24 01:30:08 2015

Only accept HTTP and HTTPS urls for opensearch descriptor.

This CL prevents http: or https: urls from referring to file: urls as search descriptor xmls.
Allowing urls to refer to other urls with the same scheme has been considered (e.g. a file: url
referring to an OSDD xml from a file: url), but this currently doesn't work for file: urls
because of http://b/863583, so is not implemented here.

BUG=429838

Review URL: https://codereview.chromium.org/917313004

Cr-Commit-Position: refs/heads/master@{#317723}

[modify] http://crrev.com/c4b8fd74e67dfb23ef150c6aa313cb506746f06f/chrome/browser/ui/search_engines/search_engine_tab_helper.cc
[add] http://crrev.com/c4b8fd74e67dfb23ef150c6aa313cb506746f06f/chrome/browser/ui/search_engines/search_engine_tab_helper_browsertest.cc
[modify] http://crrev.com/c4b8fd74e67dfb23ef150c6aa313cb506746f06f/chrome/chrome_tests.gypi


### me...@chromium.org (2015-02-24)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-02-24)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### ti...@google.com (2015-02-26)

[Empty comment from Monorail migration]

### ti...@google.com (2015-03-16)

Merge Requested for M42.

### am...@google.com (2015-03-16)

Approved for M42 (branch: 2311)

### bu...@chromium.org (2015-03-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/d4e4806e013d34953dedee735d4b2d22b43afec3

commit d4e4806e013d34953dedee735d4b2d22b43afec3
Author: Alex Mineer <amineer@chromium.org>
Date: Mon Mar 23 16:22:59 2015

Only accept HTTP and HTTPS urls for opensearch descriptor.

This CL prevents http: or https: urls from referring to file: urls as search descriptor xmls.
Allowing urls to refer to other urls with the same scheme has been considered (e.g. a file: url
referring to an OSDD xml from a file: url), but this currently doesn't work for file: urls
because of http://b/863583, so is not implemented here.

BUG=429838

Review URL: https://codereview.chromium.org/917313004

(cherry picked from commit c4b8fd74e67dfb23ef150c6aa313cb506746f06f)

Cr-Original-Commit-Position: refs/heads/master@{#317723}
Cr-Commit-Position: refs/branch-heads/2311@{#310}
Cr-Branched-From: 09b7de5dd7254947cd4306de907274fa63373d48-refs/heads/master@{#317474}

[modify] http://crrev.com/d4e4806e013d34953dedee735d4b2d22b43afec3/chrome/browser/ui/search_engines/search_engine_tab_helper.cc
[add] http://crrev.com/d4e4806e013d34953dedee735d4b2d22b43afec3/chrome/browser/ui/search_engines/search_engine_tab_helper_browsertest.cc
[modify] http://crrev.com/d4e4806e013d34953dedee735d4b2d22b43afec3/chrome/chrome_tests.gypi


### ti...@google.com (2015-04-09)

[Empty comment from Monorail migration]

### ti...@google.com (2015-04-14)

Congrats Jann - $500 for your help here and another CVE to call your own.

### ti...@google.com (2015-05-06)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-06-02)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2015-06-25)

Processing via our e-payment system can take up to two weeks, but the reward should be on its way to you. Thanks again for your help!

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/429838?no_tracker_redirect=1

[Multiple monorail components: UI>Browser>Omnibox, UI>Browser>Search]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080786)*
