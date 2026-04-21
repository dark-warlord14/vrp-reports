# Reading local files through an extension that doesn't have the file permission

| Field | Value |
|-------|-------|
| **Issue ID** | [40054742](https://issues.chromium.org/issues/40054742) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>Extensions |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | he...@gmail.com |
| **Assignee** | ct...@chromium.org |
| **Created** | 2021-02-08 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

The "tabCapture" permission allows capturing the visible area of a given tab, but doesn't seem to block the capture when the tab gets redirected to a local file - which allows an attacker to leak its contents even though the file permission was not given.

**VERSION**  

Chrome Version: 88.0.4324.150 (Official Build) (64-bit)  

Operating System: Windows 10

**REPRODUCTION CASE**

1. Download extension.zip and load it into Chrome.
2. Make sure you have the file permission disabled for the extension.
3. Click on the extension's icon on the Chrome toolbar.
4. After a few seconds, the contents of file:///C:/ will be shown inside a video tag. This information can be exfiltrated to the attacker's server.

Here's an unlisted video demonstrating the issue:  

<https://youtu.be/sKfKbhOLDKo>

**CREDIT INFORMATION**  

Reporter credit: Luan Herrera (@lbherrera\_)

## Attachments

- [extension.zip](attachments/extension.zip) (application/octet-stream, 2.7 KB)
- [background.js](attachments/background.js) (text/plain, 829 B)
- [receiver.js](attachments/receiver.js) (text/plain, 227 B)
- [manifest.json](attachments/manifest.json) (text/plain, 422 B)
- [receiver.html](attachments/receiver.html) (text/plain, 175 B)
- [icon.png](attachments/icon.png) (image/png, 1.2 KB)

## Timeline

### [Deleted User] (2021-02-08)

[Empty comment from Monorail migration]

### ts...@chromium.org (2021-02-08)

[Comment Deleted]

### ts...@chromium.org (2021-02-08)

Gah, pasted wrong link, try again - possible duplicate of https://crbug.com/1116450 ?

[Monorail components: Platform>Extensions]

### [Deleted User] (2021-02-09)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-02-09)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-02-23)

caseq: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-03-10)

caseq: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-03-11)

[Empty comment from Monorail migration]

### zh...@google.com (2021-03-17)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-15)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-26)

[Empty comment from Monorail migration]

### ad...@google.com (2021-07-08)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-05)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-07)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-16)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-11)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-22)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-15)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-02)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-30)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-25)

[Empty comment from Monorail migration]

### ts...@chromium.org (2022-07-20)

caseq - Any updates? Is this even a bug, or is it working as intended (i.e. tab capture is powerful)

### he...@gmail.com (2022-08-01)

#3, This still works, even after the fix for #1116450.

### [Deleted User] (2022-08-03)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-28)

[Empty comment from Monorail migration]

### he...@gmail.com (2022-10-14)

Hey, friendly ping!

### ad...@google.com (2022-11-23)

Hello dsv@, this hasn't had any attention yet - we're hoping/wondering whether it's simply a duplicate of https://crbug.com/chromium/1116450. Could you take a look and make that determination? If it's not a duplicate hopefully it's closely related and you know what to do here.

### ds...@chromium.org (2022-11-23)

Hi Ade,

This is about tab capture API which we don't own. It is similar to the https://crbug.com/chromium/1116450 but us using chrome.tabCapture.capture instead of Page.captureScreenshot

### ad...@google.com (2022-11-24)

Thanks Danil. mfoltz@, are you a good person to look into this? If not, please assign to the right person if at all possible.

[Monorail components: Internals>Cast]

### mf...@chromium.org (2022-11-27)

Not sure, can someone explain the issue here?


### [Deleted User] (2022-11-30)

[Empty comment from Monorail migration]

### ad...@chromium.org (2022-12-01)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-08)

[Empty comment from Monorail migration]

### mf...@chromium.org (2023-02-14)

As far as I can tell, this is working as intended.

### he...@gmail.com (2023-05-13)

Hey, I missed #33, sorry!

