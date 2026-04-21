# Security: Another autocomplete preview text leak

| Field | Value |
|-------|-------|
| **Issue ID** | [40056443](https://issues.chromium.org/issues/40056443) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Autofill |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ma...@gmail.com |
| **Assignee** | ba...@chromium.org |
| **Created** | 2021-07-07 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

This exploit allows a malicious webpage containing a HTML form to read values that are being proposed by Chrome's autocomplete feature before the user has actually selected them (i.e. while the autocomplete UI is open and in the "suggest"/"preview" state).

In this way, it is similar to the following exploits I've reported previously:  

\* <https://bugs.chromium.org/p/chromium/issues/detail?id=916838>  

\* <https://bugs.chromium.org/p/chromium/issues/detail?id=951487>  

\* <https://bugs.chromium.org/p/chromium/issues/detail?id=1013882>  

\* <https://bugs.chromium.org/p/chromium/issues/detail?id=1035058>  

\* <https://bugs.chromium.org/p/chromium/issues/detail?id=1035063>

As a reminder of the feature and its security model: Chrome's form autocompletion includes rendering suggested values inside the form fields while the user is hovering over possible autocomplete options or scrolling through them with the keyboard, but these values are \*not\* exposed via the .value property on those fields and are not supposed to be readable by the web page until the user commits a suggestion to the field (by clicking on it or pressing the Enter key).

I've included a demo below that - like my previous demos - reads the user's credit card number as soon as they press the up or down arrow key. Thus minimal social engineering is required - just lure them to a page and get them to press one key, and you have their card number. The approach used could in principle be extended to other autocomplete data, although the limited alphabet (digits only) of card numbers makes them particularly easy targets.

Below I'll list the bugs and tactics that contribute to the final demo.

<https://crbug.com/chromium/1> (remaining scrollWidth data leak in "suggest" state):

Although the fix to <https://bugs.chromium.org/p/chromium/issues/detail?id=1035058> attempted to mock scrollWidth on textareas in the "suggest" state so that no information about the width of the suggestion content would be leaked to JavaScript, it didn't completely succeed; the scrollWidth value returned for a textarea with a given width depends upon whether it contains a vertical scrollbar.

This immediately allows two tactics:

Tactic 1 (suggestion text appearance detection):

In a form where Chrome will fill suggestion text, include a tiny (e.g. 5px by 1px) textarea with autocomplete enabled. Record its initial scrollWidth into a variable when the page loads, then check its scrollWidth constantly (e.g. via a setInterval). When it changes, this indicates that a vertical scrollbar has appeared in the field, which in turn indicates that suggestion text has appeared in the field (and hence also in other fields that get autocompleted simultaneously).

Tactic 2 (vertical scrollbar detection):

In the form where autocomplete is happening, include a textarea that has autocomplete enabled, is tall and wide, and is limited via the maxlength attribute to containing 1 character. Since it is big and can only have one character of content, it can be assumed to never contain a scrollbar. When it contains suggestion text (which can be detected via Tactic 1), calculate the difference between its offsetWidth and scrollWidth and store it in a variable.

To determine whether some other textarea in the preview state has a vertical scrollbar, compute the difference between its offsetWidth and scrollWidth and check whether it is equal to the already-computed difference from the textarea known to have no scrollbar. If it is different, then the textarea has a vertical scrollbar.

Tactic 3 (suggestion text width measuring):

As long as suggestion text in a textarea is more than 1 character long, its width can be measured by setting its height to just barely above the height of one line of text (so that text spilling over to a second line will cause a vertical scrollbar will appear) and its width to 1px, then increasing the width by 1px at a time and using vertical scrollbar detection after each increase. When the vertical scrollbar vanishes, the width the textarea has been set to is equal to the width of the suggestion text.

Tactic 4 (per-character suggestion text width measuring):

The widths of the third character and onward of suggestion text in an autocomplete form can be measured by creating a series of textareas with increasing maxlength attributes, starting at 2 and going up by 1 each time, all set to autocomplete to the same value, and then using Tactic 3 on each of them. The width of e.g. the fifth character is then the difference in width between the content in the textarea with maxlength=4 and the content in the textarea with maxlength=5.

<https://crbug.com/chromium/2> (fixing of font for autocomplete text can be bypassed):

Although the fix to <https://bugs.chromium.org/p/chromium/issues/detail?id=1035058> attempted to fix the `font` CSS property of preview text in a way that couldn't be overridden by CSS on the webpage, it didn't quite manage to do that either; the font of the first line can still be modified by CSS targeting the textarea's ::first-line pseudo-element.

Tactic 5 (determining the third and subsequent characters of suggestion text):

Combining <https://crbug.com/chromium/2> and tactic 4 lets us determine what the third and subsequent characters are in preview text. We just generate a custom font where each character has a distinct width, then use <https://crbug.com/chromium/2> to set that font on each of the textareas described in tactic 4. Then we execute tactic 4 and map from the signature character widths back to the characters.

Tactic 6 (font choice conditional on suggestion text):

By declaring a font-family using a series of font-face declarations that each include a unicode-range descriptor (<https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face/unicode-range>) limiting them to a single character, then setting it on a textarea's suggestion text by targeting ::first-line as described in <https://crbug.com/chromium/2>, you can make the font(s) used depend on the character(s) in the suggestion text. This can be exploited either to trigger HTTP requests (to load the fonts) conditionally based on suggestion text, or to implement tactic 8, below...

Tactic 7 (suggestion text height measuring):

Use the same approach as tactic 3, but gradually increasing the textarea's \*height\* (instead of its width). When the vertical scrollbar disappears, the textarea is tall enough to hold all its content.

Tactic 8 (determining the first character of suggestion text):

Create a textarea limited to a maxlength of 1. Use tactic 6 to set make its font be conditionally chosen based on the character it contains, with the possible fonts all having distinct line heights (for instance by giving them increasingly large "ascender" and "descender" values, in the case of TrueType fonts; I'm not sure whether there are other ways to achieve the same thing or whether the ascender/descender concept exists for all font types). When the textarea is filled with suggestion content (detected by Tactic 1), measure the height of that content (using tactic 7). Then map that height back to the font that was used and hence the character that is contained in the suggestion text.

---

The overall exploit strategy thus looks like this:  

\* Create a page with a credit card form (which can be hidden behind other content) with one autofocused autocomplete <input> and lots of autocomplete <textarea>s that are configured to support the tactics described above.  

\* Lure a user to it and induce them to press the up or down arrow key, immediately putting autocomplete suggestion text into the textareas  

\* Via tactic 1, the page detects and reacts to the appearance of the suggestion text. It executes tactic 8 to determine the first digit of their credit card number, executes tactic 5 to determine digits 3-16 of their credit card number, and then infers the second digit by picking the value that passes the Luhn check.  

\* (Then if this was being used for real the page would send the card number off via a HTTP request to bad people who would use it for fraud etc)

**VERSION**  

Chrome Version: 92.0.4515.80 beta  

Operating System: Ubuntu 20.04

**REPRODUCTION CASE**  

Host the attached demo.html and various .js files on a HTTPS webserver. Visit demo.html from an install of Chrome where you have a Luhn-passing 16-digit credit card number stored in autocomplete (but NOT in Google Pay - for some reason the autocomplete preview text shown for a card number stored in Google Pay is \*not\* the card number itself, which defeats this attack). Press the up or down arrow key and your card number should appear in an alert.

Note that I've tested on Ubuntu but not in other OSes.

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Mark Amery

## Attachments

- [demo.html](attachments/demo.html) (text/plain, 5.2 KB)
- [fontUtils.js](attachments/fontUtils.js) (text/plain, 2.5 KB)
- [opentype.js](attachments/opentype.js) (text/plain, 455.7 KB)
- [utils.js](attachments/utils.js) (text/plain, 885 B)
- [Screen Shot 2021-07-13 at 1.08.04 PM.png](attachments/Screen Shot 2021-07-13 at 1.08.04 PM.png) (image/png, 27.8 KB)
- [Screen Shot 2021-07-14 at 22.24.25.png](attachments/Screen Shot 2021-07-14 at 22.24.25.png) (image/png, 48.8 KB)
- [Screen Shot 2021-07-14 at 22.30.08.png](attachments/Screen Shot 2021-07-14 at 22.30.08.png) (image/png, 59.3 KB)

## Timeline

### [Deleted User] (2021-07-07)

[Empty comment from Monorail migration]

### rs...@chromium.org (2021-07-08)

Thank you for this detailed report. I was able to verify this on Ubuntu on M91 using a test credit card number.

Assigning to battre@ per https://crbug.com/chromium/1035063 et al.

[Monorail components: UI>Browser>Autofill]

### ba...@chromium.org (2021-07-08)

Thank you for the bug report. We will look into it.

### [Deleted User] (2021-07-08)

[Empty comment from Monorail migration]

### ba...@chromium.org (2021-07-09)

I cannot reproduce the problem (my digits3To16 are [-9, 11, 1, 1, -17, 19, 1, -23, 25, 1, 1, -31, 33, 1]) but I can imagine that something like this works (even though I don't fully understand all steps of the attack, yet).

@futhark, @masonf, tkent@ do you see any reliable way to fix the problems on the renderer side?

1) The scrollHeight calculation was moved in this CL https://chromium-review.googlesource.com/c/chromium/src/+/2488963. Would it make sense if HTMLTextAreaElement::scrollHeight() and HTMLInputElement::scrollHeight() received their own implementations in case the elements are in preview state rather than delegating to TextControlElement::scrollHeight() (which is Element::scrollHeight())

2) Do you see a way of more reliably overriding the text style? It looks like https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/html/resources/html.css;l=580;drc=bad2e8cbbeaed94546a41bc715a6263650555254 is insufficient and can be overridden with textarea::first-line.

3) I can see a relatively straightforward approach of mitigating the problem by showing "**** **** **** 1111" instead of "4111 1111 1111 1111" as a preview state. We do this for cards from GPay as well.

