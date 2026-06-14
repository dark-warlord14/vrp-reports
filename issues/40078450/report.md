# URL Spoof Vulnerability

| Field | Value |
|-------|-------|
| **Issue ID** | [40078450](https://issues.chromium.org/issues/40078450) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI, UI>Browser>Omnibox, UI>Browser>PrintPreview |
| **Reporter** | ba...@gmail.com |
| **Assignee** | cr...@chromium.org |
| **Created** | 2013-11-24 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36

Steps to reproduce the problem:
1. Simply open the poc, click on the button
2. It will automaticly open the spoofed page
3. The spoofed page will get its 'real'/'expected' url once the hidden print dialog on the parent page is closed

What is the expected behavior?

What went wrong?
Once the new tab is opened by window.open() with a url, and is then written by document.write() it will still switch to the actual domain. But if the parent page is blocked by any visual content like alert(),prompt(),confirm()or print() this will be blocked. An attacker would use print() because it does not block the user interaction on the opened (spoofed) page.

Did this work before? N/A 

Chrome version: 31.0.1650.57  Channel: stable
OS Version: 6.2 (Windows 8)
Flash Version: Shockwave Flash 11.9 r900

This vulnerability does not seem to work on the chromium release but does on the latest version of google chrome (31.0.1650.57)

## Attachments

- [poc.png](attachments/poc.png) (image/png, 17.5 KB)
- [poc.html](attachments/poc.html) (text/html, 2.7 KB)
- [poc.html](attachments/poc_53010138.html) (text/html, 979 B)
- [url-spoof.png](attachments/url-spoof.png) (image/png, 45.5 KB)
- [poc2.jpg](attachments/poc2.jpg) (image/jpeg, 39.8 KB)
- [poc.mp4](attachments/poc.mp4) (application/octet-stream, 421.8 KB)
- [chrome.html](attachments/chrome.html) (text/html, 1.1 KB)
- [chromium.html](attachments/chromium.html) (text/html, 1.3 KB)
- [difference_demonstration.mp4](attachments/difference_demonstration.mp4) (application/octet-stream, 4.4 MB)

## Timeline

### pa...@chromium.org (2013-11-24)

I confirm that it works as advertised on Linux M31.

On Linux with a build from trunk as of a couple weeks ago, it looks like the attached screenshot: the Print dialog makes the attack ineffective/less effective, and when you Cancel the Print dialog, the URL in the Omnibox reverts to "about:blank". Still, I would not be surprised if there were a way to retain the effectiveness of the attack.

Attached is a somewhat minimized/reduced version of poc.html.

Adding some Print* labels so that maybe printing people can provide some insight about window state transitions and what has changed. But ultimately I don't think this a printing bug, of course.

### cl...@chromium.org (2013-11-24)

vitalybuka: Can you please take a look or find someone else to own it.

You are auto-assigned this issue since you are the top fixer for area label 'Cr-Internals-Printing'.

- Your friendly ClusterFuzz

### ba...@gmail.com (2013-11-24)

#1 I did not expect this to work on chromium at all. 
Which is why I stated that it only works on chrome. Please note that using chrome, the print dialog will not pop over but stay on the other tab. As shown in the picture below


### ba...@gmail.com (2013-11-24)

pal...@chromium.org
No, this is not a printing bug. One could also use anything that 'holds up' the javascript on the parent page like alert(),confirm(),prompt() or even an infinity loop for that matter. Print() was just a logical choice because it does not cause chrome to switch back to the parent window nor does it lay over the child window.

### ba...@gmail.com (2013-11-24)

I've made a short film demonstration how the poc looks in chrome, doing the same thing on ubuntu works identical. As you can see the print dialog does not block access to the page, and unless the user would immediately switch back to the parent page. The user could easily be fooled. Without unusual user interaction, and remotely exploitable.
With this behavior, does the bug still holds it's 'Low severity' label ? 

### ba...@gmail.com (2013-11-25)

pal...@chromium.org: I've looked into the behaviour of it on chromium some more, and made another poc. In the short video attached both are demonstrated, The difference is technically not that big. But the potential to fool the user with this vulnerability in chrome is bigger. Which is also why I think the security impact should be rated by the behaviour in chrome (stable) release instead of it's behaviour in the chromium (beta) release.

Both poc's shown in the film are also attached, the 'chromium.html' should work in the build of chromium you used.

### fe...@chromium.org (2013-11-25)

Is this related to https://crbug.com/chromium/149871 in terms of choosing when to commit the origin?

### vi...@chromium.org (2013-11-25)

felt@ Not sure how to handle this issue. It's more then just printing.

### me...@chromium.org (2013-11-25)

I don't know if the poc with the printing dialog in https://crbug.com/chromium/322959#c1 is related to https://crbug.com/chromium/149871, since it seems to be fixed.
The bug in https://crbug.com/chromium/322959#c6 seems to be that when you do document.write to a window you opened with window.open, the domain in the omnibox stays the same. FWIW, Firefox is changing the URL to the file which did document.write.

### ba...@gmail.com (2013-11-25)

Shouldn't the security severity be at least medium though ? Especially on chrome, it has a 'stable' window with a spoofed url ?

I did some other test. It is really only the omnibox that seems to be affected here, the window.location etc does not change. Just another side note, it does show 'cookies and site data' of the spoofed url when clicking on the document part on the left side of 'https://'. Maybe this feature should not get it's information from the omnibox, it feels unessesary.

### me...@chromium.org (2013-11-25)

Charlie, Nasko, this seems to be navigation related: calling document.write on a window opened by window.open doesn't set the URL in the omnibox. document.location is correctly set to the location of the window which called window.open. Any thoughts?

### cr...@chromium.org (2013-11-25)

This looks like fallout from the fix for https://crbug.com/chromium/9682.  We have logic that should be reverting the omnibox in cases like this, but it must be missing this case.  I'll take a look.

### ba...@gmail.com (2013-11-25)

Is this bug's SecSeverity-Low ?

### pa...@chromium.org (2013-11-25)

We are bumping it up to Medium. If you/we could get a good HTTPS indicator, it might be High.

### pa...@chromium.org (2013-11-25)

Adding the standard boilerplate text for bugs we might reward under the Vulnerability Rewards Program:

Please do NOT publicly disclose details until a fix has been released to all our
users. Early public disclosure may cancel the provisional reward.
Also, please be considerate about disclosure when the bug affects a core library
that may be used by other products.
Please do NOT share this information with third parties who are not directly
involved in fixing the bug. Doing so may cancel the provisional reward.
Please be honest if you have already disclosed anything publicly or to third parties.

http://www.chromium.org/Home/chromium-security/vulnerability-rewards-program

### cr...@chromium.org (2013-11-25)

Fix is in review: https://codereview.chromium.org/86413004/

This is a fun one to debug because print preview doesn't seem to exist in Chromium (only Google Chrome).  The bug is still visible with the modal print dialog in Chromium, though.  It's also interesting that https://www.google.com seems to immediately commit over the spoof page in M33, making the attack fail.  However, the attack succeeds in M31, M32, and for any other URL I've tested in M33 (including http://www.google.com).  I'm not sure why HTTPS Google is being treated differently in M33.

As I mentioned in https://crbug.com/chromium/322959#c12, we do have some logic to prevent things like this, but it wasn't catching this case.  We saw a similar URL spoof with modal dialogs in https://crbug.com/chromium/281256 and fixed it by notifying the browser process immediately rather than waiting for a one-shot timer (delayed by the modal dialog).  Unfortunately, that fix didn't work for document.write, which moved the FrameLoader's state machine past the initial empty document state.

The updated fix notifies the browser process of the spoof even if the FrameLoader has moved on to another state, so the user will see about:blank in the omnibox instead of the URL of the attacker's choice.

### va...@chromium.org (2013-11-25)

FYI - you can use print preview in chromium by copying the pdf plugin library into your build directory and starting chromium with the --enable-print-preview flag.

### cl...@chromium.org (2013-11-26)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-11-26)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=162673

------------------------------------------------------------------------
r162673 | creis@chromium.org | 2013-11-26T07:04:50.446301Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/loader/FrameLoader.cpp?r1=162673&r2=162672&pathrev=162673
   M http://src.chromium.org/viewvc/blink/trunk/Source/web/tests/WebFrameTest.cpp?r1=162673&r2=162672&pathrev=162673

Notify the client of a document access even if document.write is used.

Modal dialogs can usually delay the notification from reaching the client.
notifyIfInitialDocumentAccessed is used to skip the timer if a dialog
is shown (via PageGroupLoadDeferrer), but it shouldn't care whether the
FrameLoader is still in the initial empty document state.

BUG=322959
TEST=See bug for repro steps.

Review URL: https://codereview.chromium.org/86413004
------------------------------------------------------------------------

### cr...@chromium.org (2013-11-26)

Fixed in Blink revision 162673.  That didn't make today's Canary (33.0.1720.0), but so we should be able to verify it tomorrow to decide about merging.

### cl...@chromium.org (2013-11-26)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### cr...@chromium.org (2013-11-27)

Just verified the fix on the 33.0.1721.0 canary on Mac.

Karen, would you like me to merge this to M32, either before or after the long weekend?

Anthony, is it too late to merge to M31?

### ka...@google.com (2013-12-02)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-12-02)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=163011

------------------------------------------------------------------------
r163011 | creis@chromium.org | 2013-12-02T18:27:45.515706Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/1700/Source/core/loader/FrameLoader.cpp?r1=163011&r2=163010&pathrev=163011
   M http://src.chromium.org/viewvc/blink/branches/chromium/1700/Source/web/tests/WebFrameTest.cpp?r1=163011&r2=163010&pathrev=163011

Merge 162673 "Notify the client of a document access even if doc..."

> Notify the client of a document access even if document.write is used.
> 
> Modal dialogs can usually delay the notification from reaching the client.
> notifyIfInitialDocumentAccessed is used to skip the timer if a dialog
> is shown (via PageGroupLoadDeferrer), but it shouldn't care whether the
> FrameLoader is still in the initial empty document state.
> 
> BUG=322959
> TEST=See bug for repro steps.
> 
> Review URL: https://codereview.chromium.org/86413004

TBR=creis@chromium.org

Review URL: https://codereview.chromium.org/99723002
------------------------------------------------------------------------

### in...@chromium.org (2013-12-02)

Merge-Requested for m31.

### la...@google.com (2013-12-02)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-12-02)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=163024

------------------------------------------------------------------------
r163024 | creis@chromium.org | 2013-12-02T20:26:06.149761Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/1650/Source/core/loader/FrameLoader.cpp?r1=163024&r2=163023&pathrev=163024
   M http://src.chromium.org/viewvc/blink/branches/chromium/1650/Source/web/tests/WebFrameTest.cpp?r1=163024&r2=163023&pathrev=163024

Merge 162673 "Notify the client of a document access even if doc..."

> Notify the client of a document access even if document.write is used.
> 
> Modal dialogs can usually delay the notification from reaching the client.
> notifyIfInitialDocumentAccessed is used to skip the timer if a dialog
> is shown (via PageGroupLoadDeferrer), but it shouldn't care whether the
> FrameLoader is still in the initial empty document state.
> 
> BUG=322959
> TEST=See bug for repro steps.
> 
> Review URL: https://codereview.chromium.org/86413004

TBR=creis@chromium.org

Review URL: https://codereview.chromium.org/99413003
------------------------------------------------------------------------

### in...@chromium.org (2013-12-02)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-12-02)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=163029

------------------------------------------------------------------------
r163029 | creis@chromium.org | 2013-12-02T21:05:06.451040Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/1650/Source/web/tests/WebFrameTest.cpp?r1=163029&r2=163028&pathrev=163029
   M http://src.chromium.org/viewvc/blink/branches/chromium/1650/Source/core/loader/FrameLoader.cpp?r1=163029&r2=163028&pathrev=163029

Revert 163024 "Merge 162673 "Notify the client of a document acc..."

The test failed to compile.  Will try to merge again without test.

> Merge 162673 "Notify the client of a document access even if doc..."
> 
> > Notify the client of a document access even if document.write is used.
> > 
> > Modal dialogs can usually delay the notification from reaching the client.
> > notifyIfInitialDocumentAccessed is used to skip the timer if a dialog
> > is shown (via PageGroupLoadDeferrer), but it shouldn't care whether the
> > FrameLoader is still in the initial empty document state.
> > 
> > BUG=322959
> > TEST=See bug for repro steps.
> > 
> > Review URL: https://codereview.chromium.org/86413004
> 
> TBR=creis@chromium.org
> 
> Review URL: https://codereview.chromium.org/99413003

TBR=creis@chromium.org

Review URL: https://codereview.chromium.org/100123002
------------------------------------------------------------------------

### bu...@chromium.org (2013-12-02)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=163031

------------------------------------------------------------------------
r163031 | creis@chromium.org | 2013-12-02T21:08:54.985272Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/1650/Source/core/loader/FrameLoader.cpp?r1=163031&r2=163030&pathrev=163031

Merge 162673 "Notify the client of a document access even if doc..."

> Notify the client of a document access even if document.write is used.
> 
> Modal dialogs can usually delay the notification from reaching the client.
> notifyIfInitialDocumentAccessed is used to skip the timer if a dialog
> is shown (via PageGroupLoadDeferrer), but it shouldn't care whether the
> FrameLoader is still in the initial empty document state.
> 
> BUG=322959
> TEST=See bug for repro steps.
> 
> Review URL: https://codereview.chromium.org/86413004

TBR=creis@chromium.org

Review URL: https://codereview.chromium.org/99783004
------------------------------------------------------------------------

### mb...@chromium.org (2013-12-03)

Thanks for the report! This one qualifies for a $500 reward. Bugs like this one can qualify at higher reward levels if they are also able to spoof a valid https connection (with the green lock).

How would you like us to credit you when we mention this bug in our release notes?

### ba...@gmail.com (2013-12-03)

"Bas Venis" would be great, thank you :)

