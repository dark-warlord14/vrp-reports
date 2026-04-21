# Security: Possible to escape sandbox via devtools_page and Feedback app

| Field | Value |
|-------|-------|
| **Issue ID** | [40052870](https://issues.chromium.org/issues/40052870) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Platform>Apps, Platform>DevTools, Platform>Extensions |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | de...@gmail.com |
| **Assignee** | ds...@chromium.org |
| **Created** | 2020-07-16 |
| **Bounty** | $15,000.00 |

## Description

**VULNERABILITY DETAILS**  

By specifying a devtools\_page entry, an extension can run code within the context of an inspected page once the user opens the devtools. An extension can use this ability to run code within the context of the Feedback app and create an app window. That window can then be used to launch a file that was downloaded, provided that the current browser instance is not the system default browser.

**VERSION**  

Chrome Version: Tested on 84.0.4147.89 (stable) and 86.0.4204.1 (canary)  

Operating System: Windows 10, version 1909

**REPRODUCTION CASE**

1. Ensure that the browser instance you're using to test is not the system default browser.
2. Install the attached extension.
3. Open the devtools on a non-privileged page.
4. Wait about 5 seconds.
5. The target executable (in this case, Process Explorer) should be started.

**CREDIT INFORMATION**  

Reporter credit: David Erceg

## Attachments

- [background.js](attachments/background.js) (text/plain, 275 B)
- [devtools_page.html](attachments/devtools_page.html) (text/plain, 132 B)
- [devtools_page.js](attachments/devtools_page.js) (text/plain, 3.0 KB)
- [local.html](attachments/local.html) (text/plain, 334 B)
- [manifest.json](attachments/manifest.json) (text/plain, 289 B)

## Timeline

### de...@gmail.com (2020-07-16)

The extension here goes through the following steps:

1. Once the user has opened the devtools, the extension will download two files:

- local.html
- Process Explorer

2. Once both of the above downloads have completed, the extension will navigate the page being debugged to:

view-source:chrome-extension://gfdkimpbcpahaombhbimeihdjnejgicl/js/feedback.js

This is a javascript file contained within the Feedback app.

Note that the navigation to this URL is performed via the chrome.debugger API by sending the Page.navigate command. The reason this is done is that it's not possible to navigate to this location using chrome.tabs.update (an error page will simply be shown).

Additionally, the only reason the above URL is a view-source: URL is that it's not possible to navigate to the file directly. The view-source: URL, however, will load and the page will have access to all of the APIs that the Feedback app has access to.

3. The extension will then use chrome.devtools.inspectedWindow.eval to run code within the context of the page. Note that unlike https://crbug.com/chromium/1101897, which specifically relies on a timing issue to run code within the context of a privileged page, here, chrome.devtools.inspectedWindow.eval can simply be called directly. That's because although the devtools attempts to block extensions when debugging a chrome: or devtools: page, chrome-extension: pages aren't currently blocked in any way:

https://source.chromium.org/chromium/chromium/src/+/master:third_party/devtools-frontend/src/front_end/extensions/ExtensionServer.js;l=1030;drc=4576282f49d8129b6374dd0fd389271c0a291b6a

The extension uses chrome.devtools.inspectedWindow.eval to run the following code:

chrome.app.window.create("file:///path/to/local.html")

The chrome.downloads API is used to retrieve the path to this file (which was downloaded in step 1). It would be possible to determine the location of the downloads directory without use of the chrome.downloads API (via the chrome.settingsPrivate.getPref method made available to the Chrome Media Router extension), but using chrome.downloads simplifies the demonstration.

For apps that the user installs, the call above would fail. That's because passing an absolute path to chrome.app.window.create normally triggers an error:

https://source.chromium.org/chromium/chromium/src/+/master:extensions/browser/api/app_window/app_window_api.cc;l=159;drc=12b407642b48f5f29782f09a703021be62d0ccfb

However, apps installed as components (such as the Feedback app) are allowed to pass an absolute URL into chrome.app.window.create, which means the call above will succeed.

4. Once the app window has been created and local.html has been loaded, it will make the following call:

window.open("file:///path/to/processexplorer");

Again, the chrome.downloads API is used to retrieve the path to this file (which was also downloaded in step 1). Also, this call is the reason why local.html is downloaded first - normally, only local files have the ability to call window.open with the path of a local file.

When the current browser instance is not the system default browser, calling window.open from an app window results in the call being passed directly to the OS:

https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/ui/apps/chrome_app_delegate.cc;l=109;drc=3abb32da2944ffe178dd66f404e7e1bb88a58ed0

For a file: URL, that results in the file being opened. Since the file in this case is an executable, the executable is run.

### de...@gmail.com (2020-07-16)

One other related thing to note is that the _canInspectURL method in ExtensionServer.js blocks attempts to debug the Web Store:

https://source.chromium.org/chromium/chromium/src/+/master:third_party/devtools-frontend/src/front_end/extensions/ExtensionServer.js;l=1033;drc=4576282f49d8129b6374dd0fd389271c0a291b6a

However, because pages with the chrome-extension scheme aren't blocked, this check won't stop an extension from being able to make use of APIs available to the Web Store.

To do that, an extension could navigate the page being debugged to a file within the Web Store app. For example:

chrome-extension://ahfgeienlihckogmohjhadlkjgocpleb/webstore_icon_16.png

That page has access to the full set of APIs provided to the app. An extension embedded within the devtools can then make use of those APIs.

### me...@chromium.org (2020-07-17)

I tried reproing this on trunk linux (replacing procmon with a different executable that would work on Linux) but it didn't seem to work, the download of the executable failed with the message "Failed - No file".

caseq@ or rdevlin.cronin@ could one of you please take a look?

[Monorail components: Platform>DevTools Platform>Extensions]

### [Deleted User] (2020-07-18)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@chromium.org (2020-07-20)

bmeurer@ I am not sure we can do anything about it?

### bm...@chromium.org (2020-07-20)

I'm lacking some historical / technical context on this. From a first glance it looks like this could be WAI.

I'd like to hear from caseq@ on this.

### rs...@chromium.org (2020-07-28)

caseq: Could you see https://crbug.com/chromium/1106456#c6?

### [Deleted User] (2020-07-31)

caseq: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### de...@gmail.com (2020-08-06)

While waiting for caseq to take a look at this, I think I can offer a bit of additional context (based on what I've found when looking back through some of the history of the relevant code), and whether the behavior is intended.

Firstly, since the ability to call chrome.app.window.create with an absolute URL is blocked for regular extensions, it's something that's only relevant for component extensions.

The ability for a component extension to pass an absolute URL was first added in this commit:

https://chromiumcodereview.appspot.com/11048045

Before that, the URL was always treated as relative to the extension:

https://chromiumcodereview.appspot.com/10391199/diff/35003/chrome/browser/extensions/api/app_window/app_window_api.cc#newcode27

It looks like the change was made to allow chrome.app.window.create to be called with the following URL:

chrome://settings-frame/settings

From searching through the Chromium codebase, I've found the following two places where an absolute URL is currently passed to chrome.app.window.create (though it's possible there are other places that I missed or am unaware of):

URL: chrome://histograms
https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/resources/feedback/js/feedback.js;l=510;drc=d6a8ee4d9d1db6a1453ed94a2214a98d78c7a866

URL: chrome://slow_trace/tracing.zip
https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/resources/feedback/js/feedback.js;l=167;drc=d6a8ee4d9d1db6a1453ed94a2214a98d78c7a866

Both of these are also chrome: URLs.

So being able to pass a file: URL into chrome.app.window.create and then directly open a local file (particularly an executable file) from that window doesn't seem like it would be part of the intended functionality.

Even if a component app were relying on being able to open a local file using this method, it wouldn't work when the current browser instance was the system default; in that case, the file would be opened within the browser.

I can think of two ways the overall issue raised here might be fixed:

1. The first would be to block embedded extensions within the devtools when debugging a chrome-extension: page.
2. The second would be to block window.open calls in app windows, when the target is a file: URL. Regular apps can't call window.open with a file: URL anyway, so they would be unaffected. Apps installed as components would first have to call chrome.app.window.create with a file: URL, since they can't call window.open with a file: URL either.

It's also possible to take advantage of the behavior described here using the behavior described in https://crbug.com/chromium/1113558. That would allow an extension with the debugger permission to open a local executable file, provided that the current browser instance isn't the system default browser. No user interaction would be required after the extension install.

So preventing window.open calls with file: URLs would fix this issue and prevent it from being taken advantage of in other situations.

### [Deleted User] (2020-08-15)

caseq: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-08-26)