I think that 3) would get us pretty far but I would also like the last 4 digits to be not discoverable.

### ma...@gmail.com (2021-07-09)

The other thing with 3), of course, is that it only protects card numbers specifically. I've always targeted card numbers so far because only having to deal with 10 possible characters and no spaces makes these attacks a bit simpler to implement, but other autofill fields (like someone's home address) are also vulnerable in theory to the same exploit, and also potentially serious to leak.

Sorry to hear that the demo didn't work for you. I have a couple of ideas that might get it working for you:
* try setting and unsetting a .value on textAreas[0] when the page loads to force the custom font to load into memory immediately, like I do with firstDigitTester.value = '1234567890';.
* make findContentWidthOfPreviewText be an async function, await it at the place where it's called, and stick an `await timeout(1)` after each assignment to textArea.style.width

(The latter suggested change makes the attack less good, since it makes it slower and interruptible by the user, but might suffice let you see at least a toy version of it working.)

### [Deleted User] (2021-07-10)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### tk...@chromium.org (2021-07-12)

> 1) The scrollHeight calculation was moved in this CL https://chromium-review.googlesource.com/c/chromium/src/+/2488963. Would it make sense if HTMLTextAreaElement::scrollHeight() and HTMLInputElement::scrollHeight() received their own implementations in case the elements are in preview state rather than delegating to TextControlElement::scrollHeight() (which is Element::scrollHeight())

