# Security: libexpat buffer-overflow seems to affect latest version of chromium on Linux x86_64

| Field | Value |
|-------|-------|
| **Issue ID** | [40082162](https://issues.chromium.org/issues/40082162) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebRTC |
| **Reporter** | si...@gmail.com |
| **Assignee** | mb...@chromium.org |
| **Created** | 2015-05-26 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

Recently Mozilla fixed a buffer-overflow in expat. Chromium seems to be affected by that issue as well.

References:  

Advisory: <https://www.mozilla.org/en-US/security/advisories/mfsa2015-54/>  

Patch: <https://hg.mozilla.org/releases/mozilla-esr31/rev/2f3e78643f5c>

**VERSION**  

Chrome Version: 44.0.2398.0 dev (64-bit)  

Operating System: Fedora 21, fully updated.

**REPRODUCTION CASE**  

Attached is the reproducer. I dont have access to ASAN builds, but normal builds show the "Aw snap" window. I can post asan tracebacks as soon as i am able to find where asan nightly builds are stored :)

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION:  

Reproducer attached

## Attachments

- [expat.py](attachments/expat.py) (text/plain, 973 B)

## Timeline

### np...@chromium.org (2015-05-26)

I repro'd this on stable and dev channels.  The tab crashes due to OOM.

[1:2:0526/090633:ERROR:channel.cc(300)] RawChannel read error (connection broken)
Fontconfig error: Cannot load default config file
[6822:6822:0526/090710:ERROR:navigation_entry_screenshot_manager.cc(151)] Invalid entry with unique id: 34
tcmalloc: large alloc 1207959552 bytes == 0x1b604a2a7000 @ 
[1:1:0526/090719:FATAL:memory_linux.cc(43)] Out of memory.



### cl...@chromium.org (2015-05-26)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5183911974404096

### np...@chromium.org (2015-05-26)

I can't repro w/ a local file or a static file with a standard HTTP server -- seems to need the specific headers.  I've made a test endpoint and uploaded that to clusterfuzz.

### cl...@chromium.org (2015-05-26)

[Empty comment from Monorail migration]

### np...@chromium.org (2015-05-27)

There's something particular about that .pl script on localhost that triggers the crash.  I can't repro via CGI script by setting headers either.  It may be that the local server gets hit twice, once for / and once for favicon.ico.

### si...@gmail.com (2015-05-27)

Note:

The patch, has several parts, i think OOM or buffer-overflow will depend on where the XML triggers the issue. 



### cl...@chromium.org (2015-05-30)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5727549338943488

### cl...@chromium.org (2015-05-30)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-06-03)

[Empty comment from Monorail migration]

### mb...@chromium.org (2015-06-03)

I'll take a closer look at this and try to apply the patch or track down someone else to own it. Looks like we don't have owners for our copy of expat.

### mb...@chromium.org (2015-06-03)

Apparently this is a dependency of libjingle.

### mb...@chromium.org (2015-06-03)

As a side note, prebuilt chromium ASan binaries are stored at https://commondatastorage.googleapis.com/chromium-browser-asan/index.html

### si...@gmail.com (2015-06-04)

I figured out where the ASAN builds are. I get a OOM type of condition with them, but i think that is because of the way ASAN is designed, it is not good when large memory allocations are involved, due to its shadow memory structure.

Anyways, i think its worth applying the patch and checking if the buffer-overflow still exists.

### mb...@chromium.org (2015-06-04)

From what I understand blink is using libxml, so that's probably why we're only seeing the OOMs from your repro. We do have other uses of expat in chromium, so I agree that it's probably still worth it to apply the patch.

### ph...@chromium.org (2015-06-04)

Ok, let us know if we need to do anything from the WebRTC team.

### bu...@chromium.org (2015-06-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/84ee0ec84f9de080e7d0e84dae6399d12c519d72

commit 84ee0ec84f9de080e7d0e84dae6399d12c519d72
Author: mbarbella <mbarbella@chromium.org>
Date: Thu Jun 04 23:49:01 2015

Apply a patch to prevent an integer overflow in expat.

See https://www.mozilla.org/en-US/security/advisories/mfsa2015-54/ for Mozilla's advisory. Patch taken from https://hg.mozilla.org/releases/mozilla-esr31/rev/2f3e78643f5c

BUG=492052

Review URL: https://codereview.chromium.org/1151263010

