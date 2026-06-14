# Security: Possible to open chrome-native:// pages on Android and the new tab page on desktop using window.open

| Field | Value |
|-------|-------|
| **Issue ID** | [40095115](https://issues.chromium.org/issues/40095115) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Navigation |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | de...@gmail.com |
| **Assignee** | ac...@chromium.org |
| **Created** | 2019-05-21 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

On Android, the chrome-native:// scheme is used for some ChromeUI pages. For example, the bookmarks, history and new tab pages use this scheme. While it's typically not possible to open or link to one of these pages, using the "noopener" argument with window.open will allow this to be done. It's also possible to do the same thing with a link element in canary.

A similar thing can be done on desktop, to allow a site to open the new tab page, or a devtools page (the latter in canary only).

**VERSION**  

Chrome Version: On Android, tested on 74.0.3729.157 (stable) and 76.0.3800.0 (canary). On Windows, tested on 74.0.3729.157 (stable) and 76.0.3801.0 (canary).  

Operating System: Android version 9; Windows 10 Pro, version 1809

**REPRODUCTION CASE**

1. Open the history\_page\_android.html file in Chrome on Android.
2. This page simply sets up a click handler that makes the following call:

open("chrome-native://history", "\_blank", "noopener");

This should fail, given that chrome-native://history is a protected Chrome page, but instead it succeeds and the page is opened. To test this, click anywhere on the page.

It's not possible to do this without the "noopener" argument. Unlike the above, the following call will fail:

open("chrome-native://history", "\_blank");

A window will be created, but will point to about:blank.

Note that if you do open chrome-native://history using the first window.open call above, either on Android or on desktop, you won't be able to navigate back to it if you navigate to another site.

3. To test that the new tab page can be opened on desktop, open new\_tab\_page\_desktop.html.
4. Like the page above, this page sets up a click handler that makes the following call:

open("chrome-search://local-ntp/local-ntp.html", "\_blank", "noopener");

When you click the page, the new tab page should be opened.

5. Finally, on canary, the devtools scheme was recently changed from chrome-devtools:// to devtools://. It's possible to open a devtools page using the previous scheme, which is still registered as a fallback.

To test that this is possible, open devtools\_page\_canary.html in canary.

6. This page sets up a click handler that makes the following call:

open("chrome-devtools://devtools/bundled/inspector.html", "\_blank", "noopener");

Note that attempting to do this with the new scheme won't work:

open("devtools://devtools/bundled/inspector.html", "\_blank", "noopener");

This simply loads about:blank#blocked.

You can also open each of the above pages using a link element that has rel="noopener" specified. For example:

<a href="chrome-native://history" target="\_blank" rel="noopener">Open history page</a>

This doesn't work in stable or beta, but it does work in canary.

You can also try to load some other URLs using window.open and "noopener":

1. open("chrome-guest://1234", "\_blank", "noopener");

This crashes the browser, seemingly due to a failed CHECK.

2. open("data:text/html,<p>Test</p>", "\_blank", "noopener");

This will initially display a URL of about:blank, but if you click in the address bar and then somewhere else, or switch tabs and then switch back, the URL will change to the data: URL. There's no content on the page, though, so this isn't actually loading the data: URL.

**CREDIT INFORMATION**  

Reporter credit: David Erceg

## Attachments

- [devtools_page_canary.html](attachments/devtools_page_canary.html) (text/plain, 277 B)
- [history_page_android.html](attachments/history_page_android.html) (text/plain, 251 B)
- [new_tab_page_desktop.html](attachments/new_tab_page_desktop.html) (text/plain, 268 B)

## Timeline

### ts...@chromium.org (2019-05-22)

Setting severity medium as this kind of thing has been used as a middle step in an exploit chain in the past.
Nasko, could this be related to site isolation work? If not, please re-assign as appropriate.

### na...@chromium.org (2019-05-22)

The chrome-devtools: part of this bug is a regression in the range https://chromium.googlesource.com/chromium/src/+log/f0c6e2ad1d053536c7272106946bb23c76755aa2..af143acdc9c36721f8585f726d4862c4e9ce68ca and in specific r659944, which renamed the scheme from chrome-devtools: to devtools:. We can revert this one and reland it when the underlying issue is fixed.

The desktop opening chrome-search://local-ntp/ one seems to be allowed since at least 63.0.3224.0, which is how far I did a quick bisect so it will require a bit more investigation as to whether this was ever protected and if it was, when did it regress.

I have not looked at the chrome-native:// case for Android yet, so if anyone has a few cycles and can do a bisect there, that would be great.

### ke...@chromium.org (2019-05-23)

[Empty comment from Monorail migration]

[Monorail components: UI>Browser>Navigation]

### na...@chromium.org (2019-05-30)

I did a bit of poking around this area and I have a hypothesis why we have this behavior, so dumping some thoughts here for now. It is a hypothesis since I haven't confirmed in debugger/local build.

What makes window.open() with noopener special is that it does not maintain any references between windows and in that case if URL is specified as part of the window.open() call we kick off the navigation from the browser process. When the IPC is made to the browser side, we pass it through FilterURL which forbids specific URLs from being requested. However, there are more checks on the renderer side that I don't see browser side, which is why the navigation likely succeeds:

https://cs.chromium.org/chromium/src/content/renderer/render_thread_impl.cc?rcl=e11f0efeb859a36fee2974bfc2b8073a170f7e5f&l=1222
https://cs.chromium.org/chromium/src/chrome/renderer/chrome_content_renderer_client.cc?rcl=3ac7cf427357b11bc157b0d6587207ffeefe7497&l=398

Basically the schemes we get errors for in regular navigations are forbidden through the registration of those schemes as display isolated in Blink, but this capability seems to be lacking browser side. What surprises me is that we should not be allowing these through FilterURL since I don't see them registered as web safe schemes, but maybe I'm missing some other detail.

### sh...@chromium.org (2019-06-14)

nasko: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-06-29)