I think they already have special code path for the preview state.

> 2) Do you see a way of more reliably overriding the text style?

This should be unnecessary if scrollWidth and scrollHeight return font-independent values in the preview state, right?


### ba...@chromium.org (2021-07-12)

1) As per the bug report ("Tactic 1" - 3) above the special code path for the preview state is insufficient.

2) Due to "Tactic 6", we still need to find a way to override the text style.

### tk...@chromium.org (2021-07-13)

Anyway, I think the ultimate fix would be to show preview values on FrameOverlay, which is used by DevTools and form validation messages.


### ba...@chromium.org (2021-07-13)

Adding some PMs and UXers for the proposal to use FrameOverlay.

tkent@ do you see a realistic chance to address items mentioned in https://crbug.com/chromium/1227170#c9? I am not sufficiently rooted in Blink to be able to do that without guidance.

### tk...@chromium.org (2021-07-13)

Re: https://crbug.com/chromium/1227170#c9

1) Let's fix it!

2) I don't know a reliable way to protect text style.
I think specifying each of ::first-line:-internal-autofill-* and ::first-letter:-internal-autofill-* is sufficient for now.  However, if CSS will introduce new pseudo-element like them in the future, we must not miss to handle it too.


### ma...@chromium.org (2021-07-13)

I agree that it seems like the simplest way to block "https://crbug.com/chromium/2" is to specify all of the additional pseudo elements in html.css, as suggested in https://crbug.com/chromium/1227170#c12. I don't see how we could test for additional (newly added) pseudo elements, so we'll need to be watchful of that.

