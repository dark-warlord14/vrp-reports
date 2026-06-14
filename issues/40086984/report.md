# Security: Canvas composite operations and CSS blend modes leak cross-origin data via timing attacks.

| Field | Value |
|-------|-------|
| **Issue ID** | [40086984](https://issues.chromium.org/issues/40086984) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Skia, Privacy |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | pe...@gmail.com |
| **Assignee** | ch...@chromium.org |
| **Created** | 2017-03-07 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

Many of the operations supported by CanvasRenderingContext2D.globalCompositeOperation and the CSS mix-blend-mode property take varying lengths of time to complete depending on the contents of the source and destination images. This allows an attacker to infer the contents of a cross-origin image or even an arbitrary HTML element, such as an iframe.

An attacker may read the pixels of a cross-origin image by following these steps:

1. Render a single pixel from the image onto a canvas.
2. Manipulate the canvas so that it may be in one of two states depending on whether that pixel's color has certain properties.
3. Time how long it takes to render the contents of the canvas, scaled up, onto another canvas with a globalCompositeOperation chosen to maximize the difference in timing between those two states.
4. Based on whether the operation from step 3 completed quickly or slowly, it can be determined whether the pixel's color has the properties selected for in step 2.
5. Return to step 1.

Reading the pixels from an HTML element is slower and slightly more complex but, in my experience, no less reliable. This paper from 2013 details a similar exploit targeting SVG filters: <https://www.contextis.com//documents/2/Browser_Timing_Attacks.pdf>

The basic procedure when targeting mix-blend-mode is as follows:

1. By applying the feColorMatrix filter to an HTML element, select a single pixel from that element and turn it red or black depending on whether one of its channels has a value greater than a certain threshold.
2. By applying the feTile filter to the previous filter's result, blow up that single pixel of red or black to take up a large area of the screen.
3. Layer many rectangular elements with random background colors and `mix-blend-mode: saturation` on top of the filtered element.
4. Call requestAnimationFrame. When the browser is finished rendering the changes that have just been made, it will call a callback, which will be able to determine how long the render took.
5. Based on whether the render completed quickly or slowly, it can be determined whether the selected channel of the selected pixel is greater than the selected threshold.
6. Return to step 1.

**VERSION**  

Chrome Version: Chromium 56.0.2924.87 stable (64-bit)  

Operating System: Arch Linux. /proc/version: Linux version 4.9.11-1-ARCH (builduser@heftig-11715) (gcc version 6.3.1 20170109 (GCC) ) #1 SMP PREEMPT Sun Feb 19 13:45:52 UTC 2017

**REPRODUCTION CASE**  

"Minimized" reproduction cases for the globalCompositeOperation attack and the mix-blend-mode attack are in the first and second attachments, respectively. Just open them up and check the console output (after waiting a while, that is, potentially a long while in the case of the second one). You can have the devtools open, but don't open or close them while the exploits are running. You may have to serve them from a local Web server to get them to work.

While developing the exploit, I used an interface I'd built to make it easier to see how well it was working. A cleaned-up version of this interface is in the third attachment. If the first two don't seem to work for you, I recommend trying the third. Have fun with it. I actually wrote the JavaScript for it in ES6 module format and bundled it using a tool called Rollup, so look in the fourth attachment for the individual source files, which should be easier to navigate.

I tried to minimize the reproduction cases as much as possible without sacrificing the code's clarity, but it's a timing attack, which makes it a rather high-level bug, so I figured you're probably not going to be running it under gdb or anything. I hope it's in a good state to analyze.

Timing is fickle, so the exploit may or may not work on your system. In particular, my current implementation of the mix-blend-mode attack doesn't work on my Windows machine. Both exploits do work on my Android phone, however. I doubt there are any platforms that can't be targeted by both exploits with the proper tuning.

## Attachments

- [globalCompositeOperation.html](attachments/globalCompositeOperation.html) (text/plain, 7.3 KB)
- [mix-blend-mode.html](attachments/mix-blend-mode.html) (text/plain, 10.6 KB)
- [interface.zip](attachments/interface.zip) (application/octet-stream, 610.6 KB)
- [interface-source.zip](attachments/interface-source.zip) (application/octet-stream, 14.2 KB)

## Timeline

### pe...@gmail.com (2017-03-07)

See <https://drafts.fxtf.org/compositing-1/#security>. If browsers just followed the rule mentioned there, they wouldn't be vulnerable to this attack.

I think the fact that none of the browsers I've tested heed that section's warning suggests that browsers need to change their approach to mitigating timing attacks. There's a lot resting on the assumption that the pixels shown to the user aren't accessible to an attacker, but that assumption has been violated a number of times over the past four years by very similar attacks.

The solution in the past has been to modify the algorithms in question so that their timing appears to be independent of input, but as Paul Stone, the reporter of the 2013 exploit I linked to previously, wrote in a Bugzilla comment <https://bugzilla.mozilla.org/show_bug.cgi?id=711043#c5>:

> Beyond the source code, there's also things like compiler optimisations and the CPU cache that could affect timings in non-obvious ways.

An example of an attack that targeted differences in timing on the CPU level can be found here: <https://bugs.chromium.org/p/chromium/issues/detail?id=615851>

That attack was also patched, but there isn't much one can do to be certain that there aren't others like it still open, because at the end of the day, the C++ specification simply doesn't make any guarantees about the exact timing properties of a given function. Browsers are putting their carefully specified cross-origin security restrictions squarely in the hands of unspecified underlying behavior. And that's to say nothing of exploits like the one this bug report is actually about—looking at the affected Skia code, it doesn't seem to have even been considered as a potential attack vector.

Timing attacks are a sticky and unpleasant class of bug, which makes it important to have a structured approach to dealing with them. If there's a protocol and an infrastructure for them, it will be easier to keep them in mind as a risk when developing new features.

Timing attacks aren't new, and there's a fair amount of research into preventative measures. Rather than modifying the algorithm to appear to take a consistent amount of time, which is difficult and unreliable, these measures tend to involve padding the sensitive operations by sleeping after performing them. (This has the additional benefits of saving battery power and freeing up system resources, two things which as far as I know aren't viable side-channels in the case of browsers.)

In order for this strategy to work, an upper bound on time taken must be known—that's the hard part. However, by their performance-sensitive nature, rendering operations have the advantage of not taking potentially unbounded time based on sensitive information, which makes completely covering up those timing differences a bit less impossible.

The key is to understand that it's perfectly safe for the time taken to vary based on information the page's JavaScript already has access to. As a simple heuristic for calculating an upper bound on time, the renderer may time how long it takes to render a single pixel using the chosen filter/composite operation/etc, choosing a color that it expects to represent the worst case for that operation (possibly repeating the process with multiple colors and choosing the one that takes the longest), then multiply the time taken by the number of pixels being rendered.

A page's JavaScript is also, as far as I know, capable of determining which rendering operations involve data it doesn't have access to. An intelligent renderer could therefore distinguish between sensitive and non-sensitive rendering operations and pad out only the sensitive ones. Since these will likely make up a rather small subset of all rendering operations, and since Web pages will be perfectly capable of avoiding expensive operations on sensitive data if they know to do so, the impact on browser performance can be kept quite low.

The strategy I've just described still isn't guaranteed to work by any specification, of course, and still isn't a sure thing. But it would be a big step up from the way these sorts of vulnerabilities are currently handled.

That's my opinion on the matter of how best to address this bug, if you care for it, and I hope I'm not out of line. My SAT date is coming up, and this has been a rather draining project, so I probably won't be working on the PoC any more this week. I'll try to take my part in any discussion that may come up during that time, however.

### pe...@gmail.com (2017-03-07)

For the record, the console output for globalCompositeOperation.html is supposed to look like this:

> The pixel at (10, 10) does not have a r value greater than 0.5.
> The pixel at (14, 14) does have a r value greater than 0.5.

And the console output for mix-blend-mode.html is supposed to look like this:

> The pixel at (1, 1) does have a r value greater than 0.99.
> The pixel at (1, 100) does not have a r value greater than 0.99.

I probably should have made those things more obvious. mix-blend-mode.html loads Wikipedia in an iframe, so if it doesn't work, it may just be because that iframe isn't loading.

### el...@chromium.org (2017-03-07)

Summary: A Timing attack can be used to infer the content of a cross-origin image, circumventing the canvas object's usual protections against extracting contents "tainted" by cross-origin images. 

I haven't yet validated the repro (it sounds non-trivial) but based on our severity guidelines this is probably somewhere between a Low and Medium depending on reliability.

[Monorail components: Blink>Canvas Internals>GPU>Canvas2D]

### pe...@gmail.com (2017-03-07)

The globalCompositeOperation exploit does as you described, but the mix-blend-mode exploit can be used to read pixels from arbitrary HTML elements, such as iframes, and links with :visited styling. I think that makes it a bit more concerning.

The globalCompositeOperation exploit does have the advantages of higher throughput and greater ability to fly under the radar compared to the mix-blend-mode one, however.

### pe...@gmail.com (2017-03-08)

I submitted the two exploits as a single bug because they target the same properties of the same Skia code, but they do use entirely separate Web features, so splitting them up would be reasonable if that's what you think is best.

### sh...@chromium.org (2017-03-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-03-08)

[Empty comment from Monorail migration]

### pe...@gmail.com (2017-03-10)

Sorry, but can I get an acknowledgement of the clarification I made in https://crbug.com/chromium/699028#c4, please? It's not like I expect someone to come along to fix the bug instantly, but I think it's important that its scope is understood, at least.

### el...@chromium.org (2017-03-13)

reed@ can you please take a look at this? The basic repro does appear to work on my Win10 desktop, but it's not at all clear to me which team should own this going forward.

I haven't extensively validated the repro; a logical extension might be to iterate over each of the target pixels to try to reconstruct an "echo" of the image to verify the technique at a larger scale.

thanks!

### sl...@google.com (2017-03-13)

[Empty comment from Monorail migration]

[Monorail components: Internals>Skia]

### el...@chromium.org (2017-03-13)

Updating assignment based on previous request to Sheriffs.

### hc...@chromium.org (2017-03-13)

Interesting find-

These exploits likely need to be addressed in the Canvas2D and Blink filter code. Probably different code owners, but perhaps we should continue shared discussion here before forking.

Start w/ juno, stephen, florin for thoughts

[Monorail components: Blink>CSS>Filters]

### se...@chromium.org (2017-03-13)

Looks like the problematic branches in this case are in SetSat() and setSaturationComponents(). Switching to branchless SSE/NEON versions would probably likely fix it, and give a speed boost.

### ju...@chromium.org (2017-03-13)

Regarding the canvas-based attack: I think moving more canvas use cases towards the "display list" and GPU-accelerated code paths will impede timing-based attacks because these code paths are asynchronous. Currently, this attack will only work when the canvas is in software rendering mode. With the current heuristics we have in Chrome, an attacker can force a 2D canvas of any size into software rendering mode by calling getImageData (which necessarily forces a synchronous render). Bottom line is, we only need to fix the software rendering code path.

In the event that the branchless versions of the ops are significantly slower, then we could have a flag to only use the branchless versions in the render process, or something like that.

### pe...@gmail.com (2017-03-13)

> a logical extension might be to iterate over each of the target pixels to try to reconstruct an "echo" of the image to verify the technique at a larger scale.

That's what the third attachment does. It can reconstruct a cross-origin image quickly or an arbitrary HTML element slowly. It will give you options for "arena width", "arena height", and sometimes "layer count"—increasing these will improve accuracy at the cost of speed.

### el...@chromium.org (2017-03-14)

[Empty comment from Monorail migration]

### el...@chromium.org (2017-03-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-03-14)

[Empty comment from Monorail migration]

### sl...@google.com (2017-03-16)

[Empty comment from Monorail migration]

### ju...@chromium.org (2017-03-22)

@reed: Someone on the skia team should look into this, not sure who. It is probably mostly a matter of replacing current blend op implementations in the skia raster code path with branchless versions.

### sh...@chromium.org (2017-03-23)

reed: Uh oh! This issue still open and hasn't been updated in the last 16 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2017-03-23)

I suggest we have a VC to discuss this. Given https://crbug.com/chromium/699028#c1, I'm not sure that trying to modify all of the (growing) number of implementation paths in Skia will be reliable (and runs the risk of slowing everyone down). #1 suggests alternate approaches "up-stack", such has discrete delays at the JS level iff it is known that we are reading cross-domain.

### hc...@chromium.org (2017-03-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-04-07)

reed: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2017-04-20)

[Empty comment from Monorail migration]

### aa...@google.com (2017-05-01)

Heather is planning to start discussions on this.

I can reproduce both the repros fine. So, we should see if we can fix this or workaround to make the attack not work in short team.

### [Deleted User] (2017-05-02)

[Empty comment from Monorail migration]

### [Deleted User] (2017-05-02)

[Empty comment from Monorail migration]

### hc...@chromium.org (2017-05-02)

Chromies didn't end up joining the meeting (unintentionally), but we had a lot of discussion around the significant perf (and correctness) costs that clients would incur if we tried to fix this timing in the many paths in Skia.  It is also something that the browser will encounter vs other clients.  We think the browser may be in best position to detect and mitigate, vs us slowing everyone down significantly, so we're hoping that there is an easy solution Chrome-side.  I'll let Florin, Mike etc chime in with additional comments if they have them...

### ju...@chromium.org (2017-05-02)

Past experience (CL by senorblanco) has been that fixing this type of issue actually boosts performance.
The approach was to write a SIMD-optimized version of the op that replaces the conditional branch with a NEON or SSE conditional assignment instruction.


### [Deleted User] (2017-05-02)

Right, that's the approach I find a little confused.  It is true that vectorized code is often faster, and it is more challenging to branch usefully in vectorized code, but it is certainly not correct to think that vectorizing code makes it run in constant time.  We regularly branch inside vectorized code to improve drawing performance.

We want to be able to improve performance or correctness of routines in Skia independently of security.  We're not convinced that patching each of these timing attacks as they come up in Skia is maintainable.  This doesn't happen too often so we're willing to flex a little, but bandaids absolutely cannot be the correct global approach to solving this problem.

### ju...@chromium.org (2017-05-02)

> it is certainly not correct to think that vectorizing code makes it run in constant time. 

Even when conditional branches are removed?

### [Deleted User] (2017-05-02)

Yes, branches are one of several ways you can make code run in non-constant time.  There several other ways too.  Value dependent runtimes are the most obvious, where the same operation takes variable time depending on the input values.  Denormal floats are the most obvious (because they're they exhibit the most slowdown) but it's not hard to demonstrate outside denormals, and probably outside floats.

There is nothing fundamentally connecting vectorization with constant time code.  
Vectorization is simply more challenging to branch effectively with.  You can write constant time serial code.  You can write non-constant time vector code.  All 4 pairs are possible, and I'd wager there are examples of all 4 in Skia.

### se...@chromium.org (2017-05-02)

Really sorry I missed the meeting.

As Justin says, I've been able to sell previous constant-time fixes as also performance wins, although that may not always be the case. If we could find such 
a fix here, that would be ideal IMHO.

robertphillips@ had the interesting suggestion of a "constant-time fuzzer": something which tests execution time of certain code paths to ensure that they have the constant-time execution independent of input. If we could do that, we could at least avoid the current whack-a-mole approach and avoid regressions, regardless of where the fix ends up.

I feel that adding a sleep() at the Blink level is a non-starter: the value used would have be platform-dependent, and have to be necessarily pessimistic and platform-dependent. Either that or we start adding separately-tweaked values for each code path in Skia which is known to be non-constant-time, with different values for each platform. (This seems seems difficult to maintain. Correct me if I'm missing something.)

I commend the commitment to performance, but if a major client cannot use the top-performing code path anyway, due to security concerns, or the performance has to be deliberately handicapped by a higher-level sleep, have we optimized for the correct thing?

### ju...@chromium.org (2017-05-02)

So you are saying that making setSaturationComponents and setSat run in constant time is not feasible?  Even if we don't make them perfectly constant time, it just needs to be close enough to make this exploit fail.

### [Deleted User] (2017-05-02)

The point we're trying to make here is that this is a browser-only problem and we would like the browser to solve it.  We're not eager to have to maintain separate code paths for Chrome and all the other users of Skia, or to have to weigh Chrome's security needs against their performance needs.

### fm...@chromium.org (2017-05-02)

Stephen, Justin: the concern is we're playing whack-a-mole by trying to address this in Skia; even if we can make saturation constant-time AND faster, there's a bunch of other code paths which are not const time and could potentially be probed in a similar manner.

So the question is whether there is a systemic fix we can effect in Chrome, to thwart this whole class of attacks.  AFAIU, two key ingredients are a) cross-origin content and b) accurate timing.  Unlike Skia, the browser seems well positioned to detect when C/O content is used in a sensitive way, and intervene in some manner.

### [Deleted User] (2017-05-02)

Yeah, sorry if I wasn't clear or seemed off-topic in those last posts... by "this problem" I mean the overall one of how to make drawing timing attacks impossible, not this particular issue with the saturation blend mode.

### pe...@gmail.com (2017-05-02)

I definitely think this vulnerability should be addressed at the browser level, but if it's done in a manner similar to the one I suggested (sleeping up to a supposed worst-case time based on a heuristic), it may be better implemented as a Skia feature that Blink turns on or off based on whether it's dealing with cross-origin data. This brings the heuristic closer to the algorithm whose performance it approximates, and it allows other security-sensitive applications using Skia (such as Firefox!) to benefit from the fix as well.

### hc...@google.com (2017-05-15)

Moving myself to cc while this is continued to be discussed, I'm not sure who/how browser wants to address...

### [Deleted User] (2017-05-15)

For what it's worth, I've landed some new implementations of these blend modes that do not branch based on pixel values.  They don't, however, do anything to protect against other data-dependent timing attacks like denorm values.

The relevant code starts right around here: 
https://cs.chromium.org/chromium/src/third_party/skia/src/jumper/SkJumper_stages.cpp?rcl=9018952290a468886c819405c6d9495b4aa5d7d4&l=416

If you like we could explore having Chromium prefer this new code path for these modes.  The new code is primarily designed for color-correct drawing but is able to draw into legacy non-color-correct kN32_SkColorType buffers too.  It'd draw somewhat differently (usually better) and at a different speed (probably slower, maybe faster... it's really machine dependent).

