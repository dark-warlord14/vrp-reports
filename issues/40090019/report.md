# Chromium fails to leave full screen mode

| Field | Value |
|-------|-------|
| **Issue ID** | [40090019](https://issues.chromium.org/issues/40090019) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Input>PointerLock, UI>Browser>FullScreen |
| **Platforms** | Linux |
| **Reporter** | ma...@gmail.com |
| **Assignee** | ct...@chromium.org |
| **Created** | 2017-12-29 |
| **Bounty** | $1,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0

Steps to reproduce the problem:
1. Visit the website logicserverhub.club/USA/chrome/?
2. Click "ignore alert"
3. Read the browser message "Press ESC to leave full screen mode"
4. Try to leave full screen mode by pressing ESC

What is the expected behavior?
Expected behaviour is to ALLWAYS leave full screen mode after pressing the ESC key or other key or keys combination regardless of website content and this being displayed in the browser message.

What went wrong?
Misleading browser message combined with the actual browser behaviour may cause inexperienced user believe he/she is now in his/her desktop environment and then commit a lot of harmful actions.

Did this work before? N/A 

Chrome version: 62.0.3202.94  Channel: stable
OS Version: 3.13.0-125-generic #174-Ubuntu SMP Mon Jul 10 18:51:24 UTC 2017 x86_64 x86_64 x86_64 GNU/Linux
Flash Version: 28.0.0.126

This website is not yet really harmful in comparison with that what may happen is attacker using this technique has enough skills and imagination. Please copy the website sources to your local drive if you are going to investigate as this website may disappear any time.

## Attachments

- [WD.zip](attachments/WD.zip) (application/octet-stream, 334.2 KB)
- [complete.zip](attachments/complete.zip) (application/octet-stream, 547.0 KB)
- [orig.zip](attachments/orig.zip) (application/octet-stream, 425.3 KB)
- [cursor.html](attachments/cursor.html) (text/plain, 1.4 KB)

## Timeline

### el...@chromium.org (2017-12-29)

I have no problem exiting full-screen mode on this site by pressing the ESC key.

Can you reproduce this problem in Chrome 63 stable or later?

[Monorail components: UI>Browser>FullScreen]

### ma...@gmail.com (2017-12-29)

Something has changed in Chrome 63 and now I am able to leave full screen without switching to console and killing chrome. However things are still far from being normal:
1. Pressing ESC is not enough, I have also to click an inactive wesite element to complete leaving full screen. Luckily the attacker forgot to make all the area active :) in this poor example :(.
2. If the browser was opened in the window that wasn't maximized it will get back from full screen in the maximized mode without standard window navigation bar and buttons (I use system bar but see nearly the same using chrome bar), so the only result is that I can see the task bar of the graphics environment and am able to kill chrome from there.
3. Mouse cursor seems to be controlled by the website even outside the website area, so using it may cause some random actions.

I have checked Chrome 64 beta and Chromium 63.0.3239.84. Things are looking there more like in Chrome 63 than 62. Still far from being really safe.

### ma...@gmail.com (2017-12-29)

https://youtu.be/L7usGnELjjQ
What you can't see in this video is the difference between full-screen and "semi-full-screen" I am talking about (00:44). Unfortunately recordmydesktop sees the top bar of the graphics environment all the time. In the "real full screen" however the whole screen is controlled by the website the way someone could think this is real windows.

### ma...@gmail.com (2017-12-30)

[Comment Deleted]

### ma...@gmail.com (2017-12-30)

https://youtu.be/0QkbVrNbs3Q
Another machine and linux install. This time full picture from external camera. The situation even worse: can't quit from full screen with chrome 63.

### me...@chromium.org (2018-01-02)

I was sort of able to reproduce this.

Escape did not exit fullscreen when the small window opened by the initial page was in view (as can be seen in my screenshot). I bet this was because the small window had the focus and was receiving my escape presses, instead of the full screen window I wanted to exit fullscreen.

I couldn't reproduce the bluescreen issue you showed in your video or Esc not working when the small window is not in view, on a fresh ubuntu install. 

Perhaps your setup is contributing to this? Can you reproduce this with the same results (no window in view, unable to exit full screen) on any other platforms?




### pa...@chromium.org (2018-01-03)

On Windows, in a Chrome profile with JavaScript turned off (so no full screen behavior), the site still manages to exert partial control over my mouse movements and the range of motion of my mouse pointer. So we may also have a bug there. I'm not sure how that's possible (I haven't looked at the site's code at all).

[Monorail components: Blink>Input>PointerLock]

### pa...@chromium.org (2018-01-03)

[Empty comment from Monorail migration]

### bo...@chromium.org (2018-01-04)

The site is gone, any chance you could put up the locally saved version for examination?

### ma...@gmail.com (2018-01-04)

Here is locally saved version.

### ma...@gmail.com (2018-01-05)

Unfortunately the uploaded code is incomplete. The content originally rendered by calling blue.php file is missing now and it is why we can see the small window - just because it is broken. I believe this window wasn't originally visible but somehow was able to grab the keyboard and cause fake blue screen flicker on Esc key press. This is also why I failed to save it's content. This makes things really much harder to analyse as we have to guess what was in there and how did it work. And I am sure it worked across two separate linux installations, although was clearly designed to trap MS Windows users.

### me...@chromium.org (2018-01-05)

That's annoying.

Luckily they were nice enough to leave a link to a live version in their source :-)

The live version isn't identical but it seems close enough.

