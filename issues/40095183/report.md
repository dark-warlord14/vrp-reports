# Security: Possible to open new tab page, view-source: pages and chrome-native:// pages by redirecting a same-origin download

| Field | Value |
|-------|-------|
| **Issue ID** | [40095183](https://issues.chromium.org/issues/40095183) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Downloads, UI>Browser>Navigation |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | de...@gmail.com |
| **Assignee** | ti...@chromium.org |
| **Created** | 2019-05-27 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

Typically, it's not possible to open the new tab page, view-source: pages or chrome-native:// pages. However, by redirecting a same-origin download to one of these locations, it is possible to load each of these types of pages.

This issue was found as part of <https://bugs.chromium.org/p/chromium/issues/detail?id=966914>.

**VERSION**  

Chrome Version: Tested on 74.0.3729.169 (stable) and 76.0.3804.1 (canary)  

Operating System: Windows 10 Pro, version 1809

**REPRODUCTION CASE**

1. The attached files form a simple website. To begin with, download each of the files and place them in a directory.
2. In the directory you downloaded the files to, run the following command in a terminal:

python3 server.py 8080

This will start a simple web server that can be used to serve the files in the directory. server.py is necessary here, as it redirects requests received for download.txt:

if self.path.startswith('/download.txt'):  

self.send\_response(302)

```
location = parse_qs(urlparse(self.path).query).get('location', None)  
self.send_header('Location', location[0])  

self.end_headers()  

```

This is important in step 4.2 below, where a download for this file will be initiated.

3. In the browser, navigate to the following location:

<http://localhost:8080/index.html>

4. This page includes a number of sample links as well as an input form. You can either select one of the sample links or enter a URL in the form (allowing you to easily test whether a particular URL will load). Once you do enter or select a URL, the page will attempt to redirect to that URL. This is done as follows:

4.1. The page includes a link with the "download" attribute set.  

4.2. When you select a URL, it's appended onto the link location as a query parameter. The link is then clicked with JavaScript.  

4.3. server.py then redirects the request for this link to the URL you selected. This should fail for things like view-source: URLs; instead, the pages will be loaded. You can use the sample links to test this behavior.

It is possible to load some other types of pages as well:

1. chrome-search:// pages in an iframe

While view-source pages and chrome-native:// pages won't load in an iframe, some chrome-search:// pages will. Note that the new tab page itself won't load, because it has "X-Frame-Options" set to "DENY".

To test this, open the following page:

<http://localhost:8080/iframe_parent.html>

This page simply includes index.html in an iframe. If you click the chrome-search://most-visited/edit.html link, you should find that the link loads, unlike the other links on the page.

2. file:/// pages

As noted in <https://bugs.chromium.org/p/chromium/issues/detail?id=966914>, it is also possible to load file:/// pages using view-source: pages. Although not demonstrated here, this would work as follows:

If you attempt to load view-source:file:///C:/non-existent.html, the request will be rewritten to file:///C:/non-existent.html. If you can create this file (possible for files in the download directory), all you have to do is navigate the tab containing this page to another site, then navigate back.

The file, which now exists, will be loaded and if it's a HTML file you created, you can have it navigate to another file:/// location. I don't think it's very useful, though, as you have no way of retrieving the file data. You can really only use this to navigate to file:/// locations.

3. Chrome debug URLs

You can also indirectly load some Chrome debug URLs using view-source. For example, loading view-source:chrome://crashdump/ will create a crash dump, even though the view-source page apparently never loads.

4. data: URLs

You can load a data: URL in a top frame by first opening the new tab page then navigating it. You can test this by going through the following instructions:

4.1. Open a tab (to any page) and run the following command in the devtools console:

var newWindow = open("<http://localhost:8080/index.html>");

4.2. Switch to the new window and click the chrome-search://local-ntp/local-ntp.html link.

4.3. Switch back to the original tab and run the following in the devtools console:

newWindow.location.href = "data:text/html,<p>Test</p>";

This will load a data: URL within the new window.

**CREDIT INFORMATION**  

Reporter credit: David Erceg

## Attachments

- [iframe_parent.html](attachments/iframe_parent.html) (text/plain, 196 B)
- [index.html](attachments/index.html) (text/plain, 2.1 KB)
- [main.js](attachments/main.js) (text/plain, 393 B)
- [server.py](attachments/server.py) (text/plain, 691 B)

## Timeline

### ts...@chromium.org (2019-05-28)

[Empty comment from Monorail migration]

[Monorail components: UI>Browser>Navigation]

### sh...@chromium.org (2019-05-29)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### in...@chromium.org (2019-05-29)

Nasko, can you please help to find an owner for this.

### sh...@chromium.org (2019-06-11)

nasko: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-06-26)

