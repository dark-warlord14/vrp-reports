# Some cross-origin `location` properties are accessible

| Field | Value |
|-------|-------|
| **Issue ID** | [40081656](https://issues.chromium.org/issues/40081656) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Reporter** | pi...@live.nl |
| **Assignee** | yu...@chromium.org |
| **Created** | 2015-03-18 |
| **Bounty** | $3,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36

Steps to reproduce the problem:
1. Go to the below URL
2. Click the button
3. Note that on the below page, the `location.pathname` of the crbug tab is shown. Updates of this property (i.e., navigating on the crbug site) are reflected.

---
data:text/html,<!doctype html><button id="button">open crbug</button><div id="path"></div><script>var popup; button.onclick = function() { popup = open("https://crbug.com/"); }; setInterval(function() { if(popup) { path.textContent = location.__lookupGetter__("pathname").call(popup.location); } }, 500);</script>
---

What is the expected behavior?
Security error, like `popup.location.pathname` gives.

What went wrong?
`location.pathname` is indirectly accessible through the getter.

Did this work before? Yes The issue does not appear in stable 41.0.2272.89 m

Chrome version: 43.0.2337.0 canary (64-bit)  Channel: canary
OS Version: 6.3
Flash Version: Shockwave Flash 17.0 r0

Other `location` properties are also accessible (but `href` is not). The problem is that some location properties have become getters/setters; I think this bug is related to https://crbug.com/chromium/43394.

## Timeline

### ke...@chromium.org (2015-03-19)

Thanks for the report.

yukishiino@: Can you please investigate if this is related to your recent changes?

### cl...@chromium.org (2015-03-19)

This medium+ severity security issue is a regression on trunk.

Please fix this asap. If you are unable to look into this soon, please revert your change.

- Your friendly ClusterFuzz

### yu...@chromium.org (2015-03-23)

[Empty comment from Monorail migration]

### yu...@chromium.org (2015-03-24)

Found the cause and sent out a CL for fix: https://codereview.chromium.org/1016373004/

### ha...@chromium.org (2015-03-25)

[Empty comment from Monorail migration]

### dc...@chromium.org (2015-03-25)

taking over, this is fixable in blink, but it's probably better to do it in v8

### ha...@chromium.org (2015-03-27)

[Empty comment from Monorail migration]

### yu...@chromium.org (2015-03-27)

I've committed https://codereview.chromium.org/1016373004/ and the issue should be now fixed on ToT.

### yu...@chromium.org (2015-03-27)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-03-27)

[Empty comment from Monorail migration]

### bu...@chromium.org (2015-03-31)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=192678

------------------------------------------------------------------
r192678 | yukishiino@chromium.org | 2015-03-27T14:02:13.022954Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/cross-origin-access-over-property-descriptor.html?r1=192678&r2=192677&pathrev=192678
   M http://src.chromium.org/viewvc/blink/trunk/Source/bindings/tests/idls/core/TestInterfaceCheckSecurity.idl?r1=192678&r2=192677&pathrev=192678
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/frame/Window.idl?r1=192678&r2=192677&pathrev=192678
   M http://src.chromium.org/viewvc/blink/trunk/Source/bindings/templates/attributes.cpp?r1=192678&r2=192677&pathrev=192678
   M http://src.chromium.org/viewvc/blink/trunk/Source/bindings/tests/results/core/V8TestInterface.cpp?r1=192678&r2=192677&pathrev=192678
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/cross-origin-access-over-property-descriptor-expected.txt?r1=192678&r2=192677&pathrev=192678
   M http://src.chromium.org/viewvc/blink/trunk/Source/bindings/tests/results/core/V8TestInterfaceCheckSecurity.cpp?r1=192678&r2=192677&pathrev=192678
   M http://src.chromium.org/viewvc/blink/trunk/Source/bindings/tests/results/core/V8TestObject.cpp?r1=192678&r2=192677&pathrev=192678
   M http://src.chromium.org/viewvc/blink/trunk/Source/bindings/scripts/v8_attributes.py?r1=192678&r2=192677&pathrev=192678

Adds missing security checks to DOM attribute accessors.

Since DOM attributes moved to prototype chains and now attributes have getter and setter functions, we need security checks in their getters and setters as same as we have security checks in methods.

BUG=468451

Review URL: https://codereview.chromium.org/1016373004
-----------------------------------------------------------------

### bu...@chromium.org (2015-03-31)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=192835

------------------------------------------------------------------
r192835 | dcarney@chromium.org | 2015-03-31T15:08:44.451997Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/bindings/core/v8/V8DOMConfiguration.cpp?r1=192835&r2=192834&pathrev=192835
   M http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/cross-origin-access-over-property-descriptor-expected.txt?r1=192835&r2=192834&pathrev=192835
   M http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/cross-origin-access-over-property-descriptor.html?r1=192835&r2=192834&pathrev=192835

enable receiver check for accessor callbacks

R=jochen@chromium.org, haraken@chromium.org
BUG=468451

Review URL: https://codereview.chromium.org/1049533003
-----------------------------------------------------------------

### ti...@google.com (2015-04-09)

[Empty comment from Monorail migration]

### pi...@live.nl (2015-05-27)

I noticed Chrome 43 was released to stable, but I can't find this bug in the release notes. Did this bug go through the reward panel?

### mb...@chromium.org (2015-05-27)

Tim, could you check c#14?

### ti...@google.com (2015-05-27)

Hey Pim - not yet, but it was (and still is) listed on the agenda for this week's panel. You should have a decision late next week. 

FYI for stable releases, we prioritize panel reports that affect stable builds.

### pi...@live.nl (2015-06-11)

Sorry to bother you. Have you made a decision yet?

### ti...@google.com (2015-06-11)

No bother at all - we settled on the votes yesterday, now I need to go and formally update all of the bugs later today. 

... but since I'm here already, the panel decided on $3000 for this report. Congrats! We're also trying out a new payment system which should see you getting paid in ~2 weeks vs the ~8 weeks it currently takes.

### ti...@google.com (2015-06-25)

Payment process started - should be ~2 weeks from now.

### cl...@chromium.org (2015-07-03)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2015-07-28)

Thanks for getting all of the paperwork in. Processing via our e-payment system can take up to two weeks, but the reward should be on its way to you. Thanks again for your help!

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/468451?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081656)*
