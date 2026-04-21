# Security: UAF in SaveUPIOfferBubbleViews::WindowClosing

| Field | Value |
|-------|-------|
| **Issue ID** | [40064191](https://issues.chromium.org/issues/40064191) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Autofill |
| **Platforms** | Mac |
| **Reporter** | zh...@gmail.com |
| **Assignee** | vy...@google.com |
| **Created** | 2023-04-24 |
| **Bounty** | $5,000.00 |

## Description

**Steps to reproduce the problem:**

1. First, you need to have a compiled chromium locally
2. Run `git apply poc.diff` and recompile chromium locally  
   
   .What I need to explain here is poc.diff is to trigger the vulnerability function more easily, obviously, it will not maliciously change the program logic
3. Run `./Chromium.app/Contents/MacOS/Chromium --enable-features=AutofillCreditCardEnabled,AutofillSaveAndFillVPA http://127.0.0.1:8000/index.html` Click the Submit button, then close the current tab.This is done to free the WebContent object and thus trigger the UAF vulnerability. Note: This is not a vulnerability that can only be triggered by closing the browser.Detailed steps can be reproduced stably following the video.RCA coming soon:)

**Problem Description:**  

Bisect:  

<https://chromium-review.googlesource.com/c/chromium/src/+/4293475>

[jkeitel@google.com](mailto:jkeitel@google.com) might be the right owner.

**Additional Comments:**

\*\*Chrome version: \*\* 113.0.5638.0 \*\*Channel: \*\* Not sure

**OS:** Mac OS

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 28.2 KB)
- [poc.mov](attachments/poc.mov) (video/quicktime, 4.5 MB)
- [poc.diff](attachments/poc.diff) (text/plain, 933 B)
- [fix.diff](attachments/fix.diff) (text/plain, 2.4 KB)
- [index.html](attachments/index.html) (text/plain, 2.2 KB)

## Timeline

### zh...@gmail.com (2023-04-24)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-24)

[Empty comment from Monorail migration]

### zh...@gmail.com (2023-04-24)

RCA here:

Very similar to this bug:

https://bugs.chromium.org/p/chromium/issues/detail?id=1240884

SaveUPIOfferBubbleViews stores a raw pointer `controller_` to `autofill::SaveUPIBubbleController`. The controller is attached to WebContents and is deleted when the specified WebContents destroyed. However, SaveUPIOfferBubbleViews was not notified when controller being deleted thus a UAF would occur if `controller_` was accessed again.

The life cycle of class `SaveUPIBubbleControllerImpl` is attached to WebContents,but it failed to inherit from `content::WebContentsObserver` and rewrite `WebContentsDestroyed` function.

Canary 113.0.5622.0, Dev 113.0.5638.0 and Beta 113.0.5672.24 are affected by this vulnerability.

Note:

In order to reproduce this vulnerability, we need to execute the following function call chain:


```
FormDataImporter::ImportAndProcessFormData
	FormDataImporter::ProcessCreditCardImportCandidate
		UpiVpaSaveManager::OfferLocalSave
			ChromeAutofillClient::ConfirmSaveUpiIdLocally
				SaveUPIBubbleControllerImpl::OfferUpiIdLocalSave
```

In this process, the if judgment needs to be satisfied in the FormDataImporter::ProcessCreditCardImportCandidate function:

```
bool FormDataImporter::ProcessCreditCardImportCandidate(
    const FormStructure& submitted_form,
    const absl::optional<CreditCard>& credit_card_import_candidate,
    const absl::optional<std::string>& extracted_upi_id,
    bool payment_methods_autofill_enabled,
    bool is_credit_card_upstream_enabled) {
#if !BUILDFLAG(IS_ANDROID) && !BUILDFLAG(IS_IOS)
  if (extracted_upi_id && payment_methods_autofill_enabled &&
      base::FeatureList::IsEnabled(features::kAutofillSaveAndFillVPA)) {
    upi_vpa_save_manager_->OfferLocalSave(*extracted_upi_id);
  }
#endif
```


Therefore, the following flags need to be enabled when reproducing the vulnerability:

```
--enable-features=AutofillCreditCardEnabled,AutofillSaveAndFillVPA
```

But what puzzles me is that the condition of `extracted_upi_id` is not met all the time. At present, I have not found a way to trigger the call of the `extracted_upi_id` symbol condition, but this is not related to the principle of the vulnerability described above. Therefore, I provide poc.diff to trigger the vulnerability function more conveniently, release the WebContent object and trigger UAF.

Finally, I would like to add a few more details:

Before the Bisect commit:

https://chromium-review.googlesource.com/c/chromium/src/+/4293475

The function `SaveUPIOfferBubbleViews::WindowClosing` has not been implemented, which means that although we can make `controller_` a dangling pointer by closing the browser tab, there is no function call that can use this dangling pointer. However the root cause of the vulnerability
 is not the addition of the `SaveUPIOfferBubbleViews::WindowClosing` function, but because the life cycle of controller_ and WebContents was not managed well when class SaveUPIOfferBubbleViews、SaveUPIBubbleControllerImpl was first implemented.


### zh...@gmail.com (2023-04-24)

A `fix.diff` to fix this vulnerability has been updated. This is just my personal suggestion, and you can also implement similar functions based on your actual situation.

