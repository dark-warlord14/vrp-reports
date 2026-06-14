# Use after free in RenderText lineboxes.

| Field | Value |
|-------|-------|
| **Issue ID** | [40094201](https://issues.chromium.org/issues/40094201) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | mi...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2011-08-22 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

use-after free with webkit-columns

**VERSION**  

Chrome Version: trunk + beta, not stable  

Operating System: linux 64bit

**REPRODUCTION CASE**  

attached

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: renderer

==10859== ERROR: AddressSanitizer crashed on address 0x00007fffdff96480 at pc 0x7ffff40cfef3 bp 0x7fffffff5310 sp 0x7fffffff52d0  

READ of size 4 at 0x00007fffdff96480 thread T0  

#0 0x7ffff40cfef3 in WebCore::BidiContext::create(unsigned char, WTF::Unicode::Direction, bool, WebCore::BidiEmbeddingSource, WebCore::BidiContext\*) ???:0  

#1 0x7ffff3fa353c in WebCore::BidiStatus::BidiStatus(WebCore::TextDirection, bool) ???:0

0x00007fffdff96480 is located 0 bytes inside of 16-byte region [0x00007fffdff96480,0x00007fffdff96490)  

freed by thread T0 here:  

#0 0x7ffff6c88b7a in free *asan\_rtl*  

#1 0x7ffff4ff49f2 in WebCore::RootInlineBox::childRemoved(WebCore::InlineBox\*) ???:0

## Attachments

- [vg.txt](attachments/vg.txt) (text/plain; charset=us-ascii, 165.0 KB)
- [asan.txt](attachments/asan.txt) (text/plain; charset=us-ascii, 11.8 KB)
- [vg-google-chrome-beta.txt](attachments/vg-google-chrome-beta.txt) (text/plain; charset=us-ascii, 67.3 KB)
- [016.html](attachments/016.html) (text/plain; charset=us-ascii, 250 B)
- [64120.html](attachments/64120.html) (text/plain; charset=us-ascii, 453 B)
- [asan_64inside120.txt](attachments/asan_64inside120.txt) (text/x-c; charset=us-ascii, 7.1 KB)
- [still.html](attachments/still.html) (text/plain; charset=us-ascii, 4.6 KB)
- [still.txt](attachments/still.txt) (text/x-c; charset=us-ascii, 10.8 KB)
- [smallish.html](attachments/smallish.html) (text/plain; charset=us-ascii, 365 B)

## Timeline

### in...@chromium.org (2011-08-22)

Even though crash stack different, this looks same as http://code.google.com/p/chromium/issues/detail?id=89580 [and also one other bug which also crashes slightly). We should wait a little before duping, until someone can do more analysis.

Our testcase::
<style>
div { -webkit-column-count: 2; }
h2 { -webkit-column-span: all; }
</style>
<script>
setTimeout("try { gc(); } catch(e) {}", 200);
setTimeout("child = document.getElementById('anything');", 100);
setTimeout("try { document.body.offsetTop; child = document.getElementById('test'); child.parentNode.removeChild(child); } catch(e) {}", 0);
</script>
<meta http-equiv="refresh" content="1"/><div><span id="test"><h2>

### sk...@chromium.org (2011-08-23)

Unlike https://crbug.com/chromium/89580, this hits an ASSERT:
src\third_party\webkit\source\webcore\rendering\inlinebox.h
    InlineFlowBox* parent() const
    {
        ASSERT(!m_hasBadParent);
        return m_parent;
    }
...before crashing in a very similar way as https://crbug.com/chromium/89580. I think you are right inferno and this is a dup, but I have no definitive proof.

### in...@chromium.org (2011-08-29)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-08-30)

Miaubiz, you are lucky, this is a different bug. This is how lineboxes are not dirtied properly from my preliminary analysis.

### in...@chromium.org (2011-08-30)

Morrita, this looks like an issue coming from ShadowContentElement changes. This crashes readily under ASAN linux and easily on windows by resizing width to smaller size and refreshing using f5 and pressing clicks near the middle 'A'. Can you please help to take a look.

### mi...@gmail.com (2011-08-30)

is this the same?

==19687== ERROR: AddressSanitizer crashed on address 0x00007fffdbea23c0 at pc 0x7ffff4e90264 bp 0x7fffffff8310 sp 0x7fffffff82e0
WRITE of size 8 at 0x00007fffdbea23c0 thread T0
    #0 0x7ffff4e90264 in WebCore::RenderObjectChildList::destroyLeftoverChildren() ???:0
0x00007fffdbea23c0 is located 64 bytes inside of 120-byte region [0x00007fffdbea2380,0x00007fffdbea23f8)
freed by thread T0 here:
    #0 0x7ffff6c74122 in operator delete(void*) _asan_rtl_
    #1 0x7ffff2655f49 in v8::internal::GlobalHandles::Node::PostGarbageCollectionProcessing(v8::internal::Isolate*, v8::internal::GlobalHandles*) ???:0
previously allocated by thread T0 here:
    #0 0x7ffff6c744ea in operator new(unsigned long) _asan_rtl_
    #1 0x7ffff3beab3d in WebCore::HTMLElement::create(WebCore::QualifiedName const&, WebCore::Document*) ???:0


### do...@chromium.org (2011-08-30)

This unsurprisingly snaps 15.0.866.0 (Official Build 98785) canary OS Mac OS X WebKit 535.2 (@94043) if you don’t have a Linux machine handy (and weirdly the tab *stays* snapped despite reload, although maybe that is an unrelated issue.)

### in...@chromium.org (2011-08-30)

miaubiz, the testcase in c#6 is https://crbug.com/chromium/89580.

### mi...@gmail.com (2011-08-30)

@inferno: ok thanks. I thought 89580 was fixed. since the file from c#1 stopped crashing for me after your commit yesterday

### in...@chromium.org (2011-08-30)

miaubiz: which commit caused c#1 to stop crashing ?? The real fix is still pending review ?

### mi...@gmail.com (2011-08-30)

@inferno: 94001 

although it could be a completely different one. 
since this morning, c#1 won't crash for me.

last compile was probably like sunday or monday morning.

### in...@chromium.org (2011-08-30)

miaubiz, looks like you tested it wrong. testcase in c#1 is still crashing with webkit 94056, chromium 98804 under ASAN.

### [Deleted User] (2011-08-31)

Reproduced on linux debug build, it hits assertion as #2 mentioned.
Looking...


### in...@chromium.org (2011-08-31)

Morrita, i think you should look into the cloning area. The reason might be when first rendertext is destroyed, its line boxes are cleared. Then, probably a cloned rendertext with same linebox is destroyed, which causes a use after free. Please put breakpoints in splitInlines and splitBlocks caller to see the cloning process.

### [Deleted User] (2011-09-01)

I'm sorry but I'm ooo for a week and I couldn't fix this today...
I can attack this after that, or feel free to take this.


### sc...@gmail.com (2011-09-13)

@morrita: do you mind if we take you up on your offer to attack this? :)

