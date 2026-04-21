# Security: Performance APIs reveal cross-origin URLs.

| Field | Value |
|-------|-------|
| **Issue ID** | [40082523](https://issues.chromium.org/issues/40082523) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink, Blink>PermissionsAPI |
| **Reporter** | pv...@gmail.com |
| **Assignee** | ks...@chromium.org |
| **Created** | 2015-07-18 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

It is possible to read x-domain URLs after a redirect if the page can be iframed. What I think is a violation of the SOP and could be used to steal sensitive data from several pages.

If <http://victim/> redirects to <http://victim/?secret>, an attacker can iframe the first page and obtain the "secret" of the second one.

The exploit abuses what seems a bug in performance.getEntries() when dealing with cached pages.

**VERSION**  

Chrome Version: Version 43.0.2357.134 (64-bit) - stable (it also affects FF and IE)  

Operating System: Any

I have created a simple PoC with a brief explanation in the following URL: <http://vwzq.net/lab/xreadurl/>. The code is also attached, thought it will not work from file://.

Regards,

## Attachments

- [xreadurl.html](attachments/xreadurl.html) (text/html, 2.0 KB)
- [xreadurl2.html](attachments/xreadurl2.html) (text/html, 1.9 KB)

## Timeline

### wf...@chromium.org (2015-07-18)

mkwst can you help triage this report please?

### mk...@chromium.org (2015-07-19)

Yup. This looks like a problem. `http://vwzq.net/` should not have access to the cross-origin `http://demo.vwzq.net/` frame's location.

Ilya, is this a spec bug or an implementation bug? I hope the latter, but given that it apparently affects all browsers, perhaps it's the former? :)

Can you triage this to the right folks for the performance API implementation? CCing ksakamoto@ and sigbjornf@, as `git shortlog Source/core/timing` says they might have opinions here. :)

Suggesting a "High" severity, but I'll leave that up to you, Will

### cl...@chromium.org (2015-07-19)

[Empty comment from Monorail migration]

### [Deleted User] (2015-07-19)

Even without the redirect issue here, is it considered safe for the parent document (using performance.getEntries()) to be able to observe the possibly cross-domain url of an iframe resource via its PerformanceEntry.name?

The redirected-to final URL is the one requested loaded on navigating back, so it follows that PerformanceEntry.name would then use it.

### mk...@chromium.org (2015-07-19)

No, it isn't safe. That's my point. :)

The embedder should only know the URL it puts into the iframe itself; anything else should be an opaque bit of cross-origin fluff.

### [Deleted User] (2015-07-19)

Right, so you are :)

Redirects is the vector to show up this problem over (cached) resources, not somehow handling redirects incorrectly in the Performance API implementation (it has some extra support for those.)

### mk...@chromium.org (2015-07-19)

Ah, ok, now I understand your point. Renaming the bug to make that clear.

### [Deleted User] (2015-07-19)

[Empty comment from Monorail migration]

### ig...@chromium.org (2015-07-20)

Yikes. FWIW, I don't believe this is a RT spec bug, but that's not say the spec can't be improved to guard for this. Opened a tracking bug: https://github.com/w3c/resource-timing/issues/29

### ks...@chromium.org (2015-07-21)

At least in Chrome, history.back() on iframe is not essential, but history traversal on main frame is revealing iframe's redirect URL. (modified PoC attached.)

I guess resource timing for the final URL is added when restroring state of iframes.


### pv...@gmail.com (2015-07-21)

Yep, the f.history.back() and nested timeouts were necessary for FF, my fault.

### mk...@chromium.org (2015-07-21)

ksakamoto@: Since you seem to know things about the API, I'm assigning you this bug. Happy to review patches! :)

### ks...@chromium.org (2015-07-21)

I'll take a closer look tomorrow.

japhet@: I'm not familiar with history navigation. could you point me where to start looking?


### ks...@chromium.org (2015-07-23)

Probably FrameFetchContext::updateTimingInfoForIFrameNavigation should return false when restoring iframe status from history.

### bu...@chromium.org (2015-07-28)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=199553

------------------------------------------------------------------
r199553 | ksakamoto@chromium.org | 2015-07-28T03:19:38.900369Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/misc/resources/frame-final-url.html?r1=199553&r2=199552&pathrev=199553
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/misc/resources/frame-initial-url.html?r1=199553&r2=199552&pathrev=199553
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/misc/resource-timing-iframe-restored-from-history-expected.txt?r1=199553&r2=199552&pathrev=199553
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/misc/resource-timing-iframe-restored-from-history.html?r1=199553&r2=199552&pathrev=199553
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/loader/FrameFetchContext.cpp?r1=199553&r2=199552&pathrev=199553

Do not report Resource Timing for iframe navigations when restored from history

In a back/forward navigation, iframe navigates to its final URL directly.
Iframes should not report Resource Timing except for the initial
navigation requested by the parent document.

BUG=511616
TEST=http/tests/misc/resource-timing-iframe-restored-from-history.html

Review URL: https://codereview.chromium.org/1257953003
-----------------------------------------------------------------

### ks...@chromium.org (2015-07-29)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-07-29)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### ks...@chromium.org (2015-07-30)

Verified the fix in 46.0.2468.0 canary. Requesting merge to M45.

### pe...@google.com (2015-07-30)

Approved for M45 (branch: 2454)

### bu...@chromium.org (2015-07-30)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=199700

