# Text Selection menu able to overlap URL bar  

| Field | Value |
|-------|-------|
| **Issue ID** | [329476341](https://issues.chromium.org/issues/329476341) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser, UI>Browser>Mobile>ContextMenu, UI>Browser>Selection |
| **Platforms** | Android |
| **Chrome Version** | 124.0.0.0 |
| **Reporter** | ch...@gmail.com |
| **Assignee** | ji...@google.com |
| **Created** | 2024-03-14 |
| **Bounty** | $2,000.00 |

## Description

# Steps to reproduce the problem

1. Open the testcase.html or navigate to <https://lbstyle.github.io/repro.html>
2. tap anywhere

# Problem Description

When the user taps somewhere on the page, the text selection menu can appear over the URL bar, in this case, the user can be manipulated.

# Summary

Text Selection menu able to overlap URL bar

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A

## Attachments

- [repro.html](attachments/repro.html) (text/html, 666 B)
- [spoof.png](attachments/spoof.png) (image/png, 72.1 KB)
- [screen.mp4](attachments/screen.mp4) (video/mp4, 222.7 KB)
- [6423.png](attachments/6423.png) (image/png, 411.4 KB)
- [20250106_130420275.jpg](attachments/20250106_130420275.jpg) (image/jpeg, 651.2 KB)

## Timeline

### ja...@chromium.org (2024-03-14)

I was able to cause the copy/share UI to appear over the omnibox on Android M122. Setting that as the FoundIn. Also setting severity as Medium for now.

### ja...@chromium.org (2024-03-14)

I don't think this would work as convincingly on Windows because there's more screen space to see that the omnibox is covered, so removing that OS.

### ja...@chromium.org (2024-03-14)

Adding people from the owners file at chrome/android/java/src/org/chromium/chrome/browser/share/OWNERS

Hi dtrainor and wenyufu, I'm trying to find the right owner for the copy/share UI on Android. Can you help redirect this issue?

### we...@chromium.org (2024-03-14)

I've seen a lot of updates in <https://source.chromium.org/chromium/chromium/src/+/main:content/public/android/java/src/org/chromium/content/browser/selection/SelectActionMenuHelper.java;bpv=1;bpt=0> recently, wbjacksonjr@ can you help take a look / triage?

### ja...@chromium.org (2024-03-14)

Thanks for reassigning it wenyufu@. I'm adding a few others from those CLs.

### ja...@chromium.org (2024-03-15)

Assigning this issue Medium severity for now, because it allows web content to tamper with the browser's trusted UI

<https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#toc-medium-severity>

### pe...@google.com (2024-03-15)

Setting milestone because of s2 severity.

### pe...@google.com (2024-03-15)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ch...@gmail.com (2024-03-27)

Any update on this bug?

Thanks.

### pe...@google.com (2024-03-30)

wbjacksonjr: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@gmail.com (2024-04-10)

wbjacksonjr, friendly ping :-)

### wb...@chromium.org (2024-04-10)

I'll pull into our teams queue to investigate. Any idea on the timelines on when this should be handled?

### pe...@google.com (2024-04-25)

wbjacksonjr: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@gmail.com (2024-05-23)

Any update on this bug? thanks.

### ch...@gmail.com (2024-07-11)

Friendly ping :)

### ts...@google.com (2024-10-31)

Idries, is there perhaps someone on your team that might have cycles to chase down this very old bug?  Thanks!

### wb...@google.com (2024-11-01)

Assigning to [yaris@google.com](mailto:yaris@google.com) to take a look at.

### ya...@google.com (2024-11-04)

