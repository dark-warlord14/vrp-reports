# Security: Extension popups can read local files if a Browser Action invoked on a file:/// URL

| Field | Value |
|-------|-------|
| **Issue ID** | [40090610](https://issues.chromium.org/issues/40090610) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Platform>Extensions |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | 93...@gmail.com |
| **Assignee** | ka...@chromium.org |
| **Created** | 2018-02-26 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

Extension popups can load local files on the disk upon clicking on the extension icon in the toolbar (to open the popup), provided that you are viewing a file:/// URL at that time. Since extensions are exempt from the same origin policy, the parent frame (if there were to be a script in it) could read the subframe containing the contents of the local file. This means that, under certain circumstances (clicking on the extension icon while on a file:/// URL), Chrome extensions could be used to spy on local data.

**VERSION**  

Chrome Version: 66.0.3355.0 canary  

Operating System: Windows 7 Home Premium Service Pack 1

**REPRODUCTION CASE**  

This vulnerability can be demonstrated by following the instructions below:

1. Download the attached zip file.
2. Extract it to C:, so that the folder path is C:\Testcase.
3. In Chrome, open chrome://extensions.
4. Click "LOAD UNPACKED" under the search bar at the top.
5. Load "C:\Testcase\extension".
6. Once the extension has been added to Chrome, open file:///C:/ (any file:/// URL works).
7. Click on the extension icon in the toolbar (gray "T", since it doesn't have its own icon).
8. Wait a second or two for it to load.

NOTE: The password is just a fake, randomly generated password, and is not actually in use. Therefore, it is OK to derestrict this bug.

NOTE: This bug is subject to a 60-day disclosure deadline. If 60 days elapse without a fix in the source code, this bug will be publicly disclosed.

## Attachments

- [Testcase.zip](attachments/Testcase.zip) (application/octet-stream, 717 B)
- [Extension Popup.PNG](attachments/Extension Popup.PNG) (image/png, 2.9 KB)
- [Extension Popup on file URL.png](attachments/Extension Popup on file URL.png) (image/png, 129.6 KB)
- [Extension Page.PNG](attachments/Extension Page.PNG) (image/png, 51.4 KB)

## Timeline

### 93...@gmail.com (2018-02-26)

This vulnerability affects all of the following:

- File directories
- Local text (TXT) files, as demonstrated in the report
- Local HTML documents
- Local PDF documents
- Local images (PNG, JPG, JPEG, GIF, TIFF, TIF, BMP, ICO, etc.)

While one may think that "In order for that to be exploited by an attacker, they would have to be able to guess the path of the file they want to read". However, that is not true. The reason that is not true is because an extension could iframe to a file:///C:/ to explore all of the different directories and files on the disk. They could make a map of your filesystem and capture the names of all of your files. When they find a file of a type listed above (essentially, filetypes that Chrome can process), they can also iframe to those as well to read their contents. Furthermore, they can set in the HTML/CSS code to not show the iframe, so that it is present without the user seeing what is going on. Considering that only clicking on the extension icon while on a file:/// URL is enough to trigger this, I advise against classifying this as low severity.

### el...@chromium.org (2018-02-26)

Thanks for the report.

In terms of disclosure, please be aware that disclosure before patching may impact an issue's eligibility to participate in the Chrome Vulnerability Rewards program: https://www.google.com/about/appsecurity/chrome-rewards/index.html

This is similar in nature to https://crbug.com/chromium/810220.

[Monorail components: Platform>Extensions]

### 93...@gmail.com (2018-02-26)

I do understand that disclosure before patching may impact reward eligibility. However, I have the deadline anyway to ensure that bugs are fixed in a timely matter.

Could you summarize what https://crbug.com/chromium/810220 is about, if that is OK? I don't need to know all of the instructions to exploit it.

### ke...@chromium.org (2018-03-01)

https://crbug.com/chromium/810220 is basically the same thing (a malicious extension walking the file system), but the specific steps are a bit different. It looks like the PoC extension here only has 'activeTab' and 'storage' permissions, with all_urls does it remove the requirement that the user manually navigate to a file: URL?

Devlin, do you have any thoughts on this, and whether there it adds anything new?

### 93...@gmail.com (2018-03-01)

For the PoC here, I really just worked off of the manifest.json template on the Chrome developer site (https://developer.chrome.com/extensions/getstarted).

That's worth considering that adding the all_urls permission could allow extensions to walk the filesystem with NO user interaction. If that's possible, then this should be a Pri-0 and Security_Severity-Critical. In other words, it's extremely critical that the damage of malicious Chrome extensions is limited to Chrome only and does not affect the user's personal data outside of Chrome.

I'd like to note that I'm not good at coding extensions, so that's probably why I didn't understand well enough to know about the all_urls permission when first reporting this bug.

### 93...@gmail.com (2018-03-01)

[Comment Deleted]

### 93...@gmail.com (2018-03-09)

[Comment Deleted]

### ke...@chromium.org (2018-03-09)

Devlin are you able to take a look at this?

### rd...@chromium.org (2018-03-12)

This is interesting.  I don't think it's the same bug as https://crbug.com/chromium/810220.

I haven't had a chance to dive too deeply into this yet, but it appears that
a) we allow file iframes to load when the extension has file access
b) this file access could come from *either* explicitly granting it in the chrome://extensions page (Note: unpacked extensions are default-granted) or from the activeTab permission on a file:/// URL.
c) Once the extension has access to file URLs, it can embed the URL in its extension page.