I downloaded a copy of the live version that includes blue.php.

After making a few changes, like changing blue.php to blue.html (I guess it was being served with Content-Type) and fixing some javascript errors I was able to pretty much reproduce your bug.

In my case, the window appears and if I press escape rapidly the full screen window does not exit full screen and eventually the smaller window disappears. Once it is gone, I still cannot exit full screen.

Attached are zip files containing the original downloads (orig.zip) from the site and my modified copy (complete.zip).


### sh...@chromium.org (2018-01-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-01-05)

[Empty comment from Monorail migration]

### sc...@chromium.org (2018-01-09)

[Empty comment from Monorail migration]

### ra...@chromium.org (2018-01-31)

metzman: would you like to take ownership of this issue? 

If not, I think we're lacking in owners of the fullscreen feature. Fullscreen implementations vary quite a bit across platforms so I wonder if this should fall on the platform team (if we have one for linux?).

thestig: do you have ideas about who could look into this? 

The issue mentioned in #7 seems likely to be orthogonal and maybe we should treat it separately. 

### bo...@chromium.org (2018-01-31)

I've been meaning to take a look at the mouse issue since that should fall on the input team. Not sure who should take the Fullscreen issues though.

### pa...@chromium.org (2018-02-06)

Searching for "fullscreen" in files named OWNERS scares up some candidates. :) +cthomp from Enamel.

### mi...@chromium.org (2018-02-06)

It sounds like what might be happening is that the web page is using JavaScript to intercept key presses before the browser-default shortcut keys handle the events. I think we need to ensure that, while Esc may be intercepted by web sites, the browser UI should always handle the event regardless. Something like a "pre-event dispatch handler" (this is implemented in ui::views, IIRC).

Agree we don't have active OWNERS for fullscreen. I don't know how to address this problem.

I would look into this issue myself, since I have the background, but I am way oversubscribed as it is. Sorry. :(

### sh...@chromium.org (2018-02-06)

foolip: Uh oh! This issue still open and hasn't been updated in the last 38 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ct...@chromium.org (2018-02-07)

From a Security UX perspective, the proposal in #19 sounds like a good general measure. We want actions like hitting ESC to be consistent for users (and we train users that ESC can be used in cases like this), so preventing a page from completely masking it sounds good. Are there any compatibility concerns caused by this fix?

I'm not very familiar with this part of the views code, otherwise I might try writing a CL for it. If we still need someone to work on it next week, I can take another look.

### ct...@chromium.org (2018-02-15)

I have the start of a mitigation where the PreEventDispatchHandler catches VKEY_ESCAPE and makes sure at least the fullscreen exit happens. I'll try to have a CL up soon.

### ct...@chromium.org (2018-02-16)

I can't get the POC in #12 to replicate in M66 tip-of-tree. Maybe potentially due to new interventions around window.focus() causing fullscreen to exit (https://crbug.com/chromium/800056)? It is unable to trigger a fullscreen (it sometimes flickers, which is maybe the intervention causing fullscreen to exit). I am also able to exit the popup by clicking the window close button or CTRL+W multiple times.

So roughly, I _can_ replicate it in M64:
Google Chrome	64.0.3282.140 (Official Build) (64-bit)
Revision	a06bc1d5e8e285c70078802de990c1719ccc75e8-refs/branch-heads/3282@{#631}

But I can't replicate it in M66:
Chromium	66.0.3345.0 (Developer Build) (64-bit)
Revision	ae306a012a78c0bcd2f9e87a7d5fc7b263165665-

I can however replicate a weird cursor behavior from this: The replacement pointer can cross out of the webcontents into the omnibox and tab bar, which seems very strange. The page sets a replacement cursor in its CSS using a data url. I've attached an HTML file that just replicates the cursor behavior (in both M64 and M66).

Pausing work on the PreEventDispatchHandler mitigation since I can't repro this anymore on M66.

### sh...@chromium.org (2018-02-16)

[Empty comment from Monorail migration]

### ct...@chromium.org (2018-02-28)

Spent some more time trying to reduce this to a PoC that still works on M66 (66.0.3357.0), but I think the interventions landed (alert() breaking out of fullscreen in https://crbug.com/chromium/670135, focus() breaking out of fullscreen in https://crbug.com/chromium/776418, etc.) prevents this from working.

Marking this as fixed and moving the pointer weirdness concerns to a new bug. Feel free to reopen this if we get a working PoC on M66 or other concerns come up.

### sh...@chromium.org (2018-03-01)

[Empty comment from Monorail migration]

### aw...@google.com (2018-03-06)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-03-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-03-13)

Nice one marada976@! The VRP panel decided to award $1,000 for this report. A member of our finance team will be in touch to arrange payment. Also, how would you like to be credited in our release notes?

### aw...@google.com (2018-03-19)

[Empty comment from Monorail migration]

### ma...@gmail.com (2018-03-26)

It's a great honor for me to be credited in the release notes. Please use my real name and surname. Being honest videos mentioned in the comments #3 and #5 were the only details I have disclosed. Neither it was intended or viewed by the broader public, guessing by the number of views (11 and 17 accordingly). I have made them private after getting the note.

Marcin Adam

### sh...@chromium.org (2018-03-27)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-06-07)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2018-06-07)

This issue was migrated from crbug.com/chromium/798105?no_tracker_redirect=1

[Multiple monorail components: Blink>Input>PointerLock, UI>Browser>FullScreen]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40090019)*
