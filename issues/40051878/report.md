# Security: Copy & paste XSS via noscript

| Field | Value |
|-------|-------|
| **Issue ID** | [40051878](https://issues.chromium.org/issues/40051878) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Editing, Blink>SVG |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | mi...@bentkowski.info |
| **Assignee** | xi...@chromium.org |
| **Created** | 2020-03-30 |
| **Bounty** | $5,000.00 |

## Description

In https://bugs.chromium.org/p/chromium/issues/detail?id=1040755#c55, Michal reports the following:

====

Hey, not sure if this should be reported as new bug but I've found a bypass to the fix. I feel kinda bad about it since the bypass was introduced by fix to other bug I reported (https://crbug.com/chromium/1017871) and it is really similar to bug I've reported to WebKit (https://trac.webkit.org/changeset/254800/webkit) so I feel I should've caught it earlier.

Here's the bypass:

    <noscript><u title="</noscript><div contenteditable=false>
    <svg style=position:fixed;left:0;top:0;width:100%;height:100%>
    <use href=data:application/xml;base64,PHN2ZyBpZD0neCcgeG1sbnM9J2h0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnJz4KPGEgaHJlZj0namF2YXNjcmlwdDphbGVydCgxMjMpJz4KICAgIDxyZWN0IHdpZHRoPScxMDAlJyBoZWlnaHQ9JzEwMCUnIGZpbGw9J2xpZ2h0Ymx1ZScgLz4KICAgICA8dGV4dCB4PScwJyB5PScwJyBmaWxsPSdibGFjayc+CiAgICAgICA8dHNwYW4geD0nMCcgZHk9JzEuMmVtJz5Pb3BzLCB0aGVyZSdzIHNvbWV0aGluZyB3cm9uZyB3aXRoIHRoZSBwYWdlITwvdHNwYW4+CiAgICAgPHRzcGFuIHg9JzAnIGR5PScxLjJlbSc+UGxlYXNlIGNsaWNrIGhlcmUgdG8gcmVsb2FkLjwvdHNwYW4+Cjwvc3ZnPg==#x>
    "></noscript>asdasd

And here's an explanation why it works:

I've reported https://crbug.com/chromium/1017871 which is about style injection via copy&paste. The bug was resolved by going the Safari way, ie. if there's a <style> element in the pasted content:
  a) a dummy document is created,
  b) style and layout is calculated in the dummy document,
  c) the document is re-serialized as the markup to be inserted.
  
This patch however introduced a subtle issue, which I missed. The document is parsed assuming that scripting is disabled. This impacts parsing of <noscript> element [1], which is parsed differently depending on scripting being disabled or enabled. In a nutshell, if scripting is enabled, <noscript>'s content model is a text; otherwise, it is a transparent element.

The difference can be proved with a simple example. Assume that we put the following HTML to the clipboard:

    a<noscript><u></noscript>b
    
After pasting, we get the following DOM tree:

    #text: "a"
    <NOSCRIPT>
        #text: "<u>"
    #text: "b"

This is expected, since with scripting enabled, <noscript> can contain only text. 

However, when we put the following HTML to the clipboard:

    <style></style>a<noscript><u></noscript>b
    
We'll get a different DOM tree after pasting:

    #text: "a"
    <NOSCRIPT>
        #text: <u></u>
    <U>
        #text: "b"
        
Inclusion of <style> element forced the dummy document to be created, and because it was parsed with scripting disabled, it created a new <u> element.

Moving forward (and closer to the final exploit), let's assume we have the following HTML in clipboard:

    <style></style>a<noscript><u title="</noscript>SOME_INJECTION_HERE"></noscript>b
    
In the dummy document, it creates the following DOM tree:

    #text: "a"
    <NOSCRIPT>
        <U title="</noscript>SOME_INJECTION_HERE"></U>
    <U title="</noscript>SOME_INJECTION_HERE">
        #text: "b"

However, when this document is re-serialized and inserted after pasting, it is parsed differently because the scripting is now enabled, producing the following DOM tree:

    #text: "a"
    <NOSCRIPT>
        #text: "<u title=""
    #text: "SOME_INJECTION_HERE">"
    <U title="</noscript>SOME_INJECTION_HERE">
        #text: "b"

Now the string "SOME_INJECTION_HERE" escapes the title attribute because <noscript> is closed by the </noscript> that immediately precedes the string. The same behaviour was exploited by Masato Kinugawa in his famous XSS in Google Search [2]. So in my bypass, I've just substituted "SOME_INJECTION_HERE" with the same <svg> and <use> trick I've shown in this issue.

I hope the explanation is clear, please let me know if I'm wrong.

[1]: https://html.spec.whatwg.org/multipage/scripting.html#the-noscript-element
[2]: https://www.youtube.com/watch?v=lG7U3fuNw3A

## Timeline

### jd...@chromium.org (2020-03-30)

[Empty comment from Monorail migration]

### [Deleted User] (2020-03-30)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-03-31)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/43bbd38f475b9d9663f1ffabf2fef9fb26466af4

commit 43bbd38f475b9d9663f1ffabf2fef9fb26466af4
Author: Xiaocheng Hu <xiaochengh@chromium.org>
Date: Tue Mar 31 16:47:02 2020

Block copy-and-paste XSS via <noscript>

This patch is analogous to the WebKit patch for a common issue:

https://trac.webkit.org/changeset/254800/webkit

