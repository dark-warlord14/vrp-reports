# Security: document.baseURI contains not-encoded representation of URI and may lead to DOM based XSS

| Field | Value |
|-------|-------|
| **Issue ID** | [40088802](https://issues.chromium.org/issues/40088802) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>DOM, Blink>Network |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ma...@gmail.com |
| **Assignee** | mk...@chromium.org |
| **Created** | 2017-08-24 |
| **Bounty** | $500.00 |

## Description

VULNERABILITY DETAILS
Chrome is rendering unencoded version of URI when using document.write(document.baseURI); This is not expected behavior and Firefox renders encoded characters in that case.

Please have a look into it.

VERSION
Chrome Version: 60.0.3112.101 (Official Build) (64-bit)
Operating System: Windows 7 Professional

REPRODUCTION CASE
To reproduce on local please try: file:///C:/Users/abcde/Desktop/test.html#test<strong>test</strong>

I've also placed that on gist https://gistpreview.github.io/?4ce86a5183bb8317c91dbbb1839c3a4f#test<strong>test</strong>


---

Further thoughts:
- oddly enough when you do #test<script>alert('xss');</script> it'll get blocked with: ERR_BLOCKED_BY_XSS_AUDITOR
- it's tricky to say without doubt whether it's a chrome or javascript security issue then since some strings are blocked by auditor it could be that you'd like to have the values urlencoded

## Attachments

- [test.html](attachments/test.html) (text/plain, 110 B)
- [reproduced.png](attachments/reproduced.png) (image/png, 21.6 KB)

## Timeline

### el...@chromium.org (2017-08-24)

[Empty comment from Monorail migration]

[Monorail components: Blink>DOM Blink>Network]

### ta...@google.com (2017-08-25)

I'm not sure who should own this bug. This seems like a serious issue.  mkwst@, are you the right person for this?

### sh...@chromium.org (2017-08-26)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-08-26)

[Empty comment from Monorail migration]

### mk...@chromium.org (2017-08-28)

It does look like we ought to be treating this as a serialized URL when accessing the getter. That said, I don't believe this is a high-severity bug. It provides an injection vector, but preconditions exist for turning that vector into execution (at least the following: the page needs to dump `baseURI` into a context where it can be executed, needs to bypass the auditor while doing so, and needs to not overwrite the document's base URL via `<meta>`).

It's a real bug, but not one we're going to need to spin a new stable build to fix. :) I expect the fix to be small; let's see if we can get something into 61 (though that's pretty tight).

### mk...@chromium.org (2017-08-31)

Looking deeper, this is an issue with URL serialization in general (e.g. `location.href` has the same behavior). We ought to be percent-encoding a few things that we're currently not.

Retargeting to 63, as we've been living with this behavior since forever, so far as I can tell. We should align to the spec, but it's not a regression.

### ma...@gmail.com (2017-09-06)

[Comment Deleted]

### ma...@gmail.com (2017-09-06)

[Comment Deleted]

### sh...@chromium.org (2017-09-14)

mkwst: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mk...@chromium.org (2017-09-15)