### zh...@gmail.com (2023-04-24)

Sorry, I seem to have forgotten to submit the index.html used to reproduce the vulnerability

### za...@google.com (2023-04-24)

Hi estade@ can you please take a look at this UAF bug in autofilll? Thanks! 

[Monorail components: UI>Browser>Autofill]

### [Deleted User] (2023-04-24)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-24)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-04-24)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### es...@chromium.org (2023-04-24)

[Empty comment from Monorail migration]

### ma...@chromium.org (2023-04-24)

Over to Jared for proper triage.

### os...@google.com (2023-04-24)

Dominic's team made this a while ago, so over to him.  However, the feature was only half-finished, and never launched.  This has zero end-user traffic, and IIRC that makes it ineligible for security bug reporting.

I'm going to remove ReleaseBlock-Stable since this feature doesn't actually exist.

### be...@google.com (2023-04-24)

Adding Hotlist-RBS-Removed for tracking purposes.

### ba...@chromium.org (2023-04-25)

Dmitry, would you mind taking a look? I guess that https://chromium-review.googlesource.com/c/chromium/src/+/3139926 can be applied.

This is not a high urgency as we have no plans to launch UPI support, but it would be sad if we changed our mind and then learn about an old UAF.

I am setting a NextAction a month from now to ensure that we don't forget about it.

### ba...@chromium.org (2023-04-25)

Oh... and even if this is not eligible for the reward program and we don't plan to launch this:

Thanks to the reporter!

### zh...@gmail.com (2023-04-25)

The fix.diff I provided is indeed based on https://chromium-review.googlesource.com/c/chromium/src/+/3139926



### zh...@gmail.com (2023-04-25)

[Comment Deleted]

### ba...@chromium.org (2023-04-25)

ACK... The people making statements about eligibility are not the people who make decisions and we probably should not make them.

Zack, can you help assessing the security impact in light of https://crbug.com/chromium/1438549#c12 and https://crbug.com/chromium/1438549#c17, please?

### za...@chromium.org (2023-04-25)

Hi Dominic, thanks for letting me know. According to https://crbug.com/chromium/1438549#c12 and the context, the feature was only half-finished, and never launched.  It has zero end-user traffic. So I am setting it to Security_Impact-None now. Thanks for reporting zh1x1an1221@ and thanks for looking into this issue team. Please let me know if you need any help from our side.

### ad...@google.com (2023-04-25)

(putting back Security_Severity because even Security_Impact-None bugs should have severity)

Reporter, thanks for the report! This absolutely will go to the VRP panel for consideration. We do reward bugs even if they're unlaunched features, because we want to incentivize reporters to tell us about bugs _before_ those features ship to users. Obviously I can't promise whether the VRP panel will decide to reward this bug, but it will go to them for consideration.

However, there might be more of a delay than usual. Bugs don't go to the VRP panel until a fix has been landed. As this doesn't currently impact end users, we won't necessarily fix it as quickly as some other bugs. You might have to wait a while. Sorry in advance.

### ad...@google.com (2023-04-25)

[Empty comment from Monorail migration]

### zh...@gmail.com (2023-04-25)

Thank you very much for your reply. 

For me, the analysis report on this vulnerability is basically over. I also understand that you need to allocate your own time according to the actual development needs. 

Delaying the vulnerability fix does not matter to me. It doesn't matter that I can also look at the functions of other modules while I wait. Of course, if there is any other help I can provide, you can also ask me here.


### os...@google.com (2023-04-26)

Acknowledged on comments 17 and 18 as well, sorry for the confusion.  I'm certainly in no standing to make such claims either, and I didn't intend to do so in any sort of official capacity.  (I was working off of information I gained elsewhere, but upon further reflection there were indeed differences between these cases.)

Thanks!

### os...@google.com (2023-05-01)

[Empty comment from Monorail migration]

### zh...@gmail.com (2023-05-25)

Friendly ping,any update:)

### zh...@gmail.com (2023-06-09)

Friendly ping,any update？

### vy...@google.com (2023-06-09)

> Friendly ping,any update？

Sorry for the delay, the bug is fixed now and the process moves on, unfortunately I cannot estimate how soon you'll hear from us, but you'll definitely do. Thank you for your patience!

https://chromium-review.googlesource.com/c/chromium/src/+/4583230:
    UAF in SaveUPIOfferBubbleViews::WindowClosing.
    
    The reason was that the controller (managed by WebContents,
    and being killed by closing the tab) dies without notifying
    the view which hold its pointer.
    Fix recorded:
    https://screencast.googleplex.com/cast/NDgzMDE0ODczOTIwMzA3MnwxNDEyYmM1OC05Zg

### ad...@google.com (2023-06-09)

Thanks for the fix!

This will go to the VRP panel sometime in the next few weeks.

### zh...@gmail.com (2023-06-09)

Okay，thanks！

### [Deleted User] (2023-06-09)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-09)

[Empty comment from Monorail migration]

### am...@google.com (2023-06-16)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-06-16)

Congratulations! The VRP Panel has decided to award you $5,000 for this report of a mildly mitigated security bug + $1,000 bisect bonus. Thank you for your efforts and reporting this issue to us! 

### zh...@gmail.com (2023-06-16)

Thank you!

### am...@google.com (2023-06-17)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-15)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1438549?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40064191)*
