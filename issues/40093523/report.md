# Security: Two autocomplete flaws together allow sites to invisibly read credit card numbers after a single keypress

| Field | Value |
|-------|-------|
| **Issue ID** | [40093523](https://issues.chromium.org/issues/40093523) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Autofill |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ma...@curative.com |
| **Assignee** | ro...@chromium.org |
| **Created** | 2018-12-20 |
| **Bounty** | $3,337.00 |

## Description

**VULNERABILITY DETAILS**  

Two bugs together allow an attack that steals user card details with minimal user interaction and no indication that there was even a card entry form on the page.

1. When a user hovers over an option in an autocomplete dialog, or selects it with the arrow keys, but has not yet committed their selection to the form by clicking or pressing enter, the selection is previewed in the form (with the form fields given a yellow background), but this selection is not yet supposed to be visible to JavaScript; the .value attribute of those fields returns the empty string until the user clicks or presses enter. However, there is an information leak: even while the form is in this autocomplete preview state, the .scrollWidth property of any textareas being filled by the autocomplete updates to reflect the text.
2. When doing multi-field autocomplete in a card entry form, if, while in the preview state described above, the focused element is removed from the DOM by JavaScript, then the autocomplete dialog vanishes but the preview text remains permanently in the other fields. What's more, by removing the focused element fast enough, it's possible to enter into this state without the autocomplete dialog being visible for a single frame.

These two exploits permit the following attack:

We lure a user to a page which has a card entry form, with autocomplete enabled, and two fields:  

\* A cc-name input, autofocused on page load  

\* A cc-number textarea, styled to have a very narrow width

We make this form invisible to the user (e.g. by covering it up with a `position: fixed` <div>. Using other content on the page (e.g. a game), we socially engineer the user to press either the up or down arrow key. (This is the only user interaction required.)

Since a card details input is focused, the press of the up or down arrow key will immediately select one of the user's cards from their autocomplete, and populate the form fields with the details of that card (theoretically, invisibly to JavaScript). A JavaScript setInterval function running on the page every millisecond detects that this has happened by noticing an increase in the textarea's scrollwidth (thanks to vulnerability 1 above) and immediately removes the cc-name input from the DOM. As noted above, this prevents the autocomplete dialog from ever appearing on the screen, and leaves the user's card number in the textarea (still in the preview state, theoretically invisible to JavaScript).

Next, our JavaScript uses vulnerability 1 above to "read" the card number from the <textarea> with the help of a series of custom fonts using ligatures or kerning. The high-level algorithm looks like this:

\* Let cardnumber be empty string  

\* For each digit i from 0 to 9, generate a font in which all digits except i have no width, but i is very wide. Set the textarea's font to this generated font. Check if the textarea's scroll width is very wide. If it is, break, and let the cardnumber be i  

\* Extension Step: For each of the 20 possible superstrings formed by extending cardnumber by 1 digit:  

\* Generate a font in which every individual digit has no width, but the selected superstring is very wide (e.g. due to a ligature that replaces it with a very wide glyph)  

\* Set the textarea's font to this font  

\* If the textarea is very wide, let cardnumber be the superstring, break from the loop, then run the Extension Step again to add on the next digit

If the extension step terminates without any of our superstrings matching, then cardnumber is now the user's full card number.

**VERSION**  

Probably any that has multifield card autocomplete, but I've tested on these:

Chrome Version: 71.0.3578.98 + stable  

Operating System: Windows and Mac

**REPRODUCTION CASE**  

I've attached two files:

\* opentype.js  

\* demo.html

opentype.js is an MIT-licensed library (not owned by me) for manipulating OpenType fonts, which I use in demo.html

demo.html is a demo page that invites the user to press the down arrow, and, if they do, reads their card number using the approach described above and shows it in an alert.

Note that since card autocomplete only works on HTTPS pages, you will need to serve these over a HTTPS connection in order to see the demo in action.

I have a version of this attack hosted at <https://siodfjawoifjawoi.com/sdoifajegiuawhguiafaoifmeifaw123dsasd.html> that you can try.

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Mark Amery

## Attachments

- [opentype.js](attachments/opentype.js) (text/plain, 443.4 KB)
- [demo.html](attachments/demo.html) (text/plain, 4.1 KB)

## Timeline

### va...@chromium.org (2018-12-20)

[Empty comment from Monorail migration]

[Monorail components: UI>Browser>Autofill]

### va...@chromium.org (2018-12-20)

sebsg@ -- assigning to you for now. If you are not the right owner, please triage it further.

### va...@chromium.org (2018-12-20)

Similar to https://crbug.com/chromium/753645.

### se...@chromium.org (2018-12-20)

[Empty comment from Monorail migration]

### go...@chromium.org (2018-12-20)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-12-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-12-21)

[Empty comment from Monorail migration]

### ro...@chromium.org (2018-12-21)

Confirmed.

Assessiong ...

### sh...@chromium.org (2018-12-21)

[Empty comment from Monorail migration]

### ro...@chromium.org (2018-12-21)

+tkent@

Can we separate the scroll-width property for populated fields vs previewed fields?

A couple of thoughts:

* we can and should clear out the preview data if the drop-down disappears or fails to be shown. Clearing the data on the drop-down disappearing would reduce the duration of the vulnerability, but I don't think it would be eliminated, it would just be racy (?).

* we can consider moving the preview handling over to the browser. This seems like a large and fairly complex move.

Other thoughts?



### ma...@curative.com (2018-12-21)

I'll offer some partial thoughts:

1. I agree that clearing the preview data does not completely fix the vulnerability - especially considering that my demo only takes a few seconds to extract a card number and I have not made any attempt whatsoever to optimise it for speed. I can imagine many ways to reduce the number of custom fonts that the page needs to cycle through, thus making the attack faster.

2. The preview data should still be cleared, though, even if doing so turns out not to help security - leaving it there is a bug and leaves the UI in a broken state when it happens.

3. One mitigation for all autocomplete-based attacks would be to have an absolute minimum duration (of, say, half a second) that the autocomplete dropdown remains open, no matter what, in which the user cannot select a value. This would make attacks like the one I propose here impossible for a page to conceal from the user; it would *also* protect against users against sites just trying to socially-engineer the user into pressing down and enter in quick succession to enter something into an autocomplete field before they can mentally process the sight of the dropdown.

4. I'm not certain that the .scrollWidth property is the only information leak. Other ideas I had, but haven't tested:
* was to somehow construct fonts with ligature glyphs that are crafted to be extremely expensive to render, and somehow detect the performance impact of rendering those glyphs to determine whether the ligature was present
* somehow detect the appearance of the scrollbar

5. A slightly more radical possible fix would be to ignore font-family when styling preview text, and always use a fixed default font for it.

### tk...@chromium.org (2018-12-26)

> Can we separate the scroll-width property for populated fields vs previewed fields?
Yes.  LayoutTextControlSingleLine::ScrollWidth can check the AutofillState of the INPUT element, and return your favorite value.

We should store preview values separate from real values, like placeholder text.  See https://crbug.com/chromium/772433.


### sh...@chromium.org (2019-01-04)

sebsg: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### se...@chromium.org (2019-01-07)

tkent@: I think that's already what we do, no?

I like the idea of a minimum duration for the pop-up. I'll experiment with it to see how it would look like.

### se...@chromium.org (2019-01-07)

+ftirelo@ FYI.

There are 3 ways to trigger Autofill at the moment. For 2 of them, the popup freeze would work. They are the click trigger and typing trigger.

Things get a bit more complicated for the arrow down trigger, as it currently automatically selects the first entry in the dropdown. We would need to change back that behavior.

In the meantime, is there any pushback to using a default font for previews?

### ma...@curative.com (2019-01-07)

The obvious downsides I see of using a default font are:

1. Sites with pretty styling on their payment forms will be made less pretty
2. The appearance of the text will change when the user selects it, which may surprise or confuse the user briefly.

Also, so far we haven't demonstrated that it's necessary to use a default font. The only attack I've built a working demo of can be fixed simply by not updating the .scrollWidth based upon preview text. IF we were confident that was the only information leak available, then it wouldn't make sense to use a default font, since you'd be taking on the UX downsides for no reason.

I'll tinker around this week and see if I can make a demo of my second attack idea (using ligatures that are very expensive to render instead of very wide, and timing their rendering instead of looking at .scrollWidth to figure out whether they're present). If THAT approach also works, then I don't think there'll be any reasonable fix available to you other than using a default font, which basically makes the choice for you. If that approach turns out not to be viable for some reason, then you'll face a tradeoff between getting some defence in depth through using a default font or keeping the UX benefits of letting the font be customised.

### se...@chromium.org (2019-01-07)

I think I misunderstood what tkent@ said. I'll starting looking into that.

In the meantime please keep us updated on if your second attack idea works, mark.amery@

Thanks!

### ft...@chromium.org (2019-01-10)

[Empty comment from Monorail migration]

### ro...@chromium.org (2019-01-10)

After consultation with UX, we can live with using a default system font for the previews.

### ro...@google.com (2019-01-18)

I've implemented this via !important on the preview style

https://chromium-review.googlesource.com/c/chromium/src/+/1423109

It seems to work against the demo code. I did a bit of spelunking to confirm that !mportant annotation set by the User-Agent should supercede those set by the user (HTML/CSS/JS), so this seems like a valid fix.

To verify, I tried adding !important to the font-family style for the injected @font-face at line 64 of demo.html and the exploit didn't resurface, but I'm not sure I was injecting it at the right place.


### ma...@curative.com (2019-01-19)

@rogerm

> To verify, I tried adding !important to the font-family style for the injected @font-face at line 64 of demo.html and the exploit didn't resurface, but I'm not sure I was injecting it at the right place.

You weren't. That's inside a @font-face declaration, where I define a new font family that I refer to later. Adding !important inside a `@font-face` declaration isn't legal and just makes Chrome ignore the entire declaration.

What you really need to do to test this is modify the place where I set the font-family style of the text area to use !important, which is this bit on lines 121-123:

    textarea.style.fontFamily = fontFamilyFromFont(
        fontThatTestsForString(string)
    );

To set the property with priority important, you want to replace those lines with:

    textarea.style.setProperty(
        'font-family',
        fontFamilyFromFont(
            fontThatTestsForString(string)
        ),
        'important'
    );

### ma...@curative.com (2019-01-26)

@rogerm, I'll be interested to hear the results of you retrying your test with the correction I describe above. :)

### ro...@chromium.org (2019-01-28)

Testing with the correction you describe does *not* resurface the vulnerability.

I tried both with 'important' as described as well as with '!important'.

### ma...@curative.com (2019-01-28)

Excellent. Sounds like y'all have got a fix, then.

### ma...@curative.com (2019-02-01)

Still pending (I think) on this ticket is modifying the .scrollWidth property so that it can't be used to extract any information about preview content in a textarea. Either it should return 0 when there's preview text present in the textarea, or throw an error.

### sh...@chromium.org (2019-03-13)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-03-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/0bd10e13a008389ec14bbe7cc95f17d82ea151c1

commit 0bd10e13a008389ec14bbe7cc95f17d82ea151c1
Author: Roger McFarlane <rogerm@chromium.org>
Date: Thu Mar 14 19:50:30 2019

[autofill] Pin preview font-family to a system font

Bug: 916838
Change-Id: I4e874105262f2e15a11a7a18a7afd204e5827400
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1423109
Reviewed-by: Fabio Tirelo <ftirelo@chromium.org>
Reviewed-by: Koji Ishii <kojii@chromium.org>
Commit-Queue: Roger McFarlane <rogerm@chromium.org>
Cr-Commit-Position: refs/heads/master@{#640884}
[modify] https://crrev.com/0bd10e13a008389ec14bbe7cc95f17d82ea151c1/chrome/renderer/autofill/form_autofill_browsertest.cc
[modify] https://crrev.com/0bd10e13a008389ec14bbe7cc95f17d82ea151c1/third_party/blink/renderer/core/html/resources/html.css


### ro...@chromium.org (2019-03-28)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-28)

This bug requires manual review: M74 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: govind@(Android), kariahda@(iOS), dgagnon@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2019-03-28)

 +adetaylor@ (Security TPM) for M74 merge review.

### ab...@google.com (2019-03-28)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-03-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/9e68c4db781b71e9ea772ab60d34c7f10e100b57

commit 9e68c4db781b71e9ea772ab60d34c7f10e100b57
Author: Roger McFarlane <rogerm@chromium.org>
Date: Thu Mar 28 17:58:30 2019

[autofill] Pin preview font-family to a system font

(Merge to M74)

Bug: 916838
Change-Id: I4e874105262f2e15a11a7a18a7afd204e5827400
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1423109
Reviewed-by: Fabio Tirelo <ftirelo@chromium.org>
Reviewed-by: Koji Ishii <kojii@chromium.org>
Commit-Queue: Roger McFarlane <rogerm@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#640884}(cherry picked from commit 0bd10e13a008389ec14bbe7cc95f17d82ea151c1)
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1544309
Reviewed-by: Roger McFarlane <rogerm@chromium.org>
Cr-Commit-Position: refs/branch-heads/3729@{#512}
Cr-Branched-From: d4a8972e30b604f090aeda5dfff68386ae656267-refs/heads/master@{#638880}
[modify] https://crrev.com/9e68c4db781b71e9ea772ab60d34c7f10e100b57/chrome/renderer/autofill/form_autofill_browsertest.cc
[modify] https://crrev.com/9e68c4db781b71e9ea772ab60d34c7f10e100b57/third_party/blink/renderer/core/html/resources/html.css


### cr...@appspot.gserviceaccount.com (2019-03-28)

The following revision refers to this bug: 
https://chromium.googlesource.com/chromium/src.git/+/9e68c4db781b71e9ea772ab60d34c7f10e100b57

Commit: 9e68c4db781b71e9ea772ab60d34c7f10e100b57
Author: rogerm@chromium.org
Commiter: rogerm@chromium.org
Date: 2019-03-28 17:58:30 +0000 UTC

[autofill] Pin preview font-family to a system font

(Merge to M74)

Bug: 916838
Change-Id: I4e874105262f2e15a11a7a18a7afd204e5827400
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1423109
Reviewed-by: Fabio Tirelo <ftirelo@chromium.org>
Reviewed-by: Koji Ishii <kojii@chromium.org>
Commit-Queue: Roger McFarlane <rogerm@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#640884}(cherry picked from commit 0bd10e13a008389ec14bbe7cc95f17d82ea151c1)
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1544309
Reviewed-by: Roger McFarlane <rogerm@chromium.org>
Cr-Commit-Position: refs/branch-heads/3729@{#512}
Cr-Branched-From: d4a8972e30b604f090aeda5dfff68386ae656267-refs/heads/master@{#638880}

### sh...@chromium.org (2019-03-29)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-03-30)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-04-03)

[Empty comment from Monorail migration]

### na...@google.com (2019-04-10)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### na...@google.com (2019-04-10)

Congrats the Panel decided to reward $2,000 plus a $1,337 bonus for this report!

A member from our finance team will be in touch shortly. 

 

### na...@google.com (2019-04-10)

[Empty comment from Monorail migration]

### ma...@curative.com (2019-04-10)

Hmm. I expected this to qualify for $4000, @natashapabrai, since I reported this with a real attack page that actually reads credit card details without user consent. The "reward amounts" at https://www.google.com/about/appsecurity/chrome-rewards/ indicate that such a report with a functioning exploit qualifies for $4000. Could you indicate in what way the panel felt my exploit was lacking, for my future reference?

As for the marking of this as fixed - unless there's another commit not referenced here, I think that the scrollWidth leak is in fact still unfixed, and that all that's been changed so far is pinning the font to a system font. That stops the particular exploit I used here from working, but there's still a (admittedly minor) information leak that ought to be fixed by patching the scrollWidth property.

### ma...@curative.com (2019-04-10)

Since this is marked as fixed (and indeed the particular exploit here *is* fixed), I have tinkered around with the Beta release and opened a new ticket describing a new version of the exploit: https://bugs.chromium.org/p/chromium/issues/detail?id=951487

### aw...@google.com (2019-04-17)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-04-22)

[Empty comment from Monorail migration]

### aw...@google.com (2019-04-22)

+natashapabrai@ for https://crbug.com/chromium/916838#c40

### ba...@chromium.org (2019-04-29)

[Empty comment from Monorail migration]

### ba...@chromium.org (2019-06-13)

CCing tkent for access to the bug in context of https://chromium-review.googlesource.com/c/chromium/src/+/1638541

### ba...@chromium.org (2019-06-17)

I have landed the layout fix of https://chromium-review.googlesource.com/c/chromium/src/+/1638541, which landed in 77.0.3826.0.

For reason I don't know, it does not show up here.

### cr...@appspot.gserviceaccount.com (2019-06-26)

The following revision refers to this bug: 
https://chromium.googlesource.com/chromium/src.git/+/036c081fe7cec07b3e04ffb16d869103e381b445

Commit: 036c081fe7cec07b3e04ffb16d869103e381b445
Author: battre@chromium.org
Commiter: battre@chromium.org
Date: 2019-06-26 07:50:58 +0000 UTC

Fix font size for prefilled values.

This is a better way to pin the fonts than http://crrev.com/669336.
Instead of pinning the fonts to the system font, they are actually
pinned to what LayoutThemeFontProvider::SystemFont maps to
-webkit-small-control. This creates even less jank on most sites
the rely on default fonts in input elements. Also the font sizes
are now pinned.

(cherry picked from commit 005563ec0a7e7b8b6d4b4bc20702f4eb900d128d)

Bug: 916838,951487
Change-Id: I2efb2eaf11276bc75052708f0c61a35ad9ae4c88
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1670897
Commit-Queue: Dominic Battré <battre@chromium.org>
Reviewed-by: Kent Tamura <tkent@chromium.org>
Reviewed-by: Koji Ishii <kojii@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#671647}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1676707
Reviewed-by: Dominic Battré <battre@chromium.org>
Cr-Commit-Position: refs/branch-heads/3809@{#590}
Cr-Branched-From: d82dec1a818f378c464ba307ddd9c92133eac355-refs/heads/master@{#665002}


### cr...@appspot.gserviceaccount.com (2019-06-26)

Here's a summary of the rules that were executed: 
 - OnlyMergeApprovedChange: Rule Failed -- Revision 079a470ed30ef34890dbd62e088a5ee5920c0c1e was merged to refs/branch-heads/3809 branch with no merge approval from a TPM! 
Please explain why this change was merged to the branch!
 - AcknowledgeMerge: Notification Required -- 

### cr...@appspot.gserviceaccount.com (2019-06-26)

The following revision refers to this bug: 
https://chromium.googlesource.com/chromium/src.git/+/079a470ed30ef34890dbd62e088a5ee5920c0c1e

Commit: 079a470ed30ef34890dbd62e088a5ee5920c0c1e
Author: battre@chromium.org
Commiter: battre@chromium.org
Date: 2019-06-26 07:49:38 +0000 UTC

Pin preview font-family to system font in different way

crrev.com/640884 pinned the preview font-family to the system font by modifying
-internal-autofill-previewed. This cause a UI flaw in the sense that the
preview state triggered a relayout of the entire page and moved content around.

A previewed input element looks like this:

<input type="text">
  #shadow-root (user-agent)
  <div pseudo="-internal-input-suggested" id="placeholder"
      style="display: block! imporant;">suggested value</div>
  <div>actual value</div>
</input>

This CL moves the "font-family: system-ui !important;" from selector
input:-internal-autofill-previewed (which applies to the entire <input>
element and is set to the <input> element via
HTMLFormControlElement::SetAutofillState) to
input::-internal-input-suggested (which only applies to the inner <div>).

The internal <div> does not re-layout the rest of the DOM. so the reflow is
gone.

As a side effect, the font-family is only set for <input> elements but not
for <textarea> or <select> elements, which should not be counter the reason for
which crrev.com/640884 was implemented. Chrome does not fill <textarea> elements
and <select> elements draw themselves entirely differently.

(cherry picked from commit 8427f5edd001bccb4c82582d4f7a005ac8e8ee8c)

Bug: 916838
Change-Id: I72fd7b1743e85513110c98f78a0074dc8fafd560
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1638541
Reviewed-by: Kent Tamura <tkent@chromium.org>
Reviewed-by: Vadym Doroshenko <dvadym@chromium.org>
Reviewed-by: Emil A Eklund <eae@chromium.org>
Reviewed-by: Koji Ishii <kojii@chromium.org>
Commit-Queue: Dominic Battré <battre@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#669336}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1676706
Reviewed-by: Dominic Battré <battre@chromium.org>
Cr-Commit-Position: refs/branch-heads/3809@{#589}
Cr-Branched-From: d82dec1a818f378c464ba307ddd9c92133eac355-refs/heads/master@{#665002}


### ab...@google.com (2019-06-26)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-06-27)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-07-06)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### na...@google.com (2020-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/916838?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093523)*
