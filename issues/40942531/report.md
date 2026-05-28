# Security: Origin spoof caused by navigation that doesn't paint any content

| Field | Value |
|-------|-------|
| **Issue ID** | [40942531](https://issues.chromium.org/issues/40942531) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Paint, UI>Browser>Navigation, UI>Browser>Omnibox |
| **Platforms** | Mac, Windows, ChromeOS |
| **Reporter** | st...@gmail.com |
| **Assignee** | vm...@chromium.org |
| **Created** | 2023-11-14 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

If a navigation happens but doesn't render any content (by trying to navigate to an invalid URL), it will keep displaying the rendered content of the previous page, even if it's a cross-origin cross-site page, for 4 seconds. The attacker's page (with a reference to the window) can keep repeating the navigation to prolong the content spoof. The page will not be interactive, but the attacker can choose to display any content they want.

The only prerequisite is that the victim page performs a JavaScript navigation to an invalid URL or does something similar that causes no content to be painted. For instance, an open redirect in google.com/url? was vulnerable to this when I tested it a couple of weeks ago (seems that something has changed in the response that causes it not to work now).

Tested this on Windows and Android, it seems likely that it will work on other OSs as well. When reproducing this, the attacker's real origin might flicker for a split second when the navigation is happening. I noticed that tweaking the timing can make this less noticeable.

**VERSION**  

Chrome Version: 119.0.6045.124  

Operating System: Windows 11, Android 14

**REPRODUCTION CASE**  

Host the attacker and victim PoC on a different origin.

1. Open attacker-poc.html and click to open a new tab
2. Notice the tab shows victim's origin in the URL bar but displays content from the attacker

**CREDIT INFORMATION**  

Reporter credit: Thomas Orlita

## Attachments

- [poc.webm](attachments/poc.webm) (video/webm, 254.6 KB)
- [victim-poc.html](attachments/victim-poc.html) (text/plain, 72 B)
- [attacker-poc.html](attachments/attacker-poc.html) (text/plain, 409 B)
- [attacker-spoof.html](attachments/attacker-spoof.html) (text/plain, 162 B)
- [trace_paint_holding_bug.json.gz](attachments/trace_paint_holding_bug.json.gz) (application/octet-stream, 4.6 MB)

## Timeline

### [Deleted User] (2023-11-14)

[Empty comment from Monorail migration]

### ar...@google.com (2023-11-15)

(current security sheriff here)

Thanks!

I wasn't able to reproduce on M119. I hosted the attacker and victim website. We can test on:
http://cooperative-showy-gojirasaurus.glitch.me/

I observed the correct URL was displayed, on both the victim and attacker documents.
I tested on Android. On Linux, there was a prompt asking me what application should handle the intent.

Am I doing it wrong somehow, or missing something?

+creis@ FYI, in case you might be able to reproduce on your side.

[Monorail components: UI>Browser>Navigation UI>Browser>Omnibox]

### st...@gmail.com (2023-11-15)

Hi Arthur,

The reason the PoC on Glitch doesn't reproduce is that the victim page creates a paint due to the "This is the victim website: sepia-snapdragon-jasper" paragraph being rendered.

I am hosting the PoC on https://attacker--poc--intent-paint--origin-spoof.cr.vuln.foo -- I hope this helps with reproducing the bug.

### [Deleted User] (2023-11-15)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cr...@chromium.org (2023-11-15)

I can confirm https://attacker--poc--intent-paint--origin-spoof.cr.vuln.foo/ works on Mac.

This is a known issue / tradeoff with cross-origin paint holding, as referenced at https://chromium.googlesource.com/chromium/src/+/main/docs/security/overlay-policy.md.  Bugs like this are usually marked WontFix, given several mitigations: it depends on the victim page having a delayed paint (which makes this rarely successful in practice), the spoof content is non-interactive, and there's a 4 second timer limiting how long it (usually) can be displayed.

This bug shows that it's possible to work around the 4 second timer by causing more navigations from another window (either using history.back() as in the repro, or simply by doing repeated new navigations in the popup).  In theory the victim could adopt Cross-Origin-Opener-Policy to prevent being navigated from a cross-origin opener, but that shouldn't be necessary.

khushalsagar@: You've discussed a few ideas for improving this paint holding and timer in the past, and have written PoCs showing other ways that a page might delay painting (e.g., https://crbug.com/chromium/1447077).  Any thoughts on how to make the repeated navigation case described here into less of a problem?

[Monorail components: Blink>Paint]

### kh...@chromium.org (2023-11-15)

> The attacker's page (with a reference to the window) can keep repeating the navigation to prolong the content spoof.

This took me by surprise. I thought we already have mitigation for this case. Say we navigated from A to B which did paint holding. If B's content rendering timeout hasn't triggered yet, it's primary ID will be set to its own content and its fallback ID will be set to stale paint from A. If its a cross-site navigation then we must have different RWHVs for A and B. As such A and B's SurfaceIDs will have a different FrameSinkID. So the primary and fallback on B at this point should have a different FrameSinkID.

Now if a navigation is initiated to C, we need to take a SurfaceID from B to be used as stale paint. The logic picks B's primary ID if B's primary and fallback IDs have a different FrameSinkID: https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/delegated_frame_host.cc;l=620;drc=42f0b9c4f60f67676d9096b3e94df9fd47f568f4. This is equivalent to saying: "If B's fallback content comes from a different process, don't keep using the stale paint".

So when navigating to C, we should have cleared A's stale paint. The logic above is clearly not working and I'm not sure what's going on in the navigation stack in this case. I see a batch of 3 Navigation requests every 4 seconds to trigger the bug:

#1
{browser_initiated: false,
 frame_tree_node: {current_frame_host: {browsing_context_state: "0x0",
                                        frame_tree_node_id: 4,
                                        frame_type: "PRIMARY_MAIN_FRAME",
                                        lifecycle_state: "ACTIVE",
                                        origin: https://victim--poc--intent-paint--origin-spoof.cr.vuln.foo,
                                        process: {browser_context: {id: "9DFC1285B9F8CCC701F8A717B64B1458"},
                                                  child_process_id: 71759,
                                                  id: 9,
                                                  process_lock: "{ https://vuln.foo/ }"},
                                        render_frame_host_id: {process_id: 9,
                                                               routing_id: 5},
                                        site_instance: {active_rfh_count: 2,
                                                        browsing_instance_id: 5,
                                                        has_process: true,
                                                        is_default: false,
                                                        related_active_contents_count: 2,
                                                        site_info: {is_fenced: false,
                                                                    is_guest: false,
                                                                    is_sandboxed: false,
                                                                    process_lock_url: https://vuln.foo/,
                                                                    requires_origin_keyed_process: false,
                                                                    site_url: https://vuln.foo/},
                                                        site_instance_group: {active_frame_count: 2,
                                                                              process: {browser_context: {id: "9DFC1285B9F8CCC701F8A717B64B1458"},
                                                                                        child_process_id: 71759,
                                                                                        id: 9,
                                                                                        process_lock: "{ https://vuln.foo/ }"},
                                                                              site_instance_group_id: 3},
                                                        site_instance_id: 5},
                                        url: https://victim--poc--intent-paint--origin-spoof.cr.vuln.foo/},
                   frame_tree_node_id: 4,
                   is_main_frame: true,
                   speculative_frame_host: "0x0"},
 from_begin_navigation: true,
 has_committed: false,
 is_error_page: false,
 is_synchronous_renderer_commit: false,
 navigation_id: 21,
 navigation_type: "DIFFERENT_DOCUMENT",
 net_error: 0,
 reload_type: 0,
 state: 0,
 url: https://attacker--poc--intent-paint--origin-spoof.cr.vuln.foo/spoof.html}

#2
{browser_initiated: false,
 frame_tree_node: {current_frame_host: {browsing_context_state: "0x0",
                                        frame_tree_node_id: 4,
                                        frame_type: "PRIMARY_MAIN_FRAME",
                                        lifecycle_state: "ACTIVE",
                                        origin: https://attacker--poc--intent-paint--origin-spoof.cr.vuln.foo,
                                        process: {browser_context: {id: "9DFC1285B9F8CCC701F8A717B64B1458"},
                                                  child_process_id: 71759,
                                                  id: 9,
                                                  process_lock: "{ https://vuln.foo/ }"},
                                        render_frame_host_id: {process_id: 9,
                                                               routing_id: 5},
                                        site_instance: {active_rfh_count: 2,
                                                        browsing_instance_id: 5,
                                                        has_process: true,
                                                        is_default: false,
                                                        related_active_contents_count: 2,
                                                        site_info: {is_fenced: false,
                                                                    is_guest: false,
                                                                    is_sandboxed: false,
                                                                    process_lock_url: https://vuln.foo/,
                                                                    requires_origin_keyed_process: false,
                                                                    site_url: https://vuln.foo/},
                                                        site_instance_group: {active_frame_count: 2,
                                                                              process: {browser_context: {id: "9DFC1285B9F8CCC701F8A717B64B1458"},
                                                                                        child_process_id: 71759,
                                                                                        id: 9,
                                                                                        process_lock: "{ https://vuln.foo/ }"},
                                                                              site_instance_group_id: 3},
                                                        site_instance_id: 5},
                                        url: https://attacker--poc--intent-paint--origin-spoof.cr.vuln.foo/spoof.html},
                   frame_tree_node_id: 4,
                   is_main_frame: true,
                   speculative_frame_host: "0x0"},
 from_begin_navigation: false,
 has_committed: false,
 is_error_page: false,
 is_synchronous_renderer_commit: false,
 navigation_id: 22,
 navigation_type: "HISTORY_DIFFERENT_DOCUMENT",
 net_error: 0,
 reload_type: 0,
 state: 0,
 url: https://victim--poc--intent-paint--origin-spoof.cr.vuln.foo/}

#3
{browser_initiated: false,
 frame_tree_node: {current_frame_host: {browsing_context_state: "0x0",
                                        frame_tree_node_id: 4,
                                        frame_type: "PRIMARY_MAIN_FRAME",
                                        lifecycle_state: "ACTIVE",
                                        origin: https://victim--poc--intent-paint--origin-spoof.cr.vuln.foo,
                                        process: {browser_context: {id: "9DFC1285B9F8CCC701F8A717B64B1458"},
                                                  child_process_id: 71759,
                                                  id: 9,
                                                  process_lock: "{ https://vuln.foo/ }"},
                                        render_frame_host_id: {process_id: 9,
                                                               routing_id: 5},
                                        site_instance: {active_rfh_count: 2,
                                                        browsing_instance_id: 5,
                                                        has_process: true,
                                                        is_default: false,
                                                        related_active_contents_count: 2,
                                                        site_info: {is_fenced: false,
                                                                    is_guest: false,
                                                                    is_sandboxed: false,
                                                                    process_lock_url: https://vuln.foo/,
                                                                    requires_origin_keyed_process: false,
                                                                    site_url: https://vuln.foo/},
                                                        site_instance_group: {active_frame_count: 2,
                                                                              process: {browser_context: {id: "9DFC1285B9F8CCC701F8A717B64B1458"},
                                                                                        child_process_id: 71759,
                                                                                        id: 9,
                                                                                        process_lock: "{ https://vuln.foo/ }"},
                                                                              site_instance_group_id: 3},
                                                        site_instance_id: 5},
                                        url: https://victim--poc--intent-paint--origin-spoof.cr.vuln.foo/},
                   frame_tree_node_id: 4,
                   is_main_frame: true,
                   speculative_frame_host: "0x0"},
 from_begin_navigation: true,
 has_committed: false,
 is_error_page: false,
 is_synchronous_renderer_commit: false,
 navigation_id: 23,
 navigation_type: "DIFFERENT_DOCUMENT",
 net_error: 0,
 reload_type: 0,
 state: 0,
 url: "intent:x;"}

But I don't even see a renderer process for the victim page in the trace!? creis@, any pointers to explain that?

### cr...@chromium.org (2023-11-15)

Sorry, I'm not much help on tracing advice.  Maybe Nasko or Alexander know why the renderer isn't showing up for you?

But at least at a high level, I think the relevant part of the attack flow is:

1) Attacker A1 opens popup to victim V (which doesn't paint, but that's not important yet).
2) Attacker navigates popup to A2, which paints immediately.
3) A2 goes back to V, which doesn't paint.  Paint holding allows A2 to show for 4 seconds.
4) Attacker navigates popup to A2 again.  The paint holding logic wouldn't show V while waiting for A2 to paint (good), but A2 paints immediately, so all the paint holding logic is probably reset.
5) A2 goes back to V again, repeating the issue from scratch.

Does that help?

### al...@chromium.org (2023-11-15)

Re: tracing: which process are you expecting to see in the trace? I only see 71759 in the dump in #6 and I can see it in the trace.

### kh...@chromium.org (2023-11-16)

Re #7, thanks creis. I need to debug this with a dev build to figure out why the logic I mentioned above is not mitigating this attack when V doesn't paint.

Re #8, I was expecting a process labelled with victim origin when a navigation back to V2 is initiated.

### ar...@chromium.org (2023-11-16)

Thanks!
Some preliminary severity/impact rating:

Severity
--------

An address bar spoof with mitigating factors:
- The attacker can display its content under the victim's origin. The status quo was to accept this for up to 4s. This bug shows you can do it repeatedly to extend the duration.
- The attacker page is not interactive.
- The victim must have a page that renders anything, and immediately navigate toward an URL that hang for long enough.
- The victim must not use COOP.

To me, this matches Medium.
https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/severity-guidelines.md#toc-medium-severity

Impact:
-------

We can reproduce on the current stable version (M119)

### cr...@chromium.org (2023-11-16)

https://crbug.com/chromium/1502186#c10: Thanks.  Are there any known victim pages in the wild with the necessary delayed paint property?  That seems like a pretty large mitigating factor, to where I could possibly see this being Low severity.  Still, I agree that the bypass of the 4s timer here means we should aim for a fix.

### [Deleted User] (2023-11-16)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-11-16)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cr...@chromium.org (2023-11-17)

Re: tracing: I just chatted with altimin@, and it makes sense that there's only one renderer process because the attacker and victim URLs are different origins within the same site.  Both would end up in the same site-locked process unless there were a reason to isolate the origins from each other (e.g., OAC, --strict-origin-isolation, etc).

### [Deleted User] (2023-11-30)

khushalsagar: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@chromium.org (2023-12-04)

[security shepherd]

I made a quick demo of the repro (with no painted content on the victim site, to address https://crbug.com/chromium/1502186#c3) at https://stingy-colorful-cowbell.glitch.me/ and it shows the two URLs flashing back and forth while displaying the attacker content (to me, the URL spoof is not too convincing due to this flashing, although I agree it should be fixed due to bypassing the 4s timer). These are on different sites due to glitch.me being an eTLD. So I don't think it's limited to attacker+victim origins on the same site. And looking at the chrome task manager while running the repro, it seems like they are in different processes.

I can repro this on ChromeOS and Windows, so setting OS labels accordingly. On Linux I get a dialog asking for an application to handle the intent. Testing it on Android, I don't see the flashing URLs at all, it just displays the attacker URL as it should.

The demo at https://attacker--poc--intent-paint--origin-spoof.cr.vuln.foo/ also seems to show the two URLs flashing back and forth more frequently than the video in the original post. (For me at least, on M119.)

khushalsagar@: Thanks for the investigation so far! Could you please take another look at this bug (or if you are not a good owner for this bug, help find a more appropriate owner)? Thanks.

### [Deleted User] (2023-12-05)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-14)

khushalsagar: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### kh...@chromium.org (2024-01-04)

Sorry was OOO in December. Will take a look this week.

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1502186?no_tracker_redirect=1

[Multiple monorail components: Blink>Paint, UI>Browser>Navigation, UI>Browser>Omnibox]
[Monorail components added to Component Tags custom field.]

### ps...@google.com (2024-02-13)

Hello khushalsagar@,

Have you had the chance to take a look at this bug?

[Secondary security shepherd]


### pd...@chromium.org (2024-08-18)

Any update on this? This is marked as P1 so is exceeding our goals of fixing P1s within 30 days.

### kh...@chromium.org (2024-08-29)

Vlad has a change in flight for this.

### cr...@chromium.org (2024-09-19)

The fix for this is in review at <https://chromium-review.googlesource.com/c/chromium/src/+/5823867>. (Thanks!)

We're splitting out any affected cases on Android WebView into <https://crbug.com/368087192>, since there may be compatibility implications there (though I suspect the spoof might still work on apps that show an address bar for their WebView instances).

### ap...@google.com (2024-09-19)

Project: chromium/src
Branch: main

commit 7dd77c55d503584390f01fb6f0eeb33200767af9
Author: Vladimir Levin <vmpstr@chromium.org>
Date:   Thu Sep 19 18:35:55 2024

    [PH] Disable cross origin paint holding if there was no user activation.
    
    This patch disables paint holding if this is a cross origin navigation
    and there was no user activation. This is a safety measure to prevent
    sites from continually displaying mismatched URL and content.
    
    With regular user behavior (clicks, etc), the behavior should be
    unchanged since this counts as user activation.
    
    R=creis@chromium.org
    
    Bug: 40942531
    Change-Id: I4e7fba7db2f6404f7e02f1b2c501fe2dcc2d6b2f
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5823867
    Commit-Queue: Vladimir Levin <vmpstr@chromium.org>
    Reviewed-by: Charlie Reis <creis@chromium.org>
    Reviewed-by: Nate Fischer <ntfschr@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1357750}

M       android_webview/browser/aw_content_browser_client.cc
M       android_webview/browser/aw_content_browser_client.h
M       content/browser/renderer_host/delegated_frame_host.cc
M       content/browser/renderer_host/navigator.cc
M       content/browser/renderer_host/render_frame_host_impl_browsertest.cc
M       content/browser/renderer_host/render_frame_host_manager.cc
M       content/browser/renderer_host/render_frame_host_manager.h
M       content/browser/renderer_host/render_frame_host_manager_unittest.cc
M       content/common/features.cc
M       content/common/features.h
M       content/public/browser/content_browser_client.cc
M       content/public/browser/content_browser_client.h

https://chromium-review.googlesource.com/5823867


### ap...@google.com (2024-09-20)

Project: chromium/src
Branch: main

commit 011f2568aab9a77614d10ad913a18a825ea7d6bb
Author: luci-bisection@appspot.gserviceaccount.com <luci-bisection@appspot.gserviceaccount.com>
Date:   Fri Sep 20 06:55:26 2024

    Revert "[PH] Disable cross origin paint holding if there was no user activation."
    
    This reverts commit 7dd77c55d503584390f01fb6f0eeb33200767af9.
    
    Reason for revert:
    LUCI Bisection has identified this change as the cause of a test failure. See the analysis: https://ci.chromium.org/ui/p/chromium/bisection/test-analysis/b/5689950163959808
    
    Sample build with failed test: https://ci.chromium.org/b/8736340719252212641
    Affected test(s):
    [ninja://chrome/test:telemetry_gpu_integration_test/gpu_tests.trace_integration_test.TraceIntegrationTest.TraceTest_ViewTransitionsCapture](https://ci.chromium.org/ui/test/chromium/ninja:%2F%2Fchrome%2Ftest:telemetry_gpu_integration_test%2Fgpu_tests.trace_integration_test.TraceIntegrationTest.TraceTest_ViewTransitionsCapture?q=VHash%3Ad873416cf165ef15)
    
    If this is a false positive, please report it at http://b.corp.google.com/createIssue?component=1199205&description=Analysis%3A+https%3A%2F%2Fci.chromium.org%2Fui%2Fp%2Fchromium%2Fbisection%2Ftest-analysis%2Fb%2F5689950163959808&format=PLAIN&priority=P3&title=Wrongly+blamed+https%3A%2F%2Fchromium-review.googlesource.com%2Fc%2Fchromium%2Fsrc%2F%2B%2F5823867&type=BUG
    
    Original change's description:
    > [PH] Disable cross origin paint holding if there was no user activation.
    >
    > This patch disables paint holding if this is a cross origin navigation
    > and there was no user activation. This is a safety measure to prevent
    > sites from continually displaying mismatched URL and content.
    >
    > With regular user behavior (clicks, etc), the behavior should be
    > unchanged since this counts as user activation.
    >
    > R=creis@chromium.org
    >
    > Bug: 40942531
    > Change-Id: I4e7fba7db2f6404f7e02f1b2c501fe2dcc2d6b2f
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5823867
    > Commit-Queue: Vladimir Levin <vmpstr@chromium.org>
    > Reviewed-by: Charlie Reis <creis@chromium.org>
    > Reviewed-by: Nate Fischer <ntfschr@chromium.org>
    > Cr-Commit-Position: refs/heads/main@{#1357750}
    >
    
    Bug: 40942531
    Change-Id: I524aca1748a85c5e72a5b0c2044f24f3eebcb152
    No-Presubmit: true
    No-Tree-Checks: true
    No-Try: true
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5876485
    Commit-Queue: Jeremie Boulic <jboulic@chromium.org>
    Reviewed-by: Jeremie Boulic <jboulic@chromium.org>
    Owners-Override: Jeremie Boulic <jboulic@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1358026}

M       android_webview/browser/aw_content_browser_client.cc
M       android_webview/browser/aw_content_browser_client.h
M       content/browser/renderer_host/delegated_frame_host.cc
M       content/browser/renderer_host/navigator.cc
M       content/browser/renderer_host/render_frame_host_impl_browsertest.cc
M       content/browser/renderer_host/render_frame_host_manager.cc
M       content/browser/renderer_host/render_frame_host_manager.h
M       content/browser/renderer_host/render_frame_host_manager_unittest.cc
M       content/common/features.cc
M       content/common/features.h
M       content/public/browser/content_browser_client.cc
M       content/public/browser/content_browser_client.h

https://chromium-review.googlesource.com/5876485


### ap...@google.com (2024-10-03)

Project: chromium/src  

Branch: main  

Author: Vladimir Levin <[vmpstr@chromium.org](mailto:vmpstr@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/5894513>

Reapply "[PH] Disable cross origin paint holding if there was no user activation."

---


Expand for full commit details
```
Reapply "[PH] Disable cross origin paint holding if there was no user activation."

This reverts commit 011f2568aab9a77614d10ad913a18a825ea7d6bb.

Original patch description:
This patch disables paint holding if this is a cross origin navigation
and there was no user activation. This is a safety measure to prevent
sites from continually displaying mismatched URL and content.

With regular user behavior (clicks, etc), the behavior should be
unchanged since this counts as user activation.

Difference from original CL:
The difference is that we post a task to timeout paintholding, which allows embedding to differ and happen further down in the stack.

Details:
The surface eviction happens in this stack
content::DelegatedFrameHost::ResetFallbackToFirstNavigationSurface()
content::RenderWidgetHostImpl::ClearDisplayedGraphics()
content::RenderWidgetHostImpl::ForceFirstFrameAfterNavigationTimeout()
content::RenderFrameHostManager::CommitPendingIfNecessary()
content::RenderFrameHostManager::DidNavigateFrame()
content::Navigator::DidNavigate()

There is a bifurcation in ResetFallbackToFirstNavigationSurface to
decide whether to evict the delegated frame. This decision is based
on whether we have an first local surface id after navigation. On
non-Mac system, this local surface id is set in a stack similar to
the one below:

content::DelegatedFrameHost::EmbedSurface()
content::RenderWidgetHostViewAura::SynchronizeVisualProperties()
content::RenderWidgetHostViewAura::ShowWithVisibility()
content::RenderFrameHostManager::CommitPendingIfNecessary()
content::RenderFrameHostManager::DidNavigateFrame()
content::Navigator::DidNavigate()

Importantly, this happens _before_ we reset fallback, so in typical
cases we avoid eviction of the frame and simply reset its surface.

On Mac, the stack that sets the frame is below:
content::DelegatedFrameHost::EmbedSurface()
content::BrowserCompositorMac::DidNavigate()
content::RenderWidgetHostImpl::DidNavigate()
content::RenderFrameHostImpl::DidCommitNavigation()
...
content::mojom::NavigationClient_CommitNavigation_ForwardToCallback

This call happens _after_ we reset the fallback, so in typical cases
we evict the frame before embedding a new one. This is a cause for
a lot of test failures (and ultimately the reason for the revert).

Because the reset fallback path never happened synchronously with
DidNavigate, it isn't clear at this time whether this poses a problem
in non-test cases. Out of abundance of caution, I propose posting a
(non-delayed) task to remove paint holding. In practice this means
potentially having paintholding in place while the UI thread is busy.
This, however, is still a mitigation for the initial bug, albeit one
that does not have strict guarantees.

R=​creis@chromium.org
Bug: 40942531

Change-Id: Id45d1e2267147da2a6f4351cb95d3d8002d8f7ae
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5894513
Reviewed-by: Charlie Reis <creis@chromium.org>
Commit-Queue: Vladimir Levin <vmpstr@chromium.org>
Reviewed-by: Nate Fischer <ntfschr@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1363640}

```

---

Files:

- M `android_webview/browser/aw_content_browser_client.cc`
- M `android_webview/browser/aw_content_browser_client.h`
- M `content/browser/renderer_host/delegated_frame_host.cc`
- M `content/browser/renderer_host/navigator.cc`
- M `content/browser/renderer_host/render_frame_host_impl_browsertest.cc`
- M `content/browser/renderer_host/render_frame_host_manager.cc`
- M `content/browser/renderer_host/render_frame_host_manager.h`
- M `content/browser/renderer_host/render_frame_host_manager_unittest.cc`
- M `content/common/features.cc`
- M `content/common/features.h`
- M `content/public/browser/content_browser_client.cc`
- M `content/public/browser/content_browser_client.h`

---

Hash: c80d80e1ebd09d057d5c96e84807df539504e7c0  

Date:  Thu Oct 03 15:02:15 2024


---

### sp...@google.com (2024-11-15)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $3000.00 for this report.

Rationale for this decision:
report of lower-impact/mitigated security UI spoof


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-11-15)

Congratulations Thomas! Thank you for your efforts and reporting this issue to us!

### pe...@google.com (2025-01-23)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40942531)*
