# protocol property of URL including specific character doesn't return correct value

| Field | Value |
|-------|-------|
| **Issue ID** | [40093865](https://issues.chromium.org/issues/40093865) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>HTML, Internals>Core |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ma...@gmail.com |
| **Assignee** | cs...@chromium.org |
| **Created** | 2019-01-26 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.4 Safari/537.36

Steps to reproduce the problem:
If an anchor element has the URL including one of U+FDD0 ~ U+FDEF, U+FFFE or U+FFFF character in the `href` attribute, the protocol property does not return the correct value.
You can check the behavior from this code:

a = document.createElement('a');
a.href = 'javascript:alert(1)//\uFFFF';
alert(a.protocol) // === ":"

This behavior can be abused to do XSS attacks by bypassing the protocol check.

For example, the following code checks if the specified URL by users is safe but the check can be bypassed and JavaScript can be executed since Chrome does not return the correct value. 

<script>
userInput = "javascript:alert(1)//\uFFFF";
a = document.createElement('a');
a.href = userInput;

//Check if the specified protocol is safe
if (a.protocol !== 'javascript:') {
    location = a.href;
}
</script>

I attached this HTML file.
FYI, if you use `location = userInput` instead of `location = a.href`, the redirect does not work due to the following error:

Uncaught DOMException: Failed to set the 'href' property on 'Location': 'javascript:alert(1)//￿' is not a valid URL.

What is the expected behavior?
Chrome should return "javascript:".

What went wrong?
Chrome returns ":".

Did this work before? N/A 

Chrome version: 73.0.3683.4  Channel: canary
OS Version: 10.0
Flash Version:

## Attachments

- [protocol_check_bypass.html](attachments/protocol_check_bypass.html) (text/plain, 227 B)

## Timeline

### li...@chromium.org (2019-01-27)

Setting severity to medium because it's somewhat limited in scope needing to use one of the listed characters, but still enables XSS. kinuko@, would you be able to help take a look or help us find someone who can? Thanks!

[Monorail components: Blink>HTML]

### sh...@chromium.org (2019-01-28)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-01-28)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-01-30)

[Empty comment from Monorail migration]

### ki...@chromium.org (2019-02-05)

This doesn't look like a regression, the related code hasn't been changed much recently and this exists at least from M71 (just tested).  Though it still should be fixed as quickly as possible.  Removing Stable blocker for now, please put the label back if anyone disagrees.

The string gets passed to StripLeadingAndTrailingHTMLSpaces, and then passed to GURL's url parser, so either could be doing something unexpected.

Adding some members from HTML and security teams. 

Nasko: tentatively assigning this to you, is this something you can triage?  If not I can take a further look tomorrow but won't be today (in JST).

### sh...@chromium.org (2019-02-05)

[Empty comment from Monorail migration]

### na...@chromium.org (2019-02-08)

Adding some of the owners of //url/ who hopefully have a bit more knowledge than myself in GURL internals.

Hey palmer@, I hear you like URL parsers ;).

### cs...@chromium.org (2019-02-11)

The problem is that this URL is invalid, so we intentionally strip out this information. Here's the spec text:
https://html.spec.whatwg.org/multipage/links.html#dom-hyperlink-protocol

### pa...@chromium.org (2019-02-11)

Nasko: "Like" is a strong word

### pa...@chromium.org (2019-02-12)

#8: It's not obvious to me from that spec text that Chrome is doing the right thing. The URL is invalid, but not null. Firefox 65 returns "javascript:", FWIW.

### cs...@chromium.org (2019-02-12)

I think an invalid URL is supposed to be set to null in the "reinitialise-url" algorithm:
https://html.spec.whatwg.org/multipage/links.html#concept-hyperlink-url-set

I could be wrong, that's just my reading. That isn't to say we shouldn't fix this if the behavior is undesired :)

### sh...@chromium.org (2019-02-22)

nasko: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-03-09)

nasko: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-03-13)

[Empty comment from Monorail migration]

### li...@chromium.org (2019-03-28)

Friendly security sheriff ping. Is there any movement on this bug? Thanks for your help!

### na...@chromium.org (2019-04-02)

Unfortunately I won't be able to look at this myself in the near future.

csharrison@ or palmer@, would one of you be able to pick this up or potentially delegate to someone that can take it on?

### cs...@chromium.org (2019-04-03)

+domenic

