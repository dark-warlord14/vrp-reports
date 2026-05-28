# AddressSanitizer: heap-use-after-free on NetExportMessageHandler::SendEmail

| Field | Value |
|-------|-------|
| **Issue ID** | [349653218](https://issues.chromium.org/issues/349653218) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Internals>Network>Logging |
| **Platforms** | iOS |
| **Chrome Version** | 126.0.0.0 |
| **Reporter** | li...@gmail.com |
| **Assignee** | ri...@chromium.org |
| **Created** | 2024-06-27 |
| **Bounty** | $1,000.00 |

## Description

# Steps to reproduce the problem

step to repro:

1. navigate to chrome://net-export
2. click send email and close the site.

# Problem Description

0. In classic mode, closing WebContents before the callback is run will cause the NetExportMessageHandler to be deleted. Then lead to UAF.

```
void NetExportMessageHandler::OnSendNetLog(const base::Value::List& list) {
  DCHECK_CURRENTLY_ON(web::WebThread::UI);
  file_writer_->GetFilePathToCompletedLog(base::BindOnce(
      &NetExportMessageHandler::SendEmail, base::Unretained(this))); //<-- unretained(this) 
}cc

```

1.

```
void NetExportFileWriter::GetFilePathToCompletedLog(
    FilePathCallback path_callback) const {
  DCHECK(thread_checker_.CalledOnValidThread());
  if (!(log_exists_ && state_ == STATE_NOT_LOGGING)) {
    base::SingleThreadTaskRunner::GetCurrentDefault()->PostTask(
        FROM_HERE, base::BindOnce(std::move(path_callback), base::FilePath()));
    return;
  }

  DCHECK(file_task_runner_);
  DCHECK(!log_path_.empty());

  file_task_runner_->PostTaskAndReplyWithResult(
      FROM_HERE, base::BindOnce(&GetPathIfExists, log_path_),
      std::move(path_callback)); // 将会进入这里
}

```

[0]. <https://source.chromium.org/chromium/chromium/src/+/main:ios/chrome/browser/webui/ui_bundled/net_export/net_export_ui.mm;l=159;drc=3e02eb658e84b46ebb53667e0a1cb52fe53b5f87;bpv=0;bpt=1>
[1]. <https://source.chromium.org/chromium/chromium/src/+/main:components/net_log/net_export_file_writer.cc;l=277;drc=3e02eb658e84b46ebb53667e0a1cb52fe53b5f87;bpv=0;bpt=1>

bitset:
This problem has existed for a long time and was first introduced: <https://source.chromium.org/chromium/chromium/src/+/5f9f7f0695a6c3bc37a1525f04436ee79a8c2179>

# Summary

AddressSanitizer: heap-use-after-free on NetExportMessageHandler::SendEmail

# Custom Questions

#### Type of crash:

browser

#### Crash state:

see uaf5-asan.log

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A

## Attachments

- [uaf5-asan.log](attachments/uaf5-asan.log) (text/plain, 103.3 KB)
- [fix5.patch](attachments/fix5.patch) (text/x-diff, 1.1 KB)

## Timeline

### li...@gmail.com (2024-06-27)

credit to : lime(@limeSec\_) and noir(@noiir0709) From TIANGONG Team of Legendsec at QI-ANXIN Group, thanks.

### el...@chromium.org (2024-06-27)

Security shepherd: thanks for the report. I confirmed by inspection that this bug is present in //ios/chrome/browser/webui/ui\_bundled/net\_export/net\_export\_ui.mm but not in //chrome/browser/ui/webui/net\_export\_ui.cc, so I'm guessing this one is iOS-only.

Over to ricea@ from //net/OWNERS. Marking this Pri-2 Sev-2 since I don't believe there is a way for a remote attacker to trigger this one (they can't cause the netlog page to close at a targeted time).

### li...@gmail.com (2024-06-27)

Thanks for reply. I think what you said is right. and i make a fix. Please refer to it.

### pe...@google.com (2024-06-28)

Setting milestone because of s2 severity.

### ri...@chromium.org (2024-07-01)

Thanks for the patch. I wrote the fix from scratch to avoid you having to deal with CLA issues.

### ap...@google.com (2024-07-02)

Project: chromium/src
Branch: main

commit fccd7f579d5e8b522991936994036868cdc6ed03
Author: Adam Rice <ricea@chromium.org>
Date:   Tue Jul 02 02:58:51 2024

    Fix crash sending mail from chrome://net-export
    
    Clicking "send email" and immediately closing the site would crash on
    iOS due to a use of base::Unretained. Fix it.
    
    BUG=349653218
    
    Low-Coverage-Reason: TRIVIAL_CHANGE Minor bug fix to untested code.
    Change-Id: I52d6d1b9b6047a5bb81562aca6ce5281775e2132
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5670141
    Code-Coverage: findit-for-me@appspot.gserviceaccount.com <findit-for-me@appspot.gserviceaccount.com>
    Reviewed-by: Yoichi Osato <yoichio@chromium.org>
    Commit-Queue: Adam Rice <ricea@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1321970}

