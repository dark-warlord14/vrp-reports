# Security: v8: WebKitPoint() memory corruption

| Field | Value |
|-------|-------|
| **Issue ID** | [40080247](https://issues.chromium.org/issues/40080247) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink, Blink>JavaScript |
| **Reporter** | sk...@chromium.org |
| **Assignee** | mo...@google.com |
| **Created** | 2010-04-07 |
| **Bounty** | $500.00 |

## Description

By calling window.WebKitPoint(), we are causing some kind of memory 
corruption in v8. The following two html files will trigger the issue by 
calling the method in an IFRAME, while the main page refreshes the IFRAME 
from time to time to cause GarbageCollection, which exposes the memory 
corruption.

Repro5.1.html:
<IFRAME src=repro5.2.html></IFRAME>
<SCRIPT>
  setInterval(function () {
    document.body.innerHTML = "<IFRAME src=repro5.2.html></IFRAME><BR>" + 
new Date();
  }, 300);
</SCRIPT>

Repro5.2.html:
  <script language="javascript">
    setInterval("window.WebKitPoint();", 10);
  </script>

Crashes vary. I expect this to be the main culprit behind the ref_fuzz 
crashes.


## Attachments

- [repro5.2.html](attachments/repro5.2.html) (text/plain; charset=us-ascii, 95 B)
- [repro5.1.html](attachments/repro5.1.html) (text/plain; charset=us-ascii, 184 B)

## Timeline

### sc...@gmail.com (2010-04-07)

Looks simple enough, like our constructor is assuming it has at least one argument. 
I'll fix.

### sk...@chromium.org (2010-04-07)

Side note: this was found after playing with the repro for https://crbug.com/chromium/40616.

I assumed this was v8 related, so I opened a bug:
http://code.google.com/p/v8/issues/detail?id=668

### sk...@chromium.org (2010-04-07)

Repro's

### sc...@gmail.com (2010-04-07)

This patch to the v8 bindings should do it


Index: V8WebKitPointConstructor.cpp
===================================================================
--- V8WebKitPointConstructor.cpp        (revision 57160)
+++ V8WebKitPointConstructor.cpp        (working copy)
@@ -43,6 +43,10 @@
 v8::Handle<v8::Value> V8WebKitPoint::constructorCallback(const v8::Arguments& args)
 {
     INC_STATS("DOM.WebKitPoint.Constructor");
+
+    if (!args.IsConstructCall())
+        return throwError("DOM object constructor cannot be called as a function.");
+
     float x = 0;
     float y = 0;
     if (args.Length() > 1) {


It's now 4am... oops... I'll try and persuade Abhishek or Justin to get this landed 
early tomorrow... I certainly won't be around early :)

### sc...@gmail.com (2010-04-07)

Ah, it was Dimitri who fixed a similar bug in http://trac.webkit.org/changeset/45826


### sk...@chromium.org (2010-04-07)

Thanks Chris, go get some sleep :)

### sk...@chromium.org (2010-04-07)

Adding V8 peeps.

### ag...@chromium.org (2010-04-07)

[Empty comment from Monorail migration]

### sk...@chromium.org (2010-04-07)

[Empty comment from Monorail migration]

### in...@chromium.org (2010-04-07)

i had a chat with Dimitri on this. i have opened a webkit bug -
https://bugs.webkit.org/show_bug.cgi?id=37210. will fix it and also add a layout test.

### [Deleted User] (2010-04-07)

[Empty comment from Monorail migration]

### sk...@chromium.org (2010-04-07)

Fixed in http://trac.webkit.org/changeset/57224
Verified in Chromium 5.0.371.0 (43859)

Filed 10 hours ago. During MTV night. Go team!

### in...@chromium.org (2010-04-07)

Merge 57224 - 20100407 Abhishek Arya <inferno@chromium.org>

Reviewed by Adam Barth.

Make sure that calling bindings constructors as function does not result in crash.

* fast/constructors: Added.
* fast/constructors/constructorasfunctioncrashexpected.txt: Added.
* fast/constructors/constructorasfunctioncrash.html: Added.
20100407 Abhishek Arya <inferno@chromium.org>

Reviewed by Adam Barth.

[V8] Add a missing check for constructor call in WebKitPointConstructor.
https://bugs.webkit.org/show_bug.cgi?id=37210

Test: fast/constructors/constructorasfunctioncrash.html

* bindings/v8/custom/V8WebKitPointConstructor.cpp:
(WebCore::V8WebKitPoint::constructorCallback): Added a check for constructor call.

TBR=abarth@webkit.org

Committed: http://src.chromium.org/viewvc/chrome?view=rev&revision=43874

### in...@chromium.org (2010-04-07)

Hey BJ, added you to the credit list for v4.1 :). Keep up the great fuzzers!!!

### sc...@gmail.com (2010-04-08)

Adding kuzzcc@, because this test case was extracted from his test case which executes 
every function in the DOM :)

### ku...@gmail.com (2010-04-09)

I got it like this

<script>
setInterval('WebKitPoint()',10)
setTimeout('location.reload()',1000)
</script>

then press Shift+Ctrl+J it will crash 

### sc...@gmail.com (2010-04-13)

Thank you again, kuzzcc! Since your little script gave us an easy repro for a nice 
bug, we're qualifying this as a $500 reward.

### [Deleted User] (2010-04-19)

Renderer doesn't crash with Google Chrome 4.1.249.1059 (Official Build 44723)

### sc...@gmail.com (2010-05-19)

Was fixed in 4.1.249.1059

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-10-05)

Batch update.

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### yu...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-06)

This issue was migrated from crbug.com/chromium/40635?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink, Blink>JavaScript]
[Monorail mergedwith: crbug.com/chromium/40630, crbug.com/v8/668]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080247)*
