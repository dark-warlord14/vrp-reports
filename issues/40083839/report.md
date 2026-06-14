# Heap-use-after-free in FXJS_GetPrivate 

| Field | Value |
|-------|-------|
| **Issue ID** | [40083839](https://issues.chromium.org/issues/40083839) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Reporter** | ch...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2016-03-11 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

Some javascript objects created by one PDF file in an iframe is freed when another PDF file in an iframe is removed.

## Related change-set

<https://pdfium.googlesource.com/pdfium/+/61dc96f9aa2512807b62cfaec35b1cd012459a6f>

**VERSION**  

Chrome Version: [51.0.2674.0 (64-bit)] + [TOT]  

[50.0.2661.26 (64-bit)] + [beta]

Operating System: [Ubuntu Linux 14.04]

**REPRODUCTION CASE**

1. Download and save test.html, a.pdf and b.pdf to same folder.
2. Open chrome built with Address Sanitizer.
3. Open test.html.
4. Wait for about 25 seconds.
5. PDF plugin process will crash.

Please open b.pdf file in a PDF editor and view Document JavaScript section to view JavaScript of PDF file.

Type of crash: [PDF plugin process]

Crash State: [Address Sanitizer output]  

==4265==ERROR: AddressSanitizer: heap-use-after-free on address 0x6020000068d8 at pc 0x5589b17519c5 bp 0x7ffdcb3ae590 sp 0x7ffdcb3ae588

READ of size 8 at 0x6020000068d8 thread T0 (chrome)  

#0 0x5589b17519c4 in FXJS\_GetPrivate third\_party/pdfium/fpdfsdk/src/jsapi/fxjs\_v8.cpp:566:43  

#1 0x5589b17c3ddd in JSPropGetter<Icon, &Icon::name> third\_party/pdfium/fpdfsdk/src/javascript/JS\_Define.h:88:37  

#2 0x5589a9231fc8 in Call v8/src/api-arguments.cc:75:1  

#3 0x5589a8bd9d0b in GetPropertyWithAccessor v8/src/objects.cc:1062:35  

#4 0x5589a8bd6a0c in GetProperty v8/src/objects.cc:734:16  

#5 0x5589a8b083d1 in Load v8/src/ic/ic.cc:715:5  

#6 0x5589a8b1ff80 in \_\_RT\_impl\_Runtime\_LoadIC\_Miss v8/src/ic/ic.cc:2246:5  

#7 0x5589a8b1ff80 in Runtime\_LoadIC\_Miss v8/src/ic/ic.cc:2227:0  

#7 0x7f90f0306186 (<unknown module>)  

#8 0x7f90f03411bb (<unknown module>)  

#9 0x7f90f0337ae2 (<unknown module>)  

#10 0x7f90f03257ee (<unknown module>)  

#8 0x5589a897a4d2 in Invoke v8/src/execution.cc:97:13  

#9 0x5589a8979b9b in Call v8/src/execution.cc:163:10  

#10 0x5589a83d77fe in Run v8/src/api.cc:1720:23  

#11 0x5589b1750ef1 in FXJS\_Execute third\_party/pdfium/fpdfsdk/src/jsapi/fxjs\_v8.cpp:439:8  

#12 0x5589b16fbbd4 in ?? third\_party/pdfium/fpdfsdk/src/javascript/JS\_Runtime.cpp:240:14  

#13 0x5589b17c4a9a in RunScript third\_party/pdfium/fpdfsdk/src/javascript/JS\_Context.cpp:60:12  

#14 0x5589b171c011 in RunJsScript third\_party/pdfium/fpdfsdk/src/javascript/app.cpp:546:5  

#15 0x5589b171c011 in TimerProc third\_party/pdfium/fpdfsdk/src/javascript/app.cpp:534:0  

#16 0x5589b17ce119 in TimerProc third\_party/pdfium/fpdfsdk/src/javascript/JS\_Object.cpp:145:9  

#17 0x5589a5c1de5f in OnCallback pdf/pdfium/pdfium\_engine.cc:2285:3  

#18 0x5589a5c65259 in operator() ppapi/utility/completion\_callback\_factory.h:607:9  

#19 0x5589a5c65259 in Thunk ppapi/utility/completion\_callback\_factory.h:584:0  

#20 0x5589b0004015 in PP\_RunCompletionCallback ppapi/c/pp\_completion\_callback.h:240:3  

#21 0x5589b0004015 in CallWhileUnlocked<void, PP\_CompletionCallback \*, int, PP\_CompletionCallback \*, int> ppapi/shared\_impl/proxy\_lock.h:135:0  

#22 0x5589b0004015 in CallbackWrapper ppapi/proxy/ppb\_core\_proxy.cc:52:0  

#23 0x5589b00044df in Run<const PP\_CompletionCallback &, const int &> base/bind\_internal.h:159:12  

#24 0x5589b00044df in MakeItSo<const PP\_CompletionCallback &, const int &> base/bind\_internal.h:301:0  

#25 0x5589b00044df in Run base/bind\_internal.h:352:0  

#26 0x5589ad0b72a7 in Run base/callback.h:397:12  

#27 0x5589ad0b72a7 in CallWhileLocked ppapi/shared\_impl/proxy\_lock.h:199:0  

#28 0x5589ad0b74de in Run<std::\_\_1::unique\_ptr<ppapi::internal::RunWhileLockedHelper<void ()>, std::\_\_1::default\_delete<ppapi::internal::RunWhileLockedHelper<void ()> > > > base/bind\_internal.h:159:12  

#29 0x5589ad0b74de in MakeItSo<std::\_\_1::unique\_ptr<ppapi::internal::RunWhileLockedHelper<void ()>, std::\_\_1::default\_delete<ppapi::internal::RunWhileLockedHelper<void ()> > > > base/bind\_internal.h:301:0  

#30 0x5589ad0b74de in Run base/bind\_internal.h:352:0  

#31 0x5589a5de0814 in Run base/callback.h:397:12  

#32 0x5589a5de0814 in RunTask base/debug/task\_annotator.cc:51:0  

#33 0x5589a5ce9bd9 in RunTask base/message\_loop/message\_loop.cc:476:3  

#34 0x5589a5cea695 in DeferOrRunPendingTask base/message\_loop/message\_loop.cc:485:5  

#35 0x5589a5ceb58e in DoDelayedWork base/message\_loop/message\_loop.cc:635:10  

#36 0x5589a5cf1af4 in Run base/message\_loop/message\_pump\_default.cc:37:17  

#37 0x5589a5d31b95 in Run base/run\_loop.cc:35:3  

#38 0x5589a5ce831e in ?? base/message\_loop/message\_loop.cc:293:3  

#39 0x5589b1b2c63d in PpapiPluginMain content/ppapi\_plugin/ppapi\_plugin\_main.cc:160:3  

#40 0x5589a5bf6fae in RunZygote content/app/content\_main\_runner.cc:316:14  

#41 0x5589a5bf9a6d in Run content/app/content\_main\_runner.cc:766:12  

#42 0x5589a5bf62ba in ContentMain content/app/content\_main.cc:19:15  

#43 0x5589a5014a85 in ChromeMain chrome/app/chrome\_main.cc:84:12  

#44 0x7f911c6cfec4 in \_\_libc\_start\_main /build/eglibc-3GlaMS/eglibc-2.19/csu/libc-start.c:287:0

0x6020000068d8 is located 8 bytes inside of 16-byte region [0x6020000068d0,0x6020000068e0)  

freed by thread T0 (chrome) here:  

#0 0x5589a5012e7b in operator delete(void\*) ??:?  

#1 0x5589b174cf6e in FXJS\_FreePrivate third\_party/pdfium/fpdfsdk/src/jsapi/fxjs\_v8.cpp:570:3  

#2 0x5589b174cf6e in FXJS\_FreePrivate third\_party/pdfium/fpdfsdk/src/jsapi/fxjs\_v8.cpp:576:0  

#3 0x5589b174cf6e in Dispose third\_party/pdfium/fpdfsdk/src/jsapi/fxjs\_v8.cpp:145:0  

#4 0x5589b1752d89 in Clear v8/include/v8-util.h:227:9  

#5 0x5589b175036f in ~PersistentValueMapBase v8/include/v8-util.h:292:31  

#6 0x5589b175036f in ~V8TemplateMap third\_party/pdfium/fpdfsdk/include/jsapi/fxjs\_v8.h:80:0  

#7 0x5589b175036f in ReleaseDynamicObjsMap third\_party/pdfium/fpdfsdk/include/jsapi/fxjs\_v8.h:103:0  

#8 0x5589b175036f in FXJS\_ReleaseRuntime third\_party/pdfium/fpdfsdk/src/jsapi/fxjs\_v8.cpp:374:0  

#9 0x5589b16fb1a7 in ~CJS\_Runtime third\_party/pdfium/fpdfsdk/src/javascript/JS\_Runtime.cpp:125:3  

#10 0x5589b16fb4ad in ?? third\_party/pdfium/fpdfsdk/src/javascript/JS\_Runtime.cpp:116:29  

#11 0x5589b1284761 in operator() buildtools/third\_party/libc++/trunk/include/memory:2529:13  

#12 0x5589b1284761 in reset buildtools/third\_party/libc++/trunk/include/memory:2735:0  

#13 0x5589b1284761 in ~unique\_ptr buildtools/third\_party/libc++/trunk/include/memory:2703:0  

#14 0x5589b1284761 in ~CPDFDoc\_Environment third\_party/pdfium/fpdfsdk/src/fsdk\_mgr.cpp:232:0  

#15 0x5589b12423b2 in FPDFDOC\_ExitFormFillEnvironment third\_party/pdfium/fpdfsdk/src/fpdfformfill.cpp:179:3  

#16 0x5589a5c01824 in ~PDFiumEngine pdf/pdfium/pdfium\_engine.cc:644:5  

#17 0x5589a5c0212d in ?? pdf/pdfium/pdfium\_engine.cc:631:31  

#18 0x5589a5c4df21 in operator() buildtools/third\_party/libc++/trunk/include/memory:2529:13  

#19 0x5589a5c4df21 in reset buildtools/third\_party/libc++/trunk/include/memory:2735:0  

#20 0x5589a5c4df21 in ~OutOfProcessInstance pdf/out\_of\_process\_instance.cc:309:0  

#21 0x5589a5c4e6dd in ?? pdf/out\_of\_process\_instance.cc:305:47  

#22 0x5589b3cab20a in CallWhileUnlocked<void, int, int> ppapi/shared\_impl/proxy\_lock.h:128:10  

#23 0x5589b3cab20a in DidDestroy ppapi/shared\_impl/ppp\_instance\_combined.cc:53:0  

#24 0x5589b0058dcb in OnPluginMsgDidDestroy ppapi/proxy/ppp\_instance\_proxy.cc:194:3  

#25 0x5589b0058dcb in DispatchToMethodImpl<ppapi::proxy::PPP\_Instance\_Proxy \*, void (ppapi::proxy::PPP\_Instance\_Proxy::\*)(int), int, 0> base/tuple.h:204:0  

#26 0x5589b0058dcb in DispatchToMethod<ppapi::proxy::PPP\_Instance\_Proxy \*, void (ppapi::proxy::PPP\_Instance\_Proxy::\*)(int), int> base/tuple.h:212:0  

#27 0x5589b0058dcb in Dispatch<ppapi::proxy::PPP\_Instance\_Proxy, ppapi::proxy::PPP\_Instance\_Proxy, void, void (ppapi::proxy::PPP\_Instance\_Proxy::\*)(int)> ipc/ipc\_message\_templates.h:170:0  

#28 0x5589b0058dcb in OnMessageReceived ppapi/proxy/ppp\_instance\_proxy.cc:146:0  

#29 0x5589affb8e96 in OnMessageReceived ppapi/proxy/dispatcher.cc:70:10  

#30 0x5589b012aa5e in OnMessageReceived ppapi/proxy/plugin\_dispatcher.cc:252:10  

#31 0x5589a7a69204 in OnDispatchMessage ipc/ipc\_channel\_proxy.cc:293:3  

#32 0x5589a5de0814 in Run base/callback.h:397:12  

#33 0x5589a5de0814 in RunTask base/debug/task\_annotator.cc:51:0  

#34 0x5589a5ce9bd9 in RunTask base/message\_loop/message\_loop.cc:476:3  

#35 0x5589a5cea695 in DeferOrRunPendingTask base/message\_loop/message\_loop.cc:485:5  

#36 0x5589a5ceafec in DoWork base/message\_loop/message\_loop.cc:597:13  

#37 0x5589a5cf1c30 in Run base/message\_loop/message\_pump\_default.cc:33:21  

#38 0x5589a5d31b95 in Run base/run\_loop.cc:35:3  

#39 0x5589a5ce831e in ?? base/message\_loop/message\_loop.cc:293:3  

#40 0x5589b1b2c63d in PpapiPluginMain content/ppapi\_plugin/ppapi\_plugin\_main.cc:160:3  

#41 0x5589a5bf6fae in RunZygote content/app/content\_main\_runner.cc:316:14  

#42 0x5589a5bf9a6d in Run content/app/content\_main\_runner.cc:766:12  

#43 0x5589a5bf62ba in ContentMain content/app/content\_main.cc:19:15  

#44 0x5589a5014a85 in ChromeMain chrome/app/chrome\_main.cc:84:12  

#45 0x7f911c6cfec4 in \_\_libc\_start\_main /build/eglibc-3GlaMS/eglibc-2.19/csu/libc-start.c:287:0

previously allocated by thread T0 (chrome) here:  

#0 0x5589a50128bb in operator new(unsigned long) ??:?  

#1 0x5589b1750008 in FXJS\_NewFxDynamicObj third\_party/pdfium/fpdfsdk/src/jsapi/fxjs\_v8.cpp:474:38  

#2 0x5589b176237b in getIcon third\_party/pdfium/fpdfsdk/src/javascript/Document.cpp:1288:36  

#3 0x5589b1777cdc in JSMethod<Document, &Document::getIcon> third\_party/pdfium/fpdfsdk/src/javascript/JS\_Define.h:161:8  

#4 0x5589a9230bba in Call v8/src/api-arguments.cc:29:3  

#5 0x5589a84ab9fa in HandleApiCallHelper<false> v8/src/builtins.cc:3973:34  

#6 0x5589a84fbe49 in Builtin\_Impl\_HandleApiCall v8/src/builtins.cc:3997:3  

#7 0x5589a84fbe49 in Builtin\_HandleApiCall v8/src/builtins.cc:3994:0  

#7 0x7f90f0306186 (<unknown module>)  

#8 0x7f90f0340f3d (<unknown module>)  

#9 0x7f90f0337ae2 (<unknown module>)  

#10 0x7f90f03257ee (<unknown module>)  

#8 0x5589a897a4d2 in Invoke v8/src/execution.cc:97:13  

#9 0x5589a8979b9b in Call v8/src/execution.cc:163:10  

#10 0x5589a83d77fe in Run v8/src/api.cc:1720:23  

#11 0x5589b1750ef1 in FXJS\_Execute third\_party/pdfium/fpdfsdk/src/jsapi/fxjs\_v8.cpp:439:8  

#12 0x5589b16fbbd4 in ?? third\_party/pdfium/fpdfsdk/src/javascript/JS\_Runtime.cpp:240:14  

#13 0x5589b17c4a9a in RunScript third\_party/pdfium/fpdfsdk/src/javascript/JS\_Context.cpp:60:12  

#14 0x5589b125b025 in RunDocumentOpenJavaScript third\_party/pdfium/fpdfsdk/src/fsdk\_actionhandler.cpp:546:18  

#15 0x5589b125b025 in DoAction\_JavaScript third\_party/pdfium/fpdfsdk/src/fsdk\_actionhandler.cpp:33:0  

#16 0x5589b1287e64 in ProcJavascriptFun third\_party/pdfium/fpdfsdk/src/fsdk\_mgr.cpp:474:7  

#17 0x5589a5c0a625 in FinishLoadingDocument pdf/pdfium/pdfium\_engine.cc:1115:3  

#18 0x5589a5c206dc in ContinueLoadingDocument pdf/pdfium/pdfium\_engine.cc:2515:5  

#19 0x5589a5c08c18 in LoadDocument pdf/pdfium/pdfium\_engine.cc:2407:5  

#20 0x5589a5c495db in DidRead pdf/document\_loader.cc:496:5  

#21 0x5589a5c4a1a9 in operator() ppapi/utility/completion\_callback\_factory.h:607:9  

#22 0x5589a5c4a1a9 in Thunk ppapi/utility/completion\_callback\_factory.h:584:0  

#23 0x5589ad0b5e62 in PP\_RunCompletionCallback ppapi/c/pp\_completion\_callback.h:240:3  

#24 0x5589ad0b5e62 in CallWhileUnlocked<void, PP\_CompletionCallback \*, int, PP\_CompletionCallback \*, int> ppapi/shared\_impl/proxy\_lock.h:135:0  

#25 0x5589ad0b5e62 in Run ppapi/shared\_impl/tracked\_callback.cc:141:0  

#26 0x5589b00a507a in RunCallback ppapi/proxy/url\_loader\_resource.cc:363:3  

#27 0x5589b00a507a in OnPluginMsgFinishedLoading ppapi/proxy/url\_loader\_resource.cc:311:0  

#28 0x5589b00a507a in DispatchResourceReply<ppapi::proxy::URLLoaderResource, void (ppapi::proxy::URLLoaderResource::\*)(const ppapi::proxy::ResourceMessageReplyParams &, int), int> ppapi/proxy/dispatch\_reply\_message.h:35:0  

#29 0x5589b00a507a in OnReplyReceived ppapi/proxy/url\_loader\_resource.cc:249:0  

#30 0x5589affef871 in DispatchResourceReply ppapi/proxy/plugin\_message\_filter.cc:116:3  

#31 0x5589a5de0814 in Run base/callback.h:397:12  

#32 0x5589a5de0814 in RunTask base/debug/task\_annotator.cc:51:0  

#33 0x5589a5ce9bd9 in RunTask base/message\_loop/message\_loop.cc:476:3  

#34 0x5589a5cea695 in DeferOrRunPendingTask base/message\_loop/message\_loop.cc:485:5

## Attachments

- [test.html](attachments/test.html) (text/plain, 357 B)
- [a.pdf](attachments/a.pdf) (application/pdf, 1.9 KB)
- [b.pdf](attachments/b.pdf) (application/pdf, 3.3 KB)
- [test.html](attachments/test_53228105.html) (text/plain, 514 B)
- [a.pdf](attachments/a_53228106.pdf) (application/pdf, 1.9 KB)
- [b.pdf](attachments/b_53228107.pdf) (application/pdf, 4.4 KB)
- [c.pdf](attachments/c.pdf) (application/pdf, 3.4 KB)

## Timeline

### cl...@chromium.org (2016-03-11)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5040734683529216

### in...@chromium.org (2016-03-11)

[Empty comment from Monorail migration]

[Monorail components: Internals>Plugins>PDF]

### in...@chromium.org (2016-03-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-03-11)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-03-11)

[Empty comment from Monorail migration]

### ch...@gmail.com (2016-03-18)

Comment about Exploitability
============================

This bug can be exploited as a cross origin bug.

OS: Ubuntu 14.04
Chrome version : 50.0.2661.37 beta (64-bit)
                 51.0.2674.0 (64-bit) - Trunk build

Requirements : Local web server which can serve web pages from 127.0.0.1 and 127.0.0.2.

1. Download and save test.html, a.pdf, b.pdf and c.pdf in local web servers root folder.
2. Open chrome and open http://127.0.0.1/test.html.
   test.html will load below mentioned pdf files in 3 iframes.
   i. http://127.0.0.1/a.pdf
   ii. http://127.0.0.1/c.pdf
   iii. http://127.0.0.2/b.pdf

   Note : b.pdf is loaded from 127.0.0.2.
   b.pdf has this javascript code in Document Javascript section.
   this.addIcon('test',this.getField('btnTest').buttonGetIcon());
   var icon=this.getIcon('test');

   b.pdf has a button labeled 'Show Icon Name'. That button's mouse up event handler has this Javascript code.
   app.alert(icon.name,3);

   So if you load b.pdf in chrome and click 'Show Icon Name', it should alert 'test' if everything is correct.
3. Wait about 15 seconds.
   c.pdf will display an alert with message 'Now Click Show Icon Name button in PDF loaded from 127.0.0.2'
   Note: Open c.pdf in a pdf editor and view Document Javascript section to view Javascript code.
4. Click OK button in alert box.
5. Click 'Show Icon Name' button in b.pdf loaded from 127.0.0.2.
   It will display 'best' instead of 'test'.
   So files loaded fom 127.0.0.1 changed the name of icon created by  http://127.0.0.2/b.pdf.
  



### th...@chromium.org (2016-03-18)

[Empty comment from Monorail migration]

### ts...@chromium.org (2016-03-22)

+jochen for all things v8.  Implication is https://pdfium.googlesource.com/pdfium/+/61dc96f9aa2512807b62cfaec35b1cd012459a6f

### ts...@chromium.org (2016-03-22)

c.pdf's snippet of js:

var iconsarr = [];

function work() {
  i = 0;
  this.addIcon('best',this.getField('btn1').buttonGetIcon());
  while (i < 100000) {
    iconsarr[i] =this.getIcon('best');
    i++;
  }
  app.alert("Now Click Show Icon Name button in PDF loaded from 127.0.0.2",3);
}

t = app.setTimeOut('work()',12000);

### jo...@chromium.org (2016-03-23)

my suspicion is that the timer task is executed even though the pdf instance was already torn down

### ch...@gmail.com (2016-03-23)

Jochen, Timer is not required for this bug. I added  timers to test case because I wanted make sure test case actions execute in correct order.

I think problem is ReleaseDynamicObjsMap method in fxjs_v8.h free objects created in another pdf file.

### jo...@chromium.org (2016-03-23)

ah, I see, so what's going on is that we share global objects between instances.

this might lead to UaF if one instance goes down and destroys the global objects while the other is still using them, or to cross site leaks if one instance puts properties on those global objects.

### ts...@chromium.org (2016-03-23)

The map is global, but I don't think that these "dynamic" objects get shared between context -- the cross-origin leak being a Use-after-Free corruption.  I'm going to move the destuction of the map to after the refcount hits 0.

### ts...@chromium.org (2016-03-24)

https://pdfium.googlesource.com/pdfium/+/e432675850161570a8562f8c617da039f51f706d

### ts...@chromium.org (2016-03-24)

https://codereview.chromium.org/1826223002/ revered

### bu...@chromium.org (2016-03-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/9deaa936de481ebfae777b936e44720c311aa4d9

commit 9deaa936de481ebfae777b936e44720c311aa4d9
Author: ochang <ochang@chromium.org>
Date: Thu Mar 24 22:42:06 2016

Roll PDFium 4161c5c..a560806

https://pdfium.googlesource.com/pdfium.git/+log/4161c5c..a560806

TBR=tsepez@chromium.org
BUG=594120,596524,583037

Review URL: https://codereview.chromium.org/1829213002

Cr-Commit-Position: refs/heads/master@{#383173}

[modify] https://crrev.com/9deaa936de481ebfae777b936e44720c311aa4d9/DEPS


### go...@chromium.org (2016-03-28)

A friendly reminder that M50 Stable is launching soon! Your bug is labelled as Stable ReleaseBlock, pls make sure to land the fix and get it merged into the release branch by Apr-5. All changes MUST be merged into the release branch by 5pm on Apr-8 to make into the desktop Stable final build cut. Thanks!

### go...@chromium.org (2016-04-04)

M50 Stable is launching very soon! Your bug is labelled as Stable ReleaseBlock, pls make sure to land the fix and get it merged ASAP. All changes MUST be merged into the release branch by 5pm on Apr-8 to make into the desktop Stable final build cut. Thanks!

### oc...@chromium.org (2016-04-04)

Tom, this is fixed here in the reland (https://pdfium.googlesource.com/pdfium.git/+/9967cc5861fbff894eed8fca40e1e5ed524b04c6) right?

### ti...@google.com (2016-04-04)

[Automated comment] DEPS changes referenced in bugdroid comments, needs manual review.

### cl...@chromium.org (2016-04-05)

[Empty comment from Monorail migration]

### ti...@google.com (2016-04-05)

Merge approved for M50 (branch 2661). Pls go ahead merge.

### go...@chromium.org (2016-04-05)

Please merge your change to M50 branch 2661 before 4:00 PM PST today if you like to make it to this week beta. We're cutting beta candidate today.

### bu...@chromium.org (2016-04-05)

The following revision refers to this bug:
  http://goto.ext.google.com/viewvc/chrome-internal?view=rev&revision=86162

------------------------------------------------------------------
r86162 | ochang@google.com | 2016-04-05T19:27:29.394034Z

-----------------------------------------------------------------

### ch...@gmail.com (2016-05-05)

Is this bug eligible to go to reward panel?

### aa...@google.com (2016-05-05)

Yes, it will go to reward panel eventually.

### ti...@google.com (2016-06-30)

Thanks for the report and apologies for the delay here - we've been working though a backlog of Beta and Dev reward bugs, which is now cleared.

Congrats - $5,000 for this report!

We'll start payment shortly. Thanks again!

### aw...@chromium.org (2016-07-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-07-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/594120?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083839)*
