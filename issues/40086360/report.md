# contentSettings API is too powerful

| Field | Value |
|-------|-------|
| **Issue ID** | [40086360](https://issues.chromium.org/issues/40086360) |
| **Status** | Accepted |
| **Severity** | S0-Critical |
| **Priority** | P4 |
| **Component** | Platform>Extensions |
| **Reporter** | es...@chromium.org |
| **Created** | 2017-01-01 |
| **Bounty** | $1,000.00 |

## Description

A chrome extension, with the help of permissions - contentSettings and activeTab, can grant itself access to all the features like geolocation data, microphone, camera etc. without exclusively asking it from the End User.

**VULNERABILITY DETAILS**

Normally (as per the codebase <https://chromium.googlesource.com/chromium/chromium/+/master/chrome/common/content_settings_pattern.cc#288> ), allowed patterns are:

- [\*.]domain.tld (matches domain.tld and all sub-domains)
- host (matches an exact hostname)
- a.b.c.d (matches an exact IPv4 ip)
- [a:b:c:d:e:f:g:h] (matches an exact IPv6 ip)
- file:///tmp/test.html (a complete URL without a host)

However, the pattern "\*://chrome-extension-ID/\*" can also be passed as primaryPattern and any contentSetting can be set to allow.  

This will be enable the chrome extension calling the method:

chrome.contentSettings.microphone.set({  

primaryPattern: '\*://chrome-extension-ID/\*',  

setting: 'allow'  

}, function(){});

to gain access to the microphone and act as a spyware.

**VERSION**  

Chrome Version: Tested on v53.0.2785.116 and above [stable]  

Operating System: Ubuntu 16.04 (64-bit), Windows 8, Windows 10 (will exist for Mac as well)

## Attachments

- [Screenshot from 2017-01-01 12-17-38.png](attachments/Screenshot from 2017-01-01 12-17-38.png) (image/png, 7.0 KB)
- deleted (application/octet-stream, 0 B)
- [contentSetting-POC.crx](attachments/contentSetting-POC.crx) (application/octet-stream, 1.1 KB)

## Timeline

### pu...@gmail.com (2017-01-01)

[Empty comment from Monorail migration]

### el...@chromium.org (2017-01-01)

[Empty comment from Monorail migration]

[Monorail components: Internals>Permissions Platform>Extensions>API]

### ke...@chromium.org (2017-01-02)

Assigning to meacer@ for triage.

### mm...@chromium.org (2017-01-04)

Looks like a Medium severity ("exposure of sensitive user information that an attacker can exfiltrate").

### sh...@chromium.org (2017-01-04)

[Empty comment from Monorail migration]

### me...@chromium.org (2017-01-04)

This does't seem very different than an extension granting these permissions to a webpage then running a content script on that page and using the APIs. It might even be possible to do this without having any host permissions using weird URL schemes (e.g. add a content setting for a data: URL and then run that data: URL)

The main problem is that the permission warning for the content settings API isn't sufficient. It doesn't indicate that if the extension can change the settings, it can also implicitly use them itself.

Some alternatives are:
1. Prevent a content-setting changing extension from running any content scripts. This might break legitimate extensions.
2. Modify the content settings permission warning to indicate that changing settings imply granting those permissions to the extension, e.g. "Change your settings and access your cookies, JavaScript, plug-ins, geolocation, microphone, camera etc."



### pu...@gmail.com (2017-01-09)

From the last comment, I believe this is considered as an intended feature and the expected change will be an updated Permission warning to the user while installing the extension. Is that correct?

### me...@chromium.org (2017-01-09)

https://crbug.com/chromium/677714#c7: Not necessarily an intended feature. I was just explaining that this isn't different if the extension decides to abuse its "change settings" privilege to change the settings in a way it can abuse them. If we can find a way to prevent that, I'd be okay with it too (though it doesn't seem likely).

### sh...@chromium.org (2017-01-24)

meacer: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### me...@chromium.org (2017-01-24)

Devlin: Any ideas how we should proceed here? The simplest fix is to change the warning, but I'm not sure if it would trigger a "new permission request" dialog.

### me...@chromium.org (2017-02-07)

[Empty comment from Monorail migration]

### pu...@gmail.com (2017-02-16)

Any updates here?
Have you guys come up with a plan or roadmap of what needs to be done?

### pu...@gmail.com (2017-02-19)

I am working on an article detailing the effects of this vulnerability, which I plan to release in first week of March.
I hope you guys can role out a fix before then. 

### do...@chromium.org (2017-02-21)

Pinging extensions people - this bug has gone a bit stale, and it would be good to get a resolution on what should be done.

### sh...@chromium.org (2017-02-22)

meacer: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### me...@chromium.org (2017-02-22)

I'll prepare a patch for the bug in https://crbug.com/chromium/677714#c0. What to do about https://crbug.com/chromium/677714#c6 still remains open.

### rd...@chromium.org (2017-02-22)

@10, *modifying* a permission warning shouldn't result in a "new permission request" dialog, so if we just want to tweak phrasing, we should be okay.  I don't think we'll want to prevent content setting extensions from running scripts.

### ra...@chromium.org (2017-03-07)

[Empty comment from Monorail migration]

[Monorail components: -Internals>Permissions Internals>Permissions>Model]

### me...@chromium.org (2017-03-08)

Patch at https://codereview.chromium.org/2730533002/

### me...@chromium.org (2017-03-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-03-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-04-20)

[Empty comment from Monorail migration]

### pa...@chromium.org (2017-05-01)

[Empty comment from Monorail migration]

### ra...@chromium.org (2017-05-02)

meacer@ and I just chatted about this offline. I don't feel the patch in https://codereview.chromium.org/2730533002/ is the best solution because we're not creating or enforcing a security boundary. Basically, if an extension is given the ability to allow mic/camera for a website, mic/camera can then effectively be delegated back to any extension. I think meacer@ and I are in agreement that granting the power to give access to mic/camera is equivalent to giving the extension the ability to use mic/camera itself (and thus delegate it to any third party).

We think that there are better ways of designing the permissions/API surface that give users a better understanding of what they are giving access to.

My preference for the time being is still to deprecate the mic/camera contentSettings APIs which are only used by ~5 extensions in total. I think it would be better to remove them now while usage is still low and then spend the time necessary to improve the API surface as needed.

If that isn't possible, then a short-term fix may be to prevent extensions from granting websites access to mic/camera and only allow them to block access to mic/camera.

### pa...@google.com (2017-05-03)

Deprecating SGTM, FWIW (not much). :)

### pu...@gmail.com (2017-05-28)

Hey all, 
I am not complaining but its 5 months now since I filed this bug and I don't see any clarity on what needs to be done.
I agree there can be many ways to look at this and each solution has its own set of pros and cons. Taking decision on what will be the best certainly takes time.

My original concern was that the contentSettings API seemed to have too much power. It felt like the sudo. As much as it may help good developers write utilities, such amount of power will easy the life of malware developers as well.

### ra...@chromium.org (2017-05-28)

msramek: I just realized you weren't on this thread. What are your thoughts on #24?

### ms...@chromium.org (2017-05-31)

So I've been thinking about this a bit more, and I see the problem manifesting in two stages.

1: The user installs an extension, which has install-time permissions. Those do not involve a camera. However, the extension is also its own origin, and thus it can use content settings to grant a camera permission for that origin, i.e. for itself. Or for other extensions that also shouldn't have had access.

This is a problem where two permission models clash (the install-time extension permissions and the run-time content settings), and it can be solved by making only one of them apply. Specifically, content settings (or at least some of them) could simply not apply for extensions, be always blocked. This is already the case for the JavaScript setting, which doesn't work on extensions - JavaScript is always allowed.

We could then turn some of the content settings into regular extension permissions, if needed.

2. The second problem mentioned is that the website can still use a trick where it grants the permission to another origin, and then reads data from data origin thanks to the activeTab or <all_urls> permissions. However, in this case, I think the culprit is not the contentSettings API - it's the other APIs that make that fundamental cross-origin step. Even with the contentSettings API, the extension can gain access to camera/mic data by injecting code into another origin that already has the permission. Or injecting a code that triggers a permission request and tricking you to click it for whatever reason.

Or do worse things, like stealing your passwords. These APIs are designed while thinking about an extension as an extension of the browser, so I'm not sure if thinking about security boundaries applies in the usual way.

I am personally not surprised that if I grant an extension access to "allow camera on any page" and "read content on any page", the extension will be able to gain access to camera in a roundabout way as well. If we think this should be made clearer to users, let's improve the permission strings. And if we introduce an install-time permission for camera, let's make it a precondition for granting camera access to other websites using the contentSettings API.

I just think that deprecating the camera/mic contentSettings APIs is a quick patch that might solve this particular problem, but the justification with a security boundary misses the point a bit about how extensions work.

THAT SAID, if everybody thinks that deprecation makes sense to mitigate malware risk before we think of something better, and Devlin is fine with that, I won't keep pushing against that.

### ra...@chromium.org (2017-06-04)

> However, in this case, I think the culprit is not the contentSettings API - it's the other APIs that make that fundamental cross-origin step.

I'm not quite sure I agree. There are other communication channels that can be used to gain access. Even if the extension didn't have access to these APIs, it could just communicate with a site through a side-channel (e.g. a remote server). 

> I am personally not surprised that if I grant an extension access to "allow camera on any page" and "read content on any page", the extension will be able to gain access to camera in a roundabout way as well. If we think this should be made clearer to users, let's improve the permission strings.

I agree with you on this though. If I read the message carefully, it does not seem surprising to me that the extension can access mic/camera itself. However, I still think it's problematic from the standpoint that the contentSettings permission is too big of a hammer especially if we were to add all other content settings to it. See #26:

> My original concern was that the contentSettings API seemed to have too much power. It felt like the sudo. As much as it may help good developers write utilities, such amount of power will easy the life of malware developers as well.

I agree with this and I don't think it's good that granting one permission gives potential access to everything.

> I just think that deprecating the camera/mic contentSettings APIs is a quick patch that might solve this particular problem, but the justification with a security boundary misses the point a bit about how extensions work.

I think we are probably coming from different perspectives on the value of the extensions contentSettings API and I think we should try to resolve those before making any big decisions :) In the short term I don't want to step on toes by removing the API if you're not comfortable. But also in the interest of a short-term fix I would suggest that we limit extensions to only blocking camera/mic (not allowing) and that we avoid adding any new content settings to the API until we've had a larger discussion about the future of the API. How does that approach sound to you?

