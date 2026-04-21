# Security: Download & Execute File Silently Without Knowing User in Chrome

| Field | Value |
|-------|-------|
| **Issue ID** | [41496084](https://issues.chromium.org/issues/41496084) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>DataTransfer, Blink>Fullscreen, UI>Browser>Downloads, UI>Browser>FullScreen |
| **Platforms** | Windows |
| **Reporter** | pu...@gmail.com |
| **Assignee** | dc...@chromium.org |
| **Created** | 2024-01-30 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**

Using Drag Event Object & event.dataTransfer & Fullscreen

We Can Lunch a Malicious File Directly from User Pc Without Knowing User Using this Techniques in Chrome

Giving Instruction to User to drag and drop div or Image to Desktop or Folder then the File Downloads Immediately & Go to Fullscreen Mode Quickly Hides the Download Notification in Fullscreen Then Giving instruction to Hold on [Enter] Key. the Mouse Focus is Still on the Malicious File

Once the User Hold the [Enter] Key the Malicious File Executes Without Knowing User

Note: The Malicious File Has to Been in Small Size in [KB] for Fast Download

**VERSION**  

Chrome Version: [122.0.6261.6] + [beta]  

[121.0.6167.86] + [Stable]

Operating System: [Windows 10]

**REPRODUCTION CASE**

1. host the PufIndex.html
2. with `python3 -m HTTP.Server`
3. Then drag and drop the div to the desktop.
4. now Hold [Enter] Key
5. Execute File Successful.

## Attachments

- [Chrome POC.mp4](attachments/Chrome POC.mp4) (video/mp4, 426.0 KB)
- deleted (application/octet-stream, 0 B)
- [fixed.mp4](attachments/fixed.mp4) (video/mp4, 547.9 KB)
- deleted (application/octet-stream, 0 B)
- [file Focus fails.mp4](attachments/file Focus fails.mp4) (video/mp4, 121.4 KB)

## Timeline

### [Deleted User] (2024-01-30)

[Empty comment from Monorail migration]

### me...@chromium.org (2024-01-31)

Thanks for the report, this is interesting. https://crbug.com/chromium/1363495 is also similar, but doesn't have the fullscreen aspect.

Some observations:

1. When the page goes fullscreen, it should keep getting the keyboard events. Here, the drop target (Windows Explorer) gets them, so the enter key attempts to open the file. (This doesn't seem to be the case on macOS, pressing enter doesn't do anything.). I couldn't find an existing bug for this.

There seems to be differences between opening the PoC over a file:// URL vs a http://localhost URL:

2. When using a file:// URL, the bat file didn't get executed immediately due to the "publisher not verified" Windows dialog. The default button on this dialog is "Cancel" so pressing enter doesn't execute the bat. When using localhost, it seems to execute immediately without the warning. 

3. When I open the PoC as a file:// URL, the downloaded bat file has its mark-of-the-web attribute set. This is not the case when I load the PoC over an http://localhost URL. This sounds like a bug too.

Also, not sure if the downloaded bat file is passed to SafeBrowsing, but it probably wouldn't help in this case anyways.

I think we'll want to split this bug into sub issues, but I'd like to get some confirmation from area owners before doing so. Each of these could be low-severity, but imo the combined bug is dangerous enough to deserve medium-severity.

dcheng: Can you please take a look since you are the owner of https://crbug.com/chromium/1363495? Thanks.

[Monorail components: Blink>DataTransfer UI>Browser>Downloads]

### [Deleted User] (2024-01-31)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-31)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2024-01-31)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-31)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-31)

This issue was migrated from crbug.com/chromium/1523130?no_tracker_redirect=1

[Multiple monorail components: Blink>DataTransfer, UI>Browser>Downloads]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-02-13)

dcheng: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### dc...@chromium.org (2024-02-27)

I think we should probably just disallow entering fullscreen when a drag and drop is in progress. I don't really see a legitimate reason to do this, and it leads to confused focus so...

### pe...@google.com (2024-03-13)

dcheng: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### pu...@gmail.com (2024-03-14)

I'm Agree With you.

bat file didn't get executed immediately due to the "publisher not verified" Windows dialog. The default button on this dialog is "Cancel" so pressing enter doesn't execute the bat.

