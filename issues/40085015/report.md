# Security: Hijack navigation and spoofed alert dialog via. unbeforeload 

| Field | Value |
|-------|-------|
| **Issue ID** | [40085015](https://issues.chromium.org/issues/40085015) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>Navigation |
| **Platforms** | Linux, Mac, Windows |
| **Reporter** | rs...@gmail.com |
| **Assignee** | dc...@chromium.org |
| **Created** | 2016-08-03 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

An attacker can hijack navigation or spoof a alert dialog on arbitary domain by a use of setTimeout in unbeforeunload and some injected html.

The hijack happens when the user has loaded the payload and

- refreshes
- Navigates to a new site and clicks back
- When user "search on domain" in url
- Tries to navigate to a url on same domain

The vector also opens up for spoofed alert dialog with the correct origin but displayed on a arbitary site.

The possible alert spoof happens in specific cases when the user enters a new url in the address bar and hits enter.

I have attached images of the how the spoofed dialog looks and added the payloads used in the bottom.

**VERSION**  

**Chrome Version: [x.x.x.x] + [stable, beta, or dev]**  

**Operating System: [Please indicate OS, version, and service pack level]**

**REPRODUCTION CASE**

Reproduction of navigation hijack

- Goto <http://159.203.190.123/chrome/unloadhijack.html>
- Do one of the following  
  
  OR
- Refresj
- Navigate to a new site and click back
- Enter a state of "search on domain" in url and t
- Continue to <http://159.203.190.123/chrome/unloadhijack.html?randomString>

Reproduction of spoof dialog

- Go to <http://159.203.190.123/chrome/unloadhijack.html>
- Wait a few seconds, enter a full url like (github.com) and press enter, enter the full url

Please notice that the spoof dialog can be very sporadic almost like a race condition, github.com almost worked every time for me, most rarely facebook and I think is due to a race condition of some kind.

PAYLOAD AT <http://159.203.190.123/chrome/unloadhijack.html>

<p>Refresh or change the url</p>
<script>

window.onbeforeunload = function()  

{  

setTimeout(function() {  

window.document.writeln('<script>window.location.href = "alert.html";</script>');  

}, 0);

return "quux";  

};  

</script>

PAYLOAD AT <http://159.203.190.123/chrome/alert.html>

<script>
alert('IGNORED - RENDERS FOR A SPLIT');
alert('This dialog renders on the victims next page load');
alert('IGNORED');
</script>

## Attachments

- deleted (application/octet-stream, 0 B)
- [Chrome_alert_render_twtr.png](attachments/Chrome_alert_render_twtr.png) (image/png, 928.8 KB)
- [log.txt](attachments/log.txt) (text/plain, 21.0 KB)
- [log2.txt](attachments/log2.txt) (text/plain, 5.2 KB)

## Timeline

### rs...@gmail.com (2016-08-03)

Forgot to add the images. These are images of the spoofed dialog, as promised

### rs...@gmail.com (2016-08-03)

A more clear example of bypass of alert block in unload mode.
Visit 159.203.190.123/chrome/unloadalert.html 
Refresh or try typing a full url (preferly a not cached one)
Effect should be an alert box blocking the unload

Refresh
<script>
window.onbeforeunload = function() {
  alert('notAllowd!');
  setTimeout(function() {
    alert('Allowd!');
  }, 0);

  return "must return a string";
};
</script>


### ra...@chromium.org (2016-08-04)

creis: Can you please help investigate this? You can test by navigating to http://159.203.190.123/chrome/unloadhijack.html and then navigating to facebook.com.

It looks like the onbeforeunload handler manages to inject script into the page before it has finished navigating away. The script sets window.location to a file that that displays the alerts. The new navigation seems racy though - the navigation is definitely started because runs the script, which triggers the prompts. But it gets overriden by the existing navigation.

Also +avi because the alerts that get shown should be dismissed when the navigation occurs.

[Monorail components: UI>Browser>Navigation]

### cr...@chromium.org (2016-08-04)

Yes, confirmed on Windows Canary 54.0.2817.0 and Windows Stable 52.0.2743.82.

Looks like it's probably due to having multiple alert calls pending, where we only dismiss the first one.  Thanks for the report!  I'll try to look into it with Avi.

### rs...@gmail.com (2016-08-04)

Thanks for your quick response times! =)

