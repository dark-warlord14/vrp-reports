# security: click-to-call across devices has inconsistent escaping & URL validation

| Field | Value |
|-------|-------|
| **Issue ID** | [40054929](https://issues.chromium.org/issues/40054929) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>Sharing |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ki...@gmail.com |
| **Assignee** | pe...@chromium.org |
| **Created** | 2021-02-20 |
| **Bounty** | $3,000.00 |

## Description

**This template is ONLY for reporting security bugs. If you are reporting a**  

**Download Protection Bypass bug, please use the "Security - Download**  

**Protection" template. For all other reports, please use a different**  

**template.**

**Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com>**  

**/chromium/src/+/HEAD/docs/security/faq.md**

**Please see the following link for instructions on filing security bugs:**  

**<https://www.chromium.org/Home/chromium-security/reporting-security-bugs>**

**Reports may be eligible for reward payments under the Chrome VRP:**  

**<http://g.co/ChromeBugRewards>**

**NOTE: Security bugs are normally made public once a fix has been widely**  

**deployed.**

**-------------------------**

**VULNERABILITY DETAILS**  

**Please provide a brief explanation of the security issue.**

**VERSION**  

Chrome Version: 88.0.4324.150 (Official Build) (64-bit) (cohort: Stable)  

Operating System: Windows 10 OS Version 1909 (Build 18363.1379)

**REPRODUCTION CASE**  

**Please include a demonstration of the security bug, such as an attached**  

**HTML or binary file that reproduces the bug when loaded in Chrome. PLEASE**  

**make the file as small as possible and remove any content not required to**  

**demonstrate the bug, or any personal or confidential information.**

**Please attach files directly, not in zip or other archive formats, and if**  

**you've created a demonstration site please also attach the files needed to**  

**reproduce the demonstration locally.**

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

**Type of crash: [tab, browser, etc.]**  

**Crash State: [see link above: stack trace \*with symbols\*, registers,**  

**exception record]**  

**Client ID (if relevant): [see link above]**

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

**Reporter credit: [goes here]**

## Attachments

- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)

## Timeline

### [Deleted User] (2021-02-20)

[Empty comment from Monorail migration]

### ki...@gmail.com (2021-02-20)

Respected Sir/Ma'am,

Good evening. Hope you're doing well. Okay, yes, let's talk about the issue. I will bisect the report into few parts for better understanding.

1. As far as I know, browsers have a security implementation that one can't use "tel:" in the iframes means it won't open Phone Dialer app. Let's see a proof?
--> Enter this into the address bar: data:text/html,<iframe src='tel:+91123456789'>
Observations on 2 different Operating Systems:

Chrome Android (Dev | Version: 90.0.4413.0 | Android 9.0): It doesn't open Dialer app in the Android Browser.
Reason: I am not sure for the reason but it maybe because the one can't open applications from iframe using URIs like tel: mailto: etc?

Chrome Windows (Stable | Version: 88.0.4324.150 | Windows 10 x64): It will give a prompt like something where you can select a device where the same Gmail is logged in as Chrome (desktop) and once you'll click it, it will open the Dialer Android App. 
Reason: The Browser allowed tel URI from iframe which shouldn't be allowed.

Let's go to next step. As per @rbyers. there can be issues like Factory data reset etc can take place in some Android devices. I have kept a PoC where there is tel: with a '*' in it and it wasn't stripped out by the Browser when sent to the Dialer app of Android device. 

2. Few Browsers who are Chromium based aren't checking the characters after '*' and completely transferred the USSD code to the Dialer Application which maybe a huge concern for them. What kind of security check Chrome has implemented to protect against such issues, can you please share a link to that specific security check or feature? Thanks in advance. :) 

I will conclude here and tell that Chrome (desktop) is allowing tel: in the Iframe which shouldn't be done and which can be a huge security concern in older Android devices. I am not sure but this is also an issue in the Android device when it takes any digits on the dialer app without checking? If it is, what kind of check do Android OS have to protect users from it? I am always eager to learn something new from Chromium Security Team as they have got one of the best Browser team all over the World. Thanks in advance. Take care!

Kind Regards,
Kirtikumar A. R.

### ph...@gmail.com (2021-02-20)

[Empty comment from Monorail migration]

[Monorail components: UI>Browser>Sharing]

### jd...@chromium.org (2021-02-22)

