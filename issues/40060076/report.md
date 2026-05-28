# Prevent server redirect to non web accessible resource

| Field | Value |
|-------|-------|
| **Issue ID** | [40060076](https://issues.chromium.org/issues/40060076) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>Extensions, UI>Browser>Omnibox |
| **Platforms** | Linux, Windows, ChromeOS |
| **Reporter** | nd...@protonmail.com |
| **Assignee** | so...@chromium.org |
| **Created** | 2022-06-26 |
| **Bounty** | $1,000.00 |

## Description

**Steps to reproduce the problem:**  

chrome.window.create({url: 'chrome-extension://nkoccljplnhpfnfiajclkommnmllphnl/html/crosh.html?command=vmshell&args[]='})

**Problem Description:**  

The URL parameters args[] and command on chrome-extension://nkoccljplnhpfnfiajclkommnmllphnl/html/crosh.html  

Are used in chrome.terminalPrivate.openTerminalProcess or chrome.terminalPrivate.openVmshellProcess

<https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/extensions/api/terminal/terminal_private_api.cc>

This allows an extension to trigger crosh and run vmshell with arguments.  

Interestingly if you type a url in the omnibox a https:// resource is allowed to redirect to crosh. its treated as sec-fetch-site none not sure if its meant to be cross-origin.

Unrelated but I noticed ChromeOS leaks if files and folders exist to guest users file:///etc/passwd and file:///etc/ says ERROR\_ACCESS\_DENIED while file:///etc/foo says ERROR\_FILE\_NOT\_FOUND

I understand if this is a non-issue.

**Additional Comments:**

\*\*Chrome version: \*\* 103.0.0.0 \*\*Channel: \*\* Not sure

**OS:** Windows

## Attachments

- [extensionbug.mp4](attachments/extensionbug.mp4) (video/mp4, 395.2 KB)

## Timeline

### [Deleted User] (2022-06-26)

[Empty comment from Monorail migration]

### nd...@protonmail.com (2022-06-26)

Please ignore the OS:Windows

### nd...@protonmail.com (2022-06-26)

Regarding the allowed chrome-extension:// navigation on canary it seems possible to get it working with just a page window.location = "http://localhost:8000/foo" it says INVALID Response and then on the retry it works.

I know my demo code is bad.

from http.server import BaseHTTPRequestHandler, HTTPServer

sessions = set()

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if (self.path not in sessions):
            self.send_response(200)
            self.send_header("Cache-Control", "no-store")
            message = "<invalid>"
            self.wfile.write(bytes(message, "utf8"))
            self.end_headers()
            sessions.add(self.path)
        else:
            self.send_response(307)
            self.send_header('Cache-Control', 'no-store')
            self.send_header('location','chrome-extension://ghbmnnjooekpmoecnnnilnnbdlolhkhi/_generated_background_page.html')
            self.end_headers()
            sessions.remove(self.path)

with HTTPServer(('', 8000), handler) as server:
    server.serve_forever()

### aj...@google.com (2022-06-27)

[Empty comment from Monorail migration]

### aj...@google.com (2022-06-27)

Hi - could you provide the manifest & source from your example extension?

### nd...@protonmail.com (2022-06-28)

chrome-extension://nkoccljplnhpfnfiajclkommnmllphnl/html/crosh.html is an extension thats part of chromeos.
Per https://crbug.com/chromium/1339639#c3 it looks like any website can do it not just extensions however I will provide an example of an extension that does chrome.window.create({url: 'chrome-extension://nkoccljplnhpfnfiajclkommnmllphnl/html/crosh.html?command=vmshell&args[]='}) anyway no permissions would be needed for this.

### nd...@protonmail.com (2022-06-28)

manifest.json
{
  "name": "poc",
  "version": "1.0",
  "manifest_version": 3,
  "background": {
    "service_worker": "background.js"
  }
}

background.js
chrome.windows.create({url: 'chrome-extension://nkoccljplnhpfnfiajclkommnmllphnl/html/crosh.html?command=vmshell&args[]='})

### nd...@protonmail.com (2022-06-28)

It looks like this is sometimes used from chrome-untrusted:// https://bugs.chromium.org/p/chromium/issues/detail?id=1269151
You can change the command if you want it to start crosh.

### al...@google.com (2022-06-28)

+vapier since this affects the shell. At first glance this looks unintended, but I wouldn't be surprised if this is being used as a "feature".

This is high severity IMO and is particularly bad on devices with dev mode enabled.

[Monorail components: Platform>Apps>Default>Hterm UI>Browser>Omnibox]

### al...@google.com (2022-06-28)

[Empty comment from Monorail migration]

### al...@google.com (2022-06-28)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-28)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### al...@google.com (2022-06-28)

Assigning to myself until we have reproduced the issue and figured out the scope.

### va...@chromium.org (2022-06-28)

it's questionable whether an extension should be allowed to open any other chrome-extension:// URI that isn't web accessible.  that should probably get run by the browser team.

i wonder if chrome-untrusted:// works too since that's what Terminal uses.

### va...@chromium.org (2022-06-28)

wrt file:// sniffing, i don't really see too much of a problem there.  it probably assists as a side-channel user fingerprinting.  i'll note that this behavior isn't specific to CrOS though ... fairly certain it works the same on all OS's.

### al...@google.com (2022-06-28)

I cannot reproduce this issue with crosh. I set up a barebones python http server and set the redirect to:
'chrome-extension://nkoccljplnhpfnfiajclkommnmllphnl/html/crosh.html?command=vmshell&args[]=-h'

The tab that displays says:
"""
nkoccljplnhpfnfiajclkommnmllphnl is blocked
This page has been blcoked by Chrome
ERR_BLOCKED_BY_CLIENT
"""

If however, I change the extension to a non-system extension it works:
    self.send_header('location', 'chrome-extension://mkaakpdehdafacodkgkpghoibnmamcme/main.html')
Opens the Google draw extension.

My gut feeling is extensions need something akin to "Access-Control-Allow-Origin"

### al...@google.com (2022-06-28)

[Empty comment from Monorail migration]

[Monorail components: -Platform>Apps>Default>Hterm Platform>Extensions]

### nd...@protonmail.com (2022-06-29)

If you type a url in the omnibox a https:// resource is allowed to redirect to crosh.
https://crbug.com/chromium/1339639#c3 seems to be a bypass for using window.location by first sending an invalid response and letting it automatically reload the chrome-extension:// page however I have only tested that on canary.

That said chrome.windows.create({url: 'chrome-extension://nkoccljplnhpfnfiajclkommnmllphnl/html/crosh.html?command=vmshell&args[]='}) from a different browser extension seems to be like https://crbug.com/chromium/1269151 and thats still high

### al...@google.com (2022-06-29)

Addressing this seems to be one of the goals of the extension manifest V3:
https://developer.chrome.com/docs/extensions/mv3/intro/mv3-migration/#web-accessible-resources

### va...@chromium.org (2022-06-29)

iiuc, mv3 doesn't change anything here.  we don't have /html/crosh.html listed in web_accessible_resources today.

we can restrict vmshell in Secure Shell's crosh.html, but that's kind of meaningless if chrome-untrusted:// still works.

### nd...@protonmail.com (2022-06-29)

Its probably due to this exception https://source.chromium.org/chromium/chromium/src/+/main:extensions/browser/url_request_util.cc;drc=125be956a044059166dd7c2cadedb45fb349b66e;l=87


### nd...@protonmail.com (2022-06-29)

I think its from https://bugs.chromium.org/p/chromium/issues/detail?id=633963
Hopefully this can be prevented in manifest v3

### al...@google.com (2022-06-29)

I still cannot reproduce this for crosh with https and with the sessions logic added.

### [Deleted User] (2022-06-29)

[Empty comment from Monorail migration]

### nd...@protonmail.com (2022-06-29)

The session logic wont work on stable its a change coming in canary.
Does the extension from https://crbug.com/chromium/1339639#c3 work?

This works in chromeos 83 trying to get a newer version to test with.
https://terjanq.me/xss.php?h[location]=chrome-extension://nkoccljplnhpfnfiajclkommnmllphnl/html/crosh.html?command=vmshell&args[]=

### al...@google.com (2022-06-29)

I will test again with top-of-tree

### al...@google.com (2022-06-29)

[Empty comment from Monorail migration]

### al...@google.com (2022-06-29)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-29)

[Empty comment from Monorail migration]

### nd...@protonmail.com (2022-06-29)

...Now its working in the windows 10 chrome stable.
Have an extension that contains a text file thats not listed in web_assemble_resources and the python server is able to go to it.

If chrome.windows.create still works in the latest version of chromeos then thats a chromeos bug otherwise the extension part seems a general extension bug.


### nd...@protonmail.com (2022-06-29)

[Empty comment from Monorail migration]

### al...@google.com (2022-06-30)

[Empty comment from Monorail migration]

### al...@google.com (2022-06-30)

So one reason I ran into issues repro-ing this is extensions are disabled in guest mode on ChromeOS. I can repro this for the ssh extension which has the following in its manifest:

  "web_accessible_resources": [ "html/nassh.html", "html/nassh_google_relay.html" ]

The path I was able to access is:

chrome-extension://iodihamcpbpeioajjeobimgagajmlibd/html/nassh_preferences_editor.html

crosh isn't reachable on ChromeOS as far as I can tell because it uses a chrome-untrusted:// URL which gets blocked, and unless there is an alternative path that works the severity isn't as bad on ChromeOS as it first looked. This needs to be handed of to Chrome security.

### al...@google.com (2022-06-30)

One thing to note is the session code isn't needed, just the redirect code.

### al...@google.com (2022-06-30)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-30)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-06-30)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ca...@chromium.org (2022-06-30)

solomonkinard: Can you help further triage this? Feel free to reassign as appropriate, thanks.

### nd...@protonmail.com (2022-06-30)

Out of interest are you able to access
chrome-extension://iodihamcpbpeioajjeobimgagajmlibd/html/crosh.html

### nd...@protonmail.com (2022-06-30)

Thats for https://crbug.com/chromium/1339639#c33 as the secure shell extension does have the terminalPrivate permission.
https://robwu.nl/crxviewer/?crx=https%3A%2F%2Fchrome.google.com%2Fwebstore%2Fdetail%2Fsecure-shell%2Fiodihamcpbpeioajjeobimgagajmlibd

### nd...@protonmail.com (2022-06-30)

For https://crbug.com/chromium/1339639#c34 the session logic is needed for a website to do the navigation however the omnibox only needs a normal redirect.

### al...@google.com (2022-06-30)

In reference to https://crbug.com/chromium/1339639#c39. The ssh extension based path to crosh.html works.

### al...@google.com (2022-06-30)

I filed a sub bug because it looks like vmshell works through the URI when it doesn't work through crosh (i.e. if crostini is not enabled.)

### al...@google.com (2022-06-30)

https://crbug.com/chromium/1339639#c42. I tested with LaCros enabled and it doesn't work because crosh is owned by ASH and the ssh extension is only enabled for LaCros.

### nd...@protonmail.com (2022-06-30)

For title are extensions allowed to navigate to nkoccljplnhpfnfiajclkommnmllphnl even when not in guest mode?
I ask because it allows running vmshell with arguments and autorun VMs are not allowed.

### va...@chromium.org (2022-06-30)

manual navigation through omnibox is expected.  i don't see a problem with that.  it would be annoying if it didn't work.

being able to navigate to non-web_accessible URIs from either a website redirect or via another extension doing chrome.window.create is not expected imo.

nkoccljplnhpfnfiajclkommnmllphnl is the builtin crosh extension.  it's not installed from CWS.  we've been moving that to chrome-untrusted:// via the Terminal app, but i don't think we turned down fully yet.

### nd...@protonmail.com (2022-06-30)

Yeah manual navigation is fine.
The terminalPrivate API should contain the needed checks.

Being able to navigate to non-web_accessible URIs from a website seems bad as they have access to (maybe internal) APIs and it allows for extension fingerprinting that manifest v3 use_dynamic_url is meant to prevent (https://crbug.com/chromium/1208614)

### nd...@protonmail.com (2022-07-01)

Would extension and website navigation's to the ssh extension https://chrome.google.com/webstore/detail/secure-shell/iodihamcpbpeioajjeobimgagajmlibd?hl=en need to be prevented? since that has the same access to vmshell as nkoccljplnhpfnfiajclkommnmllphnl and probably wont get moved to chrome-untrusted://

### nd...@protonmail.com (2022-07-01)

[Comment Deleted]

### so...@chromium.org (2022-07-01)

> crbug.com/1339639#c38

Sure, I can read through this for the purpose of triage. Thanks.

### nd...@protonmail.com (2022-07-01)

[Comment Deleted]

### so...@chromium.org (2022-07-01)

I'm setting up a ChromeOS environment for the purpose of reproduction and debugging. I plan to continue working on this bug today. I'm out next week in case I don't have a fix today, but can resume investigation the following week. If that's okay, great. That should be fine for m105 stable. If this can't wait, maybe someone on on Crosh can take a look. Can this wait, or should we add someone such as joelhockey@ to investigate this next week? Thanks.

### al...@google.com (2022-07-02)

You don't need a ChromeOS environment to reproduce the issue. You just need a valid extension path and a webserver with the redirect logic like in https://crbug.com/chromium/1339639#c3.

### nd...@protonmail.com (2022-07-02)

Both the web_accessible (https://crbug.com/chromium/1339639#c3) and chrome-untrusted (https://crbug.com/chromium/1339639#c49) navigation bypass don't need ChromeOS.
https://crbug.com/chromium/1339639#c45 and https://crbug.com/chromium/1339639#c48 is about extensions (or websites) being able to run vmshell with arguments which seems to allow for autorunning VMs but that would need the latest chromeos version to test it.

### va...@chromium.org (2022-07-04)

[Empty comment from Monorail migration]

### jo...@chromium.org (2022-07-05)

I've tested a little now, and I see that the ability to redirect to an extension came in M86.  I used bisect-builds.py and bisected to:
https://chromium.googlesource.com/chromium/src/+log/95f84e2e1dcee8f71749f08415d063cfd226cbb4..5aa75779614994e0ced5776e7a5254f663e6bd2f

tools/bisect-builds.py --use-local-cache -a chromeos -g 791931 -b 791973 -c '%p --user-data-dir=/tmp/bisect-builds' --verify-range

I installed Secure Shell extension and ran python code with:
self.send_header('location','chrome-extension://iodihamcpbpeioajjeobimgagajmlibd/html/crosh.html?command=vmshell')

I opened a browser and opened devtools (Ctrl+Shift+J) and typed:
window.location = 'http://localhost:8000'

I might have more time tomorrow to bisect further and find the exact commit.

None of those commit descriptions really stood out to me.

### nd...@protonmail.com (2022-07-05)

I dont think this is the cause of extension or omnibox redirects but the python code abused the auto-reload of error pages.
And there is a change for that https://chromium.googlesource.com/chromium/src/+/4408a0fab85c8a2d4aafe3ede4a42524109dbb15

### jo...@chromium.org (2022-07-05)

+rockot, +mmenke, +avi, +nasko, +carlosil from change referenced in https://crbug.com/chromium/1339639#c56 and https://crbug.com/chromium/1339639#c57.

### mm...@chromium.org (2022-07-06)

If we don't trust URL A to navigate to URL B, surely if URL B is reloaded (by the user or automatically), the load should also fail.  Seems to me the issue is with committing a URL that we block a navigation to, for security reasons.  We should probably commit an top-level error URL instead, if we're blocking the navigation.

### al...@google.com (2022-07-06)

Changing the URL to an error URL to avoid accidental exposure sounds like it would work to me. However, I believe you should still give the user some visibility into what happened. Maybe a more info dropdown with information about the origin and destination of the redirect. This would be helpful for developers troublehshooting issues and users who want to report bad behavior from domains.

### nd...@protonmail.com (2022-07-06)

I think it should match open('chrome-extension://mamaljcbdcbgcpeifmkkioafgjaccdii')

mamaljcbdcbgcpeifmkkioafgjaccdii is blocked.
ERR_BLOCKED_BY_CLIENT

Currently does not show the initiator of the navigation but might be a nice feature. 

### nd...@protonmail.com (2022-07-06)

To prevent extension fingerprinting could ERR_BLOCKED_BY_CLIENT on chrome-extension:// detach the opener?

### mm...@chromium.org (2022-07-06)

We already support things like chrome://network-error/-20 (Which produces an ERR_BLOCKED_BY_CLIENT error page).  While I don't think we want to use a Chrome URL for this, since chrome URL to chrome URL navigations are potentially privileged, could imagine something like that, but with an additional query param.  Those pages do, admittedly, work by creating a URLLoader and having it fail with the specified error code, so plumbing error information down to the error page might be a bit complicated, or require the error page rendering code to recognize the network error scheme directly.

### nd...@protonmail.com (2022-07-06)

[Comment Deleted]

### nd...@protonmail.com (2022-07-07)

In https://crbug.com/chromium/1339639#c46 it says "another extension doing chrome.window.create is not expected" is it practice to prevent other extensions from navigating to non-web-accessible pages?

This would block https://crbug.com/chromium/1339639#c48 (if it is valid I dont think I got a response).

Removed https://crbug.com/chromium/1339639#c49 since it seems to be a separate issue.

### so...@chromium.org (2022-07-12)

I'm back today and working on reproducing this. Thanks.

### rd...@chromium.org (2022-07-12)

Re extensions opening pages to non-web-accessible-resources:  This is WAI, if it happens through the tabs or windows APIs.  The tabs and windows APIs are allowed to open more than the window.open() API allows, including chrome:-scheme and chrome-extension:-scheme pages.  This is intentional and is important for use cases like bookmark, session, window, and history managers.

However, we should likely *not* allow extensions to open windows to system-style apps (whether they're system web apps or extensions like crosh).  That seems like a bug.

Orthogonally, though, the fact that crosh uses the URL query params as source for input also seems scary.  It seems like this would be dangerous for cases like bookmarks (or whatever the equivalent ends up being for system web apps).

### al...@google.com (2022-07-12)

I noticed you didn't mention the HTTP location header in https://crbug.com/chromium/1339639#c67. Which API is that covered by? It should not have the same privileges as the tabs and windows APIs IIUC.

### nd...@protonmail.com (2022-07-12)

I dont think just a HTTP location header does allow going to chrome-extension:// without the bug from https://crbug.com/chromium/1339639#c3 or if initiated by the omnibox as then a redirect is allowed to go to chrome-extension:// could be intentional although it does require user interaction even if user does not know where there going.

I think the secure shell extension should not have vmshell url parameters and crosh should be on chrome-untrusted://

Browser extensions creating bookmarks with chrome-untrusted:// maybe a way to bypass the navigation rules but does need user interaction. Any way to go to chrome-untrusted:// without user interaction should be prevented. 

### va...@chromium.org (2022-07-13)

> Orthogonally, though, the fact that crosh uses the URL query params as source for input also seems scary.  It seems like this would be dangerous for cases like bookmarks (or whatever the equivalent ends up being for system web apps).

the entire point is to let people bookmark connections directly so they don't have to go through connection dialogs

i'm not really seeing a way to resolve the tension here

### nd...@protonmail.com (2022-07-13)

Yeah this is a very confusing report.

The problem of autoloading VMs can be fixed by preventing extensions from going to secure shell or crosh.
From what I can tell other then creating a token url parameter and not allowing it to leak to extensions I dont think it would be possible to prevent having the url parameters only stop them from being navigated to by extensions directly. 

html/nassh.html is in web_accessible_resources so there might be other ways to get commands from websites running.

Currently websites can abuse the bug in https://crbug.com/chromium/1339639#c3 so that would need to be fixed for secure shell to stay on chrome-extension://

### nd...@protonmail.com (2022-07-13)

If its just for bookmarks would it be possible to only allow navigation's from bookmarks and block other extensions from making bookmarks with that extension host?

Hope solomonkinard reproduced this issue.

### nd...@protonmail.com (2022-07-13)

[Comment Deleted]

### so...@chromium.org (2022-07-14)

Yes, I was able to reproduce the server side redirect to a non-web-accessible-resource from localhost. I think there are two main items discussed in this bug:

1) A URL can open vmshell/crosh.
2) A website can redirect to open vmshell/crosh/non-web-accessible-resource.

I think that the first item might be more of a feature than a bug (cc: vapier@).

The second item is a behavior that I can look into changing. That is, maybe we should prevent website redirections to Extension resources that aren't web accessible. For example, one cannot 307 redirect to chrome://settings.

### nd...@protonmail.com (2022-07-14)

1) builtin app is being moved to chrome-untrusted:// per https://crbug.com/chromium/1339639#c46 so the issue will only be for the secure shell extension.
There may be risks from allowing websites to embed or navigate to it like CSS injection (due to CSP), autoloading VMs, tricking the user into running commands but I dont have a chromebook to test anyway.

2) I think the redirects should be fixed not sure if Security_Severity-High is correct for this.