Funnily enough, the extension can't actually access that frame, it seems - we throw an error: "Blocked a frame with origin "chrome-extension://<id>" from accessing a cross-origin frame."  However, this isn't very useful, since if the extension has access to the file url, it could just use tabs.executeScript to run on the page.

The biggest question here is how much this is or isn't WAI.  Extension may, with explicit permission, access file:// URLs.  I think that, if a user explicitly grants this permission, there's not much we should do here.  There's a reason we make that a separate permission and bury it deep in the settings - it's moderately scary.  So I'd argue that the case of "the user explicitly enabled the extension to run on file urls in settings", the extension having access to local data is WAI.

This leaves us with the active-tab case.  ActiveTab allows the extension to temporarily access the origin of a tab while that tab is open *after* the user explicitly invokes the extension on that tab.  The way this applies to file URLs is that it effectively grants the extension file permission if it is invoked on a file:// URL.  I think that's incorrect behavior, and should be fixed.

A note on severity: if my understanding is correct here, that means that for this exploit to work, the user needs to install a malicious extension and then explicitly invoke the extension on a file:// URL (or explicitly grant it file access, but again, I think that's WAI overall).  Given those restrictions, I'd be inclined to reduce this severity to Severity-Low.

kenrb@, thoughts?

93m4qau783@, let me know if any of the above differ from your experience - if I'm missing something, then the severity might stay at Medium (or increase - but hopefully not).

Onto the fix: I think the right thing to do here is to limit what activeTab grants when used on a file:// url.  I think it's reasonable that it would still apply to that specific URL (otherwise, activeTab becomes useless on file:// urls), but I think we should strictly limit it to that specific file.

Another oddity discovered here: the activeTab version of this appears to *only* reproduce if the extension does not request file:// access separately (through either the <all_urls> permission or by requesting file://*/*).  If the extension does that, and the setting is disabled in the chrome://extensions page, the activeTab permission doesn't appear to be sufficient to grant access.  I'm not quite sure why.  It also doesn't matter from a security perspective, since obviously an attacker could craft the extension however they like.

I probably won't have the bandwidth to look into this right away - Karan, is this something you can dive into?

### ka...@chromium.org (2018-03-12)

Will investigate.


### 93...@gmail.com (2018-03-12)

In order to exploit this bug, a malicious extension would have to be invoked (click on its icon) while viewing a file:/// URL. The example extension is only enough to demonstrate that the bug exists, but an extension with scripts and such could walk the entire filesystem, gather filename and directory information, map out the file system, and even read some types of files (see https://crbug.com/chromium/816685#c1). Once an extension has gathered all of this data, they could send it off to servers controlled by the attacker. I would be so frightened and stressed to find out that a malicious Chrome extension had spied on all of my files.

### 93...@gmail.com (2018-03-18)

Reminder: It has now been 20 days (1/3) of your available time.

### ka...@chromium.org (2018-03-20)

So activeTab is meant to grant access to the origin of the currently visible tab's url. For file scheme urls, at least as per https://url.spec.whatwg.org/#origin, the origin is implementation defined. 

