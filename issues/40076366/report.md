# Security: Screenshot theft using WebGL

| Field | Value |
|-------|-------|
| **Issue ID** | [40076366](https://issues.chromium.org/issues/40076366) |
| **Status** | Assigned |
| **Severity** | Unknown |
| **Priority** | P2 |
| **Component** | Internals, Internals>GPU |
| **Platforms** | Mac |
| **Reporter** | dr...@gmail.com |
| **Assignee** | zm...@chromium.org |
| **Created** | 2012-09-27 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**

Using a WebGL canvas, one can get a partial screenshot of the whole computer scene, including (sometimes) areas outside/behind of the browser window, and including area from a different tab if that other tab also uses WebGL.

**VERSION**

Chrome Versions  

\*22.0.1229.91 (Beta)  

\*22.0.1229.79 (Stable)

Operating System:

Mac OS X, 10.7.5

**REPRODUCTION CASE**

To reproduce:

1. Download webgl.html and the associated JavaScript files (see attached)
2. Open webgl.html
3. In another tab, open the webpage <http://mrdoob.com/projects/glsl_sandbox/>
4. From this other tab, go fullscreen, and then exit fullscreen
5. Revisit the webgl.html tab
6. Notice that the canvas is replaced with a "garbage" image, which actually are 16 px high, translated, and reflected slices of the screen real-estate. The content usually includes content from the GLSL sandbox tab, and content outside the browser window.
7. It's possible to capture the garbage canvas image by opening the JavaScript console and typing "toImage()".
8. I've added an example for which I wrote a simple Python script to "recreate" a partial screenshot out of the garbage canvas image.

## Attachments

- [recreated.png](attachments/recreated.png) (image/png; charset=binary, 51.3 KB)
- [WebGL repro.zip](attachments/WebGL repro.zip) (application/zip; charset=binary, 39.6 KB)
- [garbage.png](attachments/garbage.png) (image/png; charset=binary, 58.3 KB)
- [other_example.png](attachments/other_example.png) (image/png; charset=binary, 275.8 KB)
- [chrome   gpu.html](attachments/chrome   gpu.html) (text/html; charset=us-ascii, 27.8 KB)
- [lesson05.zip](attachments/lesson05.zip) (application/zip; charset=binary, 63.0 KB)
- [WebGL.zip](attachments/WebGL.zip) (application/zip; charset=binary, 44.3 KB)
- [earth.zip](attachments/earth.zip) (application/zip; charset=binary, 528.9 KB)
- [Screen Shot 2012-10-23 at 6.40.34 PM.png](attachments/Screen Shot 2012-10-23 at 6.40.34 PM.png) (image/png; charset=binary, 208.4 KB)

## Timeline

### dr...@gmail.com (2012-09-27)

Here's another example, which is more representative of what usually happens.

### sc...@gmail.com (2012-09-27)

Thanks. This sounds interesting. I don't suppose you have a feel for whether it is Mac specific?

cc: Ken Russell

### kb...@chromium.org (2012-09-27)

I noticed similar behavior yesterday with the test case from https://crbug.com/chromium/152140, but didn't have time yet to investigate what was going on. That other test case displays garbage even without going full-screen and back. It wasn't apparent to me whether the garbage could be read back.

CC'ing a few other people. It'll be a couple of days before I can start investigating this.


### dr...@gmail.com (2012-09-27)

@scary: I have no idea. That the issue doesn't require the native full-screen functionality on other examples suggests that it's probably not Mac specific.

### kb...@chromium.org (2012-09-27)

Actually I suspect it is Mac-specific but I haven't had a chance to try the repro cases on other OSs yet.


### [Deleted User] (2012-09-27)

I've tried on Win 7 and don't see anything strange. I'll mark it OS-Mac unless someone is seeing this elsewhere.

### sc...@gmail.com (2012-09-28)

Ken, you seem to be the expert at spelunking into Apple driver badness. Let us know if there's something we can do or if this just needs reporting to Apple.

### kb...@chromium.org (2012-09-28)

I'll investigate as soon as possible.


### kb...@chromium.org (2012-10-02)

zmo offered to investigate this while I'm dealing with yet another P0 bug.


### zm...@chromium.org (2012-10-02)

drakefjustin: can you provide the about:gpu page content from the Mac where you can reproduce this?

### dr...@gmail.com (2012-10-03)

@zmo: Please see attached. I can reproduce in stable, dev and canary.

### zm...@chromium.org (2012-10-03)

I can reproduce this reliably on a dual GPU mac on 10.7.5.

When running on the integrated Intel GPU, everything works fine; but if we run on the NVIDIA GeForce GT 330M, then we see the corrupted rendering.

So it seems more like a Apple driver issue.  I am digging further to understand the bug better.

### zm...@chromium.org (2012-10-03)

Can't reproduce this on Macbook retina (also dual GPU with NVIDIA/Intel), neither 10.7.5 nor 10.8.2

### zm...@chromium.org (2012-10-03)

Interestingly, I rebooted my mac, and now I can't reproduce it any more.

kbr is investigating another corrupted rendering issues: we got garbage rendering after MacOSX upgrade, then if rebooting (once, for some people more than once), the issue disappears.

I suspect if here we are hitting the same Apple driver bug.

drakefjustin: can you restart your Mac, and see if you can still reproduce this?

### pa...@chromium.org (2012-10-04)

Can't reproduce this on MacBook Air, NVIDIA GeForce 320M, OS X 10.8.2.

### dr...@gmail.com (2012-10-04)

I've rebooted my computer, checked that there are no pending updates, and I can *still* reproduce the problem with 100% reliability. Here are more precise steps I use to reproduce the problem:

1) Open webgl.html
2) Open GLSL Sandbox in a different tab
3) Go full-screen from the GLSL Sandbox tab
4) Exit full-screen
5) Go to the webgl.html tab
6) Open the JavaScript console and type "toImage()" + Enter
7) After pressing Enter, you will have captured the garbage image encoded as a dataURL. Most of time, the garbage image will also appear in the canvas.
8) (Optional) If the garbage image does not appear, scroll the webgl.html page a little to "update" the canvas with the garbage image.