Would be possible for this issue to be reviewed again? I don't think this is/should be the intended behavior, given the permission requested by the extension (Read and change all your data on all websites) doesn't reflect the ability to read local files without enabling the "Allow access to file URLs" option.

### [Deleted User] (2023-05-26)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ta...@chromium.org (2023-05-29)

I think the concern may be valid here. 

IIUC the problem is that an extension that doesn't have the "Allow access to file URLs" permission can read/view the contents of local files through tab capture.

### [Deleted User] (2023-05-29)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-31)

[Empty comment from Monorail migration]

### mf...@chromium.org (2023-06-21)

[Empty comment from Monorail migration]

### he...@gmail.com (2023-06-21)

Hey, was this deemed not to be an issue?

### th...@chromium.org (2023-07-28)

The extension is able to capture and share local files remotely without explicit permission. Until explained otherwise, this should be considered a security bug and should not be closed without details as to why that is not true.

herrerahlb@, could you please upload an unzipped version of the extension?

### th...@chromium.org (2023-07-28)

cc-ing jophba@ as well, who is also listed in chrome/browser/extensions/api/tab_capture/OWNERS.

### th...@chromium.org (2023-07-28)

[Empty comment from Monorail migration]

### th...@chromium.org (2023-07-28)

[Empty comment from Monorail migration]

### he...@gmail.com (2023-07-28)

thefrog@, sure, I have attached the files as requested.

### th...@chromium.org (2023-07-28)

Thank you. I can still reproduce this in M117, so this has not yet been fixed since it was filed. I am therefore leaving the FoundIn intact. The originally set medium severity seems reasonable to me for this bug due to the mitigating factor of needing to install and trigger the extension.

### [Deleted User] (2023-08-16)

[Empty comment from Monorail migration]

### mf...@chromium.org (2023-08-18)

The functionality of the extension API is working as intended.  If security desires changes to the messaging around this extension API to better inform users about what might happen when they install a tab capture extension, that surface is not owned by us.


### ct...@chromium.org (2023-08-18)

To toss out a strawperson solution... Would the media capture team actually be okay with capturing the current full risk of this in the permission string? i.e., "This extension will have full access to read every file on your computer"? That seems strictly worse to me than treating a navigation to a file:/// URL as "breaking" the capture session.



### jd...@chromium.org (2023-08-18)

Hi mfoltz@! Thanks for chiming in.

I appreciate that extension API is working as originally designed, but I assume that you'd agree that our job is to help keep users safe, too. Sometimes that means we need to revisit design decisions or make minor changes to address those risks. We're definitely always motivated to find solutions that don't compromise on the core value of a feature -- no one wants to break stuff.

Is there no world you can envision that would reduce the powers of the extension API explicitly on, e.g., file:// type URLs? That might not be a great idea either, but we'd love your help brainstorming an alternative that might still work for everyone.

### jd...@chromium.org (2023-08-18)

[Empty comment from Monorail migration]

### mf...@chromium.org (2023-08-18)

I appreciate all of the advocacy here for user safety but I honestly don't have an opinion.  The extension API is just a wrapper around the capturer which is doing what it is told, to capture a tab.

If you want to remove the API entirely, that is fine with me; less to maintain.  The stakeholder you need to convince is the extensions team.  They know who depends on this API in the extensions development community, and owns the security surfaces that tell users what extensions they install will do.  Any changes to UI or behavior would need to start with them.



### ct...@chromium.org (2023-08-21)

Devlin could you advise on ownership for Extension APIs? This API is officially owned by mfoltz@ and jophba@ per chrome/browser/extensions/api/tab_capture/OWNERS but requires input from Extensions owners.

### rd...@chromium.org (2023-08-21)

Hey folks!

There's a few different pieces here.  I think one of my main concerns is the precedent this might set, depending on how we treat this bug.

At a high level, I understand (and, _in isolation_, am not necessarily against) the idea of not letting an extension capture a tab with a file:-scheme URL unless the extension has the file access toggle enabled, and I don't have major concerns about that.  However, I don't think that's a tenable stance: what would we do for the desktopCapture API or getDisplayMedia()?  Both of those also allow capturing the screen, and the screen may indeed contain file content, and I don't think there's any realistic way we'd want to either carve out that file content or restrict access based on the toggle (which would effectively require it be enabled anytime the user wanted to share a whole screen).  It's also worth noting that getDisplayMedia() is available directly to websites, which obviously don't have any file access toggle.

