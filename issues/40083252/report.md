# Security: security vulnerabilities in libpng (CVE-2015-7981, CVE-2015-8126)

| Field | Value |
|-------|-------|
| **Issue ID** | [40083252](https://issues.chromium.org/issues/40083252) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals |
| **CVE IDs** | CVE-2015-7981, CVE-2015-8126 |
| **Reporter** | jo...@gmail.com |
| **Assignee** | md...@chromium.org |
| **Created** | 2015-11-23 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

The libpng copy that's bundled in chromium is currently at version 1.2.52. This version is vulnerable to out-of-bound reads and writes as described on the libpng home page.  

See CVE-2015-8126, <http://www.libpng.org/pub/png/libpng.html>

libpng should be updated to 1.2.54.

## Timeline

### th...@chromium.org (2015-11-23)

[Empty comment from Monorail migration]

### md...@chromium.org (2015-11-23)

;_;

### wf...@chromium.org (2015-11-23)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-11-23)

[Empty comment from Monorail migration]

### wf...@chromium.org (2015-11-24)

[Empty comment from Monorail migration]

### md...@chromium.org (2015-11-27)

[Empty comment from Monorail migration]

### md...@chromium.org (2015-11-27)

For the record, updating to 1.2.54 will address CVE-2015-7981 too.

### no...@chromium.org (2015-11-29)

Can't find or access https://crbug.com/chromium/561979 for some reason.

### md...@chromium.org (2015-11-29)

It's Restrict-View-SecurityTeam.  I've CC'd you.

### no...@chromium.org (2015-12-01)

Thanks, adding Matt and Leon.  You guys may need to update Skia similarly, if you don't already have the fixed libpng there ...

### no...@chromium.org (2015-12-01)

... the Chromium fix is https://codereview.chromium.org/1467263003 for reference.

### bu...@chromium.org (2015-12-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/7f3d85b096f66870a15b37c2f40b219b2e292693

commit 7f3d85b096f66870a15b37c2f40b219b2e292693
Author: mdempsky <mdempsky@chromium.org>
Date: Tue Dec 01 00:48:53 2015

third_party/libpng: update to 1.2.54

TBR=darin@chromium.org
BUG=560291

Review URL: https://codereview.chromium.org/1467263003

Cr-Commit-Position: refs/heads/master@{#362298}

[modify] http://crrev.com/7f3d85b096f66870a15b37c2f40b219b2e292693/third_party/libpng/LICENSE
[modify] http://crrev.com/7f3d85b096f66870a15b37c2f40b219b2e292693/third_party/libpng/README
[modify] http://crrev.com/7f3d85b096f66870a15b37c2f40b219b2e292693/third_party/libpng/README.chromium
[modify] http://crrev.com/7f3d85b096f66870a15b37c2f40b219b2e292693/third_party/libpng/png.c
[modify] http://crrev.com/7f3d85b096f66870a15b37c2f40b219b2e292693/third_party/libpng/png.h
[modify] http://crrev.com/7f3d85b096f66870a15b37c2f40b219b2e292693/third_party/libpng/pngconf.h
[modify] http://crrev.com/7f3d85b096f66870a15b37c2f40b219b2e292693/third_party/libpng/pngget.c
[modify] http://crrev.com/7f3d85b096f66870a15b37c2f40b219b2e292693/third_party/libpng/pngpread.c
[modify] http://crrev.com/7f3d85b096f66870a15b37c2f40b219b2e292693/third_party/libpng/pngread.c
[modify] http://crrev.com/7f3d85b096f66870a15b37c2f40b219b2e292693/third_party/libpng/pngrtran.c
[modify] http://crrev.com/7f3d85b096f66870a15b37c2f40b219b2e292693/third_party/libpng/pngrutil.c
[modify] http://crrev.com/7f3d85b096f66870a15b37c2f40b219b2e292693/third_party/libpng/pngset.c
[modify] http://crrev.com/7f3d85b096f66870a15b37c2f40b219b2e292693/third_party/libpng/pngwrite.c
[modify] http://crrev.com/7f3d85b096f66870a15b37c2f40b219b2e292693/third_party/libpng/pngwutil.c


### md...@chromium.org (2015-12-01)

Updated to 1.2.54.  We'll still want to update to 1.2.55, but since that's not security relevant, I'm tracking it separately in https://crbug.com/chromium/563803.

### cl...@chromium.org (2015-12-01)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### ti...@google.com (2016-01-09)

Spoke to mdempsky - we're going to let this roll in with M49 and not merge to M48.

### no...@chromium.org (2016-01-09)

SGTM.

### no...@chromium.org (2016-01-09)

mdempsky@  Note sure if the original report had any example images that tickled these sec-bugs?  A stretch goal would be to get some examples and add them our blink layout tests and also to cluster fuzz.


### no...@chromium.org (2016-01-09)

CVE-2015-7981 - Glen tested libpng on http://sourceforge.net/p/libpng/bugs/241/#b234 and made the following note:

 "Note that only applications that call png_convert_to_rfc1123() are vulnerable."

Grepping our updated libpng code, no callers of that code so CVE-2015-7981 was benign in Chrome.


### ti...@google.com (2016-02-29)

Adding reward-topanel label so that we can consider this report under the Chrome Reward program. Full details here: https://www.google.com/about/appsecurity/chrome-rewards/

### ti...@google.com (2016-03-02)

Hi Joerg, just letting you know that our reward panel decided to award you $500 for bringing this issue to our attention. Congratulations!

We'll thank you in our Chrome 49 release notes as "joerg.bornemann". If you'd like to update the release notes to a different credit name, please let me know. I'll use CVE-2015-8126 to refer to this issue, as based on #18 it seems that CVE-2015-7981 didn't apply. 

Someone from our finance team will follow-up within 7 days to collect payment details. If this doesn't happen, please either update this bug or email me at timwillis@

Thanks for your report and helping keep Chrome libraries up to date!

### jo...@gmail.com (2016-03-04)

Cool, thanks!

### cl...@chromium.org (2016-03-08)

This security bug has been closed for more than 14 weeks. Removing view restrictions.

- Your friendly Sheriffbot

### ti...@google.com (2016-03-12)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/560291?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/561979]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083252)*
