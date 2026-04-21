# Security: allow-top-navigation-by-user-activation bypasses via message event listeners on iOS

| Field | Value |
|-------|-------|
| **Issue ID** | [40052658](https://issues.chromium.org/issues/40052658) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Mobile>iOSWeb>Security |
| **Platforms** | iOS |
| **CVE IDs** | CVE-2019-19788, CVE-2019-5840, CVE-2019-8771, CVE-2021-1801 |
| **Reporter** | el...@confiant.com |
| **Assignee** | ga...@google.com |
| **Created** | 2020-06-24 |
| **Bounty** | $5,000.00 |

## Description

Hi Team,

We have a couple of new examples of iframe sandbox bypasses that are actively being exploited by malvertisers. For context, we have reported similar findings in the past:

CVE-2019-5840
CVE-2019-8771
CVE-2019-19788

Recently, we've observed a malvertising attack where the client-side javascript payload uses the following mechanism in order to attempt forced redirection:

function receiveMessage(event) {
    top.location.href = "http://evil-landing-page.xxx";
}

window.addEventListener("message", receiveMessage);

This payload was observed to be serving via ads on a page where there was a lot of postMessage activity flying around, so we staged the experiment attached.

origin1.html -> loads payload.html under a different origin with standard ad serving sandbox parameters. Includes a button that dispatches a message to the child frame.

payload.html -> implements redirect payload above

To stage this locally, add origin1.me and origin2.me to /etc/hosts -> localhost, and point the browser to http://origin1.me/origin1.html.

Findings:

1) While Chrome on Desktop does a good job blocking the redirect upon load and upon click, we found that on Chrome for IOS, the user is redirected upon click. This is also true for Safari on Desktop, and we will be reporting this to the Apple team as well.

Given the complexity of modern day websites and that postMessages are often flying around indiscriminately, we believe that a user action that dispatches a postMessage to a sandboxed frame should not be treated as a valid activation for a top level redirect.

2) Another example of such a bypass is dependent on user interaction with a chrome extension that leverages postMessage in injected contexts. This can be tested with the MetaMask extension, which does exactly that. 

Given the test scenario above, if this malicious payload is loaded in a MetaMask enabled browser, the redirect will still be blocked upon page load and upon interaction with the "clickme" button. However, if the user interacts with MetaMask and switches the target network, MetaMask will dispatch a postMessage within the context of every frame, including the malicious frame and the user will be immediately redirected. 

We believe that interaction with a browser extension should not be treated as a valid activation for a top level redirect from a cross-origin & sandboxed frame.

While the path to the scenarios described above are a bit "long tail", the impact can actually be significant given that malvertisers like this are running large campaigns that sometimes touch millions of users in a matter of hours.

Looking forward to your feedback.

Best,
Eliya Stein


## Attachments

- [payload.html](attachments/payload.html) (text/plain, 427 B)
- [origin1.html](attachments/origin1.html) (text/plain, 469 B)

## Timeline

### dt...@chromium.org (2020-06-24)

[Empty comment from Monorail migration]

[Monorail components: Blink>Input]

### mu...@chromium.org (2020-06-24)

[Empty comment from Monorail migration]

### mu...@chromium.org (2020-06-24)

Thanks for filing the issue!  We have two different sub-problems here, as reported in the original post under "findings":

1) This is specific to Chrome for iOS which is WebKit-based and has its own set of activation problems.  Let's focus this bug on this finding.

2) And let's separate this problem out...we have this (public) https://crbug.com/chromium/1077139 to cover one subpart of a bigger problem, please comment there if your observation seems related.  If not, please file a separate bug.  Re the bigger problem (https://crbug.com/chromium/957553, sorry it's restricted): in short we can't "just fix it" because of some weird compat implications!

### mu...@chromium.org (2020-06-24)

As per my last comment, labeling this bug to cover the first finding.

### el...@confiant.com (2020-06-24)

Thanks for your feedback and comments. At first glance, it does seem like our observation is likely a manifestation of the issue referenced in https://crbug.com/chromium/1077139, or at the very least closely related. Happy to comment on that thread with the finding above and hopefully that will offer some additional context.

### bd...@chromium.org (2020-06-25)

@mustaq, I'm assigning this to you but feel free to assign this to someone else 

### [Deleted User] (2020-06-25)

[Empty comment from Monorail migration]

### mu...@chromium.org (2020-06-25)

We need experts from Bling to handle this.

gambard@: I am assigning to you since you have handled similar problems on iOS through https://crbug.com/chromium/954570.  If you are not the right owner, could you please help us find one?