Assuming we don't want to dramatically change how getDisplayMedia() and desktopCature work, I don't know why we would necessarily treat tabCapture significantly differently.  Additionally, we have a few other notable safeguards in place:
* In order to call tabCapture.capture(), the extension needs the activeTab permission to be granted -- that is, the user needs to have invoked the extension on the page.
* The tabCapture API already warns the user that the extension can read and change all data
* We recently ( https://chromium-review.googlesource.com/c/chromium/src/+/4772028 ) made a change to disallow extensions from navigating to file URLs unless they have file access.  This means the extension can only use tabCapture.capture to capture file contents (without the file access toggle enabled) if the user directly invokes the extension on the file tab.  If they do that, it seems like reasonable intent.

I think overall, the behavior of the tabCapture API is reasonable, and unless we want to significantly change other APIs, is not against our current security model.

Perhaps the best solution here is to tweak the phrasing of the toggle in the chrome://extensions page that grants file access?  It's possible for the extension to access file content even without that enabled through a few different means (capture APIs, but also if the user e.g. drags-and-drops or otherwise shares files with the extension).  I think that might be a more appropriate fix rather than trying to change the permission warning for the tabCapture API.

cthomp, WDYT?

### ct...@chromium.org (2023-08-21)

Thanks Devlin! The change in crrev.com/c/4772028 sounds like a great mitigation here actually. If the extension can no longer use the Tabs API or similar to navigate the captured tab to a file:/// URL then I think this is likely also addressed. I agree that if a user activates the extension doing the tab capture on the file:/// URL page that is a good signal of user intent and I'm okay saying that is okay to not follow the "allow file access" setting.

I think a key difference between the Tab Capture API and the getDisplayMedia() web API was that a web page can't navigate to or iframe a file:/// URL to do the exfiltration. The linked change brings these into alignment. (getDisplayMedia() also goes through a browser-mediated chooser UI, but agreed that cross-origin exfiltration risks do remain there and are on the minds of the Security team more broadly.)

### ct...@chromium.org (2023-08-23)

Marking this as blocked on https://crbug.com/chromium/1418820 as that should address the underlying root cause.

### ct...@chromium.org (2023-08-23)

[Empty comment from Monorail migration]

### mf...@chromium.org (2023-09-19)

Removing the Cast component as this doesn't have anything to do with Cast.

[Monorail components: -Internals>Cast]

### [Deleted User] (2023-10-11)

[Empty comment from Monorail migration]

### jk...@google.com (2023-10-12)

Unfortunately, I don't think https://crbug.com/chromium/1418820 will fix this bug as we won't be fixing other ways[1] to navigate to file: URLs. However, exploiting this bug will require more permissions such as debugger APIs.

[1] https://bugs.chromium.org/p/chromium/issues/detail?id=1418820#c14

### [Deleted User] (2023-12-06)

[Empty comment from Monorail migration]

### ja...@chromium.org (2023-12-13)

Hi jkokatsu@! Maybe you can provide an update while cthomp is on leave. Has this issue been sufficiently mitigated, or is more work needed?

### jk...@google.com (2023-12-13)

It needs more work. See https://crbug.com/chromium/1175946#c64.

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

This issue was migrated from crbug.com/chromium/1175946?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1468620, crbug.com/chromium/1468622]
[Monorail components added to Component Tags custom field.]

### me...@google.com (2024-10-24)

Secondary security shepherd here, triaging old bugs. There are a multiple mitigating factors to this bug, including Devlin's comments in [comment #59](https://issues.chromium.org/issues/40054742#comment59) and [crrev.com/c/4772028](https://crrev.com/c/4772028).

As such, I'm not sure that it warrants a high severity label anymore and I propose bumping it down to Medium (while still giving credit to the original reporter). Any objections?

