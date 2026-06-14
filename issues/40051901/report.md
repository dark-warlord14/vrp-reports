# Security: Crash in requestAnimationFrame when removing a frame

| Field | Value |
|-------|-------|
| **Issue ID** | [40051901](https://issues.chromium.org/issues/40051901) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | ja...@chromium.org |
| **Assignee** | ja...@chromium.org |
| **Created** | 2011-12-07 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

**Please provide a brief explanation of the security issue.**

Boris Zbarsky from Mozilla reported this crash in requestAnimationFrame handling. I don't currently have access to a debug build to see what sort of crash it is, so reporting as a security bug just in case. Repro case is inline below

**VERSION**  

Chrome Version: 17.0.962.0 (Official Build 112977) canary  

Operating System: Mac

**REPRODUCTION CASE**  

**Please include a demonstration of the security bug, such as an attached**  

**HTML or binary file that reproduces the bug when loaded in Chrome. PLEASE**  

**make the file as small as possible and remove any content not required to**  

**demonstrate the bug.**

Repro:

<!DOCTYPE html>
<script>
window.onload = function() {
var el = document.getElementsByTagName("iframe")[0];
window.frames[0].webkitRequestAnimationFrame(function() {
el.parentNode.removeChild(el);
});
window.frames[1].webkitRequestAnimationFrame(function() {
alert('Called');
});
}
</script>

There should be an alert saying 'Called'.

<iframe></iframe>
<iframe></iframe>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State: Don't have available right this second  

Client ID (if relevant): b780683255d5f911

## Timeline

### sk...@chromium.org (2011-12-08)

Confirmed in both Chrome 15 (Stable) and 18 (Trunk)
src\third_party\webkit\source\webcore\dom\scriptedanimationcontroller.cpp @ line 124:
        // A previous iteration may have invalidated style (or layout).  Update styles for each iteration
        // for now since all we check is the existence of a renderer.
        m_document->updateStyleIfNeeded();

"m_document" is corrupt, or possibly even "this" altogether.

### sk...@chromium.org (2011-12-08)

Upstream https://bugs.webkit.org/show_bug.cgi?id=74036

### ja...@chromium.org (2011-12-08)

Could you cc me (jamesr@chromium.org) on that WebKit bug?

### ja...@chromium.org (2011-12-09)

Fix landed: http://trac.webkit.org/changeset/102405

Since this is secseverity-high (arbitrary code execution in the renderer sandbox) I believe we'll need to merge this to every branch that we are still doing security releases from.  Karen, Anthony, Jason - may I merge this to the 15/16/17 branches?

### in...@chromium.org (2011-12-09)

Thanks a lot James for the quick fix. For this, we just need to merge to m16, m17 branches. Security bugs affecting stable branches have merge approval :)

### in...@chromium.org (2011-12-09)

[Empty comment from Monorail migration]

### ja...@chromium.org (2011-12-09)

http://trac.webkit.org/changeset/102463 for m16 / 912
http://trac.webkit.org/changeset/102464 for m17 / 963


### in...@chromium.org (2011-12-09)

Thanks James.

### in...@chromium.org (2011-12-15)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-12-21)

@bzbarsky: great test case for a great bug! Thanks for the report. It qualifies for a $1000 Chromium Security Reward. We'll release the fix in the first Chrome 16 patch, early in the new year.

----
Boilerplate text:
Please do NOT publicly disclose details until a fix has been released to all our
users. Early public disclosure may cancel the provisional reward.
Also, please be considerate about disclosure when the bug affects a core library
that may be used by other products.
Please do NOT share this information with third parties who are not directly
involved in fixing the bug. Doing so may cancel the provisional reward.
Please be honest if you have already disclosed anything publicly or to third parties.
----

### js...@chromium.org (2012-01-04)

[Empty comment from Monorail migration]

### js...@chromium.org (2012-01-16)

[Empty comment from Monorail migration]

### js...@chromium.org (2012-01-19)

@bzbarsky - As I understand you've already been put in touch with @cevans about receiving your reward. He's on vacation right now, so there may be some additional lag. Please ping back on this bug if there are any further hiccups.

### bz...@gmail.com (2012-01-22)

Gah.  https://crbug.com/chromium/106672#c13, or rather the cc change made with that comment, made it so I no longer get mail for this bug, effectively (since my gmail account is basically a spam-catcher; I check it once every few weeks when I remember to)....  In particular I never got the mail for that comment itself.  Could someone who has the right bits please readd my MIT address to the CC list?

Yes, I wish Google code would let log in with my Google account but use some other mailing address....

For the rest, I have no idea who @cevans is, unless it's the commenter from https://crbug.com/chromium/106672#c10.  The only people I've been in touch with about this are that commenter, jamesr, and jschuh.  If @cevans is not one of those, please let me know who he or she is.

As far as the reward goes, I'm still sorting out what I want to do with it, exactly; been traveling the last few days.  Once I get that sorted, I'll let @cevans, whoever that is, know.

### in...@chromium.org (2012-01-23)

@bzbarsky - cevans and scarybeasts are the same person - Chris Evans, manager of the Chrome Security Team.

I have re-added your mit address to cc list.

### sc...@gmail.com (2012-01-31)

Thanks for your patience Boris. Payment in system. Can take a week or two for electronic transfers believe it or not.

### bz...@gmail.com (2012-01-31)

All good.  Thank you all for your patience as well.

For the rest, I have no problem believing any sort of bustage in a large computer-based system.  ;)

### [Deleted User] (2012-05-15)

Marking old security bugs Fixed..

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-14)

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

This issue was migrated from crbug.com/chromium/106672?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40051901)*
