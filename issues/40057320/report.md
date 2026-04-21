# Chrome downgrades long-running requests from HTTPS to HTTP after 3 s.

| Field | Value |
|-------|-------|
| **Issue ID** | [40057320](https://issues.chromium.org/issues/40057320) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Internals>Network, UI>Browser>Omnibox |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | [Deleted User] |
| **Assignee** | me...@chromium.org |
| **Created** | 2021-09-20 |
| **Bounty** | $3,000.00 |

## Description

Chrome Version : 93.0.4577.82 (Official Build) (x86\_64)  

**URLs (if applicable) :**  

**Other browsers tested:**  

Add OK or FAIL, along with the version, after other browsers where you  

**have tested this issue:**  

Safari: (different behaviour altogether)  

Firefox: OK  

Edge: Not tested

**What steps will reproduce the problem?**  

**(1)** Open a new incognito window  

**(2)** Create a new throttling profile in the network tab with settings (1.0 MBit/s, 1.0 MBit/s., 4000 ms) and set it to being used  

**(3)** With network tab open, go to <https://example.com> and verify that in some cases, Chrome waits 3 s, then downgrades the https request to <http://example.com>. You might have to try several times (for me now it took 2 tries).

**What is the expected result?**  

That the browser waits for the response (even if it takes time) or that it times out.

**What happens instead?**  

Chrome cancels the first https request after 3 seconds and triggers a new request to the same URL but with http.

**Please provide any additional information below. Attach a screenshot if**  

**possible.**

This happened in a non-toy scenario for me with a site that only has https. Then Chrome attempts to switch to http and is then redirected back to https. The second time around, Chrome, correctly waits for the result as it should have done the first time (see screenshot, it says "failed" on the second attempt at https because the endpoint returns 404 after some waiting time so that is correct).

There is a Stack Overflow thread on this: <https://stackoverflow.com/questions/68492321/chrome-cancels-url-request-after-exactly-3-seconds>

I don't know if this is particularly related to https or subset of some larger pattern / problem.

**For graphics-related bugs, please copy/paste the contents of the about:gpu**  

**page at the end of this report.**

## Attachments

- [Screenshot 2021-09-20 at 08.48.38.png](attachments/Screenshot 2021-09-20 at 08.48.38.png) (image/png, 43.4 KB)

## Timeline

### ve...@chromium.org (2021-09-20)

[Empty comment from Monorail migration]

### dt...@chromium.org (2021-09-20)

[Empty comment from Monorail migration]

[Monorail components: Internals>Network]

### mm...@chromium.org (2021-09-21)

The network stack doesn't downgrade HTTPS to HTTP unless there's an explicit redirect.  Nor does it time out requests after 3 seconds.

That three second delay sounds suspicious, though - that's exactly the delay the omnibox uses before trying HTTP, when you enter a domain name without a scheme.  Maybe that's incorrectly triggering when an HTTPS URL is entered directly?

[+meacer]:  Could the work on https://crbug.com/chromium/1141691 have caused this?

I'm labelling this a security issue - using HTTP instead of HTTPS seems at least a high severity issue to me, assuming this report is accurate (and given the NetLog in the linked stackoverflow issue, that seems highly likely to me, though I haven't attempted to repro).

[Monorail components: UI>Browser>Omnibox]

### [Deleted User] (2021-09-21)

[Empty comment from Monorail migration]

### mm...@chromium.org (2021-09-21)

[Elias]:  And just to confirm, you are entering "https://example.com/" in the omnibox, and not just "example.com", or initiating the navigation some other way?

### [Deleted User] (2021-09-21)

That's right, I explicitly type https://example.com (and the same for my own domain where the same problem occurs). I also inspect the entries in the network tab to verify that the first request is to https and the second is not. I have also looked into returned headers and used curl to see if the server sends something else weird in return but it looks like a regular response -> https negotiation and then the connection remains open because it is a slow-running request. After 3.00 s., Chrome cancels the request and tries http instead (as I said, happens with a 50%+ probability but there ARE cases where Chrome correctly waits for the response instead).

