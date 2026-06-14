# Crash when webp image is invalid

| Field | Value |
|-------|-------|
| **Issue ID** | [40085478](https://issues.chromium.org/issues/40085478) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals, Internals>Media |
| **Reporter** | sl...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2010-12-01 |
| **Bounty** | $1,000.00 |

## Description

Crashes on linux 32-bit dev [9.0.587.0 (Build 66374)]
I have attached repro file (crash1.html) and webp image (crash.webp).
It doesn't crash instantly. You have to refresh even more than 10 times or more to crash.
In second repro file (crash2.html) I included image in data URI - all in one.
It crashes in few different places.
crash.webp is produced from valid oryginal.webp but some bytes are randomly changed.


Program received signal SIGSEGV, Segmentation fault.
[Switching to Thread 0xb1e5cb70 (LWP 15325)]
0x016fe8eb in WebCore::Private::NodeRemovalDispatcher<WebCore::Node, true>::dispatch (head=@0xb1e5bc9c, tail=@0xb1e5bc98, container=0x38366c0) at third_party/WebKit/WebCore/dom/ContainerNodeAlgorithms.h:99
99                  node->removedFromDocument();

#0  0x016fe8eb in WebCore::Private::NodeRemovalDispatcher<WebCore::Node, true>::dispatch (head=@0xb1e5bc9c, tail=@0xb1e5bc98, container=0x38366c0) at third_party/WebKit/WebCore/dom/ContainerNodeAlgorithms.h:99
#1  WebCore::Private::addChildNodesToDeletionQueue<WebCore::Node, WebCore::ContainerNode> (head=@0xb1e5bc9c, tail=@0xb1e5bc98, container=0x38366c0) at third_party/WebKit/WebCore/dom/ContainerNodeAlgorithms.h:139
#2  0x016fe965 in removeAllChildrenInContainer<WebCore::Node, WebCore::ContainerNode> (this=0x388b400) at third_party/WebKit/WebCore/dom/ContainerNodeAlgorithms.h:62
#3  WebCore::ContainerNode::removeAllChildren (this=0x388b400) at third_party/WebKit/WebCore/dom/ContainerNode.cpp:72
#4  0x017184df in WebCore::Document::removedLastRef (this=0x388b400) at third_party/WebKit/WebCore/dom/Document.cpp:517
#5  0x01a12621 in WebCore::TreeShared<WebCore::ContainerNode>::deref (v8Object=..., domObject=0x388b400) at third_party/WebKit/WebCore/platform/TreeShared.h:78
#6  WebCore::DOMDataStore::weakNodeCallback (v8Object=..., domObject=0x388b400) at third_party/WebKit/WebCore/bindings/v8/DOMDataStore.cpp:166
#7  0x00d58ef7 in v8::internal::GlobalHandles::Node::PostGarbageCollectionProcessing () at v8/src/global-handles.cc:180
#8  v8::internal::GlobalHandles::PostGarbageCollectionProcessing () at v8/src/global-handles.cc:385
#9  0x00d6befe in v8::internal::Heap::PerformGarbageCollection (collector=v8::internal::MARK_COMPACTOR, tracer=0xb1e5be08) at v8/src/heap.cc:763
#10 0x00d6c232 in v8::internal::Heap::CollectGarbage (space=v8::internal::OLD_POINTER_SPACE, collector=v8::internal::MARK_COMPACTOR) at v8/src/heap.cc:494
#11 0x00d6c93b in v8::internal::Heap::CollectGarbage () at v8/src/heap-inl.h:334
#12 v8::internal::Heap::CollectAllGarbage () at v8/src/heap.cc:436
#13 v8::internal::Heap::IdleNotification () at v8/src/heap.cc:3731
#14 0x00e30154 in v8::internal::V8::IdleNotification () at v8/src/v8.cc:204
#15 0x00d17f64 in v8::V8::IdleNotification () at v8/src/api.cc:3283
#16 0x016826f7 in WebCore::V8GCForContextDispose::pseudoIdleTimerFired (this=0x36cf8a0) at third_party/WebKit/WebCore/bindings/v8/V8GCForContextDispose.cpp:69
#17 0x016826b1 in WebCore::Timer<WebCore::V8GCForContextDispose>::fired (this=0x3760060) at third_party/WebKit/WebCore/platform/Timer.h:98
#18 0x016113c1 in WebCore::ThreadTimers::sharedTimerFiredInternal (this=0x353fb80) at third_party/WebKit/WebCore/platform/ThreadTimers.cpp:112
#19 0x016114a5 in WebCore::ThreadTimers::sharedTimerFired () at third_party/WebKit/WebCore/platform/ThreadTimers.cpp:90
#20 0x01079992 in webkit_glue::WebKitClientImpl::DoTimeout (this=0x346a500) at ./webkit/glue/webkitclient_impl.h:68
#21 0x01079ab7 in DispatchToMethod<webkit_glue::WebKitClientImpl, void (webkit_glue::WebKitClientImpl::*)()> (this=0x37409c0) at ./base/tuple.h:537
#22 base::BaseTimer<webkit_glue::WebKitClientImpl, false>::TimerTask::Run (this=0x37409c0) at ./base/timer.h:160
#23 0x009d328b in MessageLoop::RunTask (this=0xb1e5c1dc, task=0x37409c0) at base/message_loop.cc:418
#24 0x009d482e in MessageLoop::DeferOrRunPendingTask (this=0xb1e5c1dc, pending_task=...) at base/message_loop.cc:427
#25 0x009d4a04 in MessageLoop::DoDelayedWork (this=0xb1e5c1dc, next_delayed_work_time=0x33d8db0) at base/message_loop.cc:572
#26 0x009d6b58 in base::MessagePumpDefault::Run (this=0x33d8da0, delegate=0xb1e5c1dc) at base/message_pump_default.cc:27
#27 0x009d3d54 in MessageLoop::RunInternal (this=0xb1e5c1dc) at base/message_loop.cc:266
#28 0x009d3e7d in MessageLoop::RunHandler (this=0x3760060) at base/message_loop.cc:238
#29 MessageLoop::Run (this=0x3760060) at base/message_loop.cc:216
#30 0x009f711d in base::Thread::Run (this=0x33d1180, message_loop=0xb1e5c1dc) at base/thread.cc:140
#31 0x009f772b in base::Thread::ThreadMain (this=0x33d1180) at base/thread.cc:164
#32 0x009e59f1 in ThreadFunc (closure=0x33d1180) at base/platform_thread_posix.cc:39
#33 0xb75db96e in start_thread (arg=0xb1e5cb70) at pthread_create.c:300
#34 0xb714da4e in clone () at ../sysdeps/unix/sysv/linux/i386/clone.S:130

registers:

eax            0x3760060    58064992
ecx            0x8f8f9091   -1886416751
edx            0x94949594   -1802201708
ebx            0x2d8cb10    47762192
esp            0xb1e5bc40   0xb1e5bc40
ebp            0xb1e5bc68   0xb1e5bc68
esi            0x8c8c8c8c   -1936946036
edi            0xb1e5bc98   -1310344040
eip            0x16fe8eb    0x16fe8eb <void WebCore::Private::addChildNodesToDeletionQueue<WebCore::Node, WebCore::ContainerNode>(WebCore::Node*&, WebCore::Node*&, WebCore::ContainerNode*)+107>
eflags         0x210202 [ IF RF ID ]
cs             0x73 115
ss             0x7b 123
ds             0x7b 123
es             0x7b 123
fs             0x0  0
gs             0x33 51

asm instruction:

=> 0x16fe8eb <_ZN7WebCore7Private28addChildNodesToDeletionQueueINS_4NodeENS_13ContainerNodeEEEvRPT_S6_PT0_+107>:    call   *0x130(%edx)

Dump of assembler code for function _ZN7WebCore7Private28addChildNodesToDeletionQueueINS_4NodeENS_13ContainerNodeEEEvRPT_S6_PT0_:
   0x016fe880 <+0>: push   %ebp
   0x016fe881 <+1>: mov    %esp,%ebp
   0x016fe883 <+3>: push   %edi
   0x016fe884 <+4>: push   %esi
   0x016fe885 <+5>: sub    $0x20,%esp
   0x016fe888 <+8>: mov    0x10(%ebp),%ecx
   0x016fe88b <+11>:    mov    0xc(%ebp),%edi
   0x016fe88e <+14>:    mov    0x28(%ecx),%eax
   0x016fe891 <+17>:    test   %eax,%eax
   0x016fe893 <+19>:    je     0x16fe8cb <_ZN7WebCore7Private28addChildNodesToDeletionQueueINS_4NodeENS_13ContainerNodeEEEvRPT_S6_PT0_+75>
   0x016fe895 <+21>:    mov    %ecx,-0xc(%ebp)
   0x016fe898 <+24>:    mov    0x8(%eax),%ecx
   0x016fe89b <+27>:    mov    0x1c(%eax),%esi
   0x016fe89e <+30>:    movl   $0x0,0x18(%eax)
   0x016fe8a5 <+37>:    movl   $0x0,0x1c(%eax)
   0x016fe8ac <+44>:    test   %ecx,%ecx
   0x016fe8ae <+46>:    movl   $0x0,0xc(%eax)
   0x016fe8b5 <+53>:    jne    0x16fe8e0 <_ZN7WebCore7Private28addChildNodesToDeletionQueueINS_4NodeENS_13ContainerNodeEEEvRPT_S6_PT0_+96>
   0x016fe8b7 <+55>:    mov    (%edi),%edx
   0x016fe8b9 <+57>:    test   %edx,%edx
   0x016fe8bb <+59>:    je     0x16fe8f8 <_ZN7WebCore7Private28addChildNodesToDeletionQueueINS_4NodeENS_13ContainerNodeEEEvRPT_S6_PT0_+120>
   0x016fe8bd <+61>:    mov    %eax,0x1c(%edx)
   0x016fe8c0 <+64>:    mov    %eax,(%edi)
   0x016fe8c2 <+66>:    test   %esi,%esi
   0x016fe8c4 <+68>:    mov    %esi,%eax
   0x016fe8c6 <+70>:    jne    0x16fe898 <_ZN7WebCore7Private28addChildNodesToDeletionQueueINS_4NodeENS_13ContainerNodeEEEvRPT_S6_PT0_+24>
   0x016fe8c8 <+72>:    mov    -0xc(%ebp),%ecx
   0x016fe8cb <+75>:    movl   $0x0,0x28(%ecx)
   0x016fe8d2 <+82>:    movl   $0x0,0x2c(%ecx)
   0x016fe8d9 <+89>:    add    $0x20,%esp
   0x016fe8dc <+92>:    pop    %esi
   0x016fe8dd <+93>:    pop    %edi
   0x016fe8de <+94>:    pop    %ebp
   0x016fe8df <+95>:    ret
   0x016fe8e0 <+96>:    testb  $0x8,0x25(%eax)
   0x016fe8e4 <+100>:   je     0x16fe8c2 <_ZN7WebCore7Private28addChildNodesToDeletionQueueINS_4NodeENS_13ContainerNodeEEEvRPT_S6_PT0_+66>
   0x016fe8e6 <+102>:   mov    (%eax),%edx
   0x016fe8e8 <+104>:   mov    %eax,(%esp)
=> 0x016fe8eb <+107>:   call   *0x130(%edx)
   0x016fe8f1 <+113>:   jmp    0x16fe8c2 <_ZN7WebCore7Private28addChildNodesToDeletionQueueINS_4NodeENS_13ContainerNodeEEEvRPT_S6_PT0_+66>
   0x016fe8f3 <+115>:   nop
   0x016fe8f4 <+116>:   lea    0x0(%esi,%eiz,1),%esi
   0x016fe8f8 <+120>:   mov    0x8(%ebp),%edx
   0x016fe8fb <+123>:   mov    %eax,(%edx)
   0x016fe8fd <+125>:   jmp    0x16fe8c0 <_ZN7WebCore7Private28addChildNodesToDeletionQueueINS_4NodeENS_13ContainerNodeEEEvRPT_S6_PT0_+64>

(Full backtrace attached - bt1.txt)

...and second case (crashes when I click 'back' button trying to back to folder listing after open crash1.html):


Program received signal SIGSEGV, Segmentation fault.
[Switching to Thread 0xb1e5cb70 (LWP 15584)]
SLL_Pop (size=784) at third_party/tcmalloc/chromium/src/linked_list.h:56
56    *list = SLL_Next(*list);


#0  SLL_Pop (size=784) at third_party/tcmalloc/chromium/src/linked_list.h:56
#1  tcmalloc::ThreadCache::FreeList::Pop (size=784) at third_party/tcmalloc/chromium/src/thread_cache.h:200
#2  tcmalloc::ThreadCache::Allocate (size=784) at third_party/tcmalloc/chromium/src/thread_cache.h:349
#3  do_malloc (size=784) at third_party/tcmalloc/chromium/src/tcmalloc.cc:985
#4  cpp_alloc (size=784) at third_party/tcmalloc/chromium/src/tcmalloc.cc:1254
#5  do_malloc_or_cpp_alloc (size=784) at third_party/tcmalloc/chromium/src/tcmalloc.cc:923
#6  tc_malloc (size=784) at third_party/tcmalloc/chromium/src/tcmalloc.cc:1377
#7  0x015623ad in WTF::fastMalloc (n=784) at third_party/WebKit/JavaScriptCore/wtf/FastMalloc.cpp:250
#8  0x0171288d in WTF::FastAllocBase::operator new (this=0x35b0900) at third_party/WebKit/JavaScriptCore/wtf/FastAllocBase.h:121
#9  WebCore::Document::createStyleSelector (this=0x35b0900) at third_party/WebKit/WebCore/dom/Document.cpp:1734
#10 0x0173d3cb in WebCore::Document::styleSelector (this=0x380bfc0) at third_party/WebKit/WebCore/dom/Document.h:419
#11 WebCore::Node::styleForRenderer (this=0x380bfc0) at third_party/WebKit/WebCore/dom/Node.cpp:1354
#12 0x01740f92 in WebCore::Node::createRendererIfNeeded (this=0x380bfc0) at third_party/WebKit/WebCore/dom/Node.cpp:1331
#13 0x0172c6dc in WebCore::Element::attach (this=0x380bfc0) at third_party/WebKit/WebCore/dom/Element.cpp:887
#14 0x01397a71 in WebCore::HTMLConstructionSite::attach<WebCore::Element> (this=0x384b9ac, parent=0x35b0900, prpChild=...) at third_party/WebKit/WebCore/html/parser/HTMLConstructionSite.cpp:111
#15 0x013983c2 in WebCore::HTMLConstructionSite::insertHTMLHtmlStartTagBeforeHTML (this=0x384b9ac, token=...) at third_party/WebKit/WebCore/html/parser/HTMLConstructionSite.cpp:173
#16 0x0138fa09 in WebCore::HTMLTreeBuilder::processStartTag (this=0x384b990, token=...) at third_party/WebKit/WebCore/html/parser/HTMLTreeBuilder.cpp:1145
#17 0x01392529 in WebCore::HTMLTreeBuilder::constructTreeFromAtomicToken (this=0x384b990, token=...) at third_party/WebKit/WebCore/html/parser/HTMLTreeBuilder.cpp:451
#18 0x013925b4 in WebCore::HTMLTreeBuilder::constructTreeFromToken (this=0x384b990, rawToken=...) at third_party/WebKit/WebCore/html/parser/HTMLTreeBuilder.cpp:446
#19 0x01377dd5 in WebCore::HTMLDocumentParser::pumpTokenizer (this=0x36a3000, mode=WebCore::HTMLDocumentParser::AllowYield) at third_party/WebKit/WebCore/html/parser/HTMLDocumentParser.cpp:223
#20 0x01378420 in WebCore::HTMLDocumentParser::append (this=0x36a3000, source=...) at third_party/WebKit/WebCore/html/parser/HTMLDocumentParser.cpp:311
#21 0x01704c95 in WebCore::DecodedDataDocumentParser::appendBytes (this=0x36a3000, writer=0x37db9b4, data=0xaf244000 "<!DOCTYPE html>\n\n<html>\n\n<head>\n\n<script>\nfunction addRow(name, url, isdir, size, date_modified) {\n  if (name == \".\")\n    return;\n\n  var root = \"\" + document.location;\n  if (root.substr(-1) !== \"/\")\n "..., length=9186, shouldFlush=false) at third_party/WebKit/WebCore/dom/DecodedDataDocumentParser.cpp:54
#22 0x018563fc in WebCore::DocumentWriter::addData (this=0x37db9b4, str=0xaf244000 "<!DOCTYPE html>\n\n<html>\n\n<head>\n\n<script>\nfunction addRow(name, url, isdir, size, date_modified) {\n  if (name == \".\")\n    return;\n\n  var root = \"\" + document.location;\n  if (root.substr(-1) !== \"/\")\n "..., len=9186, flush=false) at third_party/WebKit/WebCore/loader/DocumentWriter.cpp:200
[...]

registers:

eax            0x150    336
ecx            0x4  4
edx            0x150    336
ebx            0x2d8cb10    47762192
esp            0xb1e5b580   0xb1e5b580
ebp            0xb1e5b5d8   0xb1e5b5d8
esi            0x2e60e00    48631296
edi            0x7f7f7f80   2139062144
eip            0x1e91cdc    0x1e91cdc <tc_malloc+524>
eflags         0x210216 [ PF AF IF RF ID ]
cs             0x73 115
ss             0x7b 123
ds             0x7b 123
es             0x7b 123
fs             0x0  0
gs             0x33 51

asm instruction:

=> 0x1e91cdc <tc_malloc+524>:   mov    (%edi),%edx

(full backtrace attached - bt2.txt)


## Attachments

- [original.webp](attachments/original.webp) (application/octet-stream; charset=binary, 6.1 KB)
- [crash1.html](attachments/crash1.html) (text/html; charset=us-ascii, 109 B)
- [crash2.html](attachments/crash2.html) (text/html; charset=us-ascii, 8.2 KB)
- [bt2.txt](attachments/bt2.txt) (text/plain; charset=us-ascii, 16.8 KB)
- [bt1.txt](attachments/bt1.txt) (text/plain; charset=us-ascii, 11.1 KB)
- [crash.webp](attachments/crash.webp) (application/octet-stream; charset=binary, 6.1 KB)
- [bt3.txt](attachments/bt3.txt) (text/x-c++; charset=utf-8, 46.4 KB)
- [bt2_html.txt](attachments/bt2_html.txt) (text/x-c++; charset=us-ascii, 127.0 KB)
- [bt3_svg.txt](attachments/bt3_svg.txt) (text/x-c++; charset=us-ascii, 115.2 KB)
- [bt4_svg.txt](attachments/bt4_svg.txt) (text/x-c++; charset=us-ascii, 112.0 KB)
- [bt1_svg.txt](attachments/bt1_svg.txt) (text/x-c++; charset=us-ascii, 123.7 KB)
- [bt2_direct.txt](attachments/bt2_direct.txt) (text/x-c++; charset=us-ascii, 139.0 KB)
- [crash2.webp](attachments/crash2.webp) (application/octet-stream; charset=binary, 6.1 KB)
- [bt1_html.txt](attachments/bt1_html.txt) (text/x-c++; charset=utf-8, 147.4 KB)
- [bt1_direct.txt](attachments/bt1_direct.txt) (text/x-c++; charset=us-ascii, 107.2 KB)
- [bt2_svg.txt](attachments/bt2_svg.txt) (text/x-c++; charset=utf-8, 159.9 KB)
- [crash3.webp](attachments/crash3.webp) (application/octet-stream; charset=binary, 11.5 KB)
- [original2.webp](attachments/original2.webp) (application/octet-stream; charset=binary, 11.5 KB)
- [bt4.txt](attachments/bt4.txt) (text/plain; charset=us-ascii, 9.1 KB)
- [original4.webp](attachments/original4.webp) (application/octet-stream; charset=binary, 24.1 KB)
- [crash4.webp](attachments/crash4.webp) (application/octet-stream; charset=binary, 24.4 KB)

## Timeline

### js...@chromium.org (2010-12-02)

I hit several asserts, but I'm not seeing a crash on Windows Vista trunk.

Chris, you said you were taking these. Will you have time, or should I find an owner?

### sl...@gmail.com (2010-12-02)

When I put this crash.webp into <image> in svg, I got this backtrace:

Program received signal SIGSEGV, Segmentation fault.
[Switching to Thread 0xb1e5cb70 (LWP 26762)]
0x01de8d61 in UpscaleOddBgr (cur_y=<value optimized out>, cur_u=<value optimized out>, cur_v=0x3518920 "\206\206\206\206\205\205\205\205\204\204\204\204\204\204\204\204\203\203\203\203\203\203\202\202\201\201\200\200\200\200\200\200\200\200\200\200\200\200\200\200\201\201\201\201\201\201\201\201\201\201\201\201\201\201\201\201\201\201\201\201\201\201\201\201\201\201\201\201\201\202\203\204\204\205\206\207\206\206\206\207\207\205\201\177\213\211\210\210\207\207\206\206\206\206\206\206\206\206\206\206\206\206\206\206\205\205\205\205\223\221\212\211\211\211\212\212\211\210\210\210\207\207\207\207\207\207\207\207\207\207\207\207\207\207\207\207\206\206\206\206\206\207\207\210\207\207\207\207\206\206\206\206\204\205\205\205\206\207\207\207\206\203\207\207\207\206\206\206\205\205\204\204\204\204\204\204\204\204\204\204\177\177\200\200\201\201\202\200\177}~~~~\200\200\203\203\203\203"..., top_u=0x5afffd4 <Address 0x5afffd4 out of bounds>, top_v=0x5af35d8 "\206\206\207\206\206\206\206\206\205\205\204\204\204\204\204\204\203\203\203\203\203\203\202\202\201\201\200\200\200\200\200\200\200\200\200\200\200\200\200\200\201\201\201\201\201\201\201\201\201\201\201\201\201\201\201\201\201\201\201\201\201\201\201\201\201\201\201\201\201\202\203\204\204\205\206\207\210\210\210\207\206\210\214\213\207\206\206\206\206\206\206\206\206\206\206\206\206\206\206\206\206\206\205\205\205\205\204\204\203\203\206\205\205\207\206\205\205\205\206\206\206\206\207\207\207\207\207\207\207\207\207\207\207\207\207\207\206\206\206\206\206\206\206\206\207\207\207\207\206\206\206\203\202\206\206\203\205\210\210\207\204\201zw\204\205\205\205\204\204\204\204\204\204\204\204\204\204\204\204\201\201\202\202\202\202\202\200\177~~~~~\177\200\200\201\202\202"..., len=400, dst=0x39bdfd0 "") at third_party/libwebp/webp.c:123
123 UPSCALE_FUNC(UpscaleOddBgr,   MIX_ODD,  VP8YuvToBgr,  3)

#0  0x01de8d61 in UpscaleOddBgr (cur_y=<value optimized out>, cur_u=<value optimized out>, cur_v=0x3518920 "\206\206\206\206\205\205\205\205\204\204\204\204\204\204\204\204\203\203\203\203\203\203\202\202\201\201\200\200\200\200\200\200\200\200\200\200\200\200\200\200\201\201\201\201\201\201\201\201\201\201\201\201\201\201\201\201\201\201\201\201\201\201\201\201\201\201\201\201\201\202\203\204\204\205\206\207\206\206\206\207\207\205\201\177\213\211\210\210\207\207\206\206\206\206\206\206\206\206\206\206\206\206\206\206\205\205\205\205\223\221\212\211\211\211\212\212\211\210\210\210\207\207\207\207\207\207\207\207\207\207\207\207\207\207\207\207\206\206\206\206\206\207\207\210\207\207\207\207\206\206\206\206\204\205\205\205\206\207\207\207\206\203\207\207\207\206\206\206\205\205\204\204\204\204\204\204\204\204\204\204\177\177\200\200\201\201\202\200\177}~~~~\200\200\203\203\203\203"..., top_u=0x5afffd4 <Address 0x5afffd4 out of bounds>, top_v=0x5af35d8 "\206\206\207\206\206\206\206\206\205\205\204\204\204\204\204\204\203\203\203\203\203\203\202\202\201\201\200\200\200\200\200\200\200\200\200\200\200\200\200\200\201\201\201\201\201\201\201\201\201\201\201\201\201\201\201\201\201\201\201\201\201\201\201\201\201\201\201\201\201\202\203\204\204\205\206\207\210\210\210\207\206\210\214\213\207\206\206\206\206\206\206\206\206\206\206\206\206\206\206\206\206\206\205\205\205\205\204\204\203\203\206\205\205\207\206\205\205\205\206\206\206\206\207\207\207\207\207\207\207\207\207\207\207\207\207\207\206\206\206\206\206\206\206\206\207\207\207\207\206\206\206\203\202\206\206\203\205\210\210\207\204\201zw\204\205\205\205\204\204\204\204\204\204\204\204\204\204\204\204\201\201\202\202\202\202\202\200\177~~~~~\177\200\200\201\202\202"..., len=400, dst=0x39bdfd0 "") at third_party/libwebp/webp.c:123
#1  0x01deabb6 in UpscaleLine (io=0xb1e5a8a0) at third_party/libwebp/webp.c:138
#2  CustomPut (io=0xb1e5a8a0) at third_party/libwebp/webp.c:229
#3  0x01df1146 in VP8FinishRow (dec=0x34b8c00, io=0xb1e5a8a0) at third_party/libwebp/frame.c:249
#4  0x01dece22 in ParseFrame (dec=0x34b8c00, io=0xb1e5a8a0) at third_party/libwebp/vp8.c:545
#5  VP8Decode (dec=0x34b8c00, io=0xb1e5a8a0) at third_party/libwebp/vp8.c:589
#6  0x01dea25e in DecodeInto (mode=<value optimized out>, data=<value optimized out>, data_size=6237, params=0xb1e5a928, output_size=360000, output_u_size=0, output_v_size=0) at third_party/libwebp/webp.c:366#0  0x01de8d61 in UpscaleOddBgr (cur_y=<value optimized out>, cur_u=<value optimized out>, cur_v=0x3518920 "\206\206\206\206\205\205\205\205\204\204\204\204\204\204\204\204\203\203\203\203\203\203\202\202\201\201\200\200\200\200\200\200\200\200\200\200\200\200\200\200\201\201\201\201\201\201\201\201\201\201\201\201\201\201\201\201\201\201\201\201\201\201\201\201\201\201\201\201\201\202\203\204\204\205\206\207\206\206\206\207\207\205\201\177\213\211\210\210\207\207\206\206\206\206\206\206\206\206\206\206\206\206\206\206\205\205\205\205\223\221\212\211\211\211\212\212\211\210\210\210\207\207\207\207\207\207\207\207\207\207\207\207\207\207\207\207\206\206\206\206\206\207\207\210\207\207\207\207\206\206\206\206\204\205\205\205\206\207\207\207\206\203\207\207\207\206\206\206\205\205\204\204\204\204\204\204\204\204\204\204\177\177\200\200\201\201\202\200\177}~~~~\200\200\203\203\203\203"..., top_u=0x5afffd4 <Address 0x5afffd4 out of bounds>, top_v=0x5af35d8 "\206\206\207\206\206\206\206\206\205\205\204\204\204\204\204\204\203\203\203\203\203\203\202\202\201\201\200\200\200\200\200\200\200\200\200\200\200\200\200\200\201\201\201\201\201\201\201\201\201\201\201\201\201\201\201\201\201\201\201\201\201\201\201\201\201\201\201\201\201\202\203\204\204\205\206\207\210\210\210\207\206\210\214\213\207\206\206\206\206\206\206\206\206\206\206\206\206\206\206\206\206\206\205\205\205\205\204\204\203\203\206\205\205\207\206\205\205\205\206\206\206\206\207\207\207\207\207\207\207\207\207\207\207\207\207\207\206\206\206\206\206\206\206\206\207\207\207\207\206\206\206\203\202\206\206\203\205\210\210\207\204\201zw\204\205\205\205\204\204\204\204\204\204\204\204\204\204\204\204\201\201\202\202\202\202\202\200\177~~~~~\177\200\200\201\202\202"..., len=400, dst=0x39bdfd0 "") at third_party/libwebp/webp.c:123
#1  0x01deabb6 in UpscaleLine (io=0xb1e5a8a0) at third_party/libwebp/webp.c:138
#2  CustomPut (io=0xb1e5a8a0) at third_party/libwebp/webp.c:229
#3  0x01df1146 in VP8FinishRow (dec=0x34b8c00, io=0xb1e5a8a0) at third_party/libwebp/frame.c:249
#4  0x01dece22 in ParseFrame (dec=0x34b8c00, io=0xb1e5a8a0) at third_party/libwebp/vp8.c:545
#5  VP8Decode (dec=0x34b8c00, io=0xb1e5a8a0) at third_party/libwebp/vp8.c:589
#6  0x01dea25e in DecodeInto (mode=<value optimized out>, data=<value optimized out>, data_size=6237, params=0xb1e5a928, output_size=360000, output_u_size=0, output_v_size=0) at third_party/libwebp/webp.c:366
#7  0x01dea379 in WebPDecodeBGRInto (data=0x38ce400 "RIFFV\030", data_size=6237, output=0x397f000 "ˌ:ˌ:̍;̍;Ό;Ό;ύ=ύ=ҍ=ҍ=ҍ=ҍ=Ս>Ս>\326\216?\326\216?\326\216?\326\216?\327\217@\327\217@\327\217@\327\217@\327\217@\327\217@ِAِAِAِAِAِAِAِAڑBڑBڑBڑBۑBۑBۑBۑBݑBݑBݑBݑBߐBߐB\341\221D\341\221D\341\221D\341\221D\342\223E\342\223E\342\223E\342\223E\342\223E\342\223E\342\223E\342\223E\342\223E\342\223E\342\223E\342\223E\342\223E\342\223E\342\223E\342\223E", <incomplete sequence \342\223>..., output_size=360000, output_stride=1200) at third_party/libwebp/webp.c:410
#8  0x015ed453 in WebCore::WEBPImageDecoder::decode (this=0x35fd720, onlySize=false) at third_party/WebKit/WebCore/platform/image-decoders/webp/WEBPImageDecoder.cpp:108
#9  0x015ed6ee in WebCore::WEBPImageDecoder::frameBufferAtIndex (this=0x35fd720, index=0) at third_party/WebKit/WebCore/platform/image-decoders/webp/WEBPImageDecoder.cpp:67
#10 0x015dd667 in WebCore::ImageSource::createFrameAtIndex (this=0x5af9be0, index=0) at third_party/WebKit/WebCore/platform/graphics/ImageSource.cpp:132
#11 0x0159cdc2 in WebCore::BitmapImage::cacheFrame (this=0x5af9bd0, index=0) at third_party/WebKit/WebCore/platform/graphics/BitmapImage.cpp:121
#12 0x0159d2c6 in WebCore::BitmapImage::frameAtIndex (this=0x5af9bd0, index=0) at third_party/WebKit/WebCore/platform/graphics/BitmapImage.cpp:213
#13 0x0159d318 in WebCore::BitmapImage::nativeImageForCurrentFrame (this=0x5af9bd0) at third_party/WebKit/WebCore/platform/graphics/BitmapImage.h:156
#14 0x015933d8 in WebCore::BitmapImage::draw (this=0x5af9bd0, ctxt=0xb1e5bd28, dstRect=@0xb1e5ac40, srcRect=@0xb1e5ac30, colorSpace=WebCore::ColorSpaceDeviceRGB, compositeOp=WebCore::CompositeSourceOver) at third_party/WebKit/WebCore/platform/graphics/skia/ImageSkia.cpp:450
#15 0x015a9f70 in WebCore::GraphicsContext::drawImage (this=0xb1e5bd28, image=0x5af9bd0, styleColorSpace=WebCore::ColorSpaceDeviceRGB, dest=@0xb1e5ad80, src=@0xb1e5ad70, op=WebCore::CompositeSourceOver, useLowQualityScale=false) at third_party/WebKit/WebCore/platform/graphics/GraphicsContext.cpp:413
#16 0x01e48d7e in WebCore::RenderSVGImage::paint (this=0x2e92510, paintInfo=@0xb1e5ade8) at third_party/WebKit/WebCore/rendering/RenderSVGImage.cpp:133
#17 0x0192e76d in WebCore::RenderBox::paint (this=0x2e9244c, paintInfo=@0xb1e5aed0, tx=<value optimized out>, ty=0) at third_party/WebKit/WebCore/rendering/RenderBox.cpp:733
#18 0x01b457d2 in WebCore::RenderSVGRoot::paint (this=0x2e9244c, paintInfo=@0xb1e5af70, parentX=8, parentY=8) at third_party/WebKit/WebCore/rendering/RenderSVGRoot.cpp:184
#19 0x018f5ea4 in WebCore::InlineBox::paint (this=0x2e925e0, paintInfo=@0xb1e5aff4, tx=8, ty=8) at third_party/WebKit/WebCore/rendering/InlineBox.cpp:184
#20 0x018fa277 in WebCore::InlineFlowBox::paint (this=0x2e92604, paintInfo=@0xb1e5b0fc, tx=8, ty=8) at third_party/WebKit/WebCore/rendering/InlineFlowBox.cpp:749
#21 0x019c6a80 in WebCore::RootInlineBox::paint (this=0x2e92604, paintInfo=@0xb1e5b0fc, tx=8, ty=8) at third_party/WebKit/WebCore/rendering/RootInlineBox.cpp:178
#22 0x0196ff7f in WebCore::RenderLineBoxList::paint (this=0x2e92440, renderer=0x2e923d8, paintInfo=@0xb1e5b2e0, tx=8, ty=8) at third_party/WebKit/WebCore/rendering/RenderLineBoxList.cpp:256
#23 0x0190a943 in WebCore::RenderBlock::paintContents (this=0x2e923d8, paintInfo=@0xb1e5b2e0, tx=8, ty=8) at third_party/WebKit/WebCore/rendering/RenderBlock.cpp:2224
#24 0x0191a995 in WebCore::RenderBlock::paintObject (this=0x2e923d8, paintInfo=@0xb1e5b2e0, tx=8, ty=8) at third_party/WebKit/WebCore/rendering/RenderBlock.cpp:2334
[...]

registers:

eax            0x5af35d8    95368664
ecx            0x86 134
edx            0x5afffd4    95420372
ebx            0x2d8cb10    47762192
esp            0xb1e5a5f8   0xb1e5a5f8
ebp            0xb1e5a638   0xb1e5a638
esi            0x3517fc0    55672768
edi            0x86 134
eip            0x1de8d61    0x1de8d61 <UpscaleOddBgr+33 at third_party/libwebp/webp.c:123>
eflags         0x210282 [ SF IF RF ID ]
cs             0x73 115
ss             0x7b 123
ds             0x7b 123
es             0x7b 123
fs             0x0  0
gs             0x33 51

asm:

=> 0x1de8d61 <UpscaleOddBgr+33 at third_party/libwebp/webp.c:123>:  movzbl (%edx),%eax

(Full backtrace attached - bt3.txt)

### sc...@gmail.com (2010-12-02)

Yeah, I'll get this fixed before it hits M9 stable ;-)

### js...@chromium.org (2010-12-03)

Adding labels and marking as high severity for now.

### sl...@gmail.com (2010-12-05)

Another invalid webp image (crash2.webp).
There is only one byte different than original.webp.

$ diff original.webp.hexdmp crash2.webp.hexdmp
336c336
< 000014f0  ff 05 35 2e 20 11 79 d1  b2 b4 c4 b2 7e 43 3f 62  |..5. .y.....~C?b|
---
> 000014f0  ff 05 94 2e 20 11 79 d1  b2 b4 c4 b2 7e 43 3f 62  |.... .y.....~C?b|

This file should help to analyze.

...and few backtraces: bt[1-4]_svg.txt - crash2.webp included in svg <image>, bt[1-2]_html.txt - in html <img>, bt[1-2]_direct.txt - image opened directly in browser.


### sl...@gmail.com (2010-12-05)

I just tested it on 10.0.603.0 (68315) and still crashes (linux 32-bit). Maybe it's only linux related if it doesn't crash on windows?

### sl...@gmail.com (2010-12-10)

I found another sample of webp image (crash3.webp). This one crashes instantly, everytime and allways in the same way.
It's produced from original2.webp.

Differences between images:

$ diff original2.webp.hexdmp crash3.webp.hexdmp
14c14
< 000000d0  de fe 00 bf 30 bc b3 3c  40 bd 1b d8 23 fa 37 f7  |....0..<@...#.7.|
---
> 000000d0  de fe 00 bf 30 bc b3 3c  d7 32 ea 3e 34 6b e3 31  |....0..<.2.>4k.1|


Program received signal SIGSEGV, Segmentation fault.
WebCore::WEBPImageDecoder::decode (this=Cannot access memory at address 0xffda7690
) at third_party/WebKit/WebCore/platform/image-decoders/webp/WEBPImageDecoder.cpp:111
111     for (int y = 0; y < height; ++y) {


registers:

eax            0x39bc000    60538880
ecx            0x4  4
edx            0x1c8    456
ebx            0x2ddaa08    48081416
esp            0xb1e47600   0xb1e47600
ebp            0xffda7688   0xffda7688
esi            0x357b000    56078336
edi            0x2e28   11816
eip            0x1622d0b    0x1622d0b <WebCore::WEBPImageDecoder::decode(bool)+283>
eflags         0x210206 [ PF IF RF ID ]
cs             0x73 115
ss             0x7b 123
ds             0x7b 123
es             0x7b 123
fs             0x0  0
gs             0x33 51

#0  WebCore::WEBPImageDecoder::decode (this=Cannot access memory at address 0xffda7690
) at third_party/WebKit/WebCore/platform/image-decoders/webp/WEBPImageDecoder.cpp:111
Cannot access memory at address 0xffda768c

After crash EBP allways is set to the same value: 0xffda7688

To reproduce just open crash3.webp directly in browser.

### sc...@gmail.com (2010-12-10)

Thanks, we have a few webp bugs pending -- I'll look at them next week.

### sl...@gmail.com (2010-12-15)

Due to false crashes on chromium builds taken from https://launchpad.net/~chromium-daily/+archive/dev/+packages (look at https://crbug.com/chromium/66870) I checked again those repro files.
crash3.webp doesn't crash on Google Chrome (9.0.597.19).
I apologies for confusion.

### sc...@gmail.com (2010-12-17)

crash3.webp seems to trigger https://crbug.com/chromium/65299 (cc:ed you)

Looking at the others now.

### sc...@gmail.com (2010-12-18)

Aha! Got it I think. This is indeed SecSeverity-High and a great bug.

### sc...@gmail.com (2010-12-20)

Fixed at CL 18705458 in the internal repository. Still need to do all the merge fun.

### sc...@gmail.com (2010-12-20)

[Empty comment from Monorail migration]

### sc...@gmail.com (2010-12-20)

[Empty comment from Monorail migration]

### sc...@gmail.com (2010-12-20)

@slaweck: congratulations! This bug provisionally qualifies for a $1000 Chromium Security Reward.
We are rewarding above the base $500 amount for the following reasons:
- A nice variety of test cases.
- Inclusion of stack traces and asm/register analysis.
- Extra helpfulness such as binary diffs of images :)

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