nasko: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### li...@chromium.org (2019-08-07)

Friendly ping from the security marshal. nasko, any updates? Thanks!

### sh...@chromium.org (2019-09-11)

[Empty comment from Monorail migration]

### dr...@chromium.org (2019-10-17)

Friendly security sheriff ping - Any update on this? Is there another person we could assign this to?

### sh...@chromium.org (2019-10-23)

[Empty comment from Monorail migration]

### na...@chromium.org (2019-11-19)

Adding acolwell@ and lukasz@ to land a hand here in investigating the root cause.

### sh...@chromium.org (2019-12-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2020-02-05)

[Empty comment from Monorail migration]

### [Deleted User] (2020-04-09)

[Empty comment from Monorail migration]

### [Deleted User] (2020-05-20)

[Empty comment from Monorail migration]

### [Deleted User] (2020-07-14)

nasko: Uh oh! This issue still open and hasn't been updated in the last 237 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-07-16)

[Empty comment from Monorail migration]

### [Deleted User] (2020-07-28)

nasko: Uh oh! This issue still open and hasn't been updated in the last 251 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-08-26)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-07)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-30)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-18)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-20)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### ts...@chromium.org (2021-02-04)

[Empty comment from Monorail migration]

### na...@chromium.org (2021-02-24)

I attempted to reproduce some of the reported issues, but they don't seem to work at this time on desktop dev channel.

@reporter - it might be that I'm doing things wrong, so it would be great if you can check if the report still reproduces. Note that chrome-search: links might not work anymore, but I couldn't get any of the others to work either.

Thanks in advance!

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

### ad...@google.com (2021-07-08)

derceg86@ - ping for https://crbug.com/chromium/967411#c25!

### jd...@chromium.org (2021-07-21)

derceg86: another gentle ping re: https://crbug.com/chromium/967411#c25

### de...@gmail.com (2021-07-26)

From bisecting, it looks like this issue was largely fixed by:

https://crrev.com/c/1685093

Since most of the schemes used aren't present in ProfileIOData::IsHandledProtocol:

https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/profiles/profile_io_data.cc;l=25;drc=a277f0bd38143a3e76cd8004a7cd6bd0484a9ae9

The chrome-distiller: case seems to have been fixed at some later date and the only item that still works is chrome-search://local-ntp/local-ntp.html, which gets rewritten to chrome://new-tab-page/:

https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/search/search.cc;l=345;drc=68f5e124b92e78fb2f521d8749fc9d5f78a045d0

That is a chrome: URL, however, I don't think you can set any query parameters or otherwise interact with the page. It is still something that's usually blocked, though.

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

### [Deleted User] (2022-02-02)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-30)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-25)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-03)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-28)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-30)

[Empty comment from Monorail migration]

### pg...@google.com (2023-01-24)

Security marshal here!

@reporter, it seems like the issue was mostly fixed back in 2019 according to https://crbug.com/chromium/967411#c34 - are there any cases that you can see that still reproduces? looks like we've had trouble reproducing the issues before, so we would appreciate it if you can confirm!

@alex @creis while nasko is OOO, https://crbug.com/chromium/967411#c34 seems to imply that this issue has been mitigated (if not fully fixed).  Might we be able to close this bug?

### cr...@chromium.org (2023-01-24)

Thanks for the ping!  We're taking a look now to understand r678183 and whether it's sufficient as a fix.

### al...@chromium.org (2023-01-24)

Sharing some of our findings so far after a fresh look at this bug.  On the latest canary (111.0.5558.0), only one of the URLs from original repro still works - the one for chrome-search://local-ntp/local-ntp.html, which navigates to the NTP (interestingly, ending up on chrome://new-tab-page as a result).  All other URLs silently fail, except for the most-visited URL which leads to an error page.  So this is consistent with https://crbug.com/chromium/967411#c34.

+tiborg@: we don't allow renderers to navigate to the NTP directly, right?  Tldr here is that we encounter a redirect to chrome-search://local-ntp/local-ntp.html during a download, and that ends up navigating to the (new) NTP.  Redirecting to chrome://new-tab-page doesn't work, and renderer-initiated navigations to chrome-search://local-ntp/local-ntp.html also don't work (erroring out with "not allowed to load local resource"), but redirecting to chrome-search://local-ntp/local-ntp.html works.  So it seems that the NTP rewriting logic mentioned in https://crbug.com/chromium/967411#c34 is used to bypass some of our usual restrictions on NTP navigations in this case.