In practice GURL::GetOrigin() returns file:/// as the origin of a file url instead of returning an opaque origin. cc'ing mkwst@ (who owns url/) to ensure that this is WAI.

A simple solution for us may be to just check if the url is a file url and only grant access to the particular url for active Tab.

Another thing I noticed: While granting access to the url's origin using activTab, we don't actually do any other checking. For e.g., we do end up granting access to chrome scheme hosts using activeTab. However, on a first look, I wasn't able to find a way to exploit that, since we do end up checking PermissionsData::IsRestrictedUrl for most of the uses (chrome.tabs.executeScript etc.)


### rd...@chromium.org (2018-03-20)

> A simple solution for us may be to just check if the url is a file url and only grant access to the particular url for active Tab.

I think this is probably what we should do.  The user granting the extension access to a specific file should be scoped to that file.

> While granting access to the url's origin using activTab, we don't actually do any other checking. For e.g., we do end up granting access to chrome scheme hosts using activeTab.

Yeah, this is another problem we should fix.  I think we should probably just do the IsRestrictedURL() check before granting activeTab (though it's somewhat orthogonal to this issue).

### ka...@chromium.org (2018-03-21)

So the code that allows extension frames to have file url iframes is that the file scheme is being whitelisted in Dispatcher::UpdateOriginPermissions (https://cs.chromium.org/chromium/src/extensions/renderer/dispatcher.cc?sq=package:chromium&dr&l=1245). I am not sure if it's possible to then only whitelist a particular file url in the extension renderer. 

Since the permission model in general is meant to depend on origins, it seems to me that we should gate the access in this case on whether the extension already has access to file urls. If the user has explicitly deselected allowing an extension to have access to file urls, giving the extension access through activeTab seems weird. Devlin WDYT?

### rd...@chromium.org (2018-03-21)

Hmm... I'd prefer to not break activeTab for these cases (at least in this fix), because it has (or should have) the same benefit for file URLs as everywhere else - you can let it run on a specific entity without granting it global access.  But if we can't find a better way, we can always have that as a backup option (and it's probably worth having a separate discussion about in either case).

What is the host passed to WebSecurityOrigin in this case, if we were to only add an URLPattern exactly matching the current file, and how does blink treat it?

### ka...@chromium.org (2018-03-21)

From https://en.wikipedia.org/wiki/File_URI_scheme,

A file URI takes the form of

file://host/path
where host is the fully qualified domain name of the system on which the path is accessible, and path is a hierarchical directory path of the form directory/directory/.../name. If host is omitted, it is taken to be "localhost", the machine from which the URL is being interpreted. Note that when omitting host, the slash is not omitted (while "file:///foo.txt" is valid, "file://foo.txt" is not, although some interpreters manage to handle the latter).

I think the only relevant case would be of local files. It seems we don't open links to remote files anyway - https://support.google.com/gsa/answer/2664790?hl=en. And in fact seems we never parse host for file urls - https://cs.chromium.org/chromium/src/extensions/common/url_pattern.cc?q=url_pattern.cc&sq=package:chromium&dr&l=247. Hence the parsed host in a URLPattern for a file url should always be empty.

Hence for any file url being whitelisted in Dispatcher::UpdateOriginPermissions (https://cs.chromium.org/chromium/src/extensions/renderer/dispatcher.cc?sq=package:chromium&dr&l=1245), the host should always be empty and all urls of the form file:///path would be whitelisted in the extension renderer.

Hence I thing we should gate the whitelisting on having the "Access to file urls" extension setting. 

>>Hmm... I'd prefer to not break activeTab for these cases (at least in this fix), because it has (or should have) the same benefit for file URLs as everywhere else

The special thing about file urls is that at least for local files, the host is empty, so the origin gives you access to all the local files. 
Thinking about this in another way, active tab is supposed to give you access to the origin of the requested url. It's legitimate to consider file urls as having an opaque origin, hence not actually granting any access for the general case.

Aside: Seems we'll need to make the same adjustment for Click to script code.

### el...@chromium.org (2018-03-21)

> It seems we don't open links to remote files anyway -https://support.google.com/gsa/answer/2664790?hl=en

I believe that's a bit misleading. We don't allow navigation to file URIs from http or https pages, but we do allow direct navigation in the omnibox, extension APIs, and from file://-sourced pages.

### 93...@gmail.com (2018-03-21)

Extension APIs should not be able to access local files without user consent.

### ka...@chromium.org (2018-03-21)

>> I believe that's a bit misleading. We don't allow navigation to file URIs from http or https pages, but we do allow direct navigation in the omnibox, extension APIs, and from file://-sourced pages.

Thanks for clarifying. The current code in URLPattern just ignores the case of remote hosts for file scheme though (which is probably another bug). 

Anyways still I think we should gate access through activeTab on having the "Access to local files" settings.

### 93...@gmail.com (2018-03-21)

How is the user informed that they are giving an extension permission to access local files?

### ka...@chromium.org (2018-03-21)

>> How is the user informed that they are giving an extension permission to access local files?

They'll have to manually enable it on the chrome://settings page for packed extensions. Unpacked extensions are granted this by default currently.


### rd...@chromium.org (2018-03-22)

> Thinking about this in another way, active tab is supposed to give you access to the origin of the requested url. It's legitimate to consider file urls as having an opaque origin, hence not actually granting any access for the general case.

ActiveTab grants access to the currently-active tab.  Currently, this is implemented in terms of origin, but is not defined to be so.  Do we have any rough estimate of how difficult it would be to allow blink to whitelist a specific file, rather than all files on a system?  If there's no reasonably simple way, we may need to restrict to having file access, but it's a bit of a shame.

### ka...@chromium.org (2018-03-22)

>> Do we have any rough estimate of how difficult it would be to allow blink to whitelist a specific file, rather than all files on a system?  If there's no reasonably simple way, we may need to restrict to having file access, but it's a bit of a shame.

Don't really have context into this code. cc'ing some owners.

jochen@/mkwst@/tzepez@: Is it possible to whitelist a particular URL in a renderer for cross-origin access? In other words, is there an analogous for AddOriginAccessWhitelistEntry (https://cs.chromium.org/chromium/src/third_party/WebKit/public/web/WebSecurityPolicy.h?q=WebSecurityPolicy&sq=package:chromium&dr=CSs&l=69). If not, does it make sense to introduce it?

### jo...@chromium.org (2018-03-22)

origin based checks can't deal with paths :/

### rd...@chromium.org (2018-03-22)

Hmm... looking at this more, maybe we're over-complicating it.  I don't think you can do an XHR or fetch() to a file:// URL, which means may not matter - the request will be blocked anyway.  The extension can still script the page, but we have more granularity there, and could only grant the specific file the user is on.

Am I missing something obvious - assuming we granted only the specific file as a scripting/explicit permission, is there actually any way the extension could read additional files on disk?

### ka...@chromium.org (2018-03-22)

>> I don't think you can do an XHR or fetch() to a file:// URL, which means may not matter - the request will be blocked anyway.

I was able to xhr a file url from an extension iframe with access to file:///. The logic which decides that is probably this - https://cs.chromium.org/chromium/src/third_party/WebKit/Source/platform/weborigin/SecurityOrigin.h?sq=package:chromium&dr=CSs&l=111

>>> The extension can still script the page, but we have more granularity there, and could only grant the specific file the user is on.

Currently tabs.executeScript depends on the extension having host permissions for the frame. We follow the invariant that host permissions refer to hosts currently. This would break that invariant.



### rd...@chromium.org (2018-03-22)

/sigh...

Okay, we gave it a good go.  Thank you very much for the thorough investigation, Karan!  Let's go ahead and just require file access, even with activeTab.

### ka...@chromium.org (2018-03-22)

Sounds good, will issue a patch.

### ka...@chromium.org (2018-03-23)

[Empty comment from Monorail migration]

### ka...@chromium.org (2018-03-27)

So I didn't consider that the test extension here was an unpacked extension (which is auto-granted file access)! This bug actually does not repro if the extension does not have file access. Hence it won't repro for a packed extension unless you were to explicitly grant file access to the extension.

I was able to verify that to xhr/embed a file url, an extension needs to have both:
- Access to file urls enabled. (This is auto-granted for unpacked extensions, this is enforced by the ChildProcessSecurityPolicy for the extension process in the browser).
- Have host permissions to the file url. (either through all_urls or active tab, this is only enforced in the renderer from what I can see.).

In light of this, I think this is not a security bug. What I found wrong was that even though the extension in this case had access to file urls enabled, we didn't showcase this on the extensions page (since it didn't explicitly request for file urls). This I think needs to be corrected.

### bu...@chromium.org (2018-04-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/58ef10883df7df7e5621e064c84061831ec32870

commit 58ef10883df7df7e5621e064c84061831ec32870
Author: Karan Bhatia <karandeepb@chromium.org>
Date: Mon Apr 02 23:10:56 2018

Extensions: Add more test coverage for extensions ability to xhr file urls.

This CL adds more test coverage for an extensions ability to xhr file urls
through an extension frame. To XHR a file url an extension should have "Allow
access to file URLs" setting enabled and also have host permissions to file:///.
Tests are also added for activeTab.

This also helps discover a bug with the network service implementation of the
same.

BUG=816685

Cq-Include-Trybots: master.tryserver.chromium.linux:linux_mojo
Change-Id: Ic53a1ad9c25a5db56c69eb421734f76ba9f95a1e
Reviewed-on: https://chromium-review.googlesource.com/985798
Reviewed-by: Devlin <rdevlin.cronin@chromium.org>
Commit-Queue: Karan Bhatia <karandeepb@chromium.org>
Cr-Commit-Position: refs/heads/master@{#547551}
[modify] https://crrev.com/58ef10883df7df7e5621e064c84061831ec32870/chrome/browser/extensions/active_tab_apitest.cc
[modify] https://crrev.com/58ef10883df7df7e5621e064c84061831ec32870/chrome/browser/extensions/cross_origin_xhr_apitest.cc
[add] https://crrev.com/58ef10883df7df7e5621e064c84061831ec32870/chrome/test/data/extensions/api_test/active_tab_file_urls/background.js
[add] https://crrev.com/58ef10883df7df7e5621e064c84061831ec32870/chrome/test/data/extensions/api_test/active_tab_file_urls/manifest.json
[rename] https://crrev.com/58ef10883df7df7e5621e064c84061831ec32870/chrome/test/data/extensions/api_test/cross_origin_xhr/file_access_all_urls/manifest.json
[rename] https://crrev.com/58ef10883df7df7e5621e064c84061831ec32870/chrome/test/data/extensions/api_test/cross_origin_xhr/file_access_all_urls/test.html
[rename] https://crrev.com/58ef10883df7df7e5621e064c84061831ec32870/chrome/test/data/extensions/api_test/cross_origin_xhr/file_access_all_urls/test.js
[add] https://crrev.com/58ef10883df7df7e5621e064c84061831ec32870/chrome/test/data/extensions/api_test/cross_origin_xhr/file_access_no_hosts/manifest.json
[add] https://crrev.com/58ef10883df7df7e5621e064c84061831ec32870/chrome/test/data/extensions/api_test/cross_origin_xhr/file_access_no_hosts/test.js
[rename] https://crrev.com/58ef10883df7df7e5621e064c84061831ec32870/chrome/test/data/extensions/api_test/cross_origin_xhr/no_file_access_all_urls/manifest.json
[rename] https://crrev.com/58ef10883df7df7e5621e064c84061831ec32870/chrome/test/data/extensions/api_test/cross_origin_xhr/no_file_access_all_urls/test.html
[rename] https://crrev.com/58ef10883df7df7e5621e064c84061831ec32870/chrome/test/data/extensions/api_test/cross_origin_xhr/no_file_access_all_urls/test.js
[modify] https://crrev.com/58ef10883df7df7e5621e064c84061831ec32870/testing/buildbot/filters/mojo.fyi.network_browser_tests.filter


### ka...@chromium.org (2018-04-03)

The CL in c#32 verifies that xhr to file urls behaves sensibly.

Adding to c#31, here is the current behavior of tabs.executeScript for file urls:
- With <all_urls> you can inject script using tabs.executeScript in a file frame only iff the extension has file access. This is WAI.
- With activeTab granted for a file url, you can inject script using tabs.executeScript on only that file url. (even if the extension doesn't have "Allow access to file urls" enabled). This can be hardened a bit more. We'll change this to also check for the "Allow access to file urls" permission.

### ka...@chromium.org (2018-04-04)

Also, in c#33, for the activeTab case, I meant "With activeTab granted for a file *tab*, you can inject script using tabs.executeScript on only that file *tab*."

### bu...@chromium.org (2018-04-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/7a33a5423fd1e6beab05c08cae24a6fc9dee2999

commit 7a33a5423fd1e6beab05c08cae24a6fc9dee2999
Author: Karan Bhatia <karandeepb@chromium.org>
Date: Thu Apr 05 00:41:12 2018

Extensions: Gate activeTab with file urls on having explicit file access.

When an extension is granted tab permission using activeTab (in response to say
clicking on its browser action), the extension is granted permission to the
tab's origin for the duration of the tab lifetime.

When this happens for a tab with a file url loaded, the extension gets
permission to the file scheme on the tab. This allows, for example, the
extension to read the contents of the page using apis like
chrome.tabs.executeScript. For file urls, this is not ideal since this does not
respect the "Allow access to file URLs" extension setting.

This CL changes this behavior, gating the access to the file scheme on the tab,
on the extension having explicit file access. This CL also adds extensive test
coverage for the behavior of tabs.executeScript on pages with file urls loaded
into them.

BUG=816685

Change-Id: I9175bb1883006fe594a93262c6825a962c285037
Reviewed-on: https://chromium-review.googlesource.com/994264
Commit-Queue: Karan Bhatia <karandeepb@chromium.org>
Reviewed-by: Devlin <rdevlin.cronin@chromium.org>
Cr-Commit-Position: refs/heads/master@{#548269}
[modify] https://crrev.com/7a33a5423fd1e6beab05c08cae24a6fc9dee2999/chrome/browser/extensions/active_tab_apitest.cc
[modify] https://crrev.com/7a33a5423fd1e6beab05c08cae24a6fc9dee2999/chrome/browser/extensions/active_tab_permission_granter.cc
[modify] https://crrev.com/7a33a5423fd1e6beab05c08cae24a6fc9dee2999/chrome/browser/extensions/execute_script_apitest.cc
[modify] https://crrev.com/7a33a5423fd1e6beab05c08cae24a6fc9dee2999/chrome/test/data/extensions/api_test/active_tab_file_urls/manifest.json
[add] https://crrev.com/7a33a5423fd1e6beab05c08cae24a6fc9dee2999/chrome/test/data/extensions/api_test/executescript/file_access/background.js
[add] https://crrev.com/7a33a5423fd1e6beab05c08cae24a6fc9dee2999/chrome/test/data/extensions/api_test/executescript/file_access/manifest.json


### 93...@gmail.com (2018-04-05)

As of revision 548269, the test extension is still able to read a local file while viewing a different file/folder, and the test extension shows up under chrome://extensions as having no special permissions. That said, I could be observing different behavior here as opposed to how it would behave with a non-developer-mode extension.

### ka...@chromium.org (2018-04-05)

As c#31 stated, this is just true for unpacked extensions which are granted file access permissions by default. Unpacked extensions are a developer feature, so don't think there are any security implications.

That said, we should ensure that we either show "Allow access to file URLs" for these extensions or don't grant file access to them by default.

### ka...@chromium.org (2018-04-05)

Does any one have any objections to changing this to Security-Impact-Low. The original report is mostly a non-issue from a security standpoint since it is only relevant for unpacked extensions. 

However, in further investigation we did realize that active tab wasn't respecting file access permission completely (see c#33). But that only granted access to the file scheme on a particular tab. That has now been fixed.

### ka...@chromium.org (2018-04-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-04-06)

[Empty comment from Monorail migration]

### 93...@gmail.com (2018-04-06)

If an extension has "Allow access to file URLs" permission, does that allow it to access files even when the user isn't viewing them?

What's your timeframe for adding clarification on chrome://extensions about developer mode extensions having access to file URLs?

### ka...@chromium.org (2018-04-07)

>> If an extension has "Allow access to file URLs" permission, does that allow it to access files even when the user isn't viewing them?

Presumably using xhr but it'd need explicit host permissions for the same in addition to the explicit "Allow access to file URLs". See CL in c#32.

>> What's your timeframe for adding clarification on chrome://extensions about developer mode extensions having access to file URLs?
Have filed https://crbug.com/chromium/830112 to track that.

### 93...@gmail.com (2018-04-14)

With https://crbug.com/chromium/830112 fixed, I retested this today:

- Unpacked extension shows under chrome://extensions as having access to file URLs (as is by default).
- On non-file URLs, the extension popup is always denied from accessing the requested file:/// URL.
- When access to file URLs is not granted, the extension popup is denied from accessing the requested file:/// URL, even when currently viewing a file:/// URL.
- When access to file URLs is granted, the extension popup is allowed to access the requested file:/// URL, even when currently viewing a different file:/// URL.

For the last one, is that working as intended? It seems that extensions shouldn't be able to read totally unrelated files.

Lastly, is there any additional work (besides what is described above) that is needed in order to fix this bug?

### bu...@chromium.org (2018-04-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/f020de9f4788d81c05f0a4947dabfdb777604cc6

commit f020de9f4788d81c05f0a4947dabfdb777604cc6
Author: Karan Bhatia <karandeepb@chromium.org>
Date: Tue Apr 17 06:36:26 2018

Extensions: Add test coverage for an extensions ability to embed file iframes.

This CL adds test coverage regarding an extension frame's ability to embed a
file frame. This ensures than an extension can only embed a file frame if it has
explicit file access and host permissions to the file scheme.

BUG=816685

Cq-Include-Trybots: master.tryserver.chromium.linux:linux_mojo
Change-Id: I8d167d9a8629ffece29d44bee4bd6db2ef988b02
Reviewed-on: https://chromium-review.googlesource.com/1003762
Commit-Queue: Karan Bhatia <karandeepb@chromium.org>
Reviewed-by: Devlin <rdevlin.cronin@chromium.org>
Cr-Commit-Position: refs/heads/master@{#551267}
[modify] https://crrev.com/f020de9f4788d81c05f0a4947dabfdb777604cc6/chrome/browser/extensions/active_tab_apitest.cc
[add] https://crrev.com/f020de9f4788d81c05f0a4947dabfdb777604cc6/chrome/browser/extensions/file_iframe_apitest.cc
[modify] https://crrev.com/f020de9f4788d81c05f0a4947dabfdb777604cc6/chrome/test/BUILD.gn
[add] https://crrev.com/f020de9f4788d81c05f0a4947dabfdb777604cc6/chrome/test/data/extensions/api_test/active_tab_file_urls/file_iframe.html
[add] https://crrev.com/f020de9f4788d81c05f0a4947dabfdb777604cc6/chrome/test/data/extensions/api_test/active_tab_file_urls/window_onload.js
[add] https://crrev.com/f020de9f4788d81c05f0a4947dabfdb777604cc6/chrome/test/data/extensions/file_iframe/background.html
[add] https://crrev.com/f020de9f4788d81c05f0a4947dabfdb777604cc6/chrome/test/data/extensions/file_iframe/window_onload.js


### ka...@chromium.org (2018-04-18)

>> - When access to file URLs is granted, the extension popup is allowed to access the requested file:/// URL, even when currently viewing a different file:/// URL.

>>For the last one, is that working as intended? It seems that extensions shouldn't be able to read totally unrelated files.

That's how active tab is supposed to work, it grants the extension access to the origin of the active tab. And the extension security model also depends on host permissions. Also, the user at this point has already checked a checkbox saying "Allow access to file URLs".

The bug should be fixed now, have added browser tests to sanity check the behavior with file urls.

### sh...@chromium.org (2018-04-18)

[Empty comment from Monorail migration]

### aw...@google.com (2018-04-23)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-27)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-04-27)

Thanks for the report and the follow ups 93m4qau783@, the VRP panel decided to award $500 - cheers! A member of our finance team will be in touch to arrange payment. Also, how would you like to be credited in Chrome release notes?

### aw...@chromium.org (2018-04-27)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-05-29)

[Empty comment from Monorail migration]

### aw...@google.com (2018-07-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-25)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-08-28)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-01-04)

[Empty comment from Monorail migration]

### na...@google.com (2020-01-27)

please claim your reward by 1/31/2020. Otherwise it will be donated to charity. 

### na...@google.com (2020-02-04)

Processing this as a donation. 

### is...@google.com (2020-02-04)

This issue was migrated from crbug.com/chromium/816685?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40090610)*
