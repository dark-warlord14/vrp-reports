# Security: Spoof empty titlebar via javascript: URI in Document PIP

| Field | Value |
|-------|-------|
| **Issue ID** | [40065384](https://issues.chromium.org/issues/40065384) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>Media>PictureInPicture |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ha...@gmail.com |
| **Assignee** | li...@google.com |
| **Created** | 2023-06-05 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

Its possible to spoof empty origin using javascript: URI in Document PIP

**VERSION**  

Chrome Version: 114.0.5735.91 (Official Build) (64-bit) (cohort: Stable Installs & Version Pins)  

Operating System: Windows 10 Version 22H2 (Build 19045.2965)

**REPRODUCTION CASE**  

According to <https://wicg.github.io/document-picture-in-picture/#origin-visibility>:

"It is required that the user agent makes it clear to the user which origin is controlling the DocumentPictureInPicture window at all times to ensure that the user is aware of where the content is coming from. For example, the user agent may display the origin of the website in a titlebar on the window."

However, it is possible to use an empty origin and thus an empty titlebar by launching a document PIP from javascript: URI (see attached video)

0: Enable chrome://flags/#document-picture-in-picture-api  

1: Open attached HTML file.  

2: Click on the button.  

3: You will land on about:blank URL (but this is actually a javascript: URL), follow instructions and double click.  

4: Document PIP is launched with empty title bar causing the box to overlay on Paypal page which can cause user confusion.

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Axel Chong

## Attachments

- [Untitled_ Jun 6, 2023 3_09 AM.webm](attachments/Untitled_ Jun 6, 2023 3_09 AM.webm) (video/webm, 811.7 KB)
- [pip-exploit.html](attachments/pip-exploit.html) (text/plain, 1.0 KB)
- [pip-exploit.html](attachments/pip-exploit.html) (text/plain, 411 B)
- [Untitled_ Jul 3, 2023 10_57 PM.webm](attachments/Untitled_ Jul 3, 2023 10_57 PM.webm) (video/webm, 613.3 KB)
- [Untitled_ Jul 30, 2023 3_06 PM.webm](attachments/Untitled_ Jul 30, 2023 3_06 PM.webm) (video/webm, 801.1 KB)
- [Screenshot 2023-08-03 (1).png](attachments/Screenshot 2023-08-03 (1).png) (image/png, 24.2 KB)
- [Screenshot 2023-08-03 (2).png](attachments/Screenshot 2023-08-03 (2).png) (image/png, 12.6 KB)
- [Screenshot 2023-08-03 (3).png](attachments/Screenshot 2023-08-03 (3).png) (image/png, 15.8 KB)
- [Screenshot 2023-08-03 (4).png](attachments/Screenshot 2023-08-03 (4).png) (image/png, 18.2 KB)
- [doc-pip-spoofed-omnibar.html](attachments/doc-pip-spoofed-omnibar.html) (text/plain, 919 B)
- [spoofed-omnibar.webm](attachments/spoofed-omnibar.webm) (video/webm, 548.8 KB)

## Timeline

### [Deleted User] (2023-06-05)

[Empty comment from Monorail migration]

### ca...@chromium.org (2023-06-05)

[Empty comment from Monorail migration]

### ha...@gmail.com (2023-06-05)

Oops, I had a 504 error on monorail whilst submitting 1451542 so I decided to submit again. Didn't know it created one instance of the issue in 1451542 even with 504 error.

### ca...@chromium.org (2023-06-06)

steimel: Passing this to you for further triage as an owner of the flag, feel free to reassign as appropriate.

Is PIP shipping in any platforms/milestones at this point? That would help us set either the FoundIn, or SecurityImpact_None labels

[Monorail components: Blink>Media>PictureInPicture]

### st...@chromium.org (2023-06-06)

It is in an origin trial now

### st...@chromium.org (2023-06-06)

[Empty comment from Monorail migration]

### li...@google.com (2023-06-06)

that's neat!

i'm surprised it works, since we should only open pip with secure origins.  i guess that counts as secure.  if so, then we should probably update the origin check to enforce that there's a real origin there.

### li...@google.com (2023-06-06)

[Empty comment from Monorail migration]

### ca...@chromium.org (2023-06-06)

Which milestone did the origin trial launch in? Just so I can set the foundin label accordingly.

### [Deleted User] (2023-06-06)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### li...@google.com (2023-06-06)

re c#9: the origin trial started in M111.

### ca...@chromium.org (2023-06-06)

Thanks, added the tag now

### [Deleted User] (2023-06-06)

[Empty comment from Monorail migration]

### li...@google.com (2023-06-06)

oh, sorry -- i'd have just done that if i had read c#9 more carefully :)

### ha...@gmail.com (2023-07-10)

liberato@ and steimel@, I am providing an additional test case here as I saw your fix in https://chromium-review.googlesource.com/c/chromium/src/+/4595397 which would probably fix this issue as well. I did open a new issue in https://bugs.chromium.org/p/chromium/issues/detail?id=1460025, however, but which got mistakenly marked as duplicate of an unrelated issue. But since you have a fix at  https://chromium-review.googlesource.com/c/chromium/src/+/4595397 which would fix this problem, I decided that instead of opening another issue I'll just post the test case here.

VULNERABILITY DETAILS
It is also possible to spoof document PIP address by using a long about:blank URL containing URL fragment. 

VERSION
Chrome Version: 117.0.5868.0 (Official Build) canary (64-bit) (cohort: Clang-64) [after the patch to show only origins in the titlebar/omnibox]
Operating System: Windows 10 Version 22H2 (Build 19045.3086)

REPRODUCTION CASE
1. Go to pip-exploit.html. 
2. Click on make payment.
3. Document PIP window spawned with the fake subdomain of paypal.com but the actual URL is "about:blank#very-super-duper-long-subdomain.paypal.com" 

Tested on both stable and latest canary.


### ha...@gmail.com (2023-07-30)

liberato@ and steimel@, I have a simpler solution to this problem and https://bugs.chromium.org/p/chromium/issues/detail?id=1460025. 

This patch works by:

1) First, obtaining an RFH from the active web contents by calling GetPrimaryMainFrame()

