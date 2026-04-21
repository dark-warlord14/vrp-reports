# Extensions on lens.google.com can bypass host permissions and open chrome-untrusted:// URLs with side panel

| Field | Value |
|-------|-------|
| **Issue ID** | [40067231](https://issues.chromium.org/issues/40067231) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Sandbox>SiteIsolation, Platform>Extensions, UI>Browser>TopChrome>SidePanel |
| **Platforms** | Windows, ChromeOS |
| **Reporter** | ma...@gmail.com |
| **Assignee** | na...@chromium.org |
| **Created** | 2023-07-11 |
| **Bounty** | $3,000.00 |

## Description

**Steps to reproduce the problem:**

1. Download the attached extension
2. Right click an image in chrome and click "search google for image"
3. The current tab is redirected to chrome-untrusted://terminal

**Problem Description:**  

While the steps described above do require user interaction, the chrome.sidePanel API is pending changes that could open the Side Panel on *any tab* (this is significant later). This means that once these changes are added, the exploit chain could be ran without user interaction. However, I was too impatient to wait for that to happen, so I'm just reporting now.

This bug works by running a content script on lens.google.com, which is loaded internally inside the side panel. The page is loaded *inside* of another, privileged, page: chrome-untrusted://companion-side-panel.top-chrome

The chrome-untrusted URL and lens.google.com communicate via postMessage. One of the types of messages that can be passed is {type:10}, which opens a new browser tab [1] with the mojo function openUrlInBrowser [2].

One of the issues is that there is no validation of this URL.

The following (normally blocked) can be opened:

- chrome-untrusted:// pages like crosh and terminal
- chrome://restart and other debug URLs

The code for the entire exploit is just to make a lens.google.com/\* content script containing the following:

```
top.postMessage({  
    type: 10,  
    urlToOpen: "chrome-untrusted://terminal"  
}, '\*')  

```

Another notable thing is that the urlToOpen can be set to a javascript: URL. These redirects behave with the same functionality as bookmarklets, meaning they don't affect chrome:// pages or similar, but they can be used on normal http/https tabs (which the extension does *not* have to declare host permissions for) and run scripts on these domains. TL;DR: you can bypass host permissions completely. In fact, the extension below has no permissions declared except content scripts on lens.google.com.

---

1: <https://source.chromium.org/chromium/chromium/src/+/main:out/Debug/gen/chrome/browser/companion/core/mojom/companion.mojom.h;drc=db895c06b9a4fed6800f67f1b9354ff97d27eceb;l=216>

2: <https://source.chromium.org/chromium/chromium/src/+/main:out/Debug/gen/chrome/browser/companion/core/mojom/companion.mojom.h;drc=db895c06b9a4fed6800f67f1b9354ff97d27eceb;l=216>

**Additional Comments:**

\*\*Chrome version: \*\* 117.0.0.0 \*\*Channel: \*\* Stable

**OS:** Chrome OS

## Attachments

- [bad_lens_redirect_poc.zip](attachments/bad_lens_redirect_poc.zip) (application/octet-stream, 566 B)
- [read_file_without_permission_poc.zip](attachments/read_file_without_permission_poc.zip) (application/octet-stream, 653 B)
- [all_lens_pocs.mp4](attachments/all_lens_pocs.mp4) (video/mp4, 4.6 MB)
- [lens_webstore_vid.mp4](attachments/lens_webstore_vid.mp4) (video/mp4, 764.8 KB)
- [lens_webstore_access.zip](attachments/lens_webstore_access.zip) (application/octet-stream, 1.0 KB)
- [Unnamed screencast (2).webm](attachments/Unnamed screencast (2).webm) (video/webm, 4.9 MB)
- [Screenshot 2023-07-27 15.40.10.png](attachments/Screenshot 2023-07-27 15.40.10.png) (image/png, 166.8 KB)
- [Screen recording 2023-07-27 16.51.45.webm](attachments/Screen recording 2023-07-27 16.51.45.webm) (video/webm, 2.3 MB)
- [Capture.PNG](attachments/Capture.PNG) (image/png, 399.2 KB)

## Timeline

### [Deleted User] (2023-07-11)

[Empty comment from Monorail migration]

### ma...@gmail.com (2023-07-11)

Okay, I think I was wrong about the way sidePanel works. It looks like it'll need user interaction no matter what.

### ma...@gmail.com (2023-07-11)

I believe the "javascript url" part of the bug should also allow functions to locally access files without having the permission to do so.

### ma...@gmail.com (2023-07-11)

Yep, here's a quick POC that can read /var/log without having permission to do anything except run content scripts on lens.google.com. More specifically, it can execute code on the file page, and from there, the contents of files can be sent to the extension. Only tested on ChromeOS

### ma...@gmail.com (2023-07-12)

And here's a video of everything covered in this report.

Note that the sidebar does not have to be opened by right-clicking an image; right-clicking text and pressing "search on google" works just as well.

### ma...@gmail.com (2023-07-12)

Just realized I forgot that the javascript://* trick could also be used to gain access to the Chrome Web Store, getting chrome.management (and chrome.dashboardPrivate) permissions without declaring them. Well, that makes 4 pretty major side effects of one tiny bug.

### ma...@gmail.com (2023-07-12)

[Empty comment from Monorail migration]

### ma...@gmail.com (2023-07-12)

For whoever has to read this, sorry about the avalanche of comments. To recap, there are four major bugs here:

- It's possible to completely bypass host permissions
- It's possible to scripts on the web store and thus disable other extensions without having the permission to do so
- It's possible to access local files even with the switch in the extension settings disabled
- It's possible to open chrome-untrusted:// urls like Cros VMs and debug urls (like chrome://restart) which extensions normally cannot do

That should be all.
Reporter credit: Derin Eryilmaz

### ma...@gmail.com (2023-07-12)

[Comment Deleted]

### da...@chromium.org (2023-07-12)

The root cause IIUC is that lens.google.com is opened in Chrome sidebar, with a javacscript channel to a chrome-untrusted:// frame.

That chrome-untrusted:// receives messages from the lens.google.com frame and does not validate them, allowing the lens.google.com frame to control chrome-untrusted://, and a content script for lens.google.com will also run in the sidebar not just on tabs that load lens.google.com (a likely user expectation).

So I think there's 2 things here from my POV:

1. Content scripts affecting sidebar (Is this intentional? should the sidebar be a different url?)

2. The lens.google.com untrusted frame not validating inputs from the sidebar page, and opening URLs on chrome-untrusted:// scheme or JS bookmarklets to allow JS injection into chrome-untrusted://

I don't think we have formalized the idea that your subframes can be attack vectors into a chrome-untrusted:// frame.

Injecting JS into chrome-untrusted:// would be high severity, but needing to install an extension lowers to medium.

[Monorail components: Internals>Sandbox>SiteIsolation Platform>Extensions UI>Browser>TopChrome>SidePanel]

### st...@google.com (2023-07-12)

[Empty comment from Monorail migration]

### tj...@chromium.org (2023-07-12)

[Empty comment from Monorail migration]

### ma...@gmail.com (2023-07-12)

The only way to inject js with this bug is with the javascript: protocol. So you can't actually inject js on chrome-untrusted, but you can do it on chrome.google.com and files, which are normally both inaccessible. As well as using it for a host permissions bypass.

### da...@chromium.org (2023-07-12)

As this requires a lens sidebar, I think this is ChromeOS only right now? I can't repro to determine if this affects 114 stable. I will mark it as FoundIn-114 but if it's not affecting 114, please update that.

### da...@chromium.org (2023-07-12)

Got it, thanks for clarifying.

### [Deleted User] (2023-07-12)

[Empty comment from Monorail migration]

### ma...@gmail.com (2023-07-12)

@14 I was able to reproduce on windows 115 and ChromeOS 117 but not 114 on either.

### ad...@google.com (2023-07-12)

(I am a bot: this is an auto-cc on a security bug)

### or...@google.com (2023-07-13)

[Empty comment from Monorail migration]

### or...@chromium.org (2023-07-13)

#10, this was one of the disadvantages mentioned in the chrome-untrusted:// design doc about using postMessage[1]. We never got around to formulating a proper process for this since Mojo covered the majority of the use cases :(

ChromeOS built an ipc::Message-like library[2] on top of postMessage. I can't find the bug or doc but I tried to get the message_types.js[3] files for WebUIs to be covered by IPC reviewers but couldn't follow through.

[1] https://docs.google.com/document/d/1CBFhitvxfk2EhXYormfDMQF5vesbfpwOKHYevUvdwk8/edit#heading=h.zqmkwih5czu
[2] https://source.chromium.org/chromium/chromium/src/+/main:ash/webui/system_apps/public/js/message_pipe.js
[3] https://source.chromium.org/chromium/chromium/src/+/main:ash/webui/media_app_ui/resources/js/message_types.js

### ch...@google.com (2023-07-13)

This seems not only a ChromeOS issue (see https://crbug.com/chromium/1464020#c17). Will add OS:Windows as well

### [Deleted User] (2023-07-13)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-07-17)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### st...@google.com (2023-07-24)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-26)

apalanki: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### me...@google.com (2023-07-26)

Our team is working on this right now. 

### me...@google.com (2023-07-27)

The extensions don't seem to reproducing the issue for my on Canary version 117.0.5912.0 (Official Build) canary (arm64). I included a video of me trying.

Can someone provide extra repro steps? I want to be able to reproduce the issue so we can verify the fix locally.

### me...@google.com (2023-07-27)

The also don't seem to work on my developer build Linux version 117.0.5913.0 (Developer Build) unknown (64-bit) 

### ma...@gmail.com (2023-07-27)

@28

Hm, does chrome-untrusted://companion-side-panel.top-chrome load for you on that version? And have you tried other versions?

### me...@google.com (2023-07-27)

Yes chrome-untrusted://companion-side-panel.top-chrome is loaded in the side panel in the video. I've tried two different 117 versions. I need it to work with my local build so I can verify the fix before submitting the fix. My local build is Linux version 117.0.5913.0.

### ma...@gmail.com (2023-07-27)

@30

I was just able to repro the bug on 116.0.5845.46 beta on ChromeOS. Could there be a chance that it only works for CrOS? Has anybody gotten it to work on Linux?

### me...@google.com (2023-07-27)

It didn't work for me on Mac Beta 116.0.5845.50 (Official Build) beta (arm64). I think issue should be persistent on all browsers, so is it possible the extensions only work on ChromeOS? Is there another way to verify the issue without using the extensions?

### ma...@gmail.com (2023-07-27)

I will try the exploit on Linux myself and get back to you :)

### ma...@gmail.com (2023-07-27)

@32 it looks like maybe the chrome-untrusted:// URL isnt getting loaded at all? But it was getting loaded on ChromeOS on the same version and even earlier.

### ma...@gmail.com (2023-07-27)

I think it only works on versions where the lens sidebar is labeled as "Search" instead of "Google Lens". 

### me...@google.com (2023-07-27)

You need to enable Search Companion by setting chrome://flags#csc to Enabled.

### ma...@gmail.com (2023-07-27)

@36 thanks,
and somehow the exploit did work for me on the latest Chrome beta on Linux. Video attached.

I was also to get it on Windows 116 with no flags a while ago, but I don't have a video of it.



### me...@google.com (2023-07-31)

[Empty comment from Monorail migration]

### me...@google.com (2023-08-02)

@mathia.is.fun@gmail.com Thanks for all your help! I was able to repro without the extensions but just copying the script into console. I have submitted a fix so if you wouldn't mind verifying the fix on the latest Canary that would be greatly appreciated.

### ma...@gmail.com (2023-08-02)

@mercerd@google.com

Although I'm not sure exactly what the fix was, it looks good to me.

a) The content script doesn't run (this might just be the same issue you had)
b) Only http and https URLs load from the OpenUrlInBrowser command now