[Empty comment from Monorail migration]

### ca...@chromium.org (2020-08-28)

Devlin, do you have an insight on why we expose extension bindings to view-source: pages?

### rd...@chromium.org (2020-08-28)

Interesting!

I confess, I have very little knowledge of how view-source works under the hood.  But poking around a view-source console for a bit, it looks like it actually "thinks" it's the real page.  From the task manager, it also seems like it commits within the same process as the inspected page.  If the renderer commits to an origin that has access to extension APIs from within a process that's trusted to have access to those APIs, we would instantiate the bindings on the renderer side and allow access - as far as most systems know, it's an extension page.

What's more, it doesn't look like this is restricted to extension APIs.  Opening up view-source for a chrome:// page like settings or extensions also grants access to chrome.send().  Which means there's a lot of equal badness that can happen there, if the extension were able to connect to those.

I think the underlying issue here is that the extension shouldn't be allowed to debug a view-source frame if it can't access the underlying URL.  Though, separately, I am curious why view-source pages have JS access at all - it seems like we could make them just plaintext.  Charlie, do you have some more context there?

From c#1:

> That's because although the devtools attempts to block extensions when debugging a chrome: or devtools: page, chrome-extension: pages aren't currently blocked in any way:

That's interesting.  We don't normally allow extensions to debug other extensions - check out ExtensionCanAttachToURL() [1] and PermissionsData::IsRestrictedURL() [2] - doing so should require a very-scary commandline switch ("extensions-on-chrome-urls", at which point all bets are off).  Is this an issue where a) the debugger isn't being properly detached after navigating to a restricted page (in which case, would this be fixed by some of the other bugs we've seen here?), or b) we're not classifying the inspected URL properly as being restricted?  (Said differently, is ExtensionCanAttachToURL() checked upon navigation to the view-source page?)


