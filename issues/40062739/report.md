# Security: Security DCHECK failed: IsA<Derived>(from) blink::`anonymous namespace'::CalcToNumericValue:css_numeric_value.cc:162

| Field | Value |
|-------|-------|
| **Issue ID** | [40062739](https://issues.chromium.org/issues/40062739) |
| **Status** | Fixed |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>CSS |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | m....@gmail.com |
| **Assignee** | xi...@chromium.org |
| **Created** | 2023-01-20 |
| **Bounty** | $7,000.00 |

## Description

**VERSION**  

WIN10 X64  

asan-win32-release\_x64-1094234

**REPRODUCTION CASE**  

chrome --no-sandbox --user-data-dir=test --enable-blink-test-features poc.html

Type of crash: [tab]

RCA  

Coming soon

ASAN

[12296:19268:0120/015104.784:FATAL:casting.h(115)] Security DCHECK failed: IsA<Derived>(from).  

Backtrace:  

base::debug::CollectStackTrace [0x00007FF94651E0A2+18] (D:\chromium\src\base\debug\stack\_trace\_win.cc:329)  

base::debug::StackTrace::StackTrace [0x00007FF9461B9FBA+26] (D:\chromium\src\base\debug\stack\_trace.cc:218)  

logging::LogMessage::~LogMessage [0x00007FF94621AC81+673] (D:\chromium\src\base\logging.cc:731)  

blink::`anonymous namespace'::CalcToNumericValue [0x00007FF8FACEAEBF+1727] (D:\chromium\src\third_party\blink\renderer\core\css\cssom\css_numeric_value.cc:162) blink::CSSNumericValue::FromCSSValue [0x00007FF8FACEDA9B+603] (D:\chromium\src\third_party\blink\renderer\core\css\cssom\css_numeric_value.cc:332) blink::`anonymous namespace'::CreateStyleValue [0x00007FF8FAD55608+712] (D:\chromium\src\third\_party\blink\renderer\core\css\cssom\style\_value\_factory.cc:61)  

blink::`anonymous namespace'::CreateStyleValueWithProperty [0x00007FF8FAD5270F+5343] (D:\chromium\src\third_party\blink\renderer\core\css\cssom\style_value_factory.cc:274) blink::StyleValueFactory::CssValueToStyleValueVector [0x00007FF8FAD503E0+400] (D:\chromium\src\third_party\blink\renderer\core\css\cssom\style_value_factory.cc:391) absl::functional_internal::InvokeObject<`lambda at ../../third\_party/blink/renderer/core/css/cssom/style\_property\_map\_read\_only\_main\_thread.cc:139:19',void,const blink::CSSPropertyName &,const blink::CSSValue &> [0x00007FF8FAD4BDFA+218] (D:\chromium\src\third\_party\abseil-cpp\absl\functional\internal\function\_ref.h:74)  

blink::DeclaredStylePropertyMap::ForEachProperty [0x00007FF8FAD2E4EA+1034] (D:\chromium\src\third\_party\blink\renderer\core\css\cssom\declared\_style\_property\_map.cc:112)  

blink::StylePropertyMapReadOnlyMainThread::CreateIterationSource [0x00007FF8FAD4B463+387] (D:\chromium\src\third\_party\blink\renderer\core\css\cssom\style\_property\_map\_read\_only\_main\_thread.cc:139)  

blink::`anonymous namespace'::v8_style_property_map_read_only::EntriesOperationCallback [0x00007FF8FF87CBE5+1013] (D:\chromium\src\out\asan\gen\third_party\blink\renderer\bindings\core\v8\v8_style_property_map_read_only.cc:225) v8::internal::FunctionCallbackArguments::Call [0x00007FF90355498A+1002] (D:\chromium\src\v8\src\api\api-arguments-inl.h:146) v8::internal::`anonymous namespace'::HandleApiCallHelper<0> [0x00007FF903551F32+2354] (D:\chromium\src\v8\src\builtins\builtins-api.cc:113)  

v8::internal::Builtin\_Impl\_HandleApiCall [0x00007FF90354FA48+1032] (D:\chromium\src\v8\src\builtins\builtins-api.cc:148)  

v8::internal::Builtin\_HandleApiCall [0x00007FF90354ED91+305] (D:\chromium\src\v8\src\builtins\builtins-api.cc:135)

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 319 B)
- deleted (application/octet-stream, 0 B)
- [asan.txt](attachments/asan.txt) (text/plain, 2.6 KB)

## Timeline

### [Deleted User] (2023-01-20)

[Empty comment from Monorail migration]

### m....@gmail.com (2023-01-20)

[Empty comment from Monorail migration]

### bo...@google.com (2023-01-21)

Thanks for the report. I can repro on Linux at M108 and M111 with the --enable-blink-test-features flag, but not without so setting Security_Impact-None. If you know of a way to trigger without the nonstandard flag, please let us know and we'll drop the Impact-None bit. 

Severity High because memory corruption in the sandboxed renderer process. 

With repro on Linux and Windows, I'm setting affected platforms broadly under the assumption it reproduces elsewhere. 

[Monorail components: Blink>Internals>WTF]

### m....@gmail.com (2023-01-22)

[Comment Deleted]

### m....@gmail.com (2023-01-22)

Bisect:
Introduce by CL:
https://chromium-review.googlesource.com/c/chromium/src/+/3648384

Impacted:
Canary 104 104.0.5076.0
Dev 104 104.0.5082.0
Beta 104 104.0.5112.18
Stable 104 104.0.5112.69

### tk...@chromium.org (2023-01-22)

[Empty comment from Monorail migration]

[Monorail components: -Blink>Internals>WTF Blink>CSS]

### gi...@appspot.gserviceaccount.com (2023-01-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/3b57c751b407cf0d3b26a9d8ab4bd2dadb7dc94d

commit 3b57c751b407cf0d3b26a9d8ab4bd2dadb7dc94d
Author: Xiaocheng Hu <xiaochengh@chromium.org>
Date: Tue Jan 24 09:32:53 2023

[anchor-position] Turn a type-cast guard DCHECK hit into a CHECK

We have implemented CSS `anchor()` and `anchor-size` functions, but have
not implemented their Typed OM API. There's currently a DCHECK to
prevent debug builds from type-casting them into operation nodes.

This patch turns the DCHECK into CHECK so that non-debug builds are also
safe.

Note: This is just a temporary treatment during the development of the
CSS anchor positioning feature. We will turn it back into a DCHECK after
the Typed OM API is implemented.

Fixed: 1408993
Change-Id: I7ef38e2b41f5a5729e2bdaf5a335f39e4bda0868
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4189360
Auto-Submit: Xiaocheng Hu <xiaochengh@chromium.org>
Commit-Queue: Anders Hartvoll Ruud <andruud@chromium.org>
Reviewed-by: Anders Hartvoll Ruud <andruud@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1096075}

[modify] https://crrev.com/3b57c751b407cf0d3b26a9d8ab4bd2dadb7dc94d/third_party/blink/renderer/core/css/cssom/css_numeric_value.cc


### [Deleted User] (2023-01-24)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-24)

[Empty comment from Monorail migration]

### am...@google.com (2023-02-03)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-02-03)

Congratulations! The VRP Panel has decided to award you $7,000 for this report + $1,000 bisect. Thank you for your efforts and reporting this issue to us -- nice work! 

### am...@google.com (2023-02-04)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-05-02)

This issue was migrated from crbug.com/chromium/1408993?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062739)*
