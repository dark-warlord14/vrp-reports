# Crash due to bad cast to rendertextfragment in updatefirstletter.

| Field | Value |
|-------|-------|
| **Issue ID** | [40088020](https://issues.chromium.org/issues/40088020) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | mi...@gmail.com |
| **Assignee** | in...@chromium.org |
| **Created** | 2011-02-16 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**

rip == 0 with dd, dir tags and designmode

**VERSION**  

Chromium 11.0.672.0 Ubuntu 10.10  

Linux 2.6.35-26-generic #46-Ubuntu SMP Sun Jan 30 06:59:07 UTC 2011 x86\_64

Google Chrome 9.0.597.98  

Linux 2.6.35-26-generic #46-Ubuntu SMP Sun Jan 30 06:59:07 UTC 2011 x86\_64

Google Chrome 9.0.597.98 (Official build 74359)  

Windows 7 32bit

**REPRODUCTION CASE**  

attached.

there are a bunch of nullpointerish repros, the html is similar but they segfault at different offsets.

then there's a longer repro that jumps to 0 with chromium and 7 with chrome on linux.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State:

(gdb) bt 5  

#0 0x0000000000000000 in ?? ()  

#1 0x00007ffff67b7265 in WebCore::InlineFlowBox::deleteLine (this=0x7ffff94804f8, arena=0x7ffff9cddc00) at third\_party/WebKit/Source/WebCore/rendering/InlineFlowBox.cpp:127  

#2 0x00007ffff67f01cc in WebCore::RenderBlock::layoutInlineChildren (this=0x7ffff9c6ac20, relayoutChildren=<value optimized out>, repaintLogicalTop=@0x7fffdf093f5c, repaintLogicalBottom=@0x7fffdf093f58)

## Attachments

- [nullptr70.html](attachments/nullptr70.html) (text/plain; charset=us-ascii, 246 B)
- [win.html](attachments/win.html) (text/html; charset=us-ascii, 944 B)
- [nullptr20.html](attachments/nullptr20.html) (text/html; charset=us-ascii, 251 B)
- [nullptr38.html](attachments/nullptr38.html) (text/html; charset=us-ascii, 250 B)
- [crash_wrangler_73134.txt](attachments/crash_wrangler_73134.txt) (text/x-c++; charset=us-ascii, 7.1 KB)

## Timeline

### mi...@gmail.com (2011-02-16)

attached crash wrangler for nullptr20.html on OSX 10.6 Snow Leopard and Chromium 11.0.667.0 (667.0)

exception=EXC_BAD_ACCESS:signal=10:is_exploitable=yes:instruction_disassembly=:instruction_address=0x0000000000000000:access_type=exec:access_address=0x0000000000000000:
Trying to execute a bad address, this is a potentially exploitable issue

### js...@chromium.org (2011-02-16)

CC'ing @rniwa since this appears to be an editing issue. Will take a closer look after I get into the office.

### in...@chromium.org (2011-02-16)

this looks rendering, taking a look. i will triage as well to identify if these are dupes.

### in...@chromium.org (2011-02-16)

ok, here is the deal. Three of these are dupes and one of these is a null pointer. I can fix them all since i like rendering :)

### mi...@gmail.com (2011-02-16)

dupes of each other or a previously reported bug?

### in...@chromium.org (2011-02-16)

dupes of each other :)

webkit bug filed - https://bugs.webkit.org/show_bug.cgi?id=54568

More clear testcase::
<html>
    <style>
        .test1:first-letter { content : ""; }
        .test2:first-letter { text-align : ""; }
    </style>
    <div class="test1">
    <div class="test2">
    PASS 
    </div>
    </div>
    <script>
        if (window.layoutTestController)
            layoutTestController.dumpAsText();

        document.execCommand("selectall");
        document.designMode = "on";
        document.execCommand("ForeColor", false, 1);
    </script>
</html>


### in...@chromium.org (2011-02-16)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-02-17)

http://trac.webkit.org/changeset/78744

### [Deleted User] (2011-02-17)

Wow, this was really quick!

### sc...@gmail.com (2011-02-18)

Nice one miaubiz! This might have been a stability issue too, so we're happy to be rid of it. Thanks to the high quality of the report, it provisionally qualifies for a $1000 Chromium Security Reward.

----
Boilerplate text:
Please do NOT publicly disclose details until a fix has been released to all our
users. Early public disclosure may cancel the provisional reward.
Also, please be considerate about disclosure when the bug affects a core library
that may be used by other products.
Please do NOT share this information with third parties who are not directly
involved in fixing the bug. Doing so may cancel the provisional reward.
Please be honest if you have already disclosed anything publicly or to third parties.
----

### js...@chromium.org (2011-02-28)

[Empty comment from Monorail migration]

### ch...@gmail.com (2011-02-28)

merged to m10 as http://trac.webkit.org/changeset/79903

### sc...@gmail.com (2011-03-10)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-03-15)

Invoice finalized; payment is in e-payment system.

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-10-05)

Batch update.

### js...@chromium.org (2012-04-18)

Lifting view restrictions.

### js...@chromium.org (2012-04-18)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-26)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-26)

This issue was migrated from crbug.com/chromium/73134?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40088020)*