### pa...@chromium.org (2013-12-18)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-12-18)

Hey Bas, I just kicked off of our payment process on this, which can take a couple of weeks. Someone should get in touch to sign you up as a supplier. Thanks for helping Chrome security!

### ba...@gmail.com (2014-01-15)

Is there any indication on when this bug report would become public and on when I could publish details about this vulnerability ?


### ke...@chromium.org (2014-01-15)

Removing view restrictions is a manual step that is done on a bulk set of bugs every 3 months or so.

http://www.chromium.org/Home/chromium-security/security-faq#TOC-Can-you-please-un-hide-old-security-bugs-

The 9 month threshold mentioned in that FAQ might be obsolete. Looking historically, we haven't been waiting that long to disclose.

### ba...@gmail.com (2014-02-03)

[Comment Deleted]

### [Deleted User] (2014-02-03)

Yes, the fix has shipped to all of our users so you can go ahead and talk about this publicly if you would like without impacting your award. 

Thank you for checking!

### ti...@chromium.org (2014-02-28)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-03-28)

Bulk update: removing view restriction from closed bugs.

### cl...@chromium.org (2016-02-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/322959?no_tracker_redirect=1

[Multiple monorail components: UI, UI>Browser>Omnibox, UI>Browser>PrintPreview]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40078450)*
