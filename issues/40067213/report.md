# Fullscreen Window is opened behind other windows

| Field | Value |
|-------|-------|
| **Issue ID** | [40067213](https://issues.chromium.org/issues/40067213) |
| **Status** | Assigned |
| **Severity** | Unknown |
| **Priority** | P2 |
| **Component** | Blink>Fullscreen, UI>Browser>FullScreen |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | pu...@gmail.com |
| **Assignee** | ms...@chromium.org |
| **Created** | 2023-07-11 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**

Attacker Can Spoof Full Screen Mode on Other Websites (ex:google.com) & Prevent Full Screen Exit

First User Click On [First Button] and then it will create a new Window.  

and in that window, there is another button called [Open Gmail]

User Click on [Open Gmail] it Shows the Button Does not Work. it will Instruct User to Click on [#2 Button] On the Main Page

Once User Click on [#2 Button] it Will Open Outlook Application & redirect to Google.com

in Background Full Screen Mode Gets Activated Will Show Full Screen Notification on top of the Google.com If User Try to Click [Esc] it Does not Work

In Background the First window Turn to Full Screen Mode Without Knowing User/Victim  

it Leads to Spoofing Attack

**VERSION**  

Chrome Version: 114.0.5735.199 Stable + 117.0.5882.0 canary  

Operating System: [Windows 10 (64-bit)]

**REPRODUCTION CASE**

1. Host Index.html & Wait.html In Your Local Host or Server
2. Open <http://127.0.0.1/>
3. Click On [First Click Here #1]
4. A Window Will Create Now Click On [Open Gmail] = it will Instruct the user if button does not work Click on [ #2 Open Gmail.com ] On Main Page
5. Click on [ #2 Open Gmail.com ]  
   
   6.Done

**CREDIT INFORMATION**  

Reporter credit: Puf

## Attachments

- [Puf POC Video.mp4](attachments/Puf POC Video.mp4) (video/mp4, 620.1 KB)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- [New POC Video.mp4](attachments/New POC Video.mp4) (video/mp4, 171.4 KB)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)

## Timeline

### [Deleted User] (2023-07-11)

[Empty comment from Monorail migration]

### pu...@gmail.com (2023-07-11)

[Empty comment from Monorail migration]

### da...@chromium.org (2023-07-11)

Thanks, if I understand correctly this report is that the popup window button gets a user gesture to open a fullscreen window, but it waits to use it for 4 seconds, which means the user may be doing other things when the fullscreen window happens, and the OS places the fullscreen window behind them?

Is that a fair summary?

### da...@chromium.org (2023-07-11)

[Empty comment from Monorail migration]

[Monorail components: UI>Browser>FullScreen]

### pu...@gmail.com (2023-07-11)

Attacker Tried to Destruct User & Chrome By Using Outlook Application & Redirect to google.com 

If User is Working In tabs the Full Screen Mode Automatically shows to user in Full Screen Mode & notify him Clearly


### [Deleted User] (2023-07-11)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pu...@gmail.com (2023-07-11)

fullscreen window behind them? Answer : Yes

### da...@chromium.org (2023-07-11)

Ok so I would break this down to:
- The fullscreen window is opened behind another Chrome window
- The ESC to leave fullscreen prompt is shown when the fullscreen window is not visible

Thoughts from the UX team?

### [Deleted User] (2023-07-11)

[Empty comment from Monorail migration]

### pu...@gmail.com (2023-07-11)

Another Bug Regarding this Issue

Minimize Window Hide Fullscreen Notification
Using Minimize [-] Too We Can Hide Full Screen Notification 

Bypass Fullscreen Notification Successful here

0. Host all the files in your localhost and open index.html 
1. Click On [ First Click Here Button ]
2. Next Click On [ Download Login Page ]
3. Now minimize the window 
4. Now Open the window again
5. it does not show Fullscreen Notification here 


### da...@chromium.org (2023-07-11)

Thanks, so three things:
- The fullscreen window is opened behind another Chrome window
- The ESC to leave fullscreen prompt is shown when the fullscreen window is not visible (corolary of the first)
- The ESC to leave fullscreen prompt is not shown if the opener window is minimized. Noting that this requires user interaction to minimize the window.

### pu...@gmail.com (2023-07-11)

I think for this Issue Severity should Upgrade. 

### pu...@gmail.com (2023-07-11)

minimize Window Can Hide " FullScreen Notification " I believe Severity Should Be Upgrade 





### [Deleted User] (2023-07-16)

[Empty comment from Monorail migration]

### pu...@gmail.com (2023-07-18)

Any Update on Severity Status 

### pu...@gmail.com (2023-08-01)

Any Update on Severity, Thanks


### ct...@chromium.org (2023-10-16)

Triaging fullscreen reports. msw@ could you take a look at this one? This seems similar to https://crbug.com/chromium/1492397 which I also sent your way.

Bumping this to Severity-Medium to be conservative. This does hide the fullscreen notice, but does require some user interaction and is a little noisy, but effective.

[Monorail components: Blink>Fullscreen]

### [Deleted User] (2023-10-16)

[Empty comment from Monorail migration]

### mf...@chromium.org (2023-10-17)

cthomp@: Was multi-screen window placement part of this report?  I didn't see a mention of the window management permission being involved.

### ct...@chromium.org (2023-10-17)

My understanding is this is just triggering an edge case to obscure the fullscreen notice (I think it’s letting it expire in the background before the user switches back to the fullscreen window).

### mf...@chromium.org (2023-10-17)

OK, routing over to takumif@ then.

### [Deleted User] (2023-10-17)

takumif: Uh oh! This issue still open and hasn't been updated in the last 98 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ms...@chromium.org (2023-10-17)

Looks related to https://crbug.com/chromium/1346455, minimized windows entering fullscreen seem extra broken on Linux M117.
  document.body.onclick = () => { setTimeout(()=>{document.body.requestFullscreen()},1500) } 
Perhaps requests on hidden windows should fail, maybe near document 'fully active' checks:
  https://html.spec.whatwg.org/multipage/document-sequences.html#fully-active
  https://crsrc.org/c/third_party/blink/renderer/core/fullscreen/fullscreen.cc;drc=977dc02c431b4979e34c7792bc3d646f649dacb4;l=714

### am...@chromium.org (2023-10-24)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-01)

takumif: Uh oh! This issue still open and hasn't been updated in the last 113 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pu...@gmail.com (2023-12-05)

any updates on this issue? Thank you

### pu...@gmail.com (2024-01-12)

Any Updates on this issue?

### is...@google.com (2024-01-12)

This issue was migrated from crbug.com/chromium/1463943?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>Fullscreen, UI>Browser>FullScreen]
[Monorail components added to Component Tags custom field.]

### pu...@gmail.com (2024-03-21)

Would you kindly give me an update?

### pu...@gmail.com (2024-04-15)

Would you kindly give me an update?

What’s the current status of this Issue.

Thank you!

### am...@chromium.org (2024-04-25)

This issue is being worked as part of holistic fullscreen changes.
Unfortunately there is no update on the resolution at this time, but it is being worked by the fullscreen time in addition with other issues.

### pu...@gmail.com (2024-08-13)

Verified Testing! Looks like this vulnerability is fixed! in latest Chrome Version 128.0.6613.27 beta

Please Verify and Change Status to fixed

Thank you!

### pu...@gmail.com (2024-08-13)

Verified Testing! this vulnerability is fixed! in
latest Stable Chrome Version 127.0.6533.100

### am...@chromium.org (2024-08-19)

hi msw@ -- can you please verify; this look like it could have been potentially resolved by your recent work related to [crbug.com/40941384](https://crbug.com/40941384) || <https://crrev.com/c/5666304> (I don't have access to the other bug this CL links to in order to further verify)

### ms...@chromium.org (2024-08-30)

As best I can tell this was inadvertently fixed (at least on Windows) by https://crrev.com/c/5560391 which triggered a behavior change to activate windows when entering fullscreen:
https://source.chromium.org/chromium/chromium/src/+/main:content/browser/web_contents/web_contents_impl.cc;drc=ee503055e3977e0f916da3a374eb0944b83f92da;l=4074
ToT can also repro the defect if you explicitly disable the feature: $ out/Default/chrome --disable-features=AutomaticFullscreenContentSetting

$ python3 C:\src\chromium\src\tools\bisect-builds.py -a win -g 1315988 -b 1233107 -- http://localhost:8000/NewIndex.html
https://chromium.googlesource.com/chromium/src/+log/adeac205b1e848b0d5d82c84d9e5df5c82013970..024aa8b4a1cbb5cda0d20d02d1fbc3d0b681acec

My repro attempts on Linux show slightly different breakages reminiscent of other Linux CRD graphical defects (non-updated regions), which seem tangential to this issue.

### sp...@google.com (2024-09-11)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
report of lower impact exploitation mitigation bypass 


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-09-11)

Congratulations Puf! Thank you for your efforts and reporting this issue to us.

### pu...@gmail.com (2024-10-15)

Any update Regarding CVE for this Vulnerability
Thank you

### pe...@google.com (2024-12-07)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### am...@chromium.org (2024-12-09)

The fix for this issue was landed without context of this issue. In looking through other reports of this issue, it appears this is not the first report of this issue. We'll need to merge this report into the previous version of this report and consider that issue for a reward.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40067213)*