I dug into this a bit more. I think this is a combination of the "set the url" issues + URL parser differences across browsers. For instance, a URL that most browsers agree is invalid is "https://host\0.com/path". Firefox still shows the protocol even for invalid URLs, but neither Safari nor Chrome do.

var a = document.createElement('a');
a.href = "https://host\0.com/path"
Chrome + Safari:
a.protocol -> ":"
a.host -> ""
a.path -> ""

Firefox:
a.protocol -> "https:"
a.host -> ""
a.path -> ""

Further: Firefox just returns "http" for invalid URLs:
a.href= "h\0://a.com"
a.protocol -> "http:"

https://dxr.mozilla.org/mozilla-central/source/dom/base/Link.cpp#580

This issue with "javascript:alert(1)//\uFFFF" is that neither FF nor Safari consider it an invalid URL, but Chrome does (I checked using the URL constructor). I'm not familiar enough with the parser spec to know if Chrome is in the wrong here.

### na...@chromium.org (2019-04-03)

csharrison@, I'm sending this over to you, as you have much more context and knowledge in this area.

### do...@chromium.org (2019-04-03)

Let's keep in mind that "invalid URLs" is a term for authoring tools (e.g. validators), not web browsers. https://url.spec.whatwg.org/#writing explains this in more detail.

As for how the URL in question should be parsed, you can use https://jsdom.github.io/whatwg-url/ to explore that. (However, it appears it's broken when trying to share URLs which contain Unicode characters, so you'll have to use it manually by inputting strings.)

Inputting javascript:alert(1)//￿ into the textbox there gives the result that per spec, we should have .href = 'javascript:alert(1)//%EF%BF%BF', .protocol = 'javascript:', and .pathname = 'alert(1)//%EF%BF%BF'.


that .protocol should be 'javascript:' when given the URL 'javascript:alert(1)//\uFFFF'. You can step-debug through the source code to find out what exact parser steps this results in.

### cs...@chromium.org (2019-04-03)

Thanks domenic, that live viewer is extremely helpful!

Here's the issue with our parser:
https://cs.chromium.org/chromium/src/url/url_canon_pathurl.cc?rcl=20c2c6baa6d9847db46eca1e0dcfaa3c915ebb92&l=37

For non URL code points we just fail, whereas in the spec at this point there is no failure (just validation errors). I don't have too much institutionalized knowledge in our parser to know what the consequences of relaxing the parser to match the spec. I found at least one crash in our spelling service after applying the patch:
https://chromium-review.googlesource.com/c/chromium/src/+/1551917/

+mkwst, who maybe knows but at least is the longest //url OWNER we have :P

[Monorail components: Internals>Core]

### do...@chromium.org (2019-04-03)

BTW I fixed the viewer so now you can visit https://jsdom.github.io/whatwg-url/#url=amF2YXNjcmlwdDphbGVydCgxKS8v77+/&base=YWJvdXQ6Ymxhbms= to see the URL in question directly, with no inputting into the text box needed.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-04-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/19b1e5e4e1914b5b7464062ec300b817d2bac53d

commit 19b1e5e4e1914b5b7464062ec300b817d2bac53d
Author: Charlie Harrison <csharrison@chromium.org>
Date: Fri Apr 05 13:30:53 2019

[url] Make path URL parsing more lax

Parsing the path component of a non-special URL like javascript or data
should not fail for invalid URL characters like \uFFFF. See this bit
in the spec:
https://url.spec.whatwg.org/#cannot-be-a-base-url-path-state

Note: some failing WPTs are added which are because url parsing
replaces invalid characters (e.g. \uFFFF) with the replacement char
\uFFFD, when that isn't in the spec.