### mm...@chromium.org (2021-09-21)

I've tried reproducing in All/TypedNavigationUpgradeThrottleFastTimeoutBrowserTest.UrlTypedWithoutScheme_SlowHttps_ShouldFallback/1 (after fixing a bug in how it mocks timeouts), and am not getting the downgrade behavior when navigating directly to an HTTPS URL - instead, it just hangs, as expected.  Maybe there's something else going on.

### mm...@chromium.org (2021-09-21)

[meacer]:  Going to go ahead and assign this to you, because that 3 second delay is very suspicious, and you've both touched the relevant omnibox code, and are an SSL person.

### aj...@google.com (2021-09-22)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-22)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-22)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### me...@chromium.org (2021-09-24)

I can repro. This happens in the following case:

1. Set up throttling as described in https://crbug.com/chromium/1251065#c0
2. Type https://example.com. This will load https://example.com.
3. Focus the omnibox and hit enter
4. This will wait 3 seconds, then start loading http://example.com

What's happening here is that the autocomplete input text is returned as "example.com" in the second navigation (instead of "https://example.com"). This causes omnibox to consider the URL upgraded to HTTPS which causes TypedNavigationUpgradeThrottle to kick in. The throttle's timer times out after 3 seconds and starts loading the fallback URL which is http.

### me...@google.com (2021-09-27)

Tentative fix at https://chromium-review.googlesource.com/c/chromium/src/+/3188350

### me...@chromium.org (2021-09-28)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-09-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/d5274c7c1373d9368d3fe37d84f7169fadf8ef38

commit d5274c7c1373d9368d3fe37d84f7169fadf8ef38
Author: Mustafa Emre Acer <meacer@chromium.org>
Date: Thu Sep 30 21:05:48 2021

Don't attempt to upgrade zero-suggest autocomplete inputs to HTTPS

This CL fixes an issue with the Defaulting Typed Navigations to HTTPS
feature. Consider the following scenario:

1. User types https://example.com
2. Navigation completes successfully
3. User clicks the omnibox and hits enter
4. Omnibox attempts to upgrade this navigation to HTTPS.

In step 3, OmniboxEditModel::StartZeroSuggestRequest() creates an
AutocompleteInput using its client's
ShouldDefaultTypedNavigationsToHttps() value and "example.com" as the
input text. This causes AutocompleteInput to enable the HTTP fallback
logic if the HTTPS navigation times out, thus potentially downgrading
the connection.

This CL fixes this by disabling HTTPS upgrades when starting a zero
suggest request.

