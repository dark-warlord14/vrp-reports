# Security: Side-channel attack allows accessing the browsing history

| Field | Value |
|-------|-------|
| **Issue ID** | [40064616](https://issues.chromium.org/issues/40064616) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Paint, Internals>GPU |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | is...@oy.ne.ro |
| **Assignee** | ky...@chromium.org |
| **Created** | 2023-05-17 |
| **Bounty** | $1,000.00 |

## Description

Dear Chromium Developers,

My co-authors and I are security researchers from the New Jersey Institute of Technology. Later this month, we plan to submit a paper to the journal IEEE Transactions on Dependable and Secure Computing, titled "Contention-Based Side Channels Enable Faster and Stealthier Browsing History Sniffing".

In this paper, we describe attacks based on novel use of side channel techniques, which let a malicious website discover a visitor’s browsing history. Our attacks were developed for Chrome v109.0 on a Lenovo ThinkPad P14s with an Intel i7-10610U CPU running Windows 11 Pro, and later validated on an Intel Core I9-9900K running Chrome Version 113.0.5672.126 on MacOS Ventura 13.3.1 

The paper includes an artifact repository containing attack pages, which can be accessed as follows:
git clone https://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@github.com/mjz3/HistorySniffing2023.git

We attach a draft of the paper, which includes a discussion on potential defenses. We would be happy to discuss our findings with you, and are looking forward to collaborating with you in responsibly addressing the risks we identified. For your information, the journal we are submitting to has a typical decision timeframe of 6 months.

Please note that the paper draft we are sharing is not public at this point in time. As such, we ask that you do not distribute it outside your organization.

Respectfully yours,
-Reza, Yossi, and Mojtaba



## Attachments

- [paper_main.pdf](attachments/paper_main.pdf) (application/pdf, 347.7 KB)

## Timeline

### [Deleted User] (2023-05-17)

[Empty comment from Monorail migration]

### is...@oy.ne.ro (2023-05-17)

Kindly requesting to add the following users to the cc list:
rbyers@chromium.org 
slightlyoff@chromium.org
tabatkins@chromium.org
mz334@njit.edu
crix@njit.edu

Thanks!

### ma...@google.com (2023-05-18)

[Empty comment from Monorail migration]

### ma...@google.com (2023-05-18)

[Empty comment from Monorail migration]

### aj...@google.com (2023-05-18)

[Empty comment from Monorail migration]

### ke...@chromium.org (2023-05-18)

Thank you for sharing the paper.

I'm assigning to clamy@ who seems to own outstanding side channel attack reports, but if there are other people looking specifically at :visited link style inference then they might be better owners.

### [Deleted User] (2023-05-18)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-19)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-05-22)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-05-31)

clamy: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@oy.ne.ro (2023-06-02)

Cross-reference with Mozilla bug: https://bugzilla.mozilla.org/show_bug.cgi?id=1833918

### aj...@google.com (2023-06-02)

[Empty comment from Monorail migration]

### xi...@chromium.org (2023-06-05)

[Empty comment from Monorail migration]

[Monorail components: Blink>Animation Internals>GPU]

### aj...@google.com (2023-06-05)

CC'ing Blink>Animation owners for visibility

### cw...@chromium.org (2023-06-06)

With respect to the GPU contention measurement described in the paper, `convertToBlob()` with no other calls being sufficient to measure contention likely means that it is measuring CPU contention on the GPU process and not GPU contention.

The only solution that seems close to as good as double-keying, would be to do what Firefox does and recompute the style even if the :visited class wasn't changed, but also render both the :visited type, and not :visited links. (this would make all links have the cost of the addition of :visited and not :visited). Not sure how viable or implementable this would be.

### ke...@chromium.org (2023-06-06)

If the element has a CSS transition, Blink will generate a CSS transition if either its visited or not:visited style is changed.  This at least rules out being able to look at transition events to determine if visited.  With the restricted list of properties that can be applied to visited links, any animations should run on the main thread (project to composite background color animations which is still a work in progress).  With the animation running on the main thread, it'll produce animation frames and a style update on each frame. 

### [Deleted User] (2023-06-14)

clamy: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### fl...@chromium.org (2023-06-14)

This attack vector doesn't seem to rely on the animation infrastructure at all - save for requestAnimationFrame which was only used for regular frame timing and in this contention attack could be replaced by a setTimeout or any other means of predictable measurable timing. Removing Blink>Animation.

Adding Blink>Paint for consideration of whether we could always do the work for a full style change / painting regardless of whether there was a change. I suspect this may be difficult to get right without making link pseudoclass changes very expensive.

Though it seems like we should consider double keying to close out this class of leak as preventing any means of glimpsing the difference seems quite difficult.

[Monorail components: -Blink>Animation Blink>Paint]

### fl...@chromium.org (2023-06-14)

Tab has plans to pursue keying visited links[1] to solve these :visited attacks.

[1] https://github.com/kyraseevers/Partitioning-visited-links-history

### [Deleted User] (2023-07-17)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-07-27)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pd...@chromium.org (2023-08-01)

A fix is actively being pursued in https://crbug.com/1448609.

Updating the priority to match https://crbug.com/1448609 as well as the guidance in https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/severity-guidelines.md.

### [Deleted User] (2023-08-16)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-11)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-06)

[Empty comment from Monorail migration]

### yu...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-10)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-11)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-11)

This issue was migrated from crbug.com/chromium/1446288?no_tracker_redirect=1

[Multiple monorail components: Blink>Paint, Internals>GPU]
[Monorail blocked-on: crbug.com/chromium/1448609]
[Monorail components added to Component Tags custom field.]

### ph...@chromium.org (2024-06-24)

From From <https://chromestatus.com/feature/5101991698628608>, an origin trial is planned starting M128. Setting a next action date around that to revisit.

### pe...@google.com (2024-07-22)

The NextAction date has arrived: 2024-07-22
To opt-out from this automation rule, please add Optout-Blintz-Nextaction-Alert to the "Chromium Labels" custom field.

### pe...@google.com (2024-10-26)

tabatkins: Uh oh! This issue still open and hasn't been updated in the last 499 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### pe...@google.com (2024-11-13)

kyraseevers: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ky...@google.com (2024-11-13)

We are currently running experiments and hope to launch partitioned :visited links in Q1.

### is...@oy.ne.ro (2025-01-05)

Dear Chromium Devs, the paper covering this result is now ready to publish, and we are preparing to make the repository with the PoC attack code public. Do you have any comments at this time?

Respectfully yours,
Yossi (on behalf of the authors).

### rb...@chromium.org (2025-01-06)

Thank you for the heads up! I'm checking with some colleagues to see if we want to prepare a statement. How long do we have before publication?

Do you agree with our assessment that [our partitioned visited links](https://github.com/explainers-by-googlers/Partitioning-visited-links-history) design pretty much solves this entire class of problems?

### mi...@chromium.org (2025-01-07)

It appears that <https://github.com/mjz3/HistorySniffing2023> is already public (as of today, anyways), or was there a different repository to be made public as well?

### mi...@chromium.org (2025-01-07)

iss@, if you're looking for a comment:

This research highlights the increasing value of addressing a longstanding risk in the web platform, and we're happy to see further validation of our significant investment in addressing this class of privacy threats once and for all which we currently plan to launch to all Chrome users in the coming months.

### is...@oy.ne.ro (2025-01-21)

Yes, we agree while visited link partitioning does not solve the general problem of privacy leaks via contention-based side channels, it still prevents the history-sniffing attacks we introduced in the paper. 

The repository was recently made public, when the paper was accepted to publication.

Thank you for the comment.

### ch...@google.com (2025-06-26)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### aj...@google.com (2025-07-02)

Paper was published in - 10.1109/TDSC.2025.3538541

### sp...@google.com (2025-07-02)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
Thank you for report demonstrating a security impact resulting that helped valid our planned work and prioritization of partitioning of :visited links history. 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-07-02)

Thank you for disclosing this issue to us ahead of publication. While we do not generally reward reports of issues publicly disclosed ahead of a fix and coordinated disclosure, you did give us sufficient heads up and time here so we did want to recognize that effort. 

### ch...@google.com (2025-10-03)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> Thank you for report demonstrating a security impact resulting that helped valid our planned work and prioritization of partitioning of :visited links history.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40064616)*