### sh...@chromium.org (2017-06-06)

[Empty comment from Monorail migration]

### pu...@gmail.com (2017-06-07)

Hey. Just curious, am I eligible for the bug bounty? :P 

### ra...@chromium.org (2017-06-07)

+awhalley for #31

### aw...@chromium.org (2017-06-07)

Hi punit.g7@ - we mark bugs for VRP reward consideration once they are marked as fixed, but yes, once this one is it should go up before the panel.

### ms...@chromium.org (2017-06-08)

It's not that I'm not comfortable removing the API, but

a) I'm not even sure deprecation is a short-term process (you need to make announcements first etc., otherwise extensions will break overnight and no one will ever trust CWS to be a reliable platform).

b) Removing camera and microphone really only addresses this particular bug. If punit.g7@ filed the very same complaint about location, we would be talking about location today. So singling out camera/mic seems even a bit irrational. Let's go over all content settings and evaluate risks created by extensions for each of them.

For the short term, I agree that limiting extensions to ASK/BLOCK might be a good step.

For the long term, we really do need to unify our views on extension APIs. I'm all in for making extensions safer, I just don't think that's how they were designed and how they work today. (And we had these conversations in my team before.)

So - what does Devlin think?

### pu...@gmail.com (2017-07-23)

Knock knock! Any updates?

