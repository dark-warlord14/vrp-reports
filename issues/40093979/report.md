# Any extension can be disbled by simply adding a trailing slash

| Field | Value |
|-------|-------|
| **Issue ID** | [40093979](https://issues.chromium.org/issues/40093979) |
| **Status** | Accepted |
| **Severity** | S4-Minimal |
| **Priority** | P3 |
| **Component** | Platform>Extensions |
| **Platforms** | Windows |
| **Reporter** | Ju...@microsoft.com |
| **Assignee** | la...@chromium.org |
| **Created** | 2019-02-07 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3694.0 Safari/537.36 Edg/74.0.81.0

Steps to reproduce the problem:
1. Install Adblock (https://chrome.google.com/webstore/detail/adblock/gighmmpiobklfepjocnamgkkbiglidom)
2. Go to https://shhnjk.azurewebsites.net/disable_ext.php?url=chrome-extension://gighmmpiobklfepjocnamgkkbiglidom/options.html/
3. Right click on the link and click "open link in new tab"

What is the expected behavior?
Extension page is rendered.

What went wrong?
Extension have files such as html, css, and js. If you navigate to any of those files with trailing slash, extension is considered as corrupted by Chrome and disabled.

This is bad because some people (*cough*) uses extension like phishing protection (https://chrome.google.com/webstore/detail/windows-defender-browser/bkbeeeffjjeopflfhgeknacdieedcoml). This means that such protection can be somewhat easily disabled. This is certainly true for Adblock, where many advertiser wish from heart that user had no adblock ;)

Did this work before? N/A 

Chrome version: 74  Channel: canary
OS Version: 10.0
Flash Version:

## Attachments

- [test.html](attachments/test.html) (text/plain, 156 B)
- [FixingExtensionCorruptionIssue.patch](attachments/FixingExtensionCorruptionIssue.patch) (application/octet-stream, 3.5 KB)

## Timeline

### do...@chromium.org (2019-02-07)

Thanks for the report.

I'm not sure this is a security issue since we don't assume users have any particular extensions installed to improve their security. However, arbitrary sites being able to disable extensions seems bad.

+extensions folks to investigate. I can move this out of the security queue if you agree with my assessment.

[Monorail components: Platform>Extensions]

### ka...@chromium.org (2019-02-07)

I wasn't able to repro on chrome 74 (canary) on Mac. Adding Istiaque, since this might be related to content verification.

### mm...@chromium.org (2019-02-08)

[Empty comment from Monorail migration]

### Ju...@microsoft.com (2019-02-16)

This repros in stable too. It should be Security_Impact-Stable.

### Ju...@microsoft.com (2019-03-01)

Hi, our engineers have a fix for this issue. Would you mind CCing following people?
mukul.purohit@microsoft.com, maheshjh@microsoft.com, utkpat@microsoft.com

Thanks!

### sh...@chromium.org (2019-03-13)

[Empty comment from Monorail migration]

### Ju...@microsoft.com (2019-04-02)

Attaching PoC file.

### wf...@chromium.org (2019-04-02)

[Empty comment from Monorail migration]

### rd...@chromium.org (2019-04-08)

I'm still not able to reproduce this.  The page doesn't load correctly, but the extension isn't disabled.  Are you still seeing this on Canary?

Passing to lazyboy@ to look at when he's back, unless we're able to get a repro in which case we can bump priority.

### ut...@microsoft.com (2019-04-09)

I'm able to reproduce this on Chrome 75.0.3759.4 (Official Build) canary (64-bit) on Windows.

Repro steps:
1. Go to https://chrome.google.com/webstore/search/adblock?hl=en and install the AdBlock extension that 291,500 users have rated.
2. Open the options page of AdBlock (chrome-extension://gighmmpiobklfepjocnamgkkbiglidom/options.html) and see that the extension is still present.
3. Now add a slash to the end of the options page and hit enter (chrome-extension://gighmmpiobklfepjocnamgkkbiglidom/options.html/). Notice that the extension's browser action vanishes and the extension is shown as corrupted at chrome://extensions

### rd...@chromium.org (2019-04-09)

I wonder if this is OS-specific.  I'll take a look next week when I'm back at my windows box.

### ut...@microsoft.com (2019-04-22)

Issue:
Extensions can contain resources that can be accessed by navigating to the URL chrome-extension://<extensionId>/<relativePathToResource>

When navigating to any extension resource/file, the following options are considered:

If that resource is present in the content verified files, navigation is allowed
If that resource is absent, error is notified
This is done as part of ContentHashReader::Create function where verified_contents.HasTreeHashRoot checks if the resource that we want to navigate to is present. Extensions can have 0 byte sized files and files can become unreadable or go missing. So, whenever an attempt is made to open any extension resource file by navigating to it, URLRequestFileJob::OnOpenComplete calls ContentVerifyJob::DoneReading(). This works fine for 0 byte files and content verification passes. It also works for deleted resources and content verification fails.

Whenever an attempt is made to open an extension resource, the relative path of the resource is normalized first. So, in the case when separator(s) (slash, backward slash or dot) is/are appended to the resource path and navigation is performed, the trailing separator(s) get removed and it is found that the resource is present and hence, opening the file should succeed. But when an attempt to open the actual file is made, it fails since there is no file with a trailing slash at the end. So, content verification thinks that the file was deleted and hence content verification fails causing the extension to be disabled with the message that the extension may have been corrupted.

Fix:

When an attempt is made to open an extension resource, the relative path of the resource is normalized first. This normalization should not remove the trailing separators. This will ensure that the check for the presence of the resource in the extension fails and we don't even attempt to open the file and directly show the error page for missing resource. This ensures that content verification does not fail and extension remains enabled.

Testing:

Verified that adding trailing separators to the extension resource path and navigating to it does not corrupt the extension and it remains enabled.

Review request:

Please tell me if this proposed solution seems fine and if it has any issues. Attaching a patch for the proposed fix.

### sh...@chromium.org (2019-04-24)

[Empty comment from Monorail migration]

### ut...@microsoft.com (2019-05-13)

Hello guys.

Were you able to take a look at the proposed fix for this issue described in https://crbug.com/chromium/929578#c13?
Please let me know your thoughts about the proposed fix.

Thanks.

### rd...@chromium.org (2019-05-20)

I was able to reproduce this on Windows, so it does seem platform-specific.

lazyboy@, can you take a look at this when you get a chance?

### la...@chromium.org (2019-05-20)

Sorry, I missed this, will take a look tomorrow.

### ka...@chromium.org (2019-05-21)

[Empty comment from Monorail migration]

### la...@chromium.org (2019-05-22)

OK, I got it to repro, just posting my findings here:

NormalizeRelative path seems to be converting "foo.html/" to "foo.html". Hence ContentVerifyJob is trying to compare hashes of "foo.html/" (non existent file) with "foo.html"'s corresponding hash in verified_contents.json.

[1] https://cs.chromium.org/chromium/src/extensions/browser/content_verifier.cc?rcl=74c5d1fc0fc407b7ded322f07a9b3d57c14a975a&l=45

### ut...@microsoft.com (2019-05-22)

Yes, that is what I also found as mentioned in https://crbug.com/chromium/929578#c13. I have also attached a proposed fix for the issue with the same comment.

lazyboy@, can you please review the fix too? Briefly, the fix just changes NormalizeRelativePath to keep the trailing separator instead of removing it.

### la...@chromium.org (2019-05-22)

@utkpat, Sorry I didn't notice the patch! (I  looked at the desc and the last comment only :))
While thinking about fix, yes, preserving the trailing separator at the end sounds about right. There are platform issues where we want to make sure the output has fwd slashes as verified_contents expects them.
Lmk if you want to continue with your patch, then you should use gerrit and upload the patch there and add me as a reviewer. Otherwise, I'll upload mine.

### ut...@microsoft.com (2019-05-23)

@lazyboy, No issues. I will use gerrit to upload my patch and add you as a reviewer. Thanks.

### ut...@microsoft.com (2019-05-24)

@lazyboy, I have created a patch for code review on gerrit and added you as a reviewer. Please review it. Thanks.

### sh...@chromium.org (2019-06-05)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-06-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/0c209164bcc1647d09568aaa27290e0490de2bfb

commit 0c209164bcc1647d09568aaa27290e0490de2bfb
Author: Utkarsh Patankar <utkpat@microsoft.com>
Date: Sat Jun 08 06:29:44 2019

Fixing extension corruption when navigating to extension resource with slash at end

Because of how Content Verifier currently normalizes relative paths of
an extension resource, it (incorrectly) drops any separators at the end
of the relative path. This makes Content Verifier incorrectly think
that a resource exists (if the separators came after a valid extension
resource path) and this results in content verification failure.

Fix this by ensuring content verifier path normalization does not drop
trailing separator, if present.

Bug: 929578

bar.html is present must not corrupt or disable the extension.

Test: Navigating to chrome-extension://<extensionId>/bar.html/ when
Change-Id: I3972643d9f9566e011070e4b01f0b1a50e3fa659
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1628635
Commit-Queue: Utkarsh Patankar <utkpat@microsoft.com>
Auto-Submit: Utkarsh Patankar <utkpat@microsoft.com>
Reviewed-by: Istiaque Ahmed <lazyboy@chromium.org>
Cr-Commit-Position: refs/heads/master@{#667431}

[modify] https://crrev.com/0c209164bcc1647d09568aaa27290e0490de2bfb/chrome/browser/extensions/content_verifier_browsertest.cc
[modify] https://crrev.com/0c209164bcc1647d09568aaa27290e0490de2bfb/extensions/browser/content_verifier.cc
[modify] https://crrev.com/0c209164bcc1647d09568aaa27290e0490de2bfb/extensions/browser/content_verifier.h
[modify] https://crrev.com/0c209164bcc1647d09568aaa27290e0490de2bfb/extensions/browser/content_verifier_unittest.cc


### ut...@microsoft.com (2019-06-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-06-08)

[Empty comment from Monorail migration]

### ut...@microsoft.com (2019-06-10)

Verified the fix in Chromium Version 77.0.3821.0 (Developer Build) (64-bit).

### na...@google.com (2019-06-10)

[Empty comment from Monorail migration]

### wf...@chromium.org (2019-06-19)

jun.kokatsu@microsoft.com - please remember to always attach source to your PoC on the bug when submitting an issue. This bug is missing a copy of disable_ext.php

### wf...@chromium.org (2019-06-19)

oh nvm I see it's attached in commment 7.

### na...@google.com (2019-06-20)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-06-20)

Congrats the Panel decided to reward $500 for this report 

### ad...@google.com (2019-09-09)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-09-09)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-09-14)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### na...@google.com (2019-11-21)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-11-23)

[Empty comment from Monorail migration]

### na...@google.com (2020-02-20)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/929578?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093979)*
