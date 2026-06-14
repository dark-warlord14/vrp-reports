# Security: Loading mixed content without insecure warning

| Field | Value |
|-------|-------|
| **Issue ID** | [40092040](https://issues.chromium.org/issues/40092040) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>Media>Video, Internals>Media>Network, UI>Browser>Omnibox>SecurityIndicators |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | re...@gmail.com |
| **Assignee** | da...@chromium.org |
| **Created** | 2018-07-26 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

The site seems secure but is loading mixed / insecure content.

The first time loading a page, the page is flagged unsecure. When a page refresh happens the page is flagged secure.  

To get the secure flagged page a refresh can be done through the meta refresh or a JavaScript reload.  

Sometimes the page needs to be refreshed twice to get the secure flag.

With the secure flag and mixed content the page is vulnerable for the man in the middle attack and the SSL security is bypassed.

**VERSION**  

Chrome Version: 67.0.3396.99 (Official Build) (64-bit) (tested on multiple versions)  

Operating System: Windows 10 Home 64 bit, Version 1803 (build 17134.165)

**REPRODUCTION CASE**  

<https://innzorg.nl/mixedmp4.html> Page is flagged secure, loading unsecure / mixed content

<https://innzorg.nl/mixedjs.html> Page is flagged secure, loading unsecure / mixed content  

(trying to load js from unsecure source) But still secure!

<https://innzorg.nl/mixedpng.html> (no problems with a refresh)  

<https://innzorg.nl/mixedjpg.html> (no problems with a refresh)

## Attachments

- [mixedmp4.html](attachments/mixedmp4.html) (text/plain, 350 B)
- [mixedjs.html](attachments/mixedjs.html) (text/plain, 235 B)
- [mixedpng.html](attachments/mixedpng.html) (text/plain, 283 B)
- [2018-07-31 12-11-04.mp4](attachments/2018-07-31 12-11-04.mp4) (video/mp4, 3.9 MB)

## Timeline

### mb...@chromium.org (2018-07-27)

[Empty comment from Monorail migration]

[Monorail components: UI>Browser>Omnibox>SecurityIndicators]

### mb...@chromium.org (2018-07-27)

[Empty comment from Monorail migration]

### mb...@chromium.org (2018-07-27)

cthomp: Any idea who the right owner for this would be? Punting to you since I see that you're the enamel sheriff this week, but feel free to reassign to me for triage if you aren't sure who should take it.

### me...@google.com (2018-07-27)

I was looking at this now.

> https://innzorg.nl/mixedmp4.html Page is flagged secure, loading unsecure / mixed content  

I'm unable to repro on Win 10 with Chrome 67 & 68. I see a flash of the Secure badge on page load, but it's immediately hidden.

> https://innzorg.nl/mixedjs.html Page is flagged secure, loading unsecure / mixed content

This is expected. The JavaScript code, being active content, is never run so the page still displays a secure badge.

remkoboonstra@: Are you trying the first case with a clean profile? If you have extensions running, they could be causing the problem (e.g. by blocking the subresource fetch).

### sh...@chromium.org (2018-07-28)

[Empty comment from Monorail migration]

### re...@gmail.com (2018-07-31)

I have tried the case with a clean profile, no extensions of plugins running.

In the attached file I added a video of the issue. You can see that the page is loaded with the flag unsecure. When the page reloads after 5 seconds (http refresh content 5) the page is flagged secure. The page refresh can be done with JavaScript or http refresh tag. I have set the refresh time at 5 seconds to clearly see the change in status. 

The refresh can be done faster so the user doesn’t notice the page refresh and assumes the page is secure.


### ct...@chromium.org (2018-07-31)

I can reproduce the behavior of https://innzorg.nl/mixedmp4.html on Linux Dev opening it in an incognito window. The EV badge displays and the video loads after the refresh triggers.

The fact that this isn't happening for PNG/JPG (<img> elements) but is happening for <video> elements makes me wonder if there's a weird interaction of media and our mixed content checks. Maybe something involving caching? In particular, the devtools Network Tab (with cache disabled) shows requests to the video source only _before_ the page reloads that flip the EV indicator back on.

I'll try to dig more soon or loop in media team people who may know more.

[Monorail components: Blink>Media>Video]

### ct...@chromium.org (2018-08-01)

cc'ing some folks who are more familiar with our mixed content logic.

Mike or Carlos: Any ideas why this would be happening with <video> sources?

### ct...@chromium.org (2018-08-01)

Also cc mlamouri who is owner of blink/renderer/core/html/media. Do you have any ideas about the loading/caching behavior I describe in #7 that appears to only be happening for <video> sources?

### ml...@chromium.org (2018-08-02)

+hubbe@ who is the network expert for media.

### hu...@chromium.org (2018-08-03)

There is a client-side cache for videos, which is separate from the image cache. Sounds like this cache needs to have some code to do mixed content checks?


### ct...@chromium.org (2018-08-06)

hubbe@ I'll assign this to you for now, but I'm happy to help figure out the mixed content checks if you can point me to the right parts of the code for the cache here.

### hu...@chromium.org (2018-08-06)

The cache lives in media/blink/url_index.{h,c}


### ca...@chromium.org (2018-08-10)

I've been looking at this one, and it looks like on the first access the cache creates a URLLoader (here it seems: https://cs.chromium.org/chromium/src/media/blink/resource_multibuffer_data_provider.cc?rcl=d30286c2a870ae693860e3258ce50dd9ac93c03c&l=146), which results in the mixed content check going through as normal (since the URLLoader eventually calls blink::MixedContentChecker::ShouldBlockFetch()).

Would there be a good place to call MixedContentChecker::ShouldBlockFetch() from the cache when the load is happening without a URLLoader? 

### hu...@chromium.org (2018-08-10)

Hmm, I don't know what ShouldBlockFetch() does since it lacks documentation, but I suspect that the right place to call it is media::UrlIndex::GetByUrl(). If false is returned, I assume we can just fail the cache lookup and create an empty cache entry which will eventually create an UrlLoader....


### hu...@chromium.org (2018-08-20)

Grr, it seems difficult to call ShouldBlockFetch() from inside media::UrlIndex::GetByUrl() since someone went through a bunch of throuble replacing the WebFrame that used to be there with a ResourceFetchContext. The ResourceFetchContext knows has to create a resource loader, but nothing else, which means that I don't have a way to know the frame type, among other things.
Is the frame type important?


### hu...@chromium.org (2018-08-20)

+alokp

I guess I need to add ShouldBlockFetch() to ResourceFetchContext, does that sound reasonable?


### hu...@chromium.org (2018-09-19)

ping?


### hu...@chromium.org (2018-09-24)

ping?


### ca...@chromium.org (2018-09-27)

It looks like alokp is no longer part of the team.

As for calling ShouldBlockFetch, I think the frame type is important for the decision, but I'll let mkwst correct me if I'm wrong on that.

Another thought is you might be able to somehow store whether a particular cached resource was fetched over HTTP (since that won't change while the element is cached), then on subsequent fetches from the cache if the current page is HTTPS and the resource was originally fetched over HTTP, make sure DidDisplayInsecureContent (https://cs.chromium.org/chromium/src/third_party/blink/renderer/core/frame/local_frame_client.h?rcl=35b382aa26d503c46963fdd6fa41bffe42cc7074&l=187) gets called. I haven't given this approach a lot of thought, but it might be easier.

### hu...@chromium.org (2018-10-17)

mkwst, can you take a look?
(Or can someone who is not OOO take a look sooner?)


### mm...@chromium.org (2019-04-29)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-09-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-12-11)

[Empty comment from Monorail migration]

### es...@chromium.org (2020-01-06)

I can't repro this on a local build, so I'm finding it difficult to debug and figure out what might be going on and/or where we need to call into MixedContentChecker. Could somebody on the media team perhaps be able to look into this in more detail?

### es...@chromium.org (2020-01-13)

(pinged mounir over email)

### ml...@google.com (2020-01-13)

Assigning to dalecurtis@ who has been taking this over from hubbe@

[Monorail components: Internals>Media>Network]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-01-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/dfd505cf2ad5c356a1a14a4131eb7a9a9ed933ae

commit dfd505cf2ad5c356a1a14a4131eb7a9a9ed933ae
Author: Dale Curtis <dalecurtis@chromium.org>
Date: Thu Jan 23 22:22:42 2020

Always check in with MixedContentChecker in HTMLMediaElement.

Some loads are done from an in memory cache and won't trigger the
typical mixed content warnings, so explicitly tell MixedContentChecker
about our loads to ensure the proper notifications are generated.

Fixed: 868145
Change-Id: I4df0ac3db1f2584c2ef44b5e3606acff314bc4ca
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2008396
Commit-Queue: Dale Curtis <dalecurtis@chromium.org>
Reviewed-by: Emily Stark <estark@chromium.org>
Reviewed-by: Mounir Lamouri <mlamouri@chromium.org>
Auto-Submit: Dale Curtis <dalecurtis@chromium.org>
Cr-Commit-Position: refs/heads/master@{#734631}

[modify] https://crrev.com/dfd505cf2ad5c356a1a14a4131eb7a9a9ed933ae/third_party/blink/renderer/core/html/media/html_media_element.cc


### sh...@chromium.org (2020-01-24)

[Empty comment from Monorail migration]

### da...@chromium.org (2020-01-24)

[Empty comment from Monorail migration]

### na...@google.com (2020-01-27)

[Empty comment from Monorail migration]

### na...@google.com (2020-01-30)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-01-30)

Congrats! The Panel decided to award $500 for this report! 

### na...@google.com (2020-01-30)

Also they particularly liked the video with music :) 

### na...@google.com (2020-01-30)

[Empty comment from Monorail migration]

### ad...@google.com (2020-03-09)

remkoboonstra@gmail.com - when this appears in the Chrome release notes, how would you like to be credited?

### ad...@google.com (2020-03-13)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-03-13)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-04-14)

[Empty comment from Monorail migration]

### [Deleted User] (2020-05-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2021-02-04)

Hi remkoboonstra@! Just checking in to see if you would still like to receive your reward for this submission. We are required to finalize payments of all rewards within one year. You should have received an email from a member of our payments team back in January or February of 2020. If you would still like to receive this reward, please respond to that email from the payments team or let me know if you did not receive that email and we will work to rectify the situation. 
If we do not receive a response, your reward will be donated to a charitable organization on 19 February 2021. 
Thank you! 

### am...@google.com (2021-02-22)

Reward donated to charitable cause

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/868145?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>Media>Video, Internals>Media>Network, UI>Browser>Omnibox>SecurityIndicators]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092040)*