Thanks for your report. I think what you're saying is that there are two possible bugs that intertwine interestingly:
 1. Desktop users can click a tel: link in an iframe. On Chrome, you can then send that number to a mobile Chrome, which then passes it to the dialer.
 2. Since Chrome doesn't strip # and * from the number, someone could do something nefarious.

As you noted, the second one is a known issue (crbug.com/746427). I don't know whether the lack of iframe tel support on Android is intentional or not, but it does seem plausible that we should share the behavior.

mkwst@/qinmin@: do you know if the iframe tel mitigation is intentional and/or based on some spec? Ought the desktop/Android behavior be unified?

I'm keeping this as a security bug for now, albeit Severity-Low, out of an abundance of caution. Fixing the iframe limitation would only be a fairly minimal abuse mitigation for the crbug.com/746427 issue, but whether or not unadorned iframes should have that privilege still seems like an OWP security question.

### [Deleted User] (2021-02-22)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ki...@gmail.com (2021-02-28)

[Comment Deleted]

### mk...@google.com (2021-03-01)

The relevant specs are quite vague on navigation to non-webby schemes. The switch in step 15 of https://html.spec.whatwg.org/multipage/browsing-the-web.html#navigate takes you to https://html.spec.whatwg.org/multipage/browsing-the-web.html#process-a-navigate-url-scheme, and then to https://html.spec.whatwg.org/multipage/browsing-the-web.html#hand-off-to-external-software, which waves its hands in the direction of a risk to be mitigated, but has little concrete advice about doing so.

I don't know of an intentional handling of `tel` for framed navigation, but I agree that we should be consistent across desktop and mobile. Skimming through the codebase for instances of `kTelScheme`, we have a few features which special-case it in some way (https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/chromeos/external_protocol_dialog.cc;drc=f16cad21ac6fc30b080b57bfd77db7f61a9a8927;l=119, https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/send_tab_to_self/send_tab_to_self_util.cc;drc=f16cad21ac6fc30b080b57bfd77db7f61a9a8927;l=59, https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/sharing/click_to_call/click_to_call_utils.cc;drc=f16cad21ac6fc30b080b57bfd77db7f61a9a8927;l=50), including preventing `tel:` links from being shared directly ("Click to Call" should apparently pick them up instead, if it's enabled).

+peter@ as an owner of //chrome/browser/sharing who might have opinions.

### ki...@gmail.com (2021-03-01)

Respected Sir/Ma'am,

Good evening. Hope you're doing well. :)
I am curious to know answers of few questions. Would you mind answering it and sharing your knowledge with this young kid? :) Thanks in advance.
1. Operating have some kind of mechanism not to redirect users to phone from 3rd party applications, yes? 
2. The Browser must require permission to redirect to any applications like Phone, Message etc, correct? And in the iframe it should be blocked like it does in the Chrome (Android). 

Btw, try the attached testcases too. 

Take care!

Kind Regards,
Kirtikumar A. R.

### pe...@chromium.org (2021-03-02)

[Empty comment from Monorail migration]

### kn...@chromium.org (2021-03-02)

A few observations here :-)
On Android we do seem to block navigations to external protocols here [1]. They fail with a "Navigation is blocked: tel:+xxx" log message in the JS console.
That doesn't prevent the user from clicking on tel: links though, even if the link itself is in an iframe. Relevant bug: crbug.com/594996
For desktop there is an open bug to limit external protocol navigations here: crbug.com/1011429

As for the USSD codes, we do strip parts of the tel: links here [2]. More specifically, we call GURL::GetContent() which "is everything after the scheme (skipping the scheme delimiting colon) and before the fragment (skipping the fragment delimiting octothorpe)".
Most (maybe all?) USSD codes have a '#' character in them, so they wouldn't be sent fully, is that enough to prevent bad actors?

[1]: https://source.chromium.org/chromium/chromium/src/+/master:components/external_intents/android/java/src/org/chromium/components/external_intents/InterceptNavigationDelegateImpl.java;l=158;drc=f16cad21ac6fc30b080b57bfd77db7f61a9a8927
[2]: https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/sharing/click_to_call/click_to_call_utils.cc;l=88;drc=f16cad21ac6fc30b080b57bfd77db7f61a9a8927

### ki...@gmail.com (2021-03-02)

Respected Sir/Ma'am,