### ba...@chromium.org (2021-07-14)

I tried it out, see https://paste.googleplex.com/5306451917537280, but could not get it to work.

If you look at the first attached screenshot, you see the lines 

    font: -webkit-small-control !important;
    overflow: hidden !important;
    overflow-anchor: none;

that originate from this: https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/html/resources/html.css;l=578-587;drc=bad2e8cbbeaed94546a41bc715a6263650555254

As soon as I add the extra selectors like here:

input::-internal-input-suggested,
input::first-letter:-internal-input-suggested,
input::first-line:-internal-input-suggested,
textarea::-internal-input-suggested,
textarea::first-letter:-internal-input-suggested,
textarea::first-line:-internal-input-suggested {
 ...
}

the 3 lines quoted above go away (see the second screenshot). I interpret this as the parser being unable to deal with these lines.

I have tried multiple versions:
- input::first-line:-internal-input-suggested
- input:-internal-input-suggested::first-line
- ::first-line:-internal-input-suggested

They all led to the same result shown in the second screenshot.

### ba...@chromium.org (2021-07-14)

Never mind. I found the grammar definition https://drafts.csswg.org/selectors-4/#grammar and I think that I have figured it out.

### ba...@chromium.org (2021-07-14)

Sent https://chromium-review.googlesource.com/c/chromium/src/+/3028961 your way.

### ba...@chromium.org (2021-07-15)

Adding cbiesinger@ and yosin@ here for the review of https://chromium-review.googlesource.com/c/chromium/src/+/3028961

### ba...@chromium.org (2021-07-15)

cbiesinger@ suggested kojii@ as a better reviewer for the layout changes of https://chromium-review.googlesource.com/c/chromium/src/+/3028961

### ma...@gmail.com (2021-07-17)

After some thought, my instinct is that any solution that still leaves the values in the Shadow DOM is going to still be vulnerable to some kind of attack. For instance, here's another idea I had a couple of days ago: use text fragments (https://wicg.github.io/scroll-to-text-fragment/) that target a string you're looking for in the preview text and then check whether the page scrolled. It seems that text fragments can indeed target suggestion text, and that you can change the URL fragment via JavaScript and such a change will trigger the page to scroll to the targeted text if it's present. Finally you can detect the scroll happening by polling window.scrollY.

Apparently an attack similar to this was contemplated when text fragments were implemented - see "scroll-based attack" at https://docs.google.com/document/d/1YHcl1-vE_ZnZ0kL2almeikAj2gkwCq8_5xwIae7PVik/edit#. There, though, they're contemplating attacks involving somehow detecting scrolling happening in another frame from a different origin. It doesn't seem to have been on their radar that there could be content within shadow DOMs *in the current frame* that needs to be secret too.

Chrome seems to limit text fragments to targeting full words, not partial words, as a mitigation against this kind of attack. In this case though, I don't think that offers any help, since we can use maxlength on textareas to limit how much of the suggestion gets included in the DOM in the first place; then some subset of the card number IS a full word.

