# Security: use-after-free in payment app 

| Field | Value |
|-------|-------|
| **Issue ID** | [40095942](https://issues.chromium.org/issues/40095942) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Unknown |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | da...@chromium.org |
| **Created** | 2019-08-09 |
| **Bounty** | $500.00 |

## Description

Chrome Version: 78.0.3877.0 (Official Build) canary (64-bit)  

Operating System: All

**REPRODUCTION CASE**

1. Lunch Chrome
2. Open a new incognito window and open the test case
3. Click on pay
4. After 2 seconds close the window

rax=feeefeeefeeefeee rbx=000000000091e600 rcx=0000000020c51450  

rdx=000007feea6b8c10 rsi=0000000020c51440 rdi=0000000020c51440  

rip=000007fee75a3633 rsp=000000000091e5d8 rbp=000000000091e718  

r8=0000000020c51450 r9=0000000000000000 r10=000007feea5aa53a  

r11=8101010101010100 r12=0000000000000000 r13=0000000020de4eb8  

r14=00000000fefefe01 r15=000000000091e690  

iopl=0 nv up ei pl zr na po nc  

cs=0033 ss=002b ds=002b es=002b fs=0053 gs=002b efl=00010246  

chrome\_7fee74c0000!base::SupportsUserData::GetUserData+0x13:  

000007fe`e75a3633 48395020 cmp qword ptr [rax+20h],rdx ds:feeefeee`feeeff0e=????????????????  

0:000> k  

Child-SP RetAddr Call Site  

00000000`0091e5d8 000007fe`e7f158d8 chrome\_7fee74c0000!base::SupportsUserData::GetUserData+0x13 [c:\b\s\w\ir\cache\builder\src\base\supports\_user\_data.cc @ 23]  

00000000`0091e5e0 000007fe`e76fd387 chrome\_7fee74c0000!content::`anonymous namespace'::GetStoragePartitionMap+0x24 [c:\b\s\w\ir\cache\builder\src\content\browser\browser_context.cc @ 193] 00000000`0091e630 000007fe`e80ff29f chrome_7fee74c0000!content::BrowserContext::GetStoragePartitionForSite+0x85 [c:\b\s\w\ir\cache\builder\src\content\browser\browser_context.cc @ 449] 00000000`0091e6f0 000007fe`e80ffb39 chrome_7fee74c0000!content::`anonymous namespace'::GetDevTools+0x3c [c:\b\s\w\ir\cache\builder\src\content\browser\payments\payment\_app\_provider\_impl.cc @ 491]  

00000000`0091e7b0 000007fe`e8102b7f chrome\_7fee74c0000!content::`anonymous namespace'::OnResponseForPaymentRequestOnUiThread+0x4e [c:\b\s\w\ir\cache\builder\src\content\browser\payments\payment_app_provider_impl.cc @ 549] 00000000`0091eaa0 000007fe`e8102ae5 chrome_7fee74c0000!base::internal::FunctorTraits<void (\*)(content::BrowserContext \*, long long, const url::Origin &, const std::__1::basic_string<char> &, base::OnceCallback<void (mojo::InlinedStructPtr<payments::mojom::PaymentHandlerResponse>)>, mojo::InlinedStructPtr<payments::mojom::PaymentHandlerResponse>),void>::Invoke<void (\*)(content::BrowserContext \*, long long, const url::Origin &, const std::__1::basic_string<char> &, base::OnceCallback<void (mojo::InlinedStructPtr<payments::mojom::PaymentHandlerResponse>)>, mojo::InlinedStructPtr<payments::mojom::PaymentHandlerResponse>),content::BrowserContext \*,long long,url::Origin,std::__1::basic_string<char>,base::OnceCallback<void (mojo::InlinedStructPtr<payments::mojom::PaymentHandlerResponse>)>,mojo::InlinedStructPtr<payments::mojom::PaymentHandlerResponse> >+0x93 [c:\b\s\w\ir\cache\builder\src\base\bind_internal.h @ 399] 00000000`0091eb70 000007fe`e8102857 chrome_7fee74c0000!base::internal::Invoker<base::internal::BindState<void (\*)(content::BrowserContext \*, long long, const url::Origin &, const std::__1::basic_string<char> &, base::OnceCallback<void (mojo::InlinedStructPtr<payments::mojom::PaymentHandlerResponse>)>, mojo::InlinedStructPtr<payments::mojom::PaymentHandlerResponse>),content::BrowserContext \*,long long,url::Origin,std::__1::basic_string<char>,base::OnceCallback<void (mojo::InlinedStructPtr<payments::mojom::PaymentHandlerResponse>)> >,void (mojo::InlinedStructPtr<payments::mojom::PaymentHandlerResponse>)>::RunOnce+0x3d [c:\b\s\w\ir\cache\builder\src\base\bind_internal.h @ 645] 00000000`0091ebc0 000007fe`e7501e61 chrome_7fee74c0000!base::internal::FunctorTraits<base::OnceCallback<void (mojo::InlinedStructPtr<payments::mojom::PaymentHandlerResponse>)>,void>::Invoke<base::OnceCallback<void (mojo::InlinedStructPtr<payments::mojom::PaymentHandlerResponse>)>,mojo::InlinedStructPtr<payments::mojom::PaymentHandlerResponse> >+0x53 [c:\b\s\w\ir\cache\builder\src\base\bind_internal.h @ 560] 00000000`0091ec50 000007fe`e74ff695 chrome_7fee74c0000!base::TaskAnnotator::RunTask+0x121 [c:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc @ 142] 00000000`0091ed50 000007fe`e74ff3f1 chrome_7fee74c0000!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl+0x185 [c:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc @ 366] 00000000`0091ef20 000007fe`e756f814 chrome_7fee74c0000!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoSomeWork+0x61 [c:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc @ 221] 00000000`0091efb0 000007fe`e7506f0e chrome_7fee74c0000!base::MessagePumpForUI::DoRunLoop+0xc4 [c:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc @ 218] 00000000`0091f070 000007fe`e74ff246 chrome_7fee74c0000!base::MessagePumpWin::Run+0x4e [c:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc @ 76] 00000000`0091f0c0 000007fe`e74febce chrome_7fee74c0000!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run+0x86 [c:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc @ 463] 00000000`0091f110 000007fe`e778a6c5 chrome_7fee74c0000!base::RunLoop::RunWithTimeout+0x1ae [c:\b\s\w\ir\cache\builder\src\base\run_loop.cc @ 162] 00000000`0091f1c0 000007fe`e778a5a1 chrome_7fee74c0000!ChromeBrowserMainParts::MainMessageLoopRun+0x53 [c:\b\s\w\ir\cache\builder\src\chrome\browser\chrome_browser_main.cc @ 1873] 00000000`0091f250 000007fe`e778a55f chrome_7fee74c0000!content::BrowserMainLoop::RunMainMessageLoopParts+0x35 [c:\b\s\w\ir\cache\builder\src\content\browser\browser_main_loop.cc @ 1000] 00000000`0091f2d0 000007fe`e7518aac chrome_7fee74c0000!content::BrowserMainRunnerImpl::Run+0x11 [c:\b\s\w\ir\cache\builder\src\content\browser\browser_main_runner_impl.cc @ 150] 00000000`0091f300 000007fe`e75189ce chrome_7fee74c0000!content::BrowserMain+0xc5 [c:\b\s\w\ir\cache\builder\src\content\browser\browser_main.cc @ 47] 00000000`0091f3a0 000007fe`e74ccd28 chrome\_7fee74c0000!content::RunBrowserProcessMain+0x59 [c:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc @ 544]

## Attachments

- [screen.mp4](attachments/screen.mp4) (video/mp4, 966.7 KB)
- [payment.html](attachments/payment.html) (text/plain, 1.1 KB)

## Timeline

### ke...@chromium.org (2019-08-09)

Thanks for the report.

danyao@: PTAL to help triage? This is a P0 regression.

With DCHECKs on it, this check fails: https://cs.chromium.org/chromium/src/ui/views/view.h?l=407&rcl=60f081c179bbfbfad7992fd3f5687b40e63684cc

Browser process crash ID from Mac Canary: ecdd51df3e54c1a8

Also repro'd on Windows Canary and Beta.

From a brief look at the crash in a Windows debugger, it appears that StoragePartitionMapImpl has a stale browser_context_ pointer, presumably corresponding to the closed Incognito window. https://cs.chromium.org/chromium/src/content/browser/storage_partition_impl_map.cc?l=349&rcl=0eeeebdc38851814ce56daf3bf07eb9f63f44afc

[Monorail components: UI>Browser>Payments]

### da...@chromium.org (2019-08-09)

rouslan@ - can you help take a look?

### ro...@google.com (2019-08-09)

This is the browser_context that is no longer valid:

https://cs.chromium.org/chromium/src/content/browser/payments/payment_app_provider_impl.cc?rcl=2ed0143143954978ab50bffa59943208a6f658f2&l=545

Since the window is closing, ideally this code would never be invoked. Need to think about the right way to prevent this code from triggering. 

### da...@chromium.org (2019-08-09)

Bisect found this range https://chromium.googlesource.com/chromium/src/+log/1c910ad0598eed95537945202add57e27b3c30eb..914d393376d93fa58847ee2395c0e19c47284a98
Confirmed that the regression is introduced in https://chromium-review.googlesource.com/c/chromium/src/+/1687795

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-08-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/1f3d381e1f42a45e48aa649ee942741828a40a0d

commit 1f3d381e1f42a45e48aa649ee942741828a40a0d
Author: Danyao Wang <danyao@chromium.org>
Date: Fri Aug 09 22:24:35 2019

Revert "[Web Payment][DevTools] Log payment handler responses."

This reverts commit 533cba7f1f167ac4dd4c8b3b4a86bbb695fc90fd.

Reason for revert: This introduced a new use-after-free case.
See crbug/992285

Original change's description:
> [Web Payment][DevTools] Log payment handler responses.
> 
> Bug: 980249
> Change-Id: Ia90333263e0fb5e8253c8897f3e53967e32015d0
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1687795
> Commit-Queue: Rouslan Solomakhin <rouslan@chromium.org>
> Reviewed-by: Sahel Sharify <sahel@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#675663}

TBR=rouslan@chromium.org,sahel@chromium.org

# Not skipping CQ checks because original CL landed > 1 day ago.

Bug: 980249,992285
Change-Id: I83678cf4c1a3ea94fde6ca094db6e5775d6c10f4
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1746959
Reviewed-by: Danyao Wang <danyao@chromium.org>
Commit-Queue: Danyao Wang <danyao@chromium.org>
Cr-Commit-Position: refs/heads/master@{#685758}

[modify] https://crrev.com/1f3d381e1f42a45e48aa649ee942741828a40a0d/content/browser/payments/payment_app_provider_impl.cc


### da...@chromium.org (2019-08-09)

[Empty comment from Monorail migration]

### bu...@chromium.org (2019-08-09)

[Auto-generated comment by a script] We noticed that this issue is targeted for M-77; it appears the fix may have landed after branch point, meaning a merge might be required. The owner of this bug should confirm if a merge is required here. If so, add Merge-Request-77 label and indicate which commits/CLs are to be merged. Otherwise, remove Merge-TBD label. Thanks.

### sh...@chromium.org (2019-08-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-08-10)

Not requesting merge to beta (M77) because latest trunk commit (675663) appears to be prior to beta branch point (681094). If this is incorrect, please replace the Merge-na label with Merge-Request-77. If other changes are required to fix this bug completely, please request a merge if necessary.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ro...@google.com (2019-08-10)

Sheriffbot looked at the wrong trunk commit. Should be looking at 685758 instead. Need a merge.

### sh...@chromium.org (2019-08-10)

This bug requires manual review: Reverts referenced in bugdroid comments after merge request.
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
Owners: benmason@(Android), kariahda@(iOS), dgagnon@(ChromeOS), lakpamarthy@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@gmail.com (2019-08-10)

[Comment Deleted]

### ro...@chromium.org (2019-08-12)

1. Tes, it's a crash fix.
2. https://crrev.com/1f3d381e1f42a45e48aa649ee942741828a40a0d
3. Yes.
4. To fix a crash.
5. Not a new feature. A revert of a new feature.
6. N/A.

### ro...@chromium.org (2019-08-12)

s/Tes/Yes/g

### na...@google.com (2019-08-12)

[Empty comment from Monorail migration]

### ro...@chromium.org (2019-08-13)

[Empty comment from Monorail migration]

### la...@chromium.org (2019-08-13)

merge approved for M77 branch 3865

### ro...@chromium.org (2019-08-13)

Manually applying the merged label, since it appears that commit bot does not have permissions to access this bug report. The merge:

https://crrev.com/ce0f4a101d78085707e8c9561ee793c912b1f20e

### na...@google.com (2019-08-14)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-08-14)

Congrats! The Panel decided to reward $500 for this report!

### na...@google.com (2019-08-14)

[Empty comment from Monorail migration]

### na...@google.com (2019-08-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-08-15)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ro...@chromium.org (2019-08-20)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-11-16)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2019-11-16)

This issue was migrated from crbug.com/chromium/992285?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095942)*
