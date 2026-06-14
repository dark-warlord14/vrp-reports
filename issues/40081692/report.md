# Security: Screen contents from other origins and non-Chrome applications are displayed in the browser

| Field | Value |
|-------|-------|
| **Issue ID** | [40081692](https://issues.chromium.org/issues/40081692) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Image, Internals>GPU>Internals |
| **Platforms** | Mac |
| **Reporter** | vi...@gmail.com |
| **Assignee** | ju...@chromium.org |
| **Created** | 2015-03-22 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

I was able to display in the browser images that are outside the chrome Sandbox

1. converting a specific jpg image to Base64
2. trying to display the image with data:image/png;base64 inside a <img>  
   
   result: another image is displayed instead of the original image. The image that is displayed is a combination of other images locally opened on my computer, that are outside the Chrome Sandbox .

**VERSION**  

Chrome Version: 42.0.2311.39 beta (64 bits) .  

Operating System: OS X Yosemite 10.10.1

Remark: this vulnerability happens only with this specific image and it doesn't happen on every computer with the same OS + Chrome versions.

**REPRODUCTION CASE**  

jsfiddle that reproduces the bug <http://jsfiddle.net/YvQ5y/903>  

The image displayed in the bottom part of the window is not the original image.  

The image that is displayed is a combination of other images locally opened on my computer, that are outside the Chrome Sandbox .

Attachements:

1. logo.jpg: the original jpg image
2. image bug.png: the corrupted image
3. image\_data.txt: text file that contains the base64 image data

## Attachments

- [image_data.txt](attachments/image_data.txt) (text/plain, 768.0 KB)
- [logo.jpg](attachments/logo.jpg) (image/jpeg, 536.8 KB)
- [image bug.png](attachments/image bug.png) (image/png, 503.7 KB)
- [image mac os.png](attachments/image mac os.png) (image/png, 212.3 KB)

## Timeline

### ke...@chromium.org (2015-03-22)

Does this reproduce on more than one computer at all? It might be an extension or some other piece of software interfering with the image rendering.

### vi...@gmail.com (2015-03-23)

I was able to reproduce on a second computer with the same version:
Chrome Version: 42.0.2311.39 beta (64 bits) .
Operating System: OS X Yosemite 10.10.1

On both computer, there were no extensions installed.

### ke...@chromium.org (2015-03-23)

It's hard to say if this is actually a security problem or not, and I haven't been able to reproduce although I don't have a Mac available running 10.10.

I am speculating that this is a GPU problem and adding the relevant people.

Is there anybody who can investigate this further?

### vi...@gmail.com (2015-03-24)

I was also able to reproduce the bug on a virtual windows installed on my mac with Parallel:
 the windows OS was: windows 8 and chrome version: 41.0.2272.89

doest it help?


### ke...@chromium.org (2015-03-24)

[Empty comment from Monorail migration]

### da...@chromium.org (2015-03-24)

[Empty comment from Monorail migration]

### re...@chromium.org (2015-03-24)

I'm not able to reproduce this locally but I suspect that there's a bug that is preventing us from decoding this image properly and we end up drawing garbage. However, that's not security problem.

A renderer being able to see old content from a different renderer seems bad though. Is it possible that the shared memory allocated in the browser process and passed to the renderer is not zeroed out but could contain contents used by a previous process? In that case, we should probably zero it out in the browser before we pass it to the renderer. That would apply to all shared memory usage in chrome.

### pi...@chromium.org (2015-03-24)

[Empty comment from Monorail migration]

### pi...@chromium.org (2015-03-24)

We don't typically keep around / recycle general shared memory pages in the browser. And anonymous pages should in theory be zero'd by the kernel (otherwise it's a security issue at the OS level).
@reveman: is that true as well with the discardable memory subsystem?

My suspicion is that we have a missing quad, leaving a part of the framebuffer uncovered. GPU drivers are typically not as good with clearing buffers. We do so in the GPU process for textures/buffer objects, but maybe not for the IOSurface/CALayer we use to present to the system compositor.

@original reporter - when you say "The image that is displayed is a combination of other images locally opened on my computer, that are outside the Chrome Sandbox", are you saying they are open outside of Chrome? Or in Chrome but in another page?

### re...@chromium.org (2015-03-24)

Yes, discardable memory system does not reuse a shared memory segments. A segment is only used with one renderer. As long as the pages are zero'd by the kernel we should be good.

### ts...@chromium.org (2015-03-24)

piman@ - would a renderer be able to get read-back of the pixel data?  If not, this is probably a functional bug rather than a security issue per-se.

### pi...@chromium.org (2015-03-24)

If my suspicion is correct (missing quad), the renderers would not be able to read that data (it's only visible to the browser).

### vi...@gmail.com (2015-03-25)

@piman - the images (and image pieces) that are shown are not necessarily related to chrome. i.e. I can see a complete OSX menubar (with the date and wifi signal).

A segment of the image is attached

### ts...@chromium.org (2015-03-25)

Marking this as a functional bug per #12, but keeping restrict-view in case it turns out otherwise.

### da...@chromium.org (2015-03-25)

That doesn't sound like a missing quad if it's stuff outside of chrome, does it? Seems like a driver bug giving non-zeroed memory, that the renderer could potentially read since we allow readbacks there?

### pi...@chromium.org (2015-03-25)

@#15: GPU drivers vend uninitialized memory - that's unfortunate, but the reality. We do clear textures in the GPU process so that renderers can't get access to that uninitialized memory.
What I'm saying in #9 is that I don't think we clear the IOSurface/CALayer for the main render target (in the browser process), and so a missing quad would expose that uninitialized memory on screen (and, possibly in the browser process). However renderers would not have access to that render target.

### vi...@gmail.com (2015-03-26)

@piman is there a way to run chrome without GPU optimization? It might be interesting to see if the bug occurs then...

### da...@chromium.org (2015-03-26)

--disable-gpu

### vi...@gmail.com (2015-03-26)

With gpu disabled, I'm getting the right image. It's also a lot faster, than waiting for the corruption to appear.


### vi...@gmail.com (2015-03-30)

@piman I'd like to know on what conditions this bug could appear
1. only in MacOS
2. only with this image (what's so special with this image?)

### pi...@chromium.org (2015-03-31)

@#20:
1- the way we render things on MacOS is different. In particular the code path that is used to display the frame to the screen is specific to Mac, and that is what I suspect is missing a clear.
2- I don't know what's specific about that image, maybe it triggers a decoder bug or something.

### vi...@gmail.com (2015-04-02)

@piman I have a couple of concerns:
1. This bug happened to one of my customers, while creating a pdf report from my web app (it happens in Chrome but not in Firefox). I am afraid it could happened to other customers with MacOS. Do you plan to fix this bug? Is there a workaround? Is there a way in the js code to detect that the image was not properly rendered.
2. Why this bug is not a security issue? To me it seems to be a sandbox escape (as explained here: http://www.google.co.il/about/appsecurity/chrome-rewards/)  as it allows a person navigating in chrome to access images created outside chrome

### da...@chromium.org (2015-04-02)

reveman@ can you have a look at this and try repro/understand what's happening?


To Q#2, while you can see the image, the renderer process (ie the web page) will have no access to it.

### re...@chromium.org (2015-04-02)

+ccameron

I'm traveling this week. Best to find someone else that can take a look at this if important.

It's not a security issue unless the code in the sandbox can access these images. It doesn't sound like that's the case.

### vi...@gmail.com (2015-04-03)

@dankj 
My concern is related to a computer shared between several users.
User A uses his computer, visit private sites in Incognito Mode, type passwords (with Show Password enabled) and logout
The User B logs in and goes to the fiddle page I've put in the bug description. 
Consequence: User B might be able - with the help of Chrome - to see private information of User A.

Why isn't it a security vulnerability?

### pi...@chromium.org (2015-04-03)

@#25: because anything Chrome does could be done by any other program that the other user can install.
If it's a security vulnerability (OS vends data belonging to another user), it's in the OS, not in Chrome.

### vi...@gmail.com (2015-04-13)

@danak could you please help me to answer question 1 on #22?

### da...@chromium.org (2015-04-13)

ccameron owns this bug for fixing it, it would be great to fix, yes. as piman@ says it's not exposing anything security-wise, but we do fix bugs that aren't security problems :)

### [Deleted User] (2015-04-13)

reseting priority

### cc...@chromium.org (2015-04-13)

Given the comment from #4:

> I was also able to reproduce the bug on a virtual windows installed on my
> mac with Parallel:
> the windows OS was: windows 8 and chrome version: 41.0.2272.89

This probably isn't related to the particulars of how Chrome renders on Mac (CALayers et al). It's actually pretty amazing that the bug would reproduce going through virtualization -- I would lean much more towards this being a buffer not being initialized correctly (perhaps we're failing to detect that we didn't decode an image correctly, and we we're leaving a texture uninitialized).

I haven't been able to reproduce this locally.

### vi...@gmail.com (2015-04-15)

@ccameron
my biggest concern is: how could the code detect that the bug happens or on what type of images the bug could happen
my code creates a pdf report for the user with the image embedded.
The user would be very disappointed to discover that the pdf report contains an image with "personal' information instead of the expected image.
Please provide as much info as possible. It's quite urgent.

Also, I need to know if the bug could also happen on a "native" windows machine.

Thanks

### vi...@gmail.com (2015-04-29)

I have not received any response to my questions for more than two weeks.
It is really urgent for me and my business to get the answers to those questions.
Please help

### re...@chromium.org (2015-04-29)

Just to be sure, you're not actually able to reproduce a pdf that you have access to on the server side that contains personal information, are you?

The nature of this problem is such that you can't detect it from javascript. It's just a renderer issue afaict. If you could detect it, then that would make it a real security concern.

### vi...@gmail.com (2015-04-29)

Actually, I can detect it from javascript.

Let me explain how:
The image is inside a canvas.
Therefore, with getImageData I am able to get the pixel data of the corrupted image (that contains personal information) and send it to the server.

So, to me it sounds like a security concern.
What do you say @reveman ?

### re...@chromium.org (2015-04-29)

Yes, that's a real security concern. Increasing priority and making this a RB.

### am...@chromium.org (2015-04-29)

Probably too late for M42, so retargeting to M43.  Also, +timwillis@ from the security team to evaluate the security risk implied with #34 / 35.

### vi...@gmail.com (2015-04-29)

@reveman when will I know if this security concern is eligible for chrome rewards?
https://www.google.com/about/appsecurity/chrome-rewards/

### [Deleted User] (2015-04-29)

[Empty comment from Monorail migration]

### pi...@chromium.org (2015-04-29)

@34: have you been able to produce a proof-of-concept that actually gets the corrupted pixels with getImageData? What is displayed on the screen is not necessarily the same as what you'd get out of getImageData.

### vi...@gmail.com (2015-04-30)

REMARK: As I wrote before, this bug is not easy to reproduce. I was able to get the corrupted pixeld with getImageData on two mac os computers and one windows hosted on one of those computers.


here is the poc
1. open http://jsfiddle.net/YvQ5y/1060/
2. press submit
3. wait a couple of seconds
4. open the console
5. copy the console content: it is the pixel data of the top left 100x100 rectangle of the picture
6. go to http://jsfiddle.net/9qg120d4/
7. paste the data copied from the console
result: 
you see the top left 100x100 rectangle of the corrupted picture that contains personal information of the user






### vi...@gmail.com (2015-05-05)

@piman do you need further information?

### cc...@chromium.org (2015-05-11)

-RBS, 43->44

### vi...@gmail.com (2015-05-12)

@ccameron why did you remove the "ReleasBlock-Stable" label?
Why did you postpone to M-44?

### vi...@gmail.com (2015-05-20)

@piman any update on this issue?


### pi...@chromium.org (2015-05-20)

I'm not currently working on this.

### vi...@gmail.com (2015-05-20)

who’s working on this?
It’s quite urgent for me to have:
1. an estimate about when is it going to be fixed
2. is it an issue that could happen on windows or not?

### [Deleted User] (2015-05-20)

I'm not able to reproduce this either on a MBP with Chrome 42.0.2311.152 . Since you are using canvas, I'm wondering whether there's race condition in which toDataURL returns before the canvas is actually done drawing its contents. junov@ any thoughts? 



### pe...@google.com (2015-05-21)

[AUTO] Moving all non essential bugs to the next Milestone.  (This decision is based on the labels attached to your ticket.)


Ref: https://sites.google.com/a/chromium.org/dev/developers/ticket-milestone-punting-1

### cc...@chromium.org (2015-05-21)

I am unable to reproduce this.

### vi...@gmail.com (2015-05-26)

@ccameron as I said above the bug occurs only on specific machines. I was able to reproduce it on two mac os.  If you need it, we could arrange a team viewer session so you can see the problem by yourself.

### vi...@gmail.com (2015-06-03)

@piman
I think that I've shown my issue is an escape from Sandbox.
What is the procedure in order to receive the rewards?

https://www.google.com/about/appsecurity/chrome-rewards/


### pi...@chromium.org (2015-06-03)

I'm not in the security team, so I don't know what the process is, but we still haven't been able to reproduce this bug on our side, so we can't assess the security aspect of it.

### vi...@gmail.com (2015-06-03)

Would you like to have a team-viewer access to one of the machine where I was able to reproduce the bug?
We could do it tomorrow at 15:00 UTC. Is it convenient for you?

### vi...@gmail.com (2015-06-21)

@piman I have recorded the activity on the mac computer where the security issue occurs.

chrome version: 43.0.2357.124 (64-bit)
jsfiddle: http://jsfiddle.net/YvQ5y/1060/
here is a link to the video: https://www.dropbox.com/s/a0vpceom9jdhrbn/security%20issue.mov?dl=0


### vi...@gmail.com (2015-06-29)

@ccameron + @piman Please have a look at #54 containing a video of the issue reproduced.

### pi...@chromium.org (2015-07-24)

junov: could this be related to https://code.google.com/p/chromium/issues/detail?id=504690 ?

### re...@chromium.org (2015-07-27)

junov, bounce back to me and I'll re-assign if not related to 504690.

### ju...@chromium.org (2015-07-27)

Yes this does look like it could be a duplicate of 504690. The bug occurs when calling toDataURL on a GPU-accelerated canvas after a GPU driver reset. It is likely that the test case submitted by viebel would require the same OS, GPU model and graphics driver combo in order to reproduce.  I had the same problem with the test case generated by our fuzzers where I could not reproduce locally.

@viebel: Can you help us confirm that this issue is resolved? To do so, please try to reproduce using the Chrome Canary channel (https://www.google.com/chrome/browser/canary.html)


### cl...@chromium.org (2015-07-27)

[Empty comment from Monorail migration]

### pa...@chromium.org (2015-07-27)

I can't reproduce this on Mac OS X 10.10.4, Chrome 44.0.2403.107 (64-bit), GPU: AMD FirePro D500 3072 MB.

### pa...@chromium.org (2015-07-28)

[Empty comment from Monorail migration]

### cc...@chromium.org (2015-07-28)

[Empty comment from Monorail migration]

### vi...@gmail.com (2015-07-28)

Issue resolved on Canary. 
How were you able to reproduce and analyse the issue?
Could you please explain what was the fix? 
It would be nice to share a link to the commit that solves the issue?

### ju...@chromium.org (2015-07-28)

For those who do not have access to the other bug, the fix is: http://src.chromium.org/viewvc/blink?view=revision&revision=199183

It was possible to analyse the issue because cluster fuzz found a repro case that works for the culsterfuzz bot's specific hardware/OS config. The bug was found using a linux MSAN build. This is a build that is specially instrumented to detect memory errors. It produced a report with stack trace that identified specifically where the meomory error occurs. In this case, the error was that we were reading from uninitialized memory. So the vulnerability was leaking information from de-allocated resources.



### ju...@chromium.org (2015-07-28)

Simply accessing uninitialized memory should not leak information across process boundaries though. That seems like there could be an additional component to the vulnerability, which may involve the OS or the graphics driver. Or perhaps we are mistaken in believing the vulnerability is cross-process? Someone more familiar with the MacOS process security model should chime-in here.  Is it legit for a process to have a screenshot of the OS-rendered menu bar hanging around in de-allocated memory?

### mb...@chromium.org (2015-07-30)

rsesek: Could you take a look at c#65?

Updating some labels in case this turns out not to be a duplicate.

### rs...@chromium.org (2015-07-30)

GPU memory is not normal heap memory; it is vended by the system, and corruption can reveal information about old textures.

### vi...@gmail.com (2015-08-06)

I think that I've shown my issue is an escape from Sandbox.
What is the procedure in order to receive the rewards?

https://www.google.com/about/appsecurity/chrome-rewards/

### pi...@chromium.org (2015-08-06)

You did not demonstrate sandbox escape (arbitrary code execution outside of the sandbox). This is as best information leak.

### vi...@gmail.com (2015-08-06)

Ok. So am I eligible for Information Leak/High-quality report with functional exploit ?

### da...@chromium.org (2015-08-06)

+inferno

### ju...@chromium.org (2015-08-17)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-08-17)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

Your fix is very close to the branch point. After the branch happens, please make sure to check if your fix is in.

- Your friendly ClusterFuzz

### vi...@gmail.com (2015-08-17)

[Comment Deleted]

### vi...@gmail.com (2015-08-17)

what is the procedure to be eligible for Information Leak/High-quality report with functional exploit?

I have asked this question a couple of times. Why nobody answers

### rs...@chromium.org (2015-08-17)

You do not need to do anything. The vulnerability management process will get your report evaluated now that the bug has been marked as Fixed.

### vi...@gmail.com (2015-08-17)

Ok. Thanks.
Any idea how long should it take?

### ti...@google.com (2015-08-30)

viebel: We'll take a look at this report now that it's fixed. It will probably take a few weeks as this bug is will likely ship in M46 so that we can get really good testing coverage (the fix is already in M46).

Regarding your question in #75, the reward panel will assess which category your report falls into and provide you with an answer at that time.

Let me know if you have any other questions.

### ti...@google.com (2015-09-28)

#77: This report is currently at the reward panel - you should receive an answer this week.

### vi...@gmail.com (2015-09-28)

thanks @timwil...

### vi...@gmail.com (2015-10-07)

@timwil it has been more that a week now. No answer :(

### ti...@google.com (2015-10-08)

Best answer is cash answer.

Congrats - $1000 for this report! The panel determined that this was a high end baseline report.

Our finance team will be in contact within 7 days to collect payment details. Thanks for your patience here.

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an established charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### vi...@gmail.com (2015-10-08)

Thanks @timwil

Waiting for the reward :)

### vi...@gmail.com (2015-10-15)

@timwil Nobody contacted me for the rewards :(

### ti...@google.com (2015-10-15)

Thanks for following up - I'll chase it internally and someone should reach out today or tomorrow.


### ti...@google.com (2015-10-16)

[Empty comment from Monorail migration]

### ti...@google.com (2015-10-29)

Payment is on its way - should arrive in ~7 days. Thanks again for your report!

### cl...@chromium.org (2015-11-23)

Bulk update: removing view restriction from closed bugs.

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/469507?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>Image, Internals>GPU>Internals]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081692)*