### [Deleted User] (2011-09-14)

Yeah, I just came back yesterday. Now I'm restarting on this.


### [Deleted User] (2011-09-16)

Filed upstream.
https://bugs.webkit.org/show_bug.cgi?id=68228
I tried a fix at Webkit@r94150. But the failure on 016.html disappears on r95264.
I'll post a fix anyway.


### in...@chromium.org (2011-09-16)

Yes, something has fixed it. Unable to reproduce on ASAN linux. Thanks for defensive fix.

### mi...@gmail.com (2011-09-16)

here's a crashing one on 95270.. I can minimize if need be

### mi...@gmail.com (2011-09-16)

here's a small one that crashes for me

### in...@chromium.org (2011-09-19)

Awesome Miaubiz. The smallish.html reproduces easily on windows.

Morrita, can you please check if your patch fixes the testcase in c#21. We have an upcoming m14 stable patch, so it will be awesome if we can sneak this fix in :)

### [Deleted User] (2011-09-20)

Yes, I confirmed the patch fixes the crash on smallish.html.


### in...@chromium.org (2011-09-21)

Thanks a lot Morrita.

http://trac.webkit.org/changeset/95600

### in...@chromium.org (2011-09-23)

merged to m15 in r95821

### js...@chromium.org (2011-09-26)

[Empty comment from Monorail migration]

### [Deleted User] (2011-09-26)

Merged to m14 as r96025.

### sc...@gmail.com (2011-10-01)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-10-03)

@miaubiz: nice find, good work as usual. $1000

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

### js...@chromium.org (2011-10-05)

Batch update.

### sc...@gmail.com (2011-10-07)

Payment in system.

### [Deleted User] (2012-05-15)

Marking old security bugs Fixed..

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

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/93788?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094201)*