nasko: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### li...@chromium.org (2019-08-07)

Friendly ping from the security marshal. nasko, any updates? Thanks for helping look into this!

### sh...@chromium.org (2019-09-11)

[Empty comment from Monorail migration]

### dr...@chromium.org (2019-10-17)

Friendly security sheriff ping - Any update on this? Is there another person we could assign this to?

### sh...@chromium.org (2019-10-23)

[Empty comment from Monorail migration]

### na...@chromium.org (2019-11-19)

Adding acolwell@ who is looking at scheme registries and this is related.

### ac...@chromium.org (2019-11-20)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-12-11)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-01-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/eb21998c59d15a3925df632f6f2ade52cebc4be2

commit eb21998c59d15a3925df632f6f2ade52cebc4be2
Author: Aaron Colwell <acolwell@chromium.org>
Date: Thu Jan 16 02:17:27 2020

Make noopener partition selection consistent with normal path.

Fixing an inconsistency in the partition selection in
WebContentsImpl::CreateNewWindow(). The original code appeared to be
conflating SiteInstance selection with partition_id selection. This was
causing crashes when a new SiteInstance, created by the target_url
in the noopener case, resulted in a site URL that had a different
storage partition ID.(e.g. chrome-guest://blah). This change avoids
the crashes by separating the 2 concerns. partition_id selection is
now the same between noopener and normal paths. The special noopener
SiteInstance behavior is now handled by not providing a SiteInstance
in the CreateParams. This triggers the creation of a new SiteInstance,
that does not share a BrowsingInstance with the original source
SiteInstance. It also defers setting the site URL until we get the network
response and are ready to commit. This provides the desired behavior
and makes this case more consistent with other navigation scenarios.

Bug: 965611
Change-Id: I054c2f793138a2b373bac6c61b0a85368f0adb4e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1949285
Commit-Queue: Aaron Colwell <acolwell@chromium.org>
Auto-Submit: Aaron Colwell <acolwell@chromium.org>
Reviewed-by: Nasko Oskov <nasko@chromium.org>
Cr-Commit-Position: refs/heads/master@{#732229}

[modify] https://crrev.com/eb21998c59d15a3925df632f6f2ade52cebc4be2/content/browser/frame_host/render_frame_host_manager_browsertest.cc
[modify] https://crrev.com/eb21998c59d15a3925df632f6f2ade52cebc4be2/content/browser/web_contents/web_contents_impl.cc


### do...@chromium.org (2020-01-22)

Friendly security marshall ping: can this bug be marked as Fixed now?

### ac...@chromium.org (2020-01-22)

I haven't had a chance to verify that all these different cases are fixed yet.  The chrome-guest crash is definitely fixed and many of the "noopener" scenarios should now behave like the non-"noopener" path.

### sh...@chromium.org (2020-02-05)

[Empty comment from Monorail migration]

### de...@gmail.com (2020-02-24)

Just wanted to chime in here to say that it's still possible to open devtools: URLs using chrome-devtools: and noopener. While that did only affect canary when I reported the issue, it now works in stable as well. https://crbug.com/chromium/965611#c2 mentioned that the relevant change would be reverted, but I'm guessing it might not have happened.

### lu...@chromium.org (2020-02-24)

[Empty comment from Monorail migration]

### lu...@chromium.org (2020-02-24)

RE: https://crbug.com/chromium/965611#c18: derceg86@

Thanks for the ping.  I've tried the following repros in 81.0.4044.26:

1. open("chrome-devtools://devtools/bundled/inspector.html", "_blank", "noopener")
1.1. Bug still repros - this loads DevTools (unlike when "noopener" is not specified)
1.2. I've opened separate https://crbug.com/chromium/1055524 to track this (treating it as a security bug for now)

2. open("chrome-guest://1234", "_blank", "noopener")
2.1. no longer crashes, treats chrome-guest as an externally-handled scheme
2.2. maybe there is a remaining problem here - maybe chrome-guest should not be treated as an externally-handled scheme, but instead should error out with: "Not allowed to load local resource".  I've opened separate https://crbug.com/chromium/1055532 to track this (not a security bug).

3. open("data:text/html,<p>Test</p>", "_blank", "noopener") -> bug still repros - this doesn't load the data URL
3.1. I believe this is not a security bug (since there is no content in the opened page)
3.2. This fails with "Not allowed to navigate top frame to data URL" - this feels like a desired/WAI user agent intervention

I have NOT yet tested the chrome-native repro, but let me try to CC my personal account in order to try downloading and loading history_page_android.html on my Android phone.

### lu...@chromium.org (2020-02-24)

RE: https://crbug.com/chromium/965611#c18/#c19: derceg86@

I am not able to repro on 80.0.3987.117 on Android with: window.open("chrome-native://history", "_blank", "noopener");
Can you please confirm if the chrome-native aspect of the bug is not a problem anymore?


### de...@gmail.com (2020-02-25)

After trying to load a few chrome-native pages on Android, I couldn't reproduce the issue either, so it looks like it's fixed.

### lu...@chromium.org (2020-02-25)

RE: https://crbug.com/chromium/965611#c22:

Thanks!  I'll resolve the current bug as fixed in that case (and we can track chrome-guest and devtools follow-ups in https://crbug.com/chromium/1055532 and https://crbug.com/chromium/1055524).

### [Deleted User] (2020-02-26)

[Empty comment from Monorail migration]

### na...@google.com (2020-03-02)

[Empty comment from Monorail migration]

### [Deleted User] (2020-03-02)

Not requesting merge to beta (M81) because latest trunk commit (732229) appears to be prior to beta branch point (737173). If this is incorrect, please replace the Merge-na label with Merge-Request-81. If other changes are required to fix this bug completely, please request a merge if necessary.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### na...@google.com (2020-03-05)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-03-05)

Congrats! The Panel decided to award $1,000 for this report! 

### na...@google.com (2020-03-05)

[Empty comment from Monorail migration]

### ad...@google.com (2020-03-13)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-03-13)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-04-14)

[Empty comment from Monorail migration]

### [Deleted User] (2020-06-03)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/965611?no_tracker_redirect=1

[Monorail blocked-on: crbug.com/chromium/1055524]
[Monorail components added to Component Tags custom field.]

### sw...@gmail.com (2025-03-02)

<https://jingyan.baidu.com/article/1876c852a9358dc80b1376d2.htmlHTTP://WWW.MPEGLA.COMhttps://jdih.grobogan.go.id/ILDIS_31/berita/index?page=3https://tv.youtube.com/?sjid=680945974034088737-NC&utm_servlet=prod&rd_rsn=asi&onboard=1https://www.google.com/?sjid=10731017617270249661-APhttps://help.instagram.com/477434105621119https://www.microsoft.com/swiftkey>

### sw...@gmail.com (2025-03-02)

<https://globalstealth.net/>
<https://api.whatsapp.com/send/?phone=081228871380&text&type=phone_number&app_absent=0&wame_ctl=1>
<https://programmablesearchengine.google.com/about/>
<https://play.google.com/apps?pli=1>
<https://www.unicode.org/copyright.htmlcoloros.feedback@oppo.com>
<https://creativecommons.org/licenses/by/3.0/igo/legalcode>
<https://kachaa.haokan.mobi/page/103009/318333/1?utm_source=5&utm_medium=Lock_screen&utm_campaign=103009&utm_content=5375913&det_type=true>
<https://assistant.google.com/>
componentid:1400036
<https://kachaa.haokan.mobi/page/103009/189449/1?utm_source=5&utm_medium=Lock_screen&utm_campaign=103009&utm_content=5312368&det_type=true>
<https://www.meta.com/quest/quest-2-facial-interface-recall/>

### sw...@gmail.com (2025-03-02)

deleted

### sw...@gmail.com (2025-03-02)

deleted

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095115)*
