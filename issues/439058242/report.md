# Extensions can run JS on any privileged origin by exploiting already-patched vulnerabilities under devtools:// scheme.

| Field | Value |
|-------|-------|
| **Issue ID** | [439058242](https://issues.chromium.org/issues/439058242) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>DevTools>Extensions |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | le...@gmail.com |
| **Assignee** | da...@google.com |
| **Created** | 2025-08-16 |
| **Bounty** | $4,000.00 |

## Description

# VULNERABILITY DETAILS

The **devtools://** scheme allows loading of remote assets from the domain <https://chrome-devtools-frontend.appspot.com/>. This server keeps a history of old versions of the DevTools Frontend, which can be loaded by navigating any tab to the URL "**devtools://devtools/remote/serve\_file/@<commit\_hash>/<filename>**".

When loaded this way, these assets are **fully-privileged**, with access to the *DevToolsAPI* object. Because these are old versions, **they contain many vulnerabilities that have already been patched**, effectively allowing the exploitation of such vulnerabilities **even in the latest Chrome version**.

# EXPLANATION

An extension can open a new tab and browse to a **devtools://** URL that loads an old version of the DevTools frontend from the remote server, then exploit any old vulnerability to achieve code execution under the DevTools page. This allows a malicious extension to obtain access to the *DevToolsAPI* object, which can do many privileged operations, such as **accessing local files, impersonating other extensions (even privileged ones), and performing universal XSS**. All of this can be done **with no user interaction, other than just installing the malicious extension**.

In addition to that, the extension can also setup "*Console Pins*", by writing to **localStorage** when running code under the old DevTools Frontend. These Console Pins will then execute in **ANY** privileged origin, allowing a full sandbox escape, as soon as the user opens the real DevTools console. It's not needed to open the console in a privileged page, **just by opening console anywhere**, the extension can navigate the inspected tab to a privileged page, making the Console Pin execute there.

Another way to escape sandbox, is by using DevTools to impersonate a highly-privileged extension such as *Perfetto UI*, **which can control the entire browser** (its id is hardcoded in chromium sources). This is demonstrated in the attached "PoC 2". If Perfetto UI is already installed, no user interaction is required, if not, we use the **webstorePrivate** API to show an extension install prompt (**we can even change name and icon, to make it look like our own extension**). If the user accepts the prompt, Perfetto UI will be installed, and we will impersonate it.

# VERSION

Chrome Version: 139.0.7258.128 stable

Operating System: Tested on Windows 11, should work on all operating systems.

# REPRODUCTION CASE

In this PoC, we are reusing the vulnerability described in <https://issues.chromium.org/issues/40051844>. This vulnerability has been patched long ago, but because we are loading an old DevTools frontend, we can reuse it.

## Steps to reproduce:

1. Download the attached "PoC 1.zip" file and install it as an unpacked extension
2. As soon as the extension is installed, it will open a new window with the url **devtools://devtools/remote/serve\_file/@e22de67c28798d98833a7137c0e22876237fc40a/inspector.html**.
3. After a few seconds, the extension will write the contents of the **C:\** directory to the body of the DevTools page, demonstrating that it achieved local file access through the **DevToolsAPI** object. No user interaction is required up to this step.
4. The extension will also setup a Console Pin, and wait for DevTools to be opened. As soon as you press **F12** in any page, that page will be navigated to **chrome://inspect**, and the Console Pin will execute there.
5. The script injected in **chrome://inspect** will open the Node Frontend, then it will open a DevTools console to inspect the Node Frontend. This will cause the Console Pin to be injected in the Node Frontend too.
6. Since the Node Frontend is attached to the browser target, the injected script has **full control over the browser**. The script will download **calc.exe** and use the **chrome://downloads** page to execute it.
7. At the end of the process, the extension will remove the console pin and uninstall itself, to avoid an infinite loop, and to not interefere with PoC #2.

The second PoC demonstrates the usage of the **webstorePrivate** API, to spoof a WebStore prompt, tricking the user into installing the *Perfetto UI* extension, despite the name and icon in the prompt being completely different. This uses the same vulnerability as above, but it is much stealthier: **No UI is displayed to the user, other than a minimized DevTools window that exists briefly when the extension is loaded**. It also performs a full sandbox escape, downloading and executing calc.exe in the end.

## Steps to reproduce:

1. Download and install "PoC 2.zip" as an unpacked extension.
2. A minimized, barely perceptible, DevTools window, will appear in the taskbar for some seconds, and then close itself.
3. After that, open a new tab and paste an URL of the **Chrome Web Store**, for ANY extension (ex. <https://chromewebstore.google.com/detail/framesexplorer/imijdbpfemdegalijeojlkhiamfcgklp>). After the page is fully loaded, click on the install button, and accept the prompt.
4. As soon as the installation of your chosen extension is finished, you will see an alert in the WebStore page saying "**Failed to install <extension>, please try again**". The alert shows "**Web Store extension**" as the origin.
5. After accepting the alert, you will see a second install prompt, **that looks exactly like the prompt you just accepted** (same name and icon). This would lead a user to believe that the installation "failed", and the browser is "trying again". But in reality, this second prompt, if accepted, will install the **Perfetto UI** extension.
6. As soon as Perfetto UI is installed, the extension will open another minimized DevTools window, to **impersonate the Perfetto UI extension, and take control of the browser**. After a few seconds, calc.exe will be downloaded and launched.

# CREDIT INFORMATION

Reporter credit: Leandro Teles (<https://x.com/leandrotp2>, <https://www.linkedin.com/in/leandro-teles-212014197/>)

## Attachments

- [PoC1.zip](attachments/PoC1.zip) (application/zip, 3.5 KB)
- [PoC2.zip](attachments/PoC2.zip) (application/zip, 9.1 KB)
- [background.js](attachments/background.js) (text/javascript, 466 B)
- [devtools.js](attachments/devtools.js) (text/javascript, 2.6 KB)
- [devtools-page.html](attachments/devtools-page.html) (text/html, 159 B)
- [devtools-page.js](attachments/devtools-page.js) (text/javascript, 2.9 KB)
- [manifest.json](attachments/manifest.json) (application/json, 262 B)
- [background.js](attachments/background.js) (text/javascript, 988 B)
- [devtools.js](attachments/devtools.js) (text/javascript, 1.8 KB)
- [devtools-page.html](attachments/devtools-page.html) (text/html, 159 B)
- [devtools-page.js](attachments/devtools-page.js) (text/javascript, 4.3 KB)
- [manifest.json](attachments/manifest.json) (application/json, 498 B)
- [offscreen.html](attachments/offscreen.html) (text/html, 176 B)
- [offscreen.js](attachments/offscreen.js) (text/javascript, 2.4 KB)
- [pdf-script.js](attachments/pdf-script.js) (text/javascript, 2.7 KB)
- [perfetto-script.js](attachments/perfetto-script.js) (text/javascript, 2.2 KB)
- [webstore-script.js](attachments/webstore-script.js) (text/javascript, 2.8 KB)

## Timeline

### am...@chromium.org (2025-08-16)

Hello, thanks for the report. Please unpack the POC compressed files and upload each file directly to report so we can investigate the extension components.

### le...@gmail.com (2025-08-16)

Here are the unpacked files for PoC1.zip

### le...@gmail.com (2025-08-16)

Here are the unpacked files for PoC2.zip

### pe...@google.com (2025-08-16)

Thank you for providing more feedback. Adding the requester to the CC list.

### me...@google.com (2025-08-18)

Thanks for the report.

Devlin, could you please take a look?

### me...@google.com (2025-08-19)

Tentatively assigning severity=high. The extension in poc1 doesn't require devtools permission but it can read local disk without having "Allow file access" enabled.

### ch...@google.com (2025-08-19)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2025-08-19)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ch...@google.com (2025-09-02)

rdevlin.cronin: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### rd...@chromium.org (2025-09-04)

This seems pretty scary.  dsv@, this seems like something that should be fixed on the devtools side -- we shouldn't allow retrieving known-bad versions of devtools scripts in modern versions of Chrome.  Is this something you can look at?

### ch...@google.com (2025-09-19)

danilsomsikov: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### da...@google.com (2025-09-22)

We need to serve these versions for backwards compatibility. However, I don't think we should allow `chrome.windows.create({url: "devtools://devtools/remote/..."})`. We probably should not allow this for any devtools URL. Devlin, wdyt?

### rd...@chromium.org (2025-09-22)

Hmm... I like the idea of restricting devtools window creation (we should do that regardless, I think -- opening devtools should be a user action, or, maybe, a separate API in the devtools or debugger API surfaces). That said, I'm also curious, do we need to serve these to *all chrome versions*? It seems like we could refuse to serve obsolete ones to non-obsolete Chromes? Otherwise, I do somewhat worry that this is going to turn into whack-a-mole (for instance, if the extension socially engineers the user to open devtools and then navigates to those sources via their panel, perhaps?).

### da...@google.com (2025-09-23)

This is needed for remote debugging of an older Chrome from a newer one.

### le...@gmail.com (2025-09-23)

Good morning! I have just noticed that this issue has been marked as a duplicate of another one, but that one is more recent than this, so shouldn't that issue be marked as a duplicate of this instead?

Also, is it possible to grant me access to see the other issue?

### da...@google.com (2025-09-23)

Sorry, I a wrong issue

### dx...@google.com (2025-09-25)

Project: chromium/src  

Branch:  main  

Author:  Maksim Sadym [sadym@chromium.org](mailto:sadym@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6973949>

Allow hidden targets only with enabled remote debugging

---


Expand for full commit details
```
     
    Do not allow for creating hidden targets if remote debugging was not 
    turned on. 
     
    Bug: 439058242 
    Change-Id: I9779d2243065507f8c94d2d0863f968031fe45b6 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6973949 
    Reviewed-by: Danil Somsikov <dsv@chromium.org> 
    Reviewed-by: Peter Kvitek <kvitekp@chromium.org> 
    Commit-Queue: Maksim Sadym <sadym@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1520456}

```

---

Files:

- M `content/browser/devtools/protocol/target_handler.cc`

---

Hash: [49293c82de9615d3232d673dcd3aa7ea573ca1f2](https://chromiumdash.appspot.com/commit/49293c82de9615d3232d673dcd3aa7ea573ca1f2)  

Date: Thu Sep 25 09:15:23 2025


---

### da...@google.com (2025-09-25)

If we agree on the solution, who do I need to talk to about forbidding DevTools URLs in `chrome.windows.create`?

### rd...@chromium.org (2025-10-10)

We can theoretically block that type of navigation. In fact, we already do [unless the extension has the debugger or devtools permissions](https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/extensions/extension_tab_util.cc;l=1352-1363;drc=62a9a00176f862e688fa47919ed6f19b59f77b5f). That was added in response to [issue 40051448](https://issues.chromium.org/issues/40051448).

We can remove the relaxation and prevent these navigations all the time, but that *might* break existing extensions. I'd like @ol...@chromium.org 's opinion on that, but I've uploaded a CL for it [here](https://chromium-review.googlesource.com/c/chromium/src/+/7030016).

Separately, I'd still like to revisit this:

> That said, I'm also curious, do we need to serve these to all chrome versions? It seems like we could refuse to serve obsolete ones to non-obsolete Chromes?

That would solve this problem holistically, and also just seems like a generally good idea : ) (If I'm on an up-to-date version of Chrome, I'd like my devtools to be [guaranteed to be] up-to-date, too!)

### ya...@google.com (2025-10-13)

> If I'm on an up-to-date version of Chrome, I'd like my devtools to be [guaranteed to be] up-to-date, too!

The context for this is that if you are remote debugging an older version of Chrome, e.g. on an Android device, the debugger (devtools frontend) and the debug target (the outdated Chrome on Android) need to have the same expectations on the protocol (CDP). This is the easiest to achieve by having their versions match.

### le...@gmail.com (2025-10-13)

> We can theoretically block that type of navigation. In fact, we already do unless the extension has the debugger or devtools permissions.

I would like to point out that blocking it in the Tabs API might not be enough, if the extension has the Debugger permission, it can also perform navigation using the "Page.navigate" CDP method, instead of the Tabs API.

> We can remove the relaxation and prevent these navigations all the time, but that might break existing extensions.

Maybe you don't need to block *all* navigations to **devtools://** scheme, only navigations to **devtools://remote/** urls. And if any extension is currently doing such a thing, then it really should stop working.

> If I'm on an up-to-date version of Chrome, I'd like my devtools to be [guaranteed to be] up-to-date, too!

If the older Frontend versions are only used for Remote Debugging, then they should be loaded via **https://** protocol instead of **devtools://** protocol, such that they don't have access to the privileged APIs. Because in this case, the connection is done via WebSockets, so the frontend doesn't need any special privilege.

If that gets implemented, then you could completely forbid ALL navigations to **devtools://remote/** urls, no matter where they came from. Maybe you could even remove the ability to load remote assets completely.

### dx...@google.com (2025-10-13)

Project: chromium/src  

Branch:  main  

Author:  Devlin Cronin [rdevlin.cronin@chromium.org](mailto:rdevlin.cronin@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7030016>

[Extensions] Block devtools window / tab creation from extension APIs

---


Expand for full commit details
```
     
    We currently have a carve-out that allows extensions with the devtools 
    or debugger permissions to create a devtools window. Even with these 
    permissions, this is something we'd prefer be left up to the user to 
    initiate. Don't allow these navigations. 
     
    Bug: 439058242 
    Change-Id: I402d52ffbbd6f8537df92d12a3211ca70ff7ae3c 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7030016 
    Commit-Queue: Devlin Cronin <rdevlin.cronin@chromium.org> 
    Reviewed-by: Oliver Dunk <oliverdunk@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1529133}

```

---

Files:

- M `chrome/browser/extensions/extension_tab_util.cc`
- M `chrome/browser/extensions/extension_tab_util.h`
- M `chrome/browser/extensions/extension_tab_util_unittest.cc`

---

Hash: [2f952b7796483626f16d5995221b4dca8c3680c2](https://chromiumdash.appspot.com/commit/2f952b7796483626f16d5995221b4dca8c3680c2)  

Date: Mon Oct 13 21:12:00 2025


---

### ch...@google.com (2025-10-18)

We commit ourselves to a 60 day deadline for fixing for s1 severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

### th...@chromium.org (2025-10-22)

[secondary shepherd] rdevlin.cronin@: If this issue is resolved, could you please mark it as fixed? If not, could you please summarize what is unresolved?

### ch...@google.com (2025-10-25)

rdevlin.cronin: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### an...@chromium.org (2025-10-28)

[secondary shepherd] rdevlin.cronin@: Could you comment on whether this issue is resolved? Is there any further action pending? Thanks!

### tj...@chromium.org (2025-10-29)

In terms of the immediate issue, this was largely resolved with the CL in [comment #23](https://issues.chromium.org/issues/439058242#comment23). We ended up just going with blocking all extension devtools:// scheme navigations regardless of permissions.

I would say it's still an open question if we also want to block this on the Debugger triggered "Page.navigate" CDP method, what are your opinions on that
yangguo@?

### ya...@google.com (2025-10-30)

I can't think of a good use case of Page.navigate to a devtools:// URL. @ds...@google.com, wdyt? Should we blocklist that scheme in the implementation of Page.navigate?

### da...@google.com (2025-10-30)

Yes, I will take care of this.

### ch...@google.com (2025-11-14)

danilsomsikov: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### dx...@google.com (2025-11-17)

Project: chromium/src  

Branch:  main  

Author:  Danil Somsikov [dsv@chromium.org](mailto:dsv@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7146578>

Disallow navigation to `devtools://` URLs from untrusted DevTools clients.

---


Expand for full commit details

```Disallow navigation to `devtools://` URLs from untrusted DevTools clients.

```
This change extends the check in `PageHandler::Navigate` to prevent untrusted DevTools clients from navigating to URLs with the `devtools://` scheme, similar to how `chrome-untrusted://` URLs are handled. 
 
It is fine to remove the test, as navigation from a safe origin to devtools:// should not longer be possible anyway 
 
Bug: 439058242 
Change-Id: I08a0e838d14392a9e2a414e83ca791024738ff12 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7146578 
Reviewed-by: Yang Guo <yangguo@chromium.org> 
Commit-Queue: Danil Somsikov <dsv@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1545748}

```
```

---

Files:
* M       `chrome/browser/devtools/devtools_browsertest.cc`
* M       `chrome/test/data/extensions/api_test/debugger_navigate_subframe/background.js`
* M       `content/browser/devtools/protocol/page_handler.cc`

---

Hash: [37b8d0b6055ae54af66d2ca6a354c42e59a2593e](https://chromiumdash.appspot.com/commit/37b8d0b6055ae54af66d2ca6a354c42e59a2593e)\
Date: Mon Nov 17 09:12:00 2025

</details>

---

```

### ch...@google.com (2025-11-17)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### ch...@google.com (2025-11-19)

Security Merge Request Consideration: Requesting merge to stable (M142) because latest trunk commit (1545748) appears to be after stable branch point (1522585).
Security Merge Request Consideration: Requesting merge to beta (M143) because latest trunk commit (1545748) appears to be after beta branch point (1536371).
Security Merge Request - Manual Review: Merge review required: M142 is already shipping to stable.

Security Merge Request - Manual Review: Merge review required: M143 has already been cut for stable release.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [142, 143].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### ya...@chromium.org (2025-11-24)

danilsomsikov@ Please take a look at the merge questionnaire if the fix needs merging. Thanks!

### da...@google.com (2025-11-24)

> Which CLs should be backmerged? (Please include Gerrit links.)

<https://chromium-review.googlesource.com/7030016>
<https://chromium-review.googlesource.com/7146578>

> Has this fix been verified on Canary to not pose any stability regressions?

Yes

> Does this fix pose any potential non-verifiable stability risks?

No

> Does this fix pose any known compatibility risks?

No

> Does it require manual verification by the test team? If so, please describe required testing.

See the bug description

### ch...@google.com (2025-12-01)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### sr...@google.com (2025-12-02)

can you please help complete the merges for 142 asap so they can be included in next week respin

### aj...@google.com (2025-12-03)

Adjusting to Medium severity as this has several preconditions.

### ch...@google.com (2025-12-05)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### sp...@google.com (2025-12-08)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $4000.00 for this report.

Rationale for this decision:
Moderate Impact Web Platform Privilege Escalation with a High Quality with Functional Exploit


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### le...@gmail.com (2025-12-09)

Appeal reward reason: Hello, Google VRP Team! I would like to thank you for your work on this vulnerability, and for this reward!

I have reported this vulnerability about 4 months ago, and since then, it was classified as S1 severity (High). But I just noticed that, a few days before the reward amount was defined, it was demoted to S2 severity (Medium), because of the required preconditions.

I would like to point out that there aren't really a lot of preconditions: In fact, because of how DevTools was designed, any extension that achieves Code Execution under the devtools:// origin, will yield the same result:

- Local File Access + UXSS + scripting other extensions, with NO precondition, other than just having the extension installed.
- Sandbox escaping, as soon as the user presses F12 on any unprivileged page, OR, if they have Perfetto UI installed.

In other words, the first part of the impact has no precondition at all, and for the sandbox escape, the only precondition is to open DevTools on any unprivileged page.

There have been other vulnerabilities reported in the past, with the same preconditions (installing an extension + opening DevTools), such as [crbug.com/341875171](https://crbug.com/341875171), [crbug.com/341136300](https://crbug.com/341136300), [crbug.com/338248595](https://crbug.com/338248595), and [crbug.com/40052870](https://crbug.com/40052870), and they have all been classified as S1 severity.

The report also includes a second PoC that can run scripts on the WebStore page, without the precondition of opening DevTools. It displays a spoofed WebStore prompt (arbirary name and icon), which, if accepted, will install the Perfetto UI Extension, which can be used to escape sandbox with no user interaction.

On top of that, I believe I was also able to help the team with fixing the vulnerability, by pointing that navigations should also be restricted in the "Page.navigate" CDP method. Had I not pointed that out, the originally proposed fix would be insufficient.

Once again, I want to thank you for your attention to this issue! I hope you can take this into consideration. Have a good day!

### dx...@google.com (2025-12-15)

Project: chromium/src  

Branch:  refs/branch-heads/7444  

Author:  Danil Somsikov [dsv@chromium.org](mailto:dsv@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7260514>

[M142] Disallow navigation to `devtools://` URLs from untrusted DevTools clients.

---


Expand for full commit details

```[M142] Disallow navigation to `devtools://` URLs from untrusted DevTools clients.

```
This change extends the check in `PageHandler::Navigate` to prevent untrusted DevTools clients from navigating to URLs with the `devtools://` scheme, similar to how `chrome-untrusted://` URLs are handled. 
 
It is fine to remove the test, as navigation from a safe origin to devtools:// should not longer be possible anyway 
 
(cherry picked from commit 37b8d0b6055ae54af66d2ca6a354c42e59a2593e) 
 
Bug: 439058242 
Change-Id: I08a0e838d14392a9e2a414e83ca791024738ff12 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7146578 
Reviewed-by: Yang Guo <yangguo@chromium.org> 
Commit-Queue: Danil Somsikov <dsv@chromium.org> 
Cr-Original-Commit-Position: refs/heads/main@{#1545748} 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7260514 
Auto-Submit: Danil Somsikov <dsv@chromium.org> 
Cr-Commit-Position: refs/branch-heads/7444@{#4063} 
Cr-Branched-From: 29907d3c18078029695f458b42fb8e6fda3e493d-refs/heads/main@{#1522585}

```
```

---

Files:
* M       `chrome/browser/devtools/devtools_browsertest.cc`
* M       `chrome/test/data/extensions/api_test/debugger_navigate_subframe/background.js`
* M       `content/browser/devtools/protocol/page_handler.cc`

---

Hash: [3c2982192b2cce48ca2e404ef5dcc92373357e75](https://chromiumdash.appspot.com/commit/3c2982192b2cce48ca2e404ef5dcc92373357e75)\
Date: Mon Dec 15 08:57:06 2025

</details>

---

```

### pe...@google.com (2025-12-15)

LTS Milestone M138

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### dx...@google.com (2025-12-15)

Project: chromium/src  

Branch:  refs/branch-heads/7499  

Author:  Danil Somsikov [dsv@chromium.org](mailto:dsv@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7260534>

[M143] Disallow navigation to `devtools://` URLs from untrusted DevTools clients.

---


Expand for full commit details

```[M143] Disallow navigation to `devtools://` URLs from untrusted DevTools clients.

```
This change extends the check in `PageHandler::Navigate` to prevent untrusted DevTools clients from navigating to URLs with the `devtools://` scheme, similar to how `chrome-untrusted://` URLs are handled. 
 
It is fine to remove the test, as navigation from a safe origin to devtools:// should not longer be possible anyway 
 
(cherry picked from commit 37b8d0b6055ae54af66d2ca6a354c42e59a2593e) 
 
Bug: 439058242 
Change-Id: I08a0e838d14392a9e2a414e83ca791024738ff12 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7146578 
Reviewed-by: Yang Guo <yangguo@chromium.org> 
Commit-Queue: Danil Somsikov <dsv@chromium.org> 
Cr-Original-Commit-Position: refs/heads/main@{#1545748} 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7260534 
Commit-Queue: Yang Guo <yangguo@chromium.org> 
Auto-Submit: Danil Somsikov <dsv@chromium.org> 
Cr-Commit-Position: refs/branch-heads/7499@{#3292} 
Cr-Branched-From: b30439823e5177773584139e72e0593e36863899-refs/heads/main@{#1536371}

```
```

---

Files:
* M       `chrome/browser/devtools/devtools_browsertest.cc`
* M       `chrome/test/data/extensions/api_test/debugger_navigate_subframe/background.js`
* M       `content/browser/devtools/protocol/page_handler.cc`

---

Hash: [82e5a4a183ca6b2b589fcbffff6604c560633285](https://chromiumdash.appspot.com/commit/82e5a4a183ca6b2b589fcbffff6604c560633285)\
Date: Mon Dec 15 10:09:36 2025

</details>

---

```

### pe...@google.com (2025-12-16)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### rz...@google.com (2025-12-16)

1. <https://crrev.com/c/7262411>
2. Low, no conflicts
3. 142, 143
4. Yes

### dx...@google.com (2025-12-18)

Project: chromium/src  

Branch:  refs/branch-heads/7204  

Author:  Danil Somsikov [dsv@chromium.org](mailto:dsv@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7262411>

[M138-LTS] Disallow navigation to `devtools://` URLs from untrusted DevTools clients.

---


Expand for full commit details

```[M138-LTS] Disallow navigation to `devtools://` URLs from untrusted DevTools clients.

```
This change extends the check in `PageHandler::Navigate` to prevent untrusted DevTools clients from navigating to URLs with the `devtools://` scheme, similar to how `chrome-untrusted://` URLs are handled. 
 
It is fine to remove the test, as navigation from a safe origin to devtools:// should not longer be possible anyway 
 
(cherry picked from commit 37b8d0b6055ae54af66d2ca6a354c42e59a2593e) 
 
Bug: 439058242 
Change-Id: I08a0e838d14392a9e2a414e83ca791024738ff12 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7146578 
Commit-Queue: Danil Somsikov <dsv@chromium.org> 
Cr-Original-Commit-Position: refs/heads/main@{#1545748} 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7262411 
Reviewed-by: Alex Rudenko <alexrudenko@chromium.org> 
Reviewed-by: Yang Guo <yangguo@chromium.org> 
Commit-Queue: Roger Felipe Zanoni da Silva (xWF) <rzanoni@google.com> 
Cr-Commit-Position: refs/branch-heads/7204@{#3466} 
Cr-Branched-From: d5de512dc9dc8ddfe4e6d71b0637578bb6158683-refs/heads/main@{#1465706}

```
```

---

Files:
* M       `chrome/browser/devtools/devtools_browsertest.cc`
* M       `chrome/test/data/extensions/api_test/debugger_navigate_subframe/background.js`
* M       `content/browser/devtools/protocol/page_handler.cc`

---

Hash: [acf717a4a879d97da3d95e9df1ca99924777fe76](https://chromiumdash.appspot.com/commit/acf717a4a879d97da3d95e9df1ca99924777fe76)\
Date: Thu Dec 18 19:54:43 2025

</details>

---

```

### da...@google.com (2026-01-08)

@rd...@chromium.org as you expected in the [comment #20](https://issues.chromium.org/issues/439058242#comment20) remove the relaxation did break existing extensions ([b/470115241](https://issues.chromium.org/issues/470115241)).

I still consider devtools:// URL scheme an implementation detail and would like to offer a dedicated `chrome.devtools` or `chrome.debugger` extension API to open devtools for a target. In fact, we've recently added a CDP method for that (`Target.openDevTools`), which would work in `chrome.debugger` if allow-listed.

Devlin, wdyt?

### le...@gmail.com (2026-01-08)

> In fact, we've recently added a CDP method for that (Target.openDevTools), which would work in chrome.debugger if allow-listed.

This wouldn't work for NiM's use case, since they are opening a remote connection, there's no "targetId" to be used in the "Target.openDevTools" method. They have to specify the websocket endpoint as an URL parameter.

However, as I said in [comment #22](https://issues.chromium.org/issues/439058242#comment22), one possibility is to restrict only navigations to **devtools://remote/** URLs, instead of restricting the whole **devtools://** scheme. That would fix the vulnerability, while still allowing use cases like this.

### ch...@google.com (2026-02-24)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> Moderate Impact Web Platform Privilege Escalation with a High Quality with Functional Exploit

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/439058242)*
