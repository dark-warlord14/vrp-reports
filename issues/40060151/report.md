# Security: Bypass(1301873)Chrome for Android Hide Custom Fullscreen Toast View with Repeated  delayed Enter Fullscreen Request 

| Field | Value |
|-------|-------|
| **Issue ID** | [40060151](https://issues.chromium.org/issues/40060151) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>FullScreen |
| **Platforms** | Android |
| **Reporter** | el...@gmail.com |
| **Assignee** | li...@google.com |
| **Created** | 2022-07-03 |
| **Bounty** | $4,000.00 |

## Description

**VULNERABILITY DETAILS**  

After <https://crbug.com/chromium/1264561> Chrome on Android fullscreen toast now migrated from native Android toast framework to custom toast view,and in this ticket Bypass of (1301873)

Normally the custom toast view will be displayed for 5 seconds, interestingly with appropriate timing I found the custom toast view able to hide quickly (only displayed less than a second) and there a chance to not showing at all by using delayed &repeated enter fullscreen request. with help of setTimeout function so user won't see the toast at all.

**VERSION**  

I able to reproduce the hide toast early on following Chrome version and device:

- Chrome 103.0.5060.70 on Huawei Nova7i; Android 10

**REPRODUCTION CASE**

1. Download and host file fullscreenpoc.html on a web server or visit <https://vrphunt.com/chrome/fullscreenpoc.html>
2. Click toggle button color will be changed from blue to purple
3. Click toggle button color will be changed from purple to green :) Bypass Happen and no toast at all and user entered full screen mode and forced not to quit this mode until he closed the tab and open it again ,(as i've used method from preventing user scrolling page)

POC Video  

<https://drive.google.com/file/d/1lx5BOaiIUF0GEmbcehI2hjYpVc-mxzYX/view?usp=sharing>

**CREDIT INFORMATION**  

Reporter credit: Ahmed ElMasry

Hope This Fixed ASAP

## Attachments

- [SVID_20220703_140235_1.mp4](attachments/SVID_20220703_140235_1.mp4) (video/mp4, 3.3 MB)
- [fullscreenpoc.html](attachments/fullscreenpoc.html) (text/plain, 4.1 KB)
- [XRecorder_04072022_003018.mp4](attachments/XRecorder_04072022_003018.mp4) (video/mp4, 1.2 MB)
- [Pixel6fullscreenpoc_1.mp4](attachments/Pixel6fullscreenpoc_1.mp4) (video/mp4, 418.6 KB)
- [Google Pixel6 Chrome Version&Build.jpg](attachments/Google Pixel6 Chrome Version&Build.jpg) (image/jpeg, 151.0 KB)
- [Huawei Nova7i-POC 8Sep2022.mp4](attachments/Huawei Nova7i-POC 8Sep2022.mp4) (video/mp4, 3.2 MB)
- [screen-20220912-152722.mp4](attachments/screen-20220912-152722.mp4) (video/mp4, 1.8 MB)
- [Chrome-Debug-Poc-Pixel6.txt](attachments/Chrome-Debug-Poc-Pixel6.txt) (text/plain, 4.4 KB)
- [seconed-pixel6-test.txt](attachments/seconed-pixel6-test.txt) (text/plain, 4.5 KB)
- [Debug-OnClick-Huawei-PoC.txt](attachments/Debug-OnClick-Huawei-PoC.txt) (text/plain, 11.7 KB)
- [2nd DebugTest-Huawei-PoC.txt](attachments/2nd DebugTest-Huawei-PoC.txt) (text/plain, 10.0 KB)
- [logs.txt](attachments/logs.txt) (text/plain, 8.0 KB)
- [filtered-logs.txt](attachments/filtered-logs.txt) (text/plain, 11.4 KB)
- [filtered-debugme-more.txt](attachments/filtered-debugme-more.txt) (text/plain, 35.5 KB)
- [filtered-debugme-more-animation-tracing-hide.txt](attachments/filtered-debugme-more-animation-tracing-hide.txt) (text/plain, 86.5 KB)
- [filtered-animation-tracing.txt](attachments/filtered-animation-tracing.txt) (text/plain, 16.8 KB)
- [screen-20221203-002143.mp4](attachments/screen-20221203-002143.mp4) (video/mp4, 988.6 KB)
- [filtered-debug.txt](attachments/filtered-debug.txt) (text/plain, 7.6 KB)
- [filtered-logs-debug.txt](attachments/filtered-logs-debug.txt) (text/plain, 20.5 KB)
- [Physical-Setup.jpg](attachments/Physical-Setup.jpg) (image/jpeg, 45.9 KB)
- [Remote-Physical-debug-Platform 2022-12-20 20-32-22-530.mp4](attachments/Remote-Physical-debug-Platform 2022-12-20 20-32-22-530.mp4) (video/mp4, 2.0 MB)
- [XRecorder_Edited_08012023_005334.mp4](attachments/XRecorder_Edited_08012023_005334.mp4) (video/mp4, 4.6 MB)

## Timeline

### [Deleted User] (2022-07-03)

[Empty comment from Monorail migration]

### el...@gmail.com (2022-07-03)

[Empty comment from Monorail migration]

### da...@chromium.org (2022-07-05)

Copying labels from 1301873

That change landed and was merged into 100, so FoundIn 102.

[Monorail components: UI>Browser>FullScreen]

### [Deleted User] (2022-07-05)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-07-05)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-17)

jinsukkim: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-07-27)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### el...@gmail.com (2022-08-02)

jinsukkim@: Friendly ping. Any updates on this Severity-High issue? No crbug activity since beginning of July and don't see an open CL

### [Deleted User] (2022-08-03)

[Empty comment from Monorail migration]

### ji...@chromium.org (2022-08-03)

Apology on this matter - I'm swamped with other time-critical issues. Will look into this as soon as I get some bandwidth.

### el...@gmail.com (2022-08-15)

jinsuk kim@: Friendly ping. Any updates? , is there some empty cycles to work on this bug? , No crbug activity and don't see an open CL, Hope you have some bandwidth to fix this, so I can try to bypass which will help in tight fix. 

### ji...@chromium.org (2022-08-18)

It's getting closer to the top of my work queue but I'm still too busy with other tasks. Will take on this as soon as I can. Thanks for the patience.

### ji...@chromium.org (2022-08-22)

This is not reproducible[1] on
 
- Pixel XL 104.0.5112.69/QP1A.191105.031.A1
- Pixel 2XL 104.0.5112.97/Rp1A.201005.004.A1
- Pixel 4XL 101.0.4951.41/TP1A.220509.001
- SM-G935T  104.0.5112.97 Build/R16NW 


Is there devices other than Huawei Nova7i where this issue was observed? Or any way to tweak the poc to make it happen?

[1] https://drive.google.com/file/d/1YWMRA6OV6sXbEI48Dj-hkAZTf2jeHOF3/view?usp=sharing


### el...@gmail.com (2022-08-22)

Hi jinsukkim@:

thanks for your time to reproduce and check the report, 

Actually I have my mobile Huawei Nova7i with Kirin 810 CPU  and All My Familiy Have Huawei too, But luckily i have found A brand New Huawei phone (Nova 9 SE) with Qualcomm Snapdragon 680 CPU (as i saw you have tested on all devices with snapdragon chip)

so hope the new POC for the snapdragon work with you at your test phones


Note: it is Just timing optimization for SetTimout function, The main POC file  Tested in many Huawei Devices with differnent  Kirin CPU and main POC file Worked like Charm


hope you check second poc , iam sorry for not having pixel mobile , i'll get my  pixel 6 After Next Month

the Steps in the second POC 
-----------------------------
Enter Incognito mode (prefered)

Visit https://vrphunt.com/chrome/fullscreenpocmod.html

1st Click toggle button then Quickly tab and hold on the Body of Page for 1 sec (while zoomed in) :) Bypass Happen


Repeat if not worked for 1st time

----------------------------
POC Video URL

https://drive.google.com/file/d/11z1NTnf8UldtmjXt6vlzrVgWgIHZuOlc/view?usp=sharing
--------------------------

Additional info if needed:

timing Optimization for SetTimeout Funtion  tests on Qualcomm CPU (19,320) (19,182) (18,218) may be helpful 

If any info needed let me Know 

Thanks




### ji...@chromium.org (2022-08-22)

..managed to repro it by tapping and holding the screen immediately after clicking the button as instructed, but I'm afraid this feels like too concocted steps to actually be a target of attack. I'm assuming it is not actions that users would take for their normal usage. I hope you would provide with repro steps with more ordinary actions (like the first one that consists of button clicks). I wouldn't view its severity as high. 

### el...@gmail.com (2022-08-23)

Hi jinsukkim@:

 this is good, severity high based on two click attack On Huawei Devices (main poc) in https://crbug.com/chromium/1341541#c0  https://crbug.com/chromium/1341541#c0 that I have optimized setTimeout delays based on this HW 

2nd: I have borrowed the second device from my brother's wife to do the second Snapdragon POC ,  but not sure to work with u or not, my guess on Cpu is correct, and we now stand on High Severity for All Kirin Huawei Devices with button two clicks, I'll do all my best to enhance  if I found a device for long time to test (its very hard for anyone to leave his mobile📱 😂for along time), 
----------
I need you also plz to test on MediaTech  Cpu also if you have 

need you also to test with Google pixel6 if you have Any mobile with Google Tensor Cpu 
-----
fin, what I want to say about sevirity,we should agree that this is High depending on main poc as Huawei phones have a great space in mobile market, isn't it? 