2) Obtain the previous non-null origin by calling GetLastCommittedOrigin() on the newly obtained RFH, See https://source.chromium.org/chromium/chromium/src/+/main:docs/security/origin-vs-url.md?q=GetLastCommittedOrigin() for more info.

3) Convert the origin to a URL.

With the patch applied now shows the previous origin when a null origin is encountered.

I verified locally and it works correctly - see the video :)

This way we do not need double checks in the renderer and browser and document PiP can still work in about:blank.

### ha...@gmail.com (2023-07-30)

Patch (cced you as well): https://chromium-review.googlesource.com/c/chromium/src/+/4705373

### ha...@gmail.com (2023-07-30)

Also, since document PiP don't work in iframes it is safe to use GetPrimaryMainFrame() to refer to the owner of the document PiP

### ha...@gmail.com (2023-08-03)

Attaching screenshots of edge cases with the fix applied:
(1) opening pip from directly opened about:blank
Result: fails as a about:blank share the same security context as its opener. Since it has no opener the security context is insecure and document PiP only opens in secure context.

(2) opening pip from about:blank from a file:// URL
Result: display a File on the top left hand corner and nothing else.

(3) opening pip from about:blank from an extension.
Result: displays the extension URL correctly as extensions do have an origin.

(4) opening pip from about:blank with about:blank's opener navigated
Result: same result as the opener cannot change.

### gi...@appspot.gserviceaccount.com (2023-08-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/92dd7495086c0b91c1a9db170e812d51dfec825c