### pa...@chromium.org (2012-10-04)

I can reproduce using the new instructions on the MBA GeForce 320M. I have to do step 8.

### zm...@chromium.org (2012-10-04)

drakefjustin, palmer: can you run chrome with --disable-gl-multisampling, and check about:gpu page and make sure multisampling is turned off, then see if you can still reproduce the bug.

### pa...@chromium.org (2012-10-04)

With multisampling disabled (verified in about:gpu), I cannot reproduce the bug.

### dr...@gmail.com (2012-10-05)

zmo: Same here. With multisampling disabled, I cannot reproduce.

### dr...@gmail.com (2012-10-15)

Any progress on this? For a high severity security Chrome issue this is taking a lot of time.

### js...@chromium.org (2012-10-15)

@palmer - Why was this flagged as SecSeverity-High in the first place? It looks like an unreliable leakage of partial screen state. That doesn't seem to warrant anything higher than SecSeverity-Medium at worst.

### pa...@chromium.org (2012-10-15)

I was reading this with maximum caution: http://www.chromium.org/developers/severity-guidelines

"""high severity if the vulnerability lets an attacker read or modify confidential data belonging to other web sites."""

Especially if the malicious page is sitting in the background and can take multiple partial screenshots, it could be a bad attack. In any case it seems worse to me than

"""medium severity if the vulnerability lets an attacker obtain only limited amounts or kinds of information.  For example, an issue that lets the attacker enumerate recently visited URLs"""

This isn't super-reliable (but could the attack be improved?), and it's only partial screens (improvable?), but it's definitely more than just URLs.

### js...@chromium.org (2012-10-15)

Compare this to https://crbug.com/chromium/39861, which was a full image theft across origins. Whereas for this bug you have unreliability and little to no control over what's in the canvas buffer. So, I think we're still exercising an abundance of caution if we rate this at medium.

### sc...@gmail.com (2012-10-16)

@drakefjustin: sorry that it's taking a while. One reason is that it's probably an Apple issue (their GPU drivers seem particularly buggy), but getting to that determination is tricky.

@jschuh: I'm not sure https://crbug.com/chromium/39861 can be readily compared. The web doesn't really have much in the terms of sensitive, cookie-authenticated <img> resources at predicatable URL locations, so https://crbug.com/chromium/39861 is defensibly Medium. This bug, by contrast, looks like it might leak the result of HTML rendering, which might include Gmail inbox contents, etc.

### js...@chromium.org (2012-10-16)

@scarybeasts - It's leaking random, partial image buffer data; it requires an unusual privileged action; it requires a specific hardware/driver configuration (really pointing to a bug outside Chrome). My take is that the bug is so narrow and of such little utility from an attack perspective that I worry medium-sevirty is inflated, but I figured I'd air on the side of caution.

### sc...@gmail.com (2012-10-16)