I will try to optimize the 2nd poc for you if I can 

thanks 



### [Deleted User] (2022-09-07)

We commit ourselves to a 60 day deadline for fixing for high severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### el...@gmail.com (2022-09-08)

Hi jinsukkim@:

I there any further Progress?? , didn't Hear from you since two weeks. 

==========After Some Checking=======

I see the behavior in this Bug Case is Similar to the behavior of this one you solved before 

https://bugs.chromium.org/p/chromium/issues/detail?id=1320538

Could you Check? 
==============

I Have Got My New phone now (Google Pixel6) and tested the bug  and it works fine too

Google pixel6 Android 13, Chrome 105.0.5195.79

==========
POC URL

https://vrphunt.com/chrome/fullscreenpocmodX.html

========
Attachment POC Video for Google Pixel6 and Huawei Nova7i Devices
=====
Thanks 


### el...@gmail.com (2022-09-12)

Hi jinsukkim@:

This is another test on Pixel6 phone 

Url of POC
+++++++++

https://vrphunt.com/chrome/fullscreenpocmodX-Fin.html

================
Attached POC video 

Hope you check the updates and work on the fix ASAP, thanks for your time in advance 

### el...@gmail.com (2022-09-26)



jinsukkim: , danakj@ Friendly ping. Any updates? , is there some empty cycles to work on this bug? , 

 No crbug activity  since your last https://crbug.com/chromium/1341541#c15  and I have updated the ticket with additional information you need with different real Pixel 6 device, could you start working on this?,as it has exceeded deadline , Thanks for your time and patience


### [Deleted User] (2022-09-28)

[Empty comment from Monorail migration]

### li...@chromium.org (2022-10-12)

[Security Marshal] I reached out to jinsukkim@ and he will prioritize this this week, he has been swamped with a launch. 
I have also confirmed that the PoC from https://crbug.com/chromium/1341541#c18 works on a pixel 5a test device with one click.

### ji...@chromium.org (2022-10-14)

I haven't been able to repro the issue with the URLs in https://crbug.com/chromium/1341541#c18/#c19 on any of the devices I tested (Pixel XL, Pixel, Pixel 2XL, Pixel 4XL, Pixel 5a). The top toolbar immediately appears again.

Demo with Pixel5a https://drive.google.com/file/d/19MGI0VwdnoUFE5A3wQ2eLxV-GzuFwmIj/view?usp=sharing

Is there anything I miss here in the repro step?  The instruction in the HTML page says 'Press Go then tab on Page body in 2 seconds'. But I expect it to be just a single tap, with which the issue won't get repro'ed.

### el...@gmail.com (2022-10-14)

Hi ,...
Thanks liza@  for your notes and time spent on repro the case at https://crbug.com/chromium/1341541#c22 , about your  comment yes there are some devices got full screen by one click but i have modified the PocC's to be generic so jinsukkim@ can repro very easy .. thanks for you 

jinsukkim@ i see that you have only taped one time not like the instructions say..anyway  i have tested the PoC and still works well on Google Pixel 6,and i have found that the best way to see you what actually happening, is  recording  with physical interaction showing my fingers. It will help you a lot 

So could you check this Very important to you for good repro

All pocs in https://crbug.com/chromium/1341541#c18 was tested many times in this video as you will see

https://drive.google.com/file/d/18t4_hvp_ErZl8hcJf_MRXju_fWMEaERp/view?usp=drivesdk

I think this is good , if you still have a problem in repro let me know ,or liza can help you with her thoughts about tracing the root cause .

Thanks Kim ,liza@




### ji...@chromium.org (2022-10-14)

Thanks for the clip. I was confused at the instruction telling me to tap in 2 seconds.

Let me repeat what I say at https://crbug.com/chromium/1341541#c15 : I don't think this presents itself a serious security bug if it requires such a deft hand to repro it. I'm expecting a simple gesture like a single tap to trick users.

amyressler@ would you help reassess the severity? 

### el...@gmail.com (2022-10-14)

jinsukkim@
Take https://crbug.com/chromium/1341541#c22 in your account and this reproduced by one tap in other devices liza tested it  and also i , i have attached also in the main poc of Huawei Nova with two clicks ,

I have modified the PocC's many times to make you able to repro , but it is typically the same issue like i have mentioned in https://crbug.com/chromium/1341541#c18 , @liza able to repro without any problems like me ,hope you consider this.
Thanks 

### el...@gmail.com (2022-10-14)

Cont..,
jinsukkim@
no Deft hand required as you said 
You can check 
https://bugs.chromium.org/p/chromium/issues/detail?id=1341541#c2

Repro at Huawei with clicking two times in Huawei Nova7i with kirin cpu
Demo poc or Huawei is https://vrphunt.com/chrome/fullscreenpoc.html
If you see that no deft hand required here also

liza@chromium.org  could you check and help ?


### am...@chromium.org (2022-10-17)

Hi jinsukkim@ I'm assigning back to you. I've used a Pixel (4a) and you do have to host the POC on a webserver, but it does reproduce as the videos present. Since there is only one click required, I'm leaving this as high. Since clicks are required, this issue is a borderline high-medium severity, but the omnibox is covered by the full screen overlay, so leaving at a high. Regardless of the high v medium severity, this issue would still be out of SLO. Please let me know if there are other ways we can assist here. 

### bo...@chromium.org (2022-11-02)

Hi there, this is your friendly Security Marshal checking in. It looks like we're not meeting our intended cadence in this case, sorry about that. I spoke in with @jinsukkim over chat and it seems like he's still the right person to help. Unfortunately he's swamped other bugs, but this one is on the way back up the backlog following a recent launch. 

For posterity, I was able to reproduce the PoC in https://crbug.com/chromium/1341541#c18 hosted a web server, with remote access to a physical Pixel 7 Pro provided by ACID (go/xcid - Googlers only) and using clank/bin/install_chrome.py to install the latest stable release. Feel free to reach out to me with any questions about reproducing the bug. 

### ji...@chromium.org (2022-11-03)

Learned from another similar issue that being able to repro it on stable release is one thing, doing it on a local build for debugging is another. As this issue relies on subtle timing between fullscreen requests, the action of debugging affect the repro step.

Question to the reporter: how do you tweak the parameters (and which parameters) in the poc html to make it easier to reproduce? I think I need to apply the trick myself to make it possible to repro the issue.

Once it is easily reproducible, the rest of the process to figure out the remedy would be relatively simple, from the experiences on similar issues I've resolved before.

### el...@gmail.com (2022-11-08)

 Hi All ,

Thanks bookholt@ for taking care of this issue and your time reproducing it .


Hi kim jinsukkim@,

Actually , the idea came to my mind is to race enter/exit full screen and see the behaviour as i saw that when entering fullscreen the toast get starting  to appear after fullscreen mode activated , so giving it a try as exit full screen remove the toast so why not to try enter then  exit to get the toast vanish  before start appearing and set the rest of execution. 

Worked on that for more than one day to get the best timing range to hide fullscreen toast and started  to refine.

Explanation & Debugging Referencing to the FullscreenHtmlApiHandler Code:

https://chromium.googlesource.com/chromium/src/+/f12d2f34366237497d3a7667d00fbd5a841ba824/chrome/android/java/src/org/chromium/chrome/browser/fullscreen/FullscreenHtmlApiHandler.java

In the the PoC mentioned at https://crbug.com/chromium/1341541#c18, the part that responsible for this is

<button id="btn" onclick="setTimeout(function(){toggleFullScreen();},22);setTimeout(function(){toggleFullScreen();},162);disableScroll();" >GO</button>

where 20ms timeout for enter fullscreen and second timout 162ms for toggling the mode (exit fullscreen) additionally disablescroll();  that is responsible for preventing user from exiting fullscreen mode  with gestures returning to the main page but closing page when getting back.

According to Browser Api (setTimeout) is asynchronus requests so Callback Queue  involved in  the operation and  functions executed as follows

1-disablescroll();
2- then pull the toggleFullScreen() with 20ms (to Enter fullscreen mode) from the queue to the stack to be executed.
3-then pull the toggleFullScreen() with 162ms (to Exit fullscreen mode) from the queue to the stack to be executed.

Reflecting this to the Browser internal Operations for enter/exit fullscreen process after the execution of disablescroll(); at first

Here's what happened when you have enter/exit/enterFullscreen in succession:

1- For the first (togglefullscreen() ) enterFullscreen mode executed, a toast is displayed

2- Second (togglefullscreen()) ExitFullscreen mode executes and removes the toast but not immediately (i.e. while fade in animation) that normally takes 500ms for fading in/out.

3- after removing fading in  of fullscreen by exit fullscreen the (animation finish callback) get executed as (onSystemUiVisibilityChange) is delayed with 200ms.

4- so trying  Racing with this Equation

( 20ms +JsEngineOverhead ≥ Racing ≤  200ms+JsEngineOverhead ) 

,where 20ms is the time of Entering-fullscreen mode  and 200ms is the time of Exiting-fullscreen mode  in addition of jsEngineOverhead where jsEngineOverhead is the execution time of javascript engine.

-the idea  is to race fading in toast and  showing animation delay  and fast remove of notification toast that was called at the beginning of (exitFullscreen) then entering mode
 
Suggested Fixes:-
===============

1st  Fix
======
-In order to prevent this, At the beginning of Exit-Fullscreen we need to cancel the attempt to enterfullscreen while the toast initiated by the previous enterFullscreen and is in (Fading in) state.

