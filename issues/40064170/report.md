# Portals URL spoof after crash

| Field | Value |
|-------|-------|
| **Issue ID** | [40064170](https://issues.chromium.org/issues/40064170) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Portals |
| **Platforms** | Windows |
| **Reporter** | nd...@protonmail.com |
| **Assignee** | ad...@chromium.org |
| **Created** | 2023-04-23 |
| **Bounty** | $2,000.00 |

## Description

**Steps to reproduce the problem:**  

Enable the feature in Chrome Canary using --enable-features=Portals,PortalsCrossOrigin

On any website run the following code and click anywhere.

// onclick is optional  

onclick = () => {

portal = document.createElement('portal');  

// Victim page crashs  

portal.src = '<https://ndev.tk/crashself.html>';  

document.body.appendChild(portal);  

setTimeout(() => {  

// HTTP STATUS 204  

portal.src='<https://terjanq.me/xss.php?status=204>';  

portal.activate();  

}, 6000)

}

**Problem Description:**  

The URL of "<https://ndev.tk/crashself.html>" (any website that crash's) was shown on example.com

**Additional Comments:**

\*\*Chrome version: \*\* 114.0.5728.0 \*\*Channel: \*\* Canary

**OS:** Windows

## Attachments

- [spoof.mp4](attachments/spoof.mp4) (video/mp4, 1.7 MB)

## Timeline

### [Deleted User] (2023-04-23)

[Empty comment from Monorail migration]

### nd...@protonmail.com (2023-04-23)

[Empty comment from Monorail migration]

### za...@google.com (2023-04-24)

Hi adithyas@ this is an issue related to portals, can you please help take a look or reassign? Thanks.

[Monorail components: Blink>Portals]

### [Deleted User] (2023-04-24)

[Empty comment from Monorail migration]

### ad...@chromium.org (2023-04-25)

[Empty comment from Monorail migration]

### ad...@chromium.org (2023-04-25)

Setting to Security-Impact_None because portals are behind a flag and disabled by default.

### mc...@chromium.org (2023-04-25)

The page that crashes in the description does so by exhausting memory, so depending on the machine, the setTimeout might not fire at the right time to reproduce this. A consistent repro would be to run

var portal = document.createElement('portal');
// Victim page crashs
portal.src = 'https://ndev.tk/crashself.html';
document.body.appendChild(portal);
portal.onclick = () => {
    // HTTP STATUS 204
    portal.src='https://terjanq.me/xss.php?status=204';
    portal.activate();
};

and click on the portal after it shows the sad frame.

### mc...@chromium.org (2023-04-25)

The 204 navigation is important here. It clears the portal WebContents' crashed status even though it doesn't commit. This appears to be due to the post-crash early commit optimization [1].

Fixing https://crbug.com/chromium/1133023 I think would be a robust fix for this, but in the meantime, the early commit logic seems undesirable in a portal context and we should probably skip that if we're in a portal.

Aside: Note that enabling SkipEarlyCommitPendingForCrashedFrame prevents this issue.

[1] https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:content/browser/renderer_host/render_frame_host_manager.cc;drc=a61b95c63b0b75c1cfe872d9c8cdf927c226046e;l=1394

### ad...@chromium.org (2023-04-25)

Yes, the 204 navigation is important here. We're going through the EarlyCommitPendingForCrashedFrame codepath which makes us commit a speculative RFH before getting a network response. When we do get the response, we realize its a 204 and don't actually commit a NavigationEntry. So we have a situation where we have a RFH alive (with an empty document) - but the NavigationEntry still points to the previous URL. This problem is prexisting - and if you did the same sequence of URLs on the omnibox, you'd end up with a similar (but less problematic) URL spoof.

Now if you ran the repro in #7 on a website that was previously interactive (had buttons or something) - you'll notice that after clicking on the sad frame portal, the content is no longer interactive. I think what's happening here is that we're using fallback graphics content from the previous page until we get graphics output from the new (activated) page [1]. But the activated page is empty and has no graphics content and so we continue to show the old content. There is logic to timeout showing content from an old page [2] - but it has been refactored recently and doesn't seem to be running anymore. https://chromium-review.googlesource.com/c/chromium/src/+/4451366 made changes that I think would apply to Portals if it were MPArch based. I think for now what we could do is add a `portal_contents_main_frame_view->host()->StartNewContentRenderingTimeout()` call right after we call TakeFallbackContentFrom.

[1] https://source.chromium.org/chromium/chromium/src/+/main:content/browser/portal/portal.cc;l=643;drc=a61b95c63b0b75c1cfe872d9c8cdf927c226046e
[2] https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:content/browser/renderer_host/render_widget_host_impl.h;l=1380;drc=a61b95c63b0b75c1cfe872d9c8cdf927c226046e

### ad...@chromium.org (2023-04-25)

I forgot to say that the fix I proposed in #9 will basically make a white background display after 4 seconds - I'm not sure if that's the best outcome possible here, but seems like a reasonable compromise. Another weird thing is if we don't use https://terjanq.me/xss.php?status=204 and use a blank page (eg: https://wiggly-tundra-constellation.glitch.me/blank.html) instead, it draws a white frame on its own (without needing the timeout) - so there's something about the early committed speculative RFH with no contents that makes it not draw any frames.

### nd...@protonmail.com (2023-04-25)

Yeah the spoof does also affect the omnibox however there should no longer be a ghost image since https://bugs.chromium.org/p/chromium/issues/detail?id=1258363

### ad...@chromium.org (2023-04-25)

[Empty comment from Monorail migration]

### mc...@chromium.org (2023-04-26)

Yeah, we should definitely fix the rendering timeout, but I think it's also the case that we should reject activation in this state.

### ad...@chromium.org (2023-04-26)

#13: Yeah I just reviewed all of our activating checks, and I agree, we should be blocking this.

### gi...@appspot.gserviceaccount.com (2023-04-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/ecee395d0910061f03d7a5e37c5016435f1c016f

commit ecee395d0910061f03d7a5e37c5016435f1c016f
Author: Adithya Srinivasan <adithyas@chromium.org>
Date: Wed Apr 26 22:27:44 2023

Portals: Fix activation restriction for empty documents

We were previously using NavigationEntry::IsInitialEntry to check for
portals that haven't navigated yet, but the linked bug shows a
scenario where we can have an initial empty document after a portal
has navigated.

Bug: 1436050
Change-Id: I52e7e8e25a5aebba0bfc78eb32eb97dcf373ff4a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4472971
Commit-Queue: Adithya Srinivasan <adithyas@chromium.org>
Reviewed-by: Kevin McNee <mcnee@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1136204}

[modify] https://crrev.com/ecee395d0910061f03d7a5e37c5016435f1c016f/content/browser/portal/portal.cc
[modify] https://crrev.com/ecee395d0910061f03d7a5e37c5016435f1c016f/content/browser/portal/portal_browsertest.cc


### ad...@chromium.org (2023-04-27)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-27)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-27)

[Empty comment from Monorail migration]

### am...@google.com (2023-05-12)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-05-12)

Congratulations! The VRP Panel has decided to award you $2,000 for this report. Thank you for your efforts and reporting this issue to us. 

### am...@google.com (2023-05-14)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-03)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-08-03)

This issue was migrated from crbug.com/chromium/1436050?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail blocked-on: crbug.com/chromium/1394147]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40064170)*