We Can Use Other Type of File to Execute Silently on Pressing "Enter" Key to Bypass "publisher not verified" Windows dialog. in Windows

Ex : chm , crt , cer , exe , hlp , diagcab Many other files Does not show publisher not verified" Windows dialog.

### pu...@gmail.com (2024-05-30)

Would you kindly give me an update?

What’s the current status of this Issue.

Thank you!

### pu...@gmail.com (2024-06-28)

Would you kindly give me an update?

What’s the current status of this Issue.

Thank you!

### pu...@gmail.com (2024-07-24)

Hello, any updates here?

### ke...@chromium.org (2024-09-25)

dcheng@: Are you planning to work on this, or should we find a different owner?

### pu...@gmail.com (2024-10-16)

Hello, any updates here?

### pu...@gmail.com (2024-11-04)

I'm not an expert but I Would like to give a fixing suggestion regarding this Bug

1. I think we can fix in another way how if we bring back focus back to chrome?
2. Exit fullscreen when a drag and drop is in progress

### pu...@gmail.com (2024-11-19)

Friendly ping

### ms...@chromium.org (2024-11-20)

Issue 40076195 and Issue 40067213 seem slightly relevant, they were fixed by activating windows when entering fullscreen:
https://source.chromium.org/chromium/chromium/src/+/main:content/browser/web_contents/web_contents_impl.cc;drc=ee503055e3977e0f916da3a374eb0944b83f92da;l=4074-4083

FWIW, it sounds like entering fullscreen on drag end should leave the fullscreen window active. Window manager fullscreen changes are asynchronous, so calling Activate toward the end, e.g. in Browser::WindowFullscreenStateChanged() or BrowserView::FullscreenStateChanged() (in addition to / instead of) during the fullscreen trigger could maybe help ( hopefully without breaking other features like https://chromestatus.com/feature/5173162437246976 ).

### dc...@chromium.org (2024-11-21)

We can't really exit fullscreen, because there isn't a drag and drop in progress; the example page is doing it from the dragend handler.

Even if there was a drag and drop in progress, it's trivial to bypass that by a simple `setTimeout(stage2, 0)`.

I did try activating the WebContents unconditionally in `RenderFrameHostImpl::EnterFullscreen()` but it doesn't work. This might be because of Windows trying to prevent focus stealing, or because some plumbing somewhere isn't working... I'm really not sure.

... we could block the renderer from entering fullscreen if the window isn't focused/active... but I'm not sure what side effects that would have...

### ms...@chromium.org (2024-11-21)

Hmm, not sure why Activate would be blocked (ideally in Browser::WindowFullscreenStateChanged() or BrowserView::FullscreenStateChanged()).

Otherwise, consuming transient activation on dragstart, or blocking fullscreen from inactive windows (without Automatic Fullscreen (or Window Management?)) permission might be reasonable.

+Steve, do you know anyone at Microsoft who might have some thoughts on this issue?

### pu...@gmail.com (2024-12-12)

Friendly ping

### pu...@gmail.com (2025-01-23)

Whenever you have a moment, could you please send a quick update?

Thank you

### aj...@google.com (2025-01-27)

This is similar to [issue 392375329](https://issues.chromium.org/issues/392375329) - the fix might be to change how the download notification gets focus rather than to change something to do with fullscreen.

### pu...@gmail.com (2025-06-11)

Hello, just a gentle reminder to keep this Issue on track! Thank you

### pu...@gmail.com (2025-08-26)

I've successfully verified the fix on my Windows 11 and confirmed that the issue is resolved.

I have attached Latest verified video

Thanks,

### pu...@gmail.com (2025-08-26)

[dc..@chromium.org](mailto:dc..@chromium.org)

After a file is dropped, it does not get focus on Windows. This prevents the enter key from executing the file, which aborts the attempt to open a potentially malicious file, such as a .vbs .bat file. and many more

### aj...@chromium.org (2025-09-30)

Marking Fixed based on comment 28.

### aj...@google.com (2025-10-08)

adjusting severity as there are preconditions.

### sp...@google.com (2025-10-14)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
Highly mitigated security UI spoofing


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-01-07)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> Highly mitigated security UI spoofing

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/41496084)*