2nd suggested fix
==============
2- At the beginning of Exit-Fullscreen Remove any hide-toast runnable in the queue , and ( Is to wait a reasonable time near 500 ms before hideNotificationToast();) this time   to settle Fullscreen flags and call SystemUiVisibility that  settles the UI as SystemUiVisibility change takes 200ms.

Notes :
=======
The main problem is when Requesting the Exit-fullscreen is dependent on CLEAR_LAYOUT_FULLSCREEN_DELAY_MS = 20;
Delay to allow a frame to render between getting the fullscreen layout update and clearing the SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN flag.

So we can call exit fullscreen before this time ends to call the hideNotificationToast(); at the same time of large fading in time (500ms) , the flags of system ui flags still waiting the update after this period of time,At the same time SystemUiVisibility waiting the flags to settle the UI (200ms) of the Corresponding mode.

Hope i’ve explained the idea well .
Thanks .,


### el...@gmail.com (2022-11-08)

 Cont.. to  the previous comment ,

you mentioned >>Once it is easily reproducible, the rest of the process to figure out the remedy would be relatively simple, from the experiences on similar issues I've resolved before.

>Reply to this . you can Reproduce it the same way you were able to at https://crbug.com/chromium/1341541#c15  becuase you also mentioned ( repro it on stable release is one thing, doing it on a local build for debugging is another. As this issue relies on subtle timing between fullscreen requests, the action of debugging affect the repro step)

as i mentioned in the previous comment it's a critical timing as the overhead of javascript engine execution taken into account so by logic debugging is another timing change factor .
so you can Reproduce it  as the same way you reproduce before at comment https://crbug.com/chromium/1341541#c15 

Thanks kim


### tw...@chromium.org (2022-11-11)

Thank you for all of the detailed notes!

Looking at FullscreenHtmlApiHandler, there are a couple of other things that stand out to me:

mFadeOutNotificationToastRunnable is never cancelled... should it be if we're reentering fullscreen while this animation is running? and/or in hideImmediatelyNotificationToast()?


cc liberato@ as well since I think some of the code in question was added in crrev.com/c/3585548

### li...@google.com (2022-11-11)

i agree that the runnable is likely the cause.  i thought that the call to `removeCallbacks` [1] did cancel it, though now i wonder if i really wanted `removeMessages`.  if it's not cancelling at that point, yeah, things are going to go pretty wrong.

it's a little sketchy also that it uses "the current toast" rather than a bound parameter of "the toast i was constructed to cancel".

[1] https://source.chromium.org/chromium/chromium/src/+/main:chrome/android/java/src/org/chromium/chrome/browser/fullscreen/FullscreenHtmlApiHandler.java;drc=d1e1301c82bef37d30796e2d6098856b851d90a4;l=695

### li...@google.com (2022-11-11)

=> me, since i should have some time to look at this today

### li...@google.com (2022-11-15)

sorry about the delay -- haven't forgotten, still looking.

### li...@google.com (2022-11-15)

one thing that stands out is that, after quite a few attempts in both canary (110) and stable (107) on my p4a, i've repro'd it exactly once.  i've tried both the url in c#0 and the one in c#19.

### li...@google.com (2022-11-15)

ah -- i think after re-reading c#31, i understand the issue a bit better.  let me play with the timeouts a bit to see if i can repro it more reliably locally.

### el...@gmail.com (2022-11-15)

Thanks Frank for trying to fix this issue, 

https://crbug.com/chromium/1341541#c31 is the summery of( 3 days) reading and debugging code line by line on paper not in debugger ,as i know  debugger is overhead on this critical timing issue , we want yo enter before 20ms of flags set timeout and fading in state with cancel toast function which placed in exit Fullscreen function. Btw could you check your email , so if i can assist i'll do  📨..

Thanks


### li...@google.com (2022-11-15)

haven't been able to repro it, even fiddling with timeouts.

from what i can tell, and maybe everybody else already knew this, but i think that we're not actually in full screen when the repro works, at least in the "has a fullscreen element" or "WebContents::IsFullscreen" senses.

the toast might be involved, but the problem is really that we're hiding the sys ui after exiting fullscreen.  i suppose that "the system ui is hidden" is a reasonable functional definition of what being in fullscreen, but the state machine in the browser thinks that we're not.

i've still only seen it once, so can't verify.

### el...@gmail.com (2022-11-15)

liberato@ 
>>at least in the "has a fullscreen element" or "WebContents::IsFullscreen" senses.

This is the step before setting Flags that was mentioned in notes at https://crbug.com/chromium/1341541#c31 
@
when Requesting the Exit-fullscreen is dependent on CLEAR_LAYOUT_FULLSCREEN_DELAY_MS = 20;
Delay to allow a frame to render between getting the fullscreen layout update and clearing the SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN flag.

>>the toast might be involved, but the problem is really that we're hiding the sys ui after exiting fullscreen

#you mean on layoutcahnge @line438 ?
If (webContents!=null ......,etc
To reach to this step yhe estimated time is 20ms for setting full screen flag +20ms for clear layout flag + system visibility 200ms @line412,413,415 in addition of overhead of execution  resulting  near 

240ms+JsOverhead  

EXIT FULLSCREEN Not Fully completed because the flags not well correctly set  and we have executed the enter/exit 

with this Equation

( 20ms +JsEngineOverhead ≥ Racing ≤  200ms+JsEngineOverhead ) 
  As mentioned also in https://crbug.com/chromium/1341541#c31
 
I think my suggestions for fix will cover racing and end this problem 

Because if we enter Fullscreen and toast start to fade in , we shouldn't accept the reverse (exit Fullscreen) in a short period of time 20ms +at least half of toast fadein period  near 250ms  ,, 500ms is very good


We need to define a variable flag for fading in state 
At the beginning of exit Fullscreen @line411 we should check fade in state flag  (at the beginning of exit Fullscreen func ) if still in fade in return and don't exit 

This flag can be cleared  after 5sec or half of yo be assure that user have seen the toast 

Then accept setting flags for exit full screen and exist the mode ..

But in my opinion putting hide notification toast() func  plain without any check is a problem @line 411

About repro 

Which timing you have used ??
 https://crbug.com/chromium/1341541#c18 WAS GOOG FOR ALL IN REPRO LIZA AMY bookholt and also kim but kim was using debugger and able to repro with touch and hold screen https://crbug.com/chromium/1341541#c14 and https://crbug.com/chromium/1341541#c15 to overcome debugger

Another note important if you attach debugger 
 If the  reproduction failed  don't let yourself in same page without refreshing, fail and not entered Fullscreen mode refresh page and try again ,, also preferred to use incognito mode

Hope this also help you .
Thanks 



### li...@google.com (2022-11-16)

the thing about SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN is that it doesn't really control the browser UI.  it just asks android to draw the app under the system status bar.

> #you mean on layoutcahnge @line438 ?

i mean the one at 487 [1].

after some more investigation, i wondeer if [1] isn't happening -- that's what re-shows the browser controls.  i wonder if we're (a) not setting this relayout handler, or (b) setting it but never getting a relayout at all.  from the videos, it looks believable that we might not be getting a layout, though there is plenty of room for missing frames with a screen capture.  so it's hard to tell between (a) and (b) from that.

the layout handler is set in `exitFullScreen`, which is only called when exiting persistent fullscreen mode.  even then, it's only called sometimes: if `mWebContentsInFullscreen`, `mTabInFullscreen` are set and we're in `getPersistentFullscreenMode()`.  looking at each:

 - mWebContentsInFullscreen - only cleared a few lines after the call to `exitFullscreen`, so not cleared early.  set in `enterFullscreen` near the end.  there is an early return, but i don't think that we'd hit it in the repro since we only call `enter` once.
- mTabInFullscreen - same.  neither of these seems likely to be the issue.
- `getPersistentFullscreenMode()` - cleared only after it's used in `exitPersistent...`.  set in a weird way though -- if somehow that's not being set before `exit`, maybe.  it's set either immediately in `onEnterFullscreen` or as a runnable that's run... sometime in the future by the Tab.  if it's called immediately, then (a) doesn't seem likely.

i'll try to figure out why it could be deferred to Tab, and if it's likely to race with `exitFullscreen`.

[1] https://source.chromium.org/chromium/chromium/src/+/main:chrome/android/java/src/org/chromium/chrome/browser/fullscreen/FullscreenHtmlApiHandler.java;drc=755573e31718405aa13648d37c73e6dbe7dfe572;l=487

### li...@google.com (2022-11-16)

oh -- that was easy!  turns out that it's unlikely that we're deferring it to the tab.

this would be much simpler if i could repro this locally :)

i might end up adding some logging to an apk and uploading it, to figure out which case we're in .

### el...@gmail.com (2022-11-16)

@ liberato 


at https://crbug.com/chromium/1341541#c42 
-----------------------------------------------------------
|  > #you mean on layoutcahnge @line438 ?  |
|                                                                        |
|  i mean the one at 487 [1].                             |
-------------------------------------------------------------

+++ They are same point  but different Reference file 

My Reference File Version is  what mentioned in C31 Notes 

https://chromium.googlesource.com/chromium/src/+/f12d2f34366237497d3a7667d00fbd5a841ba824/chrome/android/java/src/org/chromium/chrome/browser/fullscreen/FullscreenHtmlApiHandler.java#438
----------
Your Reference 