### ra...@chromium.org (2017-07-24)

I think we're in agreement that we should limit the extension to ASK/BLOCK for now, is that right?

msramek,rdevlin.cronin: could you confirm you're ok with that solution?

### ms...@chromium.org (2017-07-24)

I'm fine with it as a quick fix.

### rd...@chromium.org (2017-07-25)

@36 sorry, was traveling yesterday.

Do we have an idea about how many extensions this might break?  If it's a low number, I'm fine with it as a band-aid.

### ra...@chromium.org (2017-07-26)

As per #24 it was only about ~5 extensions as of 2 months ago.

### me...@chromium.org (2017-07-26)

This will also break my own "click to enable JavaScript" extension :) (context at https://crbug.com/chromium/657565)

Are we going to block ALLOW setting for all permissions? Can we at least allow it for on-by-default permissions such as Images, JavaScript and cookies? The risk of an extension granting these permissions to itself is minimal to none.

### ra...@chromium.org (2017-07-26)

meacer: this would just be for mic/camera for now, nothing else.

### me...@chromium.org (2017-07-26)

raymes: Yes, sorry.

Is anyone interested in doing this? I might not get to it very soon.

### ra...@chromium.org (2017-07-26)

I already have a patch up at: https://chromium-review.googlesource.com/c/583955/ :)

### me...@chromium.org (2017-07-26)

Thanks raymes, then I hope you don't mind me assigning this to you :)

### sh...@chromium.org (2017-07-26)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-09-06)

[Empty comment from Monorail migration]

### pu...@gmail.com (2017-09-17)

Doesn't 9 months seem to be a long time for an issue? :)

### pu...@gmail.com (2017-10-10)

Knock knock. Another month passed by.

### ra...@chromium.org (2017-10-10)

Sorry for some reason the CL that I had put up for this never got landed. This isn't the highest priority thing for me but I will be looking at it next month.

### sh...@chromium.org (2017-10-18)

[Empty comment from Monorail migration]

### es...@chromium.org (2017-11-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-12-07)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-01-25)

[Empty comment from Monorail migration]

### ca...@chromium.org (2018-02-08)

[Empty comment from Monorail migration]

### in...@chromium.org (2018-02-14)

meacer@, raymes@ - are you planning to work on this ?

### ra...@chromium.org (2018-02-15)

I still haven't had a chance to get back to this. It probably won't be for a few weeks at least. If someone else wants to pick up the CL feel free: https://chromium-review.googlesource.com/c/583955/ 

### es...@chromium.org (2018-02-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-07)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-04-19)

[Empty comment from Monorail migration]

### pu...@gmail.com (2018-05-05)

Its been one-and-a-half years! Cheers! :D

### sh...@chromium.org (2018-05-30)

[Empty comment from Monorail migration]

### pu...@gmail.com (2018-06-12)

@raymes Any hopes ??

### ts...@chromium.org (2018-06-27)

+Ben, maybe someone else besides raymes has time to work on this?

### sh...@chromium.org (2018-07-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-09-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-10-17)

[Empty comment from Monorail migration]

### ra...@chromium.org (2018-12-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-12-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-01-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-04-24)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-06-06)

[Empty comment from Monorail migration]

### me...@chromium.org (2019-06-13)

Pinged Raymes offline.

### ra...@chromium.org (2019-06-13)

I'm no longer working on content settings. Perhaps chat with engedy@ or msramek@?

### me...@chromium.org (2019-06-13)

engedy: Is this something the permissions team can own? Raymes had a patch earlier in the thread that could be picked up.

### me...@chromium.org (2019-06-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-07-31)

[Empty comment from Monorail migration]

### jd...@chromium.org (2019-08-19)

engedy@: friendly ping from the security marshal. Is permissions able to take this on?

### en...@chromium.org (2019-08-21)

Yeah, let's see if we can work out a solution for M79.

### sh...@chromium.org (2020-02-05)

[Empty comment from Monorail migration]

### pu...@gmail.com (2020-02-08)

Hey guys -- It has been 3 years. Has this been resolved separately in another thread or change request ?

### aw...@google.com (2020-02-18)

+ this week's sheriff to see where we are with this.

### aj...@google.com (2020-02-24)

+ next week's sheriff (sorry) because this week ended up being very busy. engedy - how is progress on this longstanding issue?

### [Deleted User] (2020-04-09)

[Empty comment from Monorail migration]

### [Deleted User] (2020-05-20)

[Empty comment from Monorail migration]

### [Deleted User] (2020-07-14)

engedy: Uh oh! This issue still open and hasn't been updated in the last 327 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-07-16)

[Empty comment from Monorail migration]

### [Deleted User] (2020-07-28)

engedy: Uh oh! This issue still open and hasn't been updated in the last 341 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-08-26)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-07)

[Empty comment from Monorail migration]

### bd...@chromium.org (2020-10-13)

friendly marshal, are there any updates?

### [Deleted User] (2020-10-30)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-18)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-20)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### wf...@chromium.org (2021-02-24)

given raymes had a patch up, I'm reassigning the bug to them. I wonder if there was an update here? Can devlin comment also perhaps?

### va...@chromium.org (2021-02-24)

[Empty comment from Monorail migration]

### ra...@chromium.org (2021-02-24)

I haven't worked on content settings/permissions in many years now!

Please chat with engedy@ to work out a path forward.

### [Deleted User] (2021-03-03)

[Empty comment from Monorail migration]

### en...@chromium.org (2021-03-10)

Ravjit, Illia, can you please look into this? There is a proposed CL in https://crbug.com/chromium/677714#c56 with a band-aid fix that folks above reached consensus on, we should clean it up and land it.

### [Deleted User] (2021-03-11)

[Empty comment from Monorail migration]

### zh...@google.com (2021-03-17)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-15)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-26)

[Empty comment from Monorail migration]

### ad...@google.com (2021-07-08)

[Empty comment from Monorail migration]

### ct...@google.com (2021-07-21)

ravjit@ friendly ping about this long-standing Severity-Medium bug. It would be great to fix up this long-standing issue (although the previous WIP CL may be a bit stale now).

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

### ra...@chromium.org (2021-08-18)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-11)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-22)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-15)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-02)

[Empty comment from Monorail migration]

### ca...@chromium.org (2022-03-03)

Friendly security marshal ping, taking a look at the CL it seems for the most part it should still be patchable. Are there are any blockers to picking up that work? This is our second oldest open security bug.

### [Deleted User] (2022-03-30)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-25)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-06-29)

Friendly neighborhood security marshal ping -- it looks like a patch was started (https://chromium-review.googlesource.com/c/chromium/src/+/583955/) and needs some additional work. Since this is our second oldest security bug and opened since 2016, it would be great to get some traction here and button this one up. 
Even if this cannot be worked on immediately, but getting this onto y'alls' roadmap and setting a ballpark next action date would be most helpful (and allow you to avoid additional pings from us). Thank you! 



### ts...@chromium.org (2022-07-20)

mkwst - CC'ing you as you might have an opinion on domain/pattern matching and whether we need to do anything here.

### aw...@google.com (2022-07-21)

CC'ing clamy@ for the same reason as https://crbug.com/chromium/677714#c122

### [Deleted User] (2022-08-03)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-28)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-30)

[Empty comment from Monorail migration]

### ad...@chromium.org (2022-12-01)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-08)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-05)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-31)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-16)

[Empty comment from Monorail migration]

### es...@chromium.org (2023-10-11)

This week's security shepherd here. I've been looking at this ancient bug and was going to try get https://chromium-review.googlesource.com/c/chromium/src/+/583955 picked up and landed. However, reading the bug and looking at the patch, I'm not sure that's a good course of action:

- It could be that this is a more breaking change now than it was in 2017 or whenever
- Also, as msramek@ mentioned in an earlier comment, this only addresses the problem for camera/mic; I feel like we'd still want to keep the bug open even after landing the patch because of e.g. geolocation

I'm going to check with the extensions team to see if there are changes to this API in MV3. I feel like the quick fix/band-aid solution is really to change the permissions string to make it clear that the extension can access the permissions as well -- though obviously that's not a great fix.

### [Deleted User] (2023-10-11)

[Empty comment from Monorail migration]

### es...@chromium.org (2023-10-11)

[Empty comment from Monorail migration]

### tj...@chromium.org (2023-10-11)

oliverdunk@: As per https://crbug.com/chromium/677714#c132, do you know if usage of chrome.contentSettings to set the setting for microphone and camera to "allow" has changed much in recent times?

### ol...@chromium.org (2023-10-12)

tjudkins@: Hey Tim, I took a quick look and I definitely get the feeling usage has increased:

https://chrome.google.com/webstore/detail/online-security/llbcnfanfmjhpedaedhbcnpgeepdnnok (10M users) appears to use this for some sort of permissions UI.

https://chrome.google.com/webstore/detail/honorlock/hnbmpkmhjackfpkpcbapafmpepgmmddc (1M users) appears to use this to grant access to certain exam websites.

https://chrome.google.com/webstore/detail/amazing-screen-recorder/cdepgbjlkoocpnifahdfjdhlfiamnapm (1M users) actually does exactly what we are discussing in this issue and uses it to grant itself camera permissions.


### es...@chromium.org (2023-10-13)

Hm, per internal email thread I was going to suggest that the next step might be to add UMA metrics for extensions granting themselves permissions via contentSettings API, but it sounds like that might be unfortunately common now. Perhaps the best band-aid fix is to change the permissions string to make it more clear that it gives the extension itself privileges.

### tj...@chromium.org (2023-10-16)

I agree that changing the permission string seems like a good step for now that will at least leave things better than they are currently. It's still important though to decide if this is a capability we want exposed through here and if now what the path would be to remove it without causing too much impact to these extensions which are using it currently.

### [Deleted User] (2023-12-06)

[Empty comment from Monorail migration]

### ja...@chromium.org (2023-12-12)

[Secondary security shepherd]

Hi ravjit@, does the proposal in https://crbug.com/chromium/677714#c137 work for you? If it sounds good but you aren't the right owner, can you pass it to the right person?

Thanks!

### ha...@google.com (2024-01-04)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-05)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-05)

[Empty comment from Monorail migration]

### yu...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

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

### [Deleted User] (2024-01-10)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-11)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-11)

This issue was migrated from crbug.com/chromium/677714?no_tracker_redirect=1

[Multiple monorail components: Internals>Permissions>Model, Platform>Extensions>API]
[Monorail components added to Component Tags custom field.]

### el...@chromium.org (2024-05-09)

Security shepherd: hey ravjit@ - do we have any sort of path forward here? this one has been open for quite a while :)

### pu...@gmail.com (2024-06-12)

I wish I could make an NFT out of this thread! :-D

Hey folks, I had reported this issue.

Now, given that the security around this method has improved a lot, the severity of this vulnerability is not as much.
Clearly, we have survived 7 years without touch the core function. 
Chromium is at v125 now.

Unless, this poses a risk for Electron or Chrome Apps in any manner, it should be fine to let it stay as an appendix.

What do you think ?

### so...@chromium.org (2024-06-28)

I just sent the assignee a message to get their take on this.

### jd...@chromium.org (2024-07-11)

Hi engedy@ -- can you help find some cycles for this bug? It's our longest-standing security bug of its severity, and [comment #138](https://issues.chromium.org/issues/40086360#comment138) has a pretty tactical and straightforward fix that might help a bit at least. Thanks!

### am...@chromium.org (2024-08-19)

hi engedy@ and ravjit@ -- I wanted to follow up on this. This is our oldest medium severity security issue. Since c#138 is a pretty tactical way forward it would be great if this could be resolved or assigned to someone with more immediate implementation cycles given it's age.

### es...@chromium.org (2024-08-19)

(Sorry I didn't update the bug: I revived an email thread about this last week, and made a proposal for a string change, which is at least a short-term band-aid. Unless I get strong objections, I'll just go ahead and make that change ~this week.)

### am...@chromium.org (2024-08-19)

Oh fantastic -- thanks so much for the update and also taking this on!

### ap...@google.com (2024-08-29)

Project: chromium/src
Branch: main

commit 34a2937e30659b6d5616d881f3be0f93b4a59c47
Author: Emily Stark <estark@google.com>
Date:   Thu Aug 29 04:11:21 2024

    Add metrics for chrome.contentSettings extension usage
    
    This CL adds metrics for how often chrome-extension:// origins are
    used to set content settings via the chrome.contentSettings API, to
    see if this can be deprecated.
    
    Bug: 40086360
    Change-Id: Ide2b22a6e628fd8bebbd227032e5e4c7264c1c1d
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5814282
    Reviewed-by: Balazs Engedy <engedy@chromium.org>
    Reviewed-by: Devlin Cronin <rdevlin.cronin@chromium.org>
    Reviewed-by: Kelvin Jiang <kelvinjiang@chromium.org>
    Commit-Queue: Emily Stark <estark@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1348438}