I see that we add a Y offset to the selection menu [here](https://source.chromium.org/chromium/chromium/src/+/main:content/public/android/java/src/org/chromium/content/browser/selection/SelectionPopupControllerImpl.java;drc=d176526630b2049486a8be93fd89482d0aba6cfc;bpv=1;bpt=1;l=1341?gsn=getSelectionRectRelativeToContainingView&gs=KYTHE%3A%2F%2Fkythe%3A%2F%2Fchromium.googlesource.com%2Fcodesearch%2Fchromium%2Fsrc%2F%2Fmain%3Flang%3Djava%3Fpath%3Dorg.chromium.content.browser.selection.SelectionPopupControllerImpl%23e8190679d897f32315ff757cd12bff1e59c3a31b03ff5ea86c0a838dfa3b42cf) to account for the area occupied by the browser controls but that doesn't always work. For example, I was looking into this and found that the selection menu can also cover the URL bar when you select text on the top edges of the page just below the URL bar (see attached pic). In that case, what do we want to do? Never allow the selection menu to go into the browser controls area?

We can probably add some edge case fixes here, but I wonder if this is something that needs fixing on the blink side since we get the selection rect values from native.

### ch...@gmail.com (2024-11-27)

Hi Zak! any update here? Thanks 

### ya...@google.com (2024-12-03)

Hi Khalil, I pushed a bandaid fix the other day. But after offline chat, we decided it's best to look into the root cause. I will take a look this week, and there should be an update by EOW.

### ya...@google.com (2024-12-04)

So, two things:

- Is this a regression? If it's, do you know what the earliest branch is that is broken so we can look into fixing it.
- If this is not a regression and it's a new bug, the appropriate team to take over would be the chrome android team. They're the ones who can decide what behaviour should be put in place, since Webview doesn't have the concept of a "URL bar".

### ch...@gmail.com (2024-12-05)

I think Zak made a mistake by assigning me to fix the bug.

### wb...@google.com (2024-12-05)

Assigning to Jinsuk who works on Chrome Android UI to take a look.

### tw...@google.com (2024-12-09)

> Never allow the selection menu to go into the browser controls area?

I think this is the right fix for content selected within the webpage.

We might be able to adjust here if we only want the impact of browser controls presence to apply to Chrome: <https://source.chromium.org/chromium/chromium/src/+/main:chrome/android/java/src/org/chromium/chrome/browser/ChromeActionModeHandler.java;l=289;drc=616d60fca655937c2b730db94fd32d37ddff3bb5;bpv=1;bpt=1>

### ch...@gmail.com (2024-12-19)

Any update on this bug? thanks :)

### ji...@google.com (2025-01-06)