Also, maybe I did not make it clear enough in the report but, the attacker can also in some limited cases, takeover which url the victim lands at.. for example

<script>

window.onbeforeunload = function()
{
  setTimeout(function() {
      window.document.writeln('<script>window.location.href = "//example.com";<\/script>');
  }, 0);

  return "quux";
};
</script>

If the victim loads the page and then => refreshes || goes to another page and clicks back || navigate to a same-origin url. 

They will land on the site that was injected in the //example.com



I dunno if it really matters to you =) but I would rather just make it clear.



Thanks for taking a look into it.


### cr...@chromium.org (2016-08-12)

Avi, I didn't get a chance to look at this one this week.  Since I'll be out next week, would you have a chance to take a look?  If not, I can investigate when I get back.

### av...@chromium.org (2016-08-12)

I can take a look, though I'm sheriff Mon-Tue and out Thu-Fri. I'll let you know if I figure anything out.


### rs...@gmail.com (2016-09-21)

Hi =) Is this bug report still alive?

### cr...@chromium.org (2016-09-22)

Avi, do you have some time to look at this now?  It seems to have fallen between the cracks.

As best I can tell, the "navigation hijack" part refers to the fact that the beforeunload dialog is able to navigate (thanks to the setTimeout), which we normally disallow.  dcheng@ and lfg@ would be more familiar with that aspect and whether we can block it.  (The unloadalert.html page shows a similar bug, where alert is blocked in beforeunload unless we do a setTimeout.)  Those are perhaps best treated as a separate bug from the alert dialog spoof-- maybe we can file a separate issue for them.  dcheng/lfg: Do you agree?

The primary bug here is that the alert dialog from the attack page is displayed after we do a cross-process navigation to a different site.  Avi's been working on dialogs, so maybe he can track down why the second alert succeeds.  (I know we have some logic to dismiss a dialog when navigating away, and I thought it was supposed to suppress future dialogs as well.)

### av...@chromium.org (2016-09-23)

Attaching a log.

Here's what seems to be happening re dialogs.

The setup: unloadhijack.html has an onbeforeunload handler that has a setTimeout function to load alert.html. unloadhijack is in renderer [[A]].

1. The user types "github.com" into the address bar and hits return.

2. The onbeforeunload handler calls, pops a dialog. The user hits return.

3. Renderer [[B]] is spawned, and it starts navigation to github. The timeout function in [[A]] kicks in, and starts navigation to alert.html.

4. github takes a little while to respond, so [[A]] commits first on alert.html. alert.html has three calls to dialog. The first has the content "IGNORED - RENDERS FOR A SPLIT". The alert is shown, and renderer [[A]] is locked up waiting for a reply.

5. github responds, renderer [[B]] commits. The history list now looks like [alert.html, github]. WebContents sees the commit with DidNavigateAnyFramePostCommit, and cancels all dialogs. The dialog shown in step 4 is closed.

6. Renderer [[A]] gets the response it was waiting for, and immediately fires the second dialog, the one with the content "This dialog renders on the victims next page load". The dialog request comes through WebContents, which passes it on to the JavaScript dialog manager, which is confused. Because the origin of the dialog doesn't match the origin of the main frame, it assumes it's a subframe, so it says "An embedded page says..." when in fact no embedding happens.

7. Renderer [[A]] gets torn down.

So there's no "injection" happening here for dialogs. A simple solution would be to make sure that JavaScript dialog requests are dropped for RenderFrameHosts that aren't in the current tree. Might we want to drop IPCs when we swap out a frame?

This isn't much of an answer, btw, for navigation in the beforeunload timeout function.

### dc...@chromium.org (2016-09-23)

I thought we purposely didn't want to drop IPCs, because the unload handlers use it as a last-ditch place to stick stuff into localStorage, cookies, etc.

### av...@chromium.org (2016-09-23)

Then would a simple "if (!is_active()) return" in RenderFrameHostImpl::OnRunJavaScriptMessage and friends work?

### av...@chromium.org (2016-09-23)

Although I'm curious why the "suppress further dialogs" boolean didn't help.

### cr...@chromium.org (2016-09-24)

Avi, I'm also curious why the "old_render_frame_host->SuppressFurtherDialogs();" line in RFHM::SwapOutOldFrame isn't working here.  That's supposed to send an IPC to the renderer to prevent further dialogs.  (I don't have time at the moment, but source history could reveal the bug we had and test I wrote for that.)