Bug: 925614
Change-Id: I450495bfdfa68dc70334ebed16a3ecc0d5737e88
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1551917
Reviewed-by: Mike West <mkwst@chromium.org>
Commit-Queue: Charlie Harrison <csharrison@chromium.org>
Cr-Commit-Position: refs/heads/master@{#648155}
[modify] https://crrev.com/19b1e5e4e1914b5b7464062ec300b817d2bac53d/third_party/blink/web_tests/external/wpt/url/resources/urltestdata.json
[modify] https://crrev.com/19b1e5e4e1914b5b7464062ec300b817d2bac53d/third_party/blink/web_tests/platform/linux/external/wpt/url/a-element-expected.txt
[modify] https://crrev.com/19b1e5e4e1914b5b7464062ec300b817d2bac53d/third_party/blink/web_tests/platform/linux/external/wpt/url/a-element-origin-expected.txt
[modify] https://crrev.com/19b1e5e4e1914b5b7464062ec300b817d2bac53d/third_party/blink/web_tests/platform/linux/external/wpt/url/a-element-origin-xhtml-expected.txt
[modify] https://crrev.com/19b1e5e4e1914b5b7464062ec300b817d2bac53d/third_party/blink/web_tests/platform/linux/external/wpt/url/a-element-xhtml-expected.txt
[modify] https://crrev.com/19b1e5e4e1914b5b7464062ec300b817d2bac53d/third_party/blink/web_tests/platform/linux/external/wpt/url/url-constructor-expected.txt
[modify] https://crrev.com/19b1e5e4e1914b5b7464062ec300b817d2bac53d/third_party/blink/web_tests/platform/linux/external/wpt/url/url-origin-expected.txt
[modify] https://crrev.com/19b1e5e4e1914b5b7464062ec300b817d2bac53d/third_party/blink/web_tests/platform/mac/external/wpt/url/a-element-expected.txt
[modify] https://crrev.com/19b1e5e4e1914b5b7464062ec300b817d2bac53d/third_party/blink/web_tests/platform/mac/external/wpt/url/a-element-origin-expected.txt
[modify] https://crrev.com/19b1e5e4e1914b5b7464062ec300b817d2bac53d/third_party/blink/web_tests/platform/mac/external/wpt/url/a-element-origin-xhtml-expected.txt
[modify] https://crrev.com/19b1e5e4e1914b5b7464062ec300b817d2bac53d/third_party/blink/web_tests/platform/mac/external/wpt/url/a-element-xhtml-expected.txt
[modify] https://crrev.com/19b1e5e4e1914b5b7464062ec300b817d2bac53d/third_party/blink/web_tests/platform/mac/external/wpt/url/url-constructor-expected.txt
[modify] https://crrev.com/19b1e5e4e1914b5b7464062ec300b817d2bac53d/third_party/blink/web_tests/platform/mac/external/wpt/url/url-origin-expected.txt
[modify] https://crrev.com/19b1e5e4e1914b5b7464062ec300b817d2bac53d/third_party/blink/web_tests/platform/win/external/wpt/url/a-element-expected.txt
[modify] https://crrev.com/19b1e5e4e1914b5b7464062ec300b817d2bac53d/third_party/blink/web_tests/platform/win/external/wpt/url/a-element-origin-expected.txt
[modify] https://crrev.com/19b1e5e4e1914b5b7464062ec300b817d2bac53d/third_party/blink/web_tests/platform/win/external/wpt/url/a-element-origin-xhtml-expected.txt
[modify] https://crrev.com/19b1e5e4e1914b5b7464062ec300b817d2bac53d/third_party/blink/web_tests/platform/win/external/wpt/url/a-element-xhtml-expected.txt
[modify] https://crrev.com/19b1e5e4e1914b5b7464062ec300b817d2bac53d/third_party/blink/web_tests/platform/win/external/wpt/url/url-constructor-expected.txt
[modify] https://crrev.com/19b1e5e4e1914b5b7464062ec300b817d2bac53d/third_party/blink/web_tests/platform/win/external/wpt/url/url-origin-expected.txt
[modify] https://crrev.com/19b1e5e4e1914b5b7464062ec300b817d2bac53d/url/url_canon_pathurl.cc
[modify] https://crrev.com/19b1e5e4e1914b5b7464062ec300b817d2bac53d/url/url_canon_unittest.cc


### cs...@chromium.org (2019-04-05)

OK should be fixed. Invalid chars in the path portion of javascript: URLs should not produce invalid GURLs / KURLs.

### sh...@chromium.org (2019-04-05)

[Empty comment from Monorail migration]

### na...@google.com (2019-04-10)

[Empty comment from Monorail migration]

### na...@google.com (2019-04-10)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### na...@google.com (2019-04-10)

Congrats! The Panel decided to reward $500 for this report! 

### na...@google.com (2019-04-10)

[Empty comment from Monorail migration]

### aw...@google.com (2019-04-18)

[Empty comment from Monorail migration]

### aw...@google.com (2019-06-04)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-06-04)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-06-27)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-07-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### yu...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/925614?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>HTML, Internals>Core]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093865)*
