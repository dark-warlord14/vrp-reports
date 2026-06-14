# Use after free of frame loader in DocumentLoader::commitLoad

| Field | Value |
|-------|-------|
| **Issue ID** | [40088042](https://issues.chromium.org/issues/40088042) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **CVE IDs** | CVE-2011-1291, CVE-2011-1292 |
| **Reporter** | sl...@gmail.com |
| **Assignee** | in...@chromium.org |
| **Created** | 2011-02-16 |
| **Bounty** | $1,000.00 |

## Description

Looks like null ptr deref but I'm not sure and it try to read not null address - for safety I used security template.
Crashes on linux 32-bit stable [9.0.597.98 (74359)] and dev [10.0.648.45 (74092)].

Repro file:
----- crash1.html -----
<script>
    function main(){
        window.document.body['outerHTML'] = 'foo'
    }
    window.onload = main;
</script>
<iframe src="data:application/pdf,foobar">
-----------------------

I tried other mime types but crashes only using 'application/pdf'.

Program received signal SIGSEGV, Segmentation fault.
[Switching to Thread 0xb146eb70 (LWP 6940)]
0x0142b091 in WTF::RefPtr<WebCore::Document>::get (this=0x3966dc8, loader=0x35d2800, data=0xb0c5c000 "foobar", length=6) at third_party/WebKit/Source/JavaScriptCore/wtf/RefPtr.h:60
60          T* get() const { return m_ptr; }

#0  0x0142b091 in WTF::RefPtr<WebCore::Document>::get (this=0x3966dc8, loader=0x35d2800, data=0xb0c5c000 "foobar", length=6) at third_party/WebKit/Source/JavaScriptCore/wtf/RefPtr.h:60
#1  WebCore::Frame::document (this=0x3966dc8, loader=0x35d2800, data=0xb0c5c000 "foobar", length=6) at third_party/WebKit/Source/WebCore/page/Frame.h:298
#2  WebKit::FrameLoaderClientImpl::committedLoad (this=0x3966dc8, loader=0x35d2800, data=0xb0c5c000 "foobar", length=6) at third_party/WebKit/Source/WebKit/chromium/src/FrameLoaderClientImpl.cpp:1072
#3  0x01993940 in WebCore::DocumentLoader::commitLoad (this=0x35d2800, data=0xb0c5c000 "foobar", length=6) at third_party/WebKit/Source/WebCore/loader/DocumentLoader.cpp:295
#4  0x019b3f34 in WebCore::MainResourceLoader::addData (this=0x30db000, data=0xb0c5c000 "foobar", length=6, allAtOnce=<value optimized out>) at third_party/WebKit/Source/WebCore/loader/MainResourceLoader.cpp:157
#5  0x019c56fc in WebCore::ResourceLoader::didReceiveData (this=0x30db000, data=0xb0c5c000 "foobar", length=6, lengthReceived=<value optimized out>, allAtOnce=<value optimized out>) at third_party/WebKit/Source/WebCore/loader/ResourceLoader.cpp:277
#6  0x019b432f in WebCore::MainResourceLoader::didReceiveData (this=0x30db000, data=0xb0c5c000 "foobar", length=6, lengthReceived=0, allAtOnce=false) at third_party/WebKit/Source/WebCore/loader/MainResourceLoader.cpp:442
#7  0x019c4e8c in WebCore::ResourceLoader::didReceiveData (this=0x30db000, data=0xb0c5c000 "foobar", length=6, lengthReceived=6) at third_party/WebKit/Source/WebCore/loader/ResourceLoader.cpp:428
#8  0x01f2427f in WebCore::ResourceHandleInternal::didReceiveData (this=0x36c7240, data=0xb0c5c000 "foobar", dataLength=6) at third_party/WebKit/Source/WebKit/chromium/src/ResourceHandle.cpp:173
#9  0x011a7815 in webkit_glue::WebURLLoaderImpl::Context::OnReceivedData (this=0x37a2ee0, data=0xb0c5c000 "foobar", len=6) at webkit/glue/weburlloader_impl.cc:612
#10 0x01de0c63 in ResourceDispatcher::OnReceivedData (this=0x358ac60, message=..., request_id=24, shm_handle=..., data_len=6) at chrome/common/resource_dispatcher.cc:372
#11 0x01ddffab in IPC::MessageWithTuple<Tuple3<int, base::FileDescriptor, int> >::Dispatch<ResourceDispatcher, ResourceDispatcher, int, base::FileDescriptor, int> (msg=0x39409a0, obj=0x358ac60, sender=0x358ac60, func=0x1de0b90 <ResourceDispatcher::OnReceivedData(IPC::Message const&, int, base::FileDescriptor, int)>) at ./ipc/ipc_message_utils.h:965
#12 0x01de1622 in ResourceDispatcher::DispatchMessage (this=0x358ac60, message=...) at chrome/common/resource_dispatcher.cc:528
#13 0x01de2049 in ResourceDispatcher::OnMessageReceived (this=0x358ac60, message=...) at chrome/common/resource_dispatcher.cc:297
#14 0x01dfaa7f in ChildThread::OnMessageReceived (this=0x3129b44, msg=...) at chrome/common/child_thread.cc:144
[...]

eax            0x0  0
ecx            0x0  0
edx            0x1a4    420
ebx            0x2f5f32c    49673004
esp            0xb146dab0   0xb146dab0
ebp            0xb146db18   0xb146db18
esi            0x3966dc8    60190152
edi            0xb0c5c000   -1329217536
eip            0x142b091    0x142b091 <WebKit::FrameLoaderClientImpl::committedLoad(WebCore::DocumentLoader*, char const*, int)+49>
eflags         0x210282 [ SF IF RF ID ]
cs             0x73 115
ss             0x7b 123
ds             0x7b 123
es             0x7b 123
fs             0x0  0
gs             0x33 51

Dump of assembler code for function _ZN6WebKit21FrameLoaderClientImpl13committedLoadEPN7WebCore14DocumentLoaderEPKci:
   0x0142b060 <+0>:     push   %ebp
   0x0142b061 <+1>:     mov    %esp,%ebp
   0x0142b063 <+3>:     push   %edi
   0x0142b064 <+4>:     push   %esi
   0x0142b065 <+5>:     push   %ebx
   0x0142b066 <+6>:     sub    $0x5c,%esp
   0x0142b069 <+9>:     mov    0x8(%ebp),%esi
   0x0142b06c <+12>:    call   0x2c20f7 <__i686.get_pc_thunk.bx>
   0x0142b071 <+17>:    add    $0x1b342bb,%ebx
   0x0142b077 <+23>:    mov    0x10(%ebp),%edi
   0x0142b07a <+26>:    mov    0xac(%esi),%eax
   0x0142b080 <+32>:    test   %eax,%eax
   0x0142b082 <+34>:    je     0x142b1f8 <_ZN6WebKit21FrameLoaderClientImpl13committedLoadEPN7WebCore14DocumentLoaderEPKci+408>
   0x0142b088 <+40>:    mov    0x4(%esi),%eax
   0x0142b08b <+43>:    mov    0xc4(%eax),%eax
=> 0x0142b091 <+49>:    mov    0x404(%eax),%eax
   0x0142b097 <+55>:    mov    (%eax),%edx
   0x0142b099 <+57>:    mov    %eax,(%esp)
   0x0142b09c <+60>:    call   *0x194(%edx)

(Full backtrace attached - bt1.txt)

## Attachments

- [crash1.html](attachments/crash1.html) (text/plain; charset=us-ascii, 165 B)
- [bt1.txt](attachments/bt1.txt) (text/plain; charset=us-ascii, 10.1 KB)

## Timeline

### in...@chromium.org (2011-02-22)

Tested with on Windows Vista, frameloader's vtables are clearly jacked up and it is deleted.

### in...@chromium.org (2011-02-22)

s/Tested with/Tested with 11.0.677.0 (75388) and also reproduces on M9 stable.

### js...@chromium.org (2011-02-22)

@japhet - Mind taking a peek at this and helping to find an owner?

### in...@chromium.org (2011-02-23)

Another repro that works reliably in dumprendertree as well:::

<html>
<body onload="runTest()">
<script>
    if (window.layoutTestController)
        layoutTestController.dumpAsText();
    
    function runTest()
    {
        document.body['outerHTML'] = 'PASS';
    }   
</script>
<iframe src="data:video/mpeg,foo">
</body>
</html>

Reason::
When iframe src is loading, PluginDocumentParser::appendBytes gets called which in turn calls RawDataDocumentParser::finish, which calls Document::finishParsing, which blows away the frame (and hence the frame loader).

void FrameLoader::finishedParsing()
{
    if (m_stateMachine.creatingInitialEmptyDocument())
        return;

    m_frame->injectUserScripts(InjectAtDocumentEnd);

    // This can be called from the Frame's destructor, in which case we shouldn't protect ourselves
    // because doing so will cause us to re-enter the destructor when protector goes out of scope.
    // Null-checking the FrameView indicates whether or not we're in the destructor.
    RefPtr<Frame> protector = m_frame->view() ? m_frame : 0;

    m_client->dispatchDidFinishDocumentLoad();

    checkCompleted();

    if (!m_frame->view())
        return; // We are being destroyed by something checkCompleted called.


Need to protect the frame in addition to the document loader DocumentLoader::commitLoad. We do protect frame in DocumentLoader::stopLoading as well.

void DocumentLoader::commitLoad(const char* data, int length)
{
    // Both unloading the old page and parsing the new page may execute JavaScript which destroys the datasource
    // by starting a new load, so retain temporarily.
+    RefPtr<Frame> protectFrame(m_frame);
    RefPtr<DocumentLoader> protectLoader(this);

### in...@chromium.org (2011-02-24)

Repro that works on win7 as well.

<html>
<body onload="runTest()">
<script>
    if (window.layoutTestController)
    {
        layoutTestController.dumpAsText();
        layoutTestController.waitUntilDone();
    }
    
    function runTest()
    {
        document.body.innerHTML = 'PASS';
    }

    function finish()
    {
        if (layoutTestController)
            layoutTestController.notifyDone();
    }
    
    setTimeout("finish()", 0);
</script>
<iframe id="test" src="data:video/mpeg,foo"></iframe>
</body>
</html>

### in...@chromium.org (2011-02-24)

for the last repro, make sure to have apple quicktime installed.

### in...@chromium.org (2011-02-24)

my proposed fix is probably wrong as we hit this assert in dumrendertree. Reassigning to Nate.

ASSERTION FAILED: !m_replaceMediaElementTimer.isActive()
/Users/aarya/allwebkit/webkit/Source/WebCore/html/MediaDocument.cpp(126) : virtual WebCore::MediaDocument::~MediaDocument()
1   WebCore::MediaDocument::~MediaDocument()
2   WebCore::Document::selfOnlyDeref()
3   WebCore::Document::removedLastRef()
4   WebCore::TreeShared<WebCore::ContainerNode>::deref()
5   void WTF::derefIfNotNull<WebCore::Document>(WebCore::Document*)
6   WTF::RefPtr<WebCore::Document>::operator=(WTF::PassRefPtr<WebCore::Document> const&)
7   WebCore::Frame::setDocument(WTF::PassRefPtr<WebCore::Document>)
8   WebCore::FrameLoader::clear(bool, bool, bool)
9   WebCore::FrameLoader::cancelAndClear()
10  WebCore::Frame::~Frame()
11  WTF::RefCounted<WebCore::Frame>::deref()
12  void WTF::derefIfNotNull<WebCore::Frame>(WebCore::Frame*)
13  WTF::RefPtr<WebCore::Frame>::~RefPtr()
14  WebCore::FrameView::~FrameView()
15  WTF::RefCounted<WebCore::Widget>::deref()
16  void WTF::derefIfNotNull<WebCore::Widget>(WebCore::Widget*)
17  WTF::RefPtr<WebCore::Widget>::~RefPtr()
18  std::pair<WTF::RefPtr<WebCore::Widget>, WebCore::FrameView*>::~pair()
19  WTF::HashTable<WTF::RefPtr<WebCore::Widget>, std::pair<WTF::RefPtr<WebCore::Widget>, WebCore::FrameView*>, WTF::PairFirstExtractor<std::pair<WTF::RefPtr<WebCore::Widget>, WebCore::FrameView*> >, WTF::PtrHash<WTF::RefPtr<WebCore::Widget> >, WTF::PairHashTraits<WTF::HashTraits<WTF::RefPtr<WebCore::Widget> >, WTF::HashTraits<WebCore::FrameView*> >, WTF::HashTraits<WTF::RefPtr<WebCore::Widget> > >::deallocateTable(std::pair<WTF::RefPtr<WebCore::Widget>, WebCore::FrameView*>*, int)
20  WTF::HashTable<WTF::RefPtr<WebCore::Widget>, std::pair<WTF::RefPtr<WebCore::Widget>, WebCore::FrameView*>, WTF::PairFirstExtractor<std::pair<WTF::RefPtr<WebCore::Widget>, WebCore::FrameView*> >, WTF::PtrHash<WTF::RefPtr<WebCore::Widget> >, WTF::PairHashTraits<WTF::HashTraits<WTF::RefPtr<WebCore::Widget> >, WTF::HashTraits<WebCore::FrameView*> >, WTF::HashTraits<WTF::RefPtr<WebCore::Widget> > >::~HashTable()
21  WTF::HashMap<WTF::RefPtr<WebCore::Widget>, WebCore::FrameView*, WTF::PtrHash<WTF::RefPtr<WebCore::Widget> >, WTF::HashTraits<WTF::RefPtr<WebCore::Widget> >, WTF::HashTraits<WebCore::FrameView*> >::~HashMap()
22  WebCore::RenderWidget::resumeWidgetHierarchyUpdates()
23  WebCore::Element::detach()
24  WebCore::ContainerNode::detach()
25  WebCore::Document::detach()
26  WebCore::Frame::setView(WTF::PassRefPtr<WebCore::FrameView>)
27  WebFrameLoaderClient::transitionToCommittedForNewPage()
28  WebCore::FrameLoader::transitionToCommitted(WTF::PassRefPtr<WebCore::CachedPage>)
29  WebCore::FrameLoader::commitProvisionalLoad()
30  WebCore::DocumentLoader::commitIfReady()
31  WebCore::DocumentLoader::commitLoad(char const*, int)

### ja...@chromium.org (2011-02-24)

This will reproduce in DRT without installing anything extra if you use "application/x-webkit-test-netscape" as the MIME type.

### in...@chromium.org (2011-02-26)

filed webkit bug - https://bugs.webkit.org/show_bug.cgi?id=55289

### in...@chromium.org (2011-02-26)

Committed in http://trac.webkit.org/changeset/79808

### in...@chromium.org (2011-03-01)

a null ptr fixed in http://trac.webkit.org/changeset/79897. (might not affect us probably becoz we have our own plugin logic, but lets still merge it)

### sc...@gmail.com (2011-03-17)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-03-18)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-03-18)

M11 already has this change.
Merged to M10 as http://trac.webkit.org/changeset/81428, http://trac.webkit.org/changeset/81429

### sc...@gmail.com (2011-03-18)

@slaweck -- thanks for another great bug. We should have the fix released to users next week.
And congratulations! Thanks to the high quality of the report (tiny repro, stack trace, register / asm analysis etc). we're happy to reward at the $1000 level.

### sc...@gmail.com (2011-03-18)

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

### sc...@gmail.com (2011-03-18)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-03-30)

Invoice finalized; payment is in e-payment system; it can take a couple of weeks.

### g....@gmail.com (2011-04-08)

This is CVE-2011-1292, and not CVE-2011-1291

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

This issue was migrated from crbug.com/chromium/73216?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40088042)*