### [Deleted User] (2023-08-03)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-03)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-08-07)

Hello mercerd@ -- thanks for fixing this issue. Can you please update this report with a gerrit link to the CL that resolves this issue. This is important for security merge review as well as other security-related processes. 

### me...@google.com (2023-08-07)

Yes sorry! This was fixed in https://chromium-review.googlesource.com/c/chromium/src/+/4728263

### aj...@chromium.org (2023-08-09)

I wonder if there is a larger issue here that should also be fixed - extensions should not be able to inject content scripts into pages in the side panel in the first place - the side panel should be showing trustworthy google content like other webui surfaces.

Reopening and assigning to nasko@ for their thoughts.


### aj...@chromium.org (2023-08-09)

(reopening!)

### ma...@gmail.com (2023-08-09)

I mean, I don't think extensions can inject into any side panel page, only lens.google.com and other http URLs. Still I agree that it could make for a fairly convincing phishing exploit, or access some sensitive things like in the bug here.

### [Deleted User] (2023-08-10)

nasko: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rd...@chromium.org (2023-08-15)

@ajgo:
> I wonder if there is a larger issue here that should also be fixed - extensions should not be able to inject content scripts into pages in the side panel in the first place - the side panel should be showing trustworthy google content like other webui surfaces.

On the whole, I consider extensions being able to inject into _http[s]_ pages in the side panel to be working as intended and a potentially important feature (indeed, when we were first developing the side panel utility for use with google search, it was deliberate that we *did* allow extensions to inject into hosted content).  For sensitive extensions (such as tracking blockers, accessibility extensions, etc), injecting into those sites is valid.  Additionally, I think network requests made from those sites are visible / modifiable by extensions using the webRequest and declarativeNetRequest APIs, and trying to prevent this would require including the location in which the frame is hosted in the request data, which seems undesirable.

In general, I think that any surface that is hosting web content needs to assume that web content can be manipulated by extensions (or by any number of other mechanisms, for that matter, e.g. proxies).  If a surface needs a secure and isolated environment for a built-in experience in Chrome, it should be hosted on a chrome:- or chrome-untrusted:-scheme.

### [Deleted User] (2023-08-16)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-11)

[Empty comment from Monorail migration]

### ma...@gmail.com (2023-10-16)

Hi, is any work being done on this? Why isn't it marked as Fixed?

### me...@google.com (2023-10-16)

Remarking as fixed. Based on https://crbug.com/chromium/1464020#c49 (https://bugs.chromium.org/p/chromium/issues/detail?id=1464020#c49), it seems as though the current implementation is WAI.



### am...@google.com (2023-10-18)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-10-18)

Congratulations Derin! The Chrome VRP Panel has decided to award you $3,000 for this report. Thank you for your efforts and reporting this issue to us -- nice work!

### ma...@gmail.com (2023-10-18)

Thanks!

### am...@google.com (2023-10-23)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-22)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2024-01-22)

This issue was migrated from crbug.com/chromium/1464020?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Internals>Sandbox>SiteIsolation, Platform>Extensions, UI>Browser>TopChrome>SidePanel]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40067231)*