### ke...@chromium.org (2017-05-24)

Assigning mostly to have an owner on this security bug (it helps them not languish). It sounds like there is a potential path toward a mitigation.

### sh...@chromium.org (2017-06-06)

[Empty comment from Monorail migration]

### pa...@chromium.org (2017-06-26)

[Empty comment from Monorail migration]

[Monorail components: Privacy]

### hc...@chromium.org (2017-06-28)

Removing Mike as owner as I think the work on Skia side is done here and there are options for Chrome to make changes to use new code path (and accept some differences in output) or pursue one of the other timing solutions.

I am not sure who should do this work, if none of the Chrome folks on cc, can anyone make a recommendation?

### ji...@chromium.org (2017-07-04)

[Empty comment from Monorail migration]

### el...@chromium.org (2017-07-05)

Despite the security view restriction, this bug has been CC'd to a public alias.

https://groups.google.com/a/chromium.org/forum/#!msg/paint-bugs/RIjWpTd_tf0/Gw-tRFZJEgAJ

### ji...@chromium.org (2017-07-06)

Can anyone suggest a owner for this issue?

### ra...@chromium.org (2017-07-11)

(Security sheriff triage) Assigning to senorblanco to decide what to do based on the responses from the skia team. If you need input/advice from the security team 
here, please feel free to reach out to an individual or chrome-security@.

