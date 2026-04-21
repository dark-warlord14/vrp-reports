# Triggering screenshare from an unloading page in a cross-process navigation displays the wrong origin

| Field | Value |
|-------|-------|
| **Issue ID** | [442860743](https://issues.chromium.org/issues/442860743) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>MediaStream, Internals>Sandbox>SiteIsolation, UI>Browser>Navigation, UI>Browser>Navigation>BFCache |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Chrome Version** | 140.0.7339.81 |
| **Reporter** | do...@gmail.com |
| **Assignee** | el...@chromium.org |
| **Created** | 2025-09-04 |
| **Bounty** | $10,000.00 |

## Description

# Steps to reproduce the problem

0. Host the node.js webhook for logging. (Optional)
1. Serve the provided PoCs (`PoC-redir.html` and `PoC-listener.html`) on a webserver (or any source that isn't plain `file://`).
2. Load `PoC-redir.html` or `PoC-listener.html` in Chrome Stable
   Trigger navigation as described in each PoC.

# Problem Description

After a cross-origin navigation fully commits, the previous document is no longer active.
Expected: all its task queues should be frozen (BFCache) or discarded, and it should not be able to call `history.go()` or alike.
Actual: the previous page continues to execute for ~3 seconds post-navigation, regardless of if its post or pre `pagehide` being called.

`PoC-redir.html` sets up two setTimeouts (both 1ms) on button press so the page navigates while not being blocked by the sleep. this way is restrictive in the sense of detection of navigation, but it gives much more access to the dead page than waiting for `pagehide` to be called (for example, it can actually see `localStorage` even past death).
`PoC-listener.html` sets up a `pagehide` listener and runs the code after `pagehide` gets called.
`PoC-listener.html` also shows that any kind of navigation works, including clicking a link, dragging a link over the tab or just typing a URL into the search bar. This is more flexible and would realistically be the one malicious actors use. It's downside is that you lose access to a lot of window functions and data visibility, but that shouldn't matter unless you are aiming to do something else other than abuse history.

I have tested many things and can safely say there doesn't seem to be any other cross-origin violations. Only other notable things are that rAF still fires exactly once and that requests made in the dead page all appear in new page's network tab as permanently pending.
Although they appear there, their origin is still considered the original page.

This requires zero user interaction to execute.
The attacker page can go back to any place in history using `history.go(n)`, not just back and forward.
`rel=noopener` is ineffective since this occurs in the same tab.
This is reproducible on a fresh chrome install and incognito.

This will not work if the malicious page was originally opened by `window.open()` and the opener still exists and will not work if it has a living child window it itself has opened that at any point has considered the malicious page it's opener.

.

# Summary

Cross-origin post-navigation tab hijack: dead page can force active page history traversal

# Custom Questions

#### Type of crash:

N/A

#### Crash state:

N/A

#### Reporter credit:

round.about (<https://x.com/roundaboug>)

# Additional Data

Category: Security   

Chrome Channel: Stable   

Regression: N/A \

## Attachments

- PoC-listener.html (text/html, 7.3 KB)
- PoC-redir.html (text/html, 7.0 KB)
- node-webhook.js (text/javascript, 1.4 KB)
- 2025-09-04 18-48-03.mp4 (video/mp4, 1.5 MB)
- PoC-redir.html (text/html, 7.1 KB)
- 2025-09-04 18-56-14.mp4 (video/mp4, 153.5 KB)
- Fri Sep 05 2025 13:01:29 GMT+0300 (Eastern European Summer Time).png (image/png, 64.4 KB)
- debug.log (text/plain, 36.4 KB)
- PoC-bluetoothcrash.html (text/html, 2.1 KB)
- PoC-showmedia.html (text/html, 2.0 KB)
- 2025-09-06 09-45-07.mp4 (video/mp4, 86.5 KB)
- PoC-mediabusysleeprace.html (text/html, 2.1 KB)
- PoC-eventlistenerincluded.html (text/html, 2.1 KB)
- PoC-indefiniteworker.html (text/html, 2.3 KB)
- PoC-asanlesscrash.html (text/html, 1.0 KB)
- Thu Sep 11 2025 12_23_28 GMT+0300 (Eastern European Summer Time).mp4 (video/mp4, 6.3 MB)
- recording (1).webm (video/webm, 156.9 KB)
- PoC-showmedia.html (text/html, 1.5 KB)

## Timeline

### do...@gmail.com (2025-09-04)

Why is the markdown so scuffed here? Ruined the whole formatting of my report.

Here's it with better formatting.

# Steps to reproduce the problem

0. Host the node.js webhook for logging. (Optional)
1. Serve the provided PoCs (`PoC-redir.html` and `PoC-listener.html`) on a webserver (or any source that isn't plain `file://`).
2. Load `PoC-redir.html` or `PoC-listener.html` in Chrome Stable

Trigger navigation as described in each PoC.

# Problem Description

After a cross-origin navigation fully commits, the previous document is no longer active.

Expected: all its task queues should be frozen (BFCache) or discarded, and it should not be able to call `history.go()` or alike.

Actual: the previous page continues to execute for ~3 seconds post-navigation, regardless of if its post or pre `pagehide` being called.

`PoC-redir.html` sets up two setTimeouts (both 1ms) on button press so the page navigates while not being blocked by the sleep. this way is restrictive in the sense of detection of navigation, but it gives much more access to the dead page than waiting for `pagehide` to be called (for example, it can actually see `localStorage` even past death).

`PoC-listener.html` sets up a `pagehide` listener and runs the code after `pagehide` gets called.

`PoC-listener.html` also shows that any kind of navigation works, including clicking a link, dragging a link over the tab or just typing a URL into the search bar. This is more flexible and would realistically be the one malicious actors use. It's downside is that you lose access to a lot of window functions and data visibility, but that shouldn't matter unless you are aiming to do something else other than abuse history.

I have tested many things and can safely say there doesn't seem to be any other cross-origin violations. Only other notable things are that rAF still fires exactly once and that requests made in the dead page all appear in new page's network tab as permanently pending.

Although they appear there, their origin is still considered the original page.

This requires zero user interaction to execute.

The attacker page can go back to any place in history using `history.go(n)`, not just back and forward.

`rel=noopener` is ineffective since this occurs in the same tab.

This is reproducible on a fresh chrome install and incognito.

This will not work if the malicious page was originally opened by `window.open()` and the opener still exists and will not work if it has a living child window it itself has opened that at any point has considered the malicious page it's opener.

### do...@gmail.com (2025-09-04)

Tested on android, only the redir one seems to work there, likely that pagehide isn't properly called or that it IS properly called and actually handles the page death regardless of busy-sleep.

Both versions work on Opera GX.

Firefox is not vulnerable at all.

### do...@gmail.com (2025-09-04)

What? Apparently you can upload files without finishing the captcha? But not send text?

Anyways, what I meant to say is:
Here's 2 videos showing each PoC in action and also a fixed `poc-redir` since I realised while recording that it had debug code I accidentally left in that would always send you to `https://example.com` and not the destination url.

### do...@gmail.com (2025-09-04)

Yeah I just checked and you can definitely upload files without any captcha, weird. Reportable? No clue.

No IDOR so it's not much of an issue but could probably be used to spam.

### dc...@chromium.org (2025-09-05)

Thank you for the report and the PoCs. For future reference, while a more elaborate PoC can be helpful for demonstrating a security impact, a barebones PoC can make things a bit easier to understand. I think there are two core issues reported here, but please let me know if there's something else I'm missing:

1. Navigating in `pagehide` is allowed (sometimes–more on this below).
2. Triggering navigation #1 and then immediately sleeping (blocking) means navigation #2 (in the same `ExecutionContext`) might trigger after navigation #1 has already committed. Navigation #1 should prevent navigation #2 from having an effect.

As-is, I'm not sure I'd consider this a security bug. However, I do think there's a lot of room for improvement, and I'd certainly consider this a functional bug: traditionally, we've tried to [prevent the unloading frame from navigating](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/loader/frame_loader.cc;l=1336;drc=e3ad182cacc3a02eb6a13091a867815fd17a129c), and bypassing that is not intended.

This happens because when navigating across documents, Chrome does not always wait for the old document to be unloaded before the new document commits–typically this happens when the navigation commits in a different renderer process (note: this is an implementation detail and not guaranteed to behave this way forever). So a lot of the behavior you're seeing is because of that–I don't recall exactly how long we give the old renderer process, but if there are other live frames, we probably won't forcefully terminate the renderer process to avoid sad frames. We also can't just completely detach all the browser-side infrastructure–the renderer's unload handler may have legitimate side effects (e.g. mutating localStorage) that we need to record.

Things to consider for fixes:

1. We need to do a better job disabling navigations when unloading the old document because a new document committed. This needs to be true of the entire frame tree for the old document.
2. We need to be careful about when we disable navigations; we cannot disable navigations permanently at `pagehide`, because the page might be reused–but maybe we should disable it until it's shown again
3. But even that won't help with the second issue above, as we never get to `pagehide`. It's probably more reliable to block browser-side and say if the document requesting the navigation (or any of its ancestors) are no longer the current `RenderFrameHost` in the `FrameTreeNode`, or the frame tree is no longer the primary frame tree, navigation should be disallowed. I'll look more tomorrow; perhaps there's a central point that can gate this check to avoid a (potentially endless) game of whack-a-mole.

That all being said... if you were able to demonstrate triggering a permission prompt for evil.com while example.com was already navigated-to and active, that might

### do...@gmail.com (2025-09-05)

We are not exactly navigating, we are traversing `history`. That is the entire core issue.

You can traverse `history` as long as you have a minimum amount of JS execution still allowed.

The listener PoC show's you can trigger it way past `pagehide`, and the redirection (programmatic) PoC shows that if you use a more deliberate version, you can keep access to a lot more of the window.

The page past `pagehide` should not able to survive that long and still be `BFCached`-that's not normal from what I understand, but chrome still allows it to go on. This is the main issue as far as I understand. `pagehide` should not be able to be stalled and should kill any executing JS before navigation finishes. Firefox handles it exactly like this.

Now, if the page is EXECUTING while in a `BFCache` state I don't know, because there's no indicator of the page already being in `BFCache` other than `pagehide.persisted`

When firing the `history.back()` it does return from `BFCache`, confirmed via Chrome devtools and my PoC accounts for it.

Post initial navigation to the next page: everything `async` breaks, microtasks do not fire (even immediate ones like `Promise.reject().catch()`) and all permission prompts I've tested so far auto-close or stop the rest of the code from executing (even without an `await`).

Modifying the `history` state will work.. once. It will set the state but not modify either URL (there will be no visible change, and going back will not set you at the new page URL) but the `history.state` will have saved. Trying to call a history function after modifying the state will stop JS execution entirely, without it throwing. No errors at all, very confusing.

You can pre-emptively kill the JS before it's time is up by spam-setting `location` over and over but the top page wont go anywhere as the entire `location` object is locked down at that state.

I will try some more tests.

### do...@gmail.com (2025-09-05)

Got the `navigator.mediaDevices.getDisplayMedia()` popup to open in the new page saying it is from `example.com` when it is actually running on the original page. Is this good enough? Will continue testing.

### do...@gmail.com (2025-09-05)

Found a way to crash the browser with `navigator.bluetooth.requestDevice();`.
Here's ASAN trace.

### do...@gmail.com (2025-09-05)

And if you call this right before navigation the UI stays open. But you can't go back because it causes a crash.

### do...@gmail.com (2025-09-05)

`PaymentRequest` gives an interesting error. "`UnknownError: Renderer process could not establish or lost IPC connection to the PaymentRequest service in the browser process.`". Could be worth noting.

While testing for `requestPictureInPicture()`, I got this error:
`Uncaught (in promise) AbortError: The play() request was interrupted because the containing page was frozen.` Which helps with my above theory I believe.

Those are all my notes. Biggest one is definitely `navigator.mediaDevices.getDisplayMedia()` working on the new page and saying the new page is the one requesting it.

### dc...@chromium.org (2025-09-05)

> We are not exactly navigating, we are traversing history. That is the entire core issue.

Traversing history **is** navigation.

Regular navigations likely don't succeed because they go through the NavigationClient, and we stop listening to the renderer's navigation client after committing a new document. But history navigations do not.

> Got the navigator.mediaDevices.getDisplayMedia() popup to open in the new page saying it is from example.com when it is actually running on the original page. Is this good enough? Will continue testing.

Good enough for me. Thanks!

### do...@gmail.com (2025-09-05)

It's navigation via BFCache, no? I was taking the more literal form of navigation as going to a new page.

Also, here are the bluetooth permission request crash and `getDisplayMedia()` popup PoC's with minimal stuff.

### do...@gmail.com (2025-09-05)

Oh wow, high severity, hell yeah.

### do...@gmail.com (2025-09-05)

So, out of curiosity, I see both Site Isolation and Navigation tagged in components.
Would this be considered Site isolation bypass or Security UI spoofing?

### do...@gmail.com (2025-09-05)

I don't know if it needs to be said or not, but the screenshare *IS* controlled by the original page, you can receive that data but only after forcing the victim back to the attacker page via `history.back()`.

The screenshare stays alive and any event handlers you assigned to it will start firing, so you can easily steal the screen if they accept.

Pushing it back to the safe page again after returning WILL kill the screenshare.

### dc...@chromium.org (2025-09-06)

I'm tentatively assigning to myself but only to make sure this has proper owners, as I don't work as much on navigation as I used to.

### dc...@chromium.org (2025-09-06)

> So, out of curiosity, I see both Site Isolation and Navigation tagged in components. Would this be considered Site isolation bypass or Security UI spoofing?

The components are just broad categorizations. For screensharing, I'd consider it UI spoofing, but that's just the opinion of one person: I don't know exactly how we'll end up classifying it, and we have some more systemic work to do outside the specific issues noted here in this bug. I suspect there will be a targeted fix for screenshare, but I'm also opening an umbrella bug to consider ways to handle the broader problem.

### dc...@chromium.org (2025-09-06)

tommi@, can you figure out a short-term fix for screenshare here? There are almost certainly more broken things and there's an umbrella bug for those, but this particular case is immediately problematic.

### dc...@chromium.org (2025-09-06)

I've filed [issue 443275589](https://issues.chromium.org/issues/443275589) for the Bluetooth crash as well. That one is non-security.

### do...@gmail.com (2025-09-06)

Could I get access to <https://issues.chromium.org/issues/443275589>?

### do...@gmail.com (2025-09-06)

I've been testing more and this issue seems a little worse than it does at first glance.

If you call `getDisplayMedia()`, then immediately go back, then start a timeout race with a ~15ms busy-sleep, you can get way more things to open on the unrelated page, while all the user see's is a flicker of the screenshare before the other thing is opened.

`getDisplayMedia()` seems to make it skip some sort of check, because it is necessary to make this work, and so is going back and immediately forward again.

Attaching video of another thing I was able to pop open and the PoC.

### do...@gmail.com (2025-09-06)

Some UIs like `print()` and `new PaymentRequest(...).show()` show up on the new page for split seconds but then die before rendering anything. Thought it's worth a note.

`navigator.credentials.store(...)` works fully and when exited out of and clicked again, it shows the URL as example.com in URL bar but localhost in the actual prompt.

Adding an event listener makes the File/Directory pickers and `navigator.share` work as well. They still require the `getDisplayMedia()` trick to work.

The `getDisplayMedia()` running in the original page DOESN'T work, as far as my testing went it seems it *needs* to run on the other page to trigger this behaviour.

### ch...@google.com (2025-09-06)

Setting milestone because of s0/s1 severity.

### do...@gmail.com (2025-09-06)

I might mention "window" instead of page quite a bit in these comments, my bad. I'll fix it where I notice it but please assume I mean the page either post or pre navigation and not that I'm talking about another window unless I explicitly say one is opened.

### do...@gmail.com (2025-09-06)

Would you say the much broader attack surface unlocked by calling `getDisplayMedia()` qualifies this issue for P0 priority/S0 severity?

As my comments above say and tests show, it seems that firing `getDisplayMedia()` in the cross-process document followed by `history.back()` and `history.forward()` consistently enables a broader range of UI to open from the stale document, including:

- `navigator.credentials.get()`
- `navigator.credentials.store()`
- File/directory pickers (via event listener)
- `navigator.share()` (via event listener)

These behaviors only occur reliably after the `getDisplayMedia()` call. Without it, these APIs never trigger their respective UI.

I'm not sure whether this is due to `getDisplayMedia()` changing some internal state or something, but based on current testing, it’s a required step for enabling this broader UI access from the stale document.

Additionally, it's possible to preemptively enter this state without any user interaction. Since `document.location` changes, `history` navigations or screenshare UI don’t require a gesture, the only required interaction, realistically, is the final user-gesture-based trigger if the attempted vector is one that requires an event listener. So the entire flow can be reduced to a single user gesture at most, and no user-interaction at all if they don't originally need an event listener to fire.

Given that:

- These permission UIs are being triggered from a no-longer-current document
- Several of the affected APIs involve sensitive user-trust UI

Would this now qualify for S0 severity, or is that typically reserved for a UXSS or sandbox escape? I believe P0 priority is strongly justified at this point due to the scope and user trust implications.

### do...@gmail.com (2025-09-07)

`Workers` can be spawned on the new page (after navigation, but their origin stays the original page) and continue running indefinitely without being frozen with no user interaction required. They remain alive even through further navigations, likely because there is no second freeze event applied to them (as the original page was already frozen in BFCache).

The only time they get frozen is if the user returns to the original page in history and then navigates away again at which point the browser seems to properly account for the `Worker` and suspend it.

This means an affected user ends up with a "parasite" Worker attached to their tab running in the background until they either return to the attacker's page or close the tab. Since it requires no user interaction and persists across navigations, this is pretty bad.

PoC attached, node-webhook attached in the original report above is necessary for this test as it will log the fetch pings.

### do...@gmail.com (2025-09-07)

That's probably a new issue now, should I file a separate report?

Impact-wise, at minimum this could be used to make an unknowing victim become a botnet node or cryptocurrency miner without any sign that anything wrong or malicious occurred. Considering this works across unlimited navigations as long as the tab is not closed, this is absolute madness.

Think of a scenario like this:

1. You open a shortened link.
2. The shortened link page flashes white for a split second before taking you where you needed to go.
3. You don't think anything of it and continue on with browsing, meanwhile, you have already been infected with the parasitic worker. Game over.

Here are some details that I think help make this qualify as S1:

1. It persists across cross-origin navigations indefinitely (until the tab is closed).
2. The original page is not kept alive and navigating away is actually required. Returning to that history entry cancels the persistence, but you can easily just boot up another worker once the user leaves again.
3. It’s a DedicatedWorker, and modern dedicated workers now have broad capabilities (WebSockets, Notifications, WebGPU, etc.), so compute + network + GPU are all in scope for the cryptominer or botnet scenario.
4. It has no restrictions on resource usage. I accidentally ran a while true loop in it and instead of killing the worker the browser froze.

All of these stem from a greater issue of unload not being fast or strict enough. If it'd be possible to lump all these together into one big report that could be S0 I would be grateful, otherwise I will file this one separately (that is, only if you decide that it should be considered a separate report when you respond).

### do...@gmail.com (2025-09-07)

Man it's almost 7am and I haven't slept. I'm testing the hell out of this stuff

### do...@gmail.com (2025-09-07)

I should also mention that these workers can access privileged APIs if their permissions were granted at the original page. So privileged work can run indefinitely. You can test it yourself with `new Notification()` in the original. Here's a paste-able replacement for `const code` that'll demonstrate this. Make sure the page has Notification permissions for this example.

```
const code = `
  let count = 0;
  setInterval(() => {
    count++;
    fetch("http://localhost:8080/test?ping=" + count, {
      method: "GET",
      keepalive: true
    }); new Notification(count);
  }, 5000);
`;

```

While `postMessage` dies, `IndexedDB` remains usable for transfer. This allows persisting objects such as FileHandle across navigation. The parasitic worker can retain full read/write access to user files (if originally given), even if the user clears site data, as long as File System Access permission remains at “Ask” or “Allow.”

This makes the persistence vector a confidentiality/integrity issue, not just resource abuse, since attackers could silently exfiltrate or tamper with local documents in the background until BFCache expiry.

### do...@gmail.com (2025-09-08)

Correction: I said "indefinitely", but after testing the worker (and confirming via <https://developer.chrome.com/docs/web-platform/bfcache-ccns> ) I can confirm that BFCache being deleted also deletes the worker. Meaning it goes from indefinite to 3-10 minutes, with 3 minutes being the "mitigated" version (no-store enabled).

### do...@gmail.com (2025-09-08)

Just realised the screensharing ALSO persists as you continue navigating, it just keeps showing "example.com".

### dc...@chromium.org (2025-09-08)

No need to file additional bugs; they would most likely be duped anyway. I've already created an umbrella bug to consider ways to more systemtically address this, as it's otherwise an infinite game of whack-a-mole :)

> Would you say the much broader attack surface unlocked by calling getDisplayMedia() qualifies this issue for P0 priority/S0 severity?

Probably not, as the bar for that is quite high. In the end, the label that's attached to this bug is just a guideline anyway, and VRP may not ultimately agree with the assessment.

### do...@gmail.com (2025-09-08)

What about the worker being able to survive in BFCache post-freeze with the origin's permissions?
I was pretty sure it's not getting S0, but P0 for a group of security issues stemming from one issue seems pretty appropriate

### do...@gmail.com (2025-09-08)

I should mention that unlike post-cache behaviour in windows, workers allow for full async execution via microtasks, so C2 communication would be two-way.

### fe...@chromium.org (2025-09-09)

@dc...@chromium.org is BFCache actually involved here or is all of this coming from the end-of-life events like pagehide/unload?

### do...@gmail.com (2025-09-09)

If it helps to know, most my current tests actually forcefully postpone pagehide with a blocking sleep to retain more access to APIs. This does also work in pagehide event handlers, but with less to work with. Both of them have the same execution post-navigation window of 3 seconds, no matter if you run it in a pagehide handler or postpone the pagehide for those 3 seconds.

A page that tries to postpone longer than 3 seconds will be immediately stop anything it got access to (like screenshare).

Workers are immune to this. My guess is workers are the first to be frozen post navigation, and so if one is spawned past the original worker freeze, it just continues running since there's nothing to freeze it. Then when BFCache gets remkved for getting too old (10 mins) it dies. Same thing with screenshare.

Also, remember, this allows for screenshare to persist across many navigations, up until BFCache finally gets removed.

### do...@gmail.com (2025-09-09)

Been testing a bit and encountered an interesting crash. I was unable to recreate it in ASAN (no crash occurs at all), so here is the WinDDB output. Will attach PoC. Seems to be safe, anyways.

```
(44c8.6264): Illegal instruction - code c000001d (first chance)
(44c8.6264): Illegal instruction - code c000001d (!!! second chance !!!)
chrome!CrashForExceptionInNonABICompliantCodeRange+0xabea03:
00007ffc`81057043 0f0b            ud2

```

Hopefully you guys are able to recreate it properly.
It occurs when a post-navigation worker is made using a non-local URL and then loaded from BFCache it seems. Occurs whether the fetch succeeds or fails.

I can recreate it on my stable build consistently.

For the PoC, just press navigate and wait.

### dc...@chromium.org (2025-09-09)

At this point, it's probably not adding much to find additional things–even the original report highlighted the flaw in this part of navigations, and there's already an umbrella bug tracking the long-term work for fixing the root cause. The screenshare issue demonstrates security impact. Additional bugs that are filed will just be duped into this (or the umbrella bug), since they are the same root cause; VRP will have any context they need from the discussions here and on the umbrella bug.

The umbrella bug is restricted for now, as it was filed in response to this bug and is more about planning how to mitigate this comprehensively rather than playing whack-a-mole.

@fe...@chromium.org I would say bfcache has some significance here, because it lets the screenshare example from [comment #13](https://issues.chromium.org/issues/442860743#comment13) above persist in unexpected ways. But as noted above, I'm not sure how we're going to address these issues comprehensively yet: the CSA folks will discuss it. I'll make sure we have good notes about this and figure out any followups needed.

### do...@gmail.com (2025-09-09)

I am just reporting anything significant I find because I don't see bugs with the same severity as you folks do. In my eyes, the worker is far more of an issue than screenshare, but apparently screenshare is actually more important.

I am hoping that eventually I find something that actually is more severe than the screenshare. Of course, you could just point me in the direction of what would be needed to make it considered more severe. (Or, are you saying it wont be treated as anything more severe even if a more severe issue is found?)

The crash above shows precedent that there could UAF's possible in this weird half-dead state, so I do think its worth continuing the search.

I also have nothing better to do and need to occupy my brain so it doesn't fry itself while waiting for responses.

### do...@gmail.com (2025-09-09)

How come this is still considered Unconfirmed? (Hotlists)

### do...@gmail.com (2025-09-11)

Any updates on this overall? Not part of the umbrella bug so I'm mainly in the dark on any developments and ideas.

### dc...@chromium.org (2025-09-11)

> I am hoping that eventually I find something that actually is more severe than the screenshare. Of course, you could just point me in the direction of what would be needed to make it considered more severe. (Or, are you saying it wont be treated as anything more severe even if a more severe issue is found?)

The severity guidelines are published here: <https://chromium.googlesource.com/chromium/src/+/main/docs/security/severity-guidelines.md>

> The crash above shows precedent that there could UAF's possible in this weird half-dead state, so I do think its worth continuing the search.

The crash is a `CHECK()` failure. The root cause of all the issues that have been mentioned here is clearly understood, and we also know that this can cause issues that have yet to be mentioned here; despite that, filing a bug for each and every thing that can go wrong is not going to be a useful contribution to a long-term fix.

> How come this is still considered Unconfirmed? (Hotlists)

There are many teams that use the bug tracker and they have their own hotlists/ways of tagging bugs. As far as the security is considered, this bug is triaged and being addressed.

> Any updates on this overall? Not part of the umbrella bug so I'm mainly in the dark on any developments and ideas.

Any updates for the bugs I've split out will be posted on those bugs (or here in the case of screenshare). As I've noted this above, there will be fixes for obviously wrong things, but the more comprehensive work is going to take longer. The priority and timelines for security bugs are also listed above, but that does not necessarily mean there's going to be a daily update on every bug–even for a high or critical severity bug.

### do...@gmail.com (2025-09-11)

Posting the screen-share PoC and demonstration videos as requested in [#444370596](https://issues.chromium.org/issues/444370596) here. These show that the screen can be recorded and do not just disturb the user.

I’m attaching them to this report since I no longer have access to the original report that requested them and would like a copy stored somewhere accessible remotely.

### do...@gmail.com (2025-09-18)

Out of curiosity, could I ask why triggering the screenshare popup allows more UIs to open? If you know the reason by now I mean. It's pretty strange and I'd love to know the cause.

### ch...@google.com (2025-09-20)

tommi: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### dx...@google.com (2025-09-24)

Project: chromium/src  

Branch:  main  

Author:  Elad Alon [eladalon@chromium.org](mailto:eladalon@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6976092>

DisplayMediaAccessHandler::HandleRequest() rejects on inactive RFH

---


Expand for full commit details
```
     
    Requests emanating from inactive RFHs, as can happen due to async 
    navigation, should be rejected. 
     
    Bug: 442860743 
    Change-Id: Ic3fbf7fcff764ee46e784886e610d2027d09246a 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6976092 
    Reviewed-by: Guido Urdaneta <guidou@chromium.org> 
    Commit-Queue: Elad Alon <eladalon@chromium.org> 
    Reviewed-by: Daniel Cheng <dcheng@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1519932}

```

---

Files:

- M `chrome/browser/media/webrtc/display_media_access_handler.cc`
- M `chrome/browser/media/webrtc/display_media_access_handler_unittest.cc`

---

Hash: [6be2b04353ed2e81e362f7fae0ab02f9fd568ce8](https://chromiumdash.appspot.com/commit/6be2b04353ed2e81e362f7fae0ab02f9fd568ce8)  

Date: Wed Sep 24 13:08:51 2025


---

### do...@gmail.com (2025-09-24)

awesome

### do...@gmail.com (2025-09-24)

Once `6966127` lands will this be marked fixed or will we wait for the other 5 private code changes to finish too?

### dx...@google.com (2025-09-25)

Project: chromium/src  

Branch:  main  

Author:  Elad Alon [eladalon@chromium.org](mailto:eladalon@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6966127>

Avoid propagating GenerateStreams from inactive RFHs

---


Expand for full commit details
```
     
    Soft-fail GenerateStreams() calls from RFHs that are no longer active, 
    as is the case when navigating. 
     
    This is the short-term fix. In the long-term, it's also important to 
    associate the GenerateStreams message with the RFH in the rest of the 
    pipeline, as the RFH might still asynchronously deactivate at a later 
    time that is still before the dialog is shown to the user. 
     
    Bug: 442860743 
    Change-Id: Iaf322eb151ee6e916a24dd10468b2f0426216ac1 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6966127 
    Commit-Queue: Elad Alon <eladalon@chromium.org> 
    Reviewed-by: Simon Hangl <simonha@google.com> 
    Reviewed-by: Guido Urdaneta <guidou@chromium.org> 
    Reviewed-by: Daniel Cheng <dcheng@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1520479}

```

---

Files:

- M `content/browser/renderer_host/media/media_stream_dispatcher_host.cc`
- M `content/browser/renderer_host/media/media_stream_dispatcher_host.h`
- M `content/browser/renderer_host/media/media_stream_dispatcher_host_unittest.cc`

---

Hash: [51cf4b9f857beaad802f6019792cc84f62337150](https://chromiumdash.appspot.com/commit/51cf4b9f857beaad802f6019792cc84f62337150)  

Date: Thu Sep 25 10:21:19 2025


---

### do...@gmail.com (2025-09-25)

Awesome

### do...@gmail.com (2025-09-25)

I'd appreciate an update from a human, haven't gotten one in 2 weeks..

### do...@gmail.com (2025-09-25)

Hell yeah

### el...@google.com (2025-09-25)

An audit of the relevant pipeline should still be done to ensure no races, and that the wrong RFH cannot still be used if the request ends up queued along the way. @to...@google.com, up to you to handle the relevant bug ([crbug/447172727](https://crbug.com/447172727)) and to prioritise this work as you see fit.

### ch...@google.com (2025-09-25)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### ch...@google.com (2025-09-25)

Dear owner, thanks for fixing this bug. We've reopened it because:

- Some CLs listed in the “Fixed By Code Changes” field are invalid and have been removed. Please provide an appropriate Gerrit url that matches the pattern: `https://<host>-review.googlesource.com/c/<repo>/+/<change_number>` or use the value 'NA' and re-mark this bug as fixed. If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### do...@gmail.com (2025-09-25)

All that's left is having this set with a hotlist `reward-topanel` and waiting for their response, right?

### el...@google.com (2025-09-25)

> All that's left is having this set with a hotlist reward-topanel and waiting for their response, right?

Sorry, I am not familiar with this part of the process. Hopefully @dc...@google.com is.

### ch...@google.com (2025-09-25)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M140. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M141. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [140, 141].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### el...@google.com (2025-09-25)

It's not 100% clear to me that this should be backmerged into m140 and m141 (but nor is it clear to me that it shouldn't). This issue has likely been around for quite some time and we are not presently aware of any abuse. Further, the fix - while it *looks* completely safe - is not gated by a feature flag, which IMHO would be a requirement for merging to stable. Shall we have some discussion before making this decision?

### ya...@chromium.org (2025-09-25)

Do both <https://crrev.com/c/6976092> and <https://crrev.com/c/6966127> require merging? After the more recent change has had a chance to bake on Canary for a bit, can you please answer the questionnaire answers, then we can see if a merge would be appropriate. Thanks!

### dc...@chromium.org (2025-09-25)

> I'd appreciate an update from a human, haven't gotten one in 2 weeks..

The bug will get updates when there are relevant updates. You're not getting replies because it's not the place to ask questions about code specifics or to discuss design.

> All that's left is having this set with a hotlist reward-topanel and waiting for their response, right?

You can see one specific example of how it might work here: <https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#an-example>
But please do not assume that everything will work exactly as documented in that example.

### el...@google.com (2025-09-25)

@ya...@chromium.org, please see [comment #60](https://issues.chromium.org/issues/442860743#comment60) - I am not, personally, of the opinion that this needs to be merged.

### sr...@google.com (2025-09-26)

We have already cut stable RC for desktop release and taking only P0 bugs that would block stable promotion to 100%, if any of your bugs meet this criteria please reach out to me asap, if not we will consider these merge requests for first respin in week of oct 7

### el...@google.com (2025-09-29)

I leave it to the security people to decide whether this should be cherry-picked or not.

### ts...@google.com (2025-09-30)

Let's target 142 with this one, rather than a respin next week. Thanks.

### ch...@google.com (2025-09-30)

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: alonbajayo (ChromeOS), srinivassista (Desktop US), danielyip (Desktop EMEA), harrysouders (Mobile US), eakpobaro (Mobile EMEA)

### ch...@google.com (2025-09-30)

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: lmenezes (ChromeOS), srinivassista (Desktop US), danielyip (Desktop EMEA), govind (Mobile US), eakpobaro (Mobile EMEA)

### do...@gmail.com (2025-10-02)

Nice.

### ch...@google.com (2025-10-06)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### sp...@google.com (2025-10-07)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $10000.00 for this report.

Rationale for this decision:
High Quality && High Impact UI spoofing


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### do...@gmail.com (2025-10-07)

HELL YEAH!! THANK YOU!

### ch...@google.com (2025-10-10)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### go...@google.com (2025-10-20)

[Bulk Edit]
Please merge your change to M142 by 4:00 PM PT today, M142 Early Stable RC cut tomorrow morning PT. Thank you. 

### go...@google.com (2025-10-21)

Both changes listed at #61 landed before M142 branch on Sept 29th, no merge needed here

 https://crrev.com/c/6976092 and https://crrev.com/c/6966127 

@srinivas FYI

### ch...@google.com (2025-10-29)

This V8 bug has been marked as either a release blocker or a vulnerability bug. V8 bugs affect all OSs supported by Chrome, so the OS field has been updated to reflect this. Please update the bug with the correct OS field if it only affects a subset of OSes.

### ch...@google.com (2026-01-02)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> High Quality && High Impact UI spoofing

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/442860743)*
