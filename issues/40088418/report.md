# v8 fuzzing - 1146 - invalid memory access

| Field | Value |
|-------|-------|
| **Issue ID** | [40088418](https://issues.chromium.org/issues/40088418) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink, Blink>JavaScript |
| **Reporter** | sk...@chromium.org |
| **Assignee** | mo...@google.com |
| **Created** | 2011-03-02 |
| **Bounty** | $1,000.00 |

## Description

Upstream http://code.google.com/p/v8/issues/detail?id=1146

JSchuch: invalid memory access

## Timeline

### sk...@chromium.org (2011-03-02)

[Empty comment from Monorail migration]

### sk...@chromium.org (2011-03-02)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-03-02)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-03-03)

Crashes in M9
https://crash/reportdetail?reportid=3a4d6f7295a5e9cf

Thread 0 *CRASHED* ( SIGSEGV @ 0x00000007 )

0x00a01460			
0x00a00bda			
0x009faa58			
0x009eb421			
0x08b1248f	 [chrome	 - v8/src/execution.cc:94]	v8::internal::Invoke
0x08b12983	 [chrome	 - v8/src/execution.cc:121]	v8::internal::Execution::Call
0x08ae0593	 [chrome	 - v8/src/api.cc:1299]	v8::Script::Run
0x094314d1	 [chrome	 - third_party/WebKit/WebCore/bindings/v8/V8Proxy.cpp:421]	WebCore::V8Proxy::runScript
0x09431809	 [chrome	 - third_party/WebKit/WebCore/bindings/v8/V8Proxy.cpp:375]	WebCore::V8Proxy::evaluate

### sc...@gmail.com (2011-03-03)

Manifests in M9; fixed in M10

### sc...@gmail.com (2011-03-03)

[Empty comment from Monorail migration]

### er...@gmail.com (2011-03-03)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-03-10)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-03-16)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-03-16)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-03-30)

Invoice finalized; payment is in e-payment system; it can take a couple of weeks.

### sc...@gmail.com (2011-03-30)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-10-05)

Batch update.

### js...@chromium.org (2012-04-18)

Lifting view restrictions.

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

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

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-26)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-26)

This issue was migrated from crbug.com/chromium/74675?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink, Blink>JavaScript]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40088418)*
