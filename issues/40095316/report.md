# UAF in chrome!content::Portal::Activate

| Field | Value |
|-------|-------|
| **Issue ID** | [40095316](https://issues.chromium.org/issues/40095316) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Blink>Portals |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | pa...@blackowlsec.com |
| **Assignee** | lf...@chromium.org |
| **Created** | 2019-06-06 |
| **Bounty** | $8,000.00 |

## Description

**VULNERABILITY DETAILS**  

Use-After-Free in chrome!content::Portal::Activate+0xc1 [C:\b\c\b\win64\_clang\src\content\browser\portal\portal.cc @ 195

==58576==ERROR: AddressSanitizer: heap-use-after-free on address 0x119bdfe95280 at pc 0x7ffd21aea585 bp 0x00593c9fe4a0 sp 0x00593c9fe4e8  

READ of size 8 at 0x119bdfe95280 thread T0  

#0 0x7ffd21aea584 in content::Portal::Activate(struct blink::TransferableMessage,class base::OnceCallback<void (bool)>) C:\b\swarming\w\ir\cache\builder\src\content\browser\portal\portal.cc:195:44  

[...]

Tested with PageHeap enabled.

For reproducing the case it is required to enable portals (chrome://flags/#enable-portals).

Does not reproduce reliably, seems there is a timing factor involved. Due to that i have failed to fully minimize the testcase, got it down from 500kb to 60kb, managed to minimize almost everything except the code in the eventhandler5().

**VERSION**  

Chrome Version: Tested on 76.0.3806.1 dev  

Operating System: Windows 10 x64

**REPRODUCTION CASE**  

attached ASAN and windbg logs included.

## Attachments

- [cm_portal3_asan.txt](attachments/cm_portal3_asan.txt) (text/plain, 18.0 KB)
- [cm_portal3_windbg.txt](attachments/cm_portal3_windbg.txt) (text/plain, 6.6 KB)
- [cm_portal3.html](attachments/cm_portal3.html) (text/plain, 63.9 KB)

## Timeline

### wf...@chromium.org (2019-06-06)

Thanks for your report. Initial triage.

[Monorail components: Blink>HTML>Portal]

### cl...@chromium.org (2019-06-06)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6514329641418752.

### wf...@chromium.org (2019-06-06)

[Empty comment from Monorail migration]

### wf...@chromium.org (2019-06-06)

this is in browser, but in a feature disabled by default, so it's pri-0 critical but security impact none. lfg@ can you take a look at this at your earliest convenience?

### cl...@chromium.org (2019-06-06)

Detailed report: https://clusterfuzz.com/testcase?key=6514329641418752

Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x61d000185680
Crash State:
  content::Portal::Activate
  blink::mojom::PortalStubDispatch::AcceptWithResponder
  blink::mojom::PortalStub<mojo::RawPtrImplRefTraits<blink::mojom::Portal> >::Acce
  
Sanitizer: address (ASAN)

Recommended Security Severity: Critical

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=661980:661986

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6514329641418752

See https://github.com/google/clusterfuzz-tools for instructions to reproduce this bug locally.

### sh...@chromium.org (2019-06-07)

Setting milestone and target because of Security_Impact=Head and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-06-07)

This is a critical security issue. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### lf...@chromium.org (2019-06-07)

[Empty comment from Monorail migration]

### lf...@chromium.org (2019-06-07)

[Empty comment from Monorail migration]

### cl...@chromium.org (2019-06-09)

ClusterFuzz has detected this issue as fixed in range 667469:667470.

Detailed report: https://clusterfuzz.com/testcase?key=6514329641418752

Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x61d000185680
Crash State:
  content::Portal::Activate
  blink::mojom::PortalStubDispatch::AcceptWithResponder
  blink::mojom::PortalStub<mojo::RawPtrImplRefTraits<blink::mojom::Portal> >::Acce
  
Sanitizer: address (ASAN)

Recommended Security Severity: Critical

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=661980:661986
Fixed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=667469:667470

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6514329641418752

See https://github.com/google/clusterfuzz-tools for instructions to reproduce this bug locally.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2019-06-09)

ClusterFuzz testcase 6514329641418752 is verified as fixed, so closing issue as verified.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### sh...@chromium.org (2019-06-10)

[Empty comment from Monorail migration]

### lf...@chromium.org (2019-06-10)

[Empty comment from Monorail migration]

### cr...@chromium.org (2019-06-13)

For reference, the UaF looks like it's on this line of Portal::Activate:

bool is_loading = portal_contents_impl_->IsLoading();

(Is that correct?)

### lf...@chromium.org (2019-06-14)

Yes, that is correct. I've added an explanation in the CL https://chromium-review.googlesource.com/c/chromium/src/+/1649410 here about the causes of the UaF.

### lf...@chromium.org (2019-06-17)

[Empty comment from Monorail migration]

### lf...@chromium.org (2019-06-20)

CL landed in https://chromium-review.googlesource.com/c/chromium/src/+/1649410 , looks like bugdroid didn't pick it up.

### lf...@chromium.org (2019-06-20)

[Empty comment from Monorail migration]

### lf...@chromium.org (2019-06-20)

[Empty comment from Monorail migration]

### na...@google.com (2019-06-24)

[Empty comment from Monorail migration]

### na...@google.com (2019-07-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-07-17)

Congrats the Panel decided to reward $8,000 for this report ($5,000 - sandbox escape + $3,000 - RCE) 

Additionally - please let us know how you would like to be credited in the release notes. 

### pa...@blackowlsec.com (2019-07-18)

thank you !
Regarding credits - "Pawel Wylecial of REDTEAM.PL"

### na...@google.com (2019-07-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-09-27)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mm...@chromium.org (2020-01-07)

lfg@, thank you for fixing this issue. Chrome Security team needs your knowledge to prevent that whole class of bugs from happening elsewhere. We would greatly appreciate if you could tell us more about the issue by filling out the following form: https://forms.gle/VWKDUv9a8GXCCRWm7

### mm...@chromium.org (2020-01-09)

[Empty comment from Monorail migration]

### ef...@google.com (2020-10-12)

[Empty comment from Monorail migration]

[Monorail components: Blink>Portals]

### ef...@google.com (2020-10-12)

[Empty comment from Monorail migration]

[Monorail components: -Blink>HTML>Portal]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/971702?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail blocking: crbug.com/chromium/968142]
[Monorail mergedwith: crbug.com/chromium/968142]
[Monorail components added to Component Tags custom field.]

### ti...@chromium.org (2024-06-27)

Adding `ClusterFuzz-Ignore` hotlist to all `ClusterFuzz-Wrong` issues per crbug.com/40285975.

### ti...@chromium.org (2024-06-27)

Adding `ClusterFuzz-Ignore` hotlist to all `ClusterFuzz-Wrong` issues per crbug.com/40285975.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095316)*
