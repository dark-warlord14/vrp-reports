# Security: Possible to spoof the contents of the omnibox to display any http/https URL, some extension URLs and some internal URLs

| Field | Value |
|-------|-------|
| **Issue ID** | [40095159](https://issues.chromium.org/issues/40095159) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>Navigation |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | de...@gmail.com |
| **Assignee** | ah...@chromium.org |
| **Created** | 2019-05-24 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

By redirecting a same-origin download and then performing a specific location assignment during the beforeunload event, it's possible to update the omnibox to display any desired http/https URL, some extension URLs and some internal URLs. One caveat is that the omnibox won't contain the https lock indicator, no matter which site you're spoofing.

Aside from spoofing various sites, you can cancel any browser-initiated navigation. When you do cancel a navigation, the address entered in the omnibox will remain in place, but no navigation will occur.

**VERSION**  

Chrome Version: Tested on 74.0.3729.169 (stable) and 76.0.3804.1 (canary)  

Operating System: Windows 10 Pro, version 1809

**REPRODUCTION CASE**

1. The attached files form two simple websites. Download index.html, main.js and server.py into a directory and run the following command:

python3 server.py 8080

This will start a simple web server that can be used to serve the files in the directory. server.py is necessary here, as it redirects requests received for download.txt:

if self.path == '/download.txt':  

self.send\_response(302)  

self.send\_header('Location', "<https://www.google.com/>")  

self.end\_headers()

This is important in step 6 below, where a download for this file will be initiated.

2. Next, download iframe.html and iframe-main.js into another directory and run the following command:

python3 -m http.server --bind 127.0.0.2 8080

3. In the browser, navigate to the following location:

<http://localhost:8080/index.html>

4. This page contains a cross-origin iframe (<http://127.0.0.2:8080/iframe.html>) that makes the following call when a message (sent via postMessage) is received:

parent.location.href = "chrome-guest://1234";

5. index.html sets up a beforeunload handler that makes the following call:

iframe.contentWindow.postMessage("", "\*");

Ultimately, this means that when the page is unloaded, the iframe will attempt to navigate the page to chrome-guest://1234.

6. Finally, index.html also contains the following link:

<a href="download.txt" id="first-download-link" download></a>

Two seconds after the page has loaded, this link will be clicked with JavaScript.

When that happens, the following occurs:

- server.py redirects the request received for download.txt to <https://www.google.com>. This turns a same-origin download into a cross-origin navigation.
- This sort of navigation results in the omnibox being updated, which I believe might have to do with this redirect policy:

<https://cs.chromium.org/chromium/src/content/browser/download/download_manager_impl.cc?l=877&rcl=37e0123cf4d593a940c9c5a521c0944174a18c61>

This is in contrast to other sorts of renderer-initiated navigations that don't update the omnibox immediately.

- When the redirect to <https://www.google.com> occurs, the beforeunload handler is invoked and the iframe attempts to redirect its parent to chrome-guest://1234. This ultimately results in both navigations being cancelled.

7. At this point, the address shown in the omnibox will be updated (to <https://www.google.com>), but it typically requires the user to take an action like one of the following before the updated address is displayed:

- Switch away from the tab and switch back,
- Open the devtools,
- Click twice in the omnibox,
- Click/right-click in the omnibox and then click somewhere else,
- Drag the tab into another window.

However, this is done automatically by the page in this case, by creating a new window, then immediately closing it. This is possible because when a download redirects to a javascript: URL, the page seemingly gains user activation, even if the user has never actually interacted with it (I'll file a separate issue for that).

What happens here is that another download is initiated (one second after the first download), this time one that redirects to the following javascript: URL:

javascript: var temporaryWindow = open(); temporaryWindow.close();

The fact that the window that's opened is immediately closed should mean that it's never actually visible. Importantly, though, it causes the omnibox to update.

After this is done, the URL displayed in the omnibox should switch to the target URL (i.e. <https://www.google.com>). This address will remain, even though the tab is still on the original page and no navigation is occurring.

8. There are also a number of other URL schemes you can display. I've included examples of each of these in server.py. Just uncomment the relevant line and restart the Python HTTP server to test. The additional schemes are:

- chrome-extension:// - Only works for items listed under web\_accessible\_resources, so you won't be able to display arbitrary extension URLs. The extension indicator (which states that "You're viewing an extension page") is shown in the omnibox, however.
- chrome-native:// - Includes chrome-native://bookmarks/, chrome-native://history/ and chrome-native://newtab/, which are used on Android.
- chrome-search:// - Includes chrome-search://local-ntp/local-ntp.html. This one is interesting, as it clears the URL bar altogether and displays the "Search Google or type a URL" text you see when creating a new tab.
- view-source:
- chrome-devtools:// - Canary only.

It also turns out some of these actually load (i.e. if you redirect a download to one of these schemes, the page will load). I'll file a separate issue for that as well.

There's some overlap with the schemes listed in this issue:

<https://bugs.chromium.org/p/chromium/issues/detail?id=965611>

So there might be some common causes. The view-source: scheme is one that doesn't work using window.open(), however.

9. You can also easily test that any browser-initiated navigation in the tab is cancelled. To do this, simply click on a bookmark or enter an address/search term in the omnibox. You should find that if you type an address and press enter, for example, the navigation is cancelled, but the address remains in place.

If you do this for a chrome:// page, the site indicator will change to indicate that the current page is a Chrome page, even though it's not. This isn't very useful for a site, though, as it can't redirect to a chrome:// page and it can't detect that the user has entered a chrome:// address.

Some miscellaneous notes:

- It's important that the iframe be cross-origin. The steps above won't work if the iframe is same-origin with its parent.
- The iframe is declared with the following sandbox attributes:

sandbox="allow-scripts allow-top-navigation"

allow-top-navigation allows it to navigate the top-level page without user interaction.

- The two links declared in index.html need to have the "download" attribute specified. The steps above won't work if those two links are just regular links.

In summary, a site can:

- Spoof any http/https URL, whether or not it's valid (e.g. whether or not it uses a valid TLD and actually exists).
- Spoof extension URLs, at least in the case where the resource is listed under web\_accessible\_resources.
- Spoof certain internal URLs.
- Cancel any browser-initiated navigation that takes place within the tab.
- Run code that requires user activation (e.g. window.open) without any user interaction by redirecting a same-origin download. Separate issue to be filed.
- Open certain protected pages, such as chrome-native://bookmarks/ and view-source:<https://www.google.com/> by redirecting a same-origin download. Separate issue to be filed.
- It is actually also possible to use the previous issue to load file:/// URLs, though in a roundabout way. If you attempt to load view-source:file:///C:/non-existent.html, the request will be rewritten to file:///C:/non-existent.html. If you can create this file (possible for files in the download directory), all you have to do is navigate the tab containing this page to another site, then navigate back.

The file, which now exists, will be loaded and if it's a HTML file you created, you can have it navigate to another file:/// location. I don't think it's very useful, though, as you have no way of retrieving the file data. You can really only use this to navigate to file:/// locations.

- Additionally, because an extension can load other chrome-extension:// pages, chrome:// pages and file:/// pages, it can easily spoof each of those schemes. This would be done by using chrome.tabs.update to update the URL of a tab to a chrome-extension://, chrome:// or file:/// page. This navigation would then be cancelled, in the same way as described above.

**CREDIT INFORMATION**  

Reporter credit: David Erceg

## Attachments

- [iframe.html](attachments/iframe.html) (text/plain, 153 B)
- [iframe-main.js](attachments/iframe-main.js) (text/plain, 109 B)
- [index.html](attachments/index.html) (text/plain, 493 B)
- [main.js](attachments/main.js) (text/plain, 1.2 KB)
- [server.py](attachments/server.py) (text/plain, 2.4 KB)
- [iframe.html](attachments/iframe_53105092.html) (text/plain, 153 B)
- [iframe-main.js](attachments/iframe-main_53105093.js) (text/plain, 109 B)
- [index.html](attachments/index_53105094.html) (text/plain, 3.1 KB)
- [main.js](attachments/main_53105095.js) (text/plain, 2.1 KB)
- [server.py](attachments/server_53105096.py) (text/plain, 927 B)

## Timeline

### de...@gmail.com (2019-05-27)

I've created an updated demonstration. It firstly makes the process of testing a URL easier (you can just enter it in a form). I think it also more effectively demonstrates how easily the location displayed in the omnibox can be changed.

Instructions are very similar to those in the original post:

1. Download index.html, main.js and server.py into a directory and run the following command:

python3 server.py 8080

2. Download iframe.html and iframe-main.js into another directory and run the following command:

python3 -m http.server --bind 127.0.0.2 8080

3. In the browser, navigate to the following location:

http://localhost:8080/index.html

4. This page allows you to enter and test a URL directly (rather than doing it by updating server.py). Provided the URL you enter uses one of the schemes listed in the original post, the omnibox should update a short time later.

There are also a number of sample URLs provided. Clicking one of the URLs should also update the omnibox.

One small difference with the code used in this demonstration is the use of history.back(). This is called purely to work around the download limiter. Without this call, the browser would prompt after the URL has been updated the first time (since each update technically requires initiating a download).

I've also done a bit more testing and I can't reproduce the issue on Android. From messages printed in the devtools console, I think this might be because unreachable navigations are all being routed through the following function:

https://cs.chromium.org/chromium/src/chrome/android/java/src/org/chromium/chrome/browser/tab/InterceptNavigationDelegateImpl.java?l=200&rcl=0029bff0e94b4c77b2f7238ffb78412851efd924

I have been able to reproduce the issue on Ubuntu 16.04 (and Chrome 74.0.3729.169), though I get xdg-open prompts when clicking on a sample URL or entering a URL (not sure why). It otherwise works the same as on Windows, though.

### de...@gmail.com (2019-05-27)

Regarding the ability to open certain protected pages (such as such as chrome-native://bookmarks/ and view-source:https://www.google.com/) by redirecting a same-origin download, as issue has been filed here:

https://bugs.chromium.org/p/chromium/issues/detail?id=967411

### ts...@chromium.org (2019-05-28)

[Empty comment from Monorail migration]

[Monorail components: UI>Browser>Navigation]

### de...@gmail.com (2019-05-28)

Regarding the ability to run code that requires user activation (e.g. window.open) without any user interaction by redirecting a same-origin download, an issue has been filed here:

https://bugs.chromium.org/p/chromium/issues/detail?id=967780

### in...@chromium.org (2019-05-29)

ahemery@, can you please take a look.

### ah...@chromium.org (2019-05-29)

I won't have time to investigate this since I'm leaving the office now. the next two days are Holidays in PAR office, passing this to nasko@ to redistribute to the US navigation team.

### ah...@chromium.org (2019-06-03)

Back to me since nasko@ seems to be OOO.

### ah...@chromium.org (2019-06-03)

Could I be added to the other bug as well please? Would be useful to have the whole picture.

### de...@gmail.com (2019-06-03)

Having debugged through the code, I think I can offer a bit more detail on why this particular spoof is working. Here's a description of what appears to happen when the user types an address into the omnibox while on a page like the demonstration page:

1. User types address in omnibox and navigation starts.
2. The pending navigation entry is set via NavigationControllerImpl::SetPendingEntry:

https://cs.chromium.org/chromium/src/content/browser/frame_host/navigation_controller_impl.cc?l=684&rcl=0d7a8b54a5c3212049ae19fafd0133d50a7750e5

This pending entry is displayed, as it's not renderer-initiated:

https://cs.chromium.org/chromium/src/content/browser/frame_host/navigation_controller_impl.cc?l=714&rcl=0d7a8b54a5c3212049ae19fafd0133d50a7750e5

3. The beforeunload event is dispatched for the page.
4. In the beforeunload event, the page sends a message to the iframe.
5. The iframe then navigates parent to an invalid URL. In the demonstration, I used a URL of chrome-guest://1234. That was the first URL I tried that worked, but I believe any URL that would result in a cancelled navigation works (e.g. non-existent-scheme://test works equally well).
6. The process of starting this navigation causes the original navigation to be overridden and deleted. The navigation from the iframe goes through RenderFrameProxyHost::OnOpenURL:

https://cs.chromium.org/chromium/src/content/browser/frame_host/render_frame_proxy_host.cc?l=292&rcl=0d7a8b54a5c3212049ae19fafd0133d50a7750e5

I don't think the code on this path does a check to see whether there's a pending browser-initiated navigation. That means that any navigation going through here can override a browser-initiated navigation.

7. The failure notification for the new navigation comes in (since the scheme it uses doesn't exist) and the browser process tries to clear the pending entry, but there's a mismatch in NavigatorImpl::DiscardPendingEntryIfNeeded:

https://cs.chromium.org/chromium/src/content/browser/frame_host/navigator_impl.cc?l=761&rcl=0d7a8b54a5c3212049ae19fafd0133d50a7750e5

controller_->GetPendingEntry() points to the original (user-initiated navigation), while expected_pending_entry_id points to the renderer-initiated navigation started in step 5. This causes DiscardPendingEntryIfNeeded to return without doing anything:

https://cs.chromium.org/chromium/src/content/browser/frame_host/navigator_impl.cc?l=773&rcl=0d7a8b54a5c3212049ae19fafd0133d50a7750e5

Which ultimately leaves the pending entry in place. As far as I can tell, the new navigation creates no pending entry. Because it fails, it also never commits (which is ultimately the other way the omnibox could be updated).

From further testing, the earliest I've been able to reproduce the spoof is Chrome 68 (tested on both Windows and Linux). It looks like it specifically started working with this commit:

https://chromium.googlesource.com/chromium/src/+/fb1ccf02ee8ca79e1404abfd3a3a7d540b7d2dbd

Which may just be because that caused cross-origin frame navigations to start going through RenderFrameProxyHost::OnOpenURL (I haven't tested that, though).

### ah...@chromium.org (2019-06-03)

Thanks a ton for the update, you're pretty much saving me the effort for the exact tracing I needed. Additionally, I have tested that removing the download attribute and can still reproduce. Did you add that for a specific reason? 

Given your points I don't think we do the check for OpenURL either. I believe it only gets checked in BeginNavigation and its related path.
I am not sure of the cases where we still use OpenURL for same process navigations. It might need fixes in both paths.

Checking how this can be done!

Also on a side note, regarding the other bug, server redirects to Javascript are supposed to be blocked, not sure why it works here.

### ah...@chromium.org (2019-06-04)

Have a WIP CL here:
https://chromium-review.googlesource.com/c/chromium/src/+/1643191

If you check the first version of the CL, you can see the conditions to trigger the spoof are much less than the first example. A navigation interrupted by a cross site iframe top.navigation is pretty much all we need. Need to check but it might even be possible with same-site using OpenURL.

### de...@gmail.com (2019-06-04)

Regarding the use of the download links, they don't impact the spoof itself directly. They do, however, allow two important things:

1. They allow a page to control the URL shown in the omnibox.

An issue with taking advantage of the spoof directly is that, typically, renderer-initiated navigations don't result in the omnibox being updated. That means that although a page could spoof the URL that's displayed, it would have to wait until the user has done something like enter an address in the omnibox or clicked a bookmark. As far as I know, there would be no way for the page to update the URL by itself (any pending entries it creates would never be visible, since they would always be renderer-initiated).

However, a same-origin download that redirects to a cross-origin resource does result in the omnibox being updated. It's simple enough to test this if you redirect a same-origin download to a cross-origin resource that returns a delayed response. You should see the omnibox display the redirected URL. However, it only does this after you've done something like switch tabs or open the devtools (there are some other methods listed in the original post).

This leads into the second point.

2. They allow the page to force the omnibox to redraw.

As mentioned above, the omnibox doesn't immediately update once a same-origin download is redirected. By opening and immediately closing a window, a page can force this to happen.

This is only possible because when you redirect a same-origin download to a javascript: URL, the page gains user activation and can open a window. I'm not too familiar with the situations in which the display of the omnibox is updated, so it's possible there might be a simpler way of doing this.

Combined, these two points mean that a page can take a URL spoof that would typically require user interaction (e.g. the user entering an address in the omnibox) and apply it without any user interaction.

About the OpenURL case, I actually filed a separate bug recently about the fact that it allows a page to override a browser-initiated navigation:

https://bugs.chromium.org/p/chromium/issues/detail?id=968282

As that'll be handled as part of this bug, however, that issue can be closed.

### de...@gmail.com (2019-06-04)

Just to add one more small note: The updated demonstration attached in https://crbug.com/chromium/966914#c1 should illustrate how the download links can be used to update the omnibox from the page itself (without having to enter an address in the omnibox directly). Clicking one of the sample URLs should be enough to update the omnibox.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-06-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/0eb432db4b2bf40ac847590ccc667d013695974b

commit 0eb432db4b2bf40ac847590ccc667d013695974b
Author: Arthur Hemery <ahemery@chromium.org>
Date: Wed Jun 12 16:15:11 2019

Security: Fixing URL spoof via cross-site iframe top navigation.

Currently, it is possible to spoof the URL of a site by starting a
navigation in the main frame and having a cross-site iframe initiating
another navigation in its parent frame (with extra steps for it to be
user visible).

This can also be used to cancel any browser initiated navigation in the
main frame.

The CL adresses the issue by adding checks similar to what exists in
BeginNavigation on the FrameProxy::OpenURL path.

Bug: 966914
Change-Id: If547c2ef4b30b2e0323141005583412c12bfef8e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1643191
Reviewed-by: Camille Lamy <clamy@chromium.org>
Commit-Queue: Arthur Hemery <ahemery@chromium.org>
Cr-Commit-Position: refs/heads/master@{#668435}

[modify] https://crrev.com/0eb432db4b2bf40ac847590ccc667d013695974b/content/browser/frame_host/navigation_controller_impl_browsertest.cc
[modify] https://crrev.com/0eb432db4b2bf40ac847590ccc667d013695974b/content/browser/frame_host/navigator.h
[modify] https://crrev.com/0eb432db4b2bf40ac847590ccc667d013695974b/content/browser/frame_host/navigator_impl.cc
[modify] https://crrev.com/0eb432db4b2bf40ac847590ccc667d013695974b/content/browser/frame_host/navigator_impl.h
[modify] https://crrev.com/0eb432db4b2bf40ac847590ccc667d013695974b/content/browser/frame_host/render_frame_proxy_host.cc


### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-06-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/4ba0558247dbe7eae809651300d289c7ca683ed5

commit 4ba0558247dbe7eae809651300d289c7ca683ed5
Author: Arthur Hemery <ahemery@chromium.org>
Date: Fri Jun 14 14:05:36 2019

Navigation: Cleaning up flaky test.

Test was reported flaky, moving to the correct way to verify for
SiteIsolation status.

Also minor readability improvement.

Bug: 966914
Change-Id: I09d2c13f7c41683ceaf670b9181d73e582d8e830
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1660436
Reviewed-by: Camille Lamy <clamy@chromium.org>
Commit-Queue: Arthur Hemery <ahemery@chromium.org>
Cr-Commit-Position: refs/heads/master@{#669206}

[modify] https://crrev.com/4ba0558247dbe7eae809651300d289c7ca683ed5/content/browser/frame_host/navigation_controller_impl_browsertest.cc


### sh...@chromium.org (2019-06-19)

ahemery: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ah...@chromium.org (2019-06-20)

Does not reproduce from ToT anymore. It simply navigates. Couldn't test on Android but expected behavior is not doing anything with SiteIsolation off and navigating like on Desktop with SiteIsolation on.

### sh...@chromium.org (2019-06-20)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-06-20)

Requesting merge to M76 because latest trunk commit (669206) appears to be after beta branch point (665002).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-06-20)

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

### ah...@chromium.org (2019-06-21)

Apparently the test flakes on some platforms, event after checking ONLY for the spoof (committed url != visible url). Need to investigate further.

### ah...@chromium.org (2019-06-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-06-21)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### na...@google.com (2019-06-24)

[Empty comment from Monorail migration]

### ah...@chromium.org (2019-06-25)

Reopening since I can reproduce with different timings on Linux CFI builds.

### sh...@chromium.org (2019-07-24)

We commit ourselves to a 60 day deadline for fixing for high severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-07-31)

[Empty comment from Monorail migration]

### li...@chromium.org (2019-08-07)

Friendly ping from the security marshal. Just want to make sure this is being worked on, as it is a high severity bug impacting stable.

### ah...@chromium.org (2019-08-13)

Having a go again, sorry for the delay. Current status is "Possible to reproduce under certain racy timings".

### do...@chromium.org (2019-08-30)

Friendly security marshal ping. Has there been much progress over the last couple of week?

### ah...@chromium.org (2019-09-02)

The flake is coming from the following: Under certain circumstances, we can have a user-gesture, meaning the NavigateFromFrameProxy will take precedence over the browser initiated navigation. In this case, the browser initiated NavigationRequest is cancelled, but its pending NavigationEntry is not.

A simple pending navigation reset should fix this, just waiting for confirmation from creis@ that wrote this part of the code I am not missing anything. He's back from vacation on September 4th.

### sh...@chromium.org (2019-09-11)

[Empty comment from Monorail migration]

### ah...@chromium.org (2019-09-11)

Quick update: Got reviews by creis@ and clamy@ saying this is probably OK as a fix. I am currently trying to figure out the user-gesture aspect of it since It is hard to make a non-flaky reproducing test without fully understanding this part.

### ah...@chromium.org (2019-09-12)

Update 2: This is not a user-gesture issue as I first thought, but rather a rare race condition that can happen if we start the frame proxy navigation very quickly, before the NavigationRequest for the first navigation was created. Effect is the same, cancelling an ongoing browser initiated navigation using NavigationControllerImpl::NavigateFromProxy.
User gesture is always false and I think this is a bug, but that's beyond the scope of this patch. That's why there was a lot of confusion earlier as this was unexpected. The effect it had, was that it made my first patch not fix the root cause of the issue but made it very hard to reproduce. Actual fix following soon.

### ah...@chromium.org (2019-09-18)

For some reason the fix CL was not added to the bug: https://chromium-review.googlesource.com/c/chromium/src/+/1751205

This should now be fixed.

### ad...@google.com (2019-09-23)

[Empty comment from Monorail migration]

### ad...@google.com (2019-09-25)

[Empty comment from Monorail migration]

### na...@google.com (2019-10-04)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-10-04)

Congrats! The Panel decided to reward $3,000 for this report :) 

### de...@gmail.com (2019-10-04)

Thanks!

### na...@google.com (2019-10-07)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-11-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-12-25)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/966914?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095159)*