[1] https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/extensions/api/debugger/debugger_api.cc;l=91-110;drc=02fc05043bd38d318ba9ce59ccc4c7602284f990
[2] https://source.chromium.org/chromium/chromium/src/+/master:extensions/common/permissions/permissions_data.cc;l=107-151;drc=02fc05043bd38d318ba9ce59ccc4c7602284f990

### ca...@chromium.org (2020-08-28)

I think ExtensionCanAttachToURL() works as intended here, at least based by David's comments (https://bugs.chromium.org/p/chromium/issues/attachmentText?aid=456756#65) and the fact that view-source: is not in within the list of valid schemes for  URLPattern::IsValidSchemeForExtensions()  -- the problem is rather in chrome.devtools API (i.e. the front-end, AKA devtools_page extensions) that uses a different check. We'll fix that check, of course, although it would still leave us with http://crbug.com/1101897 for now.

That said, exposing bindings to a scheme that isn't supposed to take any legitimate advantage of them looked suspicious to me, so I wonder if this needs to be fixed in more than one place.


### cr...@chromium.org (2020-08-28)

> Though, separately, I am curious why view-source pages have JS access at all - it seems like we could make them just plaintext.  Charlie, do you have some more context there?

Sorry, that predates me.  :)  I'm aware that view-source loads the original URL in a different mode, but I'm not sure how the mode works.  In general (without having read the rest of the context here), I'd be happy to see it locked down.

### rd...@chromium.org (2020-08-28)