Yeah, I agree that the long sequence of steps is sufficiently mitigating to downgrade to at least medium.

I was just noting that the pixels stolen here seem more sensitive than pixels from an <img> tag.

### dr...@gmail.com (2012-10-16)

I have been able to improve this bug to take a different partial screenshot (potentially sent to a malicious website) every second (say) without any special user interaction (such as going fullscreen). This is high priority in my opinion.

### sc...@gmail.com (2012-10-16)

@zmo: is this our fault or Apple's fault?

### gm...@chromium.org (2012-10-16)

drakefjustin, can you post the sample that doesn't require user interaction? That would be really helpful.

### gm...@chromium.org (2012-10-16)

drakefjustin, can you post the sample that doesn't require user interaction? That would be really helpful.

### dr...@gmail.com (2012-10-16)

@gman: The trick involves two canvases in the same page, and periodically reloading the page. You will see that the left canvas in my example often captures garbage, but I'm not sure if it can be captured. Anyway, the right canvas also produces garbage that for sure can be captured.

To reproduce, open my example on one window. Now open this webgl intensive page (http://jeromeetienne.github.com/tquery/plugins/car/examples/) in another window.

You should start seeing garbage frames coming in bursts. This is exacerbated by playing around with the webgl intesensive page. In particular, a simple resize generates with 100% reliability a grabable garbage frame.

Now this took me less than half an hour to cook up, and I expect that by carefully crafting the WebGL attack code with many canvases and/or larger canvases and/or complex shaders, or whatever, one would be able to deeply exploit this bug.

(BTW, I'm hoping this bug qualifies for the reward scheme as describe here: http://blog.chromium.org/2012/08/chromium-vulnerability-rewards-program.html. If so I'd be happy to put in a bit more work if required.)

### dr...@gmail.com (2012-10-16)

And the attached example...

### zm...@chromium.org (2012-10-23)

bajones confirmed this is a driver bug with NVIDIA chipset on Mac.

As confirmed earlier, disabling multisampling works around this bug, so that's what we will do until Apple releases a fix.

### zm...@chromium.org (2012-10-23)

SImple test case to reproduce this corruption (not vram pressured at all):

launch chrome with --allow-file-access-from-files

open earth.htm
switch to a new tab, open WebGL.html
switch back to the earth tab, go full screen
exit full screen mode
switch to WebGL tab
open js console, type toImage(), which triggers a multiplesampled buffer blit

See corrupted rendering on screen

### sc...@gmail.com (2012-10-24)

[Empty comment from Monorail migration]

### kb...@chromium.org (2012-10-24)

For what it's worth: Safari is affected in the same way as Chrome.


### kb...@chromium.org (2012-10-24)

[Empty comment from Monorail migration]

### dr...@gmail.com (2012-11-07)

So I'm not getting any reward for this?

### sc...@gmail.com (2012-11-07)

@drakefjustin: the status is still "reward-topanel", which means that this is a clear candidate for reward but the panel has not discussed the case. This will typically happen once the bug is fixed -- or in this case, worked around. I'll ping the base bug to see what the status is.

### sc...@gmail.com (2012-11-07)

Yeah, looks like we have a fix. We'll consider reward shortly, and get the fix merged into a M23 patch.

### sc...@gmail.com (2012-11-12)

@drakefjustin: ok! So the rewards panel decided that your report did cause us to push security usefully forward by working around the Apple driver vulnerability.

We'll be merging the workaround to the next stable patch of Chrome.

For your help, we're happy to be rewarding you a $1000 Chromium Security Reward. Congrats!

----
Boilerplate text:
Please do NOT publicly disclose details until a fix has been released to all our
users. Early public disclosure may cancel the provisional reward.
Also, please be considerate about disclosure when the bug affects a core library
that may be used by other products.
Please do NOT share this information with third parties who are not directly
involved in fixing the bug. Doing so may cancel the provisional reward.
Please be honest if you have already disclosed anything publicly or to third parties.
----

### sc...@gmail.com (2012-11-12)

@drakefjustin: also, would you like us to credit you by name? What's the correct name?

### dr...@gmail.com (2012-11-12)

@ scarybeasts: Thanks! I'm glad this report led to mitigations taking place. Sure, I would be happy to be credited by name. "Justin Drake" is fine.

### sc...@gmail.com (2012-12-18)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### js...@chromium.org (2013-11-18)

Bulk release of old security bug reports.


### sh...@chromium.org (2016-06-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/152746?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Internals, Internals>GPU]
[Monorail mergedinto: crbug.com/chromium/137303]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40076366)*
