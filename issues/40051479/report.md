# Security:  MediaElementAudioSourceNode bypasses CORS checks

| Field | Value |
|-------|-------|
| **Issue ID** | [40051479](https://issues.chromium.org/issues/40051479) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>SecurityFeature>CORS, Blink>WebAudio |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | uz...@gmail.com |
| **Assignee** | rt...@chromium.org |
| **Created** | 2020-02-11 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**

This example shows how you can access an external audio stream despite CORS protection. Although the message "MediaElementAudioSource outputs zeroes due to CORS access restrictions for" appears in the Chrome console, you can still get the data  

and use, for example, to visualize frequencies.  

Connection order:

1. Run the audio hosted on the server.
2. Replace the link to the resource, indicating the desired external audio stream.
3. Start playback.  
   
   This method allows you to use the visualization tools Web Audio API.  
   
   If you do not use a local audio file, then you cannot receive data.

If the example does not start immediately, you need to refresh the page through Ctr + F5.  

Since the example uses an external audio stream from a radio station, it may not always be available. Then you can try a number of others:

<http://cast.radiopyatnica.com.ua/radiopyatnica>  

<http://media2.brg.ua:8000/shanson_l>  

<http://cast.radiogroup.com.ua/retro>  

<http://cast.nashe.ua/nashe>  

<http://online-radiomelodia.tavrmedia.ua/RadioMelodia>  

<http://cast.nrj.in.ua/nrj>  

<http://91.218.212.84:8000/radionv.mp3>"  

<https://cast.radiogroup.com.ua/avtoradio>  

<http://radio.urg.ua/radio-stilnoe>  

<http://icecastdc.luxnet.ua/maximum>

Need to replace the link in 32 line of the file index.html  

mediaElement.setAttribute('src', '<http://online-hitfm.tavrmedia.ua/HitFM>', event);

This example was run on Open Server x64 standard configuration.

**VERSION**  

Chrome Version: [80.0.3987.87] + [dev] + [64 bit]  

Operating System: [ Майкрософт Windows 10 Pro 10.0.15063 N/A Build 15063]

**CREDIT INFORMATION**  

Taras Uzdenov

## Attachments

- [index.html](attachments/index.html) (text/plain, 2.5 KB)
- [123.mp3](attachments/123.mp3) (application/octet-stream, 11.3 MB)
- [index.html](attachments/index_53075302.html) (text/plain, 2.5 KB)
- [test3.html](attachments/test3.html) (text/plain, 2.8 KB)

## Timeline

### rs...@chromium.org (2020-02-11)

[Empty comment from Monorail migration]

[Monorail components: Blink>SecurityFeature>CORS]

### rs...@chromium.org (2020-02-11)

Thanks for reporting this. I'm currently unable to reproduce this in M82.

I did a bisect, and it seems to have been fixed somewhere in this range:
https://chromium.googlesource.com/chromium/src/+log/d9dc01de12516b79ee12215d3a73371dc719adce..2b27f7f75c45d0e897e3b9e0e93191b94c6c4ad3

(I had to adjust the test somewhat, due to media policies for autoplay)

Now, my test may not have been entirely correct, because I was using file:// resources, but that would seem to track with https://chromium.googlesource.com/chromium/src/+/69901e65bfea41eab02a3c0e947d076920f3494f

Toyoshim: As best I can tell, the repro provided seems to be a duplicate of https://crbug.com/chromium/1026546 - does that seem correct?

### rs...@chromium.org (2020-02-11)

OK, toyoshim's fix is why I couldn't reproduce when using file://. I am able to reproduce this issue when using a local test server (e.g. Python's SimpleHTTPServer)

### rs...@chromium.org (2020-02-12)

rtoy: I bisected this further with a local instance, and it seems it regressed in this range:
https://chromium.googlesource.com/chromium/src/+log/abae9cc8599530acea672e7abcb8591b327278ac..6312daacd8c4b8a58d100d51941558201bd60827

I suspect it's https://chromium.googlesource.com/chromium/src/+/761c75d2d607638ff53c764b4925bcca9be601d8

From my analysis, the move to SetFormat() seemed reasonable given the reasons. However, if the new format has the same number of channels and sample rate, we don't end up recomputing is_origin_tainted_ based on WouldTaintOrigin(), due to the conditional at https://source.chromium.org/chromium/chromium/src/+/master:third_party/blink/renderer/modules/webaudio/media_element_audio_source_node.cc;l=109;drc=75d8a90b57cfe0eb83174826ee2ba858d2223ea3?originalUrl=https:%2F%2Fcs.chromium.org%2F

The solution isn't obvious to me, so I'm hoping you could help here. I wasn't sure if https://source.chromium.org/chromium/chromium/src/+/master:third_party/blink/renderer/modules/webaudio/media_element_audio_source_node.cc;l=204;drc=75d8a90b57cfe0eb83174826ee2ba858d2223ea3?originalUrl=https:%2F%2Fcs.chromium.org%2F should be checking WouldTaintOrigin (and the is_origin_tainted_ cached variable done away with entirely), or, if that's a performance optimization to only reflect when sources are changed, whether the modification to WouldTaintOrigin() should be moved out of the conditional for the format checks, which would also require acquiring the source locks.

I'm not sure I've got the Severity right, based on https://chromium.googlesource.com/chromium/src/+/master/docs/security/severity-guidelines.md, so 

[Monorail components: Blink>WebAudio]

### rs...@chromium.org (2020-02-12)

[Empty comment from Monorail migration]

### rs...@chromium.org (2020-02-12)

Oh, and one compounding factor: These servers do set Access-Control-Allow-Origin in the responses, so it was unclear if this is WAI. However, given no cross-origin pre-flight was started before that ACAO check, it seemed to be a bug, especially since WouldTaintOrigin is failing, but it's not causing the node to update (to output zeroes)

### rs...@chromium.org (2020-02-12)

[Empty comment from Monorail migration]

### rt...@chromium.org (2020-02-12)

Thanks for the analysis.  I'm not a CORS estimate, so adding yhirano@ for help in figuring out what to do.

### to...@chromium.org (2020-02-12)

> https://crbug.com/chromium/1050996#c6

CORS preflight was only made when the CORS-enabled request does not meet the SimpleRequest conditions, and it's usually for JavaScript initiated requests that could contain more arbitrary factors in the request. So making no CORS preflight is the expected behavior here.

I haven't checked the detailed spec for the audio tag, but if it's similar to the image tag, it should make no-cors request by default, and it allows to use the data only for playing, and should not allow raw data access.

If users want to inspect wave forms, the tag should have "crossorigin" attribute so that the tag makes CORS-enabled request to fetch the data. It will set the Origin header in the request, and server can decide if such CORS requests are permitted and ACAO should be set. With this crossorigin attribute, the data is available for playing and inspecting, but only when the server permits it by the access control headers.

https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes/crossorigin mentioned that the audio tag supports it.

Also I confirmed that the FFT works even for the cross origin response that does not have the ACAO header. So the issue is reproduced regadless of ACAO existence.


### to...@chromium.org (2020-02-12)

It seems the permitted access control is not revalidated when the src is renewed.

initial src="123.mp3", updated src="http://..." => FFT works
initial src="http://", updated src="http://..." => FFT does not work
initial src="http://", updated src="123.mp3" => FFT works

initial src was not played actually due to the lack of user interactions, but access control seems to be stored.

### rs...@chromium.org (2020-02-12)

toyoshim: Yeah, for testing in M80+, I restructured the test a little (attached) to have explicit user input (attached), and run via "python -m SimpleHTTPServer"

The relevant factor here is, I believe, that the initial resource's SetFormat() matches the targeted resources format, and thus bypasses updating the tainted state.

My understanding of the expectations are:
- If the tag has <crossorigin>, and the .src would be cross-origin, perform a CORS pre-flight; if A-C-A-O is present, allow access, if it is not, block and output zeroes
- If the tag does not have <crossorigin>, and the .src would be cross-origin,  block and output zeroes

I think these missed WPT because it looks like the WPT check based on the console log expected results, rather than making sure that the data itself is not passed. However, I may be misreading them.

Prior to the CL mentioned in https://crbug.com/chromium/1050996#c4, the load was blocked using the attached test case.

### uz...@gmail.com (2020-02-12)

I analyzed the presence of the problem in different browsers and found that the behavior is different.
In Internet Explorer, the example does not work, but I think that this is due to the fact that Edge is skipping data and the audio stream is playing. Without displaying any messages to the console.
Opera's behavior is similar to Chrome.

In Mozilla, the audio stream is blocked and the message is output to the console: "HTMLMediaElement passed to createMediaElementSource, there is a resource from an extraneous source, the node will output silence."

I hope this information helps solve the problem.


### rs...@chromium.org (2020-02-12)

Right, the relevant part of the spec is:
https://webaudio.github.io/web-audio-api/#MediaElementAudioSourceOptions-security
To prevent this, a MediaElementAudioSourceNode MUST output silence instead of the normal output of the HTMLMediaElement if it has been created using an HTMLMediaElement for which the execution of the fetch algorithm [FETCH] labeled the resource as CORS-cross-origin.

The resource should be treated as CORS-cross-origin because of:
https://html.spec.whatwg.org/multipage/media.html#concept-media-load-resource

Namely, |mode| is remote, and so it should be a "potential-CORS request", and the default |corsAttributeState| is No CORS. Because of that, it should be an opaque filtered response, as per https://fetch.spec.whatwg.org/#concept-request-mode ( Restricts requests to using CORS-safelisted methods and CORS-safelisted request-headers. Upon success, fetch will return an opaque filtered response. ). This should cause it to be treated as CORS cross-origin because of https://html.spec.whatwg.org/#cors-cross-origin because the type will be "opaque" on return.

### yh...@chromium.org (2020-02-13)

The "CORS-same-origin" and "CORS-cross-origin" concept is implemented as blink::ResourceResponse::IsCorsSameOrigin and blink::ResourceResponse::IsCorsCrossOrigin respectively.

Due to the split between blink and media/blink, the media code calculates the value from response type: see [1]. This is not a problem.

Ryan's assessment sounds reasonable. Raymond, does it make sense to remove |is_origin_tainted_|, and call WouldTaintOrigin() instead?

1: https://source.chromium.org/chromium/chromium/src/+/master:media/blink/resource_multibuffer_data_provider.cc;drc=a7af154233103371fc11baf4e0ede4d1dba5f939;bpv=1;bpt=1;l=321?originalUrl=https:%2F%2Fcs.chromium.org%2F

### rt...@chromium.org (2020-02-13)

I don't remember why we have is_origin_tainted_.  Maybe because we didn't want to call WouldTaintOrigin() every 3 ms or so?  If that's the case and WouldTaintOrigin() isn't too expensive, then that would probably be best.

### sl...@google.com (2020-02-13)

The alternative solution was to grab the lock during SetFormat(); from looking at the call traces, it seems like it is called whenever a resource load switches sources. I was trying to work on a web_test for this, since we have web_tests that test for initial .src assignment, but in this case, it's a switch from an allowed .src to a disallowed .src

### rt...@chromium.org (2020-02-13)

I think the problem is basically as c#4 says.  If everything matches, we don't set is_origin_tainted.  Updating the code so that it is set in all cases fixes this.  I don't hear or see anything from the second source.

### uz...@gmail.com (2020-02-14)

Is such a solution possible?
1. Track src attribute change.
2. If a change has occurred, then stop the flow.
3. Updating src.
4. Then we start again.

If I understand correctly, then CORS will not skip the new thread.

### rt...@chromium.org (2020-02-14)

Do you mean something like this modified test case?  My prototype plays the first source, blocks the second, and plays the third (because it's the same source as the first.)


### rt...@chromium.org (2020-02-14)

[Empty comment from Monorail migration]

### ho...@chromium.org (2020-02-14)

Seems like P1?

### rs...@chromium.org (2020-02-14)

Yeah, I was told sheriffbot@ was going to set these, but it's a lie :)

### [Deleted User] (2020-02-14)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-02-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/ace7aab359d2fa00ef71e168418ae76df853445b

commit ace7aab359d2fa00ef71e168418ae76df853445b
Author: Raymond Toy <rtoy@chromium.org>
Date: Tue Feb 18 17:42:54 2020

MediaElementAudioSourceNode always sets is_origin_tainted

When a source changes for a MediaElementAudioSourceNode, the number of
channels and sample rate can be the same as the previous source.
However, we were skipping updating |is_origin_tainted_| in this case,
which allowed audio through even though we printed a message that CORS
prevented this.

Now always update |is_origin_tainted_| right away.

Bug: 1050996
Change-Id: I82b596993c7b88dbb899e5aeb00294db57a08613
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2055989
Reviewed-by: Hongchan Choi <hongchan@chromium.org>
Reviewed-by: Yutaka Hirano <yhirano@chromium.org>
Commit-Queue: Raymond Toy <rtoy@chromium.org>
Cr-Commit-Position: refs/heads/master@{#742191}

[modify] https://crrev.com/ace7aab359d2fa00ef71e168418ae76df853445b/third_party/blink/renderer/modules/webaudio/media_element_audio_source_node.cc


### rt...@chromium.org (2020-02-19)

Manually tested the fix against all of the test cases above.  The cross-origin source is blocked as expected.

### rt...@chromium.org (2020-02-19)

Does this need to be merged to M81?

### [Deleted User] (2020-02-19)

This bug requires manual review: M81's targeted beta branch promotion date has already passed, so this requires manual review
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), bindusuvarna@(iOS), geohsu@(ChromeOS), pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-02-19)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-02-20)

