# Security: Address bar spoofing in Chrome for Android

| Field | Value |
|-------|-------|
| **Issue ID** | [40078488](https://issues.chromium.org/issues/40078488) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>Navigation |
| **Platforms** | Android |
| **Reporter** | lp...@gmail.com |
| **Assignee** | dt...@chromium.org |
| **Created** | 2013-12-02 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

It is possible to spoof address bar content by opening a window and immediately writing to that window with document.write(). The address bar is filled with initial URL and not updated on document.write(), which cancels the navigation.

**VERSION**  

Chrome Version: 31.0.1650.59 stable  

Operating System: Android 4.0.4; ST21i Build/11.0.A.4.22

**REPRODUCTION CASE**  

<http://runic.pl/testy/android/chrome-31-abs.html>

<script>
function test01() {
pop = window.open('https:/www.google.com', '\_t1');
pop.document.write('<script>document.write(document.location.toString().replace("<","&lt;")+"<br>")</scr'+'ipt>');
}
</script>
<input type="button" onclick="test01()" value="Run">

RESULT  

"<https://www.google.com>" in address bar  

"<http://runic.pl/testy/android/chrome-31-abs.html>" in page content

## Timeline

### wf...@chromium.org (2013-12-03)

Confirmed on Beta and Stable Chrome on Android.  This doesn't happen on desktop.  Doesn't seem like it would require interaction to spoof the URL bar.  The padlock doesn't correctly appear on the https though.  CCs can you take a look and assign to someone?

### js...@chromium.org (2013-12-03)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-12-03)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-12-03)

Confirmed on ToT Chrome/Android. Confirmed both location bar and page content show "about:blank" on Chrome/iOS (Beta).

### cr...@chromium.org (2013-12-03)

@palmer: Are you sure it still repros?  It sounds a *lot* like https://crbug.com/chromium/322959, which I just fixed last week and merged to M31 and M32 yesterday.  What Blink revision are you testing against?

### pa...@chromium.org (2013-12-03)

I am using ToT from yesterday. I'll rebuild with today's tree and let you know.

### pa...@chromium.org (2013-12-03)

creis: Fresh tree, rebuild, reinstall, re-test. Still reproduces. Blink version: 537.36 (@163007).

### cr...@chromium.org (2013-12-03)

palmer: Thanks for checking.  I can confirm on Android, but I get about:blank in the address bar for Linux.

dtrainor: This sounds similar to the Android-only spoof we resolved in https://crbug.com/chromium/304226.  Would you mind taking a look to see if you can tell what's going on?  I'm guessing we're getting to WebContentsImpl::didAccessInitialDocument again but we don't update the address bar.

### dt...@chromium.org (2013-12-04)

I'll take a look tomorrow morning.

### dt...@chromium.org (2013-12-04)

Inside DidAccessInitialDocument the URL of the active entry is still https://www.google.com.  Is it supposed to be something different at this point?

### na...@chromium.org (2013-12-04)

Which specific DidAccessInitialDocument method are you looking at? In general, "active" entry is a deprecated concept and shouldn't be used. It should be changed from active entry to either visible or last committed.

### dt...@chromium.org (2013-12-04)

Ah sorry I mixed them up :(.  I'm talking about WebContentsImpl::DidAccessInitialDocument.  Actually the VisibleEntry is NULL here.

### dt...@chromium.org (2013-12-04)

Is a NULL visible entry expected/a valid state?  Should we be showing about:blank in this case?  We were caching the previous URL if we didn't have one (we have to do some interesting things because we can tear down an entire WebContents but still have a "tab").  It looks like we're treating an empty url incorrectly.

### cr...@chromium.org (2013-12-04)

Thanks for taking a look.  I think we need to display about:blank if GetVisibleEntry is null, since the previously displayed URL is dangerous in this case.  (I think null is expected here, since there's no last committed entry and the pending entry isn't safe to show.)

Would you be able to update it to do that?  (Sorry, I'm OOO today and tomorrow.)

### dt...@chromium.org (2013-12-05)

I have a patch in place to fix this.  We were incorrectly caching the URL value on a provisional load start and returning that value after a navigation state changed because we did got an empty string from the WebContents.  I updated the logic to only return the cached value if we don't have a WebContents present, which we need to do if we haven't restored all of the tab state yet.

Right now it says, "Search or type url" at the top if the URL is empty on Android.

### lp...@gmail.com (2013-12-05)

On a side note, I am wondering what should be shown in the address bar in similar cases, especially considering mobile browsers (Android/iOS). If address bar is meant to be a security indicator, then showing 'about:blank' or a blank address bar does not tell much to the user. Did Chrome team consider showing parent URL (with visible domain context) in such cases?

This is a general question and not related to this specific bug (which seems to be fixed ok by above description).

### lp...@gmail.com (2013-12-05)

To my last comment: see also https://crbug.com/chromium/326125 for Chrome on iOS.

### pa...@chromium.org (2013-12-05)

I think this bug is potentially rewardable under the Chrome Vulnerability Rewards Program. Putting it up to the rewards panel to decide.

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

### dt...@chromium.org (2013-12-05)

Fixed with https://chrome-internal-review.googlesource.com/#/c/149166/.

### dt...@chromium.org (2013-12-05)

This landed on trunk.  Do we need to cherry pick this to other branches?  If so lets give it a day or two on trunk and merge it over.

Marking as fixed.  If that's the incorrect process with these kind of bugs please reopen :).

### cl...@chromium.org (2013-12-06)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### cr...@chromium.org (2013-12-07)

Thanks @dtrainor!  Much appreciated.

https://crbug.com/chromium/324969#c16: It's unfortunately a difficult issue to solve without introducing more confusion.  While the about:blank page does inherit the effective origin of its opener, I would argue that it does not make sense to display that in the address bar since there's no actual URL it corresponds to.  That's a separate topic from this bug, though.

### lp...@gmail.com (2013-12-07)

[Comment Deleted]

### dt...@chromium.org (2013-12-09)

[Empty comment from Monorail migration]

### ka...@google.com (2013-12-09)

[Empty comment from Monorail migration]

### dt...@chromium.org (2013-12-10)

Merged with https://chrome-internal-review.googlesource.com/#/c/149584/.

### bu...@chromium.org (2013-12-14)

The following change refers to this bug:
https://chrome-internal-review.googlesource.com/149584

### bu...@chromium.org (2013-12-14)

The following change refers to this bug:
https://chrome-internal-review.googlesource.com/149166

### dh...@google.com (2014-01-07)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-01-09)

[Empty comment from Monorail migration]

### dh...@google.com (2014-01-09)

[Empty comment from Monorail migration]

### mb...@chromium.org (2014-01-13)

Thanks for the report! This one qualifies for a $1000 reward since it appears to be a full address bar spoof that requires minimal user interaction.

### lp...@gmail.com (2014-01-13)

It's me who should thank, that's a nice reward :)

### lp...@gmail.com (2014-01-22)

Deleted https://crbug.com/chromium/324969#c23 with credentials.

### ti...@chromium.org (2014-02-28)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-03-28)

Bulk update: removing view restriction from closed bugs.

### bh...@gmail.com (2015-02-18)

how can I see the changes .. I am new member on this site ...

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

This issue was migrated from crbug.com/chromium/324969?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40078488)*
