# Security: Microphone access not blocked if you lock your phone.

| Field | Value |
|-------|-------|
| **Issue ID** | [40080089](https://issues.chromium.org/issues/40080089) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>Media>Audio, Privacy |
| **Platforms** | Android |
| **Reporter** | ba...@chromium.org |
| **Assignee** | qi...@chromium.org |
| **Created** | 2014-07-22 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**

Visit this site on your phone:  

<https://www.standardabweichung.de/design/projekte/html5/chrome-android-mic-security-check>

Translation of the steps to reproduce:

1. Press Start button and give access to microphone.
2. Lock you phone.
3. Dictate text into phone.
4. Unlock the phone and observe that text has been recorded while phone was locked.

Translation of background:  

While experimenting with the HTML5 webkitSpeechRecognition we noticed on July 18, 2014 a strange phenomenon in the context of Android and the Chrome browser. If the user gives a website permission to the microphone, this permission remains active if the phone/table is in standby [sic; probably meant: locked]. The microphone is switched off after approximately 60 seconds or after 10 seconds with no input. If the website is delivered via HTTPS, it is possible to prevent switching off the microphone by restarting the process (see code example -> speechRestart)

They have tested with with Chrome 35.0.1916.141 on various phones. I have verified this with Chrome Dev 37.0.2062.22 on my Nexus 5.

## Timeline

### ba...@chromium.org (2014-07-22)

[Empty comment from Monorail migration]

### ba...@chromium.org (2014-07-22)

Adding Andrew and Henrik to help routing this bug to good owners. Everybody in SE seems to be on vacation.

Magnus also pointed me to xians@.

### [Deleted User] (2014-07-22)


Niklas or Tommi, is there any one we can get help on this Android speech bug?

### ba...@chromium.org (2014-07-22)

Niklas and Tommi are on vacation. Niklas will be back tomorrow.

### aj...@chromium.org (2014-07-22)

Shijing, I'm willing to be you're busy with other bugs, but TBH I think you're the best not-currently-on-vacation person to look at this. (Henrik A would otherwise be the natural owner).

### ba...@chromium.org (2014-07-22)

[Empty comment from Monorail migration]

### ke...@google.com (2014-07-22)

[Empty comment from Monorail migration]

### kl...@chromium.org (2014-07-22)

[Empty comment from Monorail migration]

### ka...@chromium.org (2014-07-22)

[Empty comment from Monorail migration]

### kl...@chromium.org (2014-07-22)

[Empty comment from Monorail migration]

### qi...@chromium.org (2014-07-22)

[Empty comment from Monorail migration]

### wj...@google.com (2014-07-22)

The original design of keeping audio on even when phone is locked is to mimic phone app behavior, since webrtc is supposedly to be kind of "phone" app.

If different behavior is desired for different apps, you might want to set different power mode for different app, IIRC.


### kl...@chromium.org (2014-07-22)

[Empty comment from Monorail migration]

### vr...@chromium.org (2014-07-22)

[Empty comment from Monorail migration]

### ju...@chromium.org (2014-07-22)

The existing text-to-speech stuff on the Android keyboard stops when the phone is locked. I think we should do the same thing here for webspeech.

Regarding how webrtc calls should be handled, agree we should mimic the phone app behavior.

### qi...@chromium.org (2014-07-22)

Looking at the javascript in #1, the site calls restart() when OnEnd or OnError is called, so unless we revoke the microphone permission, or totally disables the microphone after screen lock, it can always find a way to record speech after screen lock

### qi...@chromium.org (2014-07-22)

another thing we could do is associate onStart() with a user gesture, in that case, it will automatically lose the speech recognition after the device goes to sleep.

### ju...@chromium.org (2014-07-22)

Or we could just lock out calls to start() when the device is locked.

### kl...@chromium.org (2014-07-23)

We need to make sure the site is usable after user unlock the device. So disallow start(), throw DOM exception, when it is called when the tab is invisible.

### jw...@chromium.org (2014-07-23)

[Empty comment from Monorail migration]

### ju...@chromium.org (2014-07-23)

Which DOM exception will be thrown in this case?

We may need to do the same for getUserMedia.

### qi...@chromium.org (2014-07-23)

In my CL, i just throw InvalidStateError.  I don't want to call onError() as it might affect javascript event listeners

### [Deleted User] (2014-07-23)

Thanks Wei for the clarification.
There was a security review process before we launched WebRTC in Clank, https://code.google.com/p/chromium/issues/detail?id=223999, which clearly states that:
If the WebRTC tab with an ongoing video call is placed in the background, or if the chrome browser is minimized, or if the screen is locked (all during an ongoing video call), we will stop the video from being transmitted to the other side. But the video in-use notification will always be displayed in the Android system tray. Voice will still flow. Video will automatically resume once the WebRTC video tab is brought to the foreground.

I think this clearly supports Wei and Justin's comment "mimic phone app behavior", and hope everyone agrees that the current issue only limits to webspeech.

to #16, I think this is a general challenge to all clients using capture devices. For example, if a website gets permission from the users, the website can wake up its service any time to open the camera or microphone even though the screen is locked or the tag is on the background.
It is unclear how clank handles it today, I will create a new issue for investigation.



### [Deleted User] (2014-07-23)

+jorgelo, kaichou for privacy.

Some more information related to permission and security:

A https becomes an authorized website to capture devices once users grand the permission. This scheme has been deployed on desktop Chrome for a long time, and we haven't got privacy complaints from it yet. Phone is definitely more sensitive on this, we decided to provide sticky permission to Clank in https://code.google.com/p/chromium/issues/detail?id=307027
If we are worrying that a https website can misuse the permission, we will have to step back and re-balance the tradeoffs again.

For a http, the permission will be revoked for new request.

+Burnik, he will help me figure out the current behaviour if a background tab can use the capture devices or not.

I see different approaches to fix the current issues depending on the permission model we will choose:
# keep https with sticky permission:
When the tag with a ongoing speech call gets into background or the screen is locked, we stop the recognition.
When a background tab tries opening a capture device (camera or microphone), we fail it. (this can be done on the permission layer)

# no sticky permission for https:
Then we simply need to stop the recognition when the tag with a ongoing speech call gets into background or the screen is locked.

### ke...@google.com (2014-07-23)

Branch 1985_128 is open for blink, clank, and chromium if needed. Please merge the final fix when decided there, then request a merge for 37 as well.

### cl...@chromium.org (2014-07-23)

[Empty comment from Monorail migration]

### bu...@chromium.org (2014-07-23)

Hi all,

Regarding WebRTC and getUserMedia.

I've made a test which repeatedly (setInterval - every 5 seconds) calls getUserMedia on a page served via HTTPS, takes image snapshots and then sends a chunk of that image to the host server and logs it. I tail -f the log file on the server to observe.

https://github.com/kristijanburnik/webrtc-tests/blob/master/getusermedia_interval/test.js
(public repo, but note - the test does not expose any reference to this bug)

== Phone ==
Model: HTC Desire 500
HTC sense version 5.0
OS:  Android 4.1.2
Kernel: 3.4.0-g94272d2

== Browser ==
Chrome v. 35.0.1916.141

Setup actions:
- visit the page thru HTTPS
- approve getUserMedia request (only the first call)

The result is: 
- when I lock the screen the log shows black pixels (all zeroes in bitmap data)
- when I unlock the screen the log shows image data (pixel data of my face and bg)

Same goes when I switch to another app (i.e. when chrome tab loses focus and afterwards regains it)

I might create a test with audio too, but my guess is that all streams are muted when the tab is inactive.


### ba...@chromium.org (2014-07-23)

Hi.

I am trying to understand this:

Is there a distinction between locking the screen by pressing the button on the side of the phone and locking the screen by putting the phone to your ear?

My feeling is that in the first case, we should stop providing audio and video data to the website (regardless whether this is via WebRTC or webkitSpeechRecognition). I'd be fine if the website believes that it receives data if this data is this data is indistinguishable from a muted microphone. I.e. I don't see a need for returning an error to the website.

For the latter case, I think it is reasonable if the website still received audio data (or recognized speech).

By interpreting the screen lock as "mute the microphone (and camera)", I don't think that we need to change the permission model for HTTPS.

Please let me know if I misunderstand anything completely.

### [Deleted User] (2014-07-23)

Thanks burnik for great help.

battre, it seems that you have different opinions on #23.
Currently the muting behaviour is only for video. For webrtc audio, we support the "phone app" behaviour, since it is pretty common use case where users lock the screen (by pressing the button on the side of the phone) and continue the audio call.
For apps like speech recognition might have different behaviours, like recognition should be stopped.
Please clarify if you have any concern here.

My personal opinion is that, if we want to keep sticky permission for https, we need to narrow the speech recognition use cases to:
Only a front tab can do recognition. background tab or a locked screen should fail the recognition.

But for webrtc audio, we might want to keep the phone app behaviour.


### tn...@chromium.org (2014-07-23)

[Empty comment from Monorail migration]

### [Deleted User] (2014-07-23)

The main issue in my opinion is that we prompt the user about the microphone usage but we fail to tell them in the infobar and in the corresponding help center web page that the microphone will still be on after the phone is locked.

Maybe a possible fix would be to change the helpcenter article? 

### ba...@chromium.org (2014-07-23)

Oh wow, this is complicated... If we fix the speech recognition (in the sense that recognition is stopped if the screen is locked), it is still possible to observe somebody using webrtc.

I have a VC with Shijing at 8:30am PST to discuss this (ping me if you want to join). I'll try to make a structured analysis of the current situation and options in https://docs.google.com/a/google.com/document/d/1mbN-BjMBMPijlT5RUXIPSPkU_7J-v90dcSlIiX9hrbM/edit

### be...@chromium.org (2014-07-23)

> it is still possible to observe somebody using webrtc.

Yes, but a domain cannot use WebRTC unless the user takes action to grant that domain microphone access permission, similar to the process for a standard Play Store app getting microphone access permission upon installation.

### ba...@chromium.org (2014-07-23)

@27: Having this test for audio would be extremely useful because my understanding is that video is already handled separately if you move a tab to the background. So the question I am interested in is:

1. Website has Audio/Video permission.
2. Website continuously records audio for 5 seconds, then stops.
3. Phone is locked.
4. While phone is locked, the website tries to record another 5 seconds of audio. Is this possible?

An alternative of this experiment would move the website into the background between steps 2 and 3.

### qi...@chromium.org (2014-07-23)

In addition to phone lock, background tabs can also record audio currently.

### be...@chromium.org (2014-07-23)

Currently, a domain to which the user has granted microphone access permission is treated just like an App to which the user has granted microphone access permission.  Both can record while in the background, while locked, etc.  It seems reasonable to me that they should behave similarly, because the user has granted them the same permission.

### kl...@chromium.org (2014-07-23)

Privacy team recommended this as P0, immediately respin for the current stable.

Even we know the underline logic applied to both speechRecognition and WebRTC audio, we would like to address speechRecognition as P0. In another word, we would like to get a solution ASAP. We can continue to debate the long term solution.

For speechRecognition, we propose,

1. website gets audio permission (https persist, http ask every time. This is unchanged)
2. website get audio
3. phone locked
4. website stop getting audio. If website try to call start again, it will get DOM exception.
5. phone unlock
6. website call start to get audio, it works again.

Min has two CLs in review. We would like to get it resolved today.

https://chromiumcodereview.appspot.com/415433002/
https://chromiumcodereview.appspot.com/409183005/

### ba...@chromium.org (2014-07-23)

Here is our current proposal, which I think should solve the problem and should be easy to implement in a single CL according to xians@:

- Don’t allow accepting new calls while a tab is in the background or the phone is locked.
- Continue connection that was started before if the user locks the screen.
- Stop speech recognition when the website is not displayed.
- HTTPS permission stays sticky (we have UI that shows that the website is recording).
- HTTP permission is not sticky.
- Update Help center article to explain all of this.


### qi...@chromium.org (2014-07-23)

in #38, what does it mean by 
"Continue connection that was started before if the user locks the screen." and
"Stop speech recognition when the website is not displayed."

I feel these 2 conflicting.
BTW, would you please take a look at the CLs in 37? i added you as a reviewer/.

### kl...@chromium.org (2014-07-23)

Re #38, it seems you are suggestion

. for both webrtc and speech recognition, we disallow start while tab is not visible, either in the background or phone is locked.

. only stop speech recognition when tab turns invisible. Don't change webrtc audio when tab turns invisible.

### ba...@chromium.org (2014-07-23)

The reason for proposing to treat speech recognition and WebRTC differently was to make speech recognition as similar as possible to the Android keyword's speech recognition: It stops recording if you lock your phone or if you press the home button. 

### qi...@chromium.org (2014-07-23)

My patch in #37 should stop speech recognition after tab visibility changes, and it shouldn't impact webRTC

### [Deleted User] (2014-07-23)

klobag is right,  that is what the proposed behaviour is.

battre and I had a short discussion, the problems we see on clank include:
# when screen is locked, or a tab gets in the background, the https website with device permission can open the microphone using speech recognition or webrtc, and upload the recognized text or mic data, users won't know about the activities.
# during an ongoing speech recognition, if the screen is locked, recognition is still on going.

For WebRTC perspectives, we would like:
phone app behaviour, that says the audio should continue to flow for an ongoing call if the screen is locked.
But we probably don't want the websites to open the microphone or camera when the screen is locked or tab gets into background, probably extension is exception here. (Justin or Ben, please correct me if you have different opinions here).

So the proposals are trying to address all the problems here.

qinmin, I think your CL can stop the recognition when the tab gets hidden, but it won't fix all the problems we mentioned above. And I believe it is not complicated to write a solution which fixes all the problems. The ideas in my mind:
when a tab gets hidden, it aborts all the existing recognition session.
and in media_stream_devices_controller.cc, before it grands permission to the request, it checks if the tab is visible, if it is not, it deny the request.


I also understand this is an urgent issue, if people agree that we accept fixing only the most urgent issue, I am fine with a temporary fix which solves the speech problem.

### be...@chromium.org (2014-07-23)

> But we probably don't want the websites to open the microphone or camera when the screen is locked or tab gets into background, probably extension is exception here. (Justin or Ben, please correct me if you have different opinions here).

I disagree with this assessment.  According to the W3C specification, "Once permission has been granted, the UA should make ... readily apparent to the user ... that the page has access to the devices for which permission is given" [1].  Chrome for Android should be changed to comply with this recommendation, so that users know as soon as they open a page that it might start recording in the future, without asking.

[1] http://dev.w3.org/2011/webrtc/editor/getusermedia.html#privacy-and-security-considerations

### kl...@chromium.org (2014-07-23)

[Empty comment from Monorail migration]

### ke...@google.com (2014-07-23)

[Empty comment from Monorail migration]

### [Deleted User] (2014-07-23)

FYI, I just chatted with Min on his CL, I think we are making some progress there.

Ben, so you are suggesting that we should allow websites with permission to open the microphone and camera even though the tab is invisible (screen is locked or tab is running in the background), and somehow trigger UIs to alert the users? 
I apologize if I am making things more complicated.



### be...@chromium.org (2014-07-23)

> Ben, so you are suggesting that we should allow websites with permission to open the microphone and camera even though the tab is invisible (screen is locked or tab is running in the background),

Yes.

> and somehow trigger UIs to alert the users? 

No.  I am suggesting that a tab with sticky microphone access permission should always be visibly marked with that information, even if that tab is not currently accessing the microphone.  It's then up to the user whether to leave the tab open (and allow it to start capturing at any future time) or close it.  I believe this is the current W3C-recommended behavior.

### kl...@chromium.org (2014-07-23)

[Empty comment from Monorail migration]

### ju...@chromium.org (2014-07-23)

FWIW, native Android apps don't need to provide a notification that they might start recording in the background. I'm not sure that we should treat web apps differently - and I don't think users would understand any difference.

#43 seems like reasonable behavior to me, although I'd be curious whether native apps have the same limitation on starting recording while the screen is locked.

### [Deleted User] (2014-07-23)

Ah, I see. Though I am not sure if it is a desired solution in general. For example, google.com have access to microphone, it might not be nice to mark google.com with information that it can access the microphone at any time, given that fact that google.com will only access the microphone when users explicitly click on the mic icon.

### da...@chromium.org (2014-07-23)

Discussed with xians@, qinmin@. To be explicit here are the changes which will be made:
- Ongoing speech recognition will be shutdown upon lock or backgrounding.
- Ongoing getUserMedia() sessions will be left recording.

In all cases no speech recognition or new getUserMedia() sessions may be created once locked or backgrounded. A DOM exception will be thrown when such an attempt is made. I'll review the changes once they're ready.

### da...@chromium.org (2014-07-23)

Also, for the record, as a non-regression issue for a feature protected under permissions, I don't think this bug warrants its current priority or a M36 merge. xians@, qinmin@ and I are all in agreement on this.

That said, we defer to the privacy team's judgement lacking any higher power interceding.

### kl...@chromium.org (2014-07-23)

Here is privacy team's response earlier. We will proceed with M36 merge.

===
We have discussed this and think that this is a privacy issue rather than a security risk (therefore it was flagged as low security risk). As the information is already out in the press, we would recommend a respin to signal that we care for users' privacy.


### qi...@chromium.org (2014-07-23)

https://codereview.chromium.org/415433002 should be ready for review, this is the approach i discussed with xians@.

And I tested on my device, it should stop the media capture request when device is locked or tab goes background.

### bu...@chromium.org (2014-07-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/b8249aa9a42e626251c345df029a194c1529b27f

commit b8249aa9a42e626251c345df029a194c1529b27f
Author: qinmin@chromium.org <qinmin@chromium.org@0039d316-1c4b-4281-b951-d872f2087c98>
Date: Wed Jul 23 23:06:16 2014

Turn webspeech off when tab goes background

This change adds a toggle to turn webspeech off when tab goes background.
And further request to turn media capture devices on will be denied.
So Both WebRTC and webSpeech won't be able to initiate new requests when tab is in background.

BUG=396054
R=dalecurtis@chromium.org, jam@chromium.org

Review URL: https://codereview.chromium.org/415433002

git-svn-id: svn://svn.chromium.org/chrome/trunk/src@285072 0039d316-1c4b-4281-b951-d872f2087c98



### bu...@chromium.org (2014-07-23)

------------------------------------------------------------------
r285072 | qinmin@chromium.org | 2014-07-23T23:06:16.423190Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/content/renderer/render_view_impl.cc?r1=285072&r2=285071&pathrev=285072
   M http://src.chromium.org/viewvc/chrome/trunk/src/content/renderer/speech_recognition_dispatcher.cc?r1=285072&r2=285071&pathrev=285072
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/media/media_stream_devices_controller.cc?r1=285072&r2=285071&pathrev=285072
   M http://src.chromium.org/viewvc/chrome/trunk/src/content/renderer/speech_recognition_dispatcher.h?r1=285072&r2=285071&pathrev=285072
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/media/media_stream_devices_controller.h?r1=285072&r2=285071&pathrev=285072

Turn webspeech off when tab goes background

This change adds a toggle to turn webspeech off when tab goes background.
And further request to turn media capture devices on will be denied.
So Both WebRTC and webSpeech won't be able to initiate new requests when tab is in background.

BUG=396054
R=dalecurtis@chromium.org, jam@chromium.org

Review URL: https://codereview.chromium.org/415433002
-----------------------------------------------------------------

### jo...@chromium.org (2014-07-23)

[Empty comment from Monorail migration]

### ba...@chromium.org (2014-07-24)

addendum to #38:
- better permission string
- show an icon in the status bar when a website is recording (at least when it is recording and not in the foreground)

### bu...@chromium.org (2014-07-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/eb7c76762cfe5bd310de84468924dcd97a8ec2d5

commit eb7c76762cfe5bd310de84468924dcd97a8ec2d5
Author: johnme@chromium.org <johnme@chromium.org@0039d316-1c4b-4281-b951-d872f2087c98>
Date: Thu Jul 24 12:29:17 2014

Revert of Turn webspeech on/off when tab goes fore/background (https://codereview.chromium.org/415433002/)

Reason for revert:
Tentatively reverting because [1] has been consistently crashing in 2 layout tests ever since this landed[2], and this is the more likely looking of the two CLs on the blamelist:

http://build.chromium.org/f/chromium/perf/dashboard/ui/changelog.html?url=%2Ftrunk%2Fsrc&range=285071%3A285072&mode=html

http://build.chromium.org/f/chromium/perf/dashboard/ui/changelog_blink.html?url=%2Ftrunk&range=178788%3A178788&mode=html

[1]: http://build.chromium.org/p/chromium.webkit/builders/WebKit%20Android%20%28Nexus4%29

[2]: http://build.chromium.org/p/chromium.webkit/builders/WebKit%20Android%20%28Nexus4%29/builds/16889

Original issue's description:
> Turn webspeech off when tab goes background
> 
> This change adds a toggle to turn webspeech off when tab goes background.
> And further request to turn media capture devices on will be denied.
> So Both WebRTC and webSpeech won't be able to initiate new requests when tab is in background.
> 
> BUG=396054
> R=dalecurtis@chromium.org, jam@chromium.org
> 
> Committed: https://src.chromium.org/viewvc/chrome?view=rev&revision=285072

TBR=jam@chromium.org,juberti@chromium.org,xians@chromium.org,dalecurtis@google.com,dalecurtis@chromium.org,qinmin@chromium.org
NOTREECHECKS=true
NOTRY=true
BUG=396054

Review URL: https://codereview.chromium.org/416053002

git-svn-id: svn://svn.chromium.org/chrome/trunk/src@285208 0039d316-1c4b-4281-b951-d872f2087c98



### bu...@chromium.org (2014-07-24)

------------------------------------------------------------------
r285208 | johnme@chromium.org | 2014-07-24T12:29:17.653681Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/content/renderer/speech_recognition_dispatcher.cc?r1=285208&r2=285207&pathrev=285208
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/media/media_stream_devices_controller.cc?r1=285208&r2=285207&pathrev=285208
   M http://src.chromium.org/viewvc/chrome/trunk/src/content/renderer/speech_recognition_dispatcher.h?r1=285208&r2=285207&pathrev=285208
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/media/media_stream_devices_controller.h?r1=285208&r2=285207&pathrev=285208
   M http://src.chromium.org/viewvc/chrome/trunk/src/content/renderer/render_view_impl.cc?r1=285208&r2=285207&pathrev=285208

Revert of Turn webspeech on/off when tab goes fore/background (https://codereview.chromium.org/415433002/)

Reason for revert:
Tentatively reverting because [1] has been consistently crashing in 2 layout tests ever since this landed[2], and this is the more likely looking of the two CLs on the blamelist:

http://build.chromium.org/f/chromium/perf/dashboard/ui/changelog.html?url=%2Ftrunk%2Fsrc&range=285071%3A285072&mode=html

http://build.chromium.org/f/chromium/perf/dashboard/ui/changelog_blink.html?url=%2Ftrunk&range=178788%3A178788&mode=html

[1]: http://build.chromium.org/p/chromium.webkit/builders/WebKit%20Android%20%28Nexus4%29

[2]: http://build.chromium.org/p/chromium.webkit/builders/WebKit%20Android%20%28Nexus4%29/builds/16889

Original issue's description:
> Turn webspeech off when tab goes background
> 
> This change adds a toggle to turn webspeech off when tab goes background.
> And further request to turn media capture devices on will be denied.
> So Both WebRTC and webSpeech won't be able to initiate new requests when tab is in background.
> 
> BUG=396054
> R=dalecurtis@chromium.org, jam@chromium.org
> 
> Committed: https://src.chromium.org/viewvc/chrome?view=rev&revision=285072

TBR=jam@chromium.org,juberti@chromium.org,xians@chromium.org,dalecurtis@google.com,dalecurtis@chromium.org,qinmin@chromium.org
NOTREECHECKS=true
NOTRY=true
BUG=396054

Review URL: https://codereview.chromium.org/416053002
-----------------------------------------------------------------

### ba...@chromium.org (2014-07-24)

Failing tests of webkit_tests: 2 failed: inspector-protocol/input/dispatchMouseEvent.html fast/history/window-open.html

Stack trace:
signal 11 (SIGSEGV) at 0x00001589 (code=-6), thread 5526 (CrRendererMain)
pid: 5513, tid: 5526, name: CrRendererMain  >>> org.chromium.content_shell_apk:sandboxed_process19 <<<
signal 11 (SIGSEGV), code 1 (SEGV_MAPERR), fault addr 00000020
     r0 00000000  r1 00000001  r2 77858abc  r3 77858abc
     r4 778cf9a8  r5 778cf9a8  r6 750c2fc8  r7 40100384
     r8 750c2fd0  r9 750c32c0  sl 74dd8fbc  fp 75406289
     ip 76c7cd00  sp 750c2eb8  lr 764124a7  pc 764273ba

Stack Trace:
  RELADDR   FUNCTION                                                                                                                                                                                                                                                                                                                                                       FILE:LINE
  011ec3ba  content::SpeechRecognitionDispatcher::AbortAllRecognitions()+2                                                                                                                                                                                                                                                                                                 libgcc2.c:0
  011d74a3  content::RenderViewImpl::OnWasHidden()+26                                                                                                                                                                                                                                                                                                                      libgcc2.c:0
  01113545  _ZN3IPC7Message8DispatchIN7content20RenderWidgetHostImplES3_vEEbPKS0_PT_PT0_PT1_MS6_FvvE.isra.32+30                                                                                                                                                                                                                                                            libgcc2.c:0
  011e3b17  content::RenderWidget::OnMessageReceived(IPC::Message const&)+2154                                                                                                                                                                                                                                                                                             libgcc2.c:0
  011ddfd5  content::RenderViewImpl::OnMessageReceived(IPC::Message const&)+5436                                                                                                                                                                                                                                                                                           libgcc2.c:0
  0025ed13  content::MessageRouter::RouteMessage(IPC::Message const&)+22                                                                                                                                                                                                                                                                                                   libgcc2.c:0
  0025ecf9  content::MessageRouter::OnMessageReceived(IPC::Message const&)+20                                                                                                                                                                                                                                                                                              libgcc2.c:0
  0116c297  content::ChildThread::OnMessageReceived(IPC::Message const&)+438                                                                                                                                                                                                                                                                                               libgcc2.c:0
  002a0e35  IPC::ChannelProxy::Context::OnDispatchMessage(IPC::Message const&)+232                                                                                                                                                                                                                                                                                         libgcc2.c:0
  002a0c71  base::internal::Invoker<2, base::internal::BindState<base::internal::RunnableAdapter<void (IPC::ChannelProxy::Context::*)(IPC::Message const&)>, void (IPC::ChannelProxy::Context*, IPC::Message const&), void (IPC::ChannelProxy::Context*, IPC::Message)>, void (IPC::ChannelProxy::Context*, IPC::Message const&)>::Run(base::internal::BindStateBase*)+46  libgcc2.c:0
  0028539f  base::MessageLoop::RunTask(base::PendingTask const&)+502                                                                                                                                                                                                                                                                                                       libgcc2.c:0
  00285449  base::MessageLoop::DeferOrRunPendingTask(base::PendingTask const&)+28                                                                                                                                                                                                                                                                                          libgcc2.c:0
  00285f5d  base::MessageLoop::DoWork()+94                                                                                                                                                                                                                                                                                                                                 libgcc2.c:0
  00286149  base::MessagePumpDefault::Run(base::MessagePump::Delegate*)+14                                                                                                                                                                                                                                                                                                 libgcc2.c:0
  00285785  base::MessageLoop::RunHandler()+16                                                                                                                                                                                                                                                                                                                             libgcc2.c:0
  0028da8d  base::RunLoop::Run()+12                                                                                                                                                                                                                                                                                                                                        libgcc2.c:0
  00284d2d  base::MessageLoop::Run()+12            

### ba...@chromium.org (2014-07-24)

In speech_recognition_dispatcher_->AbortAllRecognitions(), speech_recognition_dispatcher_ is not guaranteed to be != NULL.

### [Deleted User] (2014-07-24)

I pointed out in the review thread where the problem was.
The solution will be simple, just check if (speech_recognition_dispatcher_) before calling speech_recognition_dispatcher_->AbortAllRecognitions();

It is not much work to fix the problem and reland.

### bu...@chromium.org (2014-07-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/e976c3c505f83b4dc3171cfa2209eb28da72b276

commit e976c3c505f83b4dc3171cfa2209eb28da72b276
Author: qinmin@chromium.org <qinmin@chromium.org@0039d316-1c4b-4281-b951-d872f2087c98>
Date: Thu Jul 24 17:41:55 2014

Turn webspeech on/off when tab goes fore/background

This change adds a toggle to turn webspeech off when tab goes background.
And further request to turn media capture devices on will be denied.
So Both WebRTC and webSpeech won't be able to initiate new requests when tab is in background.

This CL also fixed a bug in the original CL that was reverted: some times recognition will not be aborted immediately after screen lock.
The issue is caused by that calling abort() will not delete the session in SpeechRecognitionManagerImpl.
So if a SpeechRecognition objects calls multiple start(), several sessions with the same request_id will be created.
And when passing the request_id to abort the sessions, only 1 session will be aborted
This change requests the all sessions in the same render view to be aborted.
Thus solving the above issue.

BUG=396054
R=jochen@chromium.org, tsepez@chromium.org, xians@chromium.org

Review URL: https://codereview.chromium.org/415933002

git-svn-id: svn://svn.chromium.org/chrome/trunk/src@285314 0039d316-1c4b-4281-b951-d872f2087c98



### bu...@chromium.org (2014-07-24)

------------------------------------------------------------------
r285314 | qinmin@chromium.org | 2014-07-24T17:41:55.393290Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/content/renderer/render_view_impl.cc?r1=285314&r2=285313&pathrev=285314
   M http://src.chromium.org/viewvc/chrome/trunk/src/content/renderer/speech_recognition_dispatcher.cc?r1=285314&r2=285313&pathrev=285314
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/media/media_stream_devices_controller.cc?r1=285314&r2=285313&pathrev=285314
   M http://src.chromium.org/viewvc/chrome/trunk/src/content/browser/speech/speech_recognition_dispatcher_host.cc?r1=285314&r2=285313&pathrev=285314
   M http://src.chromium.org/viewvc/chrome/trunk/src/content/renderer/speech_recognition_dispatcher.h?r1=285314&r2=285313&pathrev=285314
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/media/media_stream_devices_controller.h?r1=285314&r2=285313&pathrev=285314
   M http://src.chromium.org/viewvc/chrome/trunk/src/content/browser/speech/speech_recognition_dispatcher_host.h?r1=285314&r2=285313&pathrev=285314
   M http://src.chromium.org/viewvc/chrome/trunk/src/content/common/speech_recognition_messages.h?r1=285314&r2=285313&pathrev=285314

Turn webspeech on/off when tab goes fore/background

This change adds a toggle to turn webspeech off when tab goes background.
And further request to turn media capture devices on will be denied.
So Both WebRTC and webSpeech won't be able to initiate new requests when tab is in background.

This CL also fixed a bug in the original CL that was reverted: some times recognition will not be aborted immediately after screen lock.
The issue is caused by that calling abort() will not delete the session in SpeechRecognitionManagerImpl.
So if a SpeechRecognition objects calls multiple start(), several sessions with the same request_id will be created.
And when passing the request_id to abort the sessions, only 1 session will be aborted
This change requests the all sessions in the same render view to be aborted.
Thus solving the above issue.

BUG=396054
R=jochen@chromium.org, tsepez@chromium.org, xians@chromium.org

Review URL: https://codereview.chromium.org/415933002
-----------------------------------------------------------------

### bu...@chromium.org (2014-07-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/c9a5241f963fbf8427125cee7c625abff30b35ea

commit c9a5241f963fbf8427125cee7c625abff30b35ea
Author: qinmin@chromium.org <qinmin@chromium.org@0039d316-1c4b-4281-b951-d872f2087c98>
Date: Thu Jul 24 17:47:42 2014

Merge 285314 "Turn webspeech on/off when tab goes fore/background"

> Turn webspeech on/off when tab goes fore/background
> 
> This change adds a toggle to turn webspeech off when tab goes background.
> And further request to turn media capture devices on will be denied.
> So Both WebRTC and webSpeech won't be able to initiate new requests when tab is in background.
> 
> This CL also fixed a bug in the original CL that was reverted: some times recognition will not be aborted immediately after screen lock.
> The issue is caused by that calling abort() will not delete the session in SpeechRecognitionManagerImpl.
> So if a SpeechRecognition objects calls multiple start(), several sessions with the same request_id will be created.
> And when passing the request_id to abort the sessions, only 1 session will be aborted
> This change requests the all sessions in the same render view to be aborted.
> Thus solving the above issue.
> 
> BUG=396054
> R=jochen@chromium.org, tsepez@chromium.org, xians@chromium.org
> 
> Review URL: https://codereview.chromium.org/415933002

TBR=qinmin@chromium.org

Review URL: https://codereview.chromium.org/419503005

git-svn-id: svn://svn.chromium.org/chrome/branches/1985_128/src@285317 0039d316-1c4b-4281-b951-d872f2087c98



### bu...@chromium.org (2014-07-24)

------------------------------------------------------------------
r285317 | qinmin@chromium.org | 2014-07-24T17:47:42.844708Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/1985_128/src/content/renderer/render_view_impl.cc?r1=285317&r2=285316&pathrev=285317
   M http://src.chromium.org/viewvc/chrome/branches/1985_128/src/content/renderer/speech_recognition_dispatcher.cc?r1=285317&r2=285316&pathrev=285317
   M http://src.chromium.org/viewvc/chrome/branches/1985_128/src/chrome/browser/media/media_stream_devices_controller.cc?r1=285317&r2=285316&pathrev=285317
   M http://src.chromium.org/viewvc/chrome/branches/1985_128/src/content/browser/speech/speech_recognition_dispatcher_host.cc?r1=285317&r2=285316&pathrev=285317
   M http://src.chromium.org/viewvc/chrome/branches/1985_128/src/content/renderer/speech_recognition_dispatcher.h?r1=285317&r2=285316&pathrev=285317
   M http://src.chromium.org/viewvc/chrome/branches/1985_128/src/chrome/browser/media/media_stream_devices_controller.h?r1=285317&r2=285316&pathrev=285317
   M http://src.chromium.org/viewvc/chrome/branches/1985_128/src/content/browser/speech/speech_recognition_dispatcher_host.h?r1=285317&r2=285316&pathrev=285317
   M http://src.chromium.org/viewvc/chrome/branches/1985_128/src/content/common/speech_recognition_messages.h?r1=285317&r2=285316&pathrev=285317

Merge 285314 "Turn webspeech on/off when tab goes fore/background"

> Turn webspeech on/off when tab goes fore/background
> 
> This change adds a toggle to turn webspeech off when tab goes background.
> And further request to turn media capture devices on will be denied.
> So Both WebRTC and webSpeech won't be able to initiate new requests when tab is in background.
> 
> This CL also fixed a bug in the original CL that was reverted: some times recognition will not be aborted immediately after screen lock.
> The issue is caused by that calling abort() will not delete the session in SpeechRecognitionManagerImpl.
> So if a SpeechRecognition objects calls multiple start(), several sessions with the same request_id will be created.
> And when passing the request_id to abort the sessions, only 1 session will be aborted
> This change requests the all sessions in the same render view to be aborted.
> Thus solving the above issue.
> 
> BUG=396054
> R=jochen@chromium.org, tsepez@chromium.org, xians@chromium.org
> 
> Review URL: https://codereview.chromium.org/415933002

TBR=qinmin@chromium.org

Review URL: https://codereview.chromium.org/419503005
-----------------------------------------------------------------

### qi...@chromium.org (2014-07-26)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-07-28)

[Empty comment from Monorail migration]

### bu...@chromium.org (2014-07-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/d42d4738cc0b679e4327b86cd0f093d241836db1

commit d42d4738cc0b679e4327b86cd0f093d241836db1
Author: kerz@chromium.org <kerz@chromium.org@0039d316-1c4b-4281-b951-d872f2087c98>
Date: Wed Jul 30 02:25:04 2014

Merge 285317 "Merge 285314 "Turn webspeech on/off when tab goes ..."

> Merge 285314 "Turn webspeech on/off when tab goes fore/background"
> 
> > Turn webspeech on/off when tab goes fore/background
> > 
> > This change adds a toggle to turn webspeech off when tab goes background.
> > And further request to turn media capture devices on will be denied.
> > So Both WebRTC and webSpeech won't be able to initiate new requests when tab is in background.
> > 
> > This CL also fixed a bug in the original CL that was reverted: some times recognition will not be aborted immediately after screen lock.
> > The issue is caused by that calling abort() will not delete the session in SpeechRecognitionManagerImpl.
> > So if a SpeechRecognition objects calls multiple start(), several sessions with the same request_id will be created.
> > And when passing the request_id to abort the sessions, only 1 session will be aborted
> > This change requests the all sessions in the same render view to be aborted.
> > Thus solving the above issue.
> > 
> > BUG=396054
> > R=jochen@chromium.org, tsepez@chromium.org, xians@chromium.org
> > 
> > Review URL: https://codereview.chromium.org/415933002
> 
> TBR=qinmin@chromium.org
> 
> Review URL: https://codereview.chromium.org/419503005

TBR=qinmin@chromium.org

Review URL: https://codereview.chromium.org/431433006

git-svn-id: svn://svn.chromium.org/chrome/branches/1985_122/src@286376 0039d316-1c4b-4281-b951-d872f2087c98



### bu...@chromium.org (2014-07-30)

------------------------------------------------------------------
r286376 | kerz@chromium.org | 2014-07-30T02:25:04.258825Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/1985_122/src/chrome/browser/media/media_stream_devices_controller.cc?r1=286376&r2=286375&pathrev=286376
   M http://src.chromium.org/viewvc/chrome/branches/1985_122/src/content/browser/speech/speech_recognition_dispatcher_host.cc?r1=286376&r2=286375&pathrev=286376
   M http://src.chromium.org/viewvc/chrome/branches/1985_122/src/content/renderer/speech_recognition_dispatcher.h?r1=286376&r2=286375&pathrev=286376
   M http://src.chromium.org/viewvc/chrome/branches/1985_122/src/chrome/browser/media/media_stream_devices_controller.h?r1=286376&r2=286375&pathrev=286376
   M http://src.chromium.org/viewvc/chrome/branches/1985_122/src/content/browser/speech/speech_recognition_dispatcher_host.h?r1=286376&r2=286375&pathrev=286376
   M http://src.chromium.org/viewvc/chrome/branches/1985_122/src/content/common/speech_recognition_messages.h?r1=286376&r2=286375&pathrev=286376
   M http://src.chromium.org/viewvc/chrome/branches/1985_122/src/content/renderer/render_view_impl.cc?r1=286376&r2=286375&pathrev=286376
   M http://src.chromium.org/viewvc/chrome/branches/1985_122/src/content/renderer/speech_recognition_dispatcher.cc?r1=286376&r2=286375&pathrev=286376

Merge 285317 "Merge 285314 "Turn webspeech on/off when tab goes ..."

> Merge 285314 "Turn webspeech on/off when tab goes fore/background"
> 
> > Turn webspeech on/off when tab goes fore/background
> > 
> > This change adds a toggle to turn webspeech off when tab goes background.
> > And further request to turn media capture devices on will be denied.
> > So Both WebRTC and webSpeech won't be able to initiate new requests when tab is in background.
> > 
> > This CL also fixed a bug in the original CL that was reverted: some times recognition will not be aborted immediately after screen lock.
> > The issue is caused by that calling abort() will not delete the session in SpeechRecognitionManagerImpl.
> > So if a SpeechRecognition objects calls multiple start(), several sessions with the same request_id will be created.
> > And when passing the request_id to abort the sessions, only 1 session will be aborted
> > This change requests the all sessions in the same render view to be aborted.
> > Thus solving the above issue.
> > 
> > BUG=396054
> > R=jochen@chromium.org, tsepez@chromium.org, xians@chromium.org
> > 
> > Review URL: https://codereview.chromium.org/415933002
> 
> TBR=qinmin@chromium.org
> 
> Review URL: https://codereview.chromium.org/419503005

TBR=qinmin@chromium.org

Review URL: https://codereview.chromium.org/431433006
-----------------------------------------------------------------

### ke...@google.com (2014-07-30)

[Empty comment from Monorail migration]

### bu...@chromium.org (2014-07-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/af9bf169e93f19c084fbd6fb6733620d2fc7f440

commit af9bf169e93f19c084fbd6fb6733620d2fc7f440
Author: qinmin@chromium.org <qinmin@chromium.org@0039d316-1c4b-4281-b951-d872f2087c98>
Date: Wed Jul 30 21:53:26 2014

Merge 285314 "Turn webspeech on/off when tab goes fore/background"

> Turn webspeech on/off when tab goes fore/background
> 
> This change adds a toggle to turn webspeech off when tab goes background.
> And further request to turn media capture devices on will be denied.
> So Both WebRTC and webSpeech won't be able to initiate new requests when tab is in background.
> 
> This CL also fixed a bug in the original CL that was reverted: some times recognition will not be aborted immediately after screen lock.
> The issue is caused by that calling abort() will not delete the session in SpeechRecognitionManagerImpl.
> So if a SpeechRecognition objects calls multiple start(), several sessions with the same request_id will be created.
> And when passing the request_id to abort the sessions, only 1 session will be aborted
> This change requests the all sessions in the same render view to be aborted.
> Thus solving the above issue.
> 
> BUG=396054
> R=jochen@chromium.org, tsepez@chromium.org, xians@chromium.org
> 
> Review URL: https://codereview.chromium.org/415933002

TBR=qinmin@chromium.org

Review URL: https://codereview.chromium.org/426143003

git-svn-id: svn://svn.chromium.org/chrome/branches/2062/src@286608 0039d316-1c4b-4281-b951-d872f2087c98



### bu...@chromium.org (2014-07-30)

------------------------------------------------------------------
r286608 | qinmin@chromium.org | 2014-07-30T21:53:26.378134Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/2062/src/content/renderer/speech_recognition_dispatcher.cc?r1=286608&r2=286607&pathrev=286608
   M http://src.chromium.org/viewvc/chrome/branches/2062/src/chrome/browser/media/media_stream_devices_controller.cc?r1=286608&r2=286607&pathrev=286608
   M http://src.chromium.org/viewvc/chrome/branches/2062/src/content/browser/speech/speech_recognition_dispatcher_host.cc?r1=286608&r2=286607&pathrev=286608
   M http://src.chromium.org/viewvc/chrome/branches/2062/src/content/renderer/speech_recognition_dispatcher.h?r1=286608&r2=286607&pathrev=286608
   M http://src.chromium.org/viewvc/chrome/branches/2062/src/chrome/browser/media/media_stream_devices_controller.h?r1=286608&r2=286607&pathrev=286608
   M http://src.chromium.org/viewvc/chrome/branches/2062/src/content/browser/speech/speech_recognition_dispatcher_host.h?r1=286608&r2=286607&pathrev=286608
   M http://src.chromium.org/viewvc/chrome/branches/2062/src/content/common/speech_recognition_messages.h?r1=286608&r2=286607&pathrev=286608
   M http://src.chromium.org/viewvc/chrome/branches/2062/src/content/renderer/render_view_impl.cc?r1=286608&r2=286607&pathrev=286608

Merge 285314 "Turn webspeech on/off when tab goes fore/background"

> Turn webspeech on/off when tab goes fore/background
> 
> This change adds a toggle to turn webspeech off when tab goes background.
> And further request to turn media capture devices on will be denied.
> So Both WebRTC and webSpeech won't be able to initiate new requests when tab is in background.
> 
> This CL also fixed a bug in the original CL that was reverted: some times recognition will not be aborted immediately after screen lock.
> The issue is caused by that calling abort() will not delete the session in SpeechRecognitionManagerImpl.
> So if a SpeechRecognition objects calls multiple start(), several sessions with the same request_id will be created.
> And when passing the request_id to abort the sessions, only 1 session will be aborted
> This change requests the all sessions in the same render view to be aborted.
> Thus solving the above issue.
> 
> BUG=396054
> R=jochen@chromium.org, tsepez@chromium.org, xians@chromium.org
> 
> Review URL: https://codereview.chromium.org/415933002

TBR=qinmin@chromium.org

Review URL: https://codereview.chromium.org/426143003
-----------------------------------------------------------------

### qi...@chromium.org (2014-07-30)

[Empty comment from Monorail migration]

### pa...@chromium.org (2014-07-31)

VRP Panel, it looks like the reporter did actually try to let us know about this issue via Chrome Feedback (I've tracked down and confirmed the report with our Consumer Operations team), so I'd like us to consider this under our VRP program for a possible reward. The reporter didn't know about http://dev.chromium.org/Home/chromium-security/vulnerability-rewards-program, but said he'll use that to file issues going forward.

### pa...@chromium.org (2014-07-31)

The reporter can be reached at d.kuhnlein@standardabweichung.de

### ba...@chromium.org (2014-08-01)

This bug is marked as fixed but our list of things to do was larger:

1) Don’t allow accepting new calls (start recording) while a tab is in the background or the phone is locked.
2) Continue connection that was started before if the user locks the screen.
3) Stop speech recognition when the website is not displayed.
4) HTTPS permission stays sticky (we have UI that shows that the website is recording).
5) HTTP permission is not sticky.
6) Update Help center article to explain all of this.
7) Better permission string.
8) Show an icon in the status bar if a website is recording.

