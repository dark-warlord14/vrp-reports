# Pinned TLS public keys (HPKP) evicted after clearing cache

| Field | Value |
|-------|-------|
| **Issue ID** | [40084092](https://issues.chromium.org/issues/40084092) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Internals>Network>SSL, Privacy |
| **Platforms** | Mac |
| **CVE IDs** | CVE-2016-1694 |
| **Reporter** | ry...@cyph.com |
| **Assignee** | es...@chromium.org |
| **Created** | 2016-04-14 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36

Steps to reproduce the problem:
1. Open a URL with a valid Public-Key-Pins header (I tested with https://cyph.im and https://github.com).

2. Confirm the browser's success of processing the header via chrome://net-internals/#hsts > "Query domain".

3. Open chrome://settings/clearBrowserData clear any arbitrary subset of items (e.g. just "Passwords", doesn't matter).

4. Re-run the query at chrome://net-internals/#hsts.

What is the expected behavior?
There should be no change from the output of step #2.

What went wrong?
Pinned key hashes (and more broadly, all records prefixed with "dynamic_") no longer exist.

May not necessarily be considered a hair-on-fire bug given the user action required to trigger it, but it almost entirely destroys the benefit of HPKP for users like myself who find themselves frequently wiping the browser cache for development/testing/debugging purposes, and it could very easily be leveraged against a user via social engineering as part of a larger targeted attack.

Did this work before? Yes See additional comments

Chrome version: 50.0.2661.75  Channel: stable
OS Version: OS X 10.11.4
Flash Version: Shockwave Flash 21.0 r0

So, I was just able to reproduce this in various versions of Chrome between 38 (the earliest with HPKP support) and 50 (current stable), both locally and in BrowserStack, which would suggest that it is not actually a regression.

However, this definitely was not reproducible a few months ago. I've confirmed with a colleague to verify that I'm not insane for insisting this to indeed be the case, as we had each (at different points in time last year / early this year) independently expended a memorable amount of effort attempting to figure out how to delete pinned TLS keys after clearing the cache failed to do so, both ultimately landing on chrome://net-internals/#hsts > "Delete domain" as the correct solution.

I can only assume that the vulnerable code is wrapped in a statement similar to if (std::time(nullptr) > 1456790400) { ... }.

## Attachments

- [Screen Shot 2016-04-15 at 11.59.52 AM.png](attachments/Screen Shot 2016-04-15 at 11.59.52 AM.png) (image/png, 107.3 KB)

## Timeline

### ry...@cyph.com (2016-04-14)

Actually, re: "Did this work before?", upon investigation I now have verifiable evidence this is in fact a recent regression.

The details aren't important so I won't discuss them here (feel free to email me for an out-of-band explanation), but I have documentation from September of last year which verifies that either 1) the behaviour observed here was not present at that time, or 2) a second colleague of mine is a pathological liar.

### ts...@chromium.org (2016-04-14)

agl@, please re-assign as appropriate.

### es...@chromium.org (2016-04-14)

This seems to have been the case for approximately forever (2011). It looks like the behavior was introduced in https://codereview.chromium.org/7717023/, possibly by accident. The commit message on that CL makes it sound like TransportSecurityState is only supposed to be cleared on REMOVE_CACHE, but the actual code change (https://codereview.chromium.org/7717023/diff/7003/chrome/browser/browsing_data_remover.cc) always clears TransportSecurityState regardless of whether REMOVE_CACHE is set. Maybe it was intentional, or maybe it was just a mistake lining up the curly braces. (Or maybe I'm misreading it.)

+mkwst: can you ask past-Mike whether or not he intended to always clear the TransportSecurityState state in that CL?

[Monorail components: Internals>Network>SSL Privacy]

### ry...@cyph.com (2016-04-15)

Hm, that's interesting. From what you saw, does it seem like there could be any conditional logic that could be producing the inconsistent results I've seen?

Also, I forgot to mention when reporting, Bryant Zadegan (bryant@zadegan.net) should be included here as the secondary reporter.

### mk...@chromium.org (2016-04-15)

Past-me has no idea whether the change was correct. Present-me doesn't have any idea either. :)

I wouldn't be sad about moving HSTS/PKP to `REMOVE_COOKIE` rather than `REMOVE_CACHE`. I'm not sure one makes more sense than the other, really, but I suppose that folks clear cache more often than cookies. *shrug*

### es...@chromium.org (2016-04-15)

Mike -- just to clarify, right now it executes unconditionally (even if neither REMOVE_COOKIE nor REMOVE_CACHE is set). So I think putting it under either one would be fine, but having it be unconditional probably doesn't make sense; it probably shouldn't get cleared if the user only selects "Passwords", for example.

### mk...@chromium.org (2016-04-15)

Ah. I missed that caveat. Yes. Both past-me and present-me agree with present-you that clearing it unconditionally is a bad idea.

### br...@zadegan.net (2016-04-15)

The interim best fit sounds like "Cookies and other site and plugin data" (Guessing this is what 'REMOVE_COOKIE' refers to), but I'd be inclined to think a separate checkbox for non-preloaded HSTS, HPKP, and other security data down the road would be the right way to go here much the way there's a separate option for content licenses.

Quick, language-crude mockup attached.

### es...@chromium.org (2016-04-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-05-02)

estark: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### es...@chromium.org (2016-05-02)