> That said, exposing bindings to a scheme that isn't supposed to take any legitimate advantage of them looked suspicious to me, so I wonder if this needs to be fixed in more than one place.

> I'm aware that view-source loads the original URL in a different mode, but I'm not sure how the mode works.  In general (without having read the rest of the context here), I'd be happy to see it locked down.

Sounds like we're all on the same page of "it'd be nice to lock this down more, since it shouldn't _really_ need anything".  Do we know who the best owner for view-source changes would be?

### [Deleted User] (2020-09-15)

We commit ourselves to a 60 day deadline for fixing for high severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-10-07)

[Empty comment from Monorail migration]

### va...@chromium.org (2020-10-22)

Friendly ping from the security 👮 for this High severity bug. Any updates?

For high severity vulnerabilities, we aim to deploy the patch to all Chrome
users in under 60 days.

### [Deleted User] (2020-10-30)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-18)

[Empty comment from Monorail migration]

### ts...@chromium.org (2020-11-30)

+mkwst, anyone in OWP have an interest in this?  Only tangentially related, but when it comes to taking away capabilities within a renderer, ahem ...

### [Deleted User] (2021-01-20)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-03)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-11)

[Empty comment from Monorail migration]

### zh...@google.com (2021-03-17)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-15)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-26)

[Empty comment from Monorail migration]

### ad...@google.com (2021-07-08)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-05)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-07)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-16)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-11)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-22)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-15)

[Empty comment from Monorail migration]

### cr...@chromium.org (2021-12-02)

Thanks to adetaylor@ for a ping on this.  Devlin and I both looked a little more closely today.  I really appreciate the detailed report and followup comments, and it's unfortunate this fell between the cracks.

First, I think the view-source privileges part is probably a red herring.  I think view-source pages are put into the same SiteInstance / principal as a normal URL from that origin, and loaded in a special RenderFrame mode.  Even if we went to the effort of putting view-source: pages into separate unprivileged processes (still separate from other sites), they would still be able to navigate to their own non-view-source URL and then end up in a privileged process (e.g., using injected scripts as done here).  So I'm guessing the attack would still work, with an extra "location.href = location.href" step to exit view-source mode.  We can have a separate discussion of whether it's worth the process model complexity to reduce view-source privileges anyway, but I think there are more important bugs to solve here.

Second, I'm wondering if the severity is set properly here.  The fact that the browser cannot be the system default browser is one mitigation, though perhaps not enough to reduce to Medium severity on its own.  Another mitigation is having to install a malicious extension with a "Manage your downloads" message shown during installation due to the downloads permission.  That already seems close to something that could do a sandbox escape for free-- I think the only distinction is that a second downloads.open permission is technically required to open a downloaded file (per https://developer.chrome.com/docs/extensions/reference/downloads/#method-open), though that isn't documented at https://developer.chrome.com/docs/extensions/mv3/declare_permissions/?  Combined, I wonder if this is Medium rather than high, but I'll defer to security sheriffs on that.

Still, it seems like we have a lot of partial security checks here that are being evaded, and we should try to fix them.  Here's a list I've identified:

1) If chrome.tabs.update doesn't allow navigating to the view-source:chrome-extension://gfdkimpbcpahaombhbimeihdjnejgicl/js/feedback.js URL, can we prevent it via Page.navigate as well?
At first glance, it seems wrong that the restrictions for these differ.

2) Can we block view-source platform app URLs from loading in tabs, if their equivalent platform app URLs can't load in tabs?
Devlin suggested this over chat, and it makes sense to me.  Not sure where the platform app URL restriction lives.