Good evening. Thank you very much for a quick update @knollr. Really a good observation. Also, yes you're correct that most or maybe all the USSD codes use "#" and also, they are ending with "#", well noted. Correct me if I am wrong. And yes, the Browser safely blocked such navigation to dialer app with the message in the Chrome (Android). Unfortunately, us mere mortals cannot see crbug.com/594996 as it is restricted to security team and I am still a normal kid and not part of the Security team. Hehe. 
Getting back to point, quoting what sir/ma'am said (https://crbug.com/chromium/1180510#c10):
Most (maybe all?) USSD codes have a '#' character in them, so they wouldn't be sent fully, is that enough to prevent bad actors?
--> It is a good prevention. And you're correct nothing is being sent to the dialer app after "*", it is being stripped out. But it might be possible on Samsung or HTC users (Similar USSD issue was in past). Not only this much but there has been issue of USSD attack from browser in Apple Safari too.
I am not sure why the Chrome Desktop didn't block the `tel` protocol like it was blocked in the Android Browser. I assume that iOS will also behave the same, it should block it. Don't you think so, Chrome should behave the same for Desktop like it did in Android? Can you share a rationale, why the Chrome desktop didn't block the navigation to Dialer from an iframe?
Once again, really a good observation and thanks for dropping your knowledge. 

Kind Regards,
Kirtikumar A. R.

### kn...@chromium.org (2021-03-02)

> But it might be possible on Samsung or HTC users (Similar USSD issue was in past).
Note that removing of the # character and the following ones is done on the Desktop side before sending it down to Android already. So this is independent of the mobile device brand.

> why the Chrome desktop didn't block the navigation to Dialer from an iframe?
That's what crbug.com/1011429 is about, understanding if we can add the same restriction we have on Android to Desktop. There might be some valid use-cases like call centers that might need behaviour like that so we need to be certain it doesn't break them.

### ki...@gmail.com (2021-03-02)

> Note that removing of the # character and the following ones is done on the Desktop side before sending it down to Android already. So this is independent of the mobile device brand.
--> Correct, yes. But thing is that Browser should stop navigation to such application the Chrome itself blocks in Android that you too know. Similarly, it should be in the Desktop Browser too which can stop malicious attackers to use `tel` protocol in the iframe. 

> That's what crbug.com/1011429 is about, understanding if we can add the same restriction we have on Android to Desktop. There might be some valid use-cases like call centers that might need behaviour like that so we need to be certain it doesn't break them.
--> Apologies I missed that. You also kept in the https://crbug.com/chromium/1180510#c10. After seeing that issue, what comes to my mind is that, commonly web developers don't use `tel` in the iframe. If it was commonly used by developers, then it won't work in the Android devices because browsers safely block them while navigating. So, it would be a good idea if the team fixes the issue on the desktop too, yes? 



### ki...@gmail.com (2021-03-02)

Taken idea from my friend related to this. There is no reason to use `tel://` in an iframe. Because in the worst case, this would automatically dial the given phone number. It is, though, useful for links that have to be clicked. (One might argue, now, that you can initiate the click via XSS, but that's not the point, here ).
Same for the lesser-known/-used phone:// pseudo-protocol or better yet: Only allow http:// and https://

In the past, some soft-phone/CAPI/TAPI solutions registered that protocol in addition to tel:// for automatically dialing the given number, when clicked. 


### ki...@gmail.com (2021-03-03)

Good morning. Would you mind if we have @eric sir in this bug report? I saw his comment on crbug.com/746427
His https://crbug.com/chromium/1180510#c15 caught my eyes which also describes similar issue in iOS. Also, see the https://crbug.com/chromium/1180510#c18, it says:

If we wanted to explicitly stop these from opening the dialer at all on the Chrome side of things, we could maybe add a check to ExternalProtocolHandler::LaunchUrl() to block URLs that have the 'tel:' scheme and start with some form of "*" or "#" or "//*" or "//#".

Thanks in advance. Have a great day ahead!

### [Deleted User] (2021-03-11)

[Empty comment from Monorail migration]

### zh...@google.com (2021-03-17)

[Empty comment from Monorail migration]

### ki...@gmail.com (2021-03-25)

Friendly ping. :) 

### ki...@gmail.com (2021-03-29)

[Comment Deleted]

### kn...@chromium.org (2021-03-29)