### eu...@chromium.org (2020-06-25)

Sounds like Safari has the same behavior, and Chrome for iOS has to use the same rendering engine.

### [Deleted User] (2020-06-26)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-06-26)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ga...@chromium.org (2020-06-29)

Chrome on iOS has to use WebKit, and it seems that the issue reproduce on Safari.
I am not sure to see how we could fix it on the Chrome side.
I would rather have it marked as external dependency.

### [Deleted User] (2020-07-13)

gambard: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ga...@chromium.org (2020-07-24)

I still think that the path forward is to file a bug against Apple https://feedbackassistant.apple.com/ or WebKit https://bugs.webkit.org/ (eliya@ you should do it to get the credit), and mark this one as external dependency.

### el...@confiant.com (2020-07-24)

Thanks for the feedback. I've already filed this with Apple via their product-security@apple.com alias as I've done in the past with CVE-2019-8771.

They confirmed that they are investigating the report on June 29th. Unfortunately that's the only feedback I have gotten since reporting the issue, so I will have to reach out for an update soon.

### aj...@google.com (2020-07-24)

Thanks. I'm marking as ExternalDependency. We like security bugs to have an owner, so assigning to gambard@ to keep an eye on things. Feel free to assign to someone else if they can do so.

eliya: do you have a radar or other reference to help us track this?

### el...@confiant.com (2020-07-24)

Here's what I have:

"Please include the line below in follow-up emails for this request. Follow-up: 738545906 Hello,"


And then this:


"We don't automatically provide status updates on issues as we work on them. We will reach out if we have any questions or need additional details. Please include the Follow-up: number when requesting updates. Including this Follow-up: number allows us to rapidly associate it with your original report."



### [Deleted User] (2020-08-26)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-07)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-30)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-31)

[Empty comment from Monorail migration]

### eu...@chromium.org (2020-11-12)

[Empty comment from Monorail migration]

[Monorail components: -Blink>Input Mobile>iOSWeb>Security]

### [Deleted User] (2020-11-18)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-14)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-20)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-21)

[Empty comment from Monorail migration]

### el...@confiant.com (2021-02-01)

Hi Team, just a heads up that we got some feedback from Apple that a fix is pending in the coming weeks.

### eu...@chromium.org (2021-02-01)

[Empty comment from Monorail migration]

### el...@confiant.com (2021-02-02)

Hi Team, 

From Apple:

WebKit
Impact: Maliciously crafted web content may violate iframe sandboxing policy
Description: This issue was addressed with improved iframe sandbox enforcement.
CVE-2021-1801: Eliya Stein of Confiant

Hope this helps.

### ga...@chromium.org (2021-02-02)

Great, thanks for letting us know!
We can now wait for the fix to be released in a future iOS version.

### el...@confiant.com (2021-02-02)

My understanding is that the fix is available in ios 14.4

### aj...@chromium.org (2021-02-02)

This is indeed fixed in iOS 14.4, by https://trac.webkit.org/changeset/270373/webkit.

### [Deleted User] (2021-02-02)

[Empty comment from Monorail migration]

### [Deleted User] (2021-02-02)

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M89. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-02-02)

This bug requires manual review: Less than 24 days to go before AppStore submit on M89
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on ToT?
4. Does this change need to be merged into other active release branches (M-1, M+1)?
5. Why are these changes required in this milestone after branch?
6. Is this a new feature?
7. If it is a new feature, is it behind a flag using finch?

Chrome OS Only:
8. Was the change reviewed and approved by the Eng Prod Representative? See Eng Prod ownership by component: http://go/cros-engprodcomponents

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), bindusuvarna@(iOS), geohsu@(ChromeOS), pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aj...@chromium.org (2021-02-02)

There's nothing to merge in Chromium. The fix landed in WebKit and is shipping in iOS 14.4.

### am...@google.com (2021-02-18)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2021-02-18)

Congratulations, Eliya! The VRP Panel has decided to award you $5,000 for this report. Thank you for informing us of this issue! 

### el...@confiant.com (2021-02-18)

Thank you! I'm excited to share this with my team.

### aw...@google.com (2021-02-19)

[Empty comment from Monorail migration]

### ad...@google.com (2021-02-26)

[Empty comment from Monorail migration]

### ad...@google.com (2021-02-26)

Fixed entirely in WebKit (AIUI) so no release notes mention here.

### [Deleted User] (2021-05-11)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

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

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1098582?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-19)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40052658)*