3) Can we prevent DevTools extensions from running code in extensions (similar to chrome:// and devtools:// pages)?
This is suggestion 1 in https://crbug.com/chromium/1106456#c9, confirmed by Devlin in https://crbug.com/chromium/1106456#c13.  Maybe this involves excluding chrome-extension:// from the _canInspectURL logic here?
https://source.chromium.org/chromium/chromium/src/+/master:third_party/devtools-frontend/src/front_end/extensions/ExtensionServer.js;l=1030;drc=4576282f49d8129b6374dd0fd389271c0a291b6a
I think this would also fix the Chrome Web Store attack vector described in https://crbug.com/chromium/1106456#c2.

4) Can we remove the component app exception that allows creating a window to a file:// URL?
This is related to suggestion 2 in https://crbug.com/chromium/1106456#c9, and Devlin turned up the comment below which suggests that we might be able to remove this ability for component apps:
https://source.chromium.org/chromium/chromium/src/+/master:extensions/browser/api/app_window/app_window_api.cc;l=150-152;drc=12b407642b48f5f29782f09a703021be62d0ccfb
In particular, it looks like that ability was added in r161828 for https://crbug.com/chromium/130210, and I wonder if allowing chrome:// URLs is sufficient and safe (rather than arbitrary URLs like file://).

5) Can we block platform apps from sending executable/dangerous URLs to the OS (when Chrome isn't the default browser)?
See https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/ui/apps/chrome_app_delegate.cc;l=109;drc=3abb32da2944ffe178dd66f404e7e1bb88a58ed0 from https://crbug.com/chromium/1106456#c1.

These seem split across DevTools and extension/app code.  Maybe Devlin can work with DevTools folks to split them up, if these changes make sense?

### rd...@chromium.org (2021-12-02)

Thanks, Charlie!

>  So I'm guessing the attack would still work, with an extra "location.href = location.href" step to exit view-source mode. 

Except that then it's trying to open a platform app resource in a chrome tab, which wouldn't work : )  So I think this *would* stop the attack vector in this case.  That said, I agree there's complexity here, and I don't think we should remove privileges for view-source just for this issue.  It might still be worth discussing, though.

Thanks for concretizing the tasks here!  2) and 4) seem very much in the extensions area; I'll file separate bugs for those and see if we can get some attention on them.  1) is in CDP, so I'll leave that to dsv@.  dsv@ also asked about 3) recently in another thread; dsv@, are you planning on looking into that?  5) is apps-related - dominickn@, can you help find someone to tackle that?

[Monorail components: Platform>Apps]

### rd...@chromium.org (2021-12-02)

Filed https://crbug.com/chromium/1276041 for 2) and https://crbug.com/chromium/1276046 for 4) from c#40.

### rd...@chromium.org (2021-12-02)

[Empty comment from Monorail migration]

### rd...@chromium.org (2021-12-02)

[Empty comment from Monorail migration]

### do...@chromium.org (2021-12-02)

> 5) Can we block platform apps from sending executable/dangerous URLs to the OS (when Chrome isn't the default browser)?

What is an executable/dangerous URL in this context? And is it expected behaviour for platform apps to be able to execute something like window.open("file://path/to/local") (given that platform apps are technically "local" files)?

### ds...@chromium.org (2021-12-03)

1) We could add check to Page.navigate, but it would still be possible to do achieve the same result using Runtime.evaluate("location.href=...") or similar with
DOM.SetOuterHTML("<iframe src=...>") so I'm not sure we could really address this.

3) Yes, I am.

### rd...@chromium.org (2021-12-15)

@ https://crbug.com/chromium/1106456#c45

> What is an executable/dangerous URL in this context? And is it expected behaviour for platform apps to be able to execute something like window.open("file://path/to/local") (given that platform apps are technically "local" files)?

Hmm... I'd lean towards saying platform apps shouldn't be able to open arbitrary files, no matter what.  This capability today is only possible for component apps, so it seems like there's little risk of breakage there, and Chrome already blocks renderer-initiated navigation to file: URLs.  "Executable/dangerous" here could be something like an exe - but I'd argue we should just disallow this in general, and probably shouldn't be punting to the system for opening any resources.  Of course, I might be missing a use case that relies on this, but I can't think of any off the top of my head.  I'd be interested in the code history there to see why we added it.

### [Deleted User] (2022-02-02)

[Empty comment from Monorail migration]

### ad...@google.com (2022-03-23)

dsv@ are you a better owner here these days?

