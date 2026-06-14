# Security: browser history sniffing via HSTS + CSP (bypass previous fix)

| Field | Value |
|-------|-------|
| **Issue ID** | [40084770](https://issues.chromium.org/issues/40084770) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>SecurityFeature, Privacy, UI>Browser>History |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | [Deleted User] |
| **Assignee** | mk...@chromium.org |
| **Created** | 2016-07-06 |
| **Bounty** | $1,000.00 |

## Description

*No description available.*

## Timeline

### lg...@chromium.org (2016-07-06)

Foiled yet again by port trickery. :-(

Assigning to OWP folks.

[Monorail components: Blink>SecurityFeature Privacy UI>Browser>History]

### mk...@chromium.org (2016-07-06)

Yup. I'll go drill another hole in CSP that maps `:80` onto `:80` and `:443`, I suppose. Since HSTS doesn't modify non-standard ports, that should address the bulk of the remaining surface area. Does that sound reasonable?

Giving this the same flags as https://crbug.com/chromium/544765 (though "medium" sounds high, honestly).

### lg...@chromium.org (2016-07-07)

mkwst: HSTS affects all ports. ;-)

" This specification also incorporates notions from [JacksonBarth2008]
   in that policy is applied on an "entire-host" basis: it applies to
   HTTP (only) over any TCP port of the issuing host."
https://tools.ietf.org/html/rfc6797#section-1

"if the URI contains an explicit port component that is not
          equal to "80", the port component value MUST be preserved;
          otherwise,"
https://tools.ietf.org/html/rfc6797#section-8.3

### ca...@chromium.org (2016-07-07)

Is this Security_Impact-Stable? Also this should have a Milestone.

### lg...@chromium.org (2016-07-07)

Yeah, it probably affects stable. ReleaseBlock-Stable isn't appropriate, since this is not a regression.

However, M52 reaches stable in 3 weeks; I'll let Mike decide if that's feasible. :-)

### mk...@chromium.org (2016-07-07)

lgarron@: Right. HSTS doesn't _modify_ non-standard ports, it simply changes the protocol. That means that there shouldn't be (??) any other port-related edge cases to worry about after https://github.com/w3c/webappsec-csp/commit/22d08b990290e49f5a666fad08de16d75bb369e7#diff-117d6498d2aa8019cc0abf5eeb87a9fa.

Patch up at https://codereview.chromium.org/2125873003. CCing Jochen on this bug, since I've asked him to review that patch. :)

### bu...@chromium.org (2016-07-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/e6d181417ea462ac221d768c960a21018266a4a8

commit e6d181417ea462ac221d768c960a21018266a4a8
Author: mkwst <mkwst@chromium.org>
Date: Thu Jul 07 11:18:19 2016

CSP: Allow ':80' to match ':443' in source expressions.

https://github.com/w3c/webappsec-csp/commit/22d08b990290e49f5a666fad08de16d75bb369e7#diff-117d6498d2aa8019cc0abf5eeb87a9fa
updated CSP to allow insecure ports to match secure ports in source
expressions. This is a refinement of the change that landed in
https://codereview.chromium.org/1455973003 to address Sniffly.

BUG=625945
R=jochen@chromium.org

