# Out of bounds read in WebCore::LayerTilerChromium::invalidateRect (dev only)

| Field | Value |
|-------|-------|
| **Issue ID** | [40087738](https://issues.chromium.org/issues/40087738) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink, Internals>Compositing |
| **Reporter** | ma...@gmail.com |
| **Assignee** | in...@chromium.org |
| **Created** | 2011-02-09 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

Under certain circumstances, the development build of google chrome will crash due to an out of bounds read of a Tile\* structure in WebCore::LayerTilerChromium::invalidateRect.

**VERSION**  

Chrome Version: Tested in Google Chrome 10.0.648.18 dev, debugging done in Chromium 11.0.662.0  

Operating System: Ubuntu 10.10 (32-bit)

**REPRODUCTION CASE**  

<video src="does\_not\_exist"></video>  

<marquee hspace="68738363">

<textarea rows="356093779">
\*\*FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION\*\*
Type of crash: tab
With a debugging build, the crash occurs at an assertion failure in WTF::Vector::at, as shown below.
Program received signal SIGSEGV, Segmentation fault.
[Switching to Thread 0xb20f6b70 (LWP 21926)]
0x09d98337 in WTF::Vector<WTF::OwnPtr<WebCore::LayerTilerChromium::Tile>, 0u>::at (this=0xc988ab4, i=84398514)
at third\_party/WebKit/Source/JavaScriptCore/wtf/Vector.h:536
536 ASSERT(i < size());
(gdb) bt
#0 0x09d98337 in WTF::Vector<WTF::OwnPtr<WebCore::LayerTilerChromium::Tile>, 0u>::at (this=0xc988ab4, i=84398514)
at third\_party/WebKit/Source/JavaScriptCore/wtf/Vector.h:536
#1 0x09d97b82 in WTF::Vector<WTF::OwnPtr<WebCore::LayerTilerChromium::Tile>, 0u>::operator[] (this=0xc988ab4, i=84398514)
at third\_party/WebKit/Source/JavaScriptCore/wtf/Vector.h:545
#2 0x09d96636 in WebCore::LayerTilerChromium::invalidateRect (this=0xc988a80,
contentRect=...)
at third\_party/WebKit/Source/WebCore/platform/graphics/chromium/LayerTilerChromium.cpp:205
#3 0x09d8f149 in WebCore::LayerRendererChromium::invalidateRootLayerRect (
this=0xc9b4120, dirtyRect=..., visibleRect=..., contentRect=...)
at third\_party/WebKit/Source/WebCore/platform/graphics/chromium/LayerRendererChromium.cpp:158
#4 0x09acc980 in WebKit::WebViewImpl::invalidateRootLayerRect (
this=0xc852840, rect=...)
at third\_party/WebKit/Source/WebKit/chromium/src/WebViewImpl.cpp:2292
#5 0x09addae6 in WebKit::ChromeClientImpl::invalidateContentsAndWindow (
this=0xc852854, updateRect=...)
at third\_party/WebKit/Source/WebKit/chromium/src/ChromeClientImpl.cpp:528
(gdb) print i
$1 = 84398514
(gdb) print this->size()
$2 = 84398514
(gdb) frame 2
#2 0x09d96636 in WebCore::LayerTilerChromium::invalidateRect (this=0xc988a80,
contentRect=...)
at third\_party/WebKit/Source/WebCore/platform/graphics/chromium/LayerTilerChromium.cpp:205
205 Tile\\* tile = m\_tiles[tileIndex(i, j)].get();
(gdb) info locals
tile = 0x0
bound = {m\_location = {m\_x = 169583214, m\_y = -1307620280}, m\_size = {
m\_width = 162123484, m\_height = -1307620232}}
i = 86531
j = 157
layerRect = {m\_location = {m\_x = 0, m\_y = 0}, m\_size = {m\_width = 137476734,
m\_height = 1402533347}}
top = 0
left = 0
right = 537018
bottom = 5478645
With a release build or the current google-chrome-unstable package, the crash occurs due to an out of bounds read (related to the assertion failure above).
Program received signal SIGSEGV, Segmentation fault.
[Switching to Thread 0xb20f6b70 (LWP 22013)]
0x094adde7 in WebCore::LayerTilerChromium::invalidateRect(WebCore::IntRect const&) ()
(gdb) disas
...
0x094addd6 <+122>: cmp -0x24(%ebp),%ebx
0x094addd9 <+125>: jg 0x94ade39 <\_ZN7WebCore18LayerTilerChromium14invalidateRectERKNS\_7IntRectE+221>
0x094adddb <+127>: mov 0x10(%esi),%ecx
0x094addde <+130>: imul %eax,%ecx
0x094adde1 <+133>: lea (%ebx,%ecx,1),%ecx
0x094adde4 <+136>: mov 0x38(%esi),%edx
=> 0x094adde7 <+139>: mov (%edx,%ecx,4),%edi
0x094addea <+142>: test %edi,%edi
...
(gdb) i r
eax 0x9f 159
ecx 0x5175400 85414912
edx 0xe70e000 242278400
ebx 0x70db 28891
esp 0xb20f4de0 0xb20f4de0
ebp 0xb20f4e58 0xb20f4e58
esi 0xb155540 185947456
edi 0x0 0
eip 0x94adde7 0x94adde7 <WebCore::LayerTilerChromium::invalidateRect(WebCore::IntRect const&)+139>
eflags 0x210212 [ AF IF RF ID ]
cs 0x73 115
ss 0x7b 123
ds 0x7b 123
es 0x7b 123
fs 0x0 0
gs 0x33 51
(gdb)
A demonstration with the google chrome from the google-chrome-unstable package follows, just to demonstrate the nature of the crash and version.
$ google-chrome --version
Google Chrome 10.0.648.18 dev
$ google-chrome crash.html
$ tail -n1 /var/log/kern.log
Feb 8 21:56:20 marty-CR600 kernel: [13657.866309] chrome[22215]: segfault at 1fca7000 ip 0940bdce sp bfa5b6e0 error 4 in chrome[8048000+2bd7000]