### sl...@gmail.com (2010-12-20)

Great. Thank You! :)

### bu...@chromium.org (2010-12-21)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=69824

------------------------------------------------------------------------
r69824 | cevans@chromium.org | Tue Dec 21 05:52:27 PST 2010

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/src/third_party/libwebp/README.chromium?r1=69824&r2=69823&pathrev=69824
 M http://src.chromium.org/viewvc/chrome/trunk/src/third_party/libwebp/dsp.c?r1=69824&r2=69823&pathrev=69824
 M http://src.chromium.org/viewvc/chrome/trunk/src/third_party/libwebp/bits.h?r1=69824&r2=69823&pathrev=69824
 M http://src.chromium.org/viewvc/chrome/trunk/src/third_party/libwebp/webp.c?r1=69824&r2=69823&pathrev=69824
 M http://src.chromium.org/viewvc/chrome/trunk/src/third_party/libwebp/tree.c?r1=69824&r2=69823&pathrev=69824
 M http://src.chromium.org/viewvc/chrome/trunk/src/third_party/libwebp/vp8i.h?r1=69824&r2=69823&pathrev=69824
 M http://src.chromium.org/viewvc/chrome/trunk/src/third_party/libwebp/frame.c?r1=69824&r2=69823&pathrev=69824
 M http://src.chromium.org/viewvc/chrome/trunk/src/third_party/libwebp/vp8.c?r1=69824&r2=69823&pathrev=69824
 M http://src.chromium.org/viewvc/chrome/trunk/src/third_party/libwebp/bits.c?r1=69824&r2=69823&pathrev=69824