Thus this technique should give us an entirely new mechanism to repeatedly query for prefixes of the card number and find out whether they're present. Once we can do that, of course, the rest of the logic of the attack is exactly like this one and the previous five I've opened: first use the mechanism to find the first character, then repeatedly test possible one-character extensions to the currently-known prefix until you've got all 16 digits.

So what's the right fix, then?

tkent earlier suggested using something called FrameOverlay to show these values, which per his comment is apparently what the dev tools do. I'm not a Chrome dev and have never heard of a FrameOverlay until now, but I assume that this would get the content out of the shadow DOM, and if so, it sounds like it's probably the right thing to do here and a much more robust fix than tinkering with the styling of the shadow DOM.

A bonus would be if there's a reasonable and non-leaky way to explicitly make the text shown in that FrameOverlay respect a subset of the font styling CSS properties that are applied to the input or textarea that spawned it, especially the font-size. That way, as well as fixing the security hole once and for all, you could also fix or mitigate the aesthetic issues that have been caused by forcing preview text to be a different font size from real form text. Those aesthetic issues upset a lot of people (see https://stackoverflow.com/q/56271193/1709587, https://stackoverflow.com/q/56026043/1709587, https://bugs.chromium.org/p/chromium/issues/detail?id=953689). The only thing to cautious about here is font-familys that point to custom fonts, due to the kind of leaks I described in tactic 6 above. Even just respecting font-size would be a big step up in aesthetics, though!

### ma...@chromium.org (2021-07-23)

...I'd like to pull in a conversation from a CL here, so we have the record in a bug. In response, essentially, to https://crbug.com/chromium/1227170#c19, I said this:

Ok, thanks for the detailed comment on the issue. I think I agree with you that we should look into using FrameOverlay (or something similar) instead of shadow dom. Having sensitive data connected to the DOM tree just seems to invite problems.




### ma...@chromium.org (2021-07-23)

Then battre@ said this:

I looked a bit into FrameOverlay and third_party/blink/renderer/core/page/validation_message_overlay_delegate.cc.

This is certainly interesting and opens up some new opportunities.

OTOH, this will always draw with the highest z-index, right? Would we have options to inject this in the right z-order?

Autofilling into hidden input elements is a concern to us, but I wonder whether this would create a weird UX.

Would there be other ways of sticking more or less to the current implementation but detaching the CSS Styles from the embedding document?

### ma...@chromium.org (2021-07-23)

And now I'd like to say this:

I believe you're correct that FrameOverlay will paint "on top" of everything else. +pdr@ to confirm.

I do see your point that using Shadow DOM as we are here automatically gets around a number of sticky issues. Shadow DOM is intended to isolate styles, so it should at least be a good starting point for this use case. The issue is that a number of properties inherit, or otherwise affect rendering, of shadow-isolated content. And there are a number of pseudo elements that also have the power to style into shadow roots. Short of making sure to explicitly style all of those in the UA stylesheet, I'm not sure there's a good way to isolate them all.

One idea, which I'm not sure would work here, would be to use `contain:strict` on the shadow roots created for this purpose. I would think that should keep any CSS adjustments from outside from affecting at least the dimensions of the outer element, and that seems to be the vector for information leakage in all of these cases.



### ba...@chromium.org (2021-07-23)

Another crazy idea: Could we hack the CSS style engine to not allow pseudo classes in some situations (i.e. when the text control element is in previous state)? If that was the case, would placeholder->style()->setProperty(GetExecutionContext(), "font", "-webkit-small-control", "important", ASSERT_NO_EXCEPTION); be sufficient because the style attribute would have the highest CSS specificity?

### ba...@chromium.org (2021-07-23)

I've been playing a bit with TextControlInnerEditorElement::CustomStyleForLayoutObject but my limited knowledge of the style engine did not get me very far. Would this be an avenue worth pursuing?

### ko...@chromium.org (2021-07-24)

Rune is the best expert, but he's OOF for another week. Here's what I can suggest from the layout perspective.

`::first-line` is probably a little different from other pseudo, because it depends on the layout result.

The lowest level entry of `::first-line` from the layout perspective is `LayoutObject::FirstLineStyleWithoutFallback`:
https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/layout/layout_object.cc;l=4142;drc=0d99d5d1985df1f0788ccdaa43b34e8d248bf2c1;bpv=0;bpt=1