M       extensions/browser/api/content_settings/content_settings_store.cc
M       extensions/browser/api/content_settings/content_settings_store_unittest.cc
M       extensions/test/DEPS
M       extensions/test/extensions_unittests_main.cc
M       tools/metrics/histograms/metadata/extensions/histograms.xml

https://chromium-review.googlesource.com/5814282


### es...@chromium.org (2024-08-29)

Summarizing from some internal discussion:

- As can be seen from #191, we're investigating whether it is uncommon enough for extensions to grant themselves permissions via a chrome-extension:// URL that we could just deprecate the use of chrome-extension:// URLs with the chrome.contentSettings API.
- Assuming we can go ahead and do that, it's not that satisfying of a solution. An extension that owns example.com could still use the chrome.contentSettings API to grant permissions to example.com and then navigate to example.com -- indirectly getting access to the same capabilities.
- We've discussed ways to tweak the permission string to capture these subtleties, but it's difficult to explain and in any case it's hard to believe that finding the perfect string would be the difference between success and failure of a malicious extension.
- We'll likely pursue deprecating chrome-extension URLs from the API and/or a string change as a short-term fix for this bug, but ultimately the contentSetting API will need to be locked down in a longer-term effort -- for example, migrating to an API where the user approves individual origins for which the extension can change settings.