When sanitizing the clipboard markup in a dummy document, we disable
scripting, and parse <noscript> in the script-disabled mode. Then we
parse the sanitized markup in script-enabled mode when inserting it into
the real document. This allows an XSS attack.

This patch introduces a new flag to page settings that allows it to
parse with the scripting flag enabled, while still disabling script
execution. It also renames the |HTMLParserOptions::script_enabled| flag
to |scripting_flag| to improve clarity and match the term in the HTML
spec (https://html.spec.whatwg.org/#scripting-flag).

Bug: 1065761
Change-Id: Ia4bd67a991b354eebd2cbfef6d3291230ddc1f6a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2128839
Reviewed-by: Yoshifumi Inoue <yosin@chromium.org>
Reviewed-by: Kent Tamura <tkent@chromium.org>
Commit-Queue: Xiaocheng Hu <xiaochengh@chromium.org>
Cr-Commit-Position: refs/heads/master@{#754969}

[modify] https://crrev.com/43bbd38f475b9d9663f1ffabf2fef9fb26466af4/third_party/blink/renderer/core/editing/serializers/serialization.cc
[modify] https://crrev.com/43bbd38f475b9d9663f1ffabf2fef9fb26466af4/third_party/blink/renderer/core/frame/settings.h
[modify] https://crrev.com/43bbd38f475b9d9663f1ffabf2fef9fb26466af4/third_party/blink/renderer/core/frame/settings.json5
[modify] https://crrev.com/43bbd38f475b9d9663f1ffabf2fef9fb26466af4/third_party/blink/renderer/core/html/parser/BUILD.gn
[modify] https://crrev.com/43bbd38f475b9d9663f1ffabf2fef9fb26466af4/third_party/blink/renderer/core/html/parser/html_document_parser.cc
[modify] https://crrev.com/43bbd38f475b9d9663f1ffabf2fef9fb26466af4/third_party/blink/renderer/core/html/parser/html_parser_options.cc
[modify] https://crrev.com/43bbd38f475b9d9663f1ffabf2fef9fb26466af4/third_party/blink/renderer/core/html/parser/html_parser_options.h
[modify] https://crrev.com/43bbd38f475b9d9663f1ffabf2fef9fb26466af4/third_party/blink/renderer/core/html/parser/html_preload_scanner_fuzzer.cc
[modify] https://crrev.com/43bbd38f475b9d9663f1ffabf2fef9fb26466af4/third_party/blink/renderer/core/html/parser/html_tokenizer.cc
[modify] https://crrev.com/43bbd38f475b9d9663f1ffabf2fef9fb26466af4/third_party/blink/renderer/core/html/parser/html_tokenizer_fuzzer.cc
[modify] https://crrev.com/43bbd38f475b9d9663f1ffabf2fef9fb26466af4/third_party/blink/renderer/core/html/parser/html_tree_builder.cc
[modify] https://crrev.com/43bbd38f475b9d9663f1ffabf2fef9fb26466af4/third_party/blink/renderer/core/html/parser/html_tree_builder_simulator.cc
[add] https://crrev.com/43bbd38f475b9d9663f1ffabf2fef9fb26466af4/third_party/blink/renderer/core/html/parser/parser_scripting_flag_policy.h
[modify] https://crrev.com/43bbd38f475b9d9663f1ffabf2fef9fb26466af4/third_party/blink/web_tests/editing/pasteboard/paste-svg-use.html


### xi...@chromium.org (2020-04-01)

I can reproduce the issue in M80. 80.0.3987.149 (Official Build) (64-bit)

We should merge the fix to M81.

### [Deleted User] (2020-04-01)

This bug requires manual review: We are only 5 days from stable.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), bindusuvarna@(iOS), geohsu@(ChromeOS), pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### xi...@chromium.org (2020-04-01)

1. Yes
2. https://chromium-review.googlesource.com/c/chromium/src/+/2128839
3. Yes
4. The security issue already exists in M81. We should fix it before it reaches stable
5. No

### pb...@google.com (2020-04-01)

+Adetaylor@(Security TPM) and +benmason@ and +govind@

### go...@chromium.org (2020-04-01)

This can wait for next M81 respin so by then change will be well baked in lower channels as CL listed at #3 just went out to last night canary. Also Security Severity Medium.

adetaylor@, are you ok with it?

### ad...@chromium.org (2020-04-02)

Yes. Let's not put this into the initial M81 drop.

### go...@chromium.org (2020-04-02)

Re #9: Sounds good , thank you.

### [Deleted User] (2020-04-02)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-04-03)

[Empty comment from Monorail migration]

### na...@google.com (2020-04-06)

[Empty comment from Monorail migration]

### na...@google.com (2020-04-08)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-04-08)

Congrats! The Panel decided to award $5,000 for this report. 

### na...@google.com (2020-04-08)

[Empty comment from Monorail migration]

### mi...@bentkowski.info (2020-04-09)

That's great thanks!

### ad...@google.com (2020-04-17)

Adjusting Security_Impact per https://crbug.com/chromium/1065761#c4.

### ad...@google.com (2020-04-17)

This is too complex a fix to pull back into M81. it could have unforeseen user-facing behavior implications, and given it's Medium severity, I'd rather release it organically via M83 to give a full test cycle including as much real user feedback as possible.

### ad...@google.com (2020-05-15)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-05-18)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-05-21)

[Empty comment from Monorail migration]

### [Deleted User] (2020-07-10)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2020-07-10)

This issue was migrated from crbug.com/chromium/1065761?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>Editing, Blink>SVG]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40051878)*