I think this is my current assessment:

1) todo
2) already the case
3) done
4) already the case
5) already the case
6) todo
7) todo
8) todo

Min, can you confirm this?

### kl...@chromium.org (2014-08-01)

I believe 1) is done and 2) only for webrtc audio due to 3)


### cl...@chromium.org (2014-08-03)

[Empty comment from Monorail migration]

### [Deleted User] (2014-08-18)

My understanding is:
1) done
2) done (webrtc audio)
3) done
4) done
5) done
6) battre, any one from the privacy team can help this?
7) battre, can you be more specific?
8) I think we show a status tray when recording is ongoing.

### mb...@chromium.org (2014-08-28)

This report qualifies for a $500 reward, but it looks like we still need to get in touch with the original reporter for this.

### ba...@chromium.org (2014-08-29)

Created https://crbug.com/chromium/408975 for the HC update.

@7 The question was whether we can convey in the permission prompt that microphone access lasts even if you lock the screen. The current message is "$SITE wants to use your microphone." and covers half of the screen already. I think now that we should put this information only on the HC article.

### ti...@chromium.org (2014-09-18)

battre@ - where did this report originate from? We want to pay a $500 reward to the originator, but it's not clear whom that was.

### mb...@chromium.org (2014-09-18)

See c#77 and c#78.

### ti...@chromium.org (2014-09-18)

Thanks Marty - I'll email them directly.


### ti...@chromium.org (2014-09-18)

Emailed d.kuhnlein@standardabweichung.de regarding instructions for receiving a reward.

### ti...@chromium.org (2014-09-19)

[Empty comment from Monorail migration]

### ti...@google.com (2014-10-21)

Processing via our e-payment system can take a few weeks, but reward should be on its way to you. Thanks again for your help!

### cl...@chromium.org (2014-11-06)

Bulk update: removing view restriction from closed bugs.

### ss...@google.com (2016-03-21)

Renaming Blink>Audio to Blink>Media>Audio for better characterization

[Monorail components: -Blink>Audio Blink>Media>Audio]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-28)

[Empty comment from Monorail migration]

### is...@google.com (2018-07-28)

This issue was migrated from crbug.com/chromium/396054?no_tracker_redirect=1

[Multiple monorail components: Blink>Media>Audio, Privacy]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080089)*
