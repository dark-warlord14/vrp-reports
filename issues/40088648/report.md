# Security: Autocomplete data can be stolen by malicious webpage

| Field | Value |
|-------|-------|
| **Issue ID** | [40088648](https://issues.chromium.org/issues/40088648) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Autofill |
| **Reporter** | st...@gmail.com |
| **Assignee** | se...@chromium.org |
| **Created** | 2017-08-09 |
| **Bounty** | $1,000.00 |

## Description



VULNERABILITY DETAILS
Chrome autocomplete data (e.g. email addresses) can be stolen by a malicious webpage, if the page can convince the user to hold down the 'up' or 'down' arrow key for a few seconds (maybe by playing a game). This works even in Incognito mode.

Pressing the up/down arrow key in a form field causes the autocomplete popup to appear. Pressing the key again causes entries to be selected and the value to appear in the form field. This is done using Shadow DOM, so the value shouldn't be accessible until the user actually chooses a value (e.g. by hitting enter or clicking it). However, doing setSelectionRange(0,0) to clear the selection, followed by execCommand('insertText', null, ' ') causes the the shadow DOM value to be modified and placed into the .value field of the input. 

The autocomplete popup can be moved by changing the position of the input field. I've had limited success with moving it offscreen. On Ubuntu it seems be fully hidden if the browser is not maximised. On Windows it sometimes partially renders if the browser is not maximised.

VERSION
Chrome Version: 62.0.3179.0 (Canary)
Operating System: Windows 10, Ubuntu 16.04

REPRODUCTION CASE
Open the attached file and hold down either the 'up' or 'down' arrow key (you can also just tap the key repeatedly). If you have email addresses in your autocomplete data, they should be shown on the page. If you click the hide button first, the page will attempt to hide the autocomplete popup. As I mentioned above this seems to work in incognito mode. 




## Attachments

- [steal.html](attachments/steal.html) (text/plain, 1.3 KB)
- [cardsteal.html](attachments/cardsteal.html) (text/plain, 1.9 KB)
- [card.html](attachments/card.html) (text/plain, 542 B)

## Timeline

### st...@gmail.com (2017-08-09)

I've also put the PoC at http://dev.jigawatt.co.uk/dev/autocomplete/steal.html 

### st...@gmail.com (2017-08-09)

Here's a version that grabs credit card details across multiple fields (also works in Incognito). You could probably also grab address data like this too. 

### st...@gmail.com (2017-08-09)

Here's a form for saving test credit card data if you need it.

### st...@gmail.com (2017-08-09)

And hosted PoCs if you want (obvs don't use real card data!):
https://www.stonie.co.uk/autocomplete/cardsteal.html
https://www.stonie.co.uk/autocomplete/cards.html

### ke...@chromium.org (2017-08-09)

Thanks for the report.

I think this might just be a duplicate of https://crbug.com/chromium/448539, where we want to make it so that hidden fields don't get autofilled.

It's a little disconcerting that the page can get the data without the user actually selecting it. On the one hand if the page has induced the user to bring up and scroll through the autofill suggestions, it can probably also get the user to press enter and populate the fields. On the other, I think we have a general expectation that you need to select an autofill option before it becomes available to JavaScript, and at least on my part I didn't know it was possible to get it right out of the bubble.

Adding palmer@ for any thoughts on that.

[Monorail components: UI>Browser>Autofill]

### ts...@chromium.org (2017-08-09)

felt, can you suggest someone on your autofill team to take a look at this?

### ts...@chromium.org (2017-08-09)

[Empty comment from Monorail migration]

### pa...@chromium.org (2017-08-09)

estark is the Enamel TL. It sounds like we need to fill the form fields not on arrow (or mouseover), but on *select* (Enter or click).

### ke...@chromium.org (2017-08-09)

re https://crbug.com/chromium/753645#c8: It sounds like that is generally the behavior, but the PoC gets around it with the following lines, to cause the value to populate into the normal DOM:
field.setSelectionRange(0,0);
var result = document.execCommand('insertText', false, ' ');

### st...@gmail.com (2017-08-09)

A more appropriate title for this bug might be 'Autocomplete data can be stolen via Shadow DOM leak'. I'm not sure if there are other places where sensitive data is held inside text fields using Shadow DOM - but if so, they would be vulnerable too.

I think another difference from https://crbug.com/chromium/448539 is that lots of data can be stolen fairly rapidly with a single user gesture. Without this bug, an attacker would have to convince a user to type 'down, down, enter', then 'down, down, down, enter' and so on.

### sh...@chromium.org (2017-08-10)

[Empty comment from Monorail migration]

### fe...@chromium.org (2017-08-21)

Hi Roger, can you have a look at this?

### sh...@chromium.org (2017-08-23)

rogerm: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ro...@chromium.org (2017-08-24)

Seb, I'm OOO with no computer for another week, do you have some cycles to look at this? If not, I can look at it once I'm back from vacation.

There's another bug about chrome failing to fill shadow dom elements, which is an interesting twist on this.

### se...@chromium.org (2017-08-24)

Looking now.

### se...@chromium.org (2017-08-25)

I digged into the code to "preview" autofill suggestions and I arrived at this: The SetSuggestedValue of the HTMLInputElement class in WebKit (link at the bottom).

tkent@ are you familiar with this part of the code? I would appreciate any pointers you might have. Thanks!

* https://cs.chromium.org/chromium/src/third_party/WebKit/Source/core/html/HTMLInputElement.cpp?sq=package:chromium&dr=CSs&l=1063


### tk...@chromium.org (2017-08-27)

Autofill team added the concept of 'suggested value' to HTMLInputElement, and I'm not so familiar with it.


Probably, we should disabled all of editing operations to a text field while it has a suggested value. Or we should show autofill preview values as 'placeholder' text instead of a kind of 'value'.

+yosin, who is an editing expert.


### se...@chromium.org (2017-08-28)

Thanks tkent@!

yosin@ can you please advise when you can?

Thanks

### se...@chromium.org (2017-08-28)

You can also "repro" the bug manually.

Steps:

- Preview an autofill value in a field (ex https://rsolomakhin.github.io/autofill/)

- Use the left arrow key to put the cursor on the left of the input field.

- Press the "space" key, or any other. 

In this case the action is taken by the user, so it makes sense to set the field's value. The bug is triggering the same behavior programmatically.

### pa...@chromium.org (2017-08-28)

[Empty comment from Monorail migration]

### se...@chromium.org (2017-08-28)

Here are some updates of my investigation:

When an Autofill suggestion is previewed/suggestion, it is selected entirely in the originating field.

By changing the selection range (field.setSelectionRange(0,0);), the previewed value becomes unselected and thus will not be overwritten if the user types.

Then when the space is inserted (document.execCommand('insertText', false, ' ');), InsertTextCommand::DoApply(*1) is called. What is surprising there is that the space is inserted in the previewed value. 

Then, since this is a change that originates from the user side (vs browser side) this new value is set as the field's value, thus it is accessible in the DOM.


I am really surprised that when the space is inserted, it gets inserted in the suggested value. It seems like the data_ attribute of the Text object(*2) contains the suggested value of the field.

*1: https://cs.chromium.org/chromium/src/third_party/WebKit/Source/core/editing/commands/InsertTextCommand.cpp?dr=CSs&q=inserttextcommand&sq=package:chromium&l=255

*2: https://cs.chromium.org/chromium/src/third_party/WebKit/Source/core/dom/CharacterData.cpp?type=cs&sq=package:chromium&l=93

### yo...@chromium.org (2017-08-29)

TL;DR: To preview suggested value like placehold == do not hold suggested value in inner editor

I suggest to introduce suggested value element in shadow DOM tree like placeholder.
The content in inner editor of text control is exposed scripts and scripts can
access someway, e.g. execCommand, copy to clipboard.


### se...@chromium.org (2017-08-29)

After some investigation I don't think I could realistically make a good change guaranteed to be correct in time for M-62 (including the merge window)

Do you think you guys could take it on? 

### zk...@chromium.org (2017-08-29)

This is definitely a candidate for merge post branch. Yosin, let us know if this is something you can tackle quickly. Thanks!

### yo...@chromium.org (2017-08-30)

Addition to https://crbug.com/chromium/753645#c22, the element for suggested value in UA shadow tree is used only
for previewing value.

Once user commits, by user action, previewed suggested value should be copied
into inner editor.

https://crbug.com/chromium/753645#c23, Do you think you guys could take it on? 
No, we don't have enough bandwidth.

Since it seems the change is not small, == too short for canary testing,
fix should be in M-63.






### zk...@chromium.org (2017-09-01)

I disagree about M63 timeline. This is pretty serious as it exposes credit cards without user consent. We should be aggressive about merge ASAP.

### es...@chromium.org (2017-09-01)

+! to https://crbug.com/chromium/753645#c26. We should get a fix landed ASAP and then evaluate the feasibility of a merge; we shouldn't delay a fix on the assumption that it won't be mergeable.

### ma...@chromium.org (2017-09-01)

It's being actively worked on by sebsg@ for M62.

### se...@chromium.org (2017-09-07)

+ vasilii@

### bu...@chromium.org (2017-10-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/0727466e09c7285f3c4fe6a7974bfc68fd9bbccb

commit 0727466e09c7285f3c4fe6a7974bfc68fd9bbccb
Author: sebsg <sebsg@chromium.org>
Date: Mon Oct 02 19:57:41 2017

[Autofill] Use ShadowDom placeholder to preview suggestions.

Bug: 753645
Change-Id: Idabb4d01b45aa08a71f9fc8ad1dd89b192cfb0c5
Reviewed-on: https://chromium-review.googlesource.com/646754
Commit-Queue: Sebastien Seguin-Gagnon <sebsg@chromium.org>
Reviewed-by: Kent Tamura <tkent@chromium.org>
Cr-Commit-Position: refs/heads/master@{#505743}
[modify] https://crrev.com/0727466e09c7285f3c4fe6a7974bfc68fd9bbccb/chrome/renderer/autofill/form_autofill_browsertest.cc
[modify] https://crrev.com/0727466e09c7285f3c4fe6a7974bfc68fd9bbccb/chrome/renderer/autofill/password_autofill_agent_browsertest.cc
[add] https://crrev.com/0727466e09c7285f3c4fe6a7974bfc68fd9bbccb/third_party/WebKit/LayoutTests/fast/forms/javascript-cannot-access-suggested-value.html
[add] https://crrev.com/0727466e09c7285f3c4fe6a7974bfc68fd9bbccb/third_party/WebKit/LayoutTests/fast/forms/suggested-value-after-empty-suggested-value-expected.txt
[add] https://crrev.com/0727466e09c7285f3c4fe6a7974bfc68fd9bbccb/third_party/WebKit/LayoutTests/fast/forms/suggested-value-after-empty-suggested-value.html
[modify] https://crrev.com/0727466e09c7285f3c4fe6a7974bfc68fd9bbccb/third_party/WebKit/LayoutTests/fast/forms/suggested-value-after-setvalue-expected.txt
[modify] https://crrev.com/0727466e09c7285f3c4fe6a7974bfc68fd9bbccb/third_party/WebKit/LayoutTests/fast/forms/suggested-value-after-setvalue.html
[modify] https://crrev.com/0727466e09c7285f3c4fe6a7974bfc68fd9bbccb/third_party/WebKit/LayoutTests/fast/forms/suggested-value-expected.txt
[modify] https://crrev.com/0727466e09c7285f3c4fe6a7974bfc68fd9bbccb/third_party/WebKit/LayoutTests/fast/forms/text/input-appearance-autocomplete-expected.html
[modify] https://crrev.com/0727466e09c7285f3c4fe6a7974bfc68fd9bbccb/third_party/WebKit/LayoutTests/platform/win7/fast/forms/suggested-value-expected.txt
[modify] https://crrev.com/0727466e09c7285f3c4fe6a7974bfc68fd9bbccb/third_party/WebKit/Source/core/html/HTMLInputElement.cpp
[modify] https://crrev.com/0727466e09c7285f3c4fe6a7974bfc68fd9bbccb/third_party/WebKit/Source/core/html/HTMLInputElement.h
[modify] https://crrev.com/0727466e09c7285f3c4fe6a7974bfc68fd9bbccb/third_party/WebKit/Source/core/html/HTMLTextAreaElement.cpp
[modify] https://crrev.com/0727466e09c7285f3c4fe6a7974bfc68fd9bbccb/third_party/WebKit/Source/core/html/HTMLTextAreaElement.h
[modify] https://crrev.com/0727466e09c7285f3c4fe6a7974bfc68fd9bbccb/third_party/WebKit/Source/core/html/TextControlElement.cpp
[modify] https://crrev.com/0727466e09c7285f3c4fe6a7974bfc68fd9bbccb/third_party/WebKit/Source/core/html/TextControlElement.h
[modify] https://crrev.com/0727466e09c7285f3c4fe6a7974bfc68fd9bbccb/third_party/WebKit/Source/core/html/forms/TextFieldInputType.cpp


### bu...@chromium.org (2017-10-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/c28f832f0c87926662c1b9f7965fd7dd19d6b239

commit c28f832f0c87926662c1b9f7965fd7dd19d6b239
Author: Sebastien Seguin-Gagnon <sebsg@chromium.org>
Date: Tue Oct 03 12:40:55 2017

Revert "[Autofill] Use ShadowDom placeholder to preview suggestions."

This reverts commit 0727466e09c7285f3c4fe6a7974bfc68fd9bbccb.

Reason for revert: Makes some passwords be visible when suggested to the user.

Bug: 771097


Original change's description:
> [Autofill] Use ShadowDom placeholder to preview suggestions.
> 
> Bug: 753645
> Change-Id: Idabb4d01b45aa08a71f9fc8ad1dd89b192cfb0c5
> Reviewed-on: https://chromium-review.googlesource.com/646754
> Commit-Queue: Sebastien Seguin-Gagnon <sebsg@chromium.org>
> Reviewed-by: Kent Tamura <tkent@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#505743}

TBR=yosin@chromium.org,tkent@chromium.org,sebsg@chromium.org

Change-Id: I3a874ea052f598724831bdfcf0e16576a09353b4
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Bug: 753645
Reviewed-on: https://chromium-review.googlesource.com/697644
Reviewed-by: Sebastien Seguin-Gagnon <sebsg@chromium.org>
Commit-Queue: Sebastien Seguin-Gagnon <sebsg@chromium.org>
Cr-Commit-Position: refs/heads/master@{#506011}
[modify] https://crrev.com/c28f832f0c87926662c1b9f7965fd7dd19d6b239/chrome/renderer/autofill/form_autofill_browsertest.cc
[modify] https://crrev.com/c28f832f0c87926662c1b9f7965fd7dd19d6b239/chrome/renderer/autofill/password_autofill_agent_browsertest.cc
[delete] https://crrev.com/86b13b4626266c45ee364474bcf86208d4e2e4a2/third_party/WebKit/LayoutTests/fast/forms/javascript-cannot-access-suggested-value.html
[delete] https://crrev.com/86b13b4626266c45ee364474bcf86208d4e2e4a2/third_party/WebKit/LayoutTests/fast/forms/suggested-value-after-empty-suggested-value-expected.txt
[delete] https://crrev.com/86b13b4626266c45ee364474bcf86208d4e2e4a2/third_party/WebKit/LayoutTests/fast/forms/suggested-value-after-empty-suggested-value.html
[modify] https://crrev.com/c28f832f0c87926662c1b9f7965fd7dd19d6b239/third_party/WebKit/LayoutTests/fast/forms/suggested-value-after-setvalue-expected.txt
[modify] https://crrev.com/c28f832f0c87926662c1b9f7965fd7dd19d6b239/third_party/WebKit/LayoutTests/fast/forms/suggested-value-after-setvalue.html
[modify] https://crrev.com/c28f832f0c87926662c1b9f7965fd7dd19d6b239/third_party/WebKit/LayoutTests/fast/forms/suggested-value-expected.txt
[modify] https://crrev.com/c28f832f0c87926662c1b9f7965fd7dd19d6b239/third_party/WebKit/LayoutTests/fast/forms/text/input-appearance-autocomplete-expected.html
[modify] https://crrev.com/c28f832f0c87926662c1b9f7965fd7dd19d6b239/third_party/WebKit/LayoutTests/platform/win7/fast/forms/suggested-value-expected.txt
[modify] https://crrev.com/c28f832f0c87926662c1b9f7965fd7dd19d6b239/third_party/WebKit/Source/core/html/HTMLInputElement.cpp
[modify] https://crrev.com/c28f832f0c87926662c1b9f7965fd7dd19d6b239/third_party/WebKit/Source/core/html/HTMLInputElement.h
[modify] https://crrev.com/c28f832f0c87926662c1b9f7965fd7dd19d6b239/third_party/WebKit/Source/core/html/HTMLTextAreaElement.cpp
[modify] https://crrev.com/c28f832f0c87926662c1b9f7965fd7dd19d6b239/third_party/WebKit/Source/core/html/HTMLTextAreaElement.h
[modify] https://crrev.com/c28f832f0c87926662c1b9f7965fd7dd19d6b239/third_party/WebKit/Source/core/html/TextControlElement.cpp
[modify] https://crrev.com/c28f832f0c87926662c1b9f7965fd7dd19d6b239/third_party/WebKit/Source/core/html/TextControlElement.h
[modify] https://crrev.com/c28f832f0c87926662c1b9f7965fd7dd19d6b239/third_party/WebKit/Source/core/html/forms/TextFieldInputType.cpp


### aw...@google.com (2017-10-05)

[Empty comment from Monorail migration]

### se...@chromium.org (2017-10-06)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-10-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/962a26fe7d0355903d4c2721faddcbe51e0ee45c

commit 962a26fe7d0355903d4c2721faddcbe51e0ee45c
Author: sebsg <sebsg@chromium.org>
Date: Thu Oct 19 01:30:20 2017

[Autofill] Use ShadowDOM placeholder to preview suggestions.

The first patch is a re-upload of
https://chromium-review.googlesource.com/c/chromium/src/+/646754

The follow-up patches will add some modifcations on how we preview
username and password suggestions.

The suggestions will be in black text, and the password suggestions
should be hidden behind dots.

Bug: 753645
Change-Id: I1d28ea47f443fc40a1cddf2cdef6b1ec86c4491e
Tbr: tkent@chromium.org
Reviewed-on: https://chromium-review.googlesource.com/702056
Commit-Queue: Sebastien Seguin-Gagnon <sebsg@chromium.org>
Reviewed-by: Yoshifumi Inoue <yosin@chromium.org>
Reviewed-by: Roger McFarlane <rogerm@chromium.org>
Cr-Commit-Position: refs/heads/master@{#509961}
[modify] https://crrev.com/962a26fe7d0355903d4c2721faddcbe51e0ee45c/chrome/renderer/autofill/form_autofill_browsertest.cc
[modify] https://crrev.com/962a26fe7d0355903d4c2721faddcbe51e0ee45c/chrome/renderer/autofill/password_autofill_agent_browsertest.cc
[add] https://crrev.com/962a26fe7d0355903d4c2721faddcbe51e0ee45c/third_party/WebKit/LayoutTests/fast/forms/javascript-cannot-access-suggested-value.html
[add] https://crrev.com/962a26fe7d0355903d4c2721faddcbe51e0ee45c/third_party/WebKit/LayoutTests/fast/forms/suggested-value-after-empty-suggested-value-expected.txt
[add] https://crrev.com/962a26fe7d0355903d4c2721faddcbe51e0ee45c/third_party/WebKit/LayoutTests/fast/forms/suggested-value-after-empty-suggested-value.html
[modify] https://crrev.com/962a26fe7d0355903d4c2721faddcbe51e0ee45c/third_party/WebKit/LayoutTests/fast/forms/suggested-value-after-setvalue-expected.txt
[modify] https://crrev.com/962a26fe7d0355903d4c2721faddcbe51e0ee45c/third_party/WebKit/LayoutTests/fast/forms/suggested-value-after-setvalue.html
[modify] https://crrev.com/962a26fe7d0355903d4c2721faddcbe51e0ee45c/third_party/WebKit/LayoutTests/fast/forms/suggested-value-expected.txt
[modify] https://crrev.com/962a26fe7d0355903d4c2721faddcbe51e0ee45c/third_party/WebKit/LayoutTests/fast/forms/text/input-appearance-autocomplete-expected.html
[add] https://crrev.com/962a26fe7d0355903d4c2721faddcbe51e0ee45c/third_party/WebKit/LayoutTests/fast/forms/text/password-input-suggested-value-appearance-expected.html
[add] https://crrev.com/962a26fe7d0355903d4c2721faddcbe51e0ee45c/third_party/WebKit/LayoutTests/fast/forms/text/password-input-suggested-value-appearance.html
[modify] https://crrev.com/962a26fe7d0355903d4c2721faddcbe51e0ee45c/third_party/WebKit/LayoutTests/platform/win7/fast/forms/suggested-value-expected.txt
[modify] https://crrev.com/962a26fe7d0355903d4c2721faddcbe51e0ee45c/third_party/WebKit/Source/core/css/html.css
[modify] https://crrev.com/962a26fe7d0355903d4c2721faddcbe51e0ee45c/third_party/WebKit/Source/core/html/forms/HTMLInputElement.cpp
[modify] https://crrev.com/962a26fe7d0355903d4c2721faddcbe51e0ee45c/third_party/WebKit/Source/core/html/forms/HTMLInputElement.h
[modify] https://crrev.com/962a26fe7d0355903d4c2721faddcbe51e0ee45c/third_party/WebKit/Source/core/html/forms/HTMLTextAreaElement.cpp
[modify] https://crrev.com/962a26fe7d0355903d4c2721faddcbe51e0ee45c/third_party/WebKit/Source/core/html/forms/HTMLTextAreaElement.h
[modify] https://crrev.com/962a26fe7d0355903d4c2721faddcbe51e0ee45c/third_party/WebKit/Source/core/html/forms/TextControlElement.cpp
[modify] https://crrev.com/962a26fe7d0355903d4c2721faddcbe51e0ee45c/third_party/WebKit/Source/core/html/forms/TextControlElement.h
[modify] https://crrev.com/962a26fe7d0355903d4c2721faddcbe51e0ee45c/third_party/WebKit/Source/core/html/forms/TextFieldInputType.cpp


### se...@chromium.org (2017-10-30)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-10-31)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-10-31)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-11-06)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2017-11-06)

Nice one! The VRP panel has rewarded $1,000 for this. Also, how would you like to be credited in release notes?  Cheers!

### st...@gmail.com (2017-11-06)

Thanks! Could you credit me as: Paul Stone of Context Information Security

### aw...@chromium.org (2017-11-09)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-12-15)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-12-15)

This bug requires manual review: Reverts referenced in bugdroid comments after merge request.
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), kbleicher@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### se...@chromium.org (2017-12-15)

I don't know why the merge request was added, it should have landed in M-64 initially.

### aw...@google.com (2018-01-22)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-01-24)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-02-06)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### aw...@google.com (2018-10-05)

[Empty comment from Monorail migration]

### is...@google.com (2018-10-05)

This issue was migrated from crbug.com/chromium/753645?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail blocking: crbug.com/chromium/772433]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40088648)*
