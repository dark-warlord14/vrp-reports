# bypass blocked autoredirects from cross-origin iframes

| Field | Value |
|-------|-------|
| **Issue ID** | [40053780](https://issues.chromium.org/issues/40053780) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>PopupBlocker |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **CVE IDs** | CVE-2021-1765 |
| **Reporter** | el...@confiant.com |
| **Assignee** | jk...@chromium.org |
| **Created** | 2020-11-04 |
| **Bounty** | $5,000.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36

Steps to reproduce the problem:
Hi Team,

Current versions of desktop and mobile web browsers including Chrome, Safari, Edge, Opera, and Brave will block automatic redirects that are not activated by user interaction from cross-origin iframes.

Consider the following payload that will always get blocked when served in a cross-origin iframe:

<script>
    top.window.location = "https://google.com";
</script>

There exists a bug that bypasses this built-in mitigation and it's currently being leveraged as part of a malvertising chain to bypass the browser's redirect protection in order to drive traffic to malware. 

The following payload is being used:

<script type="text/javascript">
  var x = '<html><body><script type="text/javascript"> window.top.location = "https://google.com";' + '</scr' + 'ipt></body></html>';
  var bs64 = btoa(x);
  document.write('<iframe sandbox="allow-top-navigation allow-scripts" src="data:text/html;base64,' + bs64 + '"></iframe>')
</script>

We have observed through testing that the sandbox parameters in the injected frame are key in in the bypass here.

The following browsers have been tested and proven to be vulnerable:

- Chrome Desktop, Android, and iOS
- Edge Desktop
- Safari Desktop, iOS
- Edge Desktop
- Opera Desktop, Android
- Brave Desktop, Android

A note on impact:

This bug is being actively abused by a malvertising group that we at Confiant have dubbed Yosec, serving fake flash drive-by downloads and tech support scams. They have been able to successfully run their malicious ads on dozens of high profile websites, including those among the Comscore top 100. On November 3rd, their activity was running at such high volumes that we have observed up to 0.5% of all United States ad impressions at certain times.

We hope that you will prioritize a fix for this soon considering how disruptive and damaging malvertising campaigns like this can be.

Best,
Eliya Stein of Confiant

What is the expected behavior?
Automatic redirects from cross-origin iframes should be blocked by the browser.

What went wrong?
This is being bypassed with the payload provided above.

Did this work before? N/A 

Chrome version: 86.0.4240.111  Channel: n/a
OS Version: OS X 10.15.7
Flash Version:

## Timeline

### [Deleted User] (2020-11-04)

[Empty comment from Monorail migration]

### aw...@google.com (2020-11-04)

[Empty comment from Monorail migration]

### ke...@chromium.org (2020-11-05)

Thanks for the report.

To clarify, the JS code you are providing is from loaded in an ad iframe, correct? Is that iframe also sandboxed with the same flags?

[Monorail components: Blink>SecurityFeature>IFrameSandbox]

### el...@confiant.com (2020-11-05)

Hi,

Yes, the payload loads from within an ad iframe, typically a DFP Safe Frame, or any other cross-origin iframe.

The redirect will occur automatically if the iframe does not have additional sandboxing properties.

However, redirects like this would typically be blocked by the browser otherwise if not for the funky payload.

Best,
Eliya



### he...@google.com (2020-11-05)

Thank you for your report. This is more of a popup blocker bypass that an iframe sandbox one. 

Were able to reproduce with this:
publisher.origin: `<iframe src='advertiser.origin'></iframe>` // no sandbox, but is cross-origin
advertiser.origin (malicious) : ```
<iframe sandbox="allow-top-navigation allow-scripts" /* allow-top-navigation takes precedence over cross-origin */
  srcdoc="<script> window.top.location = 'http://example.com' </script>">
</iframe>

[Monorail components: UI>Browser>PopupBlocker]

### el...@confiant.com (2020-11-05)

Thanks for the feedback @hexed - I appreciate the additional context!



### [Deleted User] (2020-11-05)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-11-05)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ke...@chromium.org (2020-11-07)

[Empty comment from Monorail migration]

[Monorail components: -Blink>SecurityFeature>IFrameSandbox]

### ke...@chromium.org (2020-11-07)

avi@ are you able to have a look at this? Or else would you know a better owner?

### av...@chromium.org (2020-11-07)

I’m super busy with various Mac launches. Charlie, can you poke at this?

### [Deleted User] (2020-11-18)

csharrison: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-12-02)

csharrison: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cs...@chromium.org (2020-12-03)

[Empty comment from Monorail migration]

### jk...@chromium.org (2020-12-03)

The allow-top-navigation attribute is the embedder specifically allowing the sandboxed iframe to navigate the top frame without a gesture. This is working as intended. allow-top-navigation-by-user-activation should be used if the embedder doesn't want the frame to be able to navigate the top frame.



### jk...@chromium.org (2020-12-03)

Posted to soon, meant to say "if the embedder doesn't want the frame to be able to navigate the top frame without a user gesture".

### el...@confiant.com (2020-12-03)

@jkarlin - Thanks for your feedback, but I'm not sure that this is actually working as intended. If the top frame embeds a cross-origin iframe with a basic redirect along the lines of top.location = xxxx, then the browser prevents the redirection.

The payload supplied in the example above bypasses that block.

The example that we provided is not being run in the top frame, but rather this code is being run inside a cross-origin iframe:

<script type="text/javascript">
  var x = '<html><body><script type="text/javascript"> window.top.location = "https://google.com";' + '</scr' + 'ipt></body></html>';
  var bs64 = btoa(x);
  document.write('<iframe sandbox="allow-top-navigation allow-scripts" src="data:text/html;base64,' + bs64 + '"></iframe>')
</script>

This is currently being abused in malvertising campaigns to launch forced redirections from ad slots where the redirect would normally be blocked.

If this behavior is intentional, then I don't believe that cross-origin frames would block basic redirections in the first place as they consistently do these days.



### jk...@chromium.org (2020-12-03)

Sorry, I didn't realize that the sandboxed iframe was itself placed in a cross-origin iframe to the embedder. Yes, that does seem like a bug.

### jk...@chromium.org (2020-12-04)

I'll take a look.

### jk...@chromium.org (2020-12-04)

[Empty comment from Monorail migration]

### el...@confiant.com (2020-12-22)

Hey Team,

I just wanted to share with you all that Apple has acknowledged the issue as it pertains to safari and will be looking to fix it after the new year.

Not sure if this helps you in any way, but thought I'd offer an update.

Best,
Eliya

### [Deleted User] (2021-01-20)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### el...@confiant.com (2021-01-21)

Hi Team - I just got confirmation that Apple will be rolling out the webkit fix in an upcoming patch. Curious if there's a timeline for a fix in Chrome just so that we can prepare a coordinated disclosure that doesn't compromise any impacted vendor.

Thanks,
Eliya


### el...@confiant.com (2021-02-08)

Hi Team,

Just as an FYI this bug was assigned CVE-2021-1765 for Webkit.

Best,
Eliya



### jk...@chromium.org (2021-02-11)

I've put together a basic fix in http://crrev.com/c/2688360. Will flesh it out tomorrow.

### es...@chromium.org (2021-02-24)

jkarlin, are there any updates on https://chromium-review.googlesource.com/c/chromium/src/+/2688360?

### jk...@chromium.org (2021-02-24)

Bah, I just checked and my response to Daniel wasn't sent. It was sitting as a draft. Sent, will find a solution.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-03-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/c732f0ddc0573a0926d39b2f20c81591057c2878

commit c732f0ddc0573a0926d39b2f20c81591057c2878
Author: Josh Karlin <jkarlin@chromium.org>
Date: Mon Mar 01 19:19:08 2021

Prevent sandboxed frames escaping user-gesture intervention

What: This CL ensures that sandboxed iframes with "allow-top-navigation" can't
navigate the top frame if their embedder can't.

How: If the source frame is sandboxed and has allow-top-navigation, it
calls CanNavigate() recursive on its ancestors to see if they are
able to navigate the top frame. If not, return false. One can stop
calling recursively once the first non-sandboxed ancestor has been
checked.

Details: CanNavigate() is a LocalFrame method, but ancestor frames
may be remote. So in this CL CanNavigate's contents are extracted into
a static CanNavigateHelper method that works with both Frame*. The
LocalFrame* bits are only necessary on the initial call to CanNavigate,
and not the recursive calls which might be remote.

Bug: 1145553
Change-Id: I52474431d868f4f515918845784fe30f69c8c918
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2688360
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Commit-Queue: Josh Karlin <jkarlin@chromium.org>
Cr-Commit-Position: refs/heads/master@{#858644}

[add] https://crrev.com/c732f0ddc0573a0926d39b2f20c81591057c2878/third_party/blink/web_tests/http/tests/security/frameNavigation/sandbox-DENIED-cross-origin-top-navigation.html
[modify] https://crrev.com/c732f0ddc0573a0926d39b2f20c81591057c2878/third_party/blink/renderer/core/frame/local_frame.cc
[modify] https://crrev.com/c732f0ddc0573a0926d39b2f20c81591057c2878/third_party/blink/renderer/core/frame/local_frame.h
[add] https://crrev.com/c732f0ddc0573a0926d39b2f20c81591057c2878/third_party/blink/web_tests/flag-specific/disable-site-isolation-trials/http/tests/security/frameNavigation/sandbox-DENIED-cross-origin-top-navigation-nested-sandbox-expected.txt
[add] https://crrev.com/c732f0ddc0573a0926d39b2f20c81591057c2878/third_party/blink/web_tests/http/tests/security/frameNavigation/sandbox-DENIED-cross-origin-top-navigation-nested-sandbox.html
[add] https://crrev.com/c732f0ddc0573a0926d39b2f20c81591057c2878/third_party/blink/web_tests/http/tests/security/frameNavigation/sandbox-DENIED-cross-origin-top-navigation-expected.txt
[add] https://crrev.com/c732f0ddc0573a0926d39b2f20c81591057c2878/third_party/blink/web_tests/http/tests/security/frameNavigation/resources/cross-iframe-that-performs-top-navigation-in-nested-sandboxed-frame.html
[add] https://crrev.com/c732f0ddc0573a0926d39b2f20c81591057c2878/third_party/blink/web_tests/http/tests/security/frameNavigation/sandbox-DENIED-cross-origin-top-navigation-nested-sandbox-expected.txt
[add] https://crrev.com/c732f0ddc0573a0926d39b2f20c81591057c2878/third_party/blink/web_tests/http/tests/security/frameNavigation/resources/cross-iframe-that-performs-top-navigation-in-sandboxed-frame.html
[add] https://crrev.com/c732f0ddc0573a0926d39b2f20c81591057c2878/third_party/blink/web_tests/http/tests/security/frameNavigation/resources/failed-top-navigation.html
[add] https://crrev.com/c732f0ddc0573a0926d39b2f20c81591057c2878/third_party/blink/web_tests/flag-specific/disable-site-isolation-trials/http/tests/security/frameNavigation/sandbox-DENIED-cross-origin-top-navigation-expected.txt


### [Deleted User] (2021-03-03)

[Empty comment from Monorail migration]

### ad...@google.com (2021-03-10)

jkarlin@ do you consider https://crbug.com/chromium/1145553#c29 a complete fix? If so please mark this as Fixed.

### [Deleted User] (2021-03-11)

[Empty comment from Monorail migration]

### zh...@google.com (2021-03-17)

[Empty comment from Monorail migration]

### jk...@chromium.org (2021-04-06)

Whoops, sorry for missing your comment earlier. Yes, this should be fixed now.

### ad...@google.com (2021-04-06)

Thanks!

### [Deleted User] (2021-04-06)

[Empty comment from Monorail migration]

### el...@confiant.com (2021-04-06)

Hi Team,

We have been waiting for the fix to be confirmed before doing a public disclosure, is it safe to do so now?

Thanks,
Eliya

### [Deleted User] (2021-04-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-06)

Requesting merge to beta M90 because latest trunk commit (858644) appears to be after beta branch point (857950).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-04-06)

This bug requires manual review: We are only 6 days from stable.
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
Owners: govind@(Android), bindusuvarna@(iOS), cindyb@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2021-04-06)

Re https://crbug.com/chromium/1145553#c37: Hi Eliya, unfortunately not. The bug will be opened to the public 14 weeks after it's officially marked "Fixed", in order to give time (a) for us to release the fix, which may be M90 next week but might be somewhat later, (b) for our users to absorb that fix (it takes a while for everyone to restart their browsers) and (c) for downstream Chromium browser vendors to absorb the fix. This last reason is the main reason for the long-seeming 14 week delay.

So you'll be able to talk about this publicly 14 weeks after today. We're a bit flexible on that exact date if you have a specific event in mind, but that's the default.

Of course, it's your bug so you're welcome to talk about it whenever you like, but these are the guidelines for it to be VRP-eligible.

Thanks very much for the report!

### el...@confiant.com (2021-04-06)

Thanks for the explanation. We will hold off on sharing the details for now.

### jk...@chromium.org (2021-04-06)

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines

This is an abuse fix rather than pure security, as it allows x-origin frames to navigate the top frame without having first received a user gesture. The code is moderately complex, and has a small chance to break platform behavior. It has been in canary/dev for 3 weeks now, so that increases confidence.

2. Links to the CLs you are requesting to merge.
https://chromium-review.googlesource.com/c/chromium/src/+/2688360

3. Has the change landed and been verified on ToT?
Change was landed 3 weeks ago. Verified via tests.

4. Does this change need to be merged into other active release branches (M-1, M+1)?
Just M90

5. Why are these changes required in this milestone after branch?
Because it's a way around our abuse intervention.

6. Is this a new feature?
No.

7. If it is a new feature, is it behind a flag using finch?
No.

### ad...@google.com (2021-04-06)

Discussed with jkarlin@ offline, and we're concerned that there's a slim chance that this could have unexpected compatibility implications. I'm therefore rejecting merge to M90 and this will be released in M91, which will give us and the wider community 6 weeks more to spot any such implications.

### am...@google.com (2021-04-22)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-04-23)

Hi, Eliya! Congratulations, the VRP Panel has decided to award you $5000 for this report. Nice work and quality report! 

### am...@chromium.org (2021-04-23)

eliya@ I also meant to mention to please look out for the emails I sent to the VRP researcher community about changes with the payment process! It will temporarily affect payment process starting this week. 

### el...@confiant.com (2021-04-26)

Thanks Amy! Excited to share this with my team :)

### am...@google.com (2021-04-26)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-05-24)

[Empty comment from Monorail migration]

### am...@google.com (2021-05-24)

[Empty comment from Monorail migration]

### ja...@google.com (2021-05-25)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-25)

[Empty comment from Monorail migration]

### gi...@google.com (2021-05-26)

[Empty comment from Monorail migration]

### am...@google.com (2021-06-07)

[Empty comment from Monorail migration]

### as...@google.com (2021-06-08)

[Empty comment from Monorail migration]

### [Deleted User] (2021-06-08)

[Empty comment from Monorail migration]

### gi...@google.com (2021-06-09)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-06-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/8fab4012a41825999014bc83ab253891edeef3c9

commit 8fab4012a41825999014bc83ab253891edeef3c9
Author: Josh Karlin <jkarlin@chromium.org>
Date: Wed Jun 09 16:45:58 2021

[M90-LTS] Prevent sandboxed frames escaping user-gesture intervention

What: This CL ensures that sandboxed iframes with "allow-top-navigation" can't
navigate the top frame if their embedder can't.

How: If the source frame is sandboxed and has allow-top-navigation, it
calls CanNavigate() recursive on its ancestors to see if they are
able to navigate the top frame. If not, return false. One can stop
calling recursively once the first non-sandboxed ancestor has been
checked.

Details: CanNavigate() is a LocalFrame method, but ancestor frames
may be remote. So in this CL CanNavigate's contents are extracted into
a static CanNavigateHelper method that works with both Frame*. The
LocalFrame* bits are only necessary on the initial call to CanNavigate,
and not the recursive calls which might be remote.

(cherry picked from commit c732f0ddc0573a0926d39b2f20c81591057c2878)

Bug: 1145553
Change-Id: I52474431d868f4f515918845784fe30f69c8c918
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2688360
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Commit-Queue: Josh Karlin <jkarlin@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#858644}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2947088
Owners-Override: Artem Sumaneev <asumaneev@google.com>
Reviewed-by: Victor-Gabriel Savu <vsavu@google.com>
Commit-Queue: Artem Sumaneev <asumaneev@google.com>
Cr-Commit-Position: refs/branch-heads/4430@{#1507}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[modify] https://crrev.com/8fab4012a41825999014bc83ab253891edeef3c9/third_party/blink/renderer/core/frame/local_frame.cc
[modify] https://crrev.com/8fab4012a41825999014bc83ab253891edeef3c9/third_party/blink/renderer/core/frame/local_frame.h
[add] https://crrev.com/8fab4012a41825999014bc83ab253891edeef3c9/third_party/blink/web_tests/flag-specific/disable-site-isolation-trials/http/tests/security/frameNavigation/sandbox-DENIED-cross-origin-top-navigation-expected.txt
[add] https://crrev.com/8fab4012a41825999014bc83ab253891edeef3c9/third_party/blink/web_tests/flag-specific/disable-site-isolation-trials/http/tests/security/frameNavigation/sandbox-DENIED-cross-origin-top-navigation-nested-sandbox-expected.txt
[add] https://crrev.com/8fab4012a41825999014bc83ab253891edeef3c9/third_party/blink/web_tests/http/tests/security/frameNavigation/resources/cross-iframe-that-performs-top-navigation-in-nested-sandboxed-frame.html
[add] https://crrev.com/8fab4012a41825999014bc83ab253891edeef3c9/third_party/blink/web_tests/http/tests/security/frameNavigation/resources/cross-iframe-that-performs-top-navigation-in-sandboxed-frame.html
[add] https://crrev.com/8fab4012a41825999014bc83ab253891edeef3c9/third_party/blink/web_tests/http/tests/security/frameNavigation/resources/failed-top-navigation.html
[add] https://crrev.com/8fab4012a41825999014bc83ab253891edeef3c9/third_party/blink/web_tests/http/tests/security/frameNavigation/sandbox-DENIED-cross-origin-top-navigation-expected.txt
[add] https://crrev.com/8fab4012a41825999014bc83ab253891edeef3c9/third_party/blink/web_tests/http/tests/security/frameNavigation/sandbox-DENIED-cross-origin-top-navigation-nested-sandbox-expected.txt
[add] https://crrev.com/8fab4012a41825999014bc83ab253891edeef3c9/third_party/blink/web_tests/http/tests/security/frameNavigation/sandbox-DENIED-cross-origin-top-navigation-nested-sandbox.html
[add] https://crrev.com/8fab4012a41825999014bc83ab253891edeef3c9/third_party/blink/web_tests/http/tests/security/frameNavigation/sandbox-DENIED-cross-origin-top-navigation.html


### as...@google.com (2021-06-09)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-06-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/6599d28cc87459bfc3f20f7e4eab9a783ad2bfdb

commit 6599d28cc87459bfc3f20f7e4eab9a783ad2bfdb
Author: Jana Grill <janagrill@google.com>
Date: Mon Jun 14 19:34:13 2021

[M86-LTS] Prevent sandboxed frames escaping user-gesture intervention

What: This CL ensures that sandboxed iframes with "allow-top-navigation" can't
navigate the top frame if their embedder can't.

How: If the source frame is sandboxed and has allow-top-navigation, it
calls CanNavigate() recursive on its ancestors to see if they are
able to navigate the top frame. If not, return false. One can stop
calling recursively once the first non-sandboxed ancestor has been
checked.

Details: CanNavigate() is a LocalFrame method, but ancestor frames
may be remote. So in this CL CanNavigate's contents are extracted into
a static CanNavigateHelper method that works with both Frame*. The
LocalFrame* bits are only necessary on the initial call to CanNavigate,
and not the recursive calls which might be remote.

M86 merge conflicts and resolution:
* third_party/blink/renderer/core/frame/local_frame.cc
  crrev.com/c/2579744 changes PrintNavigationErrorMessage to report
  "Unsafe attempt" instead of "Unsafe JavaScript attempt". The CL is
  missing from M86 which causes test failures for current CL if
  merged as is. Keep old message with JavaScript and update *.txt
  files to use it.

(cherry picked from commit c732f0ddc0573a0926d39b2f20c81591057c2878)

Bug: 1145553
Change-Id: I52474431d868f4f515918845784fe30f69c8c918
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2688360
Commit-Queue: Josh Karlin <jkarlin@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#858644}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2915720
Commit-Queue: Artem Sumaneev <asumaneev@google.com>
Owners-Override: Artem Sumaneev <asumaneev@google.com>
Reviewed-by: Achuith Bhandarkar <achuith@chromium.org>
Reviewed-by: Victor-Gabriel Savu <vsavu@google.com>
Cr-Commit-Position: refs/branch-heads/4240@{#1671}
Cr-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}

[modify] https://crrev.com/6599d28cc87459bfc3f20f7e4eab9a783ad2bfdb/third_party/blink/renderer/core/frame/local_frame.cc
[modify] https://crrev.com/6599d28cc87459bfc3f20f7e4eab9a783ad2bfdb/third_party/blink/renderer/core/frame/local_frame.h
[add] https://crrev.com/6599d28cc87459bfc3f20f7e4eab9a783ad2bfdb/third_party/blink/web_tests/flag-specific/disable-site-isolation-trials/http/tests/security/frameNavigation/sandbox-DENIED-cross-origin-top-navigation-expected.txt
[add] https://crrev.com/6599d28cc87459bfc3f20f7e4eab9a783ad2bfdb/third_party/blink/web_tests/flag-specific/disable-site-isolation-trials/http/tests/security/frameNavigation/sandbox-DENIED-cross-origin-top-navigation-nested-sandbox-expected.txt
[add] https://crrev.com/6599d28cc87459bfc3f20f7e4eab9a783ad2bfdb/third_party/blink/web_tests/http/tests/security/frameNavigation/resources/cross-iframe-that-performs-top-navigation-in-nested-sandboxed-frame.html
[add] https://crrev.com/6599d28cc87459bfc3f20f7e4eab9a783ad2bfdb/third_party/blink/web_tests/http/tests/security/frameNavigation/resources/cross-iframe-that-performs-top-navigation-in-sandboxed-frame.html
[add] https://crrev.com/6599d28cc87459bfc3f20f7e4eab9a783ad2bfdb/third_party/blink/web_tests/http/tests/security/frameNavigation/resources/failed-top-navigation.html
[add] https://crrev.com/6599d28cc87459bfc3f20f7e4eab9a783ad2bfdb/third_party/blink/web_tests/http/tests/security/frameNavigation/sandbox-DENIED-cross-origin-top-navigation-expected.txt
[add] https://crrev.com/6599d28cc87459bfc3f20f7e4eab9a783ad2bfdb/third_party/blink/web_tests/http/tests/security/frameNavigation/sandbox-DENIED-cross-origin-top-navigation-nested-sandbox-expected.txt
[add] https://crrev.com/6599d28cc87459bfc3f20f7e4eab9a783ad2bfdb/third_party/blink/web_tests/http/tests/security/frameNavigation/sandbox-DENIED-cross-origin-top-navigation-nested-sandbox.html
[add] https://crrev.com/6599d28cc87459bfc3f20f7e4eab9a783ad2bfdb/third_party/blink/web_tests/http/tests/security/frameNavigation/sandbox-DENIED-cross-origin-top-navigation.html


### as...@google.com (2021-06-14)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-21)

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

This issue was migrated from crbug.com/chromium/1145553?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053780)*