Sorry for the late response. I had another look at how we process tel links from clicking on a Desktop platform to receiving it on Android and noticed that we URL-decode the link twice.
The first decoding happens here on the Desktop side: https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/sharing/click_to_call/click_to_call_utils.cc;l=89;drc=0be726335b03670b246b23a41abbbfbd21b76a77
The second one here on the Android side: https://source.chromium.org/chromium/chromium/src/+/master:chrome/android/java/src/org/chromium/chrome/browser/sharing/click_to_call/ClickToCallMessageHandler.java;l=119;drc=59d3a0d03d4da59f54dcf1a860e6c156d5be1354

The result of this is that clicking on the following link on Desktop and selecting a device via ClickToCall will open the IMEI device info page on Android (on Android N and below + O&P if the screen is on & unlocked immediately, other OS versions require an additional click on a notification on Android):
<a href="tel:*%252306%2523">

The first "%25" here will be decoded to "%" (and won't be stripped by GURL::GetContent()). We then send the string "*%2306%23" to Android which decodes it again, now replacing "%23" with "#", resulting in an Intent for "tel:*#06#".
Note that this is not different from a user on Android clicking on a link like this directly: <a href="tel:*%2306%23">. We still require the user to click on their device when they see the ClickToCall dialog on desktop.

### ki...@gmail.com (2021-03-29)

Respected Sir/Ma'am,

Good evening. No worries. Hope you're doing well on the side of the screen. Firstly, thank you very much for a crystal clear explanation. 

It isn't like that user will have to click "call" to perform but the tricky stuff over here is that Chrome Android Browser blocks from iframe but not Desktop. Now, talking about USSD attack, yes, in latest Android OS, it won't be possible directly but you know what, in earlier Android device if you sent any USSD code to dialer app, it will directly execute and the user isn't required to press "Call" like it is happening in last Android OS. If I am not wrong, the Android device you tested is surely Android 5.0 Lollipop or above or most probably it will be Marshmellow, Nougat or Oreo, yes? Did you try on older versions of Android and just adding some extra information that this was possible in past, Samsung and HTC device as I mentioned in my https://crbug.com/chromium/1180510#c11, you can check about it here [1] 

Not only this much but as per [2], there was a Code execution using USSD attack and as per that blog it was done though webpages  so, it would be through browsers, yes? And Chrome is also our beloved Browser which has maximum Browser downloads on Play Store (telling as per the number of download). 
What is stated in the blog:
```
Further investigation revealed that redirects within web pages, either hard-coded or javascript, could also be used to push an arbitrary USSD code to the phone’s dialer. The feature being abused to trigger the reset is normally used to make placing phone calls easier while operating in the web browser. The disclosure shows that some unpatched devices could trigger the factory reset without human interaction.
```
It has also written that other browsers were vulnerable:
```
“The Unstructured Supplementary Service Data (USSD) code (which we won’t reproduce here) apparently only works on Samsung phones running Touchwiz, and only if you are directed to the dodgy destination while inside the stock browser (rather than Chrome, for example). “
```
There are few other browsers which are Chromium based and Samsung Internet is one of them and they are "pre-installed" in Samsung device. :) 
As per [2], the impacts are:
```
The full impact of this issue depends on the USSD codes available on a given device (i.e. what they do) and whether they execute automatically. These codes are not publicized by the carriers, although available in various forums online, and functions more damaging than factory reset might not exist. Regardless, the automatic execution of such codes is a vulnerability we will monitor and test further.
```
Adding few other references just in case if you're curious to know how this was an issue in the past. :) 

As per [3], it can wipe complete devices and this looks something dangerous of matter of concern. 

Now, speaking of https://crbug.com/chromium/1180510#c20 of @knollr sir/ma'am. 
That's really tricky, yes? You might already be aware already but adding one more idea that there is not just one was to decode it let's say if somebody has encoded it in QR code and it is later decoded and performs USSD attack? If you're curious how this type of attack works, see [4] . So, we can say that there isn't always only one way to get answer 4, one can do 2+2 as well as 3+1 and maybe there will be other ways to exploit such issues? We aren't knowing, how it will be handled in the future maybe if there will be some faulty code with which such remote attack is chained, it will become a nightmare. Why don't we take precaution beforehand and anticipate about upcoming problems? Not only this much but also, there is "No Website", you will find sharing USSD code to be click, did you notice? They are in plain text because they are well aware it can be dangerous and the reader will get into problem. 