Took a look at the issue. Content layer [SelectionControllerImpl#getSelectionRectRelativeToContainingView](https://source.chromium.org/chromium/chromium/src/+/main:content/public/android/java/src/org/chromium/content/browser/selection/SelectionPopupControllerImpl.java;drc=d176526630b2049486a8be93fd89482d0aba6cfc;bpv=1;bpt=1;l=1341?gsn=getSelectionRectRelativeToContainingView&gs=KYTHE%3A%2F%2Fkythe%3A%2F%2Fchromium.googlesource.com%2Fcodesearch%2Fchromium%2Fsrc%2F%2Fmain%3Flang%3Djava%3Fpath%3Dorg.chromium.content.browser.selection.SelectionPopupControllerImpl%23e8190679d897f32315ff757cd12bff1e59c3a31b03ff5ea86c0a838dfa3b42cf) ensures the action mode is always positioned right above or below (thus not obscuring, and not too distanced from) the selected text, but it doesn't care about the action mode overlapping top controls or not. It needs extra logic that helps Android framework make the right decision for the action bar vertical position.

In the attached drawing, (a) is the situation we should avoid vs. (b) is an acceptable case where we have enough space between top controls and the selected text for Android to place the action bar there. We can see that, if `selectedRect.top < controlHeight(ch) + actionBarHeight(ah)`, then the action bar should not be placed above the seleted text. This can be done by telling Android that the selected text is taller than it actually is i.e. setting the text.top to text.top-ah (drawing c). This makes the Android framework believe it doesn't have enough space above the text, so the action bar is placed below.

The problem is that action mode is a widget rendered by Android framework, and we don't know its height(ah). If it is, say, as tall as top controls i.e. `ah == ch` and assumes it is a reasonable approximation (both are horizontal bar UI containing a single line [Edit]Text view), we can have the desired behavior
[clip](https://drive.google.com/file/d/1YOT1RvmyU86HEmd5k0G9ISR0rZzvTk2y/view?usp=drive_link).

### tw...@google.com (2025-01-06)

Thanks for the investigation notes!

> The problem is that action mode is a widget rendered by Android framework, and we don't know its height(ah). If it is, say, as tall as top controls i.e. ah == ch and assumes it is a reasonable approximation (both are horizontal bar UI containing a single line [Edit]Text view), we can have the desired behavior clip.

While we'd be able to provide a better UX if we knew the floating action mode height, I think using an approximation is "good enough" and would improve / resolve the security vulnerability. 

### ya...@google.com (2025-01-07)

deleted

### ap...@google.com (2025-01-07)

Project: chromium/src  

Branch: main  

Author: Jinsuk Kim <[jinsukkim@chromium.org](mailto:jinsukkim@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6148920>

[Android] Fix floating action bar/top control overlapping bug

---


Expand for full commit details
```
[Android] Fix floating action bar/top control overlapping bug 
 
In order to avoid the floating bar and the top control overlapping 
with each other, this CL ensures that the action bar will be drawn 
above the selected text only if there is enough space. 
 
Bug: 329476341 
Change-Id: I7095863a845db2aa38a4d9d93efde2f2075e82a3 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6148920 
Code-Coverage: findit-for-me@appspot.gserviceaccount.com <findit-for-me@appspot.gserviceaccount.com> 
Reviewed-by: Theresa Sullivan <twellington@chromium.org> 
Commit-Queue: Jinsuk Kim <jinsukkim@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1403053}

```

---

Files:

- M `chrome/android/java/src/org/chromium/chrome/browser/ChromeActionModeHandler.java`
- M `chrome/android/java/src/org/chromium/chrome/browser/ui/RootUiCoordinator.java`
- M `chrome/android/junit/src/org/chromium/chrome/browser/ChromeActionModeHandlerUnitTest.java`

---

Hash: 9e3dedd19349d812d7dba808f07ebee91302623e  

Date:  Tue Jan 07 09:44:22 2025


---

### ch...@gmail.com (2025-01-08)

Thanks for the fix! I'll check it out on Canary tomorrow.

### ch...@gmail.com (2025-01-09)

Is this fixed?

### pe...@google.com (2025-01-09)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### ji...@google.com (2025-01-09)

Yes just marked it fixed. I see a new, different problem that I'm thinking of looking into in a separate bug, but the issue for this bug itself was fixed.

### pe...@google.com (2025-01-09)

Dear owner, thanks for fixing this bug. We've reopened it because:

- Some CLs listed in the “Fixed By Code Changes” field are invalid and have been removed. Please provide an appropriate Gerrit url that matches the pattern: `https://<host>-review.googlesource.com/c/<repo>/+/<change_number>` or use the value 'NA' and re-mark this bug as fixed. If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### sp...@google.com (2025-01-17)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
report of lower impact security UI issue 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### ch...@gmail.com (2025-01-19)

Thanks! 

### ch...@google.com (2025-04-18)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ji...@google.com (2025-04-28)

Do not file a new bug reporting that this is still reproducible. Someone else already filed one.

### ba...@opera.com (2025-09-03)

Regarding comment #39, do you have a reference to the other issue?

The test case at https://lbstyle.github.io/repro.html is still reproducible in Chrome and in most other Chromium based web browsers. As a developer of a chromium based browser affected by the same problem it would be very beneficial for us to know what you are doing to fix the issue so that we can ensure that we apply the same fix in our browser as well.

## Bounty Award

> report of lower impact security UI issue

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/329476341)*