Update libwebp from upstream repository.
Start to track an accurate lineage in README.chromium.

BUG=62276,64945,65299
TEST=added upstream

Review URL: http://codereview.chromium.org/6013003
------------------------------------------------------------------------

### bu...@chromium.org (2010-12-21)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=69826

------------------------------------------------------------------------
r69826 | cevans@chromium.org | Tue Dec 21 06:57:20 PST 2010

Changed paths:
 M http://src.chromium.org/viewvc/chrome/branches/597/src/third_party/libwebp/dsp.c?r1=69826&r2=69825&pathrev=69826
 M http://src.chromium.org/viewvc/chrome/branches/597/src/third_party/libwebp/README.chromium?r1=69826&r2=69825&pathrev=69826
 M http://src.chromium.org/viewvc/chrome/branches/597/src/third_party/libwebp/bits.c?r1=69826&r2=69825&pathrev=69826
 M http://src.chromium.org/viewvc/chrome/branches/597/src/third_party/libwebp/bits.h?r1=69826&r2=69825&pathrev=69826
 M http://src.chromium.org/viewvc/chrome/branches/597/src/third_party/libwebp/webp.c?r1=69826&r2=69825&pathrev=69826
 M http://src.chromium.org/viewvc/chrome/branches/597/src/third_party/libwebp/tree.c?r1=69826&r2=69825&pathrev=69826
 M http://src.chromium.org/viewvc/chrome/branches/597/src/third_party/libwebp/vp8i.h?r1=69826&r2=69825&pathrev=69826
 M http://src.chromium.org/viewvc/chrome/branches/597/src/third_party/libwebp/frame.c?r1=69826&r2=69825&pathrev=69826
 M http://src.chromium.org/viewvc/chrome/branches/597/src/third_party/libwebp/vp8.c?r1=69826&r2=69825&pathrev=69826

