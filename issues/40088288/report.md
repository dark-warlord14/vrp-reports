# Crash in __crt_stdio_output::output_processor<wchar_t,class __crt_stdio_output::string_ou

| Field | Value |
|-------|-------|
| **Issue ID** | [40088288](https://issues.chromium.org/issues/40088288) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Windows |
| **Reporter** | cl...@chromium.org |
| **Assignee** | ds...@chromium.org |
| **Created** | 2017-07-07 |
| **Bounty** | $3,500.00 |

## Description

Detailed report: https://clusterfuzz.com/testcase?key=5210209604861952

Fuzzer: attekett_surku_fuzzer
Job Type: windows_asan_chrome_no_sandbox
Platform Id: windows

Crash Type: UNKNOWN WRITE
Crash Address: 0x0030bdf0
Crash State:
  __crt_stdio_output::output_processor<wchar_t,class __crt_stdio_output::string_ou
  __crt_stdio_output::output_processor<wchar_t,class __crt_stdio_output::string_ou
  __crt_stdio_output::output_processor<wchar_t,class __crt_stdio_output::string_ou
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=windows_asan_chrome_no_sandbox&range=479886:479921

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5210209604861952


Issue filed automatically.

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

## Timeline

### ji...@chromium.org (2017-07-07)

Tops of the stack traces seem not in chromium code. Lower part of the stack traces suggests something related to pdfium. 

+component label internals>Plugins>PDF for now.

[Monorail components: Internals>Plugins>PDF]

### th...@chromium.org (2017-07-07)

[Empty comment from Monorail migration]

### th...@chromium.org (2017-07-07)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-07-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-07-08)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2017-07-08)

[Empty comment from Monorail migration]

### ji...@chromium.org (2017-07-10)

[Empty comment from Monorail migration]

### me...@chromium.org (2017-07-10)

Tom: Assigning to you so that this bug disappears from CF's burndown list, thanks.

### sh...@chromium.org (2017-07-11)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2017-07-11)

A friendly reminder that M61 branch is coming soon on 07/20! Your bug is labelled as Stable ReleaseBlock, pls make sure to land the fix ASAP to trunk. This way we branch M61 from a high quality trunk. Thank you.

### ts...@chromium.org (2017-07-11)

[Empty comment from Monorail migration]

### ds...@chromium.org (2017-07-12)

This is an existing issue, not a new regression, I'm not sure if the RB-Stable is required?

This also looks like it's a Windows crash, not PDFium specifically. We pass a format string with a %0.769x and we get a crash. I can repro with:


#include <stdlib.h>
#include <stdio.h>
#include <stdarg.h>

void test(wchar_t* format, ...) {
	va_list args;

	va_start(args, format);
	int len = vswprintf(nullptr, 0, format, args);
	fprintf(stderr, "Length %d\n", len);
}

int main(void) {
	test(L"%0.262x", 1);
	return 0;
}

Switching to 261 seems to run fine locally, 262 was the smallest number it crashed for me. "Exception thrown at 0x5D190AE3 (ucrtbased.dll) in ConsoleApplication1.exe: 0xC0000005: Access violation writing location 0x0030F614. occurred" is the windows error.

### br...@chromium.org (2017-07-12)

I wasn't totally comfortable with the use of "nullptr, 0" in the repro so I came up with this modified version:

  wchar_t buffer[1000];
  // This crashes sometimes. Maybe depending on ASLR and stack alignment?
  swprintf(buffer, sizeof(buffer) / sizeof(buffer[0]), L"%0.261x", 1);
  // This crashes:
  swprintf(buffer, sizeof(buffer) / sizeof(buffer[0]), L"%0.262x", 1);

The fact that the 0.261x case *sometimes* crashes is peculiar. But, the details of why are not crucial. I'm filing a VC++ bug and we'll have to work around this. Beware of going too close to the limit due to the apparent variability.

Note that this does not seem to happen with the sprintf (ASCII) family of functions, even with the buffer sizes more than doubled.

I wonder if the 261/260 limit is due to MAX_PATH = 260. Just a wild guess.


### br...@chromium.org (2017-07-12)

https://developercommunity.visualstudio.com/content/problem/79336/vswprintfswprintf-crash-with-0262x-format-string.html

And, because I like tiny tweetable bugs:
https://twitter.com/BruceDawson0xB/status/885225512066400256


### ds...@chromium.org (2017-07-12)

This is an existing bug that would also effect Stable so changing the Security_Impact, removing the Release block Stable as this isn't a regression but was just uncovered by the fuzzer.

### ds...@chromium.org (2017-07-12)

https://pdfium-review.googlesource.com/c/7630/

### bu...@chromium.org (2017-07-13)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/0c99829cc38ed2191a71d16c34278e391411aa1b

commit 0c99829cc38ed2191a71d16c34278e391411aa1b
Author: Dan Sinclair <dsinclair@chromium.org>
Date: Thu Jul 13 19:56:36 2017

Fix invalid write for util.printf

This CL fixes and invalid WRITE triggered by calling util.printf. We need to
verify that the integer format will be less then 260 characters.

Bug: chromium:740166
Change-Id: I1c9047101780582da5f39088568727e2c8b4c2d2
Reviewed-on: https://pdfium-review.googlesource.com/7630
Reviewed-by: Tom Sepez <tsepez@chromium.org>
Commit-Queue: dsinclair <dsinclair@chromium.org>

[modify] https://crrev.com/0c99829cc38ed2191a71d16c34278e391411aa1b/fpdfsdk/javascript/util.cpp
[add] https://crrev.com/0c99829cc38ed2191a71d16c34278e391411aa1b/testing/resources/javascript/bug_740166.in
[add] https://crrev.com/0c99829cc38ed2191a71d16c34278e391411aa1b/testing/resources/javascript/bug_740166_expected.txt


### ds...@chromium.org (2017-07-13)

Temporary fix landed. There is more cleanup to do in the util.printf code but the fix should handle this crash.

### ts...@chromium.org (2017-07-13)

[Empty comment from Monorail migration]

### cl...@chromium.org (2017-07-14)

ClusterFuzz has detected this issue as fixed in range 486499:486593.

Detailed report: https://clusterfuzz.com/testcase?key=5210209604861952

Fuzzer: attekett_surku_fuzzer
Job Type: windows_asan_chrome_no_sandbox
Platform Id: windows

Crash Type: UNKNOWN WRITE
Crash Address: 0x0030bdf0
Crash State:
  __crt_stdio_output::output_processor<wchar_t,class __crt_stdio_output::string_ou
  __crt_stdio_output::output_processor<wchar_t,class __crt_stdio_output::string_ou
  __crt_stdio_output::output_processor<wchar_t,class __crt_stdio_output::string_ou
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=windows_asan_chrome_no_sandbox&range=479886:479921
Fixed: https://clusterfuzz.com/revisions?job=windows_asan_chrome_no_sandbox&range=486499:486593

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5210209604861952


See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### sh...@chromium.org (2017-07-14)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-07-17)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/ffbc0d9a08f8443e67965f03dc0ae427c7f8d145

commit ffbc0d9a08f8443e67965f03dc0ae427c7f8d145
Author: Tom Sepez <tsepez@chromium.org>
Date: Mon Jul 17 16:44:06 2017

More tightly validate format strings in util.cpp.

Re-work the previous fix to be even more particular
about the input.

Bug: chromium:740166
Change-Id: I6bea3b6a6dd320a83f830b07afd52951be7d1b63
Reviewed-on: https://pdfium-review.googlesource.com/7691
Commit-Queue: Tom Sepez <tsepez@chromium.org>
Reviewed-by: dsinclair <dsinclair@chromium.org>

[modify] https://crrev.com/ffbc0d9a08f8443e67965f03dc0ae427c7f8d145/testing/resources/javascript/bug_740166_expected.txt
[modify] https://crrev.com/ffbc0d9a08f8443e67965f03dc0ae427c7f8d145/fpdfsdk/javascript/util.cpp
[modify] https://crrev.com/ffbc0d9a08f8443e67965f03dc0ae427c7f8d145/testing/resources/javascript/bug_740166.in
[modify] https://crrev.com/ffbc0d9a08f8443e67965f03dc0ae427c7f8d145/fpdfsdk/javascript/util_unittest.cpp


### aw...@chromium.org (2017-07-31)

[Empty comment from Monorail migration]

### aw...@google.com (2017-07-31)

Congratulations! The VRP Panel decided to award $3,500 for this bug! Cheers!

### aw...@chromium.org (2017-07-31)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-08-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-08-05)

This bug requires manual review: M61 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: amineer@(Android), cmasso@(iOS), ketakid@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2017-08-06)

+ awhalley@ (Security TPM) for M61 merge review.

### aw...@chromium.org (2017-08-07)

govind@ - Good for 61

### go...@chromium.org (2017-08-07)

Approving merge to M61 branch 3163 based on https://crbug.com/chromium/740166#c29. Please merge ASAP. Thank you.

### go...@chromium.org (2017-08-08)

No merge is needed here as both CLs listed at https://crbug.com/chromium/740166#c17 and #22 landed before M61 branch on July 20th. Hence, removing "Merge-Approved-61" label. 

### aw...@google.com (2017-09-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-10-22)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2017-10-22)

This issue was migrated from crbug.com/chromium/740166?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40088288)*