### hc...@chromium.org (2017-07-11)

[Empty comment from Monorail migration]

### fm...@chromium.org (2017-07-11)

We're in the process of switching Chrome to the branchless Skia impl for everything except Src & SrcOver (https://skia-review.googlesource.com/c/21372/).

I can take the bug while we work on that.

### fm...@chromium.org (2017-07-11)

I was too optimistic about that change: we're holding it off for now due to perf regression concerns.  Since it wouldn't necessarily close this attack vector anyway, it's prolly better to decouple from the bug.

### se...@chromium.org (2017-07-11)

Since this is related only to blend modes in Skia, and not image filters, I'm going to hand it off to reed@ for further triage.

### pe...@gmail.com (2017-07-20)

Is paint-bugs@chromium.org going to be removed from the Cc list? Will/can the discussion be deleted from Google Groups? I'm a little confused by the lack of a response to what seems like a significant leak to me.

### hc...@chromium.org (2017-07-24)

Groups posting seems to have been done via auto-cc, only way to stop it is removing Blink components perhaps??  doing so and +chrishtr in case he has permissions to delete the post.

It will be very tough to address this in all places, now and future, at the Skia level, so we continue to recommend it be handled by the browser(s)...

[Monorail components: -Blink>CSS>Filters -Blink>Canvas]