Bug: 1251065
Change-Id: I7ab007f7334b1366806b01231921a248857d9e19
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3188350
Commit-Queue: Mustafa Emre Acer <meacer@chromium.org>
Reviewed-by: Justin Donnelly <jdonnelly@chromium.org>
Cr-Commit-Position: refs/heads/main@{#926926}

[modify] https://crrev.com/d5274c7c1373d9368d3fe37d84f7169fadf8ef38/testing/buildbot/filters/linux-lacros.interactive_ui_tests.filter
[modify] https://crrev.com/d5274c7c1373d9368d3fe37d84f7169fadf8ef38/chrome/browser/ui/views/omnibox/omnibox_view_views_browsertest.cc
[modify] https://crrev.com/d5274c7c1373d9368d3fe37d84f7169fadf8ef38/testing/buildbot/filters/ozone-linux.interactive_ui_tests_wayland.filter
[modify] https://crrev.com/d5274c7c1373d9368d3fe37d84f7169fadf8ef38/components/omnibox/browser/omnibox_edit_model.cc


### me...@chromium.org (2021-09-30)

This should be fixed. I'll check on Canary as soon as it lands there.

### gi...@appspot.gserviceaccount.com (2021-10-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/1c6d167460b43a7498d393af667c9efb6227e137

commit 1c6d167460b43a7498d393af667c9efb6227e137
Author: Fergal Daly <fergal@chromium.org>
Date: Fri Oct 01 03:43:22 2021

Revert "Don't attempt to upgrade zero-suggest autocomplete inputs to HTTPS"

This reverts commit d5274c7c1373d9368d3fe37d84f7169fadf8ef38.

Reason for revert: introduced flaky test on Mac

Original change's description:
> Don't attempt to upgrade zero-suggest autocomplete inputs to HTTPS
>
> This CL fixes an issue with the Defaulting Typed Navigations to HTTPS
> feature. Consider the following scenario:
>
> 1. User types https://example.com
> 2. Navigation completes successfully
> 3. User clicks the omnibox and hits enter
> 4. Omnibox attempts to upgrade this navigation to HTTPS.
>
> In step 3, OmniboxEditModel::StartZeroSuggestRequest() creates an
> AutocompleteInput using its client's
> ShouldDefaultTypedNavigationsToHttps() value and "example.com" as the
> input text. This causes AutocompleteInput to enable the HTTP fallback
> logic if the HTTPS navigation times out, thus potentially downgrading
> the connection.
>
> This CL fixes this by disabling HTTPS upgrades when starting a zero
> suggest request.
>
> Bug: 1251065
> Change-Id: I7ab007f7334b1366806b01231921a248857d9e19
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3188350
> Commit-Queue: Mustafa Emre Acer <meacer@chromium.org>
> Reviewed-by: Justin Donnelly <jdonnelly@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#926926}

Bug: 1251065,1254919
Change-Id: Id5d1be1e58039bdbc7e66ef529a44b5e6eb92dca
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3197852
Auto-Submit: Fergal Daly <fergal@chromium.org>
Owners-Override: Fergal Daly <fergal@google.com>
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#927092}

[modify] https://crrev.com/1c6d167460b43a7498d393af667c9efb6227e137/testing/buildbot/filters/linux-lacros.interactive_ui_tests.filter
[modify] https://crrev.com/1c6d167460b43a7498d393af667c9efb6227e137/chrome/browser/ui/views/omnibox/omnibox_view_views_browsertest.cc
[modify] https://crrev.com/1c6d167460b43a7498d393af667c9efb6227e137/testing/buildbot/filters/ozone-linux.interactive_ui_tests_wayland.filter
[modify] https://crrev.com/1c6d167460b43a7498d393af667c9efb6227e137/components/omnibox/browser/omnibox_edit_model.cc


### me...@chromium.org (2021-10-01)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-10-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/4cf52003e7e4c17790a6d91ae6391255ace25192

commit 4cf52003e7e4c17790a6d91ae6391255ace25192
Author: Mustafa Emre Acer <meacer@chromium.org>
Date: Tue Oct 05 20:34:42 2021

[Reland] Don't attempt to upgrade zero-suggest autocomplete inputs to HTTPS

This CL fixes an issue with the Defaulting Typed Navigations to HTTPS
feature. Consider the following scenario:

1. User types https://example.com
2. Navigation completes successfully
3. User clicks the omnibox and hits enter
4. Omnibox attempts to upgrade this navigation to HTTPS.

In step 3, OmniboxEditModel::StartZeroSuggestRequest() creates an
AutocompleteInput using its client's
ShouldDefaultTypedNavigationsToHttps() value and "example.com" as the
input text. This causes AutocompleteInput to enable the HTTP fallback
logic if the HTTPS navigation times out, thus potentially downgrading
the connection.

This CL fixes this by disabling HTTPS upgrades when starting a zero
suggest request.

Bug: 1251065
Change-Id: I7bd72d661f7d9e9b0dca9df0e774e9dd0bcdfa09
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3188350
Commit-Queue: Mustafa Emre Acer <meacer@chromium.org>
Reviewed-by: Justin Donnelly <jdonnelly@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#926926}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3203050
Cr-Commit-Position: refs/heads/main@{#928315}

[modify] https://crrev.com/4cf52003e7e4c17790a6d91ae6391255ace25192/testing/buildbot/filters/linux-lacros.interactive_ui_tests.filter
[modify] https://crrev.com/4cf52003e7e4c17790a6d91ae6391255ace25192/chrome/browser/ui/views/omnibox/omnibox_view_views_browsertest.cc
[modify] https://crrev.com/4cf52003e7e4c17790a6d91ae6391255ace25192/testing/buildbot/filters/ozone-linux.interactive_ui_tests_wayland.filter
[modify] https://crrev.com/4cf52003e7e4c17790a6d91ae6391255ace25192/components/omnibox/browser/omnibox_edit_model.cc


### gi...@appspot.gserviceaccount.com (2021-10-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/24feb753b4461450404cfa079fc0bc5b12f59f33

commit 24feb753b4461450404cfa079fc0bc5b12f59f33
Author: Ian Clelland <iclelland@chromium.org>
Date: Thu Oct 07 17:06:37 2021

Revert "[Reland] Don't attempt to upgrade zero-suggest autocomplete inputs to HTTPS"

This reverts commit 4cf52003e7e4c17790a6d91ae6391255ace25192.

Reason for revert: This has been causing flaky tests since right after landing on Mac 10.13 and 10.15 bots :(

See 10.13 tests:
https://ci.chromium.org/p/chromium/builders/ci/Mac10.13%20Tests/42763
up to
https://ci.chromium.org/p/chromium/builders/ci/Mac10.13%20Tests/42837
and 10.15 tests:
https://ci.chromium.org/p/chromium/builders/ci/Mac10.15%20Tests/15799
up to
https://ci.chromium.org/p/chromium/builders/ci/Mac10.15%20Tests/15863

Original change's description:
> [Reland] Don't attempt to upgrade zero-suggest autocomplete inputs to HTTPS
>
> This CL fixes an issue with the Defaulting Typed Navigations to HTTPS
> feature. Consider the following scenario:
>
> 1. User types https://example.com
> 2. Navigation completes successfully
> 3. User clicks the omnibox and hits enter
> 4. Omnibox attempts to upgrade this navigation to HTTPS.
>
> In step 3, OmniboxEditModel::StartZeroSuggestRequest() creates an
> AutocompleteInput using its client's
> ShouldDefaultTypedNavigationsToHttps() value and "example.com" as the
> input text. This causes AutocompleteInput to enable the HTTP fallback
> logic if the HTTPS navigation times out, thus potentially downgrading
> the connection.
>
> This CL fixes this by disabling HTTPS upgrades when starting a zero
> suggest request.
>
> Bug: 1251065
> Change-Id: I7bd72d661f7d9e9b0dca9df0e774e9dd0bcdfa09
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3188350
> Commit-Queue: Mustafa Emre Acer <meacer@chromium.org>
> Reviewed-by: Justin Donnelly <jdonnelly@chromium.org>
> Cr-Original-Commit-Position: refs/heads/main@{#926926}
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3203050
> Cr-Commit-Position: refs/heads/main@{#928315}

Bug: 1251065
Change-Id: Ic4f543ea76ee0abbb8f9e5399cd89fca1ed2dd50
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3211514
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Reviewed-by: Ian Clelland <iclelland@chromium.org>
Reviewed-by: Peter Beverloo <peter@chromium.org>
Auto-Submit: Ian Clelland <iclelland@chromium.org>
Owners-Override: Ian Clelland <iclelland@chromium.org>
Commit-Queue: Peter Beverloo <peter@chromium.org>
Cr-Commit-Position: refs/heads/main@{#929258}

[modify] https://crrev.com/24feb753b4461450404cfa079fc0bc5b12f59f33/testing/buildbot/filters/linux-lacros.interactive_ui_tests.filter
[modify] https://crrev.com/24feb753b4461450404cfa079fc0bc5b12f59f33/chrome/browser/ui/views/omnibox/omnibox_view_views_browsertest.cc
[modify] https://crrev.com/24feb753b4461450404cfa079fc0bc5b12f59f33/testing/buildbot/filters/ozone-linux.interactive_ui_tests_wayland.filter
[modify] https://crrev.com/24feb753b4461450404cfa079fc0bc5b12f59f33/components/omnibox/browser/omnibox_edit_model.cc


### me...@chromium.org (2021-12-03)

There were a few landings & reverts, so just noting that this is still not fixed.

### gi...@appspot.gserviceaccount.com (2022-01-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/6023d60f712fabccbb9bb0dc885a31ae7b3bee06

commit 6023d60f712fabccbb9bb0dc885a31ae7b3bee06
Author: Mustafa Emre Acer <meacer@chromium.org>
Date: Fri Jan 07 17:28:18 2022

[Reland] Don't attempt to upgrade zero-suggest autocomplete inputs to HTTPS

This CL fixes an issue with the Defaulting Typed Navigations to HTTPS
feature. Consider the following scenario:

1. User types https://example.com
2. Navigation completes successfully
3. User clicks the omnibox and hits enter
4. Omnibox attempts to upgrade this navigation to HTTPS.

In step 3, OmniboxEditModel::StartZeroSuggestRequest() creates an
AutocompleteInput using its client's
ShouldDefaultTypedNavigationsToHttps() value and "example.com" as the
input text. This causes AutocompleteInput to enable the HTTP fallback
logic if the HTTPS navigation times out, thus potentially downgrading
the connection.

This CL fixes this by disabling HTTPS upgrades when starting a zero
suggest request.

Bug: 1251065
Change-Id: I70a00f00bd646058fd62d31e4da572971bde0dbb
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3188350
Commit-Queue: Mustafa Emre Acer <meacer@chromium.org>
Reviewed-by: Justin Donnelly <jdonnelly@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/main@{#926926}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3203050
Cr-Original-Commit-Position: refs/heads/main@{#928315}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3370903
Cr-Commit-Position: refs/heads/main@{#956558}

[modify] https://crrev.com/6023d60f712fabccbb9bb0dc885a31ae7b3bee06/testing/buildbot/filters/linux-lacros.interactive_ui_tests.filter
[modify] https://crrev.com/6023d60f712fabccbb9bb0dc885a31ae7b3bee06/chrome/browser/ui/views/omnibox/omnibox_view_views_browsertest.cc
[modify] https://crrev.com/6023d60f712fabccbb9bb0dc885a31ae7b3bee06/testing/buildbot/filters/ozone-linux.interactive_ui_tests_wayland.filter
[modify] https://crrev.com/6023d60f712fabccbb9bb0dc885a31ae7b3bee06/components/omnibox/browser/omnibox_edit_model.cc


### me...@chromium.org (2022-01-11)

Seems like this finally stuck. Marking as fixed.

### [Deleted User] (2022-01-12)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-12)

[Empty comment from Monorail migration]

### am...@google.com (2022-03-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-03-11)

Congratulations! The VRP Panel has decided to award you $3,000 for this report. A member of our finance team will be in touch with you soon to arrange payment. In the meantime, please let us know the name, handle/tag, or other identifier you would like us to use to acknowledge you for reporting this issue. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2022-03-11)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-14)

Oh how nice! Thank you! You can tag it in any way you'd like with elias@lousseief.com (NOT the mail address of this report which is associated with my current employer) and / or fast-reflexes (which is my Github account and the name I use in forums / when releasing software etc...).

Thanks for accepting the report and taking it seriously! :)

### [Deleted User] (2022-04-19)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-12-13)

For some reason the automation did not scoop up the final reland in release notes / acknowledgement and CVE processing when the fix was released in stable M99 release (v.99.0.4844.51) - sincere apologies for that, Elias! 
Labeling accordingly so can get scooped up and that resolved soon! 

### pg...@google.com (2023-02-12)

[Empty comment from Monorail migration]

### pg...@google.com (2023-07-28)

[Empty comment from Monorail migration]

### pg...@google.com (2023-07-28)

[Empty comment from Monorail migration]

### is...@google.com (2023-07-28)

This issue was migrated from crbug.com/chromium/1251065?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Internals>Network, UI>Browser>Omnibox]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057320)*
