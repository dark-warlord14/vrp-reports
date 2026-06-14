# [v8] Stale pointer in CSSStyleSheet, Invalid cast in V8ListenerList::doFindWrapper

| Field | Value |
|-------|-------|
| **Issue ID** | [40095488](https://issues.chromium.org/issues/40095488) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink, Blink>JavaScript |
| **Reporter** | in...@chromium.org |
| **Assignee** | ri...@chromium.org |
| **Created** | 2011-09-23 |
| **Bounty** | $1,500.00 |

## Description

credit: Serg
Broken off - http://code.google.com/p/chromium/issues/detail?id=97149

4. Stale pointer in CSSStyleSheet
A style sheet wrapper contains a hidden reference to its owner node to keep it alive.
v8::Handle<v8::Value> toV8(CSSStyleSheet* impl)
{
...
        V8DOMWrapper::setNamedHiddenReference(wrapper, "ownerNode", toV8(ownerNode));

The bug is partially caused by:
void StyleElement::createSheet(Element* e, int startLineNumber, const String& text)
{
...
    if (m_sheet) {
        if (m_sheet->isLoading())
            document->removePendingSheet();
        //// m_sheet->clearOwnerNode() should be here!
        m_sheet = 0;


5. Invalid cast in V8ListenerList::doFindWrapper
static V8EventListener* doFindWrapper(v8::Local<v8::Object> object, v8::Handle<v8::String> wrapperProperty)
{
...
    v8::Local<v8::Value> listener = object->GetHiddenValue(wrapperProperty);
    if (listener.IsEmpty())
        return 0;
    return static_cast<V8EventListener*>(v8::External::Unwrap(listener));

Repro:
    propName = "WebCore::HiddenProperty::listener";
    obj = {};

    Object.prototype.__defineSetter__(propName,
        function() {
            delete Object.prototype[propName];
            hiddenObj = this
        }
    );
    addEventListener("message", obj);

    hiddenObj[propName] = 0x100;
    removeEventListener("message", obj);

Hidden values would be safe if JSObject::SetHiddenPropertiesObject set the object's prototype to null.

Serg, can you please provide patch on the webkit bug soon. We have an upcoming deadline on tuesday to merge the fixes.

## Timeline

### in...@chromium.org (2011-09-23)

[Comment Deleted]

### in...@chromium.org (2011-09-23)

Sorry, this is not in webkit code, but in v8 code. Serg, we don't need any action item from your side.

Can one of the v8 guys please evaluate this change and merge this in ?




### sc...@gmail.com (2011-09-25)

Here is the 1-liner fix for evaluation. Danno?

--- objects.cc	(revision 9288)
+++ objects.cc	(working copy)
@@ -3024,6 +3024,7 @@ MaybeObject* JSObject::GetHiddenProperties(HiddenP
             isolate->context()->global_context()->object_function());
         if (!maybe_obj->ToObject(&hidden_obj)) return maybe_obj;
       }
+      JSObject::cast(hidden_obj)->SetPrototype(heap->null_value(), false);
       return obj->SetHiddenPropertiesObject(hidden_obj);
     } else {
       return heap->undefined_value();

### da...@chromium.org (2011-09-26)

At first blush, looks OK. I'll make sure that the fix gets committed and merged to the M14 and M15 branches.

### da...@chromium.org (2011-09-26)

[Empty comment from Monorail migration]

### da...@chromium.org (2011-09-26)

[Empty comment from Monorail migration]

### ri...@chromium.org (2011-09-26)

Fix committed to bleeding edge in revision 9434, 3.5 branch in 9435 and 3.4 branch in 9437. Will land on trunk with next push (or tomorrow if I can see that our push will be postponed due to GC branch landing)

### in...@chromium.org (2011-09-26)

[Empty comment from Monorail migration]

### ri...@chromium.org (2011-09-27)

Landed in chromium trunk in revision 102928 (v8 trunk revision 9442)

### sc...@gmail.com (2011-10-01)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-10-03)

@serg.glazunov: another great find! The fix seems to have been accepted verbatim by the v8 team, so there's the $500 bonus for the fix for a total of $1500.

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

### js...@chromium.org (2011-10-05)

Batch update.

### sc...@gmail.com (2011-10-07)

Payment in system.

### [Deleted User] (2012-05-15)

Marking old security bugs Fixed..

### sc...@gmail.com (2012-09-24)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-10)

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

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/97784?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink, Blink>JavaScript]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095488)*