### so...@chromium.org (2022-07-18)

My current plan is to prevent redirection to a chrome-extension:// page if the destination is not a web accessible resource. That should handle 2) to close this bug, and 1) can be handled in a different bug.

### nd...@protonmail.com (2022-07-19)

Okay seems to be a good plan ideally the blocking should not be detectable. 

### nd...@protonmail.com (2022-07-19)

Moved 1) to https://bugs.chromium.org/p/chromium/issues/detail?id=1345685 not sure if going to be fixed but I can hope :)

### so...@chromium.org (2022-07-20)

I uploaded a CL for 2) that is a WIP while I work on its tests.

### nd...@protonmail.com (2022-07-20)

:) https://chromium-review.googlesource.com/q/topic:1339639
I would change the title to reflect that this is about websites not extensions but I dont think I can.

### so...@chromium.org (2022-07-21)

The bug title or CL's title, and either way, what do you want the new title to be? The CL is WIP (work in progress) due to existing and new tests.

### nd...@protonmail.com (2022-07-21)

The bug title, I think "Prevent server redirect to non web accessible resource" would work here as well since its no longer about crosh/vmshell.


### so...@chromium.org (2022-07-21)

[Empty comment from Monorail migration]

### so...@chromium.org (2022-07-26)

This bug should probably no longer be a release blocker. It has been split into different bugs so this bug is only tracking one specific thing. A CL exists tracking a fix, but a thread is awaiting response for the advisement of the best path forward.

