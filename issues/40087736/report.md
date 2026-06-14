# Security: data-uris can be loaded on the top frame using a (failed) server redirect followed and a history back()

| Field | Value |
|-------|-------|
| **Issue ID** | [40087736](https://issues.chromium.org/issues/40087736) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>Navigation |
| **Reporter** | ma...@caballero.com.ar |
| **Assignee** | na...@chromium.org |
| **Created** | 2017-05-17 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

Data-uris can still be loaded on the top frame, using a simple server redirect (which fails) and then, loading a new page doing a history.go(-1) (back);

**VERSION**  

Chrome Version: [60.0.3102.0] + (Official Build) canary (64-bit)  

Operating System: [Windows 10 Pro, fully updated]

**REPRODUCTION CASE**  

<https://www.cracking.com.ar/demos/datauriredirback/>

window.open("redir.php?URL=data:text/html,<h1>Here's a data-uri loaded on top!</h1><script>document.write(navigator.userAgent)</script>", "DATA\_WIN");

setTimeout(function()  

{ // goback.html is doing a history.go(-1)  

window.open("goback.html", "DATA\_WIN");  

}, 1000);

## Attachments

- [data-uri-on-top.zip](attachments/data-uri-on-top.zip) (application/octet-stream, 692 B)

## Timeline

### na...@chromium.org (2017-05-17)

[Empty comment from Monorail migration]

### el...@chromium.org (2017-05-17)

Great find, thanks!

[Monorail components: UI>Browser>Navigation]

### cr...@chromium.org (2017-05-17)

nick@ suggests canceling data URLs in redirects (in the NavigationThrottle), rather than failing them in a way that gives a NavigationEntry.

meacer@: Can you take a look?

### el...@chromium.org (2017-05-17)

meacer@ is OOF for a while. lgarron@ is babysitting this area for him.

### ni...@chromium.org (2017-05-17)

[Empty comment from Monorail migration]

### na...@chromium.org (2017-05-17)

Wouldn't cancelling just leave the old page in place, which is difference in behavior? 

Also, the data: redirects are blocked because of unsafe redirect scheme, which might not be hitting NavigationThrottles at all and being blocked earlier.

An alternative is to look at the NavigationHandle for the history navigation and check whether it was renderer or browser-initiated. We need to check whether the bit comes from the NavigationEntry or the actual user action.

### cr...@chromium.org (2017-05-17)

#6: NavigationEntries intentionally clear the is_renderer_initiated_ bit at commit time, so that doesn't help here.  A back navigation using the Back button (rather than history.go(-1)) is considered browser-initiated.

### na...@chromium.org (2017-05-17)

[Comment Deleted]

### na...@chromium.org (2017-05-17)

I have a basic test case in https://codereview.chromium.org/2889003002/. It might have to change depending on our fix.

### na...@chromium.org (2017-05-17)

Dumping a few thoughts based on exploration I've done.

Unsafe redirects are handled in URLRequest and always mapped to ERR_UNSAFE_REDIRECT (https://cs.chromium.org/chromium/src/net/url_request/url_request.cc?rcl=eaf14a90c04606bf4aa4b3cea2fb3f6ddcf6afd8&l=940). Because of this, we commit the error page with the data: URL staying as the URL for the NavigationEntry. Either a reload or a back/forward will cause us to load the data: URL.

The DataUrlNavigationThrottle does not block the navigation at present. For one, it allows browser-initiated navigations, which back/forward are. Unfortunately, we cannot use the NavigationThrottle to block these navigations prior to PlzNavigate :(. The reason is that back/forward navigations are sent first to the renderer process as instructions to go to a history entry. Without PlzNavigate, data: URLs are handled entirely in the renderer, so we never go to the network stack for those. Since NavigationThrottles are notified by the IO thread/network stack without PlzNavigate, we don't get even a WillStartRequest call. With PlzNavigate, we can block it easily by checking the PageTransition type on the navigation and allow only new navigations, blocking the back/forward types.

I'm open to other ideas on how to fix this other than shipping PlzNavigate :).

### na...@chromium.org (2017-05-17)

Another tongue-in-cheek proposal for solving - fix the error page behavior to not carry the error URL :). Just adding them for completeness.

### na...@chromium.org (2017-05-18)

nick@'s proposal is to change the error on unsafe redirects to be ERR_ABORTED, which will cancel the navigation without committing an error page. This will be a change in behavior and will affect more than just the case of data: URLs, but it is conceptually the better solution in the current state of error pages committing with the blocked URL.

Also, I realize that my suggestion above to use the PageTransition for detecting back/forward is not good, since ideally we want to allow history navigations to succeed, if the user typed the URL in the omnibox themselves. As such we need to distinguish between navigation to data: URL in history when the previous result was an error vs not.

### sh...@chromium.org (2017-05-18)

[Empty comment from Monorail migration]

### cr...@chromium.org (2017-05-18)

Assigning to nasko@, who's working on a potential fix.

If I understand correctly, Chrome started blocking renderer-initiated data URLs in r466504 (60.0.3079.0) in https://crbug.com/chromium/594215.  Thus, this affects Canary and Dev but not yet Beta or Stable.  I'm not sure what we'd consider the severity yet.

As for fixes, nasko@ and I were debating the merits of blocking vs aborting and how error pages work.  Aborting the navigation isn't a great option as noted above, since it provides no feedback to the user and may affect a lot of cases.  We feel it might be better to try to fix the underlying problem that error pages for blocked navigations end up in session history and you can go back to them without being blocked a second time.  That's a more general problem than just blocked data URLs, and could affect more cases.

To change this, we need to distinguish between blocked navigations and failed navigations, since simple things like network failures should be allowed to load if the user tries again.  Blocked navigations shouldn't attempt to load again if you come back, ideally even when restoring a tab or session.

We're trying out an approach where the browser process checks if a navigation was blocked at commit time, and if so, it sets the NavigationEntry's URL and PageState to something like about:blank, and it sets the virtual URL to the blocked URL so that we display it to the user.  We'll see if this has the right behavior, so that going back to the blocked URL just shows about:blank.

### cr...@chromium.org (2017-05-19)

[Empty comment from Monorail migration]

### ke...@chromium.org (2017-05-23)

Setting Sev-Low, since this doesn't constitute a real URL spoof.

### sh...@chromium.org (2017-05-24)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-05-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/5ff4eeaefbc41f51d02887e0c42bb6e72ba292a0

commit 5ff4eeaefbc41f51d02887e0c42bb6e72ba292a0
Author: nasko <nasko@chromium.org>
Date: Thu May 25 02:51:00 2017

Change NavigationEntry to use virtual URL in error pages for blocked navigations

Error pages today commit with the original URL in the NavigationEntry. This means
that on history navigations/reload, the original URL will be used. However, when
navigations are blocked, we shouldn't be allowing the blocked URL to be set as
the NavigationEntry URL. There has been a long standing desire to change this
aspect of error pages and this CL is a small step in that direction.

The goal of this CL is to classify error pages due to blocked navigations and
change the URL of the NavigationEntry to be a safe one - "about:blank". To
preserve the existing UX, though, the originally blocked URL is set as the
virtual URL on the NavigationEntry. This allows history navigations/reload to
end up at about:blank, which is much safer behavior than allowing the load
to the blocked URL.

BUG=723796
CQ_INCLUDE_TRYBOTS=master.tryserver.chromium.linux:linux_site_isolation

Review-Url: https://codereview.chromium.org/2889003002
Cr-Commit-Position: refs/heads/master@{#474535}

[modify] https://crrev.com/5ff4eeaefbc41f51d02887e0c42bb6e72ba292a0/chrome/browser/extensions/navigation_observer.cc
[modify] https://crrev.com/5ff4eeaefbc41f51d02887e0c42bb6e72ba292a0/content/browser/browser_side_navigation_browsertest.cc
[modify] https://crrev.com/5ff4eeaefbc41f51d02887e0c42bb6e72ba292a0/content/browser/frame_host/data_url_navigation_browsertest.cc
[modify] https://crrev.com/5ff4eeaefbc41f51d02887e0c42bb6e72ba292a0/content/browser/frame_host/navigation_controller_impl.cc
[modify] https://crrev.com/5ff4eeaefbc41f51d02887e0c42bb6e72ba292a0/content/browser/frame_host/navigation_controller_impl_browsertest.cc
[modify] https://crrev.com/5ff4eeaefbc41f51d02887e0c42bb6e72ba292a0/content/browser/frame_host/navigation_handle_impl_browsertest.cc
[modify] https://crrev.com/5ff4eeaefbc41f51d02887e0c42bb6e72ba292a0/content/test/data/data_url_navigations.html


### na...@chromium.org (2017-05-25)

The fix missed the 60.0.3110.0 by a bit, so it should show up in the next Canary build. I will keep the bug open until it can be verified on canary.

### ma...@caballero.com.ar (2017-05-30)

Verified on Canary. Bug is patched.

Thanks for the speed, guys!

--------------------------------------------

Google Chrome	61.0.3115.0 (Official Build) canary (64-bit) (cohort: 64-Bit)
Revision	958dbb23d9fb6ef967f76d9cda0153a6cb05f8cd-refs/heads/master@{#475394}
OS	Windows
JavaScript	V8 6.1.11.1

### me...@chromium.org (2017-06-01)

Sorry for the late response. I'm back from OOO, but this bug concerns redirects rather than renderer initiated navigations, so my input will be limited as I'm not very familiar with how redirects to data URLs (and chrome: et al) are blocked.

What are the specific downsides of blocking redirects instead of failing them? I've seen these in the thread:
- lack of feedback to the user if we block instead of fail
- the old page will remain in place

Both of these are already true with renderer initiated data URL navigations. Is the main concern that we just don't know other implications of blocking redirects?

### na...@chromium.org (2017-06-01)

No worries, it is already taken care of, so marking as fixed.

For answering your question - we do not allow the redirect to happen, but the issue is that we allow the data: URL to be committed in the NavigationEntry. The CL I committed fixes that for certain cases, but I'm also in discussions to find out a bit more generic solution for handling such errors safely.

### sh...@chromium.org (2017-06-02)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-06-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/d894710be3b56a15871376c5979615053dddcd70

commit d894710be3b56a15871376c5979615053dddcd70
Author: davidben <davidben@chromium.org>
Date: Tue Jun 06 19:28:44 2017

Perform redirect checks before OnReceivedRedirect in //net.

Right now, if URLRequest sees a redirect, it first signals
OnReceivedRedirect, gives the caller a chance to reject the redirect
and, if okay, it carries on to URLRequest::Redirect.
URLRequest::Redirect then performs additional checks and potentially
rejects the redirect. This ordering has two quirks:

First, new_url.is_valid() is checked very late, but most consumers'
checks presumably are going to check the URLs. This means that we reject
invalid redirect URLs based not on //net code, but whatever consumer
logic happens to notice.

In //content, this is ChildProcessSecurityPolicyImpl, which
interprets the renderer as trying to fetch somewhere questionable and
just cancels the request. This results in an aborted request and no
visible error, which is confusing, particularly for navigations.

Second, URLRequest::Delegate gets called in an odd order. If we don't
think request->url() should be allowed to redirect to new_url, whatever
error we surface should be associated with request->url(), not new_url.
That is, new_url did not misbehave necessarily.  request->url() did for
daring to utter such an obviously invalid URL.

In particular, this is relevant for browser navigation logic, which
needs to associate the error page with the right URL. If the error page
is associate with new_url, reloading will skip the check, which is
problematic.

We do actually handle this properly. request->url() is not updated until
later, but since Chrome is a complex multi-threaded multi-process IPC
monster, the URLRequest is not immediate accessible. Instead, code likes
to update the working URL when it receives OnReceivedRedirect.

//net's current behavior is incompatible with this. In a normal
redirect situation, we might signal:

   OnReceivedRedirect(new_url) // url() => old_url
   OnResponseStarted(net_error) // url() => new_url.

But in this situation, we'll signal:

   OnReceivedRedirect(new_url) // url() => old_url
   OnResponseStarted(net_error) // url() => old_url!

This is weird. This CL fixes this so it looks like:

   OnResponseStarted(net_error) // url() => old_url

This means redirects to unparseable URLs simply fail with
ERR_INVALID_REDIRECT (previously //net used ERR_INVALID_URL, but since
the error page will commit at the old URL, ERR_INVALID_REDIRECT seems
clearer). It also means that code which receives OnReceivedRedirect can
eagerly update the URL, provided, of course, it orders it correctly with
its own redirect checks. But the accept/reject signal may be propagated
on-path, whereas a two-phase check (first consumer, then //net) requires
potentially two round-trips.

Unfortunately, this change does as a result require checking in newly
failing test expectations for the redirect to data URL variant of issue
#707185. Before this CL, whether we produced an opaque-redirect filtered
response for an invalid redirect depended on whether the check happened
in //net or outside. This now makes them treated similarly. Later, we
can see about fixing both cases. (One thought is to teach //net about
manual redirect mode, but this is subtle because //net persists info
in the cache based on what it believes is and isn't a redirect. Another
is to check the response object in OnResponseStarted and, if it's
redirect-shaped, produce a filtered response wrapping an error response.
This probably will involve adding a boolean to
ResourceRequestCompletionStatus.)

BUG=462272,723796,707185
CQ_INCLUDE_TRYBOTS=master.tryserver.chromium.linux:linux_site_isolation

Review-Url: https://codereview.chromium.org/2917133002
Cr-Commit-Position: refs/heads/master@{#477371}

[modify] https://crrev.com/d894710be3b56a15871376c5979615053dddcd70/chrome/browser/net/errorpage_browsertest.cc
[modify] https://crrev.com/d894710be3b56a15871376c5979615053dddcd70/components/error_page/common/localized_error.cc
[modify] https://crrev.com/d894710be3b56a15871376c5979615053dddcd70/content/browser/browser_side_navigation_browsertest.cc
[modify] https://crrev.com/d894710be3b56a15871376c5979615053dddcd70/content/browser/frame_host/data_url_navigation_browsertest.cc
[modify] https://crrev.com/d894710be3b56a15871376c5979615053dddcd70/content/browser/frame_host/navigation_controller_impl_browsertest.cc
[modify] https://crrev.com/d894710be3b56a15871376c5979615053dddcd70/content/browser/frame_host/navigation_handle_impl_browsertest.cc
[modify] https://crrev.com/d894710be3b56a15871376c5979615053dddcd70/content/browser/service_worker/service_worker_browsertest.cc
[modify] https://crrev.com/d894710be3b56a15871376c5979615053dddcd70/net/base/net_error_list.h
[modify] https://crrev.com/d894710be3b56a15871376c5979615053dddcd70/net/url_request/url_request.cc
[modify] https://crrev.com/d894710be3b56a15871376c5979615053dddcd70/net/url_request/url_request.h
[modify] https://crrev.com/d894710be3b56a15871376c5979615053dddcd70/net/url_request/url_request_job.cc
[modify] https://crrev.com/d894710be3b56a15871376c5979615053dddcd70/net/url_request/url_request_job.h
[modify] https://crrev.com/d894710be3b56a15871376c5979615053dddcd70/net/url_request/url_request_unittest.cc
[add] https://crrev.com/d894710be3b56a15871376c5979615053dddcd70/third_party/WebKit/LayoutTests/external/wpt/fetch/api/redirect/redirect-location-expected.txt
[add] https://crrev.com/d894710be3b56a15871376c5979615053dddcd70/third_party/WebKit/LayoutTests/external/wpt/fetch/api/redirect/redirect-location-worker-expected.txt
[modify] https://crrev.com/d894710be3b56a15871376c5979615053dddcd70/tools/metrics/histograms/enums.xml


### na...@chromium.org (2017-07-20)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-07-31)

[Empty comment from Monorail migration]

### aw...@google.com (2017-07-31)

Hi manuel@ - the VRP panel decided to award $500 for this report!  A member of our finance team will be in touch to arrange payment.

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2017-07-31)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-09-08)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@google.com (2017-12-14)

[Empty comment from Monorail migration]

### is...@google.com (2017-12-14)

This issue was migrated from crbug.com/chromium/723796?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40087736)*