https://source.chromium.org/chromium/chromium/src/+/main:chrome/android/java/src/org/chromium/chrome/browser/fullscreen/FullscreenHtmlApiHandler.java;drc=755573e31718405aa13648d37c73e6dbe7dfe572;l=487

the line is:
 if (webContents != null && !webContents.isDestroyed()) webContents.exitFullscreen();

--------
so , we got the same point  to start from  :) 

Good Debugging ,#C42 and https://crbug.com/chromium/1341541#c43 pleased me :) :) , has different taste than debugger , but in this case we have to do this first like that.

>>i might end up adding some logging to an apk and uploading it, to figure out which case we're in .
  
Re:/ looking forward to know  every step Results :):)

Thanks Frank 


### li...@google.com (2022-11-17)

sorry for the delay.  please download [1] and install it.  record the logs with `adb logcat`, try a repro, and upload the result.  i only care about lines that start with `AVDA`, so feel free to limit the log to those if you'd prefer.  it'll help to remove any personally identifiable information from the log.

for linux:

adb logcat -c && adb logcat |grep AVDA >logs.txt

[1] https://storage.googleapis.com/liberato2/Chrome1341541.apk

### el...@gmail.com (2022-11-17)

Hi Frank...,

never mind about the delay i know you try to figure out the cause in this case.

Actually Now I'm @ home:) , my Linux laptop @ work , But Got Android Studio installed on my Windows 10 Machine and Installed the apk on previous comment  to My Physical Pixel-6 Mobile

started debugging mode and logged the Repro with logcat as requested.

Attachment:

+Google Pixel6 Poc Mentioned at https://crbug.com/chromium/1341541#c18




### el...@gmail.com (2022-11-17)

liberato@

I've also Debugged the Behavior without Problems using 

+Physical Huawei Phone (Nova 7i) with Kirin Cpu with (OneClick ) , Debug Using also logcat Android Studio latest
 
That Poc URL was Mentioned in https://crbug.com/chromium/1341541#c0 and Represented with One Click attack at Video in https://crbug.com/chromium/1341541#c2

https://bugs.chromium.org/p/chromium/issues/detail?id=1341541#c2

Debug in txt file Attachment 

Thanks Frank, Hope i Helped You. Thanks again for your Time and Efforts if you need any further info let me know :)


### el...@gmail.com (2022-11-17)

[Empty comment from Monorail migration]

### li...@google.com (2022-11-17)

thanks for the traces.

just to be sure i understand, is it true that:
 - the two traces in c#46 are from runs where the problem happened, and
 - the trace from c#47 did not repro the problem



### el...@gmail.com (2022-11-17)


The traces in https://crbug.com/chromium/1341541#c46 for Google Pixel6 Poc Mentioned at https://crbug.com/chromium/1341541#c18 ,the problem happened , and confirmed by liza ,amy, bookholt.

The traces at https://crbug.com/chromium/1341541#c47, https://crbug.com/chromium/1341541#c48  is related to the Reproduction of poc at Huawei Devices .

All traces taken while the problem happened., I mentioned the poc and it's related comment , as the two have different SetTimout periods in the poc  . 

You can take pixel device traces .as i see all Google security engineers use Pixel devices 🙂




### li...@google.com (2022-11-18)

this line:

> exitPersistentFullscreenMode: onLayoutChange, showing browser UI

happens right before HtmlFullscreen... tries to show the browser UI that's not being shown in the repro case.  in the c#47 and c#48 traces don't show it, as expected.  they do show that the layout listener is installed correctly.  it just isn't being called.  this would be consistent with what i expected; no layout for some reason => no browser ui.

however, the c#46 traces do show these calls.  i can't explain that.

there are some additional checks elsewhere in chrome that might ignore the update, but that's rare.  i'll put together something with additional logging to make sure.

### el...@gmail.com (2022-11-18)

liberato@

So weird bug to me too , so i debugged the case twice  on each device to confirm that the debugging output is correct.

»» there are some additional checks elsewhere in chrome that might ignore the update, but that's rare.

Rep:/ you can  give the system some more time to settle everything  that may be invisible to us  , try to update an apk with delayed hide notification toast by 300ms to 500ms and give it a try .

That's besides the additional logging you want to add.

BTW the only differences between Google Pixel 6 and Huawei Device is OS and Cpu 

Google Pixel 6 cpu  is Google Tensor with Android 13

Huawei Nova7i cpu is Kirin  with Android 10


### li...@google.com (2022-11-23)

sorry for the delay, got sidetracked.  i'm putting together another apk with more debugging.

i also have a 6a on order that, hopefully, i can repro this with.

### el...@gmail.com (2022-11-25)

liberato@ 

Have you achieved a good progress on this?


### li...@google.com (2022-11-28)

i haven't touched it since last week, since Thu / Fri are holidays in the US.


### el...@gmail.com (2022-11-28)

so ,it will be looked at this week?

### li...@google.com (2022-11-29)

> so ,it will be looked at this week?

i appreciate your enthusiasm.

please try this one, and send the log:

https://storage.googleapis.com/liberato2/chrome_immediate_ui.apk


### el...@gmail.com (2022-11-30)

Hi Frank ..,

 liberato@

> i appreciate your enthusiasm.
i appreciate yours too :) ,and also your great efforts

After downloading the latest apk from https://crbug.com/chromium/1341541#c57 and testing the PoC mentioned in https://crbug.com/chromium/1341541#c18 , i've attached the logs for debugging as requested .

Device (Ubuntu Linux Machine)
=========
Command used for Debugging 

adb logcat -c && adb logcat |grep AVDA >logs.txt

========================================

**Kindly find the attached logcat debug file below**

Thanks

### el...@gmail.com (2022-11-30)

i've tested the Bug with:

(Google-Pixel 6) Physical device



### [Deleted User] (2022-11-30)

[Empty comment from Monorail migration]

### li...@google.com (2022-11-30)

it looks like the logs are truncated:

> 11-30 15:42:22.806 24347 24436 E chromium: [ERROR:layer_tree_host_impl.cc(4025)] AVDA: SetCurrentBrowserControlsShownRatio top: 0.055425 bottom: 0.055425
> 11-30 15:42:22.816 24347 24436 E chromium: [ERROR:layer_tree_host_impl.cc(4025)] AVDA: SetCurrentBrow

you might need to save the entire log, then grep for 'AVDA' as a separate step to avoid it.

### el...@gmail.com (2022-11-30)

It was debugged using one line command as mentioned in https://crbug.com/chromium/1341541#c45 

>>you might need to save the entire log, then grep for 'AVDA' as a separate step to avoid it

*Okay I'll log all and remove sensitive data if found ..., just give me max half /one hour to go back to office and prepare that for you .., 
Thanks 



### li...@google.com (2022-11-30)

it's not urgent.  i'm going to prepare a new apk too, but that's not ready.

### el...@gmail.com (2022-11-30)

I'am going now , preparing that for you until you finish the other apk file .

i'll be there till 12 AM  (3hours from now) ready for testing your new apk, once you have finished let me know.
Thanks

### el...@gmail.com (2022-11-30)

 liberato@
Check the new one.

### li...@google.com (2022-11-30)

https://storage.googleapis.com/liberato2/Chrome-more-debug.apk


### li...@google.com (2022-11-30)

re c#65: the last we see of the browser controls state, it's setting the state to 'shown' (1, first line).  then it starts animating from hidden (0.055..., third line).  No idea why it reverts back to zero in the forth line, or what happens to the animation that's supposed to be showing it.  hopefully, the new logging in the c#66 apk will provide some ideas about why.

11-30 20:57:42.516 20238 20238 E chromium: [ERROR:web_contents_impl.cc(9476)] AVDA: WCI UpdateBrowserControlsState constraints: 1 current: 1
11-30 20:57:42.516 20238 20238 E chromium: [ERROR:page_impl.cc(263)] AVDA: PI UpdateBrowserControlsState without proxy
11-30 20:57:42.520 20320 20764 E chromium: [ERROR:layer_tree_host_impl.cc(4025)] AVDA: SetCurrentBrowserControlsShownRatio top: 0.055435 bottom: 0.055435
11-30 20:57:42.528 20320 20764 E chromium: [ERROR:layer_tree_host_impl.cc(4025)] AVDA: SetCurrentBrowserControlsShownRatio top: 0 bottom: 0


### el...@gmail.com (2022-11-30)

This lines also got my intention and i searched for that on chrome bugs 

May be this related to this commit 
https://bugs.chromium.org/p/chromium/issues/detail?id=769321#c11

>>This affected URL bar hiding on Android, where the resize message was
sent while there was a provisional main frame that hasn't swapped into
the tree yet, causing the renderer to think that the browser controls
had zero height.

### el...@gmail.com (2022-11-30)

[Empty comment from Monorail migration]

### li...@google.com (2022-11-30)

interesting -- it immediately starts hiding the controls after starting to show them.

// show
11-30 22:42:04.373 15357 15397 E chromium: [ERROR:browser_controls_offset_manager.cc(195)] AVDA: UpdateBrowserControlsState animated top: 1 bottom: 1 animate: 1
11-30 22:42:04.374 15357 15397 E chromium: [ERROR:browser_controls_offset_manager.cc(519)] AVDA: Animate old top: 0 new: 0.05537
11-30 22:42:04.374 15357 15397 E chromium: [ERROR:layer_tree_host_impl.cc(4025)] AVDA: SetCurrentBrowserControlsShownRatio top: 0.05537 bottom: 0.05537

