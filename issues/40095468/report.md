# Security: UAF in OfflinePageAutoFetcher::CancelSchedule

| Field | Value |
|-------|-------|
| **Issue ID** | [40095468](https://issues.chromium.org/issues/40095468) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>Offline |
| **Platforms** | Android |
| **Reporter** | bt...@gmail.com |
| **Assignee** | mo...@google.com |
| **Created** | 2019-06-21 |
| **Bounty** | $10,000.00 |

## Description

**This template is ONLY for reporting security bugs. If you are reporting a**  

**Download Protection Bypass bug, please use the "Security - Download**  

**Protection" template. For all other reports, please use a different**  

**template.**

**Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com>**  

**/chromium/src/+/master/docs/security/faq.md**

**Please see the following link for instructions on filing security bugs:**  

**<https://www.chromium.org/Home/chromium-security/reporting-security-bugs>**

**Reports may be eligible for reward payments under the Chrome VRP:**  

**<http://g.co/ChromeBugRewards>**

**NOTE: Security bugs are normally made public once a fix has been widely**  

**deployed.**

**-------------------------**

**VULNERABILITY DETAILS**

OfflinePageAutoFetcherImpl is created with mojo::MakeStrongBinding so it is deleted on validation error. It takes a raw pointer to the RenderFrameHost, but does not observe its lifetime. When RenderFrameHost is destructed it destroys the interface, but messages can still be queued on the binding. When messages to call CancelSchedule go through that outlive the RFH, OfflinePageAutoFetcherImpl::CancelSchedule references the raw pointer to render\_frame\_host\_ resulting in a heap use-after-free in the browser process.

<https://cs.chromium.org/chromium/src/chrome/browser/offline_pages/android/offline_page_auto_fetcher.cc?l=67&rcl=755ff2f0f2edeb62178c248293af85dd128017f0>  

void OfflinePageAutoFetcher::Create(  

chrome::mojom::OfflinePageAutoFetcherRequest request,  

content::RenderFrameHost\* render\_frame\_host) {  

mojo::MakeStrongBinding(  

std::make\_unique<OfflinePageAutoFetcher>(render\_frame\_host), /\*\* Make Strong Binding with render\_frame\_host argument \*\*/  

std::move(request));  

}

<https://cs.chromium.org/chromium/src/chrome/browser/offline_pages/android/offline_page_auto_fetcher.cc?l=43&rcl=755ff2f0f2edeb62178c248293af85dd128017f0>  

OfflinePageAutoFetcher::OfflinePageAutoFetcher(  

content::RenderFrameHost\* render\_frame\_host)  

: render\_frame\_host\_(render\_frame\_host) {} /\*\* set render\_frame\_host\_ \*\*/

<https://cs.chromium.org/chromium/src/chrome/browser/offline_pages/android/offline_page_auto_fetcher.cc?l=60&rcl=755ff2f0f2edeb62178c248293af85dd128017f0>  

void OfflinePageAutoFetcher::CancelSchedule() {  

GetService()->CancelSchedule(render\_frame\_host\_->GetLastCommittedURL()); /\*\* dereference render\_fraem\_host\_ \*\*/  

}

**VERSION**  

Chrome Version: 77.0.3831.0 asan build  

Chrome Version: 75.0.3770.67 release build  

Operating System: Android <https://cs.chromium.org/chromium/src/chrome/browser/chrome_content_browser_client.cc?l=4574&rcl=4f4fbc8b684e25e17e8ed626ae022898f7a5eef2>  

Test Device 1: Android 9: Pixel3 Build/PQ2A.190205.001  

Test Device 2: Android 9: Pixel2 Build/PPR2.180905.005

**REPRODUCTION CASE**

Setup  

\* Build chromium for android and install chrome\_public\_apk  

\* Enable "command line flags on non rooted" to use MojoJS (<https://www.chromium.org/developers/how-tos/run-chromium-with-flags#TOC-Android>)  

\* Set the flag --enable-blink-features=MojoJS  

\* out/Pixel/bin/chrome\_public\_apk argv --args=' --enable-blink-features=MojoJS'  

\* Relaunch chromium and ensure enable-blink-features=MojoJS is enabled in chrome://version

Step 1  

Use my generated JS mojo bindings (should work with head)  

$ tar xvf repro.tar.gz  

or  

$ cp -r /path/to/chrome/.../out/Asan/gen .  

and generate the offline\_page\_auto\_fetcher.mojom.js file yourself by moving the mojom file to its own directory or grab it from codesearch <https://cs.chromium.org/chromium/src/out/android-Debug/gen/chrome/common/offline_page_auto_fetcher.mojom.js>

Step 2  

$ cd repro  

$ python -m SimpleHTTPServer 8000

Step 3  

Browse to hostname:8000/offline.html

Note: Research and Reproduction Steps based on issues/research by markbrand and dcheng  

(e.g. <https://bugs.chromium.org/p/chromium/issues/detail?id=922677> <https://bugs.chromium.org/p/chromium/issues/detail?id=913807>)

From that report “Note that this is \*not\* a renderer bug; it's a browser process bug that's reachable from the renderer. The attached poc is using the MojoJS bindings to trigger the issue, but a compromised renderer could perform the same actions without any special settings.”

Reproduction explanation:  

The main RFH allocates 16 child RFH using iframes. The child RFHs each allocate 2048 OfflinePageAutoFetcherImpl and send to cancelSchedule which clogs the mojo message pipe. The main RFH the removes all 16 child RFH, freeing them, then when the cancelSchedule messages are processed the UAF is triggered with the freed RFH. The main frame refreshes after 3 seconds to retry if failed.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser

=================================================================  

==28668==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x005a500b2480 at pc 0x007e9ba99e90 bp 0x007fe3b0c550 sp 0x007fe3b0c548  

READ of size 8 at 0x005a500b2480 thread T0 (chromium.chrome)  

#0 offline\_pages::OfflinePageAutoFetcher::GetService() ./../../chrome/browser/offline\_pages/android/offline\_page\_auto\_fetcher.cc:74  

#1 offline\_pages::OfflinePageAutoFetcher::CancelSchedule() ./../../chrome/browser/offline\_pages/android/offline\_page\_auto\_fetcher.cc:60  

#2 chrome::mojom::OfflinePageAutoFetcherStubDispatch::Accept(chrome::mojom::OfflinePageAutoFetcher\*, mojo::Message\*) ./gen/chrome/common/offline\_page\_auto\_fetcher.mojom.cc:294  

#3 mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:437  

#4 mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper\*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner\*) ./../../mojo/public/cpp/bindings/lib/multiplex\_router.cc:873  

#5 mojo::internal::MultiplexRouter::Accept(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/multiplex\_router.cc:594  

#6 mojo::Connector::DispatchMessage(mojo::Message) ./../../mojo/public/cpp/bindings/lib/connector.cc:509  

#7 mojo::Connector::DispatchNextMessageInQueue() ./../../mojo/public/cpp/bindings/lib/connector.cc:539  

#8 base::OnceCallback<void ()>::Run() && ./../../base/callback.h:97  

#9 base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence\_manager::LazyNow\*, bool\*) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:368  

#10 base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoSomeWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:219  

#11 base::MessagePumpForUI::OnNonDelayedLooperCallback() ./../../base/message\_loop/message\_pump\_android.cc:194  

#12 base::(anonymous namespace)::NonDelayedLooperCallback(int, int, void\*) ./../../base/message\_loop/message\_pump\_android.cc:70  

#13 0x7f46fda474 (/system/lib64/libutils.so+0x14474)  

#14 0x7f46fda08c (/system/lib64/libutils.so+0x1408c)  

#15 0x7f43f6dc2c (/system/lib64/libandroid\_runtime.so+0x120c2c)  

#16 0x74c2352c (/dev/ashmem/dalvik-jit-code-cache (deleted)+0x2352c)

Address 0x005a500b2480 is a wild pointer.  

SUMMARY: AddressSanitizer: heap-buffer-overflow (/data/app/org.chromium.chrome-YCh\_CcosiyTVJnU2-DFZBQ==/lib/arm64/libchrome.so+0x1337fe8c)  

Shadow bytes around the buggy address:  

0x001b4a016440: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x001b4a016450: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x001b4a016460: 00 00 00 00 00 00 00 00 00 fa fa fa fa fa fa fa  

0x001b4a016470: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x001b4a016480: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

=>0x001b4a016490:[fa]fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x001b4a0164a0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x001b4a0164b0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x001b4a0164c0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x001b4a0164d0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x001b4a0164e0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

Shadow byte legend (one shadow byte represents 8 application bytes):  

Addressable: 00  

Partially addressable: 01 02 03 04 05 06 07  

Heap left redzone: fa  

Freed heap region: fd  

Stack left redzone: f1  

Stack mid redzone: f2  

Stack right redzone: f3  

Stack after return: f5  

Stack use after scope: f8  

Global redzone: f9  

Global init order: f6  

Poisoned by user: f7  

Container overflow: fc  

Array cookie: ac  

Intra object redzone: bb  

ASan internal: fe  

Left alloca redzone: ca  

Right alloca redzone: cb  

Shadow gap: cc  

==28668==ABORTING

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Brendon Tiszka

## Attachments

- [repro.tar.gz](attachments/repro.tar.gz) (application/octet-stream, 806.4 KB)

## Timeline

### me...@chromium.org (2019-06-21)

[Empty comment from Monorail migration]

### cl...@chromium.org (2019-06-21)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6195474368954368.

### cl...@chromium.org (2019-06-21)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5726688553598976.

### cl...@chromium.org (2019-06-21)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4845922000961536.

### cl...@chromium.org (2019-06-21)

[Comment Deleted]

### cl...@chromium.org (2019-06-21)

[Comment Deleted]

### cl...@chromium.org (2019-06-21)

Testcase 4845922000961536 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=4845922000961536.

### bt...@gmail.com (2019-06-21)

metzman: Is there anything I can change in my testcase be more compatible with linux_asan_chrome_mojo? I'm unable to see linux_asan_chrome_mojo jobs with similar root causes (like 913807). My repro was also only tested on Pixel2/Pixel3 devices.

### bt...@gmail.com (2019-06-21)

Or the andorid equivalent of linux_asan_chrome_mojo

### cl...@chromium.org (2019-06-21)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5938092858540032.

### me...@chromium.org (2019-06-21)

Sorry the testcase only failed to repro once because I messed up the command line arguments, the other times I canceled because of other things I messed up. Aplogies for the spam!

### cl...@chromium.org (2019-06-22)

This crash occurs very frequently on android platform and is likely preventing the fuzzer  from making much progress. Fixing this will allow more bugs to be found.

Marking this bug as a blocker for next Beta release.

If this is incorrect, please add ClusterFuzz-Wrong label and remove the ReleaseBlock-Beta label.

### me...@chromium.org (2019-06-24)

^The above comment is wrong, ClusterFuzz is hitting some other bug on Android.
I'm still unable to reproduce yours, I'll see if I can on an actual device.

### me...@chromium.org (2019-06-24)

[Empty comment from Monorail migration]

### me...@chromium.org (2019-06-25)

I'm having trouble running this on device but from the looks of it, asan on Chrome might be having issues now. 

### bt...@gmail.com (2019-06-25)

[Comment Deleted]

### bt...@gmail.com (2019-06-25)

[Comment Deleted]

### bt...@gmail.com (2019-06-25)

[Comment Deleted]

### cl...@chromium.org (2019-06-25)

Testcase 4845922000961536 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=4845922000961536.

### cl...@chromium.org (2019-06-25)

ClusterFuzz testcase 4845922000961536 appears to be flaky, updating reproducibility label.

### bt...@gmail.com (2019-06-26)

[Comment Deleted]

### me...@chromium.org (2019-06-26)

Thanks for the detailed instructions they helped me get Chrome running with what I believe are the right flags. 
I'm still unable get a crash though. Sorry. How long does the crash take without ASAN?

harringtond@ or carlosk@ could you please take a look? Thanks!

### me...@chromium.org (2019-06-26)

[Empty comment from Monorail migration]

### ha...@google.com (2019-06-26)

Ah, I think this explains another crash: https://bugs.chromium.org/p/chromium/issues/detail?id=978951

I'll start working on a fix

### bt...@gmail.com (2019-06-27)

[Comment Deleted]

### sh...@chromium.org (2019-06-27)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-06-27)

[Empty comment from Monorail migration]

### bt...@gmail.com (2019-06-27)

[Comment Deleted]

### bt...@gmail.com (2019-06-27)

[Comment Deleted]

### jd...@chromium.org (2019-06-27)

[Empty comment from Monorail migration]

[Monorail components: UI>Browser>Offline]

### bt...@gmail.com (2019-06-27)

[Comment Deleted]

### sh...@chromium.org (2019-07-05)

harringtond: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-07-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/2914cfb4789e72ba5318f1aae06be36b0eed6c2b

commit 2914cfb4789e72ba5318f1aae06be36b0eed6c2b
Author: Dan Harrington <harringtond@chromium.org>
Date: Mon Jul 08 17:37:33 2019

Fix crash in OfflinePageAutoFetcher

Lifetime of RenderFrameHost was not properly maintained.

Bug: 977462

Change-Id: I66c16fa397a42c778b22bb1ad8909a3b1cf1b41f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1679551
Commit-Queue: Dan H <harringtond@chromium.org>
Reviewed-by: Cathy Li <chili@chromium.org>
Reviewed-by: Jonathan Metzman <metzman@chromium.org>
Cr-Commit-Position: refs/heads/master@{#675278}

[modify] https://crrev.com/2914cfb4789e72ba5318f1aae06be36b0eed6c2b/chrome/browser/offline_pages/android/offline_page_auto_fetcher.cc
[modify] https://crrev.com/2914cfb4789e72ba5318f1aae06be36b0eed6c2b/chrome/browser/offline_pages/android/offline_page_auto_fetcher.h
[modify] https://crrev.com/2914cfb4789e72ba5318f1aae06be36b0eed6c2b/chrome/renderer/net/net_error_helper_core.cc
[modify] https://crrev.com/2914cfb4789e72ba5318f1aae06be36b0eed6c2b/chrome/renderer/net/net_error_helper_core_unittest.cc
[modify] https://crrev.com/2914cfb4789e72ba5318f1aae06be36b0eed6c2b/chrome/renderer/net/page_auto_fetcher_helper_android.cc
[modify] https://crrev.com/2914cfb4789e72ba5318f1aae06be36b0eed6c2b/chrome/renderer/net/page_auto_fetcher_helper_android.h


### ha...@google.com (2019-07-08)

This *should* be fixed, but I wasn't able to reproduce, so can't verify.

### bt...@gmail.com (2019-07-09)

[Comment Deleted]

### sh...@chromium.org (2019-07-09)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-07-09)

Requesting merge to M76 because latest trunk commit (675278) appears to be after beta branch point (665002).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-07-09)

This bug requires manual review: M76 has already been promoted to the beta branch, so this requires manual review
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://goto.google.com/chrome-release-branch-merge-guidelines
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: govind@(Android), kariahda@(iOS), cindyb@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2019-07-09)

+awhalley@ (Security TPM) for M76 merge review as adetaylor@ is OOO.

### aw...@google.com (2019-07-09)

Thanks for the fix, harringtond@. Would you have any qualms if we merged this to 76 today so we can make this week’s Beta, given it’s only had a day on canary?

### ha...@google.com (2019-07-09)

I think that's fine. We can turn off the feature causing the crash with finch if there are unintended consequences in the fix.

### go...@chromium.org (2019-07-09)

Approving merge to M76 branch 3809 based on https://crbug.com/chromium/977462#c40  & #41. Please merge now. Thank you.

### cr...@appspot.gserviceaccount.com (2019-07-09)

The following revision refers to this bug: 
https://chromium.googlesource.com/chromium/src.git/+/7d25c892984a4bc6c782d4b43ce4b838967640d0

Commit: 7d25c892984a4bc6c782d4b43ce4b838967640d0
Author: harringtond@chromium.org
Commiter: harringtond@chromium.org
Date: 2019-07-09 18:04:34 +0000 UTC

Fix crash in OfflinePageAutoFetcher [M76 merge]

Lifetime of RenderFrameHost was not properly maintained.

Bug: 977462

(cherry picked from commit 2914cfb4789e72ba5318f1aae06be36b0eed6c2b)

Change-Id: I66c16fa397a42c778b22bb1ad8909a3b1cf1b41f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1679551
Commit-Queue: Dan H <harringtond@chromium.org>
Reviewed-by: Cathy Li <chili@chromium.org>
Reviewed-by: Jonathan Metzman <metzman@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#675278}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1691857
Reviewed-by: Dan H <harringtond@chromium.org>
Cr-Commit-Position: refs/branch-heads/3809@{#791}
Cr-Branched-From: d82dec1a818f378c464ba307ddd9c92133eac355-refs/heads/master@{#665002}


### go...@chromium.org (2019-07-09)

This is merged to M76 - https://chromium.googlesource.com/chromium/src.git/+/7d25c892984a4bc6c782d4b43ce4b838967640d0

### na...@google.com (2019-07-15)

[Empty comment from Monorail migration]

### cl...@chromium.org (2019-07-15)

ClusterFuzz testcase 5938092858540032 is still reproducing on tip-of-tree build (trunk).

Please re-test your fix against this testcase and if the fix was incorrect or incomplete, please re-open the bug. Otherwise, ignore this notification and add ClusterFuzz-Wrong label.

### ha...@google.com (2019-07-15)

https://clusterfuzz.com/testcase-detail/5938092858540032

Looks like this is a different crash, re-opening the bug.

### sh...@chromium.org (2019-07-16)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bt...@gmail.com (2019-07-16)

[Comment Deleted]

### bt...@gmail.com (2019-07-16)

Hey Natasha, Andrew. Please double this up for charity like usual if it is eligible for a reward :). 33% Amnesty International, 33% EFF, and 33% Against Malaria Foundation.

### aw...@google.com (2019-07-17)

Thanks btiszka@! +natashapabrai to note this after the panel meets.

### bt...@gmail.com (2019-07-17)

[Comment Deleted]

### bt...@gmail.com (2019-07-17)

[Comment Deleted]

### na...@google.com (2019-07-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### pa...@chromium.org (2019-07-17)

Nice one! The Panel decided to reward $10,000 for this report!

### na...@google.com (2019-07-18)

[Empty comment from Monorail migration]

### bt...@gmail.com (2019-07-19)

[Comment Deleted]

### ad...@google.com (2019-07-29)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-07-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-23)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@chromium.org (2019-11-23)

[Empty comment from Monorail migration]

### bt...@gmail.com (2020-04-18)

[Comment Deleted]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/977462?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/977195]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095468)*