Merge 69824 - Update libwebp from upstream repository.
Start to track an accurate lineage in README.chromium.

BUG=62276,64945,65299
TEST=added upstream

Review URL: http://codereview.chromium.org/6013003

TBR=cdn@chromium.org
Review URL: http://codereview.chromium.org/6002004
------------------------------------------------------------------------

### sc...@gmail.com (2010-12-21)

Fix will be in the next Beta version.

### sl...@gmail.com (2010-12-29)

There are still crashes on linux 32-bit 10.0.619.0 (Build 69830). This time instant OOM.

(I haven't debug symbols for this build)

Program received signal SIGABRT, Aborted.
[Switching to Thread 0xb31d4b70 (LWP 27882)]
0x0012d422 in __kernel_vsyscall ()
#0  0x0012d422 in __kernel_vsyscall ()
#1  0x00f41651 in *__GI_raise (sig=6) at ../nptl/sysdeps/unix/sysv/linux/raise.c:64
#2  0x00f44a82 in *__GI_abort () at abort.c:92
#3  0x088bd731 in base::debug::BreakDebugger() ()
#4  0x088cd6f0 in logging::LogMessage::~LogMessage() ()
#5  0x088e6cc2 in base::(anonymous namespace)::OnNoMemory() ()
#6  0x088a5eaf in (anonymous namespace)::cpp_alloc(unsigned int, bool) ()
#7  0x0ad16d7f in tc_malloc ()
#8  0x094e7e98 in WTF::fastMalloc(unsigned int) ()
#9  0x09569f98 in WTF::Vector<unsigned char, 0u>::reserveCapacity(unsigned int) ()
#10 0x0956a018 in WTF::Vector<unsigned char, 0u>::expandCapacity(unsigned int) ()
#11 0x09579055 in WebCore::WEBPImageDecoder::decode(bool) ()
#12 0x0957923c in WebCore::WEBPImageDecoder::frameBufferAtIndex(unsigned int) ()
#13 0x0956b48d in WebCore::ImageSource::createFrameAtIndex(unsigned int) ()
#14 0x09522412 in WebCore::BitmapImage::cacheFrame(unsigned int) ()
#15 0x095228b5 in WebCore::BitmapImage::frameAtIndex(unsigned int) ()
#16 0x095228e0 in WebCore::BitmapImage::nativeImageForCurrentFrame() ()
#17 0x0951938b in WebCore::BitmapImage::draw(WebCore::GraphicsContext*, WebCore::FloatRect const&, WebCore::FloatRect const&, WebCore::ColorSpace, WebCore::CompositeOperator) ()
#18 0x0953181f in WebCore::GraphicsContext::drawImage(WebCore::Image*, WebCore::ColorSpace, WebCore::FloatRect const&, WebCore::FloatRect const&, WebCore::CompositeOperator, bool) ()
[...]



### sc...@gmail.com (2010-12-30)

Thanks for the update! It's usually better to file new bugs for new discoveries like this.

There are many ways a page can cause the tab to go OOM, and these are not considered to be browser security issues. (This is particularly the case with Chrome, which has better tab isolation than many other browsers. OOM in one tab won't necessarily take down the whole browser).

Your specific test case is causing a large allocation in WEBPImageDecoder.cpp:
    Vector<uint8_t> rgb;
    rgb.resize(height * stride);

Where height*stride == 283843872 or ~283MB.

Note that the max size here for a WEBP is 16383 * 16383 * 3, or about 800MB. As you can see, the restricted dimension size of a WEBP makes sure that no integer overflow can occur in that multiplication, so again no security impact.

### sc...@gmail.com (2011-01-12)

Invoice finalized; payment is in e-payment system.

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-10-05)

Batch update: Guessing based on search criteria that this security bug impacted a stable release.

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/64945?no_tracker_redirect=1

[Multiple monorail components: Internals, Internals>Media]
[Monorail mergedwith: crbug.com/chromium/66591]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40085478)*