Submitted CL for review: https://codereview.chromium.org/1941073002/

### bu...@chromium.org (2016-05-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/c686e3083ac8b46b2b8ce6c036554bf05a7ed9ec

commit c686e3083ac8b46b2b8ce6c036554bf05a7ed9ec
Author: estark <estark@chromium.org>
Date: Tue May 03 16:16:10 2016

Clear network state only when REMOVE_CACHE is set, not unconditionally

Previously, network state like HSTS data was cleared whenever
BrowsingDataRemover::Remove() was called. Some archaeology
(https://codereview.chromium.org/7717023/) reveals that the original
intention was to clear this state when REMOVE_CACHE was set, but due to
a curly brace mishap, we've been clearing it over-aggressively for
years.

When I changed this behavior to remove network state only when
REMOVE_CACHE is set, it revealed that a number of tests are relying on
state being asynchronously cleared. This is no longer the case, as for
example when only REMOVE_DOWNLOADS is set. This CL fixes that by calling
NotifyIfDone() at the end of RemoveImpl(), to catch cases where no state
is being wiped asynchronously. This is a little weird since download
removal does appear to be async -- but it matches the documentation of
BrowsingDataRemover::Observer, which says that the observer fires when
"keywords have been deleted, cache cleared and all other tasks
scheduled".

BUG=603682

Review-Url: https://codereview.chromium.org/1941073002
Cr-Commit-Position: refs/heads/master@{#391248}

[modify] https://crrev.com/c686e3083ac8b46b2b8ce6c036554bf05a7ed9ec/chrome/browser/browsing_data/browsing_data_remover.cc
[modify] https://crrev.com/c686e3083ac8b46b2b8ce6c036554bf05a7ed9ec/chrome/browser/browsing_data/browsing_data_remover_browsertest.cc


### es...@chromium.org (2016-05-03)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-05-03)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### ti...@google.com (2016-05-09)

[Empty comment from Monorail migration]

### ti...@google.com (2016-05-09)

Your change meets the bar and is auto-approved for M51 (branch: 2704)

### bu...@chromium.org (2016-05-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/6ea2ef944984fc750bd1677955bb099a5d5ffeea

commit 6ea2ef944984fc750bd1677955bb099a5d5ffeea
Author: Emily Stark <estark@google.com>
Date: Tue May 10 05:48:01 2016

Clear network state only when REMOVE_CACHE is set, not unconditionally

Previously, network state like HSTS data was cleared whenever
BrowsingDataRemover::Remove() was called. Some archaeology
(https://codereview.chromium.org/7717023/) reveals that the original
intention was to clear this state when REMOVE_CACHE was set, but due to
a curly brace mishap, we've been clearing it over-aggressively for
years.

When I changed this behavior to remove network state only when
REMOVE_CACHE is set, it revealed that a number of tests are relying on
state being asynchronously cleared. This is no longer the case, as for
example when only REMOVE_DOWNLOADS is set. This CL fixes that by calling
NotifyIfDone() at the end of RemoveImpl(), to catch cases where no state
is being wiped asynchronously. This is a little weird since download
removal does appear to be async -- but it matches the documentation of
BrowsingDataRemover::Observer, which says that the observer fires when
"keywords have been deleted, cache cleared and all other tasks
scheduled".

BUG=603682

Review-Url: https://codereview.chromium.org/1941073002
Cr-Commit-Position: refs/heads/master@{#391248}
(cherry picked from commit c686e3083ac8b46b2b8ce6c036554bf05a7ed9ec)

Review URL: https://codereview.chromium.org/1966453003 .

Cr-Commit-Position: refs/branch-heads/2704@{#464}
Cr-Branched-From: 6e53600def8f60d8c632fadc70d7c1939ccea347-refs/heads/master@{#386251}

[modify] https://crrev.com/6ea2ef944984fc750bd1677955bb099a5d5ffeea/chrome/browser/browsing_data/browsing_data_remover.cc
[modify] https://crrev.com/6ea2ef944984fc750bd1677955bb099a5d5ffeea/chrome/browser/browsing_data/browsing_data_remover_browsertest.cc


### ti...@google.com (2016-05-24)

[Empty comment from Monorail migration]

### ti...@google.com (2016-05-25)

The severity is incorrect here - this should be a low severity issue. Updating labels. This bus is currently at the reward panel.

### ti...@google.com (2016-05-26)

Our reward panel decided to award you $500 for reporting this issue to us. Congrats!

The CVE-ID is CVE-2016-1694 and it's referenced here: https://googlechromereleases.blogspot.com/2016/05/stable-channel-update_25.html

Note that we won't make the details of this issue public until most users are patched (usually ~2 weeks from today).

Ryan - let me know if you want me to pay you using your already registered details.

Thanks again!

### ry...@cyph.com (2016-05-26)

Thanks Tim! Yep, my current registered details would be the best way to send the money. Also, would you be able to list Bryant Zadegan as the secondary reporter in that blog post?

### ti...@google.com (2016-05-26)

Done and done: https://googlechromereleases.blogspot.com/2016/05/stable-channel-update_25.html

### ry...@cyph.com (2016-05-26)

Great, thanks!

### ti...@google.com (2016-06-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-08-10)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### yu...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-06)

This issue was migrated from crbug.com/chromium/603682?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Internals>Network>SSL, Privacy]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084092)*