// not sure if these are cause or effect or unrelated
11-30 22:42:04.382 15272 15272 E cr_AVDA : onSystemUiVisibilityChange: vis == 0
11-30 22:42:04.382 15272 15272 E cr_AVDA : maybeEnterPending: hidden: false tab: org.chromium.chrome.browser.tab.TabImpl@76968fc opts: null

// now we hide controls.
11-30 22:42:04.401 15357 15397 E chromium: [ERROR:browser_controls_offset_manager.cc(637)] AVDA: StartAnimationIfNecessary
11-30 22:42:04.401 15357 15397 E chromium: [ERROR:browser_controls_offset_manager.cc(655)] AVDA: StartAnimationIfNecessary hiding controls

### li...@google.com (2022-11-30)

oh i see -- it notices that we're only 0.05 away from "hidden", and decides that it'd be better just to hide them.  it totally misses the fact that there's an animation in progress that's trying to show them.  at least, that's my hypothesis.  i'll try making it noop if an animation is in progress.

### li...@google.com (2022-11-30)

"it" in c#71 refers to "StartAnimationIfNecessary".

anyway, https://storage.googleapis.com/liberato2/Chrome-check-anim.apk

the thing that i don't get is why it's trying to start an animation there to begin with.  it does so after a scroll or zoom completes, but i don't think that either one should be going on during the repro.  anyway, i added some logging to figure out which one is doing it.

### el...@gmail.com (2022-12-01)

liberato@
Animation Check Debugging Related to  https://crbug.com/chromium/1341541#c72  Apk .


### el...@gmail.com (2022-12-01)

[Empty comment from Monorail migration]

### li...@google.com (2022-12-01)

interesting -- there is no animation any more when the scroll completes, because of the call to ResetAnimations(). i didn't annotate the places where it's called, but i suspect here [1], when the scroll starts.  my hypothesis was wrong, since the animation is gone by the time the scroll ends.

new sequence of events:
  - exit fullscreen, start animation to show controls
  - make little to no progress in animation, so controls are mostly hidden
  - start scroll, which stops the animation
  - end a scroll, which notices the "mostly hidden" and snaps to "entirely hidden"

since chrome hides the url bar during a scroll intentionally, i wonder if this needs fullscreen at all.  maybe just a js scroll is sufficient.  if so, then it might be WAI.  i'll poke around.

[1] https://source.chromium.org/chromium/chromium/src/+/main:cc/input/browser_controls_offset_manager.cc;drc=3f7a9d89de4c434583d520384b01ce87178ce888;l=390

### el...@gmail.com (2022-12-01)

waiting for your digging , you are the expert on that :) :)

ResetAnimations > was called earlier than it should be .. right? 


### li...@google.com (2022-12-01)

I'm not sure what the right behavior is when a scroll starts, to be honest.  I can see why one would not want an animation playing, since the compositor will adjust the top bar in sync with the scroll operation.  the animation will get in the way.

We could jump to the end of the animation instead of cancelling, but that might be janky.  we'd really want to know is something like "how much the scroll would have moved the top bar from the end of the animation", then animate to that point when the scroll stops.  i don't know if that's easy to compute, though.

before i worry about that too much, i'll put together another apk that jumps to the end of the animation when starting a scroll.  that will verify that it actually fixes the problem.  if all of the above is right, then it will jankily show the top bar, then scroll a little but not enough to hide the bar.  it'll then snap to fully shown rather than fully hidden.

the interesting part here is that the site cannot (i think) normally influence the top bar, though a similar effect can be achieved by a user-initiated scroll.  if one were to get the user to scroll downward until the top bar was gone, then capture scroll events like this demo does, then one would be in the same situation without using full screen to get there.


### li...@google.com (2022-12-02)

https://storage.googleapis.com/liberato2/Chrome-jump-anim.apk

please capture the log again, and also verify that it repros this time.  it forces the animation to jump to end when it's interrupted.

### el...@gmail.com (2022-12-02)

Nice Frank,

it works and fixed ,

I have attached screen capture for how it repro and behave.

For debug ,just wait for me to prepare it for you ..


### li...@google.com (2022-12-02)

thanks.  i don't know if jumping to the end is a reasonable thing to do in all cases, so i'll have to dig a little more.  mostly, i wanted to be sure that the explanation in c#75 was correct.

### el...@gmail.com (2022-12-02)


Debug info for apk package at https://crbug.com/chromium/1341541#c78 using  Android Studio Logcat at Windows10 machine (filtered-debug.txt).

another debug file using logcat terminal windows version also (filtered-logs-debug.txt).

if any further info needed let me know ,..Thanks 


### el...@gmail.com (2022-12-02)

**terminal version ( filtered-logs-debug.txt ) More detailed**


### li...@google.com (2022-12-06)

I've been trying to get a local repro, because i'd like to figure out why there's a ScrollEnd happening.  i believe that's supposed to require a user gesture.

With https://vrphunt.com/chrome/fullscreenpocmodX-Fin.html , i can only repro by trying to tap the gray button after clicking the red one.  this makes sense -- i'm accidentally starting a scroll with the second tap.  I'd say that this behavior is working as intended.  One might argue that for a very small scroll, it should not cancel the animation.

With https://vrphunt.com/chrome/fullscreenpoc.html i cannot get a local repro at all.  That's the interesting one, since it's a single click if I understand correctly.

All of these attempts are with a pixel 6a on stable (108?) chrome.


### el...@gmail.com (2022-12-06)

liberato@
Hi Frank 
C30 and C31 discuss that, because attaching debugger is a critical overhead, you cat take a look to this.
But https://bugs.chromium.org/p/chromium/issues/detail?id=1341541#c18 have the poc url 
https://vrphunt.com/chrome/fullscreenpocmodX.html not the ones you have mentioned as this one timing what was mentioned and Repro'ed by liza , amy, bookholt on previous comments .


>>i'm accidentally starting a scroll with the second tap.  I'd say that this behavior is working as intended

++This is wrong in repro. 

If i can help you more let me know, you can send me the new apk to test if you need.

Thanks 

### el...@gmail.com (2022-12-06)

>>i'm accidentally starting a scroll with the second tap

++ You can try this https://vrphunt.com/chrome/fullscreenpocmodX.html with tap on red button then on outside tab  quickly in Repro (with debugger attached),(don't try to scroll). To get the right debugging log.



### li...@google.com (2022-12-06)

From c#28, it sounds like a debugger is not necessary to repro with fullscreenpoc.html by clicking one button then the same button again, without any particular timing between the button clicks.  This is the interesting case, but I haven't been able to get it to work locally.

fullscreenpocmodX.html and fullscreenpocmodX-Fin.html both require multiple taps with specific timing (for example, "within two seconds"), if i understand correctly.  Multiple taps with specific timing requirements and/or a debugger make it quite a lot less likely to show up in practice. It's also not clear to me that the existing behavior is broken for multiple rapid taps; chrome intentionally hides the browser chrome on scroll.  That's what appears to be happening in the clicks-with-specific-timing cases -- the second click has to happen soon enough after the transition out of fullscreen to interrupt the animation that shows the top bar.

There is room for improvement in this behavior for very small scrolls, which i'll look into.  But, per c#28, a repro with a single click (which i'm interpreting to mean "a click that doesn't have specific timing requirements on whatever happened before") is important.

Any help you can provide in getting me a local repro of the fullscreen is appreciated -- i need to figure out where the scroll event is coming from.  From the video, it doesn't look like any sort of scroll is happening, so we might be getting a spurious event somehow.

### el...@gmail.com (2022-12-06)

Hi Frank
liberato@

>>From c#28, it sounds like a debugger is not necessary to repro with fullscreenpoc.html by clicking one button then the same button again

Rep+/ in c27 i mentioned (Demo poc or Huawei is https://vrphunt.com/chrome/fullscreenpoc.html), it's timing is different than the Pixel6 timing, because this poc was made for only Huawei devices with kirin cpu, then i've got my google Pixel6 device that based on Google Tensor , and also in c18 poc optimized for Snapdragon Chipset too , this is a big proof that hardware execution time play a vital role here .

Another interesting thing that proof this too , in this video https://bugs.chromium.org/p/chromium/issues/detail?id=1341541#c2 , i've used xrecorder to record the poc , this make the poc works for one click and using system recorder for the previous video at c1 used two click , because the native screen recoder i think attach something to the chrome tab to record it which makes overhead too but xrecorder not. I mean anything that we think it might not affect , it affect . So i relized that the best thing to do for kim is to be more generic on poc and made him two tab poc's ,because i know there will be a debugger or some inspection tool here to trace.

>>For second paragraph >>(fullscreenpocmodX.html and fullscreenpocmodX-Fin.html both require multiple taps with specific timing,.......)

Rep+/ specific timing on the instructions doesn't mean that this time is the time of the poc itself for timeout functions in the poc, but it means like counting one two three,....in normal, to let kim easy Repro with debugging (but don' exceed this because we see in code that transition take near 200ms and some other functions befor it requires some time too) ,so the instructions to let him see and focus on the cause in trace within the execution time discussed/explained with you after you take the ownership for this issue.

In second paragraph too,

>>>It's also not clear to me that the existing behavior is broken for multiple rapid taps; chrome intentionally hides the browser chrome on scroll.  That's what appears to be happening in the clicks-with-specific-timing cases -- the second click has to happen soon enough after the transition out of fullscreen to interrupt the animation that shows the top bar.

Rep:/ the animations shouldn't be broken by a tab  in normal way because there a critical actions depends on this event/function callback (showing Browser controls), if it was interrupted we should protect user and show browser controls immediately, Right?

