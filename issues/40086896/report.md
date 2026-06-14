# Security: Chrome extension is disabled by crafted chrome-extension:// URL

| Field | Value |
|-------|-------|
| **Issue ID** | [40086896](https://issues.chromium.org/issues/40086896) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Platform>Extensions |
| **Platforms** | Windows |
| **Reporter** | ma...@gmail.com |
| **Assignee** | la...@chromium.org |
| **Created** | 2017-02-25 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

If you put a `.` to the end of `chrome-extension://` resource's pathname, the extension is disabled.  

For example: `chrome-extension://[extensions]/background.html.`

Navigting from the web origin to chrome-extension:// URL is restricted but if the target extension's manifest.json has the `"web_accessible_resources": [ "\*" ]` (or ["path/\*"] ), a remote attacker can navigate and disable the target user's extension.

Also, an attacker can use <https://crbug.com/chromium/696200> in combination. In this case, the user interaction is needed but the `web_accessible_resources` is not needed.

Note that it reproduces on only Windows.

Steps to Reproduce:

1. Install Google Input Tools from <https://chrome.google.com/webstore/detail/google-input-tools/mclkkofklkfljcocdinagocijmpgbhab> .

(This extension has `"web_accessible_resources": ["\*"]`. So I use it as an example.)

2. Go to <https://vulnerabledoma.in/chrome_disable_extension_bug.html> .
3. After visiting the URL, the extension is disabled and chrome://extensions/ page shows this message: `This extension may have been corrupted.`

**VERSION**  

Windows 8.1 Chrome 58.0.3023.0（Official Build）canary

## Timeline

### in...@chromium.org (2017-02-25)

Mustafa, can you please help with an owner.

[Monorail components: Platform>Extensions]

### sh...@chromium.org (2017-02-26)

[Empty comment from Monorail migration]

### me...@chromium.org (2017-02-28)

masatokinugawa@: Thanks for the report!

Very odd bug, I can reproduce on stable. Probably something to do with extension content verification. It repros on Windows but not Linux. It also looks like a DOS rather than a vulnerability, but I'm keeping it as a security bug for now and downgrading to severity-low.

Devlin: Can you please take a look or reassign?

### ma...@gmail.com (2018-06-06)

Hi, it seems that this bug is not touched for a long time. I confirmed that latest Chrome still has this bug.

Btw, I'm a pentester. Recently I tested WebExtension based VPN application. And I noticed that this bug is a serious problem for VPN users because an attacker can downgrade to untrusted connection by disabling VPN extension.

Since extension is used for important purpose nowadays, I think this bug should be fixed as soon as possible.
Thanks!

### rd...@chromium.org (2018-06-07)

Sorry for the delay on this; agreed that it should be prioritized.

lazyboy@ or proberge@, can one of you investigate, since this is content-verification related?

### rd...@chromium.org (2018-06-07)

[Empty comment from Monorail migration]

### la...@chromium.org (2018-06-13)

Yes, it seems like windows specific filename handling issue, using "option.html." or "option.html/" or "option.html\", all seems to repro. Will take a look.

### la...@chromium.org (2018-06-13)

So far, the root cause seems base::PathExists("....option.html.") returns true on windows. This is what we use to determine whether verification should treat a request as missing file or not [1].

[1] See https://cs.chromium.org/chromium/src/extensions/browser/content_hash_reader.cc, ContentHashReader::Create

### bu...@chromium.org (2018-06-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/c74cbd497c4cbed9ea7b99cc411151b4da5059c3

commit c74cbd497c4cbed9ea7b99cc411151b4da5059c3
Author: Istiaque Ahmed <lazyboy@chromium.org>
Date: Thu Jun 28 20:57:30 2018

Ignore dot/space filename suffix(es) on win for verified_contents.

Turns out base:: file operations (PathExists/ReadFileToString, etc)
do not distinguish files "foo" vs "foo." or "foo ". In general
foo(\.|\ )+ would be treated the same as foo. This CL makes
verified_content's tree hash code aware of this.
Move existing content_verifier unittest under simple/ sub-directory
and add test coverage for change in this CL under dot_space_suffix/
sub-directory.

Bug: 696208
Change-Id: I63bcee5500385645f32d88a64cb053d8f852eca7
Reviewed-on: https://chromium-review.googlesource.com/1116349
Commit-Queue: Istiaque Ahmed <lazyboy@chromium.org>
Reviewed-by: Devlin <rdevlin.cronin@chromium.org>
Cr-Commit-Position: refs/heads/master@{#571252}
[modify] https://crrev.com/c74cbd497c4cbed9ea7b99cc411151b4da5059c3/extensions/browser/verified_contents.cc
[modify] https://crrev.com/c74cbd497c4cbed9ea7b99cc411151b4da5059c3/extensions/browser/verified_contents.h
[modify] https://crrev.com/c74cbd497c4cbed9ea7b99cc411151b4da5059c3/extensions/browser/verified_contents_unittest.cc
[add] https://crrev.com/c74cbd497c4cbed9ea7b99cc411151b4da5059c3/extensions/test/data/content_verifier/dot_space_suffix/README
[add] https://crrev.com/c74cbd497c4cbed9ea7b99cc411151b4da5059c3/extensions/test/data/content_verifier/dot_space_suffix/background.js
[add] https://crrev.com/c74cbd497c4cbed9ea7b99cc411151b4da5059c3/extensions/test/data/content_verifier/dot_space_suffix/gen/mixedCase.html
[add] https://crrev.com/c74cbd497c4cbed9ea7b99cc411151b4da5059c3/extensions/test/data/content_verifier/dot_space_suffix/gen/payload.json
[copy] https://crrev.com/c74cbd497c4cbed9ea7b99cc411151b4da5059c3/extensions/test/data/content_verifier/dot_space_suffix/gen/private_key.pem
[add] https://crrev.com/c74cbd497c4cbed9ea7b99cc411151b4da5059c3/extensions/test/data/content_verifier/dot_space_suffix/manifest.json
[add] https://crrev.com/c74cbd497c4cbed9ea7b99cc411151b4da5059c3/extensions/test/data/content_verifier/dot_space_suffix/mixedcase.html
[copy] https://crrev.com/c74cbd497c4cbed9ea7b99cc411151b4da5059c3/extensions/test/data/content_verifier/dot_space_suffix/public_key.pem
[add] https://crrev.com/c74cbd497c4cbed9ea7b99cc411151b4da5059c3/extensions/test/data/content_verifier/dot_space_suffix/verified_contents.json
[rename] https://crrev.com/c74cbd497c4cbed9ea7b99cc411151b4da5059c3/extensions/test/data/content_verifier/simple/README
[rename] https://crrev.com/c74cbd497c4cbed9ea7b99cc411151b4da5059c3/extensions/test/data/content_verifier/simple/payload.json
[rename] https://crrev.com/c74cbd497c4cbed9ea7b99cc411151b4da5059c3/extensions/test/data/content_verifier/simple/private_key.pem
[rename] https://crrev.com/c74cbd497c4cbed9ea7b99cc411151b4da5059c3/extensions/test/data/content_verifier/simple/public_key.pem
[rename] https://crrev.com/c74cbd497c4cbed9ea7b99cc411151b4da5059c3/extensions/test/data/content_verifier/simple/verified_contents.json
[rename] https://crrev.com/c74cbd497c4cbed9ea7b99cc411151b4da5059c3/extensions/test/data/content_verifier/simple/verified_contents_base64.json


### mm...@chromium.org (2019-04-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-09-11)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-10-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/c37c0ee5ba4de1f5ed71b40d4868f1931ed54e4d

commit c37c0ee5ba4de1f5ed71b40d4868f1931ed54e4d
Author: Istiaque Ahmed <lazyboy@chromium.org>
Date: Wed Oct 16 17:09:10 2019

Content Verification: Make computed hashes aware of dot/space suffix treatment.

On windows, filename with (.| )+ suffix is ignored, i.e. "foo.html."
and "foo.html" are treated the same.

VerifiedContents is already aware of this and it stores a
canonicalized version of filename for filenames containing (.| )+
suffix.
This CL makes ComputedHashes aware of the change too, so that searching
for hashes will consider canonicalized version of the filename as
candidate. This makes ComputedHashes::Reader and VerifiedContents treat
this suffix behavior consistently.

This CL also adds unittest and browsertest for the fix.

Bug: 696208
Test: See bug for test repro.
Change-Id: I7c59add5c035815673259ef1f995c7b9ed01a75b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1772643
Commit-Queue: Istiaque Ahmed <lazyboy@chromium.org>
Reviewed-by: Devlin <rdevlin.cronin@chromium.org>
Cr-Commit-Position: refs/heads/master@{#706493}

[modify] https://crrev.com/c37c0ee5ba4de1f5ed71b40d4868f1931ed54e4d/chrome/browser/extensions/content_verifier_browsertest.cc
[modify] https://crrev.com/c37c0ee5ba4de1f5ed71b40d4868f1931ed54e4d/extensions/browser/BUILD.gn
[modify] https://crrev.com/c37c0ee5ba4de1f5ed71b40d4868f1931ed54e4d/extensions/browser/computed_hashes.cc
[modify] https://crrev.com/c37c0ee5ba4de1f5ed71b40d4868f1931ed54e4d/extensions/browser/computed_hashes_unittest.cc
[add] https://crrev.com/c37c0ee5ba4de1f5ed71b40d4868f1931ed54e4d/extensions/browser/content_verifier/content_verifier_utils.cc
[add] https://crrev.com/c37c0ee5ba4de1f5ed71b40d4868f1931ed54e4d/extensions/browser/content_verifier/content_verifier_utils.h
[modify] https://crrev.com/c37c0ee5ba4de1f5ed71b40d4868f1931ed54e4d/extensions/browser/verified_contents.cc


### la...@chromium.org (2019-10-16)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-17)

[Empty comment from Monorail migration]

### la...@chromium.org (2019-10-17)

[Empty comment from Monorail migration]

### na...@google.com (2019-10-21)

[Empty comment from Monorail migration]

### na...@google.com (2019-10-23)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-10-23)

Congrats! The Panel decided to award $500 for this report :) 

### na...@google.com (2019-10-28)

[Empty comment from Monorail migration]

### ad...@google.com (2019-12-05)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-12-06)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-12-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2020-01-23)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### yu...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/696208?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/988936]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086896)*