### es...@chromium.org (2024-08-29)

Setting NextAction for when we will have data from stable.

### pe...@google.com (2024-11-01)

The NextAction date has arrived: 2024-11-01
To opt-out from this automation rule, please add Optout-Blintz-Nextaction-Alert to the "Chromium Labels" custom field.

### ap...@google.com (2024-11-19)

Project: chromium/src  

Branch: main  

Author: Emily Stark <[estark@google.com](mailto:estark@google.com)>  

Link:      <https://chromium-review.googlesource.com/6026952>

Add metrics for chrome.contentSettings extension usage, take 2

---


Expand for full commit details
```
Add metrics for chrome.contentSettings extension usage, take 2 
 
https://chromium-review.googlesource.com/c/chromium/src/+/5814282 
added metrics to try to measure extensions that were granting 
themselves content settings. However, granting settings via a 
'chrome-extension://<id>' URL is not allowed; it's only through a 
wildcard scheme that an extension can grant itself content 
settings. This CL revises the metrics to record when an extension uses 
a content settings pattern that matches its own origin. 
 
OBSOLETE_HISTOGRAMS=Extensions.ContentSettings.[Primary|Secondary]PatternChromeExtensionScheme are replaced with [Primary|Secondary]PatternMatchesExtensionOrigin 
 
Bug: 40086360 
Change-Id: I92bc7065fc935c674f323a1c1e7641f922faaa79 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6026952 
Reviewed-by: Christian Dullweber <dullweber@chromium.org> 
Commit-Queue: Emily Stark <estark@chromium.org> 
Reviewed-by: Kelvin Jiang <kelvinjiang@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1384752}

```