For third paragraph>> waiting for your trace and loved to discuss anything with you, appreciate you efforts for trying to figure out and trying to land a tight fix.


In last paragraph
>>Any help you can provide in getting me a local repro of the fullscreen is appreciated 

Rep+/ for Sure i will help with anything i can do ,

>>- i need to figure out where the scroll event is coming from.  From the video, it doesn't look like any sort of scroll is happening, so we might be getting a spurious event somehow 

Rep+/ which video you mean ,and 
spurious scroll event >>could you clear that more for me to be on the same point you have ??

I see in the previous debugging files ScrollEnd comes after ResetAnimation function

12-03 01:06:55.716 16073 16114 E chromium: [ERROR:browser_controls_offset_manager.cc(572)] AVDA: ResetAnimations
12-03 01:06:55.849 16073 16114 E chromium: [ERROR:browser_controls_offset_manager.cc(491)] AVDA: ScrollEnd starting animation if necessary

What is the effect of scrollend  after animation reset function got executed and forcing the browser controls to be shown again as it jumps animation ratio changes ?

If you want to jump ScrollEnd from code and try with different apk and test it , it will be okay 

I have used disablescroll function in my poc too

But i have commented that function and works for me so i realized that problem in animation transition state and start working on the bug.

Disablescroll()
window.addEventListener('touchmove', preventDefault, wheelOpt); // mobile

If you still need the poc with clicks on Huawei device ,let me know to arrange sometime i'll be at home and get thus device and install VMware on my pc debugging environment and also sharing you the mobile to test as you have it ,just send me you timezone  to be suitable for me and you too. It's my pleasure to help and trace this bug  with you if i can 🙂

Thanks 

### el...@gmail.com (2022-12-12)


Friendly Ping: liberato@
any further updates/progress on this?


### li...@google.com (2022-12-12)

no, i'm afraid i haven't had any more time to get back to it.

> I have used disablescroll function in my poc too

This isn't the same type of scrolling.  ScrollEnd happens in response to a user input.  The POC turns off blink-side scrolling.  I'm not super familiar with scrolling, but i think that the first one will trigger ScrollEnd while the former will not.  It might prevent ScrollEnd if blink-side is turned off, though, but I haven't tried.  Odd things happen when blink adds event handlers to scroll -- it turns off several optimizations inside chrome.

> spurious scroll event >>could you clear that more for me to be on the same point you have ??

I meant in any of the repro videos, i don't see anything that looks like a scroll gesture.  However, we do see ScrollEnd which (I think) is strictly supposed to be from a user-initiated scroll.  I don't understand where the ScrollEnd is coming from.  I also can't figure out how to make it happen locally, without doing a gesture-based scroll.

The key point is that I need to be able to repro this locally to make much more progress with it.  Ideally, it's on a physical device rather than an emulator.  The reason is that it's a timing-related issue.  We eventually need to be confident that it's fixed on a physical device, after all, and that's very hard with emulators for timing issues.

### el...@gmail.com (2022-12-13)

liberato@
I know It's a critical timing issue that need much efforts to be fixed , you now know where is the problem happened (animation state) but you need to know scrollend line too, but from long debugging you know the case very well .

About repro  i suggested to remote share my nova7i  to debug more ,  you can also  repro it easily by
https://vrphunt.com/chrome/fullscreenpocmodX.html
And click on go tab then rocket head  like counting one two 
 Every time you want to retry repro close the tab open new one and try 
You can also try tab on go button then hold the rocket head too 

This will help you in repro with debugging 

Dou you suggest someone can help you you can ask here to join us ?

If you suggest something, or if you want any further information let me know ,but please try to fix it as this case was opened since 
JULY (6~monthes ago)., appreciate your hard work on this and your time .

### el...@gmail.com (2022-12-13)

Btw emulator isn't sutable for repro at all .

### el...@gmail.com (2022-12-20)

Hi Frank .., liberato@

I've made a Good Setup for you for most Accurate Debugging Yourself . using Clicking from your side as you mentioned in https://crbug.com/chromium/1341541#c86 

>>From c#28, it sounds like a debugger is not necessary to repro with fullscreenpoc.html by clicking one button then the same button again, without any particular timing between the button clicks.  This is the interesting case, but I haven't been able to get it to work locally.

i have also attached the graph of the setup and video to show you how it really great solution in this case as you want to do it more than one time smoothly :)

Once you are Ready just give me ping msg  to start 

what you need from yourside is to get (anydesk) remote desktop application installed 

https://anydesk.com/en/downloads/windows

once installed and we setup link session together , you will be directly connected to setup mentioned 

i think this is best solution for best debugging
 
this is my time zone 
https://www.timeanddate.com/time/zone/egypt
i'am ready now if you want to start could you share me you timezone if you want more time space to work together .

BTW kim  jinsukkim@ wanted clicks to debug  ,you can ask him to join us if he can .

waiting for your Reply ....

Appreciate your efforts in advance

Thanks 




### li...@google.com (2022-12-21)

i really don't think that an emulator is the way to go here.

locally, with the link in c#18 i can only get it to work with two clicks, not one, which is what (a) the instructions say, (b) the video shows, (c) jinsukkim@ observed, and (d) what i'd expect from how the code works.  in all cases, it looks very much like the second tap is just starting a scroll, which cancels the top bar animation while it's hidden, just like happens if one scrolls down the page under normal circumstances.

to illustrate this a little better, i made a different POC [1].  it is a similar idea that doesn't involve full screen at all, or clicks.  just scroll down the page a little, then (if everything works!), you'll suddenly see the fake google header and be unable to scroll it offscreen.

what happens is this:

 - the page tries to detect when the chrome top bar is gone, by watching window.outerHeight.  admittedly, i'm doing this poorly.  assume it that could be done flawlessly, which is likely.
 - it then prevents further scrolling by intercepting touchstart or move or something => top bar won't return even if the user tries.
 - it then shows the fake top bar, suddenly.  a real attack wouldn't do this immediately, of course; it'd use the intercepted scroll events to scroll the fake image onto the screen from the top, just like the real top bar.  that way, it'd look perfectly normal and the user would suddenly appear to be on google.com when they 'scrolled' back to the top of the page.

this seems like a security issue of some kind, but it's unrelated to full screen.

[1] https://storage.googleapis.com/liberato2/detect-scroll.html



### el...@gmail.com (2022-12-21)

Hi Frank liberato@

Thanks for your feedback but i want to clear some points here, and some test results i have ..,

>>i really don't think that an emulator is the way to go here
No emulators here this is my physical phone and my pysical home pc ,,

My phone has droidvnc_ng 
app to view and control mobile from my pc over high speed wlan network 
https://play.google.com/store/apps/details?id=net.christianbeier.droidvnc_ng

The mobile you see on screen is this mobile opened in TightVnc session to control this and see  everything as you already have it 

This physical phone also connected to my pc with usb cable to catch debugging logs ,right 
After all when you log to my home pc  remotely from your site via anydesk app ,this like as you are using my physical pc and phone and like as you are here at my home and using the two devices as well... Right .. no virtual no emulators at all.

I have used the poc and device mentioned in main ticket at https://crbug.com/chromium/1341541#c0 exactly. With Huawei phone.

=========

>>locally, with the link in c#18 i can only get it to work with two clicks

Rep:
That's good , some devices repro's with one and some works with two, and this was mentioned by me before .

>>in all cases, it looks very much like the second tap is just starting a scroll, which cancels the top bar animation while it's hidden
Rep: i think that hide-toast runnable in the queue  is the cause ,
As mentioned ic https://crbug.com/chromium/1341541#c31  at 2nd suggested fix part.
Why ?? Because there are some devices Repro'ed by one tab , and tested main poc at https://crbug.com/chromium/1341541#c0 with one tab and endscroll line presents in debug log  too.. i'll show the proof at the end of this comment too..

>>to illustrate this a little better, i made a different POC [1].  it is a similar idea that doesn't involve full screen at all,....

Rep: yah i know this behavior and it isn't the case here ,i'll show you why in the poc video attached 

Details  about that and why it isn't the case here ?::

Normally: when you scroll a little bit scroll start to hide the bar as you described in the paragraph of Poc detect scroll you have made 

What breaks your expectations and why this issue related to full screen?
=======
.1st turn
Open the poc you sent detect-scroll.html and start scroll ,you will see the behavior of hiding nav bar as you mentioned in details right..

=======
2nd turn 
Install  this app(android vnc server)i've used  for example,  from play store https://play.google.com/store/apps/details?id=net.christianbeier.droidvnc_ng

Then go to accessibility menu in your android and select the installed app and enable accessibility for it and allow ?
What will happen?
This will break the scroll poc/behavior you have made and will not hide the nav bar at all .

What about full screen mode is it a Fullscreen related ? 
Yes.Sure , why because the poc https://vrphunt.com/chrome/fullscreenpocmodX.html works as it's own behavior of fullscreen and second tab not take the responsibility for hiding the navbar and controls as you mentioned in second paragraph, some devices one tab also confirm that.

>>this seems like a security issue of some kind, but it's unrelated to full screen.

Rep: maybe, but my thoughts and different notes on the behavior of fullscreen say the cause related to fullscreen.

Please have a look to this important video that shows up the details mentioned in this comment 
It's 8min repro's  every case mentioned here  normal and unexpected.

Video Url
https://drive.google.com/file/d/1ODSyJJZEWLwvutCWiMXC009al5eK3CKN/view?usp=drivesdk

