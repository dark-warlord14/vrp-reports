# WebCore::LayerTilerChromium::invalidateRect() - crash

| Field | Value |
|-------|-------|
| **Issue ID** | [40088873](https://issues.chromium.org/issues/40088873) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | sl...@gmail.com |
| **Assignee** | en...@chromium.org |
| **Created** | 2011-03-14 |
| **Bounty** | $1,000.00 |

## Description

Crashes on: 
    64-bit linux chrome dev [11.0.696.3 (Official Build 77593)]
    64-bit linux chromium dev [11.0.696.3 (Developer Build 77593)]
    32-bit linux chromium dev [11.0.696.3 (Build 77593)]

Doesn't crash on 64-bit chrome stable but shows blue background (looks like some renderer problems).

Repro file:
----- crash1.html -----
<html dir="rtl">
        <table>
                    <th>
                        <del>
                            <samp>AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA</samp>
                        </del>
                        <input></input>
                    </th>
                    <th>
                        <video src="foo"></video>
                        <select autofocus="false"></select>
                    </th>
        </table>
</html>
-----------------------

Program received signal SIGSEGV, Segmentation fault.
[Switching to Thread 0x7fffe1bf7700 (LWP 5976)]
0x00007ffff65295ed in get (this=0x7ffff951ad80, contentRect=<value optimized out>) at third_party/WebKit/Source/JavaScriptCore/wtf/OwnPtr.h:59
59          PtrType get() const { return m_ptr; }

#0  0x00007ffff65295ed in get (this=0x7ffff951ad80, contentRect=<value optimized out>) at third_party/WebKit/Source/JavaScriptCore/wtf/OwnPtr.h:59
#1  WebCore::LayerTilerChromium::invalidateRect (this=0x7ffff951ad80, contentRect=<value optimized out>) at third_party/WebKit/Source/WebCore/platform/graphics/chromium/LayerTilerChromium.cpp:211
#2  0x00007ffff65236f0 in WebCore::LayerRendererChromium::invalidateRootLayerRect (this=0x7ffffbb3f180, dirtyRect=..., visibleRect=..., contentRect=...) at third_party/WebKit/Source/WebCore/platform/graphics/chromium/LayerRendererChromium.cpp:163
#3  0x00007ffff62678a4 in WebKit::WebViewImpl::invalidateRootLayerRect (this=0x7ffff94c0000, rect=...) at third_party/WebKit/Source/WebKit/chromium/src/WebViewImpl.cpp:2297
#4  0x00007ffff626cedd in WebKit::WebViewImpl::setRootGraphicsLayer (this=0x7ffff94c0000, layer=0x7ffffbc17800) at third_party/WebKit/Source/WebKit/chromium/src/WebViewImpl.cpp:2269
#5  0x00007ffff69c2e6b in WebCore::RenderLayerCompositor::attachRootPlatformLayer (this=0x7ffffb7c2c80, attachment=WebCore::RenderLayerCompositor::RootLayerAttachedViaChromeClient) at third_party/WebKit/Source/WebCore/rendering/RenderLayerCompositor.cpp:1482
#6  0x00007ffff69c56bc in WebCore::RenderLayerCompositor::ensureRootPlatformLayer (this=0x7ffffb7c2c80) at third_party/WebKit/Source/WebCore/rendering/RenderLayerCompositor.cpp:1447
#7  0x00007ffff69c58f5 in WebCore::RenderLayerCompositor::enableCompositingMode (this=0x7ffff951adf0, enable=214) at third_party/WebKit/Source/WebCore/rendering/RenderLayerCompositor.cpp:124
#8  0x00007ffff69c59f5 in WebCore::RenderLayerCompositor::updateBacking (this=0x7ffffb7c2c80, layer=0x7ffff92ef120, shouldRepaint=WebCore::RenderLayerCompositor::CompositingChangeRepaintNow) at third_party/WebKit/Source/WebCore/rendering/RenderLayerCompositor.cpp:319
#9  0x00007ffff69c5a96 in WebCore::RenderLayerCompositor::updateLayerCompositingState (this=0x7ffff951adf0, layer=0x1d6, shouldRepaint=4294967295) at third_party/WebKit/Source/WebCore/rendering/RenderLayerCompositor.cpp:389
#10 0x00007ffff69afe12 in WebCore::RenderLayer::contentChanged (this=0x7ffff92ef120, changeType=WebCore::RenderLayer::VideoChanged) at third_party/WebKit/Source/WebCore/rendering/RenderLayer.cpp:237
#11 0x00007ffff6a128f1 in WebCore::RenderVideo::updatePlayer (this=0x7ffff92f1128) at third_party/WebKit/Source/WebCore/rendering/RenderVideo.cpp:241
#12 0x00007ffff62bdf85 in WebCore::HTMLMediaElement::mediaPlayerEngineUpdated (this=0x7ffffaafb000) at third_party/WebKit/Source/WebCore/html/HTMLMediaElement.cpp:1989
#13 0x00007ffff6519940 in WebCore::MediaPlayer::loadWithNextMediaEngine (this=0x7ffffb9021e0, current=<value optimized out>) at third_party/WebKit/Source/WebCore/platform/graphics/MediaPlayer.cpp:358
#14 0x00007ffff6519e51 in WebCore::MediaPlayer::load (this=0x7ffffb9021e0, url=..., contentType=...) at third_party/WebKit/Source/WebCore/platform/graphics/MediaPlayer.cpp:336
#15 0x00007ffff62c1af7 in WebCore::HTMLMediaElement::loadResource (this=0x7ffffaafb000, initialURL=<value optimized out>, contentType=...) at third_party/WebKit/Source/WebCore/html/HTMLMediaElement.cpp:710

rax            0x0  0
rbx            0x7ffff951ad80   140737376267648
rcx            0x1  1
rdx            0xffffffffffffffff   -1
rsi            0x1d6    470
rdi            0x7ffff951adf0   140737376267760
rbp            0xffffffff   0xffffffff
rsp            0x7fffe1bf63c0   0x7fffe1bf63c0
r8             0x100    256
r9             0x7fffe1bf63f0   140736980804592
r10            0x7ffff82b07f0   140737356957680
r11            0x246    582
r12            0x7fffe1bf64c0   140736980804800
r13            0x0  0
r14            0x7fffe1bf63d0   140736980804560
r15            0x7fffe1bf63e0   140736980804576
rip            0x7ffff65295ed   0x7ffff65295ed <WebCore::LayerTilerChromium::invalidateRect(WebCore::IntRect const&)+173>
eflags         0x10246  [ PF ZF IF RF ]
cs             0x33 51
ss             0x2b 43
ds             0x0  0
es             0x0  0
fs             0x0  0
gs             0x0  0


Dump of assembler code for function WebCore::LayerTilerChromium::invalidateRect(WebCore::IntRect const&):
[...]
   0x00007ffff65295d8 <+152>:   mov    0x80(%rbx),%edx
   0x00007ffff65295de <+158>:   mov    0x30(%rbx),%rax
   0x00007ffff65295e2 <+162>:   imul   %r13d,%edx
   0x00007ffff65295e6 <+166>:   lea    0x0(%rbp,%rdx,1),%edx
   0x00007ffff65295ea <+170>:   movslq %edx,%rdx
=> 0x00007ffff65295ed <+173>:   mov    (%rax,%rdx,8),%r12
   0x00007ffff65295f1 <+177>:   test   %r12,%r12
   0x00007ffff65295f4 <+180>:   je     0x7ffff652962c <WebCore::LayerTilerChromium::invalidateRect(WebCore::IntRect const&)+236>


## Attachments

- [crash1.html](attachments/crash1.html) (text/html; charset=us-ascii, 1.2 KB)
- [bt1.txt](attachments/bt1.txt) (text/plain; charset=us-ascii, 12.0 KB)

## Timeline

### in...@chromium.org (2011-03-14)

tileIndex(i, j) is getting negative because i=-1, j=0

We go out of bounds here
void LayerTilerChromium::invalidateRect(const IntRect& contentRect)
{
    if (contentRect.isEmpty())
        return;

    growLayerToContain(contentRect);

    // Dirty rects are always in layer space, as the layer could be repositioned
    // after invalidation.
    IntRect layerRect = contentRectToLayerRect(contentRect);

    int left, top, right, bottom;
    contentRectToTileIndices(contentRect, left, top, right, bottom);
    for (int j = top; j <= bottom; ++j) {
        for (int i = left; i <= right; ++i) {
            Tile* tile = m_tiles[tileIndex(i, j)].get();

Adrienne, can you please take a look.

### en...@chromium.org (2011-03-14)

I'll look into it.  Thanks for the detailed analysis and the repro case.  :)

I want to point out that in ToT this behaves differently, likely due to http://trac.webkit.org/changeset/80767 which hasn't been merged to m11 yet.

Just for reference, the behavior I see on m12 is a very long horizontal page of blue "this hasn't been drawn by the compositor" and then to the right of that, a long stretch of correct background and the text "AAAAAAA...", which is an adequate summation of my feelings towards this bug.

Any fix needs to be tested against m11 and against m12 to make sure that both issues are fixed.

### en...@chromium.org (2011-03-16)

I see the problem.  The tiler code just doesn't handle negative scroll offsets properly, which appears to be how rtl pages are rendered.  We definitely need a test for this.

Sadly, fixing this in m11 will require drovering the fairly invasive http://trac.webkit.org/changeset/80767 as a prerequisite (or disabling hardware acceleration on rtl pages, which is not a great option either).

### in...@chromium.org (2011-03-16)

Thanks Adrienne. So this does not affect m10 ?

Yes, sadly m11 will need this prerequisite and the security fix before jumping to stable :(

### en...@chromium.org (2011-03-16)

I looked at m10, but I do not think there is a security issue there.  There is an infrequent crash (unlike m11, which looks reliable), but it's slightly different.  I built a release build with symbols and it looks like it's a dereference of a NULL pointer (which is always NULL) and segfaults.  It's the same place as the above callstack, but the index is always zero and the buffer is NULL.

I changed the index calculation in m11, which is why the behavior of getting a negative index happens there, but not in m10.

### en...@chromium.org (2011-03-16)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-03-16)

Shuffling this to m11 then. Is there a short term fix for m11 that could revert it back to the null deref crash? I know that's not an appealing solution, but it might be preferable to a dangerous merge.

### ja...@chromium.org (2011-03-16)

That would imply crashing on all RTL pages that trigger the compositor (which in m11 means any page with WebGL, <video> or 3d CSS).

### js...@chromium.org (2011-03-16)

Oh... that's a bad thing, right? :P

### en...@chromium.org (2011-03-17)

The more I look at what needs to change to do this properly, I'm feeling like it's too invasive to merge back and I'd rather let everything bake in ToT for a while.

I think the best low risk fix would be to put a fix into m11 that turns off compositing for RTL pages.  I'll commit this into ToT first and will revert once I fix RTL properly for the compositor.

There are some pages (likely those that don't have overflow scrolling) that don't crash here, so we'd be turning off compositing for them.  However, I am not convinced that we ever rendered RTL pages with accelerated compositing correctly.  A quick test of a non-crashing page (above test, removing the AAAs) doesn't render the video properly, so it seems more likely that we'd be generally improving the quality of RTL pages that triggered the compositor.

### en...@chromium.org (2011-03-17)

See: https://bugs.webkit.org/show_bug.cgi?id=56585

### en...@chromium.org (2011-03-17)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-03-18)

Can an attacker do negative offsets by calling some apis directly, or can negative offsets be invoked through rtl pages only ? Just double checking :)

### en...@chromium.org (2011-03-18)

I don't think so.  The rect that's going negative is the internal "what's the current viewport rectangle to draw the page from" calculation.  There's no Javascript API to modify it directly.

You could also just clamp those values to a minimum of zero as a safety measure, but I think the WebKit fix above is sufficient.

### in...@chromium.org (2011-03-18)

Please do have the clamping in place, as we don't want to leave any door open. Negative array indices does not have any usecase, so better to have unsigned for indices and always check for < size of array. We can do this in a seperate webkit bug if required. 

### en...@chromium.org (2011-03-18)

It would have to be done in a separate bug.  The code's been refactored significantly on trunk to not have this issue, so I think I'd have to land such a clamping change directly on the 696 branch.  (Please correct me if I'm wrong.)

### in...@chromium.org (2011-03-18)

Adrienne, what i meant was we should have the clamping change as a long term measure. If just disabling rtl works for m11, then it is ok for now. I wanted the trunk code to have proper clamping code as such things should not be allowed at all. Let me try understanding your comment, do you mean to say you already have clamps on trunk ?

### en...@chromium.org (2011-03-18)

Ah, ok, I misunderstood what you were asking.  Just to clarify, trunk doesn't have clamping, but that class now uses a hash instead of a vector, so negative indices don't cause invalid memory accesses.

### en...@chromium.org (2011-03-18)

Merged here: http://trac.webkit.org/changeset/81513/branches/chromium/696

Compiled the branch locally and verified that this test case doesn't crash.

### in...@chromium.org (2011-03-18)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-04-15)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-04-19)

@slaweck: nice catch! Thanks for pointing this out during the dev cycle, it's great when we catch these things before releasing to stable.
And to follow on: congrats! This certainly qualifies for a provisional $1000 Chromium Security Reward. Thanks for the small repro along with good dump of stack, registers and asm!

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

### sc...@gmail.com (2011-05-06)

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

This issue was migrated from crbug.com/chromium/76059?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40088873)*