> The first "%25" here will be decoded to "%" (and won't be stripped by GURL::GetContent()). We then send the string "*%2306%23" to Android which decodes it again, now replacing "%23" with "#", resulting in an Intent for "tel:*#06#".
Note that this is not different from a user on Android clicking on a link like this directly: <a href="tel:*%2306%23">. We still require the user to click on their device when they see the ClickToCall dialog on desktop.

Absolutely correct. But don't you think so in older Android devices, it will be dangerous and can go upto "Factory Data Reset"? It isn't a good idea if an attacker erases users device by sending USSD code from Chrome Browser like it isn't good if an attacker can abuse NTFS Corruption which is a Windows bug from Browser, yes? Chrome security team will never like if there browser is being used for causing harm to mere mortals like me, yes? :)

Thanks once again. Take care!

Questions:
1. This will be fixed? 
2. When the bug will will be labeled as "allpublic"?


[1]: https://www.computerworld.com/article/2491713/ussd-attack-hit-sim-cards-and-samsung-android-devices.html
[2]: https://www.nowsecure.com/blog/2012/09/24/remote-ussd-code-execution-on-android-devices/
[3] https://www.androidauthority.com/touchwiz-vulnerability-data-wipe-117800/
[4]: https://resources.infosecinstitute.com/topic/qr-code-ussd-attack/

Ref:
1. https://www.computerworld.com/article/2491713/ussd-attack-hit-sim-cards-and-samsung-android-devices.html#:~:text=Attacks%20that%20wipe%20data%20on,disable%20SIM%20cards%2C%20experts%20say&text=A%20variation%20of%20the%20recently,many%20Android%20phones%2C%20researchers%20say.
2. http://www.bluekaizen.org/killing-android-mobile-sim-cards-using-ussd/
3. https://www.techcentral.ie/ussd-attack-not-limited-to-samsung-android-devices/
4. https://troopers.de/wp-content/uploads/2012/12/TROOPERS13-Dirty_use_of_USSD_codes_in_cellular-Ravi_Borgaonkor.pdf
5. https://www.androidauthority.com/touchwiz-vulnerability-data-wipe-117800/

### ki...@gmail.com (2021-03-29)

[Comment Deleted]

### ki...@gmail.com (2021-03-29)

[Comment Deleted]

### kn...@chromium.org (2021-04-06)

Thanks for the additional information!

To summarize, I'd suggest the following next steps for this particular bug:
1) Fix the double url-decoding I found and mentioned in https://crbug.com/chromium/1180510#c20 by always sending url-encoded numbers from Desktop
    Alternatively keep the decoded number on Desktop but don't decode again on Android.
2) Ignore received numbers that contain "*" or "#" after url-decoding on Android (we already stripped everything after "#" but that didn't work because of https://crbug.com/chromium/1180510#c20)
    This is to guard against older Chrome Desktop versions or custom builds.
3) Don't offer Click to Call devices on Desktop for numbers that would fail the validation in 2)
    Optional step but makes it clear that these numbers won't work with Click to Call.

I consider the iframe specific parts of this bug as out of scope given that we already have crbug.com/1011429 and the potentially harmful USSD codes won't be available for Click to Call anymore after the steps outlined above.

peter@ / mkwst@ WDYT?

### ki...@gmail.com (2021-04-06)

Can you please mention the reason how come it will be out of scope? Because you can transfer the Balance from one device to another directly just by sending USSD code and can perform steps like enabling and disabling functions. If this issue was limited to Restart, it can be DoS and yes then you can count it Out of scope. But as far as I can tell, it can also "reset" users device using the steps I mentioned in my previous comments. I hope that this isn't limited to restart which is DoS but wiping a user's device from Chrome browser is something which should be qualified, yes? Thanks in advance. :) 


### kn...@chromium.org (2021-04-06)

The out of scope part is to do special handling for iframes on Desktop. The current difference we have is that navigating an iframe on Android to an external protocol will be ignored, while on Desktop we will forward them to apps or, for tel: links, offer Click to Call. This is confusing to users as the number is not initiated from the top level origin which is why we show the iframe origin in the Click to Call dialog in those cases.

