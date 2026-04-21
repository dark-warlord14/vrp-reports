# Security: Sanitizer API bypass via prototype pollution

| Field | Value |
|-------|-------|
| **Issue ID** | [40059102](https://issues.chromium.org/issues/40059102) |
| **Status** | Fixed |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>SecurityFeature>SanitizerAPI |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | mi...@bentkowski.info |
| **Assignee** | vo...@chromium.org |
| **Created** | 2022-03-15 |
| **Bounty** | $1,000.00 |

## Description

Hey!

Client-side prototype pollution seems to me a more common issues that we might have previously assumed (check: https://blog.s1r1us.ninja/research/PP). I decided to check whether prototype pollution can be abused to bypass Sanitizer API. Turns out it can! 

Here's a proof of concept:

	<!doctype html>
	<script>
	// We're simulating prototype pollution here
	Object.prototype.allowElements = ['svg:svg', 'svg:use'];
	</script>
	<body>
	<script>

	// We assume that this is the original JavaScript of a website
	const s = new Sanitizer({});
	const sanitized = s.sanitizeFor("div", `<svg><use href="data:image/svg+xml;base64,PHN2ZyBpZD0neCcgeG1sbnM9J2h0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnJyB4bWxuczp4bGluaz0naHR0cDovL3d3dy53My5vcmcvMTk5OS94bGluaycgd2lkdGg9JzEwMCcgaGVpZ2h0PScxMDAnPgo8aW1hZ2UgaHJlZj0iMSIgb25lcnJvcj0iYWxlcnQoMSkiIC8+Cjwvc3ZnPg==#x" /></svg>`);
	document.body.replaceChildren(sanitized); // alert executes!

	</script>


Please note that the issue doesn't happen if no parameter is passed to the constructor (that is: "new Sanitizer()").

However, when the configuration object is passed to the constructor (as in: "new Sanitizer({})") then the prototype chain is traversed, and it can affect the sanitization. In the proof-of-concept I'm adding <svg> and <use> to list of allowed elements and execute my own javascript.

I am not sure, whether the mere fact that it is possible to configure the Sanitizer API in such a way that it allows to execute own javascript should be tracked as another bug (in other words: I don't know if we're letting users shoot themselves in the foot or not).

Chromium version: 101.0.4945.0 (with #enable-experimental-web-platform-features)


## Timeline

### [Deleted User] (2022-03-15)

[Empty comment from Monorail migration]

### ma...@chromium.org (2022-03-17)

Security_Impact-None as this requires #enable-experimental-web-platform-features flag.
Assuming it affects all blink platforms.


[Monorail components: Blink>SecurityFeature>SanitizerAPI]

### ma...@chromium.org (2022-03-17)

Medium severity since I assume this would require some other vulnerability in any affected websites that allows polluting the prototypes in the first place?
Assigning/cc based on OWNERS.

### vo...@chromium.org (2022-03-18)

Thank you for the report! I'll take a look.

I'm a little confused what happens, because so far the Sanitizer shouldn't support namespaced content at all; and when it does with the testing flag --enable-features=SanitizerAPINamespacesForTesting  it shouldn't support the use element. Clearly, something isn't working as intended...

### vo...@chromium.org (2022-03-18)

[still tentative]

I think the first bug is that - when introducing namespaced elements - I messed up the check of whether an element is 'regular' or 'unknown', with the result that all namespaced stuff - whether enabled or not - gets classified as 'unknown', and thus isn't checked against the baseline. That's pretty embarrasing. When I fix that, the example in https://crbug.com/chromium/1306450#c0 no longer works, although the general point of the report makes still stands.

<svg:use> is neither in the current nor in the svg-supporting baseline, and hence should not pass the Sanitizer. (... unless the spec at some point decides on something different.)

The second issue - where I'm not sure yet whether that's a bug or not - is that polluting the prototype indeed allows to sneak in an allow-list via Object.prototype. My gut feeling is that this is an instance of JavaScript being weird, but... I'm not sure.

### vo...@chromium.org (2022-03-18)

@koto, mkwst: I'd like a second opinion, please. Is this a bug, or is this JavaScript being JavaScript? (I do believe this is spec conforming.)

Object.prototype.allowElements = ["abc"];
new Sanitizer({}).getConfiguration().allowElements // ["abc"]

---
@Michal: Is it okay if I discuss this with Sanitizer API spec editors / contributors?
(Sometimes, bug reporters prefer to make seperate submissions to different browsers, in which case this would give it away.)

### mi...@bentkowski.info (2022-03-18)

@vogelheim, I reported this only to Chromium.  Feel free to discuss it with spec authors. 



### ko...@google.com (2022-03-18)

I don't personally think that this the prototype pollution vector should be something to address in the Sanitizer API itself. WebIDL is clear that the ES object prototype chain should be followed for dictionary type: https://webidl.spec.whatwg.org/#es-dictionary. If we wanted to address this, this should happen at WebIDL level (perhaps via a new extended attribute). 

I don't think we should address it though - environments that have their Object prototypes polluted, are already compromised, and I don't think selectively hardening chosen web APIs against that would offer much practical benefit, and it may only offer a false sense of security, at the expense of API cognitive complexity. There will always be prototype pollution gadgets in all of Web APIs and libraries. Applications should make sure to identify and remove all gadgets that pollute prototypes from user controlled sources, instead of expecting the web APIs to be resilient. 


### gi...@appspot.gserviceaccount.com (2022-03-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/0371f0b9cac60bb9bfcd36d3e1c6ed33e946a9e1

commit 0371f0b9cac60bb9bfcd36d3e1c6ed33e946a9e1
Author: Daniel Vogelheim <vogelheim@chromium.org>
Date: Wed Mar 23 13:40:45 2022

[Sanitizer API] Fix classification of namespaced elements.

The current code treats all namespaces elements as unknown HTML elements,
while they're not unknown HTML elements at all. (This is a regression from
the introduction of namespaces to the Sanitizer.)

Bug: 1306450
Change-Id: Ie65f84350ef5d9be2d5d6f3a626a248f33fae355
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3537127
Reviewed-by: Yifan Luo <lyf@chromium.org>
Commit-Queue: Daniel Vogelheim <vogelheim@chromium.org>
Cr-Commit-Position: refs/heads/main@{#984301}

[modify] https://crrev.com/0371f0b9cac60bb9bfcd36d3e1c6ed33e946a9e1/third_party/blink/web_tests/external/wpt/sanitizer-api/support/testcases.sub.js
[modify] https://crrev.com/0371f0b9cac60bb9bfcd36d3e1c6ed33e946a9e1/third_party/blink/renderer/modules/sanitizer_api/sanitizer.cc
[modify] https://crrev.com/0371f0b9cac60bb9bfcd36d3e1c6ed33e946a9e1/third_party/blink/web_tests/TestExpectations
[add] https://crrev.com/0371f0b9cac60bb9bfcd36d3e1c6ed33e946a9e1/third_party/blink/web_tests/FlagExpectations/enable-features=SanitizerAPINamespacesForTesting


### mi...@bentkowski.info (2022-04-15)

After some thinking I believe I agree with @koto. I was actually a little bit surprised to find out that you can pollute the prototype for other web APIs. So probably Sanitizer API should behave the same. 

So the only real bug here was the ability to add <svg:use> to the allow list.

### th...@chromium.org (2022-06-09)

Security marshal here. vogelheim@, if there isn't anything more to do on this ticket, could you close it out?

### vo...@chromium.org (2022-06-09)

https://crbug.com/chromium/1306450#c11: Thanks for the reminder. I think I can close it.

The svg:use issue that was raised has been fixed. (#c9)

The prototype pollution issue is working as intended and spec'd, and this behaviour is mandated by WebIDL + Javascript. From that perspective, it's not a security issue, although it's certainly ... surprising.

### [Deleted User] (2022-06-09)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-09)

[Empty comment from Monorail migration]

### am...@google.com (2022-06-29)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-06-29)

Congratulations, Michal! The VRP Panel has decided to award you $1,000 for this report. This was an odd one, but in the end it did help us to find a different, other bug that we needed to resolve. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2022-07-01)

[Empty comment from Monorail migration]

### ko...@google.com (2022-07-18)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-15)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2022-09-15)

This issue was migrated from crbug.com/chromium/1306450?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059102)*
