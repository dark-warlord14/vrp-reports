# WebGL crashes depending on uniform names

| Field | Value |
|-------|-------|
| **Issue ID** | [40087034](https://issues.chromium.org/issues/40087034) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Blink>WebGL, Internals, Internals>GPU |
| **Reporter** | yu...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2011-01-19 |
| **Bounty** | $500.00 |

## Description

Chrome Version : 8 stable, 9 beta  

**URLs (if applicable) :**  

Other browsers tested: Firefox 4 beta  

**Add OK or FAIL after other browsers where you have tested this issue:**  

**Safari 5:**  

**Firefox 3.x:**  

**IE 7/8:**

**What steps will reproduce the problem?**

1. Open the page attached
2. It will print to console "before link call" and "after link call"
3. Change uniform name "bone\_trans\_before" to "bone\_trans\_before2"  
   
   or "u\_alpha\_discard\_tttt" to "u\_alpha\_discard\_ttt"

**What is the expected result?**  

It must print to console "before link call" and "after link call"

**What happens instead?**  

It print "before link call" and crashes

**Please provide any additional information below. Attach a screenshot if**  

**possible.**

Working fine on Linux, Win XP and Win 7 in Firefox 4 beta 9 and in Chrome 8 with --use-gl=desktop flag, and on Linux in Chrome 8 without that flag

## Attachments

- [crash_test.html](attachments/crash_test.html) (text/html; charset=us-ascii, 1.5 KB)
- [screen.png](attachments/screen.png) (image/png; charset=binary, 177.3 KB)
- [About GPU.htm](attachments/About GPU.htm) (text/html; charset=us-ascii, 6.3 KB)
- [crash_test2.html](attachments/crash_test2.html) (text/html; charset=us-ascii, 1.6 KB)
- [About GPU.htm](attachments/About GPU_52998962.htm) (text/html; charset=utf-8, 6.2 KB)
- [screen.PNG](attachments/screen.PNG) (image/png; charset=binary, 78.3 KB)
- [test3-not-working-vertex.html](attachments/test3-not-working-vertex.html) (text/html; charset=us-ascii, 1.8 KB)
- [test3-not-working-fragment.html](attachments/test3-not-working-fragment.html) (text/html; charset=us-ascii, 1.8 KB)
- [test3-working.html](attachments/test3-working.html) (text/html; charset=us-ascii, 1.6 KB)

## Timeline

### th...@chromium.org (2011-01-19)

- What crashes? Just the tab or the entire browser?
- What OS do you experience the crash on?
- What exact version is crashing for you?
- What command line switches did you pass to the browser?

Can you get a crash report id?
http://dev.chromium.org/for-testers/bug-reporting-guidelines/reporting-crash-bug

### zm...@chromium.org (2011-01-20)

I'll have a look.

### gm...@chromium.org (2011-01-20)

Looking at the shaders this looks like it could be the NVidia bug.

The shader is declaring an array of vec3 but only using 1 element

...
uniform vec3 bone_trans_before[2]; 
void main(void) {
    vec3 newpos  = a_position + bone_trans_before[0];
...

The NVidia drivers see that only 1 element is used and optimize to just 1 element instead of 2 but then report 2 in other places and corrupt memory. This is true of all WIndows Nvidia drivers until at least 11/2010 when the bug was found. (not sure about other OSes but I'd be surprised if it wasn't there too)

Do you happen to be using an NVidia card? if you change

    uniform vec3 bone_trans_before[2]; 

to

   uniform vec3 bone_trans_before[1]; 

does the problem go away?

### zm...@chromium.org (2011-01-20)

[Empty comment from Monorail migration]

### yu...@gmail.com (2011-01-21)

Hi Greg,

Yes I'm using Nvidia cards. In my new test the drivers cannot see how many elements are used but the problem still here.

### yu...@gmail.com (2011-01-21)

I also tried an ATI / Win XP combo

### gm...@chromium.org (2011-01-22)

So I've confirmed this on my machine. Unfortunately it's a memory corruption bug and I'm not sure where the corruption happens. On my work machine it doesn't crash Chrome immediately on link. I crashes sometime after by manipulating the browser. For example opening the dev console sometimes crashes after running this program.

Al's machine, no crash. Ken's machine, no crash. My Macbookpro, no crash.

Will try some other stuff.

### kb...@chromium.org (2011-01-22)

On the hypothesis that it's the NVIDIA bug can you try modifying the shader to reference the last element of the uniform array in the way we figured out earlier?

If that seems to fix the crash then we can try to fix the shader validator to patch up such shaders on NVIDIA hardware.


### yu...@gmail.com (2011-03-01)

I've reproduced this behavior using latest browsers: Firefox 4 beta 12 (always works), Chrome 9.0.597.107 stable, Chrome 11.0.686.0 canary (both crash, work with use-gl=desktop). 

I've also made absolutely minimal shaders and supplied code with compile/link status reporting. There are 3 test files now - one is working and other 2 contain slight changes in uniform names already applied, one in vertex shader and another in fragment one. 

Some findings:

1. This issue supposedly is not card vendor/driver specific as it takes place both on NVidia Quadro FX 1800 and ATI Radeon HD 4550.
2. It happens only on Windows (7 and XP tested), all is ok on Linux (Mac not tested).
3. It happens when OpenGL-to-D3D translator (ANGLE) is used.
4. It seems to be tied to GLSL vector arrays somehow.
5. Lexical subroutines involved. 

Hope this will help.


### yu...@gmail.com (2011-03-01)

[Empty comment from Monorail migration]

### kb...@chromium.org (2011-03-01)

Filed http://code.google.com/p/angleproject/issues/detail?id=122 to track this issue in ANGLE.


### hb...@google.com (2011-03-08)

let's try to fix this for m11.

### kb...@chromium.org (2011-03-09)

If you are experiencing this crash please add yourself to the CC: list for http://code.google.com/p/angleproject/issues/detail?id=122 . TransGaming has been unable to reproduce the crash.


### ka...@google.com (2011-03-09)

rolling non releaseblocker mstone 11 bugs to mstone 12. 

### la...@chromium.org (2011-03-19)

Chrome Version : 8 stable, 9 beta  

**URLs (if applicable) :**  

Other browsers tested: Firefox 4 beta  

**Add OK or FAIL after other browsers where you have tested this issue:**  

**Safari 5:**  

**Firefox 3.x:**  

**IE 7/8:**

**What steps will reproduce the problem?**

1. Open the page attached
2. It will print to console "before link call" and "after link call"
3. Change uniform name "bone\_trans\_before" to "bone\_trans\_before2"  
   
   or "u\_alpha\_discard\_tttt" to "u\_alpha\_discard\_ttt"

**What is the expected result?**  

It must print to console "before link call" and "after link call"

**What happens instead?**  

It print "before link call" and crashes

**Please provide any additional information below. Attach a screenshot if**  

**possible.**

Working fine on Linux, Win XP and Win 7 in Firefox 4 beta 9 and in Chrome 8 with --use-gl=desktop flag, and on Linux in Chrome 8 without that flag

### la...@chromium.org (2011-03-19)

Chrome Version : 8 stable, 9 beta  

**URLs (if applicable) :**  

Other browsers tested: Firefox 4 beta  

**Add OK or FAIL after other browsers where you have tested this issue:**  

**Safari 5:**  

**Firefox 3.x:**  

**IE 7/8:**

**What steps will reproduce the problem?**

1. Open the page attached
2. It will print to console "before link call" and "after link call"
3. Change uniform name "bone\_trans\_before" to "bone\_trans\_before2"  
   
   or "u\_alpha\_discard\_tttt" to "u\_alpha\_discard\_ttt"

**What is the expected result?**  

It must print to console "before link call" and "after link call"

**What happens instead?**  

It print "before link call" and crashes

**Please provide any additional information below. Attach a screenshot if**  

**possible.**

Working fine on Linux, Win XP and Win 7 in Firefox 4 beta 9 and in Chrome 8 with --use-gl=desktop flag, and on Linux in Chrome 8 without that flag

### zm...@chromium.org (2011-03-24)

This might be fixed with Angle r592,r593,r594.  See http://code.google.com/p/angleproject/issues/detail?id=135.

Adding Feature-Security to this bug.

### sc...@gmail.com (2011-03-24)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-03-24)

[Empty comment from Monorail migration]

### kb...@chromium.org (2011-03-30)

[Empty comment from Monorail migration]

### zm...@chromium.org (2011-03-30)

Since Vangelis is doing the merging, re-assign this bug.

### [Deleted User] (2011-03-30)

Created chrome_m11 branch for ANGLE at rev 562, merged in changes 563-571 (M11 branch had actually moved to 571) and 592, 593 that fix the bug. 

Updated 696 buildspec to point to the ANGLE branch @603 in rev 14105:
http://goto.ext.google.com/viewvc/chrome-internal?view=rev&revision=14105





### in...@chromium.org (2011-03-30)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-03-31)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-04-12)

@yuri.ko616: thanks for reporting this issue! Although not originally reported as a Chromium security issue, it does provisionally qualify for a $500 Chromium Security Reward, so thanks and congrats!
Also, is there some name other than "yuri.ko616" you would like us to use to credit you in the release notes?

---
NOTE: normally we do not reward security bugs unless initially filed with the
security template. Sometimes we make an exception for the first time an individual
files a security bug as a non-security issue.
For full guidelines on filing security bugs, see:
http://www.chromium.org/Home/chromium-security/reporting-security-bugs
---

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

### sc...@gmail.com (2011-04-12)

[Empty comment from Monorail migration]

### yu...@gmail.com (2011-04-13)

Thanks. Please use Yuri Ko.

### sc...@gmail.com (2011-06-29)

@yuri.ko616 -- looks like we fixed this a while back; please e-mail cevans@chromium.org for details on how to collect your reward.

### sc...@gmail.com (2011-08-26)

Going to charity (increasing donation to $1337 as is customary in these cases).

### sc...@gmail.com (2011-08-26)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-08-26)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-10-05)

Batch update.

### js...@chromium.org (2012-04-18)

Lifting view restrictions.

### js...@chromium.org (2012-04-18)

Lifting view restrictions.

### js...@chromium.org (2012-04-18)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-09)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### ss...@google.com (2017-02-07)

Moving old issues out of Internal>Graphics to delete this obsolete component (crbug.com/685425 for details)

[Monorail components: -Internals>Graphics Internals>GPU]

### is...@google.com (2017-02-07)

This issue was migrated from crbug.com/chromium/70070?no_tracker_redirect=1

[Multiple monorail components: Blink>WebGL, Internals, Internals>GPU]
[Monorail blocked-on: crbug.com/angleproject/122]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40087034)*