### sh...@chromium.org (2017-07-26)

[Empty comment from Monorail migration]

### mk...@chromium.org (2017-08-07)

Hey folks, it looks like this bug is languishing. It also looks like it has real impact on user privacy/security.

Chris, can you triage this within the paint team, since Skia is punting it?

### mk...@chromium.org (2017-08-07)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-08-07)

[Empty comment from Monorail migration]

### ch...@chromium.org (2017-08-07)

Update: I am looking into the right solution. Also, I deleted the thread from
paint-bugs.

### ru...@google.com (2017-08-28)

Are there any updates on this issue?

### he...@google.com (2017-08-28)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-09-06)

[Empty comment from Monorail migration]

### ru...@google.com (2017-09-13)

Friendly ping.

### aa...@google.com (2017-10-17)

Hey folks,

What's the plan for this bug, is it still a Severity-Medium & P1? The cross-origin leak can in some cases have fairly bad consequences and it looks like there has been no movement here in the last 2-3 months.

Thanks,
-Artur

### pe...@gmail.com (2017-10-18)

The leak to Google Groups also makes me a little nervous about leaving this bug open for too long.

There doesn't have to be a systemic fix right away. A "band-aid" in the short term would be enough to effectively close this particular attack vector.

### sh...@chromium.org (2017-10-18)

