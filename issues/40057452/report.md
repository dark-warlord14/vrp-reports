# Security: libxml2 1-byte heap-buffer-overflow in xmlXPtrEvalXPtrPart

| Field | Value |
|-------|-------|
| **Issue ID** | [40057452](https://issues.chromium.org/issues/40057452) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals |
| **Reporter** | as...@ut.ee |
| **Assignee** | [Deleted User] |
| **Created** | 2012-04-28 |
| **Bounty** | $1,500.00 |

## Description

**VULNERABILITY DETAILS**

Here is some code from xmlXPtrEvalXPtrPart at xpointer.c:

```
len = xmlStrlen(ctxt->cur);  
len++;  
buffer = (xmlChar \*) xmlMallocAtomic(len \* sizeof (xmlChar));  
if (buffer == NULL) {  
    xmlXPtrErrMemory("allocating buffer");  
return;  
}  

cur = buffer;  
while (CUR != 0) {  
if (CUR == ')') {  
    level--;  
    if (level == 0) {  
	NEXT;  
	break;  
    }  
    \*cur++ = CUR;  
} else if (CUR == '(') {  
    level++;  
    \*cur++ = CUR;  
} else if (CUR == '^') {  
    NEXT;  
    if ((CUR == ')') || (CUR == '(') || (CUR == '^')) {  
	\*cur++ = CUR;  
    } else {  
	\*cur++ = '^';  
	\*cur++ = CUR;  
    }  
} else {  
    \*cur++ = CUR;  
}  
NEXT;  
}  
printf("before=%08x\n", \*(unsigned \*)cur);  
\*cur = 0;  
printf("after=%08x\n", \*(unsigned \*)cur);  

```

(I added the two printf's for debugging.)

Overflow occurs when ctxt->cur string ends with '^'. For example if ctxt->cur is "aaaaaaaaaaaaaa^", then:

1. len = 15 + 1 = 16
2. 16 byte buffer is allocated
3. 14 'a' chars are copied
4. '^' and '\x00' are copied together
5. \*cur = 0 will overflow

With tcmalloc, if the 16-byte block after buffer is not in use, its first bytes are a pointer to the next free block.  

Low byte of this pointer is overwritten to 0x00.

**VERSION**  

Chrome Version: 18.0.969.0 (Developer Build 113953 Linux)  

Operating System: Ubuntu 10.04.3 LTS, i686

**REPRODUCTION CASE**  

Open <http://www.ut.ee/~asd/xslt/bad.xml>

I usually also have to force chrome to use more heap by moving mouse or clicking. It might take some tries.

It prints out:

before=b95bee20  

after=b95bee00  

third\_party/tcmalloc/chromium/src/free\_list.cc:115] Memory corruption detected.

So a pointer to next free block is corrupted and tcmalloc detects the corruption. I don't think it would be too difficult to corrupt arbitrary memory, but I'm not sure, haven't tried.

## Timeline

### sc...@gmail.com (2012-04-29)

Thanks for the report. And thanks for the code analysis -- seems like you're 90% of the way to a fix?

Do you fancy taking a go at providing a Chromium patch? It would require learning how to contribute patches to Chromium (e.g. http://dev.chromium.org/developers/contributing-code), but could be worthwhile: for simple fixes to security bugs, we typically top-up any reward with a +$500 bonus.

An example of a previous Chromium patch to libxml, including link to codereview, is here:
http://src.chromium.org/viewvc/chrome?view=rev&revision=95382

### as...@ut.ee (2012-04-29)

Sure, I'll give it a try.

### as...@ut.ee (2012-04-30)

Ok, I created a patch and uploaded it for review. Chris, I currently set you as a reviewer, should I add someone else as a reviewer instead?


### sc...@gmail.com (2012-04-30)

I may not get to it immediately but I'd be delighted to be the reviewer.

### sc...@gmail.com (2012-05-02)

Confirmed on 20.0.1115.1 dev

(crash ID af7f42845f5ec1ae)

https://chromiumcodereview.appspot.com/10263014/ from Juri.

### sc...@gmail.com (2012-05-02)

[Empty comment from Monorail migration]

### [Deleted User] (2012-05-02)

[Empty comment from Monorail migration]

### ve...@gmail.com (2012-05-03)

To be honnest I looked at the patch but didn't took yet the time to investigate.
A priori XPointer is not hooked to any default handling and that wasn't looking
urgent (that module is fairly rought for historical reasons). Is there
a reproducer
by chance ? since it seems a clang report I'm afraid there isn't one,
but I'm asking
anyway :-)

Daniel

### sc...@gmail.com (2012-05-03)

@veillard: the test case hosted at http://www.ut.ee/~asd/xslt/bad.xml seems to crash Chrome for me.

The magic piece in the linked XSL file is:

<xsl:value-of select="document('doc.xml#name(aaaaaaaaaaaaaa%5E')"/>

When you say that xpointer is "not hooked to any default handling", perhaps there's an unexpected entry patch via the document() function?


### ve...@gmail.com (2012-05-03)

Ah, I had forgotten we hooked to XPointer in libxslt for document() ...

Okay, I see, I could reproduce this with valgrind using xsltproc. Weirdly
I can't reproduce it directly at the libxml2 level with
  valgrind ./testXPath -i doc.xml --xptr "name(aaaaaaaaaaaaaa^')"
though it really goes through the same code path.

Patch looks correct to me, might be a good idea to send it upstream
once you feel it is safe to send out,

Daniel

### sc...@gmail.com (2012-05-03)

Feel free to commit upstream, I'll commit to Chromium today.

### bu...@chromium.org (2012-05-03)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=135174

------------------------------------------------------------------------
r135174 | cevans@chromium.org | Thu May 03 10:32:37 PDT 2012

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/src/third_party/libxml/src/xpointer.c?r1=135174&r2=135173&pathrev=135174
 M http://src.chromium.org/viewvc/chrome/trunk/src/third_party/libxml/README.chromium?r1=135174&r2=135173&pathrev=135174

Fix XPointer bug.

BUG=125462
AUTHOR=asd@ut.ee
R=cevans@chromium.org
Review URL: https://chromiumcodereview.appspot.com/10344022
------------------------------------------------------------------------

### in...@chromium.org (2012-05-03)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-05-04)

M19: r135380

### bu...@chromium.org (2012-05-04)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=135380

------------------------------------------------------------------------
r135380 | cevans@chromium.org | Fri May 04 11:33:54 PDT 2012

Changed paths:
 M http://src.chromium.org/viewvc/chrome/branches/1084/src/third_party/libxml/src/xpointer.c?r1=135380&r2=135379&pathrev=135380
 M http://src.chromium.org/viewvc/chrome/branches/1084/src/third_party/libxml/README.chromium?r1=135380&r2=135379&pathrev=135380

Merge 135174 - Fix XPointer bug.

BUG=125462
AUTHOR=asd@ut.ee
R=cevans@chromium.org
Review URL: https://chromiumcodereview.appspot.com/10344022

TBR=cevans@chromium.org
Review URL: https://chromiumcodereview.appspot.com/10383012
------------------------------------------------------------------------

### sc...@gmail.com (2012-05-04)

Hi Juri!

Definitely reward-worthy here!
$1000 for the great find and high quality report. With $500 bonus for an accepted fix.

$1500 total

### as...@ut.ee (2012-05-05)

Thank you :)

### ve...@gmail.com (2012-05-07)

Fix pushed upstream:
http://git.gnome.org/browse/libxml2/commit/?id=d8e1faeaa99c7a7c07af01c1c72de352eb590a3e

thanks !

Daniel

### sc...@gmail.com (2012-05-10)

Payment in system.

### sc...@gmail.com (2012-05-14)

[Empty comment from Monorail migration]

### [Deleted User] (2012-05-15)

Updating status to Fixed on security bugs which were fixed when m19 went to stable.

### js...@chromium.org (2012-07-13)

CC'ing Debian libxml maintainer.

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-14)

[Empty comment from Monorail migration]

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

This issue was migrated from crbug.com/chromium/125462?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057452)*
