# Heap-buffer-overflow in xmlStringLenDecodeEntities

| Field | Value |
|-------|-------|
| **Issue ID** | [40052021](https://issues.chromium.org/issues/40052021) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals |
| **CVE IDs** | CVE-2011-3919 |
| **Reporter** | as...@ut.ee |
| **Assignee** | [Deleted User] |
| **Created** | 2011-12-11 |
| **Bounty** | $4,000.00 |

## Description

**VULNERABILITY DETAILS**  

A buffer overflow occurs in libxml/src/parser.c:2589:xmlStringLenDecodeEntities when decoding an entity reference with a long name.

The code at parser.c:2589 is:

```
if (nbchars > buffer_size - i - XML_PARSER_BUFFER_SIZE) {  
    growBuffer(buffer, XML_PARSER_BUFFER_SIZE);  
}  
for (;i > 0;i--)  
    buffer[nbchars++] = \*cur++;  

```

It checks whether additional i elements fit to the buffer, increases the buffer when necessary, and copies the data. The problem is that growBuffer grows the buffer by a fixed amount, so with enough data the overflow still occurs.

There is a similar case on line 3772, but growBuffer is handled correctly.

**VERSION**  

Chrome Version: 18.0.969.0 (Developer Build 113953 Linux) custom  

Operating System: Linux 2.6.32, Ubuntu 10.04

**REPRODUCTION CASE**  

Open poc.xhtml in chromium.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash state:

[I added printf("nbchars=%d, buffer\_size=%d\n", nbchars, buffer\_size); to the data copying loop.]

nbchars=2040, buffer\_size=700  

nbchars=2041, buffer\_size=700  

nbchars=2042, buffer\_size=700  

nbchars=2043, buffer\_size=700  

nbchars=2044, buffer\_size=700  

nbchars=2045, buffer\_size=700  

nbchars=2046, buffer\_size=700  

nbchars=2047, buffer\_size=700  

nbchars=2048, buffer\_size=700

Program received signal SIGSEGV, Segmentation fault.  

0xb28c8716 in DieFromMemoryCorruption ()  

at third\_party/tcmalloc/chromium/src/tcmalloc.cc:1828  

1828 \*p += 3; // Segv.  

(gdb) x/1i $eip  

=> 0xb28c8716 <DieFromMemoryCorruption+20>: movzbl (%eax),%eax  

(gdb) info reg  

eax 0x3 3  

ecx 0xb824cff4 -1205547020  

edx 0x2e0e4420 772686880  

ebx 0xb824cff4 -1205547020  

esp 0xbfffd768 0xbfffd768  

ebp 0xbfffd778 0xbfffd778  

esi 0xffffef3e -4290  

edi 0xb834a280 -1204510080  

eip 0xb28c8716 0xb28c8716 <DieFromMemoryCorruption+20>  

eflags 0x210206 [ PF IF RF ID ]  

cs 0x73 115  

ss 0x7b 123  

ds 0x7b 123  

es 0x7b 123  

fs 0x0 0  

gs 0x33 51  

(gdb) bt  

#0 0xb28c8716 in DieFromMemoryCorruption ()  

at third\_party/tcmalloc/chromium/src/tcmalloc.cc:1828  

#1 0xb28c88e9 in ValidateAllocatedRegion (ptr=0xb8391080, cl=26)  

at third\_party/tcmalloc/chromium/src/tcmalloc.cc:1921  

#2 0xb28c7b56 in do\_free\_with\_callback (ptr=0xb8391080,  

invalid\_free\_fn=0xb28c60e4 <InvalidFree>)  

at third\_party/tcmalloc/chromium/src/tcmalloc.cc:1221  

#3 0xb28c7d7e in do\_free (ptr=0xb8391080)  

at third\_party/tcmalloc/chromium/src/tcmalloc.cc:1249  

#4 0xb62ab827 in tc\_free ()  

#5 0xb450e63e in xmlParseAttValueComplex (ctxt=0xb837de00, attlen=0xbfffda04,  

normalize=0) at third\_party/libxml/src/parser.c:3759  

#6 0xb451b7bf in xmlParseAttValueInternal (ctxt=0xb837de00, len=0xbfffda04,  