And, could you confirm what needs to be done under this particular crbug (as opposed to the bugs which Devlin raised separately?)

### ds...@chromium.org (2022-03-23)

In crbug/1115460 I already forbid devtools extension access to component extension. Do I understand correctly that forbidding "view-source:" prefix to the list of forbidden origin would close this vulnerability?

### ad...@chromium.org (2022-03-24)

(to state the obvious - I don't understand this bug well enough to answer https://crbug.com/chromium/1106456#c50 definitively - so I hope that question was addressed at Devlin or Charlie!)

### rd...@chromium.org (2022-03-28)

@50: I think that would be sufficient.  I'd prefer the farther-reaching change of changing view-source pages to be permission-less text-only contexts (which would then solve this issue and any related issues), but that's a much farther reaching change.

While https://crbug.com/chromium/1276041 is nice-to-have, I don't think it needs to block resolution of this bug.

### [Deleted User] (2022-03-30)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-04-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/359da7a1736043e30ee0a9f1e5ac9597422bf877

commit 359da7a1736043e30ee0a9f1e5ac9597422bf877
Author: Danil Somsikov <dsv@chromium.org>
Date: Mon Apr 04 08:32:54 2022

Add an extra test to check that devtools extension can't use
view-source: scheme to circumvent access checks.

Bug: 1106456
Change-Id: Icedc2c65f94de97e18ecb66e622ac1fa2b0ef044
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3563061
Auto-Submit: Danil Somsikov <dsv@chromium.org>
Reviewed-by: Yang Guo <yangguo@chromium.org>
Commit-Queue: Yang Guo <yangguo@chromium.org>
Cr-Commit-Position: refs/heads/main@{#988409}

[modify] https://crrev.com/359da7a1736043e30ee0a9f1e5ac9597422bf877/chrome/browser/devtools/devtools_browsertest.cc
[modify] https://crrev.com/359da7a1736043e30ee0a9f1e5ac9597422bf877/chrome/test/data/devtools/extensions/can_inspect_url/devtools.js
[modify] https://crrev.com/359da7a1736043e30ee0a9f1e5ac9597422bf877/chrome/test/data/devtools/extensions/can_inspect_url/manifest.json


### ds...@chromium.org (2022-04-04)

I can't reproduce the issue and I think my previous CLs that forbid connecting to the component extensions are enough as view-source: URLs are handled specially [1] and DevTools gets to see a URL without a view-source: prefix. I've added a test to confirm that and I think the issue could be closed.

[1]: https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/navigation_controller_impl.cc;l=428;drc=7fb345a0da63049b102e1c0bcdc8d7831110e324;bpv=0;bpt=1

### [Deleted User] (2022-04-04)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-04)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-04)

Requesting merge to stable M100 because latest trunk commit (988409) appears to be after stable branch point (972766).

Requesting merge to beta M101 because latest trunk commit (988409) appears to be after beta branch point (982481).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-04-05)

Merge review required: M101 is already shipping to beta.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: benmason (Android), harrysouders (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-04-05)

Merge review required: M100 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), harrysouders (iOS), dgagnon (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ds...@chromium.org (2022-04-05)

No need to merge, the fix is https://chromiumdash.appspot.com/commit/09927ca7399717d3bb45c2948ffbb7682526b579  and is already in M100M.

### ad...@google.com (2022-04-08)

(labelling as Release-2-M100 so this gets picked up in the next release notes, even though we fixed this a while back)

### ad...@google.com (2022-04-11)

[Empty comment from Monorail migration]

### am...@google.com (2022-04-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-04-13)

Congratulations, David! The VRP Panel has decided to award you $15,000 for this report. Thanks for all your efforts and great work! 

### am...@google.com (2022-04-16)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2022-07-26)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-29)

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

This issue was migrated from crbug.com/chromium/1106456?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Platform>Apps, Platform>DevTools, Platform>Extensions]
[Monorail blocked-on: crbug.com/chromium/1276041, crbug.com/chromium/1276046]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40052870)*