### nd...@protonmail.com (2022-07-26)

I think high and medium are Pri-1 so it may get changed back.
Also this would need to match the blocking https://crbug.com/chromium/1341030 that I dont know much about.

If its no longer Severity-High then probably change that as well.

### so...@chromium.org (2022-07-26)

[Empty comment from Monorail migration]

### so...@chromium.org (2022-07-27)

https://crbug.com/chromium/1339639#c84 and https://crbug.com/chromium/1339639#c85 has context for the removal of the rbs label.

### [Deleted User] (2022-07-28)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### nd...@protonmail.com (2022-07-28)

Calm down sheriffbot its NA.

### nd...@protonmail.com (2022-07-28)

Its still a Severity-Medium regression since I dont think it used to work on stable.
Not sure what the rules are for it.

### [Deleted User] (2022-08-04)

[Empty comment from Monorail migration]

### pb...@google.com (2022-08-08)

[Bulk Edit] M105 is already promoted to Beta and we are just 2 weeks away from Stable RC cut this bug has been marked as Stable blocker, Please take a look asap. thank you.

### nd...@protonmail.com (2022-08-08)

Per https://crbug.com/chromium/1339639#c30 this is Security_Impact-Stable I dont think this needs to block the release as the bug has the same impact anyway.

### so...@chromium.org (2022-08-09)