This is very important, keep me informed about any updates.

Thanks 



### el...@gmail.com (2022-12-25)

Hi , Frank  liberato@

Have you checked the previous comment C94 and made some debugging on that behavior to see endscroll line ?

Additional information / simple summerized steps .

You can use Voice Access App instead of droid vnc mentioned above in 2nd turn 

-Go to mobile settings >Accessibility>enable Voice Access (under interaction control)

Summery :
Before Accessibility Enable for voice Access/Other App

A)PoC[1] you mentioned in C93 will work as you designed and hides top bar.

B) Fullscreen poc mentioned https://vrphunt.com/chrome/fullscreenpocmodX.html also works  as expected.
 
So what about your hypothesis on that paragraph?

>>in all cases, it looks very much like the second tap is just starting a scroll, which cancels the top bar animation while it's hidden, just like happens if one scrolls down the page under normal circumstances.

Rep: No, the second tab isn't the cause yo do that.

Another Proof:some devices works with one tab depends on Hw as i discussed and explained before.

So, what about the cause?  And is it related to fullscreen or not??
Yes ,it's a full screen component Related Bug.

Why?.

Second Turn yo test..

Enable Accessibility for Voice Access, then 

A)-try PoC[1] detect-scroll.html in C93 , It (will Not Working), so hypothesis for scroll is the cause cancelled as no scroll any more because of Accessibility Override.

So what about Fullscreen poc?

2) Fullscreen PoC still working, this is a good proof and evidence that the issue is due to fullscreen component .

Video PoC at previous comment  at C94 described this behavior.

Is there any further information required?

Thanks, Merry Christmas 🎄 and Happy New Year for you and your Family👨‍👩‍👧‍👦










### li...@google.com (2023-01-03)

> 2) Fullscreen PoC still working, this is a good proof and evidence that the issue is due to fullscreen component.

The animation to re-show the top bar is cancelled by a ScrollStart, so chrome believes that there is a scroll gesture happening somehow.  When we tried a modified apk that does not cancel on scroll, the repro went away.  These seem like very good evidence that a scroll, timed very closely after the full screen ends, is responsible for cancelling the top bar animation.

It is true that full screen does cause the "show" animation that is being cancelled in this particular case, but anything that starts such an animation by re-showing the top bar would be equally good.

I do not understand why there is a scroll happening.  This, to me, is the most important thing; I believe that the single click repro is, somehow, also starting a very short scroll.  Without that scroll, there would be no one click repro.  It is possible that the transition out of full screen is somehow responsible for that; i don't know.

### el...@gmail.com (2023-01-03)

Hi..

When i was thinking in the timing and getting different working timeout randomly within margin of timeouts set in FullscreenhtmlApiHandler.java

**The most important thing that let the timeout works is getting in  before transition timout of fullscreen ends , this is the time to cancel toast using exitfullscreen mode  at the same time animation got interrupted as you described and debug lines shows .. so i suggested the fixes for delay at the beginning of exitfullscreen or checking flags of which mode we are still , so hide toast or not .

I took another look  to debug file
After getting in full screen mode the second toggle to exit interrupted the animation state of fullscreen mode executed 1st and 
Hide notification toast called
ResetAnimation
SetbrowserControlShowRatio
ResetAnimation again
Scrollend

++and at this comment at R[1]shows that scroll is already present 
for some tracking (syncing)viewport 
R[1] : https://source.chromium.org/chromium/chromium/src/+/main:cc/input/browser_controls_offset_manager.cc;l=380;drc=fd7b4c1844e6431a5ba4475eb515257a3a238a31;bpv=1;bpt=1

And after calling ResetAnimation the problem begin from this point

https://source.chromium.org/chromium/chromium/src/+/main:cc/input/browser_controls_offset_manager.cc;l=415;drc=fd7b4c1844e6431a5ba4475eb515257a3a238a31;bpv=1;bpt=1

>>starting a very short scroll
ResetAnimation calls ResetBaseline  function 
// Reset the baseline so the controls will immediately begin to scroll
 // once we're at the top
I think short scroll comes from here ( between the enter and exit mode ) while transition there is short scroll  because browser think it still animating and create a cumulated delta for syncing viewport

The proof in my point of view the poc video that working with Huawei device  with click one  then click the button again  and Fullscreen mode comes 

This one 
video at https://crbug.com/chromium/1341541#c92 https://bugs.chromium.org/p/chromium/issues/attachment?aid=581420&signed_aid=n8L8ccYlcyrDts0VJMUOZQ==&inline=1

1st click enter and exit mode 
2nd click enter the Fullscreen mode without toast . Because browser still think we are in transition state time.

Let me know about what comes to your mind in this point  and your ways to start  on this just Thinking out loud


Scroll override from accessibility to viewport scroll  is related to R[1] 

>>>I do not understand why there is a scroll happening.  This, to me, is the most important thing;

Rep:/ if you tried enabling Accessibility there no scroll on browser anymore ,as C95  clear that 

The scroll got fired from transition so PoC[1] https://storage.googleapis.com/liberato2/detect-scroll.html will not working.
 
Have you digged more and reached to something? 

Thanks frank

### li...@google.com (2023-01-03)

> The proof in my point of view the poc video that working with Huawei device  with click one  then click the button again  and Fullscreen mode comes 
> 1st click enter and exit mode 
> 2nd click enter the Fullscreen mode without toast . Because browser still think we are in transition state time.

This is where i get confused -- that's not one click.

I agree that with two clicks one can easily cause this -- in every case i've seen, one of those clicks starts a gesture scroll => cancels animation.  I don't know whether the scroll is because the touch starts a scroll in the normal way, or if it's some interaction with the full screen transition / toast that causes it.  I'm not sure that it matters -- if we allow a second gesture, then it's easy to make that second gesture a scroll.

Maybe there's a way for a single click to start a scroll and then convert to a tap or something, and the ScrollEnd might get delayed and interrupt the animation.  However, I don't know if that can really happen.

In every single instance I've seen, the cause is that a "ScrollBegin" cancels the animation to show the top bar.  Toasts and accessibility settings and fullscreen seem like additional complexity on top of that to me.  Those things might cause the ScrollBegin on one repro vs another, but one is as good as the other given that ScrollBegin is called.

Anyway, i'll see if i can put together something to prevent the very narrow case of cancelling a top bar animation because a small scroll.

### el...@gmail.com (2023-01-03)

Hi

>>This is where i get confused -- that's not one click

Rep:/ No confusion  the repro instructions for the poc  says that in https://crbug.com/chromium/1341541#c0

1-Click toggle button color will be changed from blue to purple
2- Click toggle button color will be changed from purple to green :) Bypass Happen

and video poc in https://crbug.com/chromium/1341541#c0 with native system show touch on screen recorder  add some overhead as it related to Accessibility somehow so  when use native recorder with show touch the 2 clicks is the way to achieve, i've add another video also in https://crbug.com/chromium/1341541#c0 for same poc in same device but without native recorder ,it was recorded by Xrecorder that doesn't have show touch on screen so the POC works with one Click  and you see the color of the button that it was pressed one time only , this one tab achieved by other googlers after C18 on different devices ..

I'am not arguing with how many tabs/clicks but i want to show you how is the time and overhead acts..

Another thing i've noticed while creating the poc code , the event handler can play vital role also and change timing i've tested touch, touchstart,touchend  these events add more overhead so i ho back to onclick

>>Toasts and accessibility settings and fullscreen seem like additional complexity on top of that to me. 

Re:/ I want you see all digging results coming from long days to let you make a very tight fix ,you can fix using the best way you see ,you are the expert on that :)

>>Anyway, i'll see if i can put together something to prevent the very narrow case of cancelling a top bar animation because a small scroll.

Re:/ this is also a very good solution , waiting for your CL fixing this

Thanks frank 








### gi...@appspot.gserviceaccount.com (2023-01-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/5ef87ae18da3cb25764e9551e7357b0c5f780e57

commit 5ef87ae18da3cb25764e9551e7357b0c5f780e57
Author: Frank Liberato <liberato@chromium.org>
Date: Fri Jan 06 16:59:55 2023

Reorder "show browser controls" animation after gesture scrolls.

If chrome starts an animation to show browser controls that has
either (a) not completed before a user gesture scroll starts, or
(b) starts during the user gesture scroll, then restart the
animation after the scroll completes.  This makes it unambiguous
to the user that the controls can be present, since the scroll
will cancel the animation otherwise.  We don't want a small
scroll, which is easy to generate accidentally, to have the large
effect of preventing the browser controls from becoming visible.

For simplicity, this CL doesn't try to differentiate a small
scroll from any other; any scroll that overlaps with an animation
to show the browser controls results in the controls becoming
visible when the scroll completes.

Bug: 1341541
Change-Id: I58950b78bd02cb84989290a45cf5f67626508c61
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4136461
Reviewed-by: David Bokan <bokan@chromium.org>
Commit-Queue: Frank Liberato <liberato@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1089760}

[modify] https://crrev.com/5ef87ae18da3cb25764e9551e7357b0c5f780e57/cc/input/browser_controls_offset_manager.cc
[modify] https://crrev.com/5ef87ae18da3cb25764e9551e7357b0c5f780e57/cc/input/browser_controls_offset_manager.h
[modify] https://crrev.com/5ef87ae18da3cb25764e9551e7357b0c5f780e57/cc/input/browser_controls_offset_manager_unittest.cc


### li...@google.com (2023-01-06)

c#100 will hopefully work around the issue we've seen.

