# Security: Extension messages can indefinitely extend user activation expiry and repeatedly use of it

| Field | Value |
|-------|-------|
| **Issue ID** | [40094769](https://issues.chromium.org/issues/40094769) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Input, Platform>Extensions |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | de...@gmail.com |
| **Assignee** | mu...@chromium.org |
| **Created** | 2019-04-29 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

A user activation is required in order to perform certain actions on a webpage. For example, a page won't be able to open a popup window without a (recent) user activation.

However, when an extension with some simple specific (and valid) behavior is installed, a page can do three things:

1. Gain transient user activation from actions that take place outside of the page.
2. Extend the lifetime of this transient user activation indefinitely.
3. Repeatedly make use of it, to spawn an unlimited number of popups, for example.

**VERSION**  

Chrome Version: Tested on 74.0.3729.108 (stable) and 76.0.3780.0 (canary)  

Operating System: Windows 10 Pro, version 1809

**REPRODUCTION CASE**

1. Install the attached extension (made up of manifest.json, background.js and content\_script.js).
2. The other attached files (index.html, main.js and link\_to\_index.html) form a simple website. Download each of the files and place them in a directory.
3. In the directory you downloaded the files to, run the following command in a terminal:

python3 -m http.server 8080

This will start a simple web server that can be used to serve the files in the directory.  

4. In the browser, navigate to the following location:

<http://localhost:8080/index.html>

5. Click this page a single time. It should then open a popup a short time later and reload. This process should continue indefinitely, so that the page opens an endless stream of popups (one every 2 seconds).
6. There are also alternative ways of triggering this behavior. In the items below, "target page" refers to the page above (i.e. <http://localhost:8080/index.html>).

6.1. Open any http or https site. Next, open the target page in a background tab (this can be done by bookmarking the page, then right-clicking the bookmark and selecting "Open in new tab"). Next click the http/https site a single time. As above, the target page should start opening a series of tabs.

6.2. Open any http or https site. Open the target page in a background tab. Next, switch to that tab by clicking on the tab in the tab strip or pressing Ctrl+Tab. As above, the target page should start opening a series of tabs.

6.3. Open the target page. Then switch to any other tab, by clicking on a tab in the tab strip, or by pressing Ctrl+Tab/Ctrl+Shift+Tab. As above, the target page should start opening a series of tabs. This also works if you switch tabs in a different window.

6.4. Open <http://localhost:8080/link_to_index.html>. This page simply contains a link to index.html. Click the link. The target page should start opening a series of tabs. This also works if the link is on another domain, it doesn't have to be same origin.

6.5. Open any http or https site, click the page of that website, then load the target page from a bookmark. Provided you do this within the activation timeout (5 seconds), the target page will immediately gain activation and start opening new tabs a short time later.

6.6. Open the target page. Then switch to the first tab by pressing Ctrl+1. The target page will gain activation and start opening new tabs a short time later.

6.7. Open the target page. Next close the tab, then reopen it using Ctrl+Shift+T. The target page will gain activation and start opening new tabs a short time later. This doesn't work if the tab is reopened from the history menu.

There are likely other ways of triggering activation, and that will depend on the exact extension that's installed.

Some detail on what's happening:

The extension that's installed does a few simple things:

- It registers an event listener for the chrome.tabs.onActivated event and simply logs a message to the console when it's received.
- It declares a content script that runs in all http and https origins.
- The content script firstly posts a message to the extension when a page is loaded.
- The extension posts a message back once it's received this message.
- The content script then sends a second message once it's received a reply to the first.
- The extension again sends a reply message. The sequence of messages is:

message-1 -> reply-1 -> message-2 -> reply-2

- The content script also posts a message when the window it's embedded within is clicked.

Putting these pieces together, what happens is that when the content script posts a message to the extension, the extension gains user activation (if the webpage itself has it). So when you click on any http/https site and the content script posts a message back to the extension, the extension gains user activation.

Then, any page that happens to load shortly after this has happened (before the user activation has expired) will gain the user activation from the extension. The page loads, the content script posts a message to the extension and when the extension posts a message back, the page gains user activation.

When the content script described above posts the second message, my understanding is that this has the side effect of resetting the activation timeout within the extension back to its original value (of 5 seconds). This is because the page gains the user activation when receiving a reply to the first message and when the second message is sent, it resets the activation timeout within the extension.

When the page reloads, it regains activation from the extension, the process described here is repeated (so that the activation timeout within the extension is extended again) and the page can keep the activation alive indefinitely and repeatedly use it.

Unlike the regular postMessage process, which prevents a user activation from being endlessly exchanged between windows, the user activation here can be passed back and forth without limit.

The extension also gains user activation when the tab selection is changed, at least if it's listening for the chrome.tabs.onActivated event and the user was responsible for the tab selection change (as opposed to it being changed by an extension or webpage). This is why switching tabs in step 6 above allowed the target page to open repeated new windows.

The page in the demonstration above is set up so that it reloads once every 2 seconds and attempts to open a popup window. 2 seconds is below the user activation timeout (of 5 seconds). This, in combination with the messages being passed between the content script and extension, prevent the activation from expiring.

To allow you to verify that the extension is gaining activation from the page, the extension will run the following console.log() command once every second:

console.log("navigator.userActivation.isActive: " + navigator.userActivation.isActive);

If you inspect the background page of the extension in a separate window, switch to the console tab and monitor that when you switch between tabs or click on a website, you should find that the extension gains activation. When the target page above starts repeatedly opening tabs, you should then find that the extension never loses the activation. The above log statement will keep printing true indefinitely.

The behavior described here isn't purely hypothetical. It applies to real world extensions that are used by a large number of users. uBlock Origin has this exact behavior. If you install that instead of the extension attached here, you'll see the same results. It's trivially easy to take advantage of this behavior with uBlock Origin. You can also achieve similar results with the LastPass extension (I don't think it sets up a click handler, but switching between tabs will trigger the behavior). The basic thing you need is for an extension to exchange messages with a content script.

As shown in step 6 above, it's possible to gain activation a number of different ways. All a site would require to gain activation and keep activation is for the user to open the site and perform some very basic interaction with the browser itself (not the page). And not even that if one of these extensions happens to have user activation when the page is first loaded (because another page was recently clicked, for example).

That means that if one of these extensions, or a similar extension, is installed, the behavior is trivial to take advantage of. It also allows you to do some relatively nasty things, which I'll describe in my next message.

**CREDIT INFORMATION**  

Reporter credit: David Erceg

## Attachments

- [background.js](attachments/background.js) (text/plain, 519 B)
- [content_script.js](attachments/content_script.js) (text/plain, 833 B)
- [manifest.json](attachments/manifest.json) (text/plain, 494 B)
- [index.html](attachments/index.html) (text/plain, 134 B)
- [link_to_index.html](attachments/link_to_index.html) (text/plain, 125 B)
- [main.js](attachments/main.js) (text/plain, 166 B)
- [renew_activation_state_thru_send_reply.zip](attachments/renew_activation_state_thru_send_reply.zip) (application/octet-stream, 3.2 KB)

## Timeline

### de...@gmail.com (2019-04-29)

I have some detailed examples of how you can abuse this behavior, but to summarize here:

- The first obvious thing a page can do is open an unlimited number of tabs/popups. Although the page in the demonstration above opens a new tab every 2 seconds, there's no reason you would have to wait this long. You could spawn new windows at a much faster rate.

- A page can set focus to a window it's created at any point. If you're in another window in Chrome, this will pull focus back to the window the target tab is in. If you're working outside of Chrome, this will cause it to request focus (e.g. by flashing the taskbar icon on Windows). This could be used maliciously to attempt to attract attention to a particular tab.

- This can be further abused to set focus to a window in a tight loop (therefore preventing any other tab from being selected). This is somewhat mitigated by the fact that background tabs are throttled (so that the tight loop in the background tab will run less often), but it still very effectively prevents the user from giving focus to another tab.

- This would then essentially break other parts of the browser's UI. For example, clicking the "History" item in Chrome's main menu would result in the history page being opened, but focus would immediately switch back to the other tab and it would be difficult to assign the history tab focus.

- A page can show a file picker prompt at any point after activation has been gained. This prompt will appear over any other tab that happens to be selected, possibly making it appear like that tab is the one requesting a file.

- The page can show file picker prompts repeatedly, to try and force the user to select a file.

- A page can repeatedly enter full screen mode. Even though you can dismiss the full screen effect by pressing ESC, the next full screen request is invoked immediately. This prevents you from being able to easily reach the browser's UI.

This is different from standard behavior. Normally, a page can only request full screen while the transient user activation is set. Because a page can retain transient activation indefinitely, there is no point at which the full screen requests will stop.

- A page can override all browser-initiated navigations that take place within its tab. This is because it appears that any navigations the page makes are user-initiated.

- A page can open a new window when unloaded. This can be used to create a duplicate tab when the tab is closed and that duplicate tab will have the same behavior, effectively preventing the tab from being closed.

- This can be abused further to effectively stop the user from being able to cleanly close a window or exit the browser itself. The issue is that to close a window, the browser needs to close each tab. A tab with the behavior described above will be able to open a duplicate of itself and that duplicate tab will open a duplicate of itself. This process repeats endlessly. Past a certain point (about 6 tabs from testing I've done), closing a window with these tabs in will just result in an unlimited number of new tabs being created, stopping the window from being closed.

The same process will also stop the browser from being able to exit cleanly, as to exit, the browser needs to close each tab, but closing these duplicate tabs isn't possible without creating more tabs.


You can do each of these things without having the user interact with your page at all. If the user has an appropriate extension installed, clicking a link to your website, switching tabs after opening the site or clicking the page of another site will be enough to grant the page indefinite activation. Key presses in another tab may also grant activation, depending on exactly what events an extension listens and responds to.

A downside to this sort of behavior, from an attacker's point of view, is that there's no way to retain activation once the browser is restarted. You can retain activation whilst the browser is running, but once it's restarted, the page won't have it and the user can close the tabs. There's still the potential problem here that if the user has one of these tabs opened, it loads and the user doesn't immediately close it, it could regain activation fairly easily.

I can attach some demonstration files to illustrate the above effects.

Overall, some of these effects would allow you to effectively take control of the browser's UI. That is, you could prevent users from switching tabs, from navigating within a tab and you could open new tabs or popup windows at any time.

### mm...@chromium.org (2019-04-29)

Thanks for your report. It's hard for me to judge whether there is any abuse / unintended behavior, so handing this over to Devlin, the Extensions lead for further triage.

[Monorail components: Platform>Extensions]

### mm...@chromium.org (2019-04-29)

[Empty comment from Monorail migration]

### rd...@chromium.org (2019-04-29)

Yeah, extensions + user gestures aren't in a great state - there's actually a fair amount wrong with them (I don't think we have a meta bug for it, so I'll file one after this).  We don't usually use user gesture as a real security measure for extensions.  There are a few times we require user gesture in extension functions (e.g., permissions.request()), but this is more commonly because we want to prevent annoyance, rather than provide protection.  Additionally, the majority of actions that require user gesture on the web and are described here (e.g., opening popups) are trivially available to extensions without any user gesture through the tabs API.  A few are more interesting - fullscreen and file picker, for instance.

I don't know if these are truly security vulnerabilities (again, most are just annoying, when taking into account what the extension can already do), but I wouldn't be surprised if there's some malice that can happen.  I think Severity-Low is probably right.

### de...@gmail.com (2019-04-29)

The issue here isn't so much with the extension, but with the propagation of the user activation to a webpage. The extension in this case isn't doing anything that's invalid or wrong, but the webpage gains user activation from it anyway. In other words, a webpage can gain activation from a legitimate extension without any direct cooperation from that extension and the webpage can use that activation in the ways described above. Whether the extension can misuse the activation is a separate matter.

A webpage targeting this behavior, for example, could use the presence of uBlock Origin to gain user activation for itself. uBlock Origin is just a stepping stone that's used by an ordinary website here. uBlock Origin wouldn't be directly participating in any way.

### de...@gmail.com (2019-04-29)

So this isn't really an issue with extensions per se, more with the way user activation is propagated. The ordinary postMessage process stops windows from exchanging the user activation between themselves an unlimited number of times. Here, a webpage can use an unwitting extension to do precisely that.

### rd...@chromium.org (2019-04-29)

I see - that is indeed strange.  We synthesize a user gesture in the receiving context for an extension message, but it's done with a WebScopedUserGesture - I wouldn't expect this to have the same "activation period" that "real" user gestures do.  However, it seems to, since the message from the background page is being sent asynchronously from when it was received, and the user gesture is still active.  That's very strange.

+mustaq, is that WAI for a WebScopedUserGesture?  I would have expected the gesture to terminate the moment the WebScopedUserGesture goes out of scope?

It'd also be great if we could restrict the WebScopedUserGesture to a specific v8 context, instead of a frame - that would prevent web pages from hijacking extension user gestures at any time.

### rd...@chromium.org (2019-04-29)

Also, filed https://crbug.com/chromium/957633 for general extension user gesture issues (sorry, restricted, since it discusses a bit more than just what's here).

### sh...@chromium.org (2019-04-30)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mu...@chromium.org (2019-05-06)

Thanks derceg86@gmail.com for the repro and detailed analysis.  We internally sensed the possibility of such an abuse before from user activation perspective, but I never came up with a repro (as a non-expert in extensions).

Re WebScopedUserGesture: with UAv2, the scoping concept is gone.  I believe we need a fix that would satisfy the core requirements of https://crbug.com/chromium/848778.

### mu...@chromium.org (2019-05-06)

[Empty comment from Monorail migration]

### mu...@chromium.org (2019-05-07)

[Empty comment from Monorail migration]

### mu...@chromium.org (2019-05-07)

Charlie made another (internal) repro that we had been struggling to understand; Ella just discovered that it is caused by some extension.  https://crbug.com/chromium/951934.

### mu...@chromium.org (2019-05-07)

[Empty comment from Monorail migration]

### rd...@chromium.org (2019-05-07)

> Re WebScopedUserGesture: with UAv2, the scoping concept is gone.  I believe we need a fix that would satisfy the core requirements of https://crbug.com/chromium/848778.

I think it's important to not just have a way to satisfy a browser-triggered user gesture, but also a way to ensure it doesn't persist for a long activation period (else this bug won't be fixed).  Since this seems to be an issue with the general UAv2 framework, passing ownership to mustaq@.

### mu...@chromium.org (2019-05-07)

To be clear, the root cause is not the lack of scoping in UAv2, but the creation of WebScopedUserGesture token on receiver.  This is a problem that existed before UAv2: with site isolation, every extension message creates a /separate/ copy of WebScopedUserGesture token in the receiver process with or without UAv2; because of process separation, there is no way to link these two tokens.
- Without UAv2, this allows multiple consumption calls unconditionally (similar to https://crbug.com/chromium/937330 with postMessages).
- UAv2 improves the situation a bit by guaranteeing single consumption per page (per frame tree), and by fusing consecutive notification calls in the same process.

In fact, the reporter here implemented exactly what we feared about "multiplying tokens" earlier last year.

### mu...@chromium.org (2019-06-07)

[Empty comment from Monorail migration]

### mu...@chromium.org (2019-06-24)

[Empty comment from Monorail migration]

### mu...@chromium.org (2019-07-18)

rdevlin.cronin@: Seems like the suggestion recently made in an unrelated bug [1] can be use used to break the token creation cycle, right?  Something like: the background script would never forward the "active" state to content script unless the background activation is from browser UI (i.e. direct activation of the background script). 
- If this message from background script was in response to an "activated" message from the same content script, that particular script would still be active upon receiving the reply (because UAv2 has no stack-scoped tokens) so should work w/o any compat problems I believe.
- If the message from background script was in response to a message from /another/ content script, the response receiver shouldn't expect user activation.

Do you think we can try this?

[1] https://bugs.chromium.org/p/chromium/issues/detail?id=907167#c53

### mu...@chromium.org (2019-07-25)

[Empty comment from Monorail migration]

### mu...@chromium.org (2019-08-21)

This is still blocked on a problem in extension messaging (https://crbug.com/chromium/957633).  We had a few suggestions on that bug, need more information to investigate any of them.

### sh...@chromium.org (2019-09-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-12-11)

[Empty comment from Monorail migration]

### mu...@chromium.org (2020-01-15)

[Empty comment from Monorail migration]

### sh...@chromium.org (2020-02-05)

[Empty comment from Monorail migration]

### [Deleted User] (2020-04-09)

[Empty comment from Monorail migration]

### [Deleted User] (2020-05-20)

[Empty comment from Monorail migration]

### mu...@chromium.org (2020-05-21)

[Empty comment from Monorail migration]

### mu...@chromium.org (2020-05-21)

[Empty comment from Monorail migration]

### mu...@chromium.org (2020-05-26)

[Empty comment from Monorail migration]

### mu...@chromium.org (2020-05-26)

[Empty comment from Monorail migration]

### nz...@chromium.org (2020-06-12)

[Empty comment from Monorail migration]

### mu...@chromium.org (2020-06-24)

We have another related bug filed by an external "ad security/abuse" company: https://crbug.com/chromium/1098582.  The bug covers two separate problems, I just marked it to cover the first subproblem (with WebKit).  The second subproblem is this bug!

### [Deleted User] (2020-07-16)

[Empty comment from Monorail migration]

### [Deleted User] (2020-08-26)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-07)

[Empty comment from Monorail migration]

### mu...@chromium.org (2020-10-09)

FYI for future reference: An unrelated problem is planning to add user activation checks as a solution.  See Issue 1051198c#76.

### mu...@chromium.org (2020-10-09)

Correct link: http://crbug.com/1051198#c76

### [Deleted User] (2020-10-30)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-18)

[Empty comment from Monorail migration]

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

### lu...@chromium.org (2021-05-06)

rdevlin.cronin@, mustaq@ and others: Is low security severity right here?

This severity was set in https://crbug.com/chromium/957553#c2 and confirmed https://crbug.com/chromium/957553#c4, but maybe this was based on some assumptions that might not hold, like
A. An assumption that the bug only gives extra unwanted powers to extensions (not to arbitrary web pages)
B. An assumption that a webpage can't exploit the bug without a cooperating-or-buggy extension

Arguments for bumping the severity:
I am guessing that there is a non-empty set of security capabilities that are gated on a user gesture.  Other security bugs may have their severity lowered if an exploit requires a user gesture (based on https://chromium.googlesource.com/chromium/src/+/master/docs/security/severity-guidelines.md#toc-low-severity).

Let me proactively bump up the severity - please shout (and downgrade back again) if you think the lower severity is more correct.

### [Deleted User] (2021-05-06)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mu...@chromium.org (2021-05-06)

I agree with https://crbug.com/chromium/957553#c48 arguments about bumping the severity.

lukasza@ But P1 (set in https://crbug.com/chromium/957553#c49) feels like too high because it's an old bug?

### rd...@chromium.org (2021-05-06)

> lukasza@ But P1 (set in https://crbug.com/chromium/957553#c49) feels like too high because it's an old bug?

Drive-by: I don't think age should determine priority.  (Something can potentially be very high priority to fix, but still unaddressed.)  I'd lean towards keeping priority and severity in-sync with one another.

### [Deleted User] (2021-05-21)

mustaq: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-05-26)

[Empty comment from Monorail migration]

### [Deleted User] (2021-06-04)

mustaq: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mu...@chromium.org (2021-06-09)

This security bug is the first actionable blocker for https://crbug.com/chromium/957633.

To simplify the bug dependency, moved the blocking https://crbug.com/chromium/848778 from here to "bigger-picture" https://crbug.com/chromium/957633.



### mu...@chromium.org (2021-06-09)

Cross-posting a comment originally posted four months ago here: https://bugs.chromium.org/p/chromium/issues/detail?id=957633#c24.  We will start looking into it in Q3.

<quote>
I summarized the related bugs and possible solutions in the following Google-only doc.  Let's discuss in the doc, and I will update the bug once we have a reasonable solution/plan.
https://docs.google.com/document/d/1TKjjwFlQGh2LLm0_mOW6FJdmmwyOBMj_fdWJyAJ_Q50/edit?usp=sharing
</quote>

### ad...@google.com (2021-07-08)

[Empty comment from Monorail migration]

### mu...@chromium.org (2021-07-27)

[Empty comment from Monorail migration]

### mu...@chromium.org (2021-07-27)

[Empty comment from Monorail migration]

### mu...@chromium.org (2021-07-27)

In Interactions team today, we discussed about concrete next steps here.  This bug potentially allows infinite number of popups (which is just one example of things that can go bad) so we should do something to fix it!

We know that removing the artificial user activation trigger [1] from extension messaging fixes this bug.   But measuring the potential impact of that change is not easy [2].  Our histogram data (see kExtensionMessaging* in the graphs here [3]) shows a bit of reliance of web-APIs on this unwanted activation but there is a chance this data is polluted by too many false positives.  Our experience with UAv2 suggests that a big part of the reliance could be just unexpected leftover from pre-UAv2 code.

So far we don't know a single real-world extension that would certainly break from this change.

To get a sense of true real-world impact, we decided to run a finch trial to remove the artificial user activation trigger [1].  We will start with a low trial coverage and then increase the coverage slowly while keeping an eye on bug reports.

[1] https://source.chromium.org/chromium/chromium/src/+/main:extensions/renderer/native_renderer_messaging_service.cc;drc=0775b29ae4f4dc6d3ad250f525d76c97320e6e75;l=345
[2] https://bugs.chromium.org/p/chromium/issues/detail?id=957633#c5
[3] https://docs.google.com/document/d/1TKjjwFlQGh2LLm0_mOW6FJdmmwyOBMj_fdWJyAJ_Q50/edit#heading=h.hkadlh63j890

[Monorail components: Blink>Input]

### mu...@chromium.org (2021-07-28)

[Adding one more detail to my last post https://crbug.com/chromium/957553#c60]

I _think_ just removing artificial user activation trigger [1] would work fine, without a special handling for "privileged" message sender.  This is because our UMA data [3] has no "privileged" sender counts, which implies this case is not actually relying on the artificial trigger in [1].

### rd...@chromium.org (2021-07-28)

Thanks for getting back to this one, mustaq@!

If we fully remove the artificial activation trigger, I am very concerned about breakage.  (For instance, I suspect that a content script messaging a background page to use an API with a user gesture is not uncommon.)  Additionally, we know that this breakage can be hard to detect and hard to diagnose.  We've had multiple escalations from changes that aren't properly discovered until stable, at which point it becomes a P0 to fix.  Do you have a concrete plan for ensuring we don't break critical use cases for users, or how to properly attribute it if we do?

The other solution we've discussed to this in the past is that gestures should be consumed once used.  This seems like a much less controversial change with significantly lower risk of breakage (and if it does cause breakage, it seems much more reasonable - I don't think many folks would argue that a gesture should be able to be used infinite times).  Can you describe why removing the synthetic gesture entirely, rather than limiting one gesture to one use, is preferable?

### rd...@chromium.org (2021-07-28)

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

### mu...@chromium.org (2021-09-10)

For records, in order to resolve the question on https://crbug.com/chromium/957553#c62, we (rdevlin.cronin@, flackr@ and me) met the next day and decided to add a restricted bit to the user activation state just for the extension messaging use-case.  The details appear in this section [1] of a Google-only doc (which is the same doc we mentioned in https://crbug.com/chromium/957553#c56 above).

[1] https://docs.google.com/document/d/1TKjjwFlQGh2LLm0_mOW6FJdmmwyOBMj_fdWJyAJ_Q50/edit#heading=h.z4gmcqnjat75


### [Deleted User] (2021-09-11)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-22)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-10-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/69f1b053c26ed3206d7c356b0d1c62bc490566ea

commit 69f1b053c26ed3206d7c356b0d1c62bc490566ea
Author: Mustaq Ahmed <mustaq@google.com>
Date: Wed Oct 06 22:38:01 2021

Add a restricted user activation state for synthetic triggers.

Also suppress synthetic activation triggering at an extension messaging
recipient when the message sender has a restricted activation.

Bug: 957553, 957633
Change-Id: I0b363fe907d18ef55d132b98a533c1cdf5e0d485
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3154195
Commit-Queue: Mustaq Ahmed <mustaq@chromium.org>
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Reviewed-by: Devlin <rdevlin.cronin@chromium.org>
Cr-Commit-Position: refs/heads/main@{#928908}

[modify] https://crrev.com/69f1b053c26ed3206d7c356b0d1c62bc490566ea/third_party/blink/common/frame/user_activation_state.cc
[modify] https://crrev.com/69f1b053c26ed3206d7c356b0d1c62bc490566ea/third_party/blink/renderer/core/frame/web_local_frame_impl.cc
[modify] https://crrev.com/69f1b053c26ed3206d7c356b0d1c62bc490566ea/third_party/blink/renderer/core/frame/web_local_frame_impl.h
[modify] https://crrev.com/69f1b053c26ed3206d7c356b0d1c62bc490566ea/extensions/renderer/messaging_util.cc
[modify] https://crrev.com/69f1b053c26ed3206d7c356b0d1c62bc490566ea/third_party/blink/public/web/web_local_frame.h
[modify] https://crrev.com/69f1b053c26ed3206d7c356b0d1c62bc490566ea/third_party/blink/public/common/frame/user_activation_state.h
[modify] https://crrev.com/69f1b053c26ed3206d7c356b0d1c62bc490566ea/third_party/blink/renderer/core/frame/frame.h
[modify] https://crrev.com/69f1b053c26ed3206d7c356b0d1c62bc490566ea/chrome/browser/extensions/extension_messages_apitest.cc


### mu...@chromium.org (2021-10-07)

The reported problem has been fixed, yayy!

We will use https://crbug.com/chromium/957633 for other related work around extension messaging user activation.

### mu...@chromium.org (2021-10-07)

[Empty comment from Monorail migration]

### mu...@chromium.org (2021-10-07)

> 1. Why does your merge fit within the merge criteria for these milestones (Chrome Browser, Chrome OS)?
Yes

> 2. What changes specifically would you like to merge? Please link to Gerrit.
https://chromium-review.googlesource.com/c/chromium/src/+/3154195

> 3. Have the changes been released and tested on canary?
No: waiting for Canary release.

> 4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
No.

> 5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative?
Not applicable.

### [Deleted User] (2021-10-07)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-07)

[Empty comment from Monorail migration]

### mu...@chromium.org (2021-10-07)

> 3. Have the changes been released and tested on canary?
Yes: just verified that in the latest Canary (96.0.4663.2) on Windows prevents both the original repro and my own repro (attached).

### go...@chromium.org (2021-10-07)

M96 is going to branch tonight and change listed at #76 is already in M96. No merge needed. 

### am...@google.com (2021-10-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-10-13)

Congratulations, David! The VRP Panel had decided to award you $3,000 for this report. Thank you for this report as well as your patience while the teams addressed this issue and got it resolved! 

### am...@google.com (2021-10-14)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-11-11)

[Empty comment from Monorail migration]

### ad...@google.com (2021-11-12)

[Empty comment from Monorail migration]

### am...@google.com (2021-12-23)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-13)

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

This issue was migrated from crbug.com/chromium/957553?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>Input, Platform>Extensions]
[Monorail blocking: crbug.com/chromium/957633]
[Monorail mergedwith: crbug.com/chromium/1233127, crbug.com/chromium/1233544, crbug.com/chromium/951934]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094769)*