My reasoning for making this out of scope is that we already have crbug.com/1011429 that will look into iframe navigations to external protocols *and* USSD codes won't be able to be sent at all, including iframes, after the steps outlined in https://crbug.com/chromium/1180510#c24 are implemented.

### ki...@gmail.com (2021-04-06)

[Comment Deleted]

### el...@chromium.org (2021-04-21)

Sharing triage:
* Clarifying the summary
* Setting a target milestone, despite severity-low
* Bumping priority

### kn...@chromium.org (2021-04-22)

A CL for this is already in review: crrev.com/c/2825704
Should land soon and make it into M92 :-)

### ki...@gmail.com (2021-04-22)

Respected Sir/Ma'am,

@knollr, I would request you make this issue allpublic as per the comment: http://crbug.com/1199402#c58
Thanks in advance. It was a great pleasure working with Chromium Security team. 

### am...@chromium.org (2021-04-22)

kirtiar@, as mentioned in my response to your bug/comment linked above, this bug cannot be marked allpublic at this time. That will occur 14 weeks after status is Fixed/Closed. 

### ki...@gmail.com (2021-04-22)

For this issue, I will be acknowledged as this isn't a dup, yes?

### gi...@appspot.gserviceaccount.com (2021-04-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/e041be8dc8b5b9e3012e752c2636fcf1cd8b0b1d

commit e041be8dc8b5b9e3012e752c2636fcf1cd8b0b1d
Author: Richard Knoll <knollr@chromium.org>
Date: Fri Apr 23 08:56:16 2021

Prevent USSD codes via Click to Call

Click to Call allows users to send a phone number from their Chrome
desktop instance to their Android phone. This number either comes from a
user's selection and sent via the context menu, or by clicking on a link
with a "tel:" href.
Sending from the context menu is gated by a regular expression and will
not allow any special characters like '#' or '*' to be contained in the
phone number.
Sending link hrefs does not go through that check as we assume the link
is a valid phone number. We do call GURL::GetContent() to get the number
which should discard anything after a (and including the) '#' character.
However, we also URL-decoded the resulting string before then sending it
over to Android, where we URL-decoded it again when constructing the
Dialer intent. This allows sending double-URL-encoded USSD tel links
which will be sent straight to the Dialer on certain Android versions
and device states.

The fix here is on both desktop and Android side:
Desktop:
 - URL-decode the number and ignore if it contains '#', '*' or '%'.
 - Send the raw number (URL-encoded) to Android
Android:
 - Verify that URL-decoding the received raw number is valid as above
 - Show the decoded number in the notification
 - Parse the raw number in Java into a Uri object for the Dialer

Together this makes sure that we only URL-decode tel: links once and
verify it on both sender and receiver side before passing it on to the
Android Dialer.