for whatever it's worth, any single click repro seen earlier is very likely not the same as this bug.

one confusing thing i did notice locally when using a device + screen cast (go/acid) is that this would happen:

  - click once
  - site enters full screen
  - screen cast elides most frames with a toast, presumably because the whole display changed, which is a bad case for screen casting.  i saw several weird artifacts around full screen changes that i suspect are related to the screen cast falling behind.
  - see full screen web page, which looks like what a repro state looks like
  - site does not exit full screen, probably because the timer in the script that exits full screen lost a race.  this is the step that happens sometimes but not others.

anyway, when that happens, it looks like it's in the repro state, but really it's not. this state is in full screen, while the repro is not.  the CL above does nothing for this case. i suspect it's WAI -- screen casting is just hard to do.

### el...@gmail.com (2023-01-07)

Hi Frank..,

Thanks for your efforts fixing this issue , i've tested the fix in 

Google Chrome: 111.0.5524.0 (Official Build) canary (64-bit) 

Revision: d90da2d9e52ed9cbd2bc01863e5e6ed49704898d-refs/branch-heads/5524@{#1}

OS	Android 13; Pixel 6 Build/TQ1A.221205.011

**and I Confirm that the issue has been fixed.**

>>About 3rd &4th paragraph  describing screen cast behavior

Re:/ Actually i didn't dig on that behavior before , but if i found something relating to this I'll update you here.

Jut let me know if any further information required from my side, i'll be happy to assist 🙂.

Thanks 






### el...@gmail.com (2023-01-09)

Hi , Frank  liberato@

The animation interrupt (racing) has been fixed  ,but there is something broken i noticed here after doing many tests on Canary
111.0.5528.0 (Official Build) canary (64-bit) , that thing is Notification toast position

Notification toast position becomes at the end of screen(bottom) instead of showing at the top, which needs to be fixed too.

Thanks 

### el...@gmail.com (2023-01-19)


NEW Update:

Broken toast positioning of fullscreen mode entry at (Stable) Release v 109.0.5414.86 since Jan 10 2023 update

Toast position becomes at the bottom of screen instead of being at the top  which can be covered easily and spoof browser controls and omnibar .

Thanks for your attention, Regards.

### li...@google.com (2023-01-19)

i suggest filing a new issue, since that sounds unrelated to this one.


### te...@chromium.org (2023-01-19)

FWIW, the toast was moved to the bottom as part of another security issue, so I'd consider that working as intended:
https://chromium-review.googlesource.com/c/chromium/src/+/3990410

### [Deleted User] (2023-01-19)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-19)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-19)

Requesting merge to extended stable M108 because latest trunk commit (1089760) appears to be after extended stable branch point (1058933).

Requesting merge to stable M109 because latest trunk commit (1089760) appears to be after stable branch point (1070088).

Requesting merge to beta M110 because latest trunk commit (1089760) appears to be after beta branch point (1084008).

Merge review required: M108 is already shipping to stable.

Merge review required: M109 is already shipping to stable.

Merge review required: M110 is already shipping to beta.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [108, 109, 110].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### li...@google.com (2023-01-19)

i'm not sure we should merge this back, except maybe to 110. i'll defer to the security folks, but it really doesn't seem serious enough for a respin.  the code isn't terribly big, but there are a lot of subtleties.  i have no idea if the assumptions still work in 108 or 109.

### am...@chromium.org (2023-01-19)

In tracking this issue for awhile, I fully concur. Stable/109 and Extended/108 RC cut is tomorrow and this seems far too risky to backmerge for this deadline considering the subtle complexities in this change. 
Let's let this bake over the weekend and revisit for M110 merge review on Monday, which is well in advance of next M110 beta release on Wednesday. 

### am...@chromium.org (2023-01-23)

not seeing any stability issues from this fix so far from canary and dev data; unless there's any issues or concerns, please merge this fix to M110/branch 5481 at your earliest availability so this fix can be included on M110 next beta / early stable 

### li...@google.com (2023-01-23)

sg, thanks.  i'll try this right now.

### li...@google.com (2023-01-23)

cherry-pick applied cleanly [1] -- trying to land it.

[1] https://chromium-review.googlesource.com/c/chromium/src/+/4189877

### gi...@appspot.gserviceaccount.com (2023-01-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/769c1f74432b2c9937836bab5f3bb60f6b524f8e

commit 769c1f74432b2c9937836bab5f3bb60f6b524f8e
Author: Frank Liberato <liberato@chromium.org>
Date: Tue Jan 24 16:51:43 2023

[M110] Reorder "show browser controls" animation after gesture scrolls.

If chrome starts an animation to show browser controls that has
either (a) not completed before a user gesture scroll starts, or
(b) starts during the user gesture scroll, then restart the
animation after the scroll completes.  This makes it unambiguous
to the user that the controls can be present, since the scroll
will cancel the animation otherwise.  We don't want a small
scroll, which is easy to generate accidentally, to have the large
effect of preventing the browser controls from becoming visible.

For simplicity, this CL doesn't try to differentiate a small
scroll from any other; any scroll that overlaps with an animation
to show the browser controls results in the controls becoming
visible when the scroll completes.

(cherry picked from commit 5ef87ae18da3cb25764e9551e7357b0c5f780e57)

Bug: 1341541
Change-Id: I58950b78bd02cb84989290a45cf5f67626508c61
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4136461
Reviewed-by: David Bokan <bokan@chromium.org>
Commit-Queue: Frank Liberato <liberato@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1089760}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4189877
Cr-Commit-Position: refs/branch-heads/5481@{#621}
Cr-Branched-From: 130f3e4d850f4bc7387cfb8d08aa993d288a67a9-refs/heads/main@{#1084008}

[modify] https://crrev.com/769c1f74432b2c9937836bab5f3bb60f6b524f8e/cc/input/browser_controls_offset_manager.cc
[modify] https://crrev.com/769c1f74432b2c9937836bab5f3bb60f6b524f8e/cc/input/browser_controls_offset_manager_unittest.cc
[modify] https://crrev.com/769c1f74432b2c9937836bab5f3bb60f6b524f8e/cc/input/browser_controls_offset_manager.h


### am...@google.com (2023-01-26)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-01-26)

Congratulations! The VRP Panel has decided to award you $4,000 for this report; part of this reward includes a bonus as we appreciate your helpfulness in the analysis and input in working with the developer toward the fix. Thank you for your efforts and reporting this issue to us -- nice work! 

### el...@gmail.com (2023-01-27)

Thanks Amy amyressler@ for the Reward, but i expected to have same reward of that similar impact earlier report (https://crbug.com/chromium/1270593), which have 
impact(Browser  UI Spoofing) ,For reference, (earlier similar report https://crbug.com/chromium/1270593,https://crbug.com/chromium/1259492 and https://crbug.com/chromium/1320538) , which I would argue has a similar impact to this issue, hope you consider this report as high quality report referencing bounty to the earlier reports mentioned above , referring to https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules and bounty amount table for high quality report with functional exploit, with Security UI Spoofing impact with Bisect bonus for debugging, I would appreciate it if the VRP panel could re-evaluate the reward amount at a future VRP Panel session for a reassessment and potential change in reward amount... Thanks in advance!

### am...@google.com (2023-01-28)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-01-30)

re https://crbug.com/chromium/1341541#c118, we are happy to revisit and reassess this issue. I do want to mention in advance, while impact is important, it is not the only parameter for reward decisions, as report quality is also taken into consideration. A number of the other reports you reference consisted of a bisect (before the bisect reward was put in place) as well a full spoofing exploit rather than just a POC. 

>>>with Security UI Spoofing impact with Bisect bonus for debugging,
As mentioned in https://crbug.com/chromium/1341541#c117, we did include a bonus to your reward for your assist with debugging.
Your report would not be eligible for a bisect bonus, as you did not provide a bisection. A bisection helps us considerably during the triage process, so we would not be able to extend this bonus to you for debugging.

### el...@gmail.com (2023-01-31)

Thanks Amy amyressler@ for your feedback.., 

> we are happy to revisit and reassess this issue.

+ Thanks for that.

>while impact is important, it is not the only parameter for reward decisions, as report quality is also taken into consideration.

+ I think i have followed rules for VRP program to write High Quality Report , but the decision upon to the panel with full respect.

+ For example this one is simple report  https://crbug.com/chromium/1320538 with only poc without any (debugging/analysis/multi functional PoCs,root cause details)  like this case.

+ If you feel this report can be reassessed it will be Okay.

Thanks.

### am...@chromium.org (2023-02-02)

Hi Ahmed, we have reassessed this report and believe that the reward amount is sufficient for the bug class and impact, report, and quality. While reporting is similar but not exact in comparison to https://crbug.com/chromium/1320538, that was exceptionally concise and also the researcher provided information similar to a bisect, detailing which versions of active release channel and the device this bug reproduced on. Similar to what we'd consider as part of a bisect bonus now that has been introduced. 

For a more fair comparison, it is important to note that the original issue - https://crbug.com/chromium/1264561- that this report is a bypass of, was awarded $2500. This report is most similar to that issue and report, but with you receiving a bonus for your debugging and analysis. 

### el...@gmail.com (2023-02-02)

Thanks Amy for your feedback and efforts on that.


### am...@chromium.org (2023-02-03)

[Empty comment from Monorail migration]

### pg...@google.com (2023-02-07)

[Empty comment from Monorail migration]

### pg...@google.com (2023-02-07)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-27)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1341541?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060151)*