We also downloaded Chrome 74.0.3729.169 (Mac) and tried out the repro there, and indeed, most of the redirect URLs used to work, which is scary.  This includes chrome-native URLs, chrome-search://most-visited in an iframe, view-source:https://www.google.com/, view-source:chrome://settings (!!), and view-source:file.  The chrome-distiller URL led to an error page for me, and chrome-devtools: led to a failed download.  Note also that using chrome URLs directly (without view-source) didn't work, and data: URLs also didn't work, though we don't immediately know where that gets blocked; that might be worth understanding better.  Also, javascript: URLs *did* work: using javascript:alert("hi") on the repro page resulted in an alert.

We agree with https://crbug.com/chromium/967411#c34 that this was largely fixed by r678183, which added some scheme restrictions on download redirect targets.  Another important part of the fix seems to be setting the is_renderer_initiated bit on those navigations in r690869, which should hopefully help ensure that we block URLs that the renderer isn't allowed to navigate to. The bug was likely introduced in M69, when the feature to turn cross-origin redirects in downloads into navigations was added in https://chromium-review.googlesource.com/c/chromium/src/+/1138081.

Overall, the only remaining issue to look into here would be the unexpectedly allowed NTP redirect, everything else seems to be fixed.

[Monorail components: UI>Browser>Downloads]

### ti...@chromium.org (2023-01-25)

Yeah, renderer shouldn't navigate to an NTP. I think the primary reason we added the redirect was to provide seamless migration when we launched the WebUI NTP. We thought there may be users who navigate to chrome-search://local-ntp/local-ntp.html directly via a bookmark or some such. However, I'm supportive of removing the redirect to fix a potential security vulnerability.

### [Deleted User] (2023-02-08)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-05)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-31)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-16)

[Empty comment from Monorail migration]

### na...@chromium.org (2023-09-15)

[Empty comment from Monorail migration]

### ad...@google.com (2023-09-25)

Security shepherd here! Alex, Nasko has unassigned this, which is not allowed for security bugs. Please could you find a suitable owner? It sounds like you've got the most context.

### [Deleted User] (2023-10-11)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-06)

[Empty comment from Monorail migration]

### ja...@chromium.org (2023-12-12)

[secondary security shepherd]

Hi alexmos@, is there another fix you are planning on doing for this issue? Based on https://crbug.com/chromium/967411#c52 and https://crbug.com/chromium/967411#c53, it looks like you may be interested in blocking an NTP navigation.

An plan for next steps would be appreciated. Thanks!

### al...@chromium.org (2023-12-13)

Yes, it seems that the remaining fix here is to disallow the redirect to chrome-search://local-ntp/local-ntp.html, and it sounds like we can do that by removing support for chrome-search://local-ntp from the rewriting logic at [1].  This should be even safer now that chrome://new-tab-page has been around for a while. tiborg@, would you or someone on the NTP team be able to handle this, as owners of this code?

[1] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/search/search.cc;l=352;drc=68f5e124b92e78fb2f521d8749fc9d5f78a045d0

[Monorail components: UI>Browser>NewTabPage]

### ti...@chromium.org (2023-12-13)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-12-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/9bfc074d2233e7b747e990d71569aa0261ce0c2b

commit 9bfc074d2233e7b747e990d71569aa0261ce0c2b
Author: Tibor Goldschwendt <tiborg@chromium.org>
Date: Wed Dec 13 19:32:45 2023

[ntp] Remove local NTP redirect

Previously, when navigating to chrome-search://local-ntp we redirected
to chrome://new-tab-page. This smoothed the transition from the local to
the WebUI NTP. The local NTP is deprecated for a couple of years now.
It is time to remove the redirect.

Fixed: 967411
Change-Id: Iab14e7d377a5f1385f4a8723e03df6995e3aac4e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5120394
Reviewed-by: Alex Moshchuk <alexmos@chromium.org>
Commit-Queue: Tibor Goldschwendt <tiborg@chromium.org>
Code-Coverage: findit-for-me@appspot.gserviceaccount.com <findit-for-me@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#1237114}

[modify] https://crrev.com/9bfc074d2233e7b747e990d71569aa0261ce0c2b/chrome/browser/search/search.cc
[modify] https://crrev.com/9bfc074d2233e7b747e990d71569aa0261ce0c2b/chrome/common/url_constants.h


### [Deleted User] (2023-12-14)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-14)

[Empty comment from Monorail migration]

### am...@google.com (2024-01-03)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-01-03)

Congratulations David! The Chrome VRP has decided to award you a (long overdue) $1,000 for this report. Thank you for your efforts (almost five years ago) and reporting this issue to us, as well as your patience while it was resolved. 

### am...@google.com (2024-01-05)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

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

This issue was migrated from crbug.com/chromium/967411?no_tracker_redirect=1

[Multiple monorail components: UI>Browser>Downloads, UI>Browser>Navigation, UI>Browser>NewTabPage]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-21)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095183)*