This has been around for a while so it probably doesn't need to block stable. If anyone disagrees, feel free to restore the label.

### va...@chromium.org (2022-08-09)

i agree this isn't a release blocker since it's not (afaict) a regression

### [Deleted User] (2022-08-10)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### nd...@protonmail.com (2022-08-10)

Bot did you not noticed the comments from me, solomonkinard and vapier?
We dont think it needs to block stable since its already impacting stable.

### mm...@chromium.org (2022-08-10)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-08-10)

The bot is ignoring the removal because it believes this is a regression and release blocker. This is a good thing because it ensure release blockers are not missed. ReleaseBlock-NA is the correct label to add here, which mmenke@ has nicely done.

### mm...@chromium.org (2022-08-10)

Why is the bot assuming an issue not marked as a regression is an regression?  Bots shouldn't misrepresent available information, and assert that as truth.  :(

### nd...@protonmail.com (2022-08-10)

I think because its set as Security_Impact-Beta not Security_Impact-Stable
If someone removes the label multiple times they may mean it but its better to avoid a new security issue getting added to stable by mistake.

### [Deleted User] (2022-08-30)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-27)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-28)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-30)

[Empty comment from Monorail migration]

### ad...@chromium.org (2022-12-01)

[Empty comment from Monorail migration]

### so...@chromium.org (2022-12-14)

There's a CL up for this. Time needs to be allocated to address reviewer comments.

### [Deleted User] (2023-02-08)

[Empty comment from Monorail migration]

### nd...@protonmail.com (2023-03-22)

Look like this has not been worked on since last year :(
https://chromium-review.googlesource.com/c/chromium/src/+/3771104

### [Deleted User] (2023-04-05)

[Empty comment from Monorail migration]

### so...@chromium.org (2023-04-17)

It's in my queue. Maybe in a few weeks?

### so...@chromium.org (2023-05-09)

CL updated and awaiting review.

### so...@chromium.org (2023-05-12)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-31)

[Empty comment from Monorail migration]

### nd...@protonmail.com (2023-07-14)

I tried the code from https://crbug.com/chromium/1339639#c3 looks like open() no longer works you need to type the url directly in the address bar which gets redirected.

### am...@chromium.org (2023-07-21)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-16)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-11)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-06)

[Empty comment from Monorail migration]

### yu...@google.com (2024-01-06)

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

### [Deleted User] (2024-01-10)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-11)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-11)

This issue was migrated from crbug.com/chromium/1339639?no_tracker_redirect=1

[Multiple monorail components: Platform>Extensions, UI>Browser>Omnibox]
[Monorail blocked-on: crbug.com/chromium/1341030]
[Monorail mergedwith: crbug.com/chromium/1291984]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-02-21)

solomonkinard: Uh oh! This issue still open and hasn't been updated in the last 284 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### pe...@google.com (2024-03-07)