commit 92dd7495086c0b91c1a9db170e812d51dfec825c
Author: Frank Liberato <liberato@chromium.org>
Date: Thu Aug 03 06:13:38 2023

Disallow document pip for non-https / file resources.

Only https / file resources should be able to open document pip
windows.  Anything else, like javascript or about://blank, is
hard to describe.

This CL implements the renderer-side checks to fail fast.  A follow-
up CL will add browser-side checks.

Bug: 1451543
Change-Id: I2a66768d8116b16adbf19ab1c76acbce6034963a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4595397
Reviewed-by: Tommy Steimel <steimel@chromium.org>
Commit-Queue: Frank Liberato <liberato@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1178832}

[modify] https://crrev.com/92dd7495086c0b91c1a9db170e812d51dfec825c/third_party/blink/renderer/modules/document_picture_in_picture/picture_in_picture_controller_test.cc
[modify] https://crrev.com/92dd7495086c0b91c1a9db170e812d51dfec825c/third_party/blink/renderer/modules/document_picture_in_picture/picture_in_picture_controller_impl.cc


### ha...@gmail.com (2023-08-03)

I took the time to code up the browser-side check for https://crbug.com/chromium/1451543#c20 here https://chromium-review.googlesource.com/c/chromium/src/+/4746980

### ha...@gmail.com (2023-08-08)

[Comment Deleted]

### ha...@gmail.com (2023-08-08)

Removed https://crbug.com/chromium/1451543#c17 to https://crbug.com/chromium/1451543#c19 as no longer relevant*

### gi...@appspot.gserviceaccount.com (2023-08-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/444b0a82fb9f59dd2c3c05dfbccc56fc16c124d2

commit 444b0a82fb9f59dd2c3c05dfbccc56fc16c124d2
Author: Haxatron Sec <haxatron1@gmail.com>
Date: Fri Aug 11 21:03:01 2023

Disallow document pip for non-https / file resources. (browser-side)

browser-side followup of https://chromium-review.googlesource.com/c/chromium/src/+/4595397

Fixed: 1451543, 1460025
Change-Id: Id726c087b3d9994ed5a152b8e40f2094338840de
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4746980
Commit-Queue: Ken Buchanan <kenrb@chromium.org>
Reviewed-by: Tommy Steimel <steimel@chromium.org>
Reviewed-by: Ken Buchanan <kenrb@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1182779}

[modify] https://crrev.com/444b0a82fb9f59dd2c3c05dfbccc56fc16c124d2/content/browser/renderer_host/render_frame_host_impl.cc


### [Deleted User] (2023-08-12)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-12)

[Empty comment from Monorail migration]

### ha...@gmail.com (2023-08-15)

As an additional PoC, I also found another way to exploit the empty document PiP omnibar for this bug. Since the omnibar in the document PiP is empty, then we can extend the omnibar using CSS to include our own contents in it (such as https://paypal.com)

Note that only one click is required because we do not need to window.open("https://paypal.com")

Demo: https://hushed-knowledgeable-mastodon.glitch.me/doc-pip-spoofed-omnibar.html

Video attached



### am...@chromium.org (2023-09-09)

[Empty comment from Monorail migration]

### pg...@google.com (2023-09-12)

[Empty comment from Monorail migration]

### pg...@google.com (2023-09-12)

[Empty comment from Monorail migration]

### am...@google.com (2023-09-21)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-09-21)

Congratulations on yet another one, Axel! The Chrome VRP Panel has decided to award you $1,000 for this report + $1,000 patch bonus. 
The reward amount was decided on due to the limited and lower security implications of an empty title bar versus incorrect / spoofed origin information in the omnibox or title bar. 
Thanks for all your efforts here and reporting this issue to us! 

### am...@google.com (2023-09-22)

[Empty comment from Monorail migration]

### be...@gmail.com (2023-09-25)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-18)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-11-18)

This issue was migrated from crbug.com/chromium/1451543?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1451542]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40065384)*