M       ios/chrome/browser/webui/ui_bundled/net_export/net_export_ui.mm

https://chromium-review.googlesource.com/5670141


### pe...@google.com (2024-07-02)

Requesting merge to beta (M127) because latest trunk commit (1321970) appears to be after beta branch point (1313161).
Merge rejected: M127 is already shipping to beta and this issue is marked as a Priority:P2,P3 or Type:feature request.

Please contact the milestone owner if you have questions.
Owners: eakpobaro (Android), eakpobaro (iOS), alonbajayo (ChromeOS), danielyip (Desktop)
Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [127].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.

### ri...@chromium.org (2024-07-03)

1. <https://chromium-review.googlesource.com/c/chromium/src/+/5670141>
2. Not yet (it seems that there's no canary for iOS?)
3. It is reasonably expected to be safe.
4. None.
5. It would be helpful if someone would verify the issue is fixed on an iOS device. I don't have one.

### am...@chromium.org (2024-07-16)

Medium severity issues are considered P1; because this issue was marked P2 the bot assumed it was not a security issue or was a feature request and auto-rejected merge
Since this is a very minimal and safe fix, I'm going to go ahead and approve this for merge to M127 / branch 6533
M127 Stable RC is supposed to be cut today, but I'm not sure if that is the case for iOS, so please merge this fix as soon as possible so that it can be included in the next M127 update

### pe...@google.com (2024-07-22)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ap...@google.com (2024-07-23)

Project: chromium/src
Branch: refs/branch-heads/6533

commit 275c26ff2812df38ac11f97dbd2c1c8b843f74a3
Author: Adam Rice <ricea@chromium.org>
Date:   Tue Jul 23 17:55:38 2024

    Fix crash sending mail from chrome://net-export
    
    Clicking "send email" and immediately closing the site would crash on
    iOS due to a use of base::Unretained. Fix it.
    
    BUG=349653218
    
    (cherry picked from commit fccd7f579d5e8b522991936994036868cdc6ed03)
    
    Low-Coverage-Reason: TRIVIAL_CHANGE Minor bug fix to untested code.
    Change-Id: I52d6d1b9b6047a5bb81562aca6ce5281775e2132
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5670141
    Code-Coverage: findit-for-me@appspot.gserviceaccount.com <findit-for-me@appspot.gserviceaccount.com>
    Reviewed-by: Yoichi Osato <yoichio@chromium.org>
    Commit-Queue: Adam Rice <ricea@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1321970}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5733472
    Commit-Queue: Harry Souders <harrysouders@google.com>
    Cr-Commit-Position: refs/branch-heads/6533@{#1787}
    Cr-Branched-From: 7e0b87ec6b8cb5cb2969e1479fc25776e582721d-refs/heads/main@{#1313161}

M       ios/chrome/browser/webui/ui_bundled/net_export/net_export_ui.mm

https://chromium-review.googlesource.com/5733472


### vb...@google.com (2024-07-23)

Verified on chrome beta version 127.0.6533.77 following the steps mentioned in comment #0 and #12 on iPhone 15 pro max with iOS 17.5.1.  No crashes are observed.  Looks good.

### sp...@google.com (2024-07-25)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
report of highly mitigated memory corruption in a non-sandboxed process -- mitigated by preconditions to exploit and user gesture 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-07-25)

Thank you for your efforts and reporting this issue to us, lime!

### pe...@google.com (2024-10-09)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/349653218)*