---

Files:

- M `extensions/browser/api/content_settings/content_settings_store.cc`
- M `extensions/browser/api/content_settings/content_settings_store_unittest.cc`
- M `tools/metrics/histograms/metadata/extensions/histograms.xml`

---

Hash: 133d86129664dc30af9ce2fb2d36f6de4874d5a4  

Date:  Tue Nov 19 03:58:07 2024


---

### es...@chromium.org (2024-11-19)

Requesting a merge for <https://chromium-review.googlesource.com/6026952> (adding metrics)

### pe...@google.com (2024-11-19)

Merge review required: a commit with DEPS changes was detected.

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
Owners: govind (Android), govind (iOS), alonbajayo (ChromeOS), srinivassista (Desktop)

### am...@chromium.org (2024-11-19)

Since this is just adding metrics, approving this now. Please merge to branch 6834 ASAP if you'd like to get to get this into beta sooner, as there is a release freeze next week starting this Friday.

### ap...@google.com (2024-11-20)

Project: chromium/src  

Branch: refs/branch-heads/6834  

Author: Emily Stark <[estark@google.com](mailto:estark@google.com)>  

Link:      <https://chromium-review.googlesource.com/6034425>

Add metrics for chrome.contentSettings extension usage, take 2

---


Expand for full commit details
```
Add metrics for chrome.contentSettings extension usage, take 2 
 
https://chromium-review.googlesource.com/c/chromium/src/+/5814282 
added metrics to try to measure extensions that were granting 
themselves content settings. However, granting settings via a 
'chrome-extension://<id>' URL is not allowed; it's only through a 
wildcard scheme that an extension can grant itself content 
settings. This CL revises the metrics to record when an extension uses 
a content settings pattern that matches its own origin. 
 
OBSOLETE_HISTOGRAMS=Extensions.ContentSettings.[Primary|Secondary]PatternChromeExtensionScheme are replaced with [Primary|Secondary]PatternMatchesExtensionOrigin 
 
(cherry picked from commit 133d86129664dc30af9ce2fb2d36f6de4874d5a4) 
 
Bug: 40086360 
Change-Id: I92bc7065fc935c674f323a1c1e7641f922faaa79 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6026952 
Reviewed-by: Christian Dullweber <dullweber@chromium.org> 
Commit-Queue: Emily Stark <estark@chromium.org> 
Reviewed-by: Kelvin Jiang <kelvinjiang@chromium.org> 
Cr-Original-Commit-Position: refs/heads/main@{#1384752} 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6034425 
Auto-Submit: Emily Stark <estark@chromium.org> 
Commit-Queue: Christian Dullweber <dullweber@chromium.org> 
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
Cr-Commit-Position: refs/branch-heads/6834@{#603} 
Cr-Branched-From: 47a3549fac11ee8cb7be6606001ede605b302b9f-refs/heads/main@{#1381561}

```

