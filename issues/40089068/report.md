# Security: UAF in CPWL_Edit::OnChar

| Field | Value |
|-------|-------|
| **Issue ID** | [40089068](https://issues.chromium.org/issues/40089068) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ma...@gmail.com |
| **Assignee** | hn...@chromium.org |
| **Created** | 2017-09-20 |
| **Bounty** | $5,000.00 |

## Description

Notice: Please don't consider this same root cause as https://bugs.chromium.org/p/chromium/issues/detail?id=765384 (btw how could we insert <a> tag like [https://crbug.com/chromium/765384])

To repro, open the pdf, try to a value of edit textbox |myfield| -> ASan crashes.

At 00:26s of poc.mov , I was typing "x" to make its value changes.

They got different root cause, just same path. 

To understand, let's check the source code:

PATCH = https://pdfium.googlesource.com/pdfium/+/b1f9205bb1a0671c31e44e7362784c770bf2a948

-----------------------------------------------

Before the PATCH:

std::pair<bool, bool> CFFL_InteractiveFormFiller::OnBeforeKeyStroke(
[...]
  CPDFSDK_Annot::ObservedPtr pObserved(pData->pWidget);
  if (!pData->pWidget->OnAAction(CPDF_AAction::KeyStroke, fa,
                                 pData->pPageView)) {
    if (!IsValidAnnot(pData->pPageView, pData->pWidget))
      bExit = true;
    return {bRC, bExit};
  }
[...]

-----------------------------------------------

After the PATCH:

std::pair<bool, bool> CFFL_InteractiveFormFiller::OnBeforeKeyStroke(
[...]
  CPDFSDK_Annot::ObservedPtr pObserved(privateData.pWidget);
  bool action_status = privateData.pWidget->OnAAction(
      CPDF_AAction::KeyStroke, fa, privateData.pPageView);
  if (!pObserved || !IsValidAnnot(privateData.pPageView, privateData.pWidget))
    return {true, true};
  if (!action_status)
    return {true, false};
  }
[...]

-----------------------------------------------


So even *prior to the patch or afterwards*, if |OnAAction| returns failure, |OnBeforeKeyStroke| will return pair or |{true,false}| then.


Let's checkout |CPWL_Edit::OnChar|

https://cs.chromium.org/chromium/src/third_party/pdfium/fpdfsdk/pwl/cpwl_edit.cpp?q=CPWL_Edit::OnChar&sq=package:chromium&l=548

You can see at 542th line, it's invoking |OnBeforeKeyStroke|, then at 548th line, it checks both |bRC| and |bExit|, so... there is only one case we can reach 553th line (if (IPVT_FontMap* pFontMap = GetFontMap()) { ... ) is when we make |OnAAction| failed.

So what if, we make |CPWL_Edit| freed right at the middle of |OnAAction::KeyStroke|, also make it failed to reach 553th line.

UAF occurs.

==> The point here is |CPWL_Edit::OnChar| doesn't check whether |this| is still alive or not. 

==> Root cause is different from [https://crbug.com/chromium/765384], it's not duplicate (sure, the PoC still make ASan crashes).









## Attachments

- [asan](attachments/asan) (text/plain, 19.2 KB)
- [onchar.in](attachments/onchar.in) (application/octet-stream, 1.5 KB)
- [onchar.pdf](attachments/onchar.pdf) (application/pdf, 2.4 KB)
- [poc.mov](attachments/poc.mov) (application/octet-stream, 8.6 MB)
- [control_reg.in](attachments/control_reg.in) (application/octet-stream, 1.8 KB)
- [control_reg.pdf](attachments/control_reg.pdf) (application/pdf, 2.7 KB)
- [Screenshot from 2017-09-20 16-45-46.png](attachments/Screenshot from 2017-09-20 16-45-46.png) (image/png, 322.4 KB)

## Timeline

### ma...@gmail.com (2017-09-20)

ah yea, I think I got the way to embed <a> link.

Btw, more clarify, to let |OnAAction| failed, I add "/Next 20 0 R" inside "20 0 object", turns it into recursive, so |ExecuteFieldAction| will ignore it and |return false|

https://cs.chromium.org/chromium/src/third_party/pdfium/fpdfsdk/fsdk_actionhandler.cpp?type=cs&sq=package:chromium&l=240





### ma...@gmail.com (2017-09-20)

This PoC takes control [rdi], and possible to control RIP as well.

Tested on Chromium Linux local build.



### ma...@gmail.com (2017-09-20)

Ah Just notice that, before the patch (current stable Chrome) it will crash sooner at the line: | if (!IsValidAnnot(pData->pPageView, pData->pWidget)) |

because pdf window has been destroyed, so |pData| which is a element in |CPWL_Edit| is been freed as well. 

-----------------------------------------------

Before the PATCH:

std::pair<bool, bool> CFFL_InteractiveFormFiller::OnBeforeKeyStroke(
[...]
  CPDFSDK_Annot::ObservedPtr pObserved(pData->pWidget);
  if (!pData->pWidget->OnAAction(CPDF_AAction::KeyStroke, fa,
                                 pData->pPageView)) {
    if (!IsValidAnnot(pData->pPageView, pData->pWidget))
      bExit = true;
    return {bRC, bExit};
  }
[...]

-----------------------------------------------


### cl...@chromium.org (2017-09-20)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4917559085498368.

### pa...@chromium.org (2017-09-20)

[Empty comment from Monorail migration]

[Monorail components: Internals>Plugins>PDF]

### pa...@chromium.org (2017-09-21)

I'm having a hard time figuring out how far back this vulnerability goes. The relevant code seems to have had only cosmetic/minor changes recently? Maybe tsepez can shed light on that, and fill in the Security_Impact-Foo label.

### sh...@chromium.org (2017-09-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-09-21)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ma...@gmail.com (2017-09-21)

Hm, sorry my explanation might get us misunderstood. I just meant that this bug exists in stable branch m61 both before and after the patch. 

### ts...@chromium.org (2017-09-21)

[Empty comment from Monorail migration]

### ds...@chromium.org (2017-09-21)

If this bug already exists in Stable, why is it ReleaseBlock-Stable?

hnakashima@ can you please take a look?

### bu...@chromium.org (2017-09-22)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/f5777a117a7557507616eaf585de5eb266531e16

commit f5777a117a7557507616eaf585de5eb266531e16
Author: Henrique Nakashima <hnakashima@chromium.org>
Date: Fri Sep 22 18:22:06 2017

Fix UAF after destroying a widget during OnBeforeKeyStroke().

Bug: chromium:766957
Change-Id: I61b282059fb4fc2c8ba6dafc502f030f31dd324d
Reviewed-on: https://pdfium-review.googlesource.com/14710
Commit-Queue: Henrique Nakashima <hnakashima@chromium.org>
Reviewed-by: Tom Sepez <tsepez@chromium.org>

[modify] https://crrev.com/f5777a117a7557507616eaf585de5eb266531e16/fpdfsdk/pwl/cpwl_list_box.cpp
[modify] https://crrev.com/f5777a117a7557507616eaf585de5eb266531e16/fpdfsdk/pwl/cpwl_edit.cpp


### ts...@chromium.org (2017-09-22)

This bug has been around for a while, do we want to merge?

### sh...@chromium.org (2017-09-22)

This bug requires manual review: M62 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: amineer@(Android), cmasso@(iOS), bhthompson@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ma...@gmail.com (2017-09-22)

[Comment Deleted]

### hn...@chromium.org (2017-09-22)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-09-23)

[Empty comment from Monorail migration]

### ab...@chromium.org (2017-09-25)

thanks for the fix. What is the complexity of this fix? Has it been well tested in Canary and covered by unit tests? 

My recommendation is to wait until M63 if this is not critical, since we're past M62 branch. 

### hn...@chromium.org (2017-09-25)

The fix is very simple logically, we simply watch for whether the object running a method has been destroyed by a callback it invokes. If it was destroyed (that is, the ObservedPtr became invalid) we simply return from it before doing anything else and thus do not access freed memory anymore.



### ab...@chromium.org (2017-09-26)

Thanks - have you built this locally and confirmed it will merge cleanly? If yes, please go ahead and merge to M62, branch:3202.

### bu...@chromium.org (2017-09-26)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/26d87f53b5c1e7169455fdaf8e2305e3b9fcbb54

commit 26d87f53b5c1e7169455fdaf8e2305e3b9fcbb54
Author: Henrique Nakashima <hnakashima@chromium.org>
Date: Tue Sep 26 21:19:43 2017

[Merge M62] Fix UAF after destroying a widget during OnBeforeKeyStroke().

> Bug: chromium:766957
> Change-Id: I61b282059fb4fc2c8ba6dafc502f030f31dd324d
> Reviewed-on: https://pdfium-review.googlesource.com/14710
> Commit-Queue: Henrique Nakashima <hnakashima@chromium.org>
> Reviewed-by: Tom Sepez <tsepez@chromium.org>

Change-Id: I1dae26d28dd5720b57d8696a77fe3b514646edcd
Reviewed-on: https://pdfium-review.googlesource.com/14835
Commit-Queue: Henrique Nakashima <hnakashima@chromium.org>
Commit-Queue: dsinclair <dsinclair@chromium.org>
Reviewed-by: dsinclair <dsinclair@chromium.org>

[modify] https://crrev.com/26d87f53b5c1e7169455fdaf8e2305e3b9fcbb54/fpdfsdk/pwl/cpwl_list_box.cpp
[modify] https://crrev.com/26d87f53b5c1e7169455fdaf8e2305e3b9fcbb54/fpdfsdk/pwl/cpwl_edit.cpp


### as...@chromium.org (2017-09-27)

[Empty comment from Monorail migration]

### aw...@google.com (2017-10-05)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-10-06)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2017-10-06)

And a $5,000 reward for this one, too!

### aw...@chromium.org (2017-10-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-12-30)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-03-27)

[Empty comment from Monorail migration]

### is...@google.com (2018-03-27)

This issue was migrated from crbug.com/chromium/766957?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40089068)*