Review-Url: https://codereview.chromium.org/2125873003
Cr-Commit-Position: refs/heads/master@{#404127}

[modify] https://crrev.com/e6d181417ea462ac221d768c960a21018266a4a8/third_party/WebKit/Source/core/frame/csp/CSPSource.cpp
[modify] https://crrev.com/e6d181417ea462ac221d768c960a21018266a4a8/third_party/WebKit/Source/core/frame/csp/CSPSourceTest.cpp


### sh...@chromium.org (2016-07-07)

[Empty comment from Monorail migration]

### mk...@chromium.org (2016-07-07)

Preemptively requesting a merge back to 53 and 52. The patch is small and should be pretty low risk. I don't think it's worth trying to merge into 51, but if things don't explode on Canary tomorrow, I'd like to pull this patch back to beta. 

+{dbates,johnwilander}@webkit.org, ckerschbaumer@mozilla.com who might want to pull similar patches for their respective browsers. I don't have access to the Bugzilla bug or I'd just comment there.

xiaoyin.li@: It's probably worth copy/pasting this report to bugs.webkit.org as well.

### lg...@chromium.org (2016-07-07)

> HSTS doesn't _modify_ non-standard ports, it simply changes the protocol

Ah, yes, you're correct, sorry.
The spec explicitly specifies that port 80 is mapped to 443, and nothing else.

The scheme is modified, but I guess we already have that covered.

### mk...@chromium.org (2016-07-08)

xiaoyin.l@: I don't think the proposed mitigation helps.

First, you can improve your PoC by using the `securitypolicyviolation` event, which will certainly trigger if we block the request to the upgraded URL. That is, this isn't a timing issue, it's a fundamental issue with the interaction between CSP's current behavior and HSTS. If we allow the one to block the other, then we're vulnerable to the information leakage you're describing.

Second, CSP ought to be blocking outgoing requests if it's to be effective at doing the work it's trying to do. That is, if we don't change the existing behavior, then it's not at all clear to me that allowing requests to go through despite violating the policy is a reasonable thing to do.

Third, I think I'm philosophically opposed to allowing a site to lock itself into insecure transport, if for no other reason than the fact that it would present a barrier to eventual migration to TLS. :)

### sh...@chromium.org (2016-07-08)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-07-09)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-14)

[Empty comment from Monorail migration]

### go...@chromium.org (2016-07-14)

Before we approve merge to M52, Could you please confirm whether this change is baked/verified in Canary and safe to merge?

Also is this change applicable to all OS or any specific OS?

### mk...@chromium.org (2016-07-15)

> Before we approve merge to M52, Could you please confirm whether this change is baked/verified in Canary and safe to merge?

Patch landed a week ago and hasn't exploded yet. The bulk of the change is ~2 lines in CSPSource that are fairly straightforward to visually confirm. I think it's safe to merge.

> Also is this change applicable to all OS or any specific OS?

All OSs that use Blink (that is, everything except iOS). I've marked the OS checkboxes accordingly.

### go...@chromium.org (2016-07-15)

Thank you  mkwst@@. 

+awhalley@ to decide whether we can take this merge in for M52 as it is only baked in canary (not baked in dev/beta yet).

### aw...@chromium.org (2016-07-15)

Externally medium merging to Beta (just!) so we're good here; and I agree the diffs look reasonable.

### go...@chromium.org (2016-07-15)

Approving merge to M53 branch 2785 and M52 branch 2743 based on https://crbug.com/chromium/625945#c24. Please merge ASAP (possibly before 5:00 PM PST today, Friday or latest by 4:00 PM PST on Monday).

### go...@chromium.org (2016-07-15)

[Comment Deleted]

### bu...@chromium.org (2016-07-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/17f5f3aa721a2b0069174f29e38d7d48cea05945

commit 17f5f3aa721a2b0069174f29e38d7d48cea05945
Author: Mike West <mkwst@google.com>
Date: Fri Jul 15 18:50:45 2016

CSP: Allow ':80' to match ':443' in source expressions.

https://github.com/w3c/webappsec-csp/commit/22d08b990290e49f5a666fad08de16d75bb369e7#diff-117d6498d2aa8019cc0abf5eeb87a9fa
updated CSP to allow insecure ports to match secure ports in source
expressions. This is a refinement of the change that landed in
https://codereview.chromium.org/1455973003 to address Sniffly.

BUG=625945
R=jochen@chromium.org

Review-Url: https://codereview.chromium.org/2125873003
Cr-Commit-Position: refs/heads/master@{#404127}
(cherry picked from commit e6d181417ea462ac221d768c960a21018266a4a8)

Review URL: https://codereview.chromium.org/2156653002 .

Cr-Commit-Position: refs/branch-heads/2785@{#161}
Cr-Branched-From: 68623971be0cfc492a2cb0427d7f478e7b214c24-refs/heads/master@{#403382}

[modify] https://crrev.com/17f5f3aa721a2b0069174f29e38d7d48cea05945/third_party/WebKit/Source/core/frame/csp/CSPSource.cpp
[modify] https://crrev.com/17f5f3aa721a2b0069174f29e38d7d48cea05945/third_party/WebKit/Source/core/frame/csp/CSPSourceTest.cpp


### bu...@chromium.org (2016-07-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/6ebff0f8de665d2ea2a7d109ef1aeca753993396

commit 6ebff0f8de665d2ea2a7d109ef1aeca753993396
Author: Mike West <mkwst@google.com>
Date: Fri Jul 15 18:56:00 2016

CSP: Allow ':80' to match ':443' in source expressions.

https://github.com/w3c/webappsec-csp/commit/22d08b990290e49f5a666fad08de16d75bb369e7#diff-117d6498d2aa8019cc0abf5eeb87a9fa
updated CSP to allow insecure ports to match secure ports in source
expressions. This is a refinement of the change that landed in
https://codereview.chromium.org/1455973003 to address Sniffly.

BUG=625945
R=jochen@chromium.org

Review-Url: https://codereview.chromium.org/2125873003
Cr-Commit-Position: refs/heads/master@{#404127}
(cherry picked from commit e6d181417ea462ac221d768c960a21018266a4a8)

Review URL: https://codereview.chromium.org/2148793008 .

Cr-Commit-Position: refs/branch-heads/2743@{#650}
Cr-Branched-From: 2b3ae3b8090361f8af5a611712fc1a5ab2de53cb-refs/heads/master@{#394939}

[modify] https://crrev.com/6ebff0f8de665d2ea2a7d109ef1aeca753993396/third_party/WebKit/Source/core/frame/csp/CSPSource.cpp
[modify] https://crrev.com/6ebff0f8de665d2ea2a7d109ef1aeca753993396/third_party/WebKit/Source/core/frame/csp/CSPSourceTest.cpp


### aw...@chromium.org (2016-07-19)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-25)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-25)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-25)

Our panel has decided to award $1,000 for this report!  A member of our finance team will be in touch in the next few weeks.

### aw...@chromium.org (2016-07-25)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-08-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-14)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/625945?no_tracker_redirect=1

[Multiple monorail components: Blink>SecurityFeature, Privacy, UI>Browser>History]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084770)*