solomonkinard: Uh oh! This issue still open and hasn't been updated in the last 299 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### so...@chromium.org (2024-05-30)

Planning to revisit this as time allows.

### so...@chromium.org (2024-08-05)

Should this be P2? For example, I am already tracking P1s and P2s aren't likely to get resourced any time soon.

### nd...@protonmail.com (2024-08-06)

Based off <https://issues.chromium.org/issues/40060076#comment116> doing `window.open` with the code in <https://issues.chromium.org/issues/40060076#comment4> no longer works however:

- The PDF extension bookmarks still bypass WAR via redirects (Since it uses the extension API)
- A HTTP redirect from the URL bar still bypass WAR (Obfuscates an attack)

So there's a migration but in my biased option its still medium/P1 and given that this issue is from 2022 maybe it should be fixed quicker :)

### so...@chromium.org (2024-08-06)

Based on [#comment139](https://issues.chromium.org/issues/40060076#comment139), optimistically changing back to P1, but unfortunately I'm overloaded with other items including other P1s.

### nd...@protonmail.com (2024-08-06)

Well looking forward to this now P1 issue getting fixed in a couple more years :)

### so...@chromium.org (2024-08-12)

I created a [CL](https://crrev.com/c/3771104/comment/bdad68c3_dd5fe381) for this a while back. Most comments were addressed. However, based on that open comment, it looks like it would require a significant change to the navigation system.

### nd...@protonmail.com (2024-08-13)

Guessing its the "tag a navigation's redirect as being from an extension's webRequest listener rather than from a server", could also be useful information for <https://issues.chromium.org/40064165> and <https://issues.chromium.org/40064157> both abusing extension redirects.

### na...@chromium.org (2024-08-22)

Hey extensions folks, I'm very curious what "it looks like it would require a significant change to the navigation system." means. Can you give us some more details? I'm happy to also jump on a higher bandwidth discussion medium and see if I can help with unsticking this.

### so...@chromium.org (2024-08-29)

IIRC some progress was made in the CL but the work was ultimately put on hold for other work. Will schedule some time in a higher bandwidth discussion medium, which I assume you mean could be a quick meeting for the fastest wall clock time.

### ap...@google.com (2024-09-06)

Project: chromium/src
Branch: main

commit ee63f226247c1692ac85d488dfc49d592ef2707c
Author: Solomon Kinard <solomonkinard@chromium.org>
Date:   Fri Sep 06 22:04:09 2024

    Extensions: WAR: Metrics on resource redirect that's not web accessible
    
    This is for a server initiated redirect. Renderer initiated redirects
    don't appear to go through where this histogram boolean is set. Both MV3
    and MV2 are included.
    
    > Does this mean that opaque origins (like sandboxed frames) can still
    server-redirect to web-accessible resources?
    
    Opaque origins can be covered in a follow up CL if they're deemed worthy
    of being considered.
    
    Doc:
    https://docs.google.com/document/d/1ALcxHF2m85pqxEtJVQ_shHqzlIBpr3747ceSDuw7E_w
    
    Bug: chromium:40060076
    Change-Id: Ice6ec3ac5334546b88a6f8584a2aaaf89c3a2162
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5835905
    Reviewed-by: Justin Lulejian <jlulejian@chromium.org>
    Reviewed-by: Devlin Cronin <rdevlin.cronin@chromium.org>
    Commit-Queue: Solomon Kinard <solomonkinard@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1352326}

M       chrome/browser/extensions/web_accessible_resources_browsertest.cc
M       extensions/browser/extension_navigation_throttle.cc
M       tools/metrics/histograms/metadata/extensions/histograms.xml

https://chromium-review.googlesource.com/5835905


### ap...@google.com (2024-09-09)

Project: chromium/src
Branch: main