[Empty comment from Monorail migration]

### ch...@chromium.org (2017-10-31)

Update: the Skia team moved 'saturation' to the raster pipeline a while
ago:

https://skia-review.googlesource.com/c/skia/+/17992

which I believe means the particular exploit in this bug is likely fixed.
A local test by fmalita@ last week seemed to confirm that.



### mm...@chromium.org (2017-11-15)

chrishtr@, should we mark this as Fixed, or are there any blockers?

### ch...@chromium.org (2017-11-15)

I would like to verify one more time that it seems to be fixed first.

### ch...@chromium.org (2017-11-15)

Marking as fixed.

### sh...@chromium.org (2017-11-16)

[Empty comment from Monorail migration]

### aw...@google.com (2017-11-20)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-12-01)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2017-12-01)

Nice one permutatorem@! The Chrome VRP panel decided to award $2,000 for this report! A member of our finance team will be in touch to arrange the details.  Also, how would you like to be credited in our release notes?

### aw...@chromium.org (2017-12-01)

[Empty comment from Monorail migration]

### pe...@gmail.com (2017-12-01)

Thank you! You can credit me as Max May.

### aw...@google.com (2017-12-04)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-12-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-02-22)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### aw...@google.com (2018-10-05)

[Empty comment from Monorail migration]

### is...@google.com (2018-10-05)

This issue was migrated from crbug.com/chromium/699028?no_tracker_redirect=1

[Multiple monorail components: Internals>Skia, Privacy]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086984)*