alloc=0xbfffda00, normalize=0) at third\_party/libxml/src/parser.c:8600  

#7 0xb451b90a in xmlParseAttribute2 (ctxt=0xb837de00, pref=0x0,  

elem=0xb857fa26 "body", prefix=0xbfffda50, value=0xbfffda48,  

len=0xbfffda04, alloc=0xbfffda00) at third\_party/libxml/src/parser.c:8656  

#8 0xb451bd98 in xmlParseStartTag2 (ctxt=0xb837de00, pref=0xbfffdaf4,  

URI=0xbfffdaf0, tlen=0xbfffdb14) at third\_party/libxml/src/parser.c:8814  

#9 0xb4521ae7 in xmlParseTryOrFinish (ctxt=0xb837de00, terminate=0)  

at third\_party/libxml/src/parser.c:10867  

#10 0xb4523f3c in xmlParseChunk (ctxt=0xb837de00, chunk=0xb857d05a "S",  

size=8578, terminate=0) at third\_party/libxml/src/parser.c:11645  

(more stack frames follow)

## Attachments

- [poc.xhtml](attachments/poc.xhtml) (text/html; charset=us-ascii, 4.2 KB)
- [parser.patch](attachments/parser.patch) (text/x-c; charset=us-ascii, 4.4 KB)

## Timeline

### sk...@chromium.org (2011-12-11)

Affects all versions. Overflow corrupts the heap. I've found that sometimes the overflow in the PoC will not immediately crash the renderer, but causing the renderer to use the heap some more (eg. by clicking anywhere on the page) will trigger an exception.

There is an obvious fix for this if you compare the bad code with line 3772:
BAD @ 2589:
		if (nbchars > buffer_size - i - XML_PARSER_BUFFER_SIZE) {
		    growBuffer(buffer, XML_PARSER_BUFFER_SIZE);
		}
GOOD @ 3772:
		    while (len > buf_size - i - 10) {
			growBuffer(buf, i + 10);
		    }


@Chris: do you want to take this one?

### sk...@chromium.org (2011-12-11)

I just confirmed that changing if to while seems to fix the issue as expected.

This may have been a bad copy of code from elsewhere in the code of parser.c:
http://codesearch.google.com/codesearch#OAMlx_jo-ck/src/third_party/libxml/src/parser.c&q=growBuffer&exact_package=chromium
Maybe we should have a look to make sure this problem doesn't affect other parts of the code?

### as...@ut.ee (2011-12-11)

I spent some time with parser.c and HTMLparser.c. Couldn't find anymore obvious overflows though.

### sc...@gmail.com (2011-12-12)

@skylined: are you sure you meant to assign to me? For obvious reasons...

### sk...@chromium.org (2011-12-12)

Heh, no! You just relax and change nappies :)

### sc...@gmail.com (2011-12-13)

@skylined: it seems like you have a fix and it is fairly simple? How about cutting out the middle man and uploading the patch yourself? Make sure to change README.chromium too to describe the patch (see http://src.chromium.org/viewvc/chrome?view=rev&revision=100953 for an example of exactly what to do).

Also, please paste the patch inline into this bug (since it is small) and then cc: veillard@gmail.com who is the upstream libxml maintainer.

### in...@chromium.org (2011-12-13)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4427213

Uploader: inferno@chromium.org

Crash Type: Heap-buffer-overflow WRITE 1
Crash Address: 0x7f2aa98bff3c
Crash State:
  - crash stack -
  xmlStringLenDecodeEntities
  xmlParseAttValueInternal
  xmlParseStartTag2
  

Minimized Testcase (4.19 Kb): https://cluster-fuzz.appspot.com/download/AMIfv97-qX4BNSV9PsAq_IiXhViKBbi422WIm0RA86ifgLRtKimQ8fxdzNmI4zYwbT1Vc8h9Cm0HXLbehUAXu6M_nQF4gW1M7UDh8v0MzHLYjelr4-Fenz4v1anJ10lVe0SY4UEJt4yYohkZKRpTsJ00wSO4Wrqnsg

### in...@chromium.org (2011-12-13)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-12-14)

[Empty comment from Monorail migration]

### ve...@gmail.com (2011-12-14)

Hum,

do you have a CVE for this ? I'm trying to see if that's something we
tracked independently,
it seems not, but a CVE would help :-)
Problem identification looks right, but I need to double check

  thanks for the heads-up !

