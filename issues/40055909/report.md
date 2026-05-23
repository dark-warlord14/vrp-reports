# crash in canvas filter

| Field | Value |
|-------|-------|
| **Issue ID** | [40055909](https://issues.chromium.org/issues/40055909) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Canvas |
| **Platforms** | Mac |
| **Reporter** | wx...@gmail.com |
| **Assignee** | aa...@chromium.org |
| **Created** | 2021-05-18 |
| **Bounty** | $5,000.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36

Steps to reproduce the problem:
1. first enable Experimental canvas 2D API features
2. python -m SimpleHTTPServer 
3. chrome visit the http://127.0.0.1:8000/test.html

What is the expected behavior?

What went wrong?
as the function ColorMatrixFilterOperation* ResolveColorMatrix()

```
ColorMatrixFilterOperation* ResolveColorMatrix(
    v8::Local<v8::Object> v8_filter_object,
    ScriptState* script_state,
    ExceptionState& exception_state) {
  v8::Local<v8::Value> v8_value;
  v8::Local<v8::Array> v8_array;
  if (v8_filter_object
          ->Get(script_state->GetContext(),
                V8String(script_state->GetIsolate(), "values"))
          .ToLocal(&v8_value)) {
    if (!v8_value->IsArray()) {
      exception_state.ThrowTypeError(
          "Failed to construct color matrix filter, 'values' must be an array "
          "of 20 numbers.");
      return nullptr;
    }
    v8_array = v8_value.As<v8::Array>();
  }

```
the code ```
v8_filter_object
          ->Get(
```

we could reset the object property in js like the code

```
 Object.defineProperty(obj, 'values', {
    get: function () {
      console.log("getter");
      document.body.removeChild(iframe);
      return matrx;
    }
  });
```

here we destroy the v8's isolate context.
maybe reuse in construct.

here is my mac log
```
Received signal 11 SEGV_MAPERR 000000000000
 [0x00011921eed9]
 [0x000118fc9c53]
 [0x00011921ec5b]
 [0x7fff207a7d7d]
 [0x7ffeef054160]
 [0x00012c72dadf]
 [0x00012c72f708]
 [0x00012c72b30c]
 [0x00012b489700]
 [0x000114cfbcdc]
 [0x000114cf841d]
 [0x000114cf6bce]
 [0x7e9e000768f8]
[end of stack trace]
[0518/153544.623568:WARNING:process_memory_mac.cc(93)] mach_vm_read(0x7ffeef05b000, 0x2000): (os/kern) invalid address (1)
```

here is the linux debug log
```
#
# Fatal error in ../../v8/src/api/api-inl.h, line 131
# Debug check failed: allow_empty_handle || that != nullptr.
#
#
#
#FailureMessage Object: 0x7f22169e6060#0 0x55b133407f8b (/home/raven/Desktop/asan-linux-debug-883812/chrome+0x9133f8a)
#1 0x7f22ed50e8ff (/home/raven/Desktop/asan-linux-debug-883812/libbase.so+0xd648fe)
#2 0x7f22ecdb1874 (/home/raven/Desktop/asan-linux-debug-883812/libbase.so+0x607873)
#3 0x7f22ecdb16e5 (/home/raven/Desktop/asan-linux-debug-883812/libbase.so+0x6076e4)
#4 0x7f22507a3983 (/home/raven/Desktop/asan-linux-debug-883812/libgin.so+0xaa982)
#5 0x7f2250b61190 (/home/raven/Desktop/asan-linux-debug-883812/libv8_libbase.so+0x3c18f)
#6 0x7f2250b600df (/home/raven/Desktop/asan-linux-debug-883812/libv8_libbase.so+0x3b0de)
#7 0x7f22528af014 (/home/raven/Desktop/asan-linux-debug-883812/libv8.so+0x1d18013)
#8 0x7f2249372ade (/home/raven/Desktop/asan-linux-debug-883812/libblink_modules.so+0x6863add)
#9 0x7f2249374797 (/home/raven/Desktop/asan-linux-debug-883812/libblink_modules.so+0x6865796)
#10 0x7f224936f8a3 (/home/raven/Desktop/asan-linux-debug-883812/libblink_modules.so+0x68608a2)
#11 0x7f224723f4ca (/home/raven/Desktop/asan-linux-debug-883812/libblink_modules.so+0x47304c9)
#12 0x7f2252a4d365 (/home/raven/Desktop/asan-linux-debug-883812/libv8.so+0x1eb6364)
#13 0x7f2252a46807 (/home/raven/Desktop/asan-linux-debug-883812/libv8.so+0x1eaf806)
#14 0x7f2252a432c1 (/home/raven/Desktop/asan-linux-debug-883812/libv8.so+0x1eac2c0)
#15 0x7f2252a423b1 (/home/raven/Desktop/asan-linux-debug-883812/libv8.so+0x1eab3b0)
#16 0x7edc003196ff <unknown>
[4094:4094:0518/003652.295726:INFO:CONSOLE(28)] "getter", source: http://127.0.0.1:8000/test.html (28)
[4129:4149:0518/003652.415996:ERROR:ssl_client_socket_impl.cc(981)] handshake failed; returned -1, SSL error code 1, net_error -107
[0518/003652.549702:ERROR:process_snapshot_linux.cc(120)] thread not found 1
[4129:4149:0518/003652.564261:ERROR:ssl_client_socket_impl.cc(981)] handshake failed; returned -1, SSL error code 1, net_error -107
[0518/003652.822125:ERROR:process_snapshot_linux.cc(120)] thread not found 1
Received signal 4 ILL_ILLOPN 7f2250b7f598
#0 0x55b133407f8b (/home/raven/Desktop/asan-linux-debug-883812/chrome+0x9133f8a)
#1 0x7f22ed50e8ff (/home/raven/Desktop/asan-linux-debug-883812/libbase.so+0xd648fe)
#2 0x7f22ecdb1874 (/home/raven/Desktop/asan-linux-debug-883812/libbase.so+0x607873)
#3 0x7f22ecdb16e5 (/home/raven/Desktop/asan-linux-debug-883812/libbase.so+0x6076e4)
#4 0x7f22ed50cef1 (/home/raven/Desktop/asan-linux-debug-883812/libbase.so+0xd62ef0)
#5 0x7f22394b5980 (/lib/x86_64-linux-gnu/libpthread-2.27.so+0x1297f)
#6 0x7f2250b7f598 (/home/raven/Desktop/asan-linux-debug-883812/libv8_libbase.so+0x5a597)
#7 0x7f2250b611ad (/home/raven/Desktop/asan-linux-debug-883812/libv8_libbase.so+0x3c1ac)
#8 0x7f2250b600df (/home/raven/Desktop/asan-linux-debug-883812/libv8_libbase.so+0x3b0de)
#9 0x7f22528af014 (/home/raven/Desktop/asan-linux-debug-883812/libv8.so+0x1d18013)
#10 0x7f2249372ade (/home/raven/Desktop/asan-linux-debug-883812/libblink_modules.so+0x6863add)
#11 0x7f2249374797 (/home/raven/Desktop/asan-linux-debug-883812/libblink_modules.so+0x6865796)
#12 0x7f224936f8a3 (/home/raven/Desktop/asan-linux-debug-883812/libblink_modules.so+0x68608a2)
#13 0x7f224723f4ca (/home/raven/Desktop/asan-linux-debug-883812/libblink_modules.so+0x47304c9)
#14 0x7f2252a4d365 (/home/raven/Desktop/asan-linux-debug-883812/libv8.so+0x1eb6364)
#15 0x7f2252a46807 (/home/raven/Desktop/asan-linux-debug-883812/libv8.so+0x1eaf806)
#16 0x7f2252a432c1 (/home/raven/Desktop/asan-linux-debug-883812/libv8.so+0x1eac2c0)
#17 0x7f2252a423b1 (/home/raven/Desktop/asan-linux-debug-883812/libv8.so+0x1eab3b0)
#18 0x7edc003196ff <unknown>
  r8: 000000000000a000  r9: 00007f2219b53250 r10: 00000000000001e2 r11: 00007f2250b7f580
 r12: 00000fe446c8e108 r13: 00007f22169e6020 r14: 00007f2236470840 r15: 00007f22169e6060
  di: 00007f221650a000  si: 0000000000000001  bp: 00007fff7b3353b0  bx: 00007fff7b3353c0
  dx: 00007f2219ce6560  ax: 00007f2219cd7000  cx: 000010006f65e800  sp: 00007fff7b3353b0
  ip: 00007f2250b7f598 efl: 0000000000010202 cgf: 002b000000000033 erf: 0000000000000000
 trp: 0000000000000006 msk: 0000000000000000 cr2: 0000000000000000
[end of stack trace]

```

my chromium commmit is a6b14dfd44d7cd7a5edd7572edb925c4225900f3

Did this work before? N/A 

Chrome version: 90.0.4430.212  Channel: stable
OS Version: OS X 10.15.7
Flash Version:

## Attachments

- [test.html](attachments/test.html) (text/plain, 1.9 KB)

## Timeline

### [Deleted User] (2021-05-18)

[Empty comment from Monorail migration]

### va...@chromium.org (2021-05-19)

[Empty comment from Monorail migration]

### va...@chromium.org (2021-05-19)

Thanks for the report. Can you please share the symbolized stack trace by following https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/testing/linux_running_asan_tests.md ?



### va...@chromium.org (2021-05-19)

Security_Impact-None because it requires enabling Experimental canvas 2D API features, based on https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/security-labels.md#toc-security_impact-none

### va...@chromium.org (2021-05-19)

jgruber/aaronhk: Could you comment on the Security_Severity of this bug?

[Monorail components: Blink>Canvas]

### jg...@chromium.org (2021-05-19)

I don't have enough context to comment much. Just wanted to confirm that calling `Get` on a user-controlled object (https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/canvas/canvas2d/canvas_filter_operation_resolver.cc;l=71;drc=29b194da62b8475b74bc08eeb0f0212b92411c89) can trigger execution of user-provided JS code as the report shows. I don't know if that's a problem here or not.

### wx...@gmail.com (2021-05-19)

I try this step(https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/testing/linux_running_asan_tests.md), and there still has no symbols stack.

### va...@chromium.org (2021-05-22)

[Empty comment from Monorail migration]

### aa...@chromium.org (2021-05-26)

The best kind of bug, a fix was already in the works
https://chromium-review.googlesource.com/c/chromium/src/+/2910714

I can confirm that the test page no longer crashes on linux. It should get merged any second now.

### gi...@appspot.gserviceaccount.com (2021-05-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/524b932441c3526c2e424dffafc9f5e2dcb62aed

commit 524b932441c3526c2e424dffafc9f5e2dcb62aed
Author: Aaron Krajeski <aaronhk@chromium.org>
Date: Wed May 26 17:19:18 2021

Use Dictionary in CanvasFilterOperationResolver

Refactor the CanvasFilterOperationResolver to make use of classes
already available in the blink/renderer/bindings/core/v8/ directory.

Filters attributes are defined here:
https://drafts.fxtf.org/filter-effects-1/

Bug: 1169216, 1210394
Change-Id: I00b725b81fa9d2ab14d02eef9d66af4afd14c6c0
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2910714
Reviewed-by: Fredrik Söderquist <fs@opera.com>
Commit-Queue: Aaron Krajeski <aaronhk@chromium.org>
Cr-Commit-Position: refs/heads/master@{#886779}

[modify] https://crrev.com/524b932441c3526c2e424dffafc9f5e2dcb62aed/third_party/blink/renderer/core/svg/svg_enumeration_map.h
[modify] https://crrev.com/524b932441c3526c2e424dffafc9f5e2dcb62aed/third_party/blink/renderer/core/svg/svg_fe_convolve_matrix_element.cc
[modify] https://crrev.com/524b932441c3526c2e424dffafc9f5e2dcb62aed/third_party/blink/renderer/modules/canvas/canvas2d/canvas_filter.cc
[modify] https://crrev.com/524b932441c3526c2e424dffafc9f5e2dcb62aed/third_party/blink/renderer/modules/canvas/canvas2d/canvas_filter.h
[modify] https://crrev.com/524b932441c3526c2e424dffafc9f5e2dcb62aed/third_party/blink/renderer/modules/canvas/canvas2d/canvas_filter.idl
[modify] https://crrev.com/524b932441c3526c2e424dffafc9f5e2dcb62aed/third_party/blink/renderer/modules/canvas/canvas2d/canvas_filter_operation_resolver.cc
[modify] https://crrev.com/524b932441c3526c2e424dffafc9f5e2dcb62aed/third_party/blink/renderer/modules/canvas/canvas2d/canvas_filter_operation_resolver.h
[modify] https://crrev.com/524b932441c3526c2e424dffafc9f5e2dcb62aed/third_party/blink/web_tests/external/wpt/html/canvas/element/filters/2d.filter.canvasFilterObject.convolveMatrix.exceptions.html
[modify] https://crrev.com/524b932441c3526c2e424dffafc9f5e2dcb62aed/third_party/blink/web_tests/external/wpt/html/canvas/offscreen/filters/2d.filter.canvasFilterObject.convolveMatrix.exceptions.html
[modify] https://crrev.com/524b932441c3526c2e424dffafc9f5e2dcb62aed/third_party/blink/web_tests/external/wpt/html/canvas/offscreen/filters/2d.filter.canvasFilterObject.convolveMatrix.exceptions.worker.js
[modify] https://crrev.com/524b932441c3526c2e424dffafc9f5e2dcb62aed/third_party/blink/web_tests/external/wpt/html/canvas/tools/yaml/element/filters.yaml
[modify] https://crrev.com/524b932441c3526c2e424dffafc9f5e2dcb62aed/third_party/blink/web_tests/external/wpt/html/canvas/tools/yaml/offscreen/filters.yaml


### aa...@chromium.org (2021-05-27)

No longer crashes on Mac canary with my patch applied.

### wx...@gmail.com (2021-05-27)

great job

### [Deleted User] (2021-05-27)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-27)

[Empty comment from Monorail migration]

### am...@google.com (2021-06-10)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-06-10)

Congratulations - the VRP Panel had decided to award you $5,000 for this report. Nice work! 

### am...@google.com (2021-06-14)

[Empty comment from Monorail migration]

### wx...@gmail.com (2021-07-07)

Hello,I still can't see  the bug bounty, Is there any wrong with the system of payments?

### am...@google.com (2021-07-23)

Just seeing this question in the bug report, but similar to my response via email a couple of weeks ago, there have been changes to the finance system, and payment processing has been a bit slower as finance acclimates to the new system. They are working on improving this, but it will take a bit more time.

This payment was fully processed 28 June, so you should be receiving payment very soon. Apologies this took so long and thank you for your patience as well as your bug reports! 


### [Deleted User] (2021-09-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2021-09-02)

This issue was migrated from crbug.com/chromium/1210394?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1210395]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055909)*