This seems to call `LayoutObject::GetUncachedPseudoElementStyle`, which calls `Element::StyleForPseudoElement`. Maybe either of these are good point to disable pseudo?

### pd...@chromium.org (2021-07-26)

Re https://crbug.com/chromium/1227170#c22: yes, FrameOverlay paints on top of everything else. If it were modified to paint with the correct z-order, we'd be open to timing attacks that time subtle differences in how long it takes to apply filters on various inputs. These timing attacks are a much higher bar than getting data out of the DOM (e.g., timing is slow and unreliable), but we should probably investigate an approach that still paints above everything the page can control.

### gi...@appspot.gserviceaccount.com (2021-07-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/be292efb581a1e0c0c5ca45bf7c3fe0a99ae18dc

commit be292efb581a1e0c0c5ca45bf7c3fe0a99ae18dc
Author: Dominic Battre <battre@chromium.org>
Date: Tue Jul 27 13:41:43 2021

Change local card previews to show **** 1111

This CL harmonizes the previews of server cards and local cards. After
this change, both are shown in obfuscated state during preview.

Bug: 1227170
Change-Id: I22d080bd70f99016fae7d28d4b79620a11c3562b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3055995
Commit-Queue: Christoph Schwering <schwering@google.com>
Reviewed-by: Christoph Schwering <schwering@google.com>
Cr-Commit-Position: refs/heads/master@{#905709}

[modify] https://crrev.com/be292efb581a1e0c0c5ca45bf7c3fe0a99ae18dc/components/autofill/core/browser/browser_autofill_manager.cc
[modify] https://crrev.com/be292efb581a1e0c0c5ca45bf7c3fe0a99ae18dc/components/autofill/core/browser/browser_autofill_manager.h
[modify] https://crrev.com/be292efb581a1e0c0c5ca45bf7c3fe0a99ae18dc/components/autofill/core/browser/field_filler.cc
[modify] https://crrev.com/be292efb581a1e0c0c5ca45bf7c3fe0a99ae18dc/components/autofill/core/browser/field_filler.h
[modify] https://crrev.com/be292efb581a1e0c0c5ca45bf7c3fe0a99ae18dc/components/autofill/core/browser/field_filler_unittest.cc


### [Deleted User] (2021-08-05)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-07)

battre: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-08-16)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-22)

battre: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ko...@google.com (2021-08-23)

Adding mamir@ as our UI expert.

### [Deleted User] (2021-09-11)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-22)

[Empty comment from Monorail migration]

### ba...@chromium.org (2021-09-27)

I am currently investigating whether StyleAdjuster::AdjustComputedStyle or LayoutTheme::AdjustStyle would be our friends.

https://crbug.com/chromium/1253103 says that <select> elements are rendered differently. Not sure whether that would need more work.

### ba...@chromium.org (2021-09-27)

I have a prototype that seems to be working except for the ::first-line pseudo state: For ::first-line, the computed style of the shadow dom is correct (as per DevTools) but it is not applied.

I believe that
https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/css/resolver/style_resolver.cc;l=1047;drc=9834395f60edc393922232e5194b4e299b6174e9
may be the culprit. The passed element is a nullptr, so I cannot see that this has a ShadowPseudoId() == shadow_element_names::kPseudoInternalInputSuggested whose style should be overridden.

I need to find a nice place to override the style. StyleAdjuster::AdjustComputedStyle or LayoutTheme::AdjustStyle looked nice, but I don't have the element to check whether to hard code the font and overflow properties.

Maybe andruud@ has an idea, who worked on this code recently.

### ba...@chromium.org (2021-09-28)

I have uploaded a CL here: https://chromium-review.googlesource.com/c/chromium/src/+/3192670

This is a very crude prototype whose primary purpose is to ask questions. It kind of works for ::first-line but there are many open questions.

tkent@, masonf@, futhark@ I would appreciate your expertise and guidance.

### ba...@chromium.org (2021-10-18)