Digging into this a bit more, Firefox isn't actually following the spec, as it looks like they're encoding the fragment state (https://url.spec.whatwg.org/#fragment-state) according to the rules for either path or query state. I think their behavior is reasonable, though. *shrug* CCing Anne for his thoughts, as I might be misinterpreting.

https://chromium-review.googlesource.com/#/c/chromium/src/+/668363 takes care of UTF8 characters. I'll look at the rest of the path percent-encode set (https://url.spec.whatwg.org/#path-percent-encode-set) characters that Firefox is encoding in fragments in a subsequent patch.

### an...@gmail.com (2017-09-15)

Safari is the browser most closely aligned with the standard. Firefox likely still has many little deviations.

### mk...@chromium.org (2017-09-15)

Anne: Right. I was asking whether Firefox's deviation with regard to ref encoding seems reasonable to you as an alteration to the spec, or whether there are compelling reasons to align with Safari/the spec. :)

### an...@gmail.com (2017-09-15)

It might be reasonable to change since I think it's a bit surprising that U+0020 doesn't get encoded.

### mk...@chromium.org (2017-09-15)

Filed https://github.com/whatwg/url/issues/344.

### bu...@chromium.org (2017-10-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/f8f6ed59949be4451ee2f5443d8a313f102fde60

commit f8f6ed59949be4451ee2f5443d8a313f102fde60
Author: Mike West <mkwst@chromium.org>
Date: Mon Oct 09 20:58:50 2017

Percent-encode UTF8 characters in URL fragment identifiers.

This brings us into line with Firefox, Safari, and the spec.

Bug: 758523
Change-Id: I7e354ab441222d9fd08e45f0e70f91ad4e35fafe
Reviewed-on: https://chromium-review.googlesource.com/668363
Commit-Queue: Mike West <mkwst@chromium.org>
Reviewed-by: Jochen Eisinger <jochen@chromium.org>
Reviewed-by: Andy Paicu <andypaicu@chromium.org>
Cr-Commit-Position: refs/heads/master@{#507481}
[modify] https://crrev.com/f8f6ed59949be4451ee2f5443d8a313f102fde60/components/url_formatter/elide_url_unittest.cc
[modify] https://crrev.com/f8f6ed59949be4451ee2f5443d8a313f102fde60/components/url_formatter/url_formatter_unittest.cc
[modify] https://crrev.com/f8f6ed59949be4451ee2f5443d8a313f102fde60/components/url_matcher/url_matcher_unittest.cc
[rename] https://crrev.com/f8f6ed59949be4451ee2f5443d8a313f102fde60/third_party/WebKit/LayoutTests/external/wpt/url/url-setters-expected.txt
[modify] https://crrev.com/f8f6ed59949be4451ee2f5443d8a313f102fde60/third_party/WebKit/LayoutTests/fast/domurl/url-hash.html
[modify] https://crrev.com/f8f6ed59949be4451ee2f5443d8a313f102fde60/third_party/WebKit/LayoutTests/fast/url/anchor-expected.txt
[modify] https://crrev.com/f8f6ed59949be4451ee2f5443d8a313f102fde60/third_party/WebKit/LayoutTests/fast/url/file-http-base-expected.txt
[modify] https://crrev.com/f8f6ed59949be4451ee2f5443d8a313f102fde60/third_party/WebKit/LayoutTests/fast/url/script-tests/anchor.js
[modify] https://crrev.com/f8f6ed59949be4451ee2f5443d8a313f102fde60/third_party/WebKit/LayoutTests/fast/url/script-tests/file-http-base.js
[modify] https://crrev.com/f8f6ed59949be4451ee2f5443d8a313f102fde60/third_party/WebKit/LayoutTests/fast/url/script-tests/file.js
[modify] https://crrev.com/f8f6ed59949be4451ee2f5443d8a313f102fde60/third_party/WebKit/LayoutTests/fast/url/script-tests/segments.js
[modify] https://crrev.com/f8f6ed59949be4451ee2f5443d8a313f102fde60/third_party/WebKit/LayoutTests/fast/url/script-tests/standard-url.js
[modify] https://crrev.com/f8f6ed59949be4451ee2f5443d8a313f102fde60/third_party/WebKit/LayoutTests/fast/url/segments-expected.txt
[modify] https://crrev.com/f8f6ed59949be4451ee2f5443d8a313f102fde60/third_party/WebKit/LayoutTests/http/tests/uri/resolve-encoding-relative-expected.txt
[modify] https://crrev.com/f8f6ed59949be4451ee2f5443d8a313f102fde60/third_party/WebKit/LayoutTests/platform/linux/external/wpt/url/a-element-expected.txt
[modify] https://crrev.com/f8f6ed59949be4451ee2f5443d8a313f102fde60/third_party/WebKit/LayoutTests/platform/linux/external/wpt/url/a-element-xhtml-expected.txt
[modify] https://crrev.com/f8f6ed59949be4451ee2f5443d8a313f102fde60/third_party/WebKit/LayoutTests/platform/linux/external/wpt/url/url-constructor-expected.txt
[modify] https://crrev.com/f8f6ed59949be4451ee2f5443d8a313f102fde60/third_party/WebKit/LayoutTests/platform/linux/external/wpt/url/url-setters-expected.txt
[modify] https://crrev.com/f8f6ed59949be4451ee2f5443d8a313f102fde60/third_party/WebKit/LayoutTests/platform/linux/fast/url/file-expected.txt
[modify] https://crrev.com/f8f6ed59949be4451ee2f5443d8a313f102fde60/third_party/WebKit/LayoutTests/platform/linux/fast/url/file-http-base-expected.txt
[modify] https://crrev.com/f8f6ed59949be4451ee2f5443d8a313f102fde60/third_party/WebKit/LayoutTests/platform/linux/fast/url/segments-expected.txt
[modify] https://crrev.com/f8f6ed59949be4451ee2f5443d8a313f102fde60/third_party/WebKit/LayoutTests/platform/linux/fast/url/standard-url-expected.txt
[modify] https://crrev.com/f8f6ed59949be4451ee2f5443d8a313f102fde60/third_party/WebKit/LayoutTests/platform/mac/external/wpt/url/a-element-expected.txt
[modify] https://crrev.com/f8f6ed59949be4451ee2f5443d8a313f102fde60/third_party/WebKit/LayoutTests/platform/mac/external/wpt/url/a-element-xhtml-expected.txt
[modify] https://crrev.com/f8f6ed59949be4451ee2f5443d8a313f102fde60/third_party/WebKit/LayoutTests/platform/mac/external/wpt/url/url-constructor-expected.txt
[modify] https://crrev.com/f8f6ed59949be4451ee2f5443d8a313f102fde60/third_party/WebKit/LayoutTests/platform/mac/external/wpt/url/url-setters-expected.txt
[modify] https://crrev.com/f8f6ed59949be4451ee2f5443d8a313f102fde60/third_party/WebKit/LayoutTests/platform/mac/fast/url/file-expected.txt
[modify] https://crrev.com/f8f6ed59949be4451ee2f5443d8a313f102fde60/third_party/WebKit/LayoutTests/platform/mac/fast/url/standard-url-expected.txt
[modify] https://crrev.com/f8f6ed59949be4451ee2f5443d8a313f102fde60/third_party/WebKit/LayoutTests/platform/win/external/wpt/url/a-element-expected.txt
[modify] https://crrev.com/f8f6ed59949be4451ee2f5443d8a313f102fde60/third_party/WebKit/LayoutTests/platform/win/external/wpt/url/a-element-xhtml-expected.txt
[modify] https://crrev.com/f8f6ed59949be4451ee2f5443d8a313f102fde60/third_party/WebKit/LayoutTests/platform/win/external/wpt/url/url-constructor-expected.txt
[modify] https://crrev.com/f8f6ed59949be4451ee2f5443d8a313f102fde60/third_party/WebKit/LayoutTests/platform/win/fast/url/file-expected.txt
[modify] https://crrev.com/f8f6ed59949be4451ee2f5443d8a313f102fde60/third_party/WebKit/LayoutTests/platform/win/fast/url/file-http-base-expected.txt
[modify] https://crrev.com/f8f6ed59949be4451ee2f5443d8a313f102fde60/third_party/WebKit/LayoutTests/platform/win/fast/url/segments-expected.txt
[modify] https://crrev.com/f8f6ed59949be4451ee2f5443d8a313f102fde60/third_party/WebKit/LayoutTests/platform/win/fast/url/standard-url-expected.txt
[modify] https://crrev.com/f8f6ed59949be4451ee2f5443d8a313f102fde60/third_party/WebKit/Source/platform/weborigin/KURLTest.cpp
[modify] https://crrev.com/f8f6ed59949be4451ee2f5443d8a313f102fde60/url/url_canon_etc.cc
[modify] https://crrev.com/f8f6ed59949be4451ee2f5443d8a313f102fde60/url/url_canon_unittest.cc


### mk...@chromium.org (2017-10-10)

After some discussion, it looks like there's consensus converging on Firefox's percent-encoding algorithm for fragments. I'm working on getting  https://github.com/whatwg/url/pull/347 and https://github.com/w3c/web-platform-tests/pull/7641 folded in to lock that down, and will adjust Chrome's URL library to follow.

### mm...@chromium.org (2017-11-14)

Mike, it looks like there was some progress on the github issues you mentioned. Are you planning to land any new CLs here?

### pa...@chromium.org (2017-11-29)

mkwst: Friendly ping. :) Is there any more work for this CL? If the work done so far closes the DOM XSS vector, you can close this and file regular bugs for the spec work or other cleanup.

### mk...@chromium.org (2017-12-01)

I'm working through bugs with the patch at https://chromium-review.googlesource.com/c/chromium/src/+/719004 for the last bit of this, and I think other vendors are on board as well. I'll go ping the relevant GitHub issue.

### go...@chromium.org (2017-12-07)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-12-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/01c25d47d2d22456368363e576083d766eedf8f6

commit 01c25d47d2d22456368363e576083d766eedf8f6
Author: Mike West <mkwst@chromium.org>
Date: Tue Dec 12 09:31:00 2017

Encode ' ', '"', '<', '>', and '`' in URL fragments.

Implements the changes to fragment processing described in
https://github.com/whatwg/url/pull/347, which adds a new "fragment
percent-encode set" which contains the C0 control percent-encode set,
along with:

* 0x20 SPACE
* 0x22 (")
* 0x3C (<)
* 0x3E (>)
* 0x60 (`)

This brings our implementation into line with Firefox.

Bug: 758523
Change-Id: I25de642017ccb69473626a327ad194b3431a11ed
Reviewed-on: https://chromium-review.googlesource.com/719004
Commit-Queue: Mike West <mkwst@chromium.org>
Reviewed-by: Jochen Eisinger <jochen@chromium.org>
Cr-Commit-Position: refs/heads/master@{#523383}
[modify] https://crrev.com/01c25d47d2d22456368363e576083d766eedf8f6/third_party/WebKit/LayoutTests/editing/pasteboard/copy-standalone-image-escaping.html
[modify] https://crrev.com/01c25d47d2d22456368363e576083d766eedf8f6/third_party/WebKit/LayoutTests/fast/dom/HTMLAnchorElement/set-href-attribute-hash-expected.txt
[modify] https://crrev.com/01c25d47d2d22456368363e576083d766eedf8f6/third_party/WebKit/LayoutTests/fast/dom/HTMLAnchorElement/set-href-attribute-hash.html
[modify] https://crrev.com/01c25d47d2d22456368363e576083d766eedf8f6/third_party/WebKit/LayoutTests/fast/url/anchor-expected.txt
[modify] https://crrev.com/01c25d47d2d22456368363e576083d766eedf8f6/third_party/WebKit/LayoutTests/fast/url/script-tests/anchor.js
[modify] https://crrev.com/01c25d47d2d22456368363e576083d766eedf8f6/third_party/WebKit/LayoutTests/fast/url/script-tests/segments.js
[modify] https://crrev.com/01c25d47d2d22456368363e576083d766eedf8f6/third_party/WebKit/LayoutTests/fast/url/script-tests/standard-url.js
[modify] https://crrev.com/01c25d47d2d22456368363e576083d766eedf8f6/third_party/WebKit/LayoutTests/http/tests/security/xssAuditor/anchor-url-dom-write-location-expected.txt
[modify] https://crrev.com/01c25d47d2d22456368363e576083d766eedf8f6/third_party/WebKit/LayoutTests/http/tests/security/xssAuditor/anchor-url-dom-write-location2-expected.txt
[modify] https://crrev.com/01c25d47d2d22456368363e576083d766eedf8f6/third_party/WebKit/LayoutTests/platform/linux/external/wpt/url/a-element-expected.txt
[modify] https://crrev.com/01c25d47d2d22456368363e576083d766eedf8f6/third_party/WebKit/LayoutTests/platform/linux/external/wpt/url/a-element-xhtml-expected.txt
[modify] https://crrev.com/01c25d47d2d22456368363e576083d766eedf8f6/third_party/WebKit/LayoutTests/platform/linux/external/wpt/url/url-constructor-expected.txt
[modify] https://crrev.com/01c25d47d2d22456368363e576083d766eedf8f6/third_party/WebKit/LayoutTests/platform/linux/external/wpt/url/url-setters-expected.txt
[modify] https://crrev.com/01c25d47d2d22456368363e576083d766eedf8f6/third_party/WebKit/LayoutTests/platform/linux/fast/url/segments-expected.txt
[modify] https://crrev.com/01c25d47d2d22456368363e576083d766eedf8f6/third_party/WebKit/LayoutTests/platform/linux/fast/url/standard-url-expected.txt
[modify] https://crrev.com/01c25d47d2d22456368363e576083d766eedf8f6/third_party/WebKit/LayoutTests/platform/mac/external/wpt/url/a-element-expected.txt
[modify] https://crrev.com/01c25d47d2d22456368363e576083d766eedf8f6/third_party/WebKit/LayoutTests/platform/mac/external/wpt/url/a-element-xhtml-expected.txt
[modify] https://crrev.com/01c25d47d2d22456368363e576083d766eedf8f6/third_party/WebKit/LayoutTests/platform/mac/external/wpt/url/url-constructor-expected.txt
[modify] https://crrev.com/01c25d47d2d22456368363e576083d766eedf8f6/third_party/WebKit/LayoutTests/platform/mac/external/wpt/url/url-setters-expected.txt
[rename] https://crrev.com/01c25d47d2d22456368363e576083d766eedf8f6/third_party/WebKit/LayoutTests/platform/mac/fast/url/segments-expected.txt
[modify] https://crrev.com/01c25d47d2d22456368363e576083d766eedf8f6/third_party/WebKit/LayoutTests/platform/mac/fast/url/standard-url-expected.txt
[modify] https://crrev.com/01c25d47d2d22456368363e576083d766eedf8f6/third_party/WebKit/LayoutTests/platform/win/external/wpt/url/a-element-expected.txt
[modify] https://crrev.com/01c25d47d2d22456368363e576083d766eedf8f6/third_party/WebKit/LayoutTests/platform/win/external/wpt/url/a-element-xhtml-expected.txt
[modify] https://crrev.com/01c25d47d2d22456368363e576083d766eedf8f6/third_party/WebKit/LayoutTests/platform/win/external/wpt/url/url-constructor-expected.txt
[modify] https://crrev.com/01c25d47d2d22456368363e576083d766eedf8f6/third_party/WebKit/LayoutTests/platform/win/external/wpt/url/url-setters-expected.txt
[modify] https://crrev.com/01c25d47d2d22456368363e576083d766eedf8f6/third_party/WebKit/LayoutTests/platform/win/fast/url/segments-expected.txt
[modify] https://crrev.com/01c25d47d2d22456368363e576083d766eedf8f6/third_party/WebKit/LayoutTests/platform/win/fast/url/standard-url-expected.txt
[modify] https://crrev.com/01c25d47d2d22456368363e576083d766eedf8f6/third_party/WebKit/LayoutTests/platform/win7/fast/url/standard-url-expected.txt
[modify] https://crrev.com/01c25d47d2d22456368363e576083d766eedf8f6/third_party/WebKit/Source/core/exported/WebFrameSerializerTest.cpp
[modify] https://crrev.com/01c25d47d2d22456368363e576083d766eedf8f6/third_party/WebKit/Source/core/frame/LocalFrameView.cpp
[modify] https://crrev.com/01c25d47d2d22456368363e576083d766eedf8f6/url/url_canon_etc.cc
[modify] https://crrev.com/01c25d47d2d22456368363e576083d766eedf8f6/url/url_canon_unittest.cc
[modify] https://crrev.com/01c25d47d2d22456368363e576083d766eedf8f6/url/url_util_unittest.cc


### rb...@chromium.org (2018-01-17)

It looks like we aren't yet actually matching Firefox here.  Since my investigation is part of a GWS web compat effort where I'd like to link to the bug, I've filed a separate public bug: https://crbug.com/chromium/803103

### xz...@chromium.org (2018-01-24)

[Comment Deleted]

### sh...@chromium.org (2018-01-25)

[Empty comment from Monorail migration]

### ri...@chromium.org (2018-01-25)

[Comment Deleted]

### el...@chromium.org (2018-01-25)

[Comment Deleted]

### el...@chromium.org (2018-01-25)

I filed https://bugs.chromium.org/p/chromium/issues/detail?id=806076 for the problem noted in #25/#26 above.

### ri...@chromium.org (2018-01-25)

[Comment Deleted]

### in...@chromium.org (2018-02-14)

Is there any other work remaining here. If not please closed as Fixed. rbyers@, ricardoq@ - ping!

### ri...@chromium.org (2018-02-14)

inferno@, by mistake, I thought that the CL associated in this bug caused a regression. But as elawrence@ pointed out, it was another CL that caused the regression. So, from my part, I wouldn't know whether or not this bug is fixed or not.

### el...@chromium.org (2018-02-15)

This was fixed by #21 and the POC in #0 no longer repros.

### sh...@chromium.org (2018-02-16)

[Empty comment from Monorail migration]

### aw...@google.com (2018-02-19)

[Empty comment from Monorail migration]

### rb...@chromium.org (2018-02-21)

Verified this is actually fixed in Chrome 65 - eg. now passing "http://f:21/ b ? d # e" test case in https://w3c-test.org/url/a-element.html (but fails in Chrome 64).

### aw...@chromium.org (2018-02-26)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-02-26)

Nice one mateusz.krzeszowiec@ - the VRP panel decided to award $500 for this report. A member of our finance team will be in touch to arrange payment. Also, how would you like to be credited in the Chrome release notes? Thanks for the report!

### ma...@gmail.com (2018-02-26)

Thank you! Just regular release notes entry would do. Please pass the award to UNICEF.

### aw...@chromium.org (2018-03-06)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-03-06)

[Empty comment from Monorail migration]

### aw...@google.com (2018-03-07)

Many thanks Mateusz, that's excellent!  I'll get that processed for you now.

### sh...@chromium.org (2018-03-16)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-16)

This bug requires manual review: M66 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), josafat@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cm...@google.com (2018-03-19)

Please verify the fix in the latest canary

### ab...@google.com (2018-03-19)

No merge needed

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-05-25)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@google.com (2018-11-14)

[Empty comment from Monorail migration]

### yu...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-06)

This issue was migrated from crbug.com/chromium/758523?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>DOM, Blink>Network]
[Monorail blocking: crbug.com/chromium/803103]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40088802)*
