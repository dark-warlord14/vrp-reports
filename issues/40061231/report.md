# UNKNOWN in WebCore::StylePropertySet::addParsedProperties

| Field | Value |
|-------|-------|
| **Issue ID** | [40061231](https://issues.chromium.org/issues/40061231) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | sl...@gmail.com |
| **Assignee** | ds...@chromium.org |
| **Created** | 2012-07-12 |
| **Bounty** | $1,000.00 |

## Description

Crashes on windows dev 22.0.1201.0 (145644) and canary 22.0.1204.0 (146291). 

Repro:
----- crash1.html -----
<html>
  <head>
    <script>
      window.onload = main;
      
      function main() {
        window.document.styleSheets[0].cssRules[0][0].style.color = 0;   
      }
    </script>
    <style>
      @-webkit-keyframes foo {
        1% {color: initial;}
      }
    </style>
  </head>
  <body></body>
</html>
-----------------------

(1290.1538): Access violation - code c0000005 (first chance)
First chance exceptions are reported before any exception handling.
This exception may be expected and handled.
eax=01438fe0 ebx=002fe12c ecx=002fe12c edx=01438fe0 esi=400003e9 edi=002fe234
eip=01817d01 esp=002fe104 ebp=002fe110 iopl=0         nv up ei pl zr na pe nc
cs=001b  ss=0023  ds=0023  es=0023  fs=003b  gs=0000             efl=00010246
chrome_1490000!WebCore::StylePropertySet::addParsedProperties+0xf:
01817d01 8b06            mov     eax,dword ptr [esi]  ds:0023:400003e9=????????

ExceptionAddress: 01817d01 (chrome_1490000!WebCore::StylePropertySet::addParsedProperties+0x0000000f)
   ExceptionCode: c0000005 (Access violation)
  ExceptionFlags: 00000000
NumberParameters: 2
   Parameter[0]: 00000000
   Parameter[1]: 400003e9
Attempt to read from address 400003e9

ChildEBP RetAddr  
002fe110 018170ff chrome_1490000!WebCore::StylePropertySet::addParsedProperties+0xf
002fe138 018164bb chrome_1490000!WebCore::CSSParser::parseValue+0x8d
002febc0 01816377 chrome_1490000!WebCore::CSSParser::parseValue+0x139
002febec 01815feb chrome_1490000!WebCore::StylePropertySet::setProperty+0x9d
002fec10 01815538 chrome_1490000!WebCore::PropertySetCSSStyleDeclaration::setPropertyInternal+0x51
002fec40 0171cf8e chrome_1490000!WebCore::V8CSSStyleDeclaration::namedPropertySetter+0xa9
002fecac 016d4160 chrome_1490000!v8::internal::JSObject::SetPropertyWithInterceptor+0x211
002fed08 016d3c17 chrome_1490000!v8::internal::JSObject::SetPropertyForResult+0x3fa
002fed48 016d32ed chrome_1490000!v8::internal::JSReceiver::SetProperty+0x96
002fed8c 016d2de1 chrome_1490000!v8::internal::StoreIC::Store+0x3a2
002fee7c 016ac0a5 chrome_1490000!v8::internal::StoreIC_Miss+0xc5
002feec4 016abf60 chrome_1490000!v8::internal::Invoke+0x139
002fef04 0172a48e chrome_1490000!v8::internal::Execution::Call+0x17b
002fef58 0181cc78 chrome_1490000!v8::Function::Call+0x117
002fefa4 0181ca23 chrome_1490000!WebCore::V8Proxy::instrumentedCallFunction+0x1ae
002fefc8 0181c159 chrome_1490000!WebCore::V8Proxy::callFunction+0x22
002feff0 0181bf37 chrome_1490000!WebCore::V8EventListener::callListenerFunction+0x86
002ff030 0181ac87 chrome_1490000!WebCore::V8AbstractEventListener::invokeEventHandler+0x109
002ff070 0181aac1 chrome_1490000!WebCore::V8AbstractEventListener::handleEvent+0x76
002ff0a0 015acb40 chrome_1490000!WebCore::EventTarget::fireEventListeners+0x124
002ff0d0 0160aed7 chrome_1490000!WebCore::EventTarget::fireEventListeners+0x73
002ff0f8 018fdadc chrome_1490000!WebCore::DOMWindow::dispatchEvent+0xee
002ff11c 015ebbd0 chrome_1490000!WebCore::DOMWindow::dispatchLoadEvent+0x120
002ff140 015eba97 chrome_1490000!WebCore::Document::implicitClose+0x134
002ff150 015eb8f0 chrome_1490000!WebCore::FrameLoader::checkCallImplicitClose+0x4e
002ff168 015eabd7 chrome_1490000!WebCore::FrameLoader::checkCompleted+0x150
002ff170 015eaa6e chrome_1490000!WebCore::FrameLoader::finishedParsing+0x3d
002ff188 015b0611 chrome_1490000!WebCore::Document::finishedParsing+0xe6
002ff19c 015afdbf chrome_1490000!WebCore::HTMLDocumentParser::prepareToStopParsing+0x133
002ff1a4 015aee8e chrome_1490000!WebCore::HTMLDocumentParser::finish+0x1a
002ff1b0 01596db0 chrome_1490000!WebCore::DocumentWriter::end+0x30
002ff1b8 01774915 chrome_1490000!WebCore::DocumentLoader::finishedLoading+0x74
002ff224 01774887 chrome_1490000!WebCore::MainResourceLoader::didFinishLoading+0x74
002ff234 01774845 chrome_1490000!WebCore::ResourceLoader::didFinishLoading+0x13
002ff248 017747b7 chrome_1490000!WebCore::ResourceHandleInternal::didFinishLoading+0x3d
002ff314 0177413c chrome_1490000!webkit_glue::WebURLLoaderImpl::Context::OnCompletedRequest+0x13f
002ff344 01773e4a chrome_1490000!content::ResourceDispatcher::OnRequestComplete+0x71
002ff3a0 0167c611 chrome_1490000!ResourceMsg_RequestComplete::Dispatch<content::ResourceDispatcher,content::ResourceDispatcher,void (__thiscall content::ResourceDispatcher::*)(int,net::URLRequestStatus const &,std::basic_string<char,std::char_traits<char>,std::allocator<char> > const &,base::TimeTicks const &)>+0x5a
002ff438 0151c692 chrome_1490000!content::ResourceDispatcher::DispatchMessageW+0x83
002ff45c 0151c44e chrome_1490000!content::ResourceDispatcher::OnMessageReceived+0xa8
002ff4c8 014be215 chrome_1490000!ChildThread::OnMessageReceived+0x1a
002ff50c 014b8b31 chrome_1490000!IPC::ChannelProxy::Context::OnDispatchMessage+0xb1
002ff51c 014b94b7 chrome_1490000!base::internal::Invoker<2,base::internal::BindState<base::internal::RunnableAdapter<void (__thiscall quota_internals::QuotaInternalsProxy::*)(std::vector<quota_internals::PerOriginStorageInfo,std::allocator<quota_internals::PerOriginStorageInfo> > const &)>,void __cdecl(quota_internals::QuotaInternalsProxy *,std::vector<quota_internals::PerOriginStorageInfo,std::allocator<quota_internals::PerOriginStorageInfo> > const &),void __cdecl(quota_internals::QuotaInternalsProxy *,std::vector<quota_internals::PerOriginStorageInfo,std::allocator<quota_internals::PerOriginStorageInfo> >)>,void __cdecl(quota_internals::QuotaInternalsProxy *,std::vector<quota_internals::PerOriginStorageInfo,std::allocator<quota_internals::PerOriginStorageInfo> > const &)>::Run+0x16
002ff578 014b8140 chrome_1490000!MessageLoop::RunTask+0x193
002ff6c8 014b82a1 chrome_1490000!MessageLoop::DoWork+0x330
[...]


## Attachments

- [crash1.html](attachments/crash1.html) (text/html; charset=us-ascii, 311 B)
- [stack1.txt](attachments/stack1.txt) (text/x-c++; charset=us-ascii, 12.0 KB)

## Timeline

### in...@chromium.org (2012-07-12)

nice bug. css type confusion.

    union {
        Vector<CSSProperty>* m_mutablePropertyVector;
        void* m_properties;
    };

### in...@chromium.org (2012-07-12)

Upstreamed - https://bugs.webkit.org/show_bug.cgi?id=91153

### in...@chromium.org (2012-07-12)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-07-12)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=76132312

Uploader: inferno@chromium.org

Crash Type: UNKNOWN
Crash Address: 0x0000400003e9
Crash State:
  - crash stack -
  WebCore::StylePropertySet::addParsedProperties
  WebCore::CSSParser::parseValue
  WebCore::CSSParser::parseValue
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=144898:144906

Minimized Testcase (0.23 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv96xX2NezXNpH_AD5vNhmJQL7qMUAahin03syatPB1ii1RbArQHHoEuBz8_BPdzV29evDWugG6Ove6Ew_HtLxyUj2pkBMmJVTN4qVf89q0xGyvmlB2cTiH0l2kf9RARo8TyYJLNIXvh0ilZzhomD8XYNSM1MjCpjO7yZ88CeaIDiIakJqYA
<script>
      window.onload = main;
      
      function main() {
        window.document.styleSheets[0].cssRules[0][0].style.color = 0;   
      }
    </script>
    <style>
      @-webkit-keyframes foo {
        1% {color: initial;}

### ab...@chromium.org (2012-07-16)

[Empty comment from Monorail migration]

### ka...@google.com (2012-07-16)

[Empty comment from Monorail migration]

### ka...@google.com (2012-07-16)

[Empty comment from Monorail migration]

### mi...@chromium.org (2012-07-17)

Doug - can you please take a look at this one.

@inferno - can you please add Doug and I to the WebKit bug?

### in...@chromium.org (2012-07-17)

done!

### ds...@chromium.org (2012-07-17)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-07-18)

http://trac.webkit.org/changeset/122976

### sc...@gmail.com (2012-07-18)

[Empty comment from Monorail migration]

### cl...@chromium.org (2012-07-19)

ClusterFuzz has detected this issue as fixed in range 147361:147371.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=76132312

Uploader: inferno@chromium.org

Crash Type: UNKNOWN
Crash Address: 0x0000400003e9
Crash State:
  - crash stack -
  WebCore::StylePropertySet::addParsedProperties
  WebCore::CSSParser::parseValue
  WebCore::CSSParser::parseValue
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=144898:144906
Fixed: https://cluster-fuzz.appspot.com/revisions?range=147361:147371

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv96xX2NezXNpH_AD5vNhmJQL7qMUAahin03syatPB1ii1RbArQHHoEuBz8_BPdzV29evDWugG6Ove6Ew_HtLxyUj2pkBMmJVTN4qVf89q0xGyvmlB2cTiH0l2kf9RARo8TyYJLNIXvh0ilZzhomD8XYNSM1MjCpjO7yZ88CeaIDiIakJqYA

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### sc...@gmail.com (2012-08-20)

Nice regression catch! $1000 reward.

### sc...@gmail.com (2012-09-12)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-10-14)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-01-18)

Restrict-View-EditIssue is preferred since it allows anyone who can edit an issue (committers and contributors) to view the bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-14)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

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

This issue was migrated from crbug.com/chromium/137125?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061231)*