Daniel

### ve...@gmail.com (2011-12-14)

I just looked and we should avoid the while, an if is better in this case
as an allocation error in growBuffer leads to a proper failure. we just need
to allocate the amount we computed as being needed.

Daniel

diff --git a/parser.c b/parser.c
index 4e5dcb9..c55e41d 100644
--- a/parser.c
+++ b/parser.c
@@ -2709,7 +2709,7 @@ xmlStringLenDecodeEntities(xmlParserCtxtPtr ctxt, const xm
 
                buffer[nbchars++] = '&';
                if (nbchars > buffer_size - i - XML_PARSER_BUFFER_SIZE) {
-                   growBuffer(buffer, XML_PARSER_BUFFER_SIZE);
+                   growBuffer(buffer, i + XML_PARSER_BUFFER_SIZE);
                }
                for (;i > 0;i--)
                    buffer[nbchars++] = *cur++;


### js...@chromium.org (2011-12-14)

@veillard - Sorry, I just saw your request. I've allocated CVE-2011-3919 for you.

### ve...@gmail.com (2011-12-15)

Could someone verify in your framework that the patch in https://crbug.com/chromium/107128#c11 fixes it for
you ? It should and avoid looping over realloc (in growBuffer) which is often a
costly operation

  thanks,

Daniel

### in...@chromium.org (2011-12-15)

Daniel, i verified that your fix works perfectly with ASAN and stops the buffer overflow.

### ve...@gmail.com (2011-12-16)

Cool, thanks :-) !

Daniel

### ve...@gmail.com (2011-12-16)

Cool, thanks :-) !

Daniel

### sk...@chromium.org (2011-12-16)

Thanks Daniel, that is a lot better. Looking again at the code in https://crbug.com/chromium/107128#c1, that "growBuffer" call inside the "while" that I copied from makes no sense - it will always be false on the second loop, so an if should suffice there. There are a few more places like it where "while" is used where "if" would be just as good.

In an attempt to prevent future regressions and/or similar mistakes, I'd like to fix this by introducing a new macro that does both the check and grow. I've replaced all existing code that does a check+grow with a call to this macro. This fixes the buffer overflow and the unneeded "while" loops. This macro will make sure the check and the grow always use the same size. Thoughts?




### sc...@gmail.com (2011-12-30)

@skylined: is the fix you and Daniel settled on landed in Chromium yet?
I want this fixed in the Chrome 16 stable update, which is coming up really soon.

### in...@chromium.org (2011-12-31)

I had a chat with Anthony and we need to take care all the merges for m16 by this Tuesday (Jan 3rd). For a m16 patch that hasn't baked on trunk, i would prefer to go with Daniel's one word patch in c#11 and then we can do the skylined's patch as a followup. Skylined, do you have time to submit a chromium patch (similar to other libxml patches) and committed on tuesday ?

### sc...@gmail.com (2011-12-31)

Yes, let's just use the upstream patch. It's simple and risk-free.

It was already committed upstream:
http://git.gnome.org/browse/libxml2/commit/?id=5bd3c061823a8499b27422aee04ea20aae24f03e

So all we need to do is copy the 3-character addition into our own libxml source tree and update README.chromium to reference the above upstream commit URL.

I would have done this myself last night, but it seems I powered off my work Linux machine for my absence.

### sc...@gmail.com (2012-01-01)

I can get this all done on Tuesday, assuming the merge deadline is the usual 7pm Tuesday.

### in...@chromium.org (2012-01-01)

Yes, Anthony said end of day for the deadline.

### sc...@gmail.com (2012-01-02)

Ok. I'll kick by the office to say hi and pick up some stuff and take care of it then :)

### bu...@chromium.org (2012-01-03)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=116175

------------------------------------------------------------------------
r116175 | cevans@chromium.org | Tue Jan 03 11:53:21 PST 2012

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/src/third_party/libxml/src/parser.c?r1=116175&r2=116174&pathrev=116175
 M http://src.chromium.org/viewvc/chrome/trunk/src/third_party/libxml/README.chromium?r1=116175&r2=116174&pathrev=116175