---

Files:

- M `extensions/browser/api/content_settings/content_settings_store.cc`
- M `extensions/browser/api/content_settings/content_settings_store_unittest.cc`
- M `tools/metrics/histograms/metadata/extensions/histograms.xml`

---

Hash: 7ba02e91435f82305b10426639fdb480fb275aca  

Date:  Wed Nov 20 12:03:25 2024


---

### ar...@chromium.org (2024-12-13)

**(Secondary Security Shepherd)**

Hi [estark@chromium.org](mailto:estark@chromium.org),

I'm following up on a patch you merged two months ago that added metrics for this bug. Thanks!

I'm just checking in to see if you've had a chance to analyze the results of these metrics. I've taken a look at the associated histogram ([link to histogram](https://uma.googleplex.com/p/chrome/timeline_v2?sid=c6f1a6c18e9aa1ee841b0680caadc303)), but haven't seen any data yet. There are a few possibilities:

- The metric might not be recording data yet.
- There could be a bug in the implementation.
- The histogram I'm looking at might not be the correct one.

Would you be able to share any insights you've gained from the metric data, if any?

Thanks,

### es...@chromium.org (2024-12-13)

Hey Arthur - there was a bug in the first patch I landed that added metrics, and the follow-up CL (<https://chromium-review.googlesource.com/6034425>) isn't in stable yet. I have a NextAction date set on the bug to check the fixed metrics in stable at the end of January.

### ar...@chromium.org (2024-12-13)

👍 Thanks Emily!

Let's wait until 2025-01-28 for the results.

### pe...@google.com (2025-01-28)

The NextAction date has arrived: 2025-01-28
To opt-out from this automation rule, please add Optout-Blintz-Nextaction-Alert to the "Chromium Labels" custom field.

### ap...@google.com (2025-02-14)

Project: chromium/src  

Branch: main  

Author: Emily Stark <[estark@google.com](mailto:estark@google.com)>  

Link:      <https://chromium-review.googlesource.com/6270737>

Change permission string for contentSettings extension API

---


Expand for full commit details
```
Change permission string for contentSettings extension API 
 
This CL changes the permission string for extensions that use the 
contentSettings API. The point of the change is to make it more clear 
that this API can allow extensions to grant themselves permissions via 
a wildcard scheme. Ideally we will change this behavior in the future 
to not allow extensions to grant themselves permissions via 
contentSettings -- and to secure the contentSettings API more 
generally -- but this would be a larger breaking change that needs 
some coordination and deprecation timelines in place. 
 
Bug: 40086360 
Change-Id: Id3180c275fc1cc2b6420ec38423ddf4095e19ec1 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6270737 
Reviewed-by: Balazs Engedy <engedy@chromium.org> 
Commit-Queue: Emily Stark <estark@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1420761}

```

---

Files:

- M `chrome/app/generated_resources.grd`
- A `chrome/app/generated_resources_grd/IDS_EXTENSION_PROMPT_WARNING_CONTENT_SETTINGS.png.sha1`

---

Hash: d2dfa6c653e88758c80530d5edfa464c5e865e98  

Date:  Fri Feb 14 14:56:44 2025


---

### es...@chromium.org (2025-02-14)

The metrics added in #199 show that usage of this bug is actually quite high (i.e., it's quite common for users to use extensions that grant themselves permissions via contentSettings API). I've therefore made a change to the permission string to make it more clear that this capability exists (#204).

This is an unsatisfying resolution to this bug for two reasons: (1) it's not clear that the string change will make any difference in users' willingness to install extensions that abuse this bug, and (2) the contentSettings API is scary regardless of this bug. Even if this bug were fixed such that extensions couldn't directly grant themselves capabilities via contentSettings API, an extension with control of evil[.]com could use the contentSettings API to grant permissions to evil[.]com, and then the extension could open evil[.]com and the website would gain access to sensitive data or powerful capabilities. This would potentially be noisier than the extension using the capabilities directly, but still scary.

I'm therefore going to close out this bug and open a separate (public) one for larger-scale contentSettings lockdown, which would likely involve some outreach effort and phased deprecation timelines.

Thanks for the report!

### es...@chromium.org (2025-02-14)

Follow-up bug is <https://issues.chromium.org/issues/396612321>

### pg...@google.com (2025-02-18)

Not sure if there are string/i18n related schedule things blocking string change backmerges, but merge approved for M134! Adding merge label manually since automation likely will see other "merged" labels and think it has done its job.

### es...@chromium.org (2025-02-18)

@pgrace I think maybe something got confused because of a merge request for a previous CL (adding metrics) on this bug. I don't think we need a merge for the fix (in #204). i.e., no merge needed at the moment.

### sp...@google.com (2025-02-20)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
reward for report issue that resulted in some long-term considerations contentSettings API and potential abuse of it by extensions 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-02-20)

Despite this issue not being truly resolved, we did want to acknowledge this report with a small reward, albeit quite some time since you submitted this issue back in 2016.

### pg...@google.com (2025-03-29)

@repoter, how would you like to be credited for this report?

### ch...@google.com (2025-05-24)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> reward for report issue that resulted in some long-term considerations contentSettings API and potential abuse of it by extensions

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086360)*
