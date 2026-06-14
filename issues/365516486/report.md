# UaF in LensOverlayBlurLayerDelegate::FetchBackgroundImage

| Field | Value |
|-------|-------|
| **Issue ID** | [365516486](https://issues.chromium.org/issues/365516486) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser |
| **Platforms** | Linux, Mac, Windows |
| **Chrome Version** | 130.0.6706.0 |
| **Reporter** | ch...@gmail.com |
| **Assignee** | me...@google.com |
| **Created** | 2024-09-09 |
| **Bounty** | $2,000.00 |

## Description

# Steps to reproduce the problem

1. Open google.com/chrome twice in the same tab
2. Click on "Google Lens" inside the search box
3. Double click to go back

# Problem Description

```

void LensOverlayBlurLayerDelegate::FetchBackgroundImage() {
  if (!background_view_) {
    return;
  }
  auto size = background_view_->GetViewBounds().size();                                // Crash
  auto quality = lens::features::GetLensOverlayCustomBlurQuality();
  background_view_->CopyFromSurface(
      /*src_rect=*/gfx::Rect(),
      /*output_size=*/
      gfx::Size(size.width() * quality, size.height() * quality),
      base::BindOnce(&LensOverlayBlurLayerDelegate::UpdateBackgroundImage,
                     weak_factory_.GetWeakPtr()));
}

```
# Summary

UaF in LensOverlayBlurLayerDelegate::FetchBackgroundImage

# Custom Questions

#### Type of crash:

Browser

#### Crash state:

```

rax=efefefefefefefef rbx=000000345a3fdd48 rcx=00005fc403494300
rdx=00007ff93d2dcd10 rsi=00005fc404df9480 rdi=00005fc403e9da30
rip=00007ff88210c8a8 rsp=000000345a3fdc60 rbp=000001db75103230
 r8=2fc155fd3ba0ff83  r9=000000007ffe1000 r10=00000fff1042190e
r11=0000000000004000 r12=00005fc00004d9e8 r13=0000000000000001
r14=00005fc403bd5160 r15=0000000000008235
iopl=0         nv up ei pl nz na po nc
cs=0033  ss=0000  ds=0000  es=0000  fs=0053  gs=002b             efl=00010206
chrome!lens::LensOverlayBlurLayerDelegate::FetchBackgroundImage+0x38:
00007ff8`8210c8a8 488b8090000000  mov     rax,qword ptr [rax+90h] ds:efefefef`efeff07f=????????????????
0:000> k
  *** Stack trace for last set context - .thread/.cxr resets it
 # Child-SP          RetAddr               Call Site
00 00000034`5a3fdc60 00007ff8`7b84a5b2     chrome!lens::LensOverlayBlurLayerDelegate::FetchBackgroundImage+0x38 [C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\lens\lens_overlay_blur_layer_delegate.cc @ 91] 
01 (Inline Function) --------`--------     chrome!base::RepeatingCallback<void ()>::Run+0x2f [C:\b\s\w\ir\cache\builder\src\base\functional\callback.h @ 344] 
02 00000034`5a3fdd10 00007ff8`7de25c33     chrome!base::RepeatingTimer::RunUserTask+0x1c2 [C:\b\s\w\ir\cache\builder\src\base\timer\timer.cc @ 217] 
03 (Inline Function) --------`--------     chrome!base::OnceCallback<void ()>::Run+0x33 [C:\b\s\w\ir\cache\builder\src\base\functional\callback.h @ 156] 
04 (Inline Function) --------`--------     chrome!base::TaskAnnotator::RunTaskImpl+0x11a [C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc @ 203] 
05 (Inline Function) --------`--------     chrome!base::TaskAnnotator::RunTask+0x17d [C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.h @ 90] 
06 (Inline Function) --------`--------     chrome!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl+0x687 [C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc @ 470] 
07 00000034`5a3fdd90 00007ff8`7df78cc8     chrome!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork+0x723 [C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc @ 332] 
08 00000034`5a3fe560 00007ff8`7adb2368     chrome!base::MessagePumpForUI::DoRunLoop+0x1d8 [C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc @ 261] 
09 00000034`5a3fe670 00007ff8`7ee51c34     chrome!base::MessagePumpWin::Run+0xa8 [C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc @ 86] 
0a 00000034`5a3fe6d0 00007ff8`7b88aaa3     chrome!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run+0xe4 [C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc @ 643] 
0b 00000034`5a3fe770 00007ff8`7bd41202     chrome!base::RunLoop::Run+0x1b3 [C:\b\s\w\ir\cache\builder\src\base\run_loop.cc @ 136] 
0c 00000034`5a3fe870 00007ff8`7bd40ea6     chrome!content::BrowserMainLoop::RunMainMessageLoop+0xb2 [C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_loop.cc @ 1104] 
0d (Inline Function) --------`--------     chrome!content::BrowserMainRunnerImpl::Run+0xf [C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_runner_impl.cc @ 156] 
0e 00000034`5a3fe8e0 00007ff8`7bd3f77e     chrome!content::BrowserMain+0x176 [C:\b\s\w\ir\cache\builder\src\content\browser\browser_main.cc @ 34] 
0f (Inline Function) --------`--------     chrome!content::RunBrowserProcessMain+0x113 [C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc @ 732] 
10 00000034`5a3fe9a0 00007ff8`7bd0f20f     chrome!content::ContentMainRunnerImpl::RunBrowser+0x76e [C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc @ 1307] 
11 00000034`5a3febc0 00007ff8`7bd0e5ac     chrome!content::ContentMainRunnerImpl::Run+0x2bf [C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc @ 1158] 
12 (Inline Function) --------`--------     chrome!content::RunContentProcess+0x348 [C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc @ 356] 
13 00000034`5a3fed50 00007ff8`7bd0ca3d     chrome!content::ContentMain+0x3bc [C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc @ 369] 
14 00000034`5a3fef90 00007ff7`c15908e8     chrome!ChromeMain+0x26d [C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc @ 233] 
15 00000034`5a3ff270 00007ff7`c158e8db     chrome_exe!MainDllLoader::Launch+0x398 [C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc @ 201] 
16 00000034`5a3ff4f0 00007ff7`c16a73f2     chrome_exe!wWinMain+0x23b [C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc @ 351] 
17 (Inline Function) --------`--------     chrome_exe!invoke_main+0x21 [D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl @ 118] 
18 00000034`5a3ff900 00007ff9`3bfc7344     chrome_exe!__scrt_common_main_seh+0x106 [D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl @ 288] 
19 00000034`5a3ff940 00007ff9`3d29cc91     KERNEL32!BaseThreadInitThunk+0x14
1a 00000034`5a3ff970 00000000`00000000     ntdll!RtlUserThreadStart+0x21


```
# Additional Data

Category: Security   

Chrome Channel: Canary   

Regression: N/A

## Attachments

- [09.09.2024_06.44.59_REC.mp4](attachments/09.09.2024_06.44.59_REC.mp4) (video/mp4, 2.6 MB)
- [windbg.txt](attachments/windbg.txt) (text/plain, 5.1 KB)

## Timeline

### aj...@google.com (2024-09-10)

I can confirm that this leads to a crash - <https://crash.corp.google.com/browse?q=reportid=%2708083ce87e78a9e8%27>

Does not repro on Stable.

1. open Chrome
2. google.com/chrome
3. in same tab - re-enter and press enter
4. click lens
5. double-click back button

Almost certainly relates to <https://chromium-review.googlesource.com/c/chromium/src/+/5839240>

So sending to mercerd

### aj...@google.com (2024-09-10)

CL was cherry-picked to 129 - <https://chromium-review.googlesource.com/c/chromium/src/+/5841313>

### aj...@google.com (2024-09-10)

There are crashes from several Canary versions - it is a little disappointing that these were not investigated before merging:-

<https://crash.corp.google.com/browse?q=product_name%3D%27Chrome%27+AND+EXISTS+%28SELECT+1+FROM+UNNEST%28CrashedStackTrace.StackFrame%29+WHERE+Regexp_Contains%28FunctionName%2C%27LensOverlayBlurLayerDelegate%3A%3AFetchBackgroundImage%27%29%29++AND+ComparableVersion%28product.version%29+%3E%3D+ComparableVersion%28%27130.0.0.1%27%29#+samplereports:30,productname:1000,productversion:20,processtype:120,magicsignature:100,magicsignature2:50,stablesignature:50,clientid:100,osversion:100,cpuinfo:100,url:30,runningfinchexperiments:5000>

### aj...@google.com (2024-09-10)

The Delegate itself (which I think is what is free'd) is a unique\_ptr:-

```
void LensOverlayController::AddBackgroundBlur() {
  // We do not blur unless the overlay is currently active.
  if (state_ != State::kOverlay && state_ != State::kOverlayAndResults) {
    return;
  }

  if (lens::features::GetLensOverlayUseCustomBlur()) {
    overlay_view_->SetPaintToLayer();
    ui::Layer* background_layer = overlay_view_->layer();
    background_layer->SetFillsBoundsOpaquely(true);

    content::RenderWidgetHostView* live_page_view = tab_->GetContents()
                                                        ->GetPrimaryMainFrame()
                                                        ->GetRenderViewHost()
                                                        ->GetWidget()
                                                        ->GetView();

    // Create the blur delegate which will start blurring the background;
    lens_overlay_blur_layer_delegate_ =
        std::make_unique<lens::LensOverlayBlurLayerDelegate>(background_layer,
                                                             live_page_view);
    return;
  }

```

It is not immediately clear to me from these crashes if there is a miracle-ptr protecting this region, or not, so for now this must be treated as a security issue.

### aj...@google.com (2024-09-10)

Not able to repro in my asan build, but possibly I do not have the correct set of features enabled.

### pe...@google.com (2024-09-10)

Setting milestone because of s2 severity.

### pe...@google.com (2024-09-10)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security Impact hotlist or the Severity field, and remove the ReleaseBlock hotlist.

### pe...@google.com (2024-09-10)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### pe...@google.com (2024-09-10)

This issue appears to be blocking an upcoming release and is therefore an **Urgent Release Blocking Issue** as per <http://go/chrome-slo#release-blocking-issues>. Bumping the priority to P0 to better reflect the urgency.

If this is not a release blocking issue, please adjust the release block field. Adjusting the priority will have no affect, P0 will be re-applied whilever this is marked as a release blocking issue.

### me...@google.com (2024-09-10)

Looking into this now

### me...@google.com (2024-09-10)

Since cut for release candidate is today, not going to be able to get a fix and CP in time. Therefore, going to revert the CP.
<https://chromium-review.googlesource.com/c/chromium/src/+/5851278>

Will follow up with a fix and re-cherrypick to include in the M129 respin.

### aj...@google.com (2024-09-10)

reopening - as the CL on main/ is still there

### aj...@google.com (2024-09-10)

Thanks for reverting on 129.

### me...@google.com (2024-09-10)

I have <https://buganizer.corp.google.com/issues/365775923> to follow up on main. @srinivassista asked me to close this as it is no longer a blocker for the M129 release.

### pe...@google.com (2024-09-11)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M129. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [129].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### me...@google.com (2024-09-11)

Nothin needs to be merged back AFAIK. The culprit CL was reverted from the M129 branch.

### pe...@google.com (2024-09-13)

This release blocking issue appears to be targeted for one or more milestones which may have already branched:

- M129, which branched on 2024-08-19 (Chromium branch: 6668, Chromium branch position: 1343869)

Because this issue was marked as fixed on or after branch day, a merge of any CLs which landed on or after branch day may be required.

If no merge is needed (e.g. the necessary CLs are already present in the relevant branch), please remove TBD-## from the Merge field and replace it with NA-## (where ## corresponds to the milestone under evaluation). If a merge is necessary, the requested milestone(s) to the Merge-Request field. If you're not sure, reach out to the relevant release manager (can be found at <https://chromiumdash.appspot.com/schedule>).

To learn more about the merge process, including how to land any required merges, see <https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md>.

### pe...@google.com (2024-09-14)

Setting milestone because of s2 severity.

### pe...@google.com (2024-09-15)

This release blocking issue appears to be targeted for one or more milestones which may have already branched:

- M129, which branched on 2024-08-19 (Chromium branch: 6668, Chromium branch position: 1343869)

Because this issue was marked as fixed on or after branch day, a merge of any CLs which landed on or after branch day may be required.

If no merge is needed (e.g. the necessary CLs are already present in the relevant branch), please remove TBD-## from the Merge field and replace it with NA-## (where ## corresponds to the milestone under evaluation). If a merge is necessary, the requested milestone(s) to the Merge-Request field. If you're not sure, reach out to the relevant release manager (can be found at <https://chromiumdash.appspot.com/schedule>).

To learn more about the merge process, including how to land any required merges, see <https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md>.

### me...@google.com (2024-09-16)

This is issue is no longer in M129 because the CL that caused it was reverted. Not sure what I need to do to stop these automated comments.

### sp...@google.com (2024-09-18)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
report of highly mitigated memory corruption in a non-sandboxed process


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-09-18)

Congratulations Khalil! Thank you for your efforts and reporting this issue to us.

### pe...@google.com (2024-12-18)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/365516486)*