## Attachments

- [crash.html](attachments/crash.html) (text/plain; charset=us-ascii, 93 B)

## Timeline

### ma...@gmail.com (2011-02-09)

I forgot to mention that the crash does not occur on a 64-bit system, so it is likely related to an integer overflow. This seems to make sense given the definition of the tileIndex function.

int LayerTilerChromium::tileIndex(int i, int j) const
{
    ASSERT(i >= 0 && j >= 0 && i < m_layerTileSize.width() && j < m_layerTileSize.height());
    return i + j * m_layerTileSize.width();
}

### in...@chromium.org (2011-02-09)

Thanks Marty for another awesome issue. The problem looks to be in 

oid LayerTilerChromium::resizeLayer(const IntSize& size)
{
    if (m_layerSize == size)
        return;

    int width = (size.width() + m_tileSize.width() - 1) / m_tileSize.width();
    int height = (size.height() + m_tileSize.height() - 1) / m_tileSize.height();

    Vector<OwnPtr<Tile> > newTiles;
    newTiles.resize(width * height);

we cannot just multiply this correctly :)

### in...@chromium.org (2011-02-09)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-02-09)

There was one more place with similar pattern. So, i am thinking the patch like this

----
Index: platform/graphics/chromium/LayerTilerChromium.cpp
===================================================================
--- platform/graphics/chromium/LayerTilerChromium.cpp	(revision 77686)
+++ platform/graphics/chromium/LayerTilerChromium.cpp	(working copy)
@@ -80,7 +80,17 @@
     reset();
 
     m_tileSize = size;
-    m_tilePixels = adoptArrayPtr(new uint8_t[m_tileSize.width() * m_tileSize.height() * 4]);
+
+    if (m_tileSize.width() > INT_MAX / m_tileSize.height())
+        CRASH();
+
+    int tilePixelsSize = m_tileSize.width() * m_tileSize.height();
+    if (tilePixelsSize > INT_MAX / 4)
+        CRASH();
+
+    tilePixelsSize = tilePixelsSize * 4;
+    
+    m_tilePixels = adoptArrayPtr(new uint8_t[tilePixelsSize]);
 }
 
 void LayerTilerChromium::reset()
@@ -412,6 +422,9 @@
     int width = (size.width() + m_tileSize.width() - 1) / m_tileSize.width();
     int height = (size.height() + m_tileSize.height() - 1) / m_tileSize.height();
 
+    if (width > INT_MAX / height)
+        CRASH();
+
     Vector<OwnPtr<Tile> > newTiles;
     newTiles.resize(width * height);
     for (int j = 0; j < m_layerTileSize.height(); ++j)

This will trigger a hard crash in release build. I dont know if this is an acceptable approach or do we want a better functional fix which clamps the values and does not crash ?


### in...@chromium.org (2011-02-09)

Adrienne also told me that this might be a dup of existing bug - http://code.google.com/p/chromium/issues/detail?id=69458 (that one does not have a repro). Also, she was planning to take a look at this repro and seeing if solution is ok.


### en...@chromium.org (2011-02-09)

This looks to be different than https://crbug.com/chromium/69458.

Given this bug report, the naive m_tiles data structure is really not going to work long-term.  However, I don't want to risk merging a complex fix that hasn't had time to bake to a stable branch.

I looked into just capping the number of tiles so that Chrome would stop rendering past a boundary rather than crashing.  However, the logic got a little bit thorny and I couldn't convince myself that I'd successfully caught all of the edge cases to prevent this particular crash.

Given that this is a really an edge case and will only happen in extremely unlikely cases where a page has dimensions of millions of pixels in both directions, adding CRASH calls seems like the simplest and most easily testable short-term solution.  I'll file a WebKit bug to replace this array with a better data structure. 

Also, you shouldn't need the check in the reset() function, as the tile size is capped to be the maximum texture size of a graphics card, which is at most 8k.

### in...@chromium.org (2011-02-09)

Awesome! thanks Adrienne. Will fix the resizeLayer issue only. Uploading patch to webkit soon.

### in...@chromium.org (2011-02-09)

Adrienne confirmed that the tiler went in WebKit r74568, so it's not in m9.

Filed webkit bug - https://bugs.webkit.org/show_bug.cgi?id=54132


### in...@chromium.org (2011-02-09)

Fix committed in http://trac.webkit.org/changeset/78143.

Only needs merging to m10.

### in...@chromium.org (2011-02-10)

merged to m10 in r78229. does not need m9 merge.

### sc...@gmail.com (2011-02-23)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-04-19)

@MartyBarbella: thanks for catching this regression before we released it! The report is good quality as usual; this certainly qualifies for a $1000 Chromium Security Reward, congrats!

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

### sc...@gmail.com (2011-05-04)

Invoice finalized; payment is in e-payment system; it can take a couple of weeks.

### js...@chromium.org (2011-10-05)

Batch update.

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

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-05)

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

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/72387?no_tracker_redirect=1

[Multiple monorail components: Blink, Internals>Compositing]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40087738)*
