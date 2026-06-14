# Security: Use-After-Free in CFFL_ComboBox::SaveData

| Field | Value |
|-------|-------|
| **Issue ID** | [341095523](https://issues.chromium.org/issues/341095523) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux, Mac, Windows |
| **Chrome Version** |  125.0.6422.60 |
| **Reporter** | kd...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2024-05-16 |
| **Bounty** | $1,000.00 |

## Description

# Steps to reproduce the problem

This is found by manual code audit, so there is no poc. I'm not 100% sure that it's exploitable, but according to the prior issue I report it to be safe.
Now I'm working on a poc.
This bug requires XFA enabled.

# Problem Description

In function CFFL\_ComboBox::SaveData, the `m_pWidget->SetOptionSelection` will invoke a js call, which allows to free the m\_pWidget object via crafted js code in the pdf file. Afterward, the `m_pWidget->ResetFieldAppearance` was used without validation.

```
  if (bSetValue) {
    m_pWidget->SetValue(swText);
  } else {
    m_pWidget->GetSelectedIndex(0);
    m_pWidget->SetOptionSelection(nCurSel);                  <= JS Call
  }
  ObservedPtr<CPDFSDK_Widget> observed_widget(m_pWidget);
  ObservedPtr<CFFL_ComboBox> observed_this(this);

  m_pWidget->ResetFieldAppearance();  <= Use without checking 

```

For step 1 (invoke js), I slightly modify the condition of poc from 40064490, and successfully invoked the js call.
For step 2 (free m\_pWidget), I'm still working on that, but according to 40088733, it should be possible.

# Summary

Security: Use-After-Free in CFFL\_ComboBox::SaveData

# Custom Questions

#### Type of crash:

tab

#### Reporter credit:

Han Zheng (HexHive)

# Additional Data

Category: Security   

Chrome Channel: Stable   

Regression: N/A

## Timeline

### el...@chromium.org (2024-05-16)

Security shepherd: thanks for the report; the UaF you describe sounds plausible to me. Over to pdfium folks :)

### el...@chromium.org (2024-05-16)

Bug without working PoC (yet) -> Pri-2 Sev-2, and assuming this affects desktop platforms.

### el...@chromium.org (2024-05-16)

The involved code is all years old, so setting FoundIn to stable.

### pe...@google.com (2024-05-17)

Setting milestone because of s2 severity.

### ts...@google.com (2024-05-17)

Seems plausible, can fix without waiting on a PoC, though reward decisions will be impacted if you can't demonstrate one.
The access in question is through an UnownedPtr<>, which is PFDium's wrapper around miracle ptr, so reduction in severity appropriate.


### ts...@google.com (2024-05-17)

So, the issue is with XFA that we need to call Synchronize() to put the XFA widgets in sync with the PDF ones, and doing so may fire JS which can't be reached in a non-xfa mode.
The callers of synchronize are as follows:
Synchronize()
  CPDFSDK_Widget::SetCheck(bool bChecked)
    CFFL_CheckBox::SaveData()
    CFFL_RadioButton::SaveData()
  CPDFSDK_Widget::SetValue(const WideString& sValue)
    CFFL_ComboBox::SaveData()
    CFFL_TextField::SaveData()
  CPDFSDK_Widget::SetOptionSelection(int index)
    CFFL_ComboBox::SaveData()
    CFFL_ListBox::SaveData()  (2x)
  CPDFSDK_Widget::ClearSelection()
    CFFL_ListBox::SaveData()

I'll need to investigate each of these to make sure the widget destruction is observed before use.



### ts...@chromium.org (2024-05-17)

https://pdfium-review.googlesource.com/c/pdfium/+/119318 adds defense for two questionable methods from above.

### ts...@chromium.org (2024-05-17)

There's also a follow-on task that once an observed version of a member has been made on the stack, it should be used in place of the member itself.  In which case, cases like these become null-deref segvs and not security issues.

### pe...@google.com (2024-05-22)

This is sufficiently serious that it should be merged to beta. But I can't  see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M126. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.


Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [126].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


### am...@chromium.org (2024-05-24)

<https://pdfium-review.googlesource.com/c/pdfium/+/119318> (roll == <https://crrev.com/c/5549675>) approved for backmerge to M126, please merge this fix to branch 6478 by EOD Tuesday, 28 May so this fix can be included in the next M126 Beta update -- thanks!

### pe...@google.com (2024-05-28)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### pe...@google.com (2024-06-03)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### sp...@google.com (2024-06-26)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
report of highly mitigated memory corruption in a sandboxed process 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-06-27)

Thank you for this speculative report of highly mitigated renderer memory corruption. As were able to make a security-relevant change based on the information in your report, we wanted to extend you a reward of appreciation and to reflect that. Thanks for your efforts and reporting this issue to us! 

### pe...@google.com (2024-08-28)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/341095523)*