[Empty comment from Monorail migration]

### ad...@google.com (2020-02-20)

I think I agree that this is High severity, though like rsleevi@ I'm not 100% sure.

But if it is High, we would normally merge to stable as well as beta. Approving merge to beta M81 (branch: 4044) now, and adding a merge request for stable which we can consider in a few days (unfortunately we just missed a beta cycle). (Sheriffbot would normally have added an M80 merge request, but it decided that the human in https://crbug.com/chromium/1050996#c26 was probably smarter than it.)

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-02-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/7b23472ce68c53961b39f6cf812dfe2fc7a041a5

commit 7b23472ce68c53961b39f6cf812dfe2fc7a041a5
Author: Raymond Toy <rtoy@chromium.org>
Date: Thu Feb 20 22:10:16 2020

MediaElementAudioSourceNode always sets is_origin_tainted

When a source changes for a MediaElementAudioSourceNode, the number of
channels and sample rate can be the same as the previous source.
However, we were skipping updating |is_origin_tainted_| in this case,
which allowed audio through even though we printed a message that CORS
prevented this.

Now always update |is_origin_tainted_| right away.

(cherry picked from commit ace7aab359d2fa00ef71e168418ae76df853445b)

Bug: 1050996
Change-Id: I82b596993c7b88dbb899e5aeb00294db57a08613
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2055989
Reviewed-by: Hongchan Choi <hongchan@chromium.org>
Reviewed-by: Yutaka Hirano <yhirano@chromium.org>
Commit-Queue: Raymond Toy <rtoy@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#742191}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2067284
Reviewed-by: Raymond Toy <rtoy@chromium.org>
Cr-Commit-Position: refs/branch-heads/4044@{#388}
Cr-Branched-From: a6d9daf149a473ceea37f629c41d4527bf2055bd-refs/heads/master@{#737173}

[modify] https://crrev.com/7b23472ce68c53961b39f6cf812dfe2fc7a041a5/third_party/blink/renderer/modules/webaudio/media_element_audio_source_node.cc


### rt...@chromium.org (2020-02-24)

Should I merge this to M80?

### na...@google.com (2020-02-24)

[Empty comment from Monorail migration]

### rs...@chromium.org (2020-02-26)

Ade: I think https://crbug.com/chromium/1050996#c32 is directed to you?

### ad...@chromium.org (2020-02-26)

Yes - approved for merge to M80 (branch 3987) assuming things still look good on canary.

### rt...@chromium.org (2020-02-26)

Thanks.  I'll merge now.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-02-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/947073840323470f894c9957e974b28f1c6f730e

commit 947073840323470f894c9957e974b28f1c6f730e
Author: Raymond Toy <rtoy@chromium.org>
Date: Wed Feb 26 23:21:01 2020

MediaElementAudioSourceNode always sets is_origin_tainted

When a source changes for a MediaElementAudioSourceNode, the number of
channels and sample rate can be the same as the previous source.
However, we were skipping updating |is_origin_tainted_| in this case,
which allowed audio through even though we printed a message that CORS
prevented this.

Now always update |is_origin_tainted_| right away.

(cherry picked from commit ace7aab359d2fa00ef71e168418ae76df853445b)

Bug: 1050996
Change-Id: I82b596993c7b88dbb899e5aeb00294db57a08613
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2055989
Reviewed-by: Hongchan Choi <hongchan@chromium.org>
Reviewed-by: Yutaka Hirano <yhirano@chromium.org>
Commit-Queue: Raymond Toy <rtoy@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#742191}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2075339
Reviewed-by: Raymond Toy <rtoy@chromium.org>
Cr-Commit-Position: refs/branch-heads/3987@{#959}
Cr-Branched-From: c4e8da9871cc266be74481e212f3a5252972509d-refs/heads/master@{#722274}

[modify] https://crrev.com/947073840323470f894c9957e974b28f1c6f730e/third_party/blink/renderer/modules/webaudio/media_element_audio_source_node.cc


### na...@google.com (2020-02-27)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-02-27)

Congrats the Panel decided to award $1,000 for this report!

### uz...@gmail.com (2020-02-27)

Hi, thanks for the reward.

Can I find out how this report was rated according to https://www.google.com/about/appsecurity/chrome-rewards/#rewards

To which category of security errors has been assigned?
As far as I understand, Security_Severity-High.

How is the quality level estimated? High or basic? 

If basic, then what should have been done better?

This information will help me in the future.
Thanks.

### ad...@google.com (2020-02-29)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-02-29)

[Empty comment from Monorail migration]

### na...@google.com (2020-03-03)

[Empty comment from Monorail migration]

### ad...@google.com (2020-03-04)

[Empty comment from Monorail migration]

### na...@google.com (2020-03-05)

The Panel determined your report to be a baseline Web Platform Privilege Escalation which is how they came to the reward value of $1,000. 

### ad...@chromium.org (2020-03-19)

[Empty comment from Monorail migration]

### [Deleted User] (2020-05-27)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1050996?no_tracker_redirect=1

[Multiple monorail components: Blink>SecurityFeature>CORS, Blink>WebAudio]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40051479)*