(Edit: never mind, S2=Medium already, so perhaps we can now consider it low severity instead?)

### pe...@google.com (2024-10-26)

cthomp: Uh oh! This issue still open and hasn't been updated in the last 429 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### pe...@google.com (2024-11-10)

cthomp: Uh oh! This issue still open and hasn't been updated in the last 444 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ke...@chromium.org (2025-06-11)

cthomp@: Is there a path to move forward on this? I think we need to decide whether the existing list of mitigations is sufficient, or if there is more to be done, and if the latter then put it in someone's queue. Jun points out that an extension with the debugger permission along with tabCapture can still do this (comment 65), though subject to the limitations that Devlin listed.

### ct...@chromium.org (2025-09-12)

The debugger permission is pretty powerful, and it kind of makes sense that it can potentially break some other properties we try to enforce (like "can't navigate to a file:// URL" here), and ultimately is probably fine to just consider working-as-intended. Jun also previously flagged some of these as being out-of-scope in <https://crbug.com/40063229#comment23>. I think at this point we have to accept that the debugger permission inherently opens up certain information leakage due to the powers it gives to an extension. Maybe we should update the Extensions Security FAQ accordingly?

### ke...@chromium.org (2025-09-12)

Assigning to Devlin for the question in comment 96.

### rd...@chromium.org (2025-09-17)

SGTM; I'll take a stab at that.

### dx...@google.com (2025-09-17)

Project: chromium/src  

Branch:  main  

Author:  Devlin Cronin [rdevlin.cronin@chromium.org](mailto:rdevlin.cronin@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6961403>

[Extensions] Update debugger API entry in security FAQ

---


Expand for full commit details
```
     
    Bug: 40054742 
    Change-Id: I6e91b89e2b075eb16e8567b5c76ea8da3364fb30 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6961403 
    Commit-Queue: Devlin Cronin <rdevlin.cronin@chromium.org> 
    Reviewed-by: Chris Thompson <cthomp@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1516943}

```

---

Files:

- M `extensions/docs/security_faq.md`

---

Hash: [2061e6224f53dfff08dc3117c860e6b9e4d658ee](https://chromiumdash.appspot.com/commit/2061e6224f53dfff08dc3117c860e6b9e4d658ee)  

Date: Wed Sep 17 23:43:14 2025


---

### rd...@chromium.org (2025-09-18)

Passing back to cthomp -- if you're comfortable with the state here after the update submitted, feel free to close.

### ct...@chromium.org (2025-09-18)

Thanks Devlin -- I think we have hardened things around this attack vector to the extent that we reasonably can, and the updated FAQ helps call out that the debugger API can sometimes work around restrictions like this. Closing as fixed.

### sp...@google.com (2025-09-26)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
user information disclosure, baseline - lower impact.


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### he...@gmail.com (2025-09-27)

Hey, I just noticed the VRP panel's reward for this report, and I have to admit I was expecting a larger bounty. I know that comparing different reports isn't always straightforward, but based on past, similar issues that had very similar outcomes, I had anticipated a higher award.

I'm particularly confused when comparing this report with [issue 40061772](https://issues.chromium.org/issues/40061772) (awarded $10,000). In both instances, the consequence for the user is identical: an extension can successfully bypass the "Allow access to file URLs" setting and is able to read and exfiltrate arbitrary local file contents. My attack used the tabCapture API, and the other used captureVisibleTab, but the result is the same information disclosure.

Since the impact is equivalent, I'm finding it genuinely difficult to understand this $8,000 discrepancy. I would appreciate if the VRP panel could re-evaluate this bug's reward. If it is deemed to be correct, could you provide more details behind the rationale? Thanks!

### wf...@chromium.org (2025-10-08)

Thank you for your comment. I will put this up for re-evaluation at the next panel meeting, and we will post our decision here.

### wf...@chromium.org (2025-10-20)

Thank you for raising this with us. The panel agrees with your assessment and we have adjusted the reward appropriately.

### sp...@google.com (2025-10-20)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $8000.00 for this report.


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2025-12-26)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> user information disclosure, baseline - lower impact.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40054742)*