https://chromium-review.googlesource.com/c/chromium/src/+/3225931 is a new attempt

### gi...@appspot.gserviceaccount.com (2021-10-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b773c550412c39c69014a558015aafe447231039

commit b773c550412c39c69014a558015aafe447231039
Author: Dominic Battre <battre@chromium.org>
Date: Tue Oct 19 08:58:30 2021

Prevent ::first-line from styling prefilled values

Fixed: 1253101, 1227170
Change-Id: I54e7a547c38f7a5558a7b29807f3e523b31cef52
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3225931
Commit-Queue: Dominic Battré <battre@chromium.org>
Reviewed-by: Kent Tamura <tkent@chromium.org>
Reviewed-by: Koji Ishii <kojii@chromium.org>
Reviewed-by: Mason Freed <masonf@chromium.org>
Reviewed-by: Rune Lillesveen <futhark@chromium.org>
Cr-Commit-Position: refs/heads/main@{#932921}

[add] https://crrev.com/b773c550412c39c69014a558015aafe447231039/third_party/blink/web_tests/fast/forms/text/input-appearance-autofill-ignoring-first-line-expected.html
[add] https://crrev.com/b773c550412c39c69014a558015aafe447231039/third_party/blink/web_tests/fast/forms/text/input-appearance-autofill-ignoring-first-line.html
[modify] https://crrev.com/b773c550412c39c69014a558015aafe447231039/third_party/blink/renderer/core/layout/layout_block.cc


### [Deleted User] (2021-10-19)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-19)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-10-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/d3886012130816c950285b68ecce157d26676293

commit d3886012130816c950285b68ecce157d26676293
Author: Dominic Battre <battre@chromium.org>
Date: Thu Oct 21 16:42:29 2021

Prevent ::first-line from styling prefilled values

(cherry picked from commit b773c550412c39c69014a558015aafe447231039)

Fixed: 1253101, 1227170
Change-Id: I54e7a547c38f7a5558a7b29807f3e523b31cef52
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3225931
Commit-Queue: Dominic Battré <battre@chromium.org>
Reviewed-by: Kent Tamura <tkent@chromium.org>
Reviewed-by: Koji Ishii <kojii@chromium.org>
Reviewed-by: Mason Freed <masonf@chromium.org>
Reviewed-by: Rune Lillesveen <futhark@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#932921}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3236668
Auto-Submit: Dominic Battré <battre@chromium.org>
Commit-Queue: Rune Lillesveen <futhark@chromium.org>
Cr-Commit-Position: refs/branch-heads/4664@{#293}
Cr-Branched-From: 24dc4ee75e01a29d390d43c9c264372a169273a7-refs/heads/main@{#929512}

[add] https://crrev.com/d3886012130816c950285b68ecce157d26676293/third_party/blink/web_tests/fast/forms/text/input-appearance-autofill-ignoring-first-line-expected.html
[add] https://crrev.com/d3886012130816c950285b68ecce157d26676293/third_party/blink/web_tests/fast/forms/text/input-appearance-autofill-ignoring-first-line.html
[modify] https://crrev.com/d3886012130816c950285b68ecce157d26676293/third_party/blink/renderer/core/layout/layout_block.cc


### gi...@appspot.gserviceaccount.com (2021-10-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f785fa7895f6e12e2c181f71d646828ef87e5dcb

commit f785fa7895f6e12e2c181f71d646828ef87e5dcb
Author: Dominic Battre <battre@chromium.org>
Date: Wed Oct 27 12:19:55 2021

Prevent ::first-line from styling prefilled values

(cherry picked from commit b773c550412c39c69014a558015aafe447231039)

Fixed: 1253101, 1227170
Change-Id: I54e7a547c38f7a5558a7b29807f3e523b31cef52
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3225931
Commit-Queue: Dominic Battré <battre@chromium.org>
Reviewed-by: Kent Tamura <tkent@chromium.org>
Reviewed-by: Koji Ishii <kojii@chromium.org>
Reviewed-by: Mason Freed <masonf@chromium.org>
Reviewed-by: Rune Lillesveen <futhark@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#932921}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3247154
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Commit-Queue: Rune Lillesveen <futhark@chromium.org>
Auto-Submit: Dominic Battré <battre@chromium.org>
Cr-Commit-Position: refs/branch-heads/4638@{#977}
Cr-Branched-From: 159257cab5585bc8421abf347984bb32fdfe9eb9-refs/heads/main@{#920003}

[add] https://crrev.com/f785fa7895f6e12e2c181f71d646828ef87e5dcb/third_party/blink/web_tests/fast/forms/text/input-appearance-autofill-ignoring-first-line-expected.html
[add] https://crrev.com/f785fa7895f6e12e2c181f71d646828ef87e5dcb/third_party/blink/web_tests/fast/forms/text/input-appearance-autofill-ignoring-first-line.html
[modify] https://crrev.com/f785fa7895f6e12e2c181f71d646828ef87e5dcb/third_party/blink/renderer/core/layout/layout_block.cc


### am...@google.com (2021-10-28)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-10-28)

Congratulations, Mark! The VRP Panel has decided to award you $5000 for this report. A member of our finance team will be in touch soon to arrange payment. Thanks for your efforts in reporting these issues and nice work! 

### am...@google.com (2021-10-29)

[Empty comment from Monorail migration]

### ba...@chromium.org (2021-11-02)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-11-05)

was accidentally left off release notes since two bugs were on merge and the other was merged into this one after the fact 

### am...@google.com (2021-11-05)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-11-05)

Hi Mark, just FYSA, I've updated the release notes for the latest stable channel update to reflect this issue being included in that release as well as attribute the finding to you: https://chromereleases.googleblog.com/2021/10/stable-channel-update-for-desktop_28.html
Apologies this got included only after the fact! 

### rz...@google.com (2021-11-08)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-15)

[Empty comment from Monorail migration]

### gi...@google.com (2021-11-18)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-11-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/2a42048222665b97f9e9725ba87284b1d4717f64

commit 2a42048222665b97f9e9725ba87284b1d4717f64
Author: Dominic Battre <battre@chromium.org>
Date: Mon Nov 22 13:26:26 2021

[M90-LTS] Prevent ::first-line from styling prefilled values

(cherry picked from commit b773c550412c39c69014a558015aafe447231039)

Fixed: 1253101, 1227170
Change-Id: I54e7a547c38f7a5558a7b29807f3e523b31cef52
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3225931
Commit-Queue: Dominic Battré <battre@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#932921}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3268077
Reviewed-by: Dominic Battré <battre@chromium.org>
Reviewed-by: Oleh Lamzin <lamzin@google.com>
Owners-Override: Oleh Lamzin <lamzin@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Cr-Commit-Position: refs/branch-heads/4430@{#1668}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[add] https://crrev.com/2a42048222665b97f9e9725ba87284b1d4717f64/third_party/blink/web_tests/fast/forms/text/input-appearance-autofill-ignoring-first-line-expected.html
[add] https://crrev.com/2a42048222665b97f9e9725ba87284b1d4717f64/third_party/blink/web_tests/fast/forms/text/input-appearance-autofill-ignoring-first-line.html
[modify] https://crrev.com/2a42048222665b97f9e9725ba87284b1d4717f64/third_party/blink/renderer/core/layout/layout_block.cc


### gi...@appspot.gserviceaccount.com (2021-11-22)

https://crbug.com/chromium/1253101 has been un-merged from this issue.


### gi...@appspot.gserviceaccount.com (2021-11-22)

[Empty comment from Monorail migration]

### rz...@google.com (2021-11-22)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-26)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-03-18)

reward processed for charitable donation at the request of the researcher; email with donation code in the amount of $10,000 sent to researcher 

### ba...@google.com (2022-03-21)

👏

### am...@chromium.org (2022-07-29)

description for this CVE filed sometime back in 2021, automation seemed to skip removing label on this one

### am...@chromium.org (2022-12-13)

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

This issue was migrated from crbug.com/chromium/1227170?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/1253101]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056443)*