Cr-Commit-Position: refs/heads/master@{#332964}

[modify] http://crrev.com/84ee0ec84f9de080e7d0e84dae6399d12c519d72/third_party/expat/README.chromium
[modify] http://crrev.com/84ee0ec84f9de080e7d0e84dae6399d12c519d72/third_party/expat/files/lib/xmlparse.c
[add] http://crrev.com/84ee0ec84f9de080e7d0e84dae6399d12c519d72/third_party/expat/files/lib/xmlparse.c.original


### mb...@chromium.org (2015-06-05)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-06-05)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### mb...@chromium.org (2015-06-05)

[Empty comment from Monorail migration]

### si...@gmail.com (2015-06-07)

Is there a build with this patch available, so that i can test?

### mb...@chromium.org (2015-06-07)

Any of ASan LKGR builds from c#12 after r332964 should have the fix. Note that the poc from the original report shouldn't have been triggering the issue since blink uses libxml.

### si...@gmail.com (2015-06-11)

Any clue when this fix is going to released in a stable version?

### ti...@google.com (2015-07-08)

Merge-Request to M44 (branch 2403)

### pe...@google.com (2015-07-08)

[Automated comment] Less than 2 weeks to go before stable on M44, manual review required.

### pe...@google.com (2015-07-10)

#16 approved for merge to m44 branch 2403.  Please get the merge done before end of business PST Monday.

### bu...@chromium.org (2015-07-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/33f223ef93963e0efd0360445b28ce630f59bdc5

commit 33f223ef93963e0efd0360445b28ce630f59bdc5
Author: Martin Barbella <mbarbella@chromium.org>
Date: Fri Jul 10 16:52:56 2015

Apply a patch to prevent an integer overflow in expat.

See https://www.mozilla.org/en-US/security/advisories/mfsa2015-54/ for Mozilla's advisory. Patch taken from https://hg.mozilla.org/releases/mozilla-esr31/rev/2f3e78643f5c

BUG=492052

Review URL: https://codereview.chromium.org/1151263010

Cr-Commit-Position: refs/heads/master@{#332964}
(cherry picked from commit 84ee0ec84f9de080e7d0e84dae6399d12c519d72)

Review URL: https://codereview.chromium.org/1224303003 .

Cr-Commit-Position: refs/branch-heads/2403@{#484}
Cr-Branched-From: f54b8097a9c45ed4ad308133d49f05325d6c5070-refs/heads/master@{#330231}

[modify] http://crrev.com/33f223ef93963e0efd0360445b28ce630f59bdc5/third_party/expat/README.chromium
[modify] http://crrev.com/33f223ef93963e0efd0360445b28ce630f59bdc5/third_party/expat/files/lib/xmlparse.c
[add] http://crrev.com/33f223ef93963e0efd0360445b28ce630f59bdc5/third_party/expat/files/lib/xmlparse.c.original


### bu...@chromium.org (2015-07-15)

The following revision refers to this bug:
  https://chrome-internal.googlesource.com/bling/chromium.git/+/33f223ef93963e0efd0360445b28ce630f59bdc5

commit 33f223ef93963e0efd0360445b28ce630f59bdc5
Author: Martin Barbella <mbarbella@chromium.org>
Date: Fri Jul 10 16:52:56 2015


### mb...@chromium.org (2015-07-16)

[Empty comment from Monorail migration]

### si...@gmail.com (2015-07-22)

I see this is fixed in the latest release at:
http://googlechromereleases.blogspot.com/2015/07/stable-channel-update_21.html

I was surprised to see this issue not being mentioned on the security advisory page though?

### mb...@chromium.org (2015-07-24)

[Empty comment from Monorail migration]

### si...@gmail.com (2015-07-25)

Does this qualify for a reward? :)

### ti...@google.com (2015-08-17)

@sidhpurwala.huzaifa: The reward panel debated back and forth here as to whether this met the threshold for reward. The impact wasn't very clear, the OOM condition didn't appear exploitable, but we did err on the side of being generous and decided to reward this report with a $500 reward.

We'll be in contact this week to collect payment details. Congratulations!

### si...@gmail.com (2015-08-20)

Cool, thanks!

### ti...@google.com (2015-08-28)

[Empty comment from Monorail migration]

### si...@gmail.com (2015-08-29)

Hi,

It seems, no one got in touch with me, to collect payment details!

### ti...@google.com (2015-09-02)

Just following up here - someone did get in touch :)


### si...@gmail.com (2015-09-03)

Yes, someone did, thanks!

### ti...@google.com (2015-09-10)

Processing via our e-payment system takes ~7 days, but the reward should be on its way to you. Thanks again for your help!

### cl...@chromium.org (2015-09-11)

Bulk update: removing view restriction from closed bugs.

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

This issue was migrated from crbug.com/chromium/492052?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082162)*
