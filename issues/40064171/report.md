# Heap-use-after-free in WebCore::ElementV8Internal::onclickAttrGetter

| Field | Value |
|-------|-------|
| **Issue ID** | [40064171](https://issues.chromium.org/issues/40064171) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink, Blink>JavaScript |
| **Reporter** | at...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2012-08-19 |
| **Bounty** | $1,000.00 |

## Description

Repro-file as attachment.

Reproduces clean on my machines.

Chrome version: ASAN Chromium 23.0.1240.0

ASAN-report:

==3559== ERROR: AddressSanitizer heap-use-after-free on address 0x7f40e0cc3790 at pc 0x7f40f693a837 bp 0x7fff60e9ee20 sp 0x7fff60e9ee18
READ of size 8 at 0x7f40e0cc3790 thread T0
    #0 0x7f40f693a836 in WebCore::ElementV8Internal::onclickAttrGetter(v8::Local<v8::String>, v8::AccessorInfo const&) gen/webkit/bindings/V8DerivedSources03.cpp:0
    #1 0x7f40f820832c in v8::internal::JSObject::GetPropertyWithCallback(v8::internal::Object*, v8::internal::Object*, v8::internal::String*) ???:0
    #2 0x7f40f867f5ba in v8::internal::LoadIC::Load(v8::internal::InlineCacheState, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::String>) ???:0
    #3 0x7f40f8690e06 in v8::internal::LoadIC_Miss(v8::internal::Arguments, v8::internal::Isolate*) ???:0
.
.
.


## Attachments

- [chrome-heap-use-after-free-WebCoreElementV8InternalonclickAttrGetter-7e7.html](attachments/chrome-heap-use-after-free-WebCoreElementV8InternalonclickAttrGetter-7e7.html) (text/html; charset=us-ascii, 336 B)

## Timeline

### in...@chromium.org (2012-08-19)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=96258880

Uploader: inferno@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x7f2ee8d65b90
Crash State:
  - crash stack -
  WebCore::ElementV8Internal::onclickAttrGetter
  v8::internal::JSObject::GetPropertyWithCallback
  - free stack -
  WebCore::removeListenerFromVector
  WebCore::EventListenerMap::remove
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=114961:114982

Minimized Testcase (0.19 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv96BxALLi6Yv2p7caO_Pc7PitL_ULl32sFpgCtEX10IgvjxgkLtEkvA81FhJ_4NP-lv_rvFSzyq191wRpsYzsrq558Z3HuE_8Y3INSYVP2IrJZ8eIHdiB4oEjwl25Pcfte-99eToxfloaO4lgTgJC_6FJqQ3cDowiz4CLFZJW075jsKAfu4
<body>
<script>
function foo() {
	document.body.setAttribute("onclick", "var x=;");
}

window.onerror = foo
document.body.setAttribute("onclick", "var x=;");
document.body.onclick;

</script>

### in...@chromium.org (2012-08-19)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-08-19)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-08-19)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-08-20)

Upstreamed - https://bugs.webkit.org/show_bug.cgi?id=94440

### in...@chromium.org (2012-08-20)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-08-21)

I asked Anton for help since i don't know the bindings code well enough.

### in...@chromium.org (2012-08-30)

http://trac.webkit.org/changeset/127117

### cl...@chromium.org (2012-08-31)

ClusterFuzz has detected this issue as fixed in range 154235:154298.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=96258880

Uploader: inferno@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x7f2ee8d65b90
Crash State:
  - crash stack -
  WebCore::ElementV8Internal::onclickAttrGetter
  v8::internal::JSObject::GetPropertyWithCallback
  - free stack -
  WebCore::removeListenerFromVector
  WebCore::EventListenerMap::remove
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=114961:114982
Fixed: https://cluster-fuzz.appspot.com/revisions?range=154235:154298

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv96BxALLi6Yv2p7caO_Pc7PitL_ULl32sFpgCtEX10IgvjxgkLtEkvA81FhJ_4NP-lv_rvFSzyq191wRpsYzsrq558Z3HuE_8Y3INSYVP2IrJZ8eIHdiB4oEjwl25Pcfte-99eToxfloaO4lgTgJC_6FJqQ3cDowiz4CLFZJW075jsKAfu4

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### sc...@gmail.com (2012-09-05)

M22: http://trac.webkit.org/changeset/127630

### sc...@gmail.com (2012-09-05)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-09-25)

@attekett: nice find, $1000

### sc...@gmail.com (2012-10-12)

[Empty comment from Monorail migration]

### js...@chromium.org (2012-12-20)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-10)

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

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

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

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/143609?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink, Blink>JavaScript]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40064171)*
