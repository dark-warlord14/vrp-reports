# Cross-origin audio leak using Web Audio API

| Field | Value |
|-------|-------|
| **Issue ID** | [40091300](https://issues.chromium.org/issues/40091300) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>WebAudio |
| **Platforms** | iOS |
| **Reporter** | s....@gmail.com |
| **Assignee** | rt...@chromium.org |
| **Created** | 2018-05-04 |
| **Bounty** | $1,000.00 |

## Description

Steps to reproduce the problem:
1. Go to https://vuln.shhnjk.com/ios_leaks.html
2. Play a sound on the left side.
3. Observe that Audio is stolen and playable via sound on the right side.

What is the expected behavior?
Cross-origin audio data should not leak.

What went wrong?
Per spec: https://webaudio.github.io/web-audio-api/#MediaElementAudioSourceOptions-security
"HTMLMediaElement allows the playback of cross-origin resources. Because Web Audio allows inspection of the content of the resource (e.g. using a MediaElementAudioSourceNode, and a ScriptProcessorNode to read the samples), information leakage can occur if scripts from one origin inspect the content of a resource from another origin.

To prevent this, a MediaElementAudioSourceNode MUST output silence instead of the normal output of the HTMLMediaElement if it has been created using an HTMLMediaElement for which the execution of the fetch algorithm labeled the resource as CORS-cross-origin."

But this isn't respected.

Did this work before? N/A 

Chrome version: 66.0.3359.122  Channel: stable
OS Version: 11.3.1
Flash Version: 

I've reported this to Webkit (https://bugs.webkit.org/show_bug.cgi?id=184866) :( What happens in this case?

## Timeline

### ts...@chromium.org (2018-05-07)

[Empty comment from Monorail migration]

[Monorail components: Blink>WebAudio]

### ts...@chromium.org (2018-05-07)

[Empty comment from Monorail migration]

### rt...@chromium.org (2018-05-07)

[Empty comment from Monorail migration]

### s....@gmail.com (2018-05-07)

I don’t think this is a duplicate because:

1. This is a bug in WKWebView.
2. This doesn’t require a redirect.

### rt...@chromium.org (2018-05-07)

Oh, IOS.  That would be a webkit bug, not a Chrome bug because I think Chrome is required to use webkit.

Don't have an IOS device to test this on.

Undup'ing for now.

### sh...@chromium.org (2018-05-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-05-08)

[Empty comment from Monorail migration]

### kb...@chromium.org (2018-05-09)

Sorry, I can't own this.


### rt...@chromium.org (2018-05-09)

Sorry, I meant to reassign this to me.

### rt...@chromium.org (2018-05-21)

Depends on webkit fixing this for iOS.

### rt...@chromium.org (2018-06-05)

https://trac.webkit.org/changeset/231513/webkit indicates that webkit https://crbug.com/chromium/184866 has been fixed.  Don't know when this will actually roll out to users, but the fix has landed.

Closing this as fixed.

### sh...@chromium.org (2018-06-06)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-06-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-06-12)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-06-12)

This bug requires manual review: M68 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), kariahda@(iOS), bhthompson@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ka...@chromium.org (2018-06-13)

I see sheriffbot added a merge-request. If Apple fixed the webkit issue, do we need any merge? Please remove if not.

### rt...@chromium.org (2018-06-13)

I don't do any development of Chrome on iOS, so I don't really know, but I think there's nothing to do in chrome since the fix is in WebKit.

### aw...@chromium.org (2018-06-15)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2018-06-15)

and $1,000 for this one, too - cheers!

### aw...@chromium.org (2018-06-15)

[Empty comment from Monorail migration]

### ka...@chromium.org (2018-06-15)

Thanks rtoy@. Removing merge request.

### sh...@chromium.org (2018-09-13)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2018-09-13)

This issue was migrated from crbug.com/chromium/839983?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedinto: crbug.com/chromium/826552]
[Monorail components added to Component Tags custom field.]

### dt...@google.com (2025-02-13)

Bulk update of issues accidentally marked as duplicate in issue tracker migration (b/325072672)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091300)*