Bug: 1180510
Test: updated unit_tests and browser_tests to check for conversion
Change-Id: Idf380b629cdf00155ecab054398af69f37ec2ef9
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2825704
Reviewed-by: Robert Kaplow <rkaplow@chromium.org>
Reviewed-by: David Jacobo <djacobo@chromium.org>
Reviewed-by: Gayane Petrosyan <gayane@chromium.org>
Reviewed-by: Istiaque Ahmed <lazyboy@chromium.org>
Reviewed-by: Peter Beverloo <peter@chromium.org>
Commit-Queue: Richard Knoll <knollr@chromium.org>
Cr-Commit-Position: refs/heads/master@{#875572}

[modify] https://crrev.com/e041be8dc8b5b9e3012e752c2636fcf1cd8b0b1d/chrome/android/java/src/org/chromium/chrome/browser/sharing/click_to_call/ClickToCallMessageHandler.java
[modify] https://crrev.com/e041be8dc8b5b9e3012e752c2636fcf1cd8b0b1d/chrome/android/junit/src/org/chromium/chrome/browser/sharing/click_to_call/ClickToCallMessageHandlerTest.java
[modify] https://crrev.com/e041be8dc8b5b9e3012e752c2636fcf1cd8b0b1d/chrome/browser/BUILD.gn
[modify] https://crrev.com/e041be8dc8b5b9e3012e752c2636fcf1cd8b0b1d/chrome/browser/ash/arc/intent_helper/arc_external_protocol_dialog.cc
[modify] https://crrev.com/e041be8dc8b5b9e3012e752c2636fcf1cd8b0b1d/chrome/browser/ash/arc/intent_helper/arc_external_protocol_dialog_unittest.cc
[modify] https://crrev.com/e041be8dc8b5b9e3012e752c2636fcf1cd8b0b1d/chrome/browser/renderer_context_menu/render_view_context_menu.cc
[modify] https://crrev.com/e041be8dc8b5b9e3012e752c2636fcf1cd8b0b1d/chrome/browser/send_tab_to_self/send_tab_to_self_util_unittest.cc
[modify] https://crrev.com/e041be8dc8b5b9e3012e752c2636fcf1cd8b0b1d/chrome/browser/sharing/click_to_call/click_to_call_message_handler_android.cc
[modify] https://crrev.com/e041be8dc8b5b9e3012e752c2636fcf1cd8b0b1d/chrome/browser/sharing/click_to_call/click_to_call_message_handler_android.h
[add] https://crrev.com/e041be8dc8b5b9e3012e752c2636fcf1cd8b0b1d/chrome/browser/sharing/click_to_call/click_to_call_message_handler_android_unittest.cc
[modify] https://crrev.com/e041be8dc8b5b9e3012e752c2636fcf1cd8b0b1d/chrome/browser/sharing/click_to_call/click_to_call_ui_controller.cc
[modify] https://crrev.com/e041be8dc8b5b9e3012e752c2636fcf1cd8b0b1d/chrome/browser/sharing/click_to_call/click_to_call_ui_controller_unittest.cc
[modify] https://crrev.com/e041be8dc8b5b9e3012e752c2636fcf1cd8b0b1d/chrome/browser/sharing/click_to_call/click_to_call_utils.cc
[modify] https://crrev.com/e041be8dc8b5b9e3012e752c2636fcf1cd8b0b1d/chrome/browser/sharing/click_to_call/click_to_call_utils.h
[modify] https://crrev.com/e041be8dc8b5b9e3012e752c2636fcf1cd8b0b1d/chrome/browser/sharing/click_to_call/click_to_call_utils_unittest.cc
[modify] https://crrev.com/e041be8dc8b5b9e3012e752c2636fcf1cd8b0b1d/chrome/browser/ui/views/sharing/click_to_call_browsertest.cc
[modify] https://crrev.com/e041be8dc8b5b9e3012e752c2636fcf1cd8b0b1d/chrome/test/BUILD.gn
[modify] https://crrev.com/e041be8dc8b5b9e3012e752c2636fcf1cd8b0b1d/tools/metrics/histograms/histograms_xml/sharing/histograms.xml


### ad...@google.com (2021-04-23)

 kirtiar15502@ I see no evidence that this is a duplicate.

As we regard this as Low severity, we won't take any stability risk by merging it back to beta or stable branches. Therefore this is likely to be released in M92 and you can expect to be credited then - https://chromiumdash.appspot.com/schedule.

### ki...@gmail.com (2021-04-24)

Oh, ok thanks. By that time, can you please check other Spoofing issues which I have sent and are open since December? Thanks. 

### kn...@chromium.org (2021-04-26)

Marking as fixed after https://crbug.com/chromium/1180510#c33 landed in Canary for M92 and manually verified that a default build does not offer ClickToCall for links containing '#', '*' or '%'.
Also tried modifying a local build to not include the check and send numbers containing those characters and verified that no notification / dialer popped up and there are entries in chrome://histograms for Sharing.ClickToCallPhoneNumberValid.

### [Deleted User] (2021-04-26)

[Empty comment from Monorail migration]

### ki...@gmail.com (2021-04-26)

Am I allowed to send similar issues? 

### [Deleted User] (2021-04-27)

[Empty comment from Monorail migration]

### ad...@google.com (2021-05-06)

> Am I allowed to send similar issues?

I'm not sure I understand the question. But yes, if you find new bugs which are not fixed by this fix, please report them! :)

### ki...@gmail.com (2021-05-13)

Hello @adetaylor sir,

Good evening. I will verify it before sending. Would you mind adding @ericlaw and homesen83@gmail.com into CC? As I took help of Eric sir while I was understanding URL handlers (also, used his report in reference) and HomeSen sir for the USSD stuff. Thanks once again! :)




### ad...@chromium.org (2021-05-13)

[Empty comment from Monorail migration]

### ki...@gmail.com (2021-05-13)

Thanks! :) 

### am...@google.com (2021-05-20)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ki...@gmail.com (2021-05-20)