Pull entity fix from upstream.

BUG=107128
Review URL: http://codereview.chromium.org/9072008
------------------------------------------------------------------------

### sc...@gmail.com (2012-01-03)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-01-03)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=116213

------------------------------------------------------------------------
r116213 | cevans@chromium.org | Tue Jan 03 14:03:07 PST 2012

Changed paths:
 M http://src.chromium.org/viewvc/chrome/branches/912/src/third_party/libxml/README.chromium?r1=116213&r2=116212&pathrev=116213
 M http://src.chromium.org/viewvc/chrome/branches/912/src/third_party/libxml/src/parser.c?r1=116213&r2=116212&pathrev=116213

Merge 116175 - Pull entity fix from upstream.

BUG=107128
Review URL: http://codereview.chromium.org/9072008

TBR=cevans@chromium.org
Review URL: http://codereview.chromium.org/9014028
------------------------------------------------------------------------

### bu...@chromium.org (2012-01-03)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=116214

------------------------------------------------------------------------
r116214 | cevans@chromium.org | Tue Jan 03 14:04:38 PST 2012

Changed paths:
 M http://src.chromium.org/viewvc/chrome/branches/963/src/third_party/libxml/src/parser.c?r1=116214&r2=116213&pathrev=116214
 M http://src.chromium.org/viewvc/chrome/branches/963/src/third_party/libxml/README.chromium?r1=116214&r2=116213&pathrev=116214

Merge 116175 - Pull entity fix from upstream.

BUG=107128
Review URL: http://codereview.chromium.org/9072008

TBR=cevans@chromium.org
Review URL: http://codereview.chromium.org/9072018
------------------------------------------------------------------------

### sc...@gmail.com (2012-01-03)

@asd@ut.ee: what name should we use for credit in our release notes / hall of fame?

### ve...@gmail.com (2012-01-04)

Oops, I didn't realized there was something pending on this.
I had commited the minimal patch in libvirt git but it's not skylined' version.
I just looked at his patch and it's fine too, it's just a code cleanup IMHO does
not change semantic. So either way the build should be fine.

Daniel

### as...@ut.ee (2012-01-04)

@scarybeasts: Please use 'Jüri Aedla'.

### js...@chromium.org (2012-01-04)

[Empty comment from Monorail migration]

### js...@chromium.org (2012-01-04)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-01-05)

Thank you Jüri!

And also congratulations! This is a very nice bug, and reported well, so it certainly qualifies for a $1000 Chromium Security Reward.

With any luck, we'll be able to get the fix to users tomorrow.

### as...@ut.ee (2012-01-05)

Thanks!

### sc...@gmail.com (2012-02-15)

[Empty comment from Monorail migration]

### [Deleted User] (2012-05-15)

Marking old security bugs Fixed..

### js...@chromium.org (2012-07-13)

CC'ing Debian libxml maintainer.

### sc...@gmail.com (2012-08-06)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-08-16)

Increasing reward by $3000 to $4000 as per http://blog.chromium.org/2012/08/chromium-vulnerability-rewards-program.html


### sc...@gmail.com (2012-09-12)

Top-up reward paid as part of a $4000 batch.

### bu...@chromium.org (2012-10-14)

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

### cl...@chromium.org (2013-06-13)

ClusterFuzz has detected this issue as fixed in range 116169:116185.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4427213

Uploader: inferno@chromium.org

Crash Type: Heap-buffer-overflow WRITE 1
Crash Address: 0x7f2aa98bff3c
Crash State:
  - crash stack -
  xmlStringLenDecodeEntities
  xmlParseAttValueInternal
  xmlParseStartTag2
  
Fixed: https://cluster-fuzz.appspot.com/revisions?range=116169:116185

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv97-qX4BNSV9PsAq_IiXhViKBbi422WIm0RA86ifgLRtKimQ8fxdzNmI4zYwbT1Vc8h9Cm0HXLbehUAXu6M_nQF4gW1M7UDh8v0MzHLYjelr4-Fenz4v1anJ10lVe0SY4UEJt4yYohkZKRpTsJ00wSO4Wrqnsg

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

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

This issue was migrated from crbug.com/chromium/107128?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40052021)*