------------------------------------------------------------------
r199700 | ksakamoto@chromium.org | 2015-07-30T03:12:07.172944Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/2454/Source/core/loader/FrameFetchContext.cpp?r1=199700&r2=199699&pathrev=199700
   A http://src.chromium.org/viewvc/blink/branches/chromium/2454/LayoutTests/http/tests/misc/resources/frame-final-url.html?r1=199700&r2=199699&pathrev=199700
   A http://src.chromium.org/viewvc/blink/branches/chromium/2454/LayoutTests/http/tests/misc/resources/frame-initial-url.html?r1=199700&r2=199699&pathrev=199700
   A http://src.chromium.org/viewvc/blink/branches/chromium/2454/LayoutTests/http/tests/misc/resource-timing-iframe-restored-from-history-expected.txt?r1=199700&r2=199699&pathrev=199700
   A http://src.chromium.org/viewvc/blink/branches/chromium/2454/LayoutTests/http/tests/misc/resource-timing-iframe-restored-from-history.html?r1=199700&r2=199699&pathrev=199700

Merge 199553 "Do not report Resource Timing for iframe navigatio..."

> Do not report Resource Timing for iframe navigations when restored from history
> 
> In a back/forward navigation, iframe navigates to its final URL directly.
> Iframes should not report Resource Timing except for the initial
> navigation requested by the parent document.
> 
> BUG=511616
> TEST=http/tests/misc/resource-timing-iframe-restored-from-history.html
> 
> Review URL: https://codereview.chromium.org/1257953003

TBR=ksakamoto@chromium.org

Review URL: https://codereview.chromium.org/1266733002
-----------------------------------------------------------------

### la...@google.com (2015-08-04)

Manually move Cr-Blink-Performance-APIs to Cr-Blink-PermissionsAPI

### ks...@chromium.org (2015-08-07)

[Empty comment from Monorail migration]

### ks...@chromium.org (2015-08-07)

Verified the fix in 46.0.2471.2 dev. Can we merge this to M44 stable?

### pe...@google.com (2015-08-07)

[Automated comment] Request affecting a post-stable build (M44), manual review required.

### pe...@chromium.org (2015-08-07)

Merge approved for m44 branch 2403.  If there is another refresh, this can go along for the ride.

### bu...@chromium.org (2015-08-11)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=200289

------------------------------------------------------------------
r200289 | ksakamoto@chromium.org | 2015-08-11T03:09:36.192317Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/branches/chromium/2403/LayoutTests/http/tests/misc/resource-timing-iframe-restored-from-history.html?r1=200289&r2=200288&pathrev=200289
   M http://src.chromium.org/viewvc/blink/branches/chromium/2403/Source/core/loader/FrameFetchContext.cpp?r1=200289&r2=200288&pathrev=200289
   A http://src.chromium.org/viewvc/blink/branches/chromium/2403/LayoutTests/http/tests/misc/resources/frame-final-url.html?r1=200289&r2=200288&pathrev=200289
   A http://src.chromium.org/viewvc/blink/branches/chromium/2403/LayoutTests/http/tests/misc/resources/frame-initial-url.html?r1=200289&r2=200288&pathrev=200289
   A http://src.chromium.org/viewvc/blink/branches/chromium/2403/LayoutTests/http/tests/misc/resource-timing-iframe-restored-from-history-expected.txt?r1=200289&r2=200288&pathrev=200289

Merge 199553 "Do not report Resource Timing for iframe navigatio..."

> Do not report Resource Timing for iframe navigations when restored from history
> 
> In a back/forward navigation, iframe navigates to its final URL directly.
> Iframes should not report Resource Timing except for the initial
> navigation requested by the parent document.
> 
> BUG=511616
> TEST=http/tests/misc/resource-timing-iframe-restored-from-history.html
> 
> Review URL: https://codereview.chromium.org/1257953003

TBR=ksakamoto@chromium.org

Review URL: https://codereview.chromium.org/1281283004
-----------------------------------------------------------------

### ig...@chromium.org (2015-08-18)

Can we remove the security access restriction on this bug? 

### pv...@gmail.com (2015-08-18)

Btw, is this bug elegible for bounty?

### ti...@google.com (2015-08-31)

Marking for M45 release notes, as I'm not confident that this has made into a stable M44 (though it's merged).

#28: Sure - We'll take your report to the reward panel :)

#27: I can remove access restrictions once I can confirm this shipped with a M44 build (i.e. was there a M44 release after the patch landed on branch 2403). Better to be safe than sorry!

### ti...@google.com (2015-08-31)

Updating severity for release notes.

### ti...@google.com (2015-08-31)

Congratulations - Our reward panel decided to award you $1,000 for this report.

We'll credit you in the Chrome release notes as "pvtolkien". Please let me know if you would like to use another name.

Our finance team should reach out to collect your details for payment sometime this week. If that doesn't happen or if you have any questions, please either update this bug or reach out to me at timwillis@

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an established charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************



### pv...@gmail.com (2015-09-01)

Wow! Thank you! :D

Yep, I would prefer to use "cgvwzq" as name.

### ti...@google.com (2015-09-04)

[Empty comment from Monorail migration]

### ti...@google.com (2015-09-23)

Processing via our e-payment system takes ~7 days, but the reward should be on its way to you. Thanks again for your help!

### cl...@chromium.org (2015-11-04)

Bulk update: removing view restriction from closed bugs.

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

This issue was migrated from crbug.com/chromium/511616?no_tracker_redirect=1

[Multiple monorail components: Blink, Blink>PermissionsAPI]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082523)*