Respected Sir/Ma'am,

Hope everything is OP on the side of your screen. Wait.. what? Thanks @amyressler sir/ma'am for getting cherry on the top in my bug for second time in a row. Looking forward for the "hat-trick". 

As the issue was in collaboration. So, yes, they should also be acknowledged too. 
 
Acknowledgement details: Patrick "HomeSen" Walker, Eric Lawerence (@ericlaw) & Kirtikumar Anandrao Ramchandani (@Kirtikumar_A_R)

Thanks to all the team members for great co-operation and working so quickly. GGs to Chrome Security team and GGs to HomeSen & Eric. Take care!

Kind Regards,
Kirtikumar A. R.


### ho...@gmail.com (2021-05-20)

Awesome find, my friend.
For Acknowledgement, can I have my Twitter handle added, please. So, it would be: Patrick Walker (@homesen).

Thank you :)

Kind regards
Patrick

### er...@microsoft.com (2021-05-20)

My last name is Lawrence (extra "e" is not needed) but I don't need any credit for this one.

### am...@chromium.org (2021-05-20)

Congratulations Kirtikumar and Patrick! Yes, I'll be sure to Patrick (complete with twitter handle) when we credit this issue in the release notes. Nice work! 

### am...@google.com (2021-05-21)

[Empty comment from Monorail migration]

### ki...@gmail.com (2021-05-27)

Hello,
Good afternoon. 
RE https://crbug.com/chromium/1180510#c48: Thank you @amy ma'am. :)

I am currently not sure about this. But @knollr is it possible to check this case as well? We've got one more URI like `tel:` which is `callto:`. I was trying to go more deeper for the `tel:` URI in the RFC5341 at [1]. While going through that, something which clicked to me was about Skype which also has ability to call and as Skype uses URI like `callto:`, if we use that URI with the USSD code, it will directly be called, PTAL at [2]. Currently, I haven't tried to check if this will be possible to use. Like if we use USSD code and if the user has selected Skype as application which should be used then it might be problem. 

And is it really possible to use phone number without prefix `tel:`? Maybe check [3].

Viber also has a URI  like `viber://` it also has calling function but have never seen a real life example where it will be possible to make a call. Like for whatsapp too we have ability to send a text and that too the test will be added in the text box but won't be sent until user clicks `>`/Send. So, yes, application like this who have calling function won't be affected from it and as Chrome would be stripping it out on their behalf for `tel:` URI, there won't be issue.

Will `callto:` have similar issue? The protection is well implemented by the team for `tel:` URI as the `%` itself is blocked so, everything is in good hands and there is no bypass. :P But would be happy if one can check for this `callto:` functionality. Does this work? I don't have skype on my device but maybe try with this:

data:text/html,<a href="callto:*%2306%23">click</a>

When I use that URI in the Chrome stable (OS: Android), it says about:blank#blocked, looks like to be good but no idea why it has different behavior in the Desktop. I don't have one iOS device on my hand. So, I don't know what is behavior on it. But most probably iOS will have same behavior as Android.


[1]: https://datatracker.ietf.org/doc/html/rfc5341
[2]: https://stackoverflow.com/questions/20132663/sending-ussd-code-programmatically-dials-skype-instead-of-normal-phone-call
[3]: https://www.wikidata.org/wiki/Property:P1329

### kn...@chromium.org (2021-05-27)

Click to Call (the feature that sends a number from desktop > phone) is only shown for tel: links [1] and won't show for callto: or other external protocols.
If you find an issue with those links (callto, viber, etc) feel free to open a new bug with the repro steps but it'll likely not affect Click to Call.

[1]: https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/sharing/click_to_call/click_to_call_utils.cc;l=82;drc=9fcc9d7b2915b6192ee6810eec54c50deb6313c6

### ki...@gmail.com (2021-05-27)


Yes, correct. `callto:` isn't allowing to send to the device like the `tel:` was doing. I will create a new issue for `callto:` if it is successful. Thanks for clarification. 

### am...@chromium.org (2021-07-19)

[Empty comment from Monorail migration]

### am...@google.com (2021-07-19)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2021-08-03)

[Empty comment from Monorail migration]

### mi...@gmail.com (2023-08-25)

[Comment Deleted]

### mi...@gmail.com (2023-08-28)

[Comment Deleted]

### yu...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1180510?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40054929)*