Anyway, yes, I agree that dialogs sent from the non-current RFH should be auto-dismissed.  (And agreed that we shouldn't just ignore the IPC or the renderer process could hang, potentially blocking other tabs.)

Thanks for tracking it down!  And maybe someone can file a separate blocking bug for the "setTimeout allows bypassing nav/alert restrictions on beforeunload" issue?

### av...@chromium.org (2016-09-24)

Re SuppressFurtherDialogs it seems that the render process simply isn't receiving it. It's being sent successfully from the host, but nothing is hitting my logging statements on the renderer side.

But my logging statements are perturbing the race to make it even worse. I'm attaching a log where the race is being lost even worse.

In this race:
1. Old renderer sends dialog right as new renderer commits.
2. The SuppressFurtherDialogs call is made on the old renderer. It somehow isn't received by the old renderer and it doesn't matter.
3. WebContents cancels all dialogs from the old site.
4. The IPC shows up from the old renderer and causes the dialog to be shown.

Even if we figure out the SuppressFurtherDialogs call, we're still losing the race. We need to check in the RFHI that it's not swapped out.

### bu...@chromium.org (2016-09-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/1e870b1fa5121d217751feb61d5aa30386a0a0d2

commit 1e870b1fa5121d217751feb61d5aa30386a0a0d2
Author: avi <avi@chromium.org>
Date: Wed Sep 28 18:27:44 2016

Don't show dialogs from swapped out frames.

BUG=634108
TEST=as in bug
CQ_INCLUDE_TRYBOTS=master.tryserver.chromium.linux:linux_site_isolation

Review-Url: https://codereview.chromium.org/2366693006
Cr-Commit-Position: refs/heads/master@{#421580}

[modify] https://crrev.com/1e870b1fa5121d217751feb61d5aa30386a0a0d2/content/browser/frame_host/navigation_controller_impl_browsertest.cc
[modify] https://crrev.com/1e870b1fa5121d217751feb61d5aa30386a0a0d2/content/browser/frame_host/render_frame_host_impl.cc
[add] https://crrev.com/1e870b1fa5121d217751feb61d5aa30386a0a0d2/content/test/data/navigation_controller/beforeunload_dialog.html


### av...@chromium.org (2016-09-28)

So dialogs are addressed. Daniel, can you look at navigation here?

### dc...@chromium.org (2016-09-28)

Sorry, what am I supposed to look at from the navigation side? Blocking navigations in callbacks queued from beforeunload?

### av...@chromium.org (2016-09-28)

Yes.

Apparently navigation directly from a beforeunload handler doesn't happen, but if we queue a setTimeout callback, navigation from there works.

### dc...@chromium.org (2016-09-28)

+jochen in case there's some v8 mechanism I'm missing.

However, I don't see any easy / feasible way of doing this, we'd have to have some way of capturing extra state into a closure when it's created and then pushing the state back onto the stack when the closure runs at a later point.

We could just say that we don't allow navigations once a page is definitely going to unload, but that is also difficult to determine when that would be: it's before to run beforeunload, and then for the page to never be unloaded if the navigation turns into a download, right?

IMO, the important part here is:
- Navigations queued in this way shouldn't override the initial navigation that triggered the beforeunload dialog, even if the initial navigation is slow to commit.
- Modal dialogs triggered in this way cannot block the actual navigation from committing either.

### av...@chromium.org (2016-09-28)

I'm in agreement with your summary list, and I believe neither of those happen.

### jo...@chromium.org (2016-09-29)

indeed, there's no easy way to capture state for a closure (no easy way as in, it would be very easy for some web api to forget to capture the state)

### sh...@chromium.org (2016-10-13)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-11-21)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-12-02)

[Empty comment from Monorail migration]

### aw...@google.com (2016-12-19)

Seems reasonable to mark this one as fixed.

### sh...@chromium.org (2016-12-20)

[Empty comment from Monorail migration]

### rs...@gmail.com (2016-12-23)

[Comment Deleted]

### aw...@chromium.org (2017-01-23)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-23)

Hi rskansing@ - the panel decided to award $500 for this bug.  Thanks for the report!  A member of our finance team will be in touch.

### aw...@chromium.org (2017-01-23)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-24)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-03-28)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/634108?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40085015)*
