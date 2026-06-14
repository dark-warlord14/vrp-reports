# Chrome automatically downloads certain files even though the "Ask before downloading" option is enabled

| Field | Value |
|-------|-------|
| **Issue ID** | [40088749](https://issues.chromium.org/issues/40088749) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>Extensions, UI>Browser>Downloads |
| **Platforms** | Mac, Windows |
| **Reporter** | be...@gmail.com |
| **Assignee** | qi...@chromium.org |
| **Created** | 2017-08-18 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36

Steps to reproduce the problem:
1. Go to chrome://settings/?search=download
2. Enable the option "Ask where to save each file before downloading"
3. Start a HTTP server with the file below and a custom Content-Disposition header:

$ cat HManager.user.js
// ==UserScript==
// @name        test
// ==/UserScript==

$ = unsafeWindow.$;

$ python httpd.py 8080 'Content-Disposition:attachment; filename="HManager.user.js"'
Serving HTTP on 0.0.0.0 port 8080 ...

4. Visit the URL using Chrome and the file would be downloaded automatically. The following message will be displayed: "Apps, extensions, and user scripts cannot be added from this website."

What is the expected behavior?
Chrome should block the automatic download.

What went wrong?
Chrome downloaded the .js automatically without asking where to save the file before downloading.

Did this work before? N/A 

Chrome version: 60.0.3112.101  Channel: stable
OS Version: OS X 10.12.6
Flash Version:

## Attachments

- [chrome-down.png](attachments/chrome-down.png) (image/png, 216.0 KB)
- [chrome1.png](attachments/chrome1.png) (image/png, 237.7 KB)
- [chrome2.png](attachments/chrome2.png) (image/png, 258.5 KB)

## Timeline

### el...@chromium.org (2017-08-18)

[Comment Deleted]

[Monorail components: UI>Browser>Downloads]

### el...@chromium.org (2017-08-18)

[Comment Deleted]

[Monorail components: Platform>Extensions]

### el...@chromium.org (2017-08-18)

Fun; this works in a default install. Simpler repro: https://whytls.com/1.user.js

It happens because we treat files ending in ".user.js" specially: https://cs.chromium.org/chromium/src/chrome/browser/download/download_crx_util.cc?type=cs&sq=package:chromium&l=125

### el...@chromium.org (2017-08-18)

https://whytls.com/js.html is a different repro page that doesn't require that the user directly navigate to the file in the omnibox.

On Windows, we see that these navigations result in warning notifications in the Download tray (because .JS files are a dangerous file type on that platform) while on Mac they do not.

### be...@gmail.com (2017-08-18)

You can set any filename/extension on the Content-Disposition and Chrome would download it without the warning message. I tested your script on Windows and I received a warning. I tried the script below and the .js was downloaded without any warning:

$ echo hello > w00t.user.js
$ python httpd.py 8080 'Content-Disposition:attachment; filename="javascript.js"'
172.16.136.xxx - - [18/Aug/2017 19:49:47] "GET /w00t.user.js HTTP/1.1" 200 -

$ cat httpd.py
#!/usr/bin/env python

import SimpleHTTPServer
import BaseHTTPServer
import sys

"""
Usage:
    python httpd.py [port] [additional headers ...]
Example:
    python httpd.py 8000 'Pragma: no-cache' 'Cache-Control: no-cache' 'Expires: 0'
"""

class CustomHTTPRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_new_headers()

        SimpleHTTPServer.SimpleHTTPRequestHandler.end_headers(self)

    def send_new_headers(self):
        for i in sys.argv[2:]:
            key, value = i.split(":", 1)
            self.send_header(key, value)

if __name__ == '__main__':
    BaseHTTPServer.test(HandlerClass=CustomHTTPRequestHandler, ServerClass = BaseHTTPServer.HTTPServer, protocol="HTTP/1.1")


### rs...@chromium.org (2017-08-21)

Devlin: Can you please help triage.

### aw...@google.com (2018-02-14)

Bumping to Medium - this feels like the sort of thing that would turn up in a Pwn2Own exploit chain.

### sh...@chromium.org (2018-02-15)

rdevlin.cronin: Uh oh! This issue still open and hasn't been updated in the last 181 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-02-15)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-02-15)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-02-15)

We commit ourselves to a 60 day deadline for fixing for high severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### el...@chromium.org (2018-02-15)

Pairing this with another unpatched vulnerability, I think I can get a one-click RCE on Windows via this issue. 

Does Chrome even support user-script extensions any longer? Can we simply remove this special-case logic?

### rd...@chromium.org (2018-02-21)

Wow, that was a big jump (severity low -> severity high)!  awhalley@, elawrence@, I'll try to fllow up with y'all offline to get a little more detail on why this is so bad.

### el...@chromium.org (2018-02-21)

Andrew triaged to Medium in #7 and had a typo when assigning the label. I've fixed that.

I think there's a reasonable case to be made for keeping this at Low insofar as today Chrome doesn't treat .JS as a dangerous filetype and thus this mechanism for evading the prompt is only useful if the user has manually enabled prompting. 

However, I agree with the sentiment that this does seem like the class of bug that pops up as a part of larger, scarier chains.

### rd...@chromium.org (2018-02-21)

Given we don't currently warn for JS files, I think this is probably Low (one could make an argument for it just being a UI bug, since the behavior is exactly what would happen for most users that download a JS file).

Regardless, I'd still like to see it fixed.  I'll start digging.

### rd...@chromium.org (2018-02-23)

+some downloads folks.

This isn't looking to be quite as straight-forward (to me) as I'd like.  Conceptually, what I'd like the outcome to be is that we should treat a crx/user.js file like any other *unless* the download is coming directly from a source whitelisted in the policy (so for the vast majority of users, all crx/user.js files would just be treated normally).  This would hopefully also ensure that users are warned of danger, have the opportunity to choose the save target, etc.

Unfortunately, I can't find a good way of hooking in here.  We have download_crx_util, which does check if offstore installation is allowed (download_crx_util::OffStoreInstallAllowedByPrefs) as well as if it's an extension download (download_crx_util::IsExtensionDownload), but the flow is pretty convoluted.  We don't check if the offstore installation is allowed until *after* we already download the extension and try to install it, and otherwise just make decisions based on if an item is a crx/user.js file.  Ideally, we could basically just make an IsPermittedExtensionDownload(), but it looks like IsExtensionDownload is pretty widely used, and doesn't always have easy access to the associated profile (which we'd need for checking the policy).  And, somewhat more tricky, DownloadItem seems to indicate that many fields (like url and mime type) are fluid throughout the download process, and may not be set when the DownloadItem is created.

So, question for the downloads folks is: is there a good place we could hook in to check whether an extension download is permitted by policy?  Any rough idea how this would look?

I'm also very happy to hand this off to someone more familiar with downloads code, since I'm a bit out of my depth here. :)

### as...@chromium.org (2018-02-25)

-> dtrainor@

### sh...@chromium.org (2018-03-07)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-10)

rdevlin.cronin: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rd...@chromium.org (2018-03-11)

Assigning to dtrainor@ for downloads expertise (see https://crbug.com/chromium/756825#c16).

### dt...@chromium.org (2018-03-14)

+qinmin@ for more historical info in case I'm missing details.

Is the problem coming from DownloadTargetDeterminer checking IsExtensionDownload and bypassing the expected checks?  If that's the case, we should be able to check policy there.  IIUC at that point we've already gone through the redirect chain and have the mime type (Min let me know if I'm wrong about this part).

If you want a single place to check for all downloads that go by, you might be able to use DownloadManagerDelegate::InterceptDownloadIfApplicable().  That should be called after we've gotten the redirect chain/mime types as well and passes the relevant info to the delegate to figure out if the download should just be outright blocked or not.  But it doesn't sound like we want to block, we just don't want to bypass checks unless it's in the whitelist.

I'll look at the other calls to IsExtensionDownload later today/tomorrow.  It looked like we probably had a profile_ somewhere close to all the call sites (if we have the DownloadItem we are probably close to having the profile in the chrome/ layer).

### qi...@chromium.org (2018-03-15)

That logic is introduced here: http://codereview.chromium.org/252005 as it tries to fix crbug/23011. Not sure if the bug is still there if we enable the check, the bug is ancient


### dt...@chromium.org (2018-03-20)

rdevlin.cronin@ - Just to confirm, what's the policy called for whitelists extension sources?  Is OffStoreInstallAllowedByPrefs() the correct check?

### rd...@chromium.org (2018-03-22)

Yep, that's the one!

### dt...@chromium.org (2018-03-23)

Ok took a look at all IsExtensionDownload calls:

download_database.cc:
  - Don't save these to be resumed on restart/be tracked on chrome://downloads after restart.

download_commands.cc:
  - Don't enable "open using the platform handler," "open when download is complete," or "auto-open this type."
  - Check "open when complete" by default.

download_item_model.cc:
  - Tweak UI string for dangerous extensions vs. dangerous files.
  - Remove from the shelf when complete.
  - Don't show download started animation.

download_target_determiner.cc:
  - Bypass confirmation **the thing this bug wants changed**
  - Checking if extension & pref-whitelisted to default to not dangerous.

webstore_installer.cc:
  - Early-outs on completed downloads if not an extension.

download_item_notification.cc:
  - Tweak UI string for dangerous extensions vs. dangerous files and other status strings (e.g. installing, unpacking, etc.).

chrome_download_manager_delegate.cc:
  - Sets up an extension install on the "ShouldOpenDownload" request.

downloads_list_tracker.cc:
  - Does not show extension downloads in the DownloadsListTracker.


So I guess this comes down to a question about the behavior expectations on treating "IsExtensionDownload() == true" like other files except when white listed.  Do we actually only want download checks (target determinator for example) to behave like normal downloads?

### sh...@chromium.org (2018-04-19)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-05-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-09-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-10-17)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-12-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-01-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-04-24)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-06-06)

[Empty comment from Monorail migration]

### be...@chromium.org (2019-07-24)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-07-31)

[Empty comment from Monorail migration]

### jd...@chromium.org (2019-08-19)

dtrainor@: any movement on this?
- friendly security marshal

### dt...@chromium.org (2019-08-19)

Moving to Min who has the context and has worked on this code recently.  Min can you take a look?

### qi...@chromium.org (2019-08-21)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-08-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/4961219aafff3478250532a4872e3df59cbc645f

commit 4961219aafff3478250532a4872e3df59cbc645f
Author: Min Qin <qinmin@chromium.org>
Date: Wed Aug 21 18:25:12 2019

Treat extension download from untrusted sources as regular download

This CL treats extension downloads from untrusted sources as regular
downloads. That means these downloads will be prompted, show up in
downloads page and download shelf as normal downloads.

BUG=756825

Change-Id: I515bba2fa0a64198a56a06ce38864ef59ad18c9e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1761374
Reviewed-by: Xing Liu <xingliu@chromium.org>
Commit-Queue: Min Qin <qinmin@chromium.org>
Cr-Commit-Position: refs/heads/master@{#689091}

[modify] https://crrev.com/4961219aafff3478250532a4872e3df59cbc645f/chrome/browser/download/download_crx_util.cc
[modify] https://crrev.com/4961219aafff3478250532a4872e3df59cbc645f/chrome/browser/download/download_crx_util.h
[modify] https://crrev.com/4961219aafff3478250532a4872e3df59cbc645f/chrome/browser/download/download_crx_util_android.cc
[modify] https://crrev.com/4961219aafff3478250532a4872e3df59cbc645f/chrome/browser/download/download_history.cc
[modify] https://crrev.com/4961219aafff3478250532a4872e3df59cbc645f/chrome/browser/download/download_item_model.cc
[modify] https://crrev.com/4961219aafff3478250532a4872e3df59cbc645f/chrome/browser/download/download_target_determiner.cc
[modify] https://crrev.com/4961219aafff3478250532a4872e3df59cbc645f/chrome/browser/download/download_target_determiner_unittest.cc
[modify] https://crrev.com/4961219aafff3478250532a4872e3df59cbc645f/chrome/browser/ui/webui/downloads/downloads_list_tracker.cc


### qi...@chromium.org (2019-08-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-08-22)

[Empty comment from Monorail migration]

### na...@google.com (2019-08-26)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-08-27)

Requesting merge to beta M77 because latest trunk commit (689091) appears to be after beta branch point (681094).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-08-27)

This bug requires manual review: We are only 13 days from stable.
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
Owners: benmason@(Android), kariahda@(iOS), dgagnon@(ChromeOS), lakpamarthy@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### la...@google.com (2019-08-27)

gimin@ - please respond to C#46 to consider the merge request

### qi...@chromium.org (2019-08-27)

Does this require a merge? I don't think it is high security issue, as this behavior has been there for quite a long time. And it only impacts extension download, so I am not sure whether this qualifies for a merge

### la...@google.com (2019-08-27)

[Empty comment from Monorail migration]

### na...@google.com (2019-08-28)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### pa...@chromium.org (2019-08-28)

Congrats! The Panel decided to reward $500 for this report! 

### na...@google.com (2019-08-28)

[Empty comment from Monorail migration]

### ad...@google.com (2019-10-18)

[Empty comment from Monorail migration]

### ad...@google.com (2019-10-18)

bernardo.mrod@gmail.com, thanks for the report. How would you like to be credited in the release notes?

### ad...@google.com (2019-10-18)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-10-18)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-11-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-11-28)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-04)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-05)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/756825?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Platform>Extensions, UI>Browser>Downloads]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40088749)*