commit 77975359a075a36610b27c0f180e77eda1fb08ba
Author: Rasika Navarange <rasikan@google.com>
Date:   Mon Sep 09 11:45:04 2024

    Revert "Extensions: WAR: Metrics on resource redirect that's not web accessible"
    
    This reverts commit ee63f226247c1692ac85d488dfc49d592ef2707c.
    
    Reason for revert: This caused an official build failure see bug (chromium:365483228)
    
    Original change's description:
    > Extensions: WAR: Metrics on resource redirect that's not web accessible
    >
    > This is for a server initiated redirect. Renderer initiated redirects
    > don't appear to go through where this histogram boolean is set. Both MV3
    > and MV2 are included.
    >
    > > Does this mean that opaque origins (like sandboxed frames) can still
    > server-redirect to web-accessible resources?
    >
    > Opaque origins can be covered in a follow up CL if they're deemed worthy
    > of being considered.
    >
    > Doc:
    > https://docs.google.com/document/d/1ALcxHF2m85pqxEtJVQ_shHqzlIBpr3747ceSDuw7E_w
    >
    > Bug: chromium:40060076
    > Change-Id: Ice6ec3ac5334546b88a6f8584a2aaaf89c3a2162
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5835905
    > Reviewed-by: Justin Lulejian <jlulejian@chromium.org>
    > Reviewed-by: Devlin Cronin <rdevlin.cronin@chromium.org>
    > Commit-Queue: Solomon Kinard <solomonkinard@chromium.org>
    > Cr-Commit-Position: refs/heads/main@{#1352326}
    
    Bug: chromium:40060076
    Change-Id: Ifb8d10cf02dfff30b224f1a1f20b63dfede4a391
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5844889
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Owners-Override: Rasika Navarange <rasikan@google.com>
    Commit-Queue: Rasika Navarange <rasikan@google.com>
    Cr-Commit-Position: refs/heads/main@{#1352663}

M       chrome/browser/extensions/web_accessible_resources_browsertest.cc
M       extensions/browser/extension_navigation_throttle.cc
M       tools/metrics/histograms/metadata/extensions/histograms.xml

https://chromium-review.googlesource.com/5844889


### ap...@google.com (2024-09-09)

Project: chromium/src
Branch: refs/branch-heads/6707

commit 8d632e3f79d63bc6b1858934e5e85e18f0007b48
Author: Rasika Navarange <rasikan@google.com>
Date:   Mon Sep 09 12:07:11 2024

    Revert "Extensions: WAR: Metrics on resource redirect that's not web accessible"
    
    This reverts commit ee63f226247c1692ac85d488dfc49d592ef2707c.
    
    Reason for revert: This caused an official build failure see bug (chromium:365483228)
    
    Original change's description:
    > Extensions: WAR: Metrics on resource redirect that's not web accessible
    >
    > This is for a server initiated redirect. Renderer initiated redirects
    > don't appear to go through where this histogram boolean is set. Both MV3
    > and MV2 are included.
    >
    > > Does this mean that opaque origins (like sandboxed frames) can still
    > server-redirect to web-accessible resources?
    >
    > Opaque origins can be covered in a follow up CL if they're deemed worthy
    > of being considered.
    >
    > Doc:
    > https://docs.google.com/document/d/1ALcxHF2m85pqxEtJVQ_shHqzlIBpr3747ceSDuw7E_w
    >
    > Bug: chromium:40060076
    > Change-Id: Ice6ec3ac5334546b88a6f8584a2aaaf89c3a2162
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5835905
    > Reviewed-by: Justin Lulejian <jlulejian@chromium.org>
    > Reviewed-by: Devlin Cronin <rdevlin.cronin@chromium.org>
    > Commit-Queue: Solomon Kinard <solomonkinard@chromium.org>
    > Cr-Commit-Position: refs/heads/main@{#1352326}
    
    (cherry picked from commit 77975359a075a36610b27c0f180e77eda1fb08ba)
    
    Bug: chromium:40060076
    Change-Id: Ifb8d10cf02dfff30b224f1a1f20b63dfede4a391
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5844889
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Owners-Override: Rasika Navarange <rasikan@google.com>
    Commit-Queue: Rasika Navarange <rasikan@google.com>
    Cr-Original-Commit-Position: refs/heads/main@{#1352663}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5844792
    Owners-Override: Erhu Akpobaro <eakpobaro@google.com>
    Commit-Queue: Erhu Akpobaro <eakpobaro@google.com>
    Reviewed-by: Erhu Akpobaro <eakpobaro@google.com>
    Auto-Submit: Erhu Akpobaro <eakpobaro@google.com>
    Cr-Commit-Position: refs/branch-heads/6707@{#4}
    Cr-Branched-From: a17b2b968803fcbb915cafbfaacb31586fcf2e48-refs/heads/main@{#1352543}

M       chrome/browser/extensions/web_accessible_resources_browsertest.cc
M       extensions/browser/extension_navigation_throttle.cc
M       tools/metrics/histograms/metadata/extensions/histograms.xml

https://chromium-review.googlesource.com/5844792


### ap...@google.com (2024-09-09)

Project: chromium/src
Branch: main

commit 71047efbd7851b689d47cc8a196b0bc6192ed77a
Author: Solomon Kinard <solomonkinard@chromium.org>
Date:   Mon Sep 09 21:12:07 2024

    Extensions: WAR: Metrics on resource redirect that's not web accessible
    
    This is for a server initiated redirect. Renderer initiated redirects
    don't appear to go through where this histogram boolean is set. Both MV3
    and MV2 are included.
    
    > Does this mean that opaque origins (like sandboxed frames) can still
    server-redirect to web-accessible resources?
    
    Opaque origins can be covered in a follow up CL if they're deemed worthy
    of being considered.
    
    Doc:
    https://docs.google.com/document/d/1ALcxHF2m85pqxEtJVQ_shHqzlIBpr3747ceSDuw7E_w
    
    Bug: chromium:40060076
    Change-Id: Ia70ca5d0aadc638293ac3f65d0be2e64181f92e4
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5845591
    Auto-Submit: Solomon Kinard <solomonkinard@chromium.org>
    Reviewed-by: David Bertoni <dbertoni@chromium.org>
    Reviewed-by: Justin Lulejian <jlulejian@chromium.org>
    Commit-Queue: Justin Lulejian <jlulejian@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1352991}

M       chrome/browser/extensions/web_accessible_resources_browsertest.cc
M       extensions/browser/extension_navigation_throttle.cc
M       tools/metrics/histograms/metadata/extensions/histograms.xml

https://chromium-review.googlesource.com/5845591


### ap...@google.com (2024-09-10)

Project: chromium/src
Branch: main

commit b1039fca60bec23bcbb16af66b35dc65fa51979b
Author: Solomon Kinard <solomonkinard@chromium.org>
Date:   Tue Sep 10 20:05:54 2024

    Extensions: WAR: Metrics test both accessible and non-accessible paths
    
    The original plan was to only have metrics when the resource was not
    web accessible. Since that changed later, update the test to reflect it.
    
    Bug: chromium:40060076
    Change-Id: I850df385d1b52d1f51ed2e94aebcc58d93f3ea68
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5851731
    Auto-Submit: Solomon Kinard <solomonkinard@chromium.org>
    Commit-Queue: David Bertoni <dbertoni@chromium.org>
    Reviewed-by: David Bertoni <dbertoni@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1353556}

M       chrome/browser/extensions/web_accessible_resources_browsertest.cc

https://chromium-review.googlesource.com/5851731


### ar...@chromium.org (2024-12-13)

**(secondary security shepherd)**

Hi [solomonkinard@chromium.org](mailto:solomonkinard@chromium.org), this but hasn't been updated for a while.

Here are the metrics you collected in the last patches.
<https://uma.googleplex.com/p/chrome/timeline_v2?sid=9bd757aa8ba97791ee24f9ba0121640f>

Could you please take a look and let us know what are the next steps?

### so...@chromium.org (2025-01-06)

I'm back now and will take a look at the metrics. Thank you.

### ap...@google.com (2025-02-01)

Project: chromium/src  

Branch: main  

Author: Solomon Kinard <[solomonkinard@chromium.org](mailto:solomonkinard@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6219551>

Extensions: WAR: Reduce two tests into one and simplify its call site

---


Expand for full commit details
```
Extensions: WAR: Reduce two tests into one and simplify its call site 
 
Bug: chromium:40060076 
Change-Id: I42d3fcadc445ddf66c66d86d52e7143e71eb6f5d 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6219551 
Commit-Queue: Solomon Kinard <solomonkinard@chromium.org> 
Reviewed-by: David Bertoni <dbertoni@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1414528}

```

---

Files:

- M `chrome/browser/extensions/web_accessible_resources_browsertest.cc`

---

Hash: 45959af8177219413254c32956b6589d1fef490f  

Date:  Fri Jan 31 20:30:11 2025


---

### ap...@google.com (2025-02-01)

Project: chromium/src  

Branch: main  

Author: Solomon Kinard <[solomonkinard@chromium.org](mailto:solomonkinard@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6219552>

Extensions: WAR: Colocate test class and test case

---


Expand for full commit details
```
Extensions: WAR: Colocate test class and test case 
 
Bug: chromium:40060076 
Change-Id: I4c73c90524816f9f7eebafc64b54955281b97eb5 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6219552 
Reviewed-by: David Bertoni <dbertoni@chromium.org> 
Commit-Queue: Solomon Kinard <solomonkinard@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1414531}

```

---

Files:

- M `chrome/browser/extensions/web_accessible_resources_browsertest.cc`

---

Hash: 6665607bfb193215232d658fb6a9fda178c20eee  

Date:  Fri Jan 31 20:58:26 2025


---

### ap...@google.com (2025-02-05)

Project: chromium/src  

Branch: main  

Author: Solomon Kinard <[solomonkinard@chromium.org](mailto:solomonkinard@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6160996>

Extensions: WAR: Prevent server redirect to non web accessible resources

---


Expand for full commit details
```
Extensions: WAR: Prevent server redirect to non web accessible resources 
 
Doc: 
https://docs.google.com/document/d/1ALcxHF2m85pqxEtJVQ_shHqzlIBpr3747ceSDuw7E_w/edit?usp=sharing 
 
Fixed: chromium:40060076 
Change-Id: I0440d9556ccc793d1963e434c1bb4bd097745b2e 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6160996 
Commit-Queue: Solomon Kinard <solomonkinard@chromium.org> 
Reviewed-by: Devlin Cronin <rdevlin.cronin@chromium.org> 
Reviewed-by: Mihai Sardarescu <msarda@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1416132}

```

---

Files:

- M `chrome/browser/extensions/web_accessible_resources_browsertest.cc`
- M `chrome/browser/profiles/profile_keyed_service_browsertest.cc`
- M `chrome/test/data/extensions/api_test/webrequest/test_redirects/manifest.json`
- M `extensions/browser/BUILD.gn`
- M `extensions/browser/api/web_request/extension_web_request_event_router.cc`
- M `extensions/browser/api/web_request/web_request_event_router_factory.cc`
- M `extensions/browser/core_browser_context_keyed_service_factories.cc`
- A `extensions/browser/extension_navigation_registry.cc`
- A `extensions/browser/extension_navigation_registry.h`
- M `extensions/browser/extension_navigation_throttle.cc`
- M `extensions/browser/extension_web_contents_observer.cc`
- M `extensions/common/extension_features.cc`
- M `extensions/common/extension_features.h`
- M `extensions/common/manifest_handlers/web_accessible_resources_info.cc`

---

Hash: ce0f402f288d3f0aacfdd843f57d8839613b70db  

Date:  Wed Feb 05 06:54:39 2025


---

### pe...@google.com (2025-02-05)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### nd...@protonmail.com (2025-02-05)

🥳

### ap...@google.com (2025-02-05)

Project: chromium/src  

Branch: main  

Author: Solomon Kinard <[solomonkinard@chromium.org](mailto:solomonkinard@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6230274>

Extensions: WAR: Colocate navigation decisioning to its registry

---


Expand for full commit details
```
Extensions: WAR: Colocate navigation decisioning to its registry 
 
No behavior change expected. 
 
Bug: chromium:40060076 
Low-Coverage-Reason: TRIVIAL_CHANGE 
Change-Id: Ib4feabdd7e0560673531f593e4128aa23e24b59c 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6230274 
Reviewed-by: Devlin Cronin <rdevlin.cronin@chromium.org> 
Commit-Queue: Solomon Kinard <solomonkinard@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1416233}

```

---

Files:

- M `extensions/browser/extension_navigation_registry.cc`
- M `extensions/browser/extension_navigation_registry.h`
- M `extensions/browser/extension_navigation_throttle.cc`

---

Hash: 87c77f3cdf63ff9cdead9b97f1f627427654b0d1  

Date:  Wed Feb 05 09:16:51 2025


---

### ap...@google.com (2025-02-07)

Project: chromium/src  

Branch: main  

Author: Solomon Kinard <[solomonkinard@chromium.org](mailto:solomonkinard@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6230814>

Extensions: WAR: Prevent extension redirect to non-WAR

---


Expand for full commit details
```
Extensions: WAR: Prevent extension redirect to non-WAR 
 
Includes a shorter function name, typed flat_map members, and other 
small improvements. 
 
Bug: chromium:40060076 
Change-Id: I2fa8078f819173fb4701362aa88390e4945ee62a 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6230814 
Reviewed-by: Devlin Cronin <rdevlin.cronin@chromium.org> 
Commit-Queue: Solomon Kinard <solomonkinard@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1417131}

```

---

Files:

- M `chrome/browser/extensions/api/web_request/web_request_api_unittest.cc`
- M `chrome/browser/extensions/web_accessible_resources_browsertest.cc`
- M `extensions/browser/api/web_request/extension_web_request_event_router.cc`
- M `extensions/browser/api/web_request/web_request_api_helpers.cc`
- M `extensions/browser/api/web_request/web_request_api_helpers.h`
- M `extensions/browser/extension_navigation_registry.cc`
- M `extensions/browser/extension_navigation_registry.h`
- M `extensions/browser/extension_navigation_throttle.cc`

---

Hash: 8c29dd7a6c9b72170056d95cafa4130e50eb0968  

Date:  Thu Feb 06 18:52:27 2025


---

### ap...@google.com (2025-02-13)

Project: chromium/src  

Branch: main  

Author: Solomon Kinard <[solomonkinard@chromium.org](mailto:solomonkinard@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6262487>

Extensions: WAR: Simplify and rename class for better re-usability

---


Expand for full commit details
```
Extensions: WAR: Simplify and rename class for better re-usability 
 
Bug: chromium:40060076 
Change-Id: I348cb3cc153bafb48d871d9957910f53244c2ff1 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6262487 
Reviewed-by: Devlin Cronin <rdevlin.cronin@chromium.org> 
Commit-Queue: Solomon Kinard <solomonkinard@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1420160}

```

---

Files:

- M `chrome/browser/extensions/web_accessible_resources_browsertest.cc`

---

Hash: be949061e561cfc316cd5559e122de5877fda659  

Date:  Thu Feb 13 14:18:46 2025


---

### ap...@google.com (2025-02-14)

Project: chromium/src  

Branch: main  

Author: Solomon Kinard <[solomonkinard@chromium.org](mailto:solomonkinard@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6253993>

Extensions: WAR: Add test for main frame server redirection prevention

---


Expand for full commit details
```
Extensions: WAR: Add test for main frame server redirection prevention 
 
Bug: chromium:40060076 
Change-Id: I1c4b2c3710b68c3598e1a4973756bd3b3aa08702 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6253993 
Reviewed-by: Devlin Cronin <rdevlin.cronin@chromium.org> 
Commit-Queue: Solomon Kinard <solomonkinard@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1420316}

```

---

Files:

- M `chrome/browser/extensions/web_accessible_resources_browsertest.cc`

---

Hash: 4148ca3591995ceff87918da51f89f769a462221  

Date:  Thu Feb 13 21:50:25 2025


---

### ap...@google.com (2025-02-14)

Project: chromium/src  

Branch: main  

Author: Sergey Poromov <[poromov@chromium.org](mailto:poromov@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6268841>

Revert "Extensions: WAR: Add test for main frame server redirection prevention"

---


Expand for full commit details
```
Revert "Extensions: WAR: Add test for main frame server redirection prevention" 
 
This reverts commit 4148ca3591995ceff87918da51f89f769a462221. 
 
Reason for revert: The test seems to be flaky: 
https://ci.chromium.org/ui/p/chromium/builders/ci/Win11%20Tests%20x64/28575/overview 
 
Original change's description: 
> Extensions: WAR: Add test for main frame server redirection prevention 
> 
> Bug: chromium:40060076 
> Change-Id: I1c4b2c3710b68c3598e1a4973756bd3b3aa08702 
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6253993 
> Reviewed-by: Devlin Cronin <rdevlin.cronin@chromium.org> 
> Commit-Queue: Solomon Kinard <solomonkinard@chromium.org> 
> Cr-Commit-Position: refs/heads/main@{#1420316} 
 
Bug: chromium:40060076 
Change-Id: Ie17227016ab86b4cf4fab2af0535a9a7ba2ea8ee 
No-Presubmit: true 
No-Tree-Checks: true 
No-Try: true 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6268841 
Commit-Queue: Sergey Poromov <poromov@chromium.org> 
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
Owners-Override: Sergey Poromov <poromov@chromium.org> 
Auto-Submit: Sergey Poromov <poromov@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1420436}

```

---

Files:

- M `chrome/browser/extensions/web_accessible_resources_browsertest.cc`

---

Hash: 1d71eeec5226ee36245064b4c76e4f99caed4209  

Date:  Fri Feb 14 04:58:30 2025


---

### ap...@google.com (2025-02-19)

Project: chromium/src  

Branch: main  

Author: Solomon Kinard <[solomonkinard@chromium.org](mailto:solomonkinard@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6268224>

Extensions: WAR: Add test for main frame server redirection prevention

---


Expand for full commit details
```
Extensions: WAR: Add test for main frame server redirection prevention 
 
Bug: chromium:40060076 
Change-Id: I32577f61cb989fbc446e7c63d2e4587cf335cc64 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6268224 
Reviewed-by: Devlin Cronin <rdevlin.cronin@chromium.org> 
Commit-Queue: Solomon Kinard <solomonkinard@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1421945}

```

---

Files:

- M `chrome/browser/extensions/web_accessible_resources_browsertest.cc`

---

Hash: 29cb77bec10a689ab16dc4816340405f3d9e368c  

Date:  Wed Feb 19 07:33:20 2025


---

### ap...@google.com (2025-02-20)

Project: chromium/src  

Branch: main  

Author: Solomon Kinard <[solomonkinard@chromium.org](mailto:solomonkinard@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6278083>

Extensions: WAR: Add a test for subresource navigation

---


Expand for full commit details
```
Extensions: WAR: Add a test for subresource navigation 
 
Included: 
* Cross origin navigation for main_frame test: 
  crrev.com/c/6253993/comment/6c709edd_44e058f4 
 
Bug: chromium:40060076 
Change-Id: Ic08725fda5846f7bd07019cee0f618e553c8c156 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6278083 
Reviewed-by: Devlin Cronin <rdevlin.cronin@chromium.org> 
Commit-Queue: Solomon Kinard <solomonkinard@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1422716}

```

---

Files:

- M `chrome/browser/extensions/web_accessible_resources_browsertest.cc`

---

Hash: 6dd275ac73511547f92ce0545a27a8e186404678  

Date:  Thu Feb 20 11:50:14 2025


---

### ap...@google.com (2025-02-21)

Project: chromium/src  

Branch: main  

Author: Solomon Kinard <[solomonkinard@chromium.org](mailto:solomonkinard@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6288045>

Extensions: WAR: Enable "ExtensionWARForRedirect" by default

---


Expand for full commit details
```
Extensions: WAR: Enable "ExtensionWARForRedirect" by default 
 
$ chromium --enable-features=ExtensionWARForRedirect 
 
Fixed: chromium:40060076 
Change-Id: I77584d73d8ea5be04bd4378f4661c030bad92801 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6288045 
Reviewed-by: Oliver Dunk <oliverdunk@chromium.org> 
Commit-Queue: Solomon Kinard <solomonkinard@chromium.org> 
Reviewed-by: Devlin Cronin <rdevlin.cronin@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1423049}

```

---

Files:

- M `extensions/common/extension_features.cc`

---

Hash: 9e4e1d6af14a445e01f21e1bf5165a22b8fa8205  

Date:  Fri Feb 21 04:40:56 2025


---

### pe...@google.com (2025-02-21)

LTS Milestone M132

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### ch...@google.com (2025-02-21)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### so...@chromium.org (2025-02-21)

There are several CLs though, but this is one of the early ones.

### ch...@google.com (2025-02-21)

Dear owner, thanks for fixing this bug. We've reopened it because:

- Some CLs listed in the “Fixed By Code Changes” field are invalid and have been removed. Please provide an appropriate Gerrit url that matches the pattern: `https://<host>-review.googlesource.com/c/<repo>/+/<change_number>` or use the value 'NA' and re-mark this bug as fixed. If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### sp...@google.com (2025-03-06)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
report of lower impact web platform privilege escalation


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-03-06)

Thank you for your efforts and reporting this issue to us!

### qk...@google.com (2025-03-06)

Labelling as not applicable for LTS 132 and 126, because the fixes required to enable "ExtensionWARForRedirect" by default[1]. But we cannot merge new features to the LTS branch.

[1] https://chromium-review.googlesource.com/c/chromium/src/+/6288045

### nd...@protonmail.com (2025-03-06)

Thanks for fixing and the reward :)

### ch...@google.com (2025-06-03)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### dx...@google.com (2025-07-18)

Project: chromium/src  

Branch:  main  

Author:  Solomon Kinard [solomonkinard@chromium.org](mailto:solomonkinard@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6763646>

Extensions: WAR: Remove kExtensionWARForRedirect which merged in m135

---


Expand for full commit details
```
     
    Bug: 40060076 
    Change-Id: I14c23e96f057e2d5a2e65c914f3c4cca9e5a1fcb 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6763646 
    Reviewed-by: Devlin Cronin <rdevlin.cronin@chromium.org> 
    Commit-Queue: Solomon Kinard <solomonkinard@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1488877}

```

---

Files:

- M `chrome/browser/extensions/web_accessible_resources_browsertest.cc`
- M `extensions/browser/extension_navigation_registry.cc`
- M `extensions/browser/extension_navigation_registry.h`
- M `extensions/common/extension_features.cc`
- M `extensions/common/extension_features.h`

---

Hash: [d8aa62782b311b0037520a176fd3b9d93d86e6bc](http://crrev.com/d8aa62782b311b0037520a176fd3b9d93d86e6bc)  

Date: Fri Jul 18 15:41:37 2025


---

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060076)*
