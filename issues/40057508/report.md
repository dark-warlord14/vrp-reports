# Security: UI spoofing using a very long URL

| Field | Value |
|-------|-------|
| **Issue ID** | [40057508](https://issues.chromium.org/issues/40057508) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>MediaCapture, UI>Browser>Permissions>Prompts, UI>Security (Use Subcomponent)>UrlFormatting |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | st...@gmail.com |
| **Assignee** | av...@chromium.org |
| **Created** | 2021-10-04 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

Changing the URL using `history.replaceState` to 10M+ characters causes a spoofing bug in various security UIs.

**VERSION**  

Chrome Version: 94.0.4606.71 + all channels  

Operating System: Tested on Windows 10, Mac OS, Android 11

**REPRODUCTION CASE**

# Classic Tab

1. Open <https://example.com>
2. Eval: `history.replaceState(null, '', window.location.pathname + '?' + 'x'.repeat(10000000));`
3. URL is `about:blank#blocked`

# Payment Dialog

1. Go to <https://liquangumax.github.io/apps/max-nonbasiccard/> and Install
2. Go to <https://maxlgu.github.io/pr/max-nonbasiccard/> and click Buy
3. Navigate the payment dialog to <https://example.com>
4. Eval: `history.replaceState(null, '', window.location.pathname + '?' + 'x'.repeat(10000000));`
5. URL is not displayed
6. (Optionally) change the title: `document.title='https:\u200e//google.com'`

# Screen Share Dialog

1. Open <https://example.com>
2. Eval: `history.replaceState(null, '', window.location.pathname + '?' + 'x'.repeat(10000000));`
3. Eval: `navigator.mediaDevices.getDisplayMedia()`
4. Page origin is not displayed in the dialog.

Attached are screenshots of the bug in various UIs.

**CREDIT INFORMATION**  

Reporter credit: Thomas Orlita

## Attachments

- [payment-dialog-custom-title-spoof.png](attachments/payment-dialog-custom-title-spoof.png) (image/png, 25.9 KB)
- [payment-dialog-spoof.png](attachments/payment-dialog-spoof.png) (image/png, 25.5 KB)
- [permission-access-denied-spoof.png](attachments/permission-access-denied-spoof.png) (image/png, 16.9 KB)
- [pwa-custom-title-spoof.png](attachments/pwa-custom-title-spoof.png) (image/png, 28.6 KB)
- [screen-share-dialog-spoof.png](attachments/screen-share-dialog-spoof.png) (image/png, 4.3 KB)
- [screen-share-fullscreen-share-spoof.png](attachments/screen-share-fullscreen-share-spoof.png) (image/png, 4.7 KB)
- [screen-share-tab-share-spoof.png](attachments/screen-share-tab-share-spoof.png) (image/png, 4.3 KB)
- [tab-url-spoof.png](attachments/tab-url-spoof.png) (image/png, 24.5 KB)
- [window-url-spoof.png](attachments/window-url-spoof.png) (image/png, 30.6 KB)

## Timeline

### [Deleted User] (2021-10-04)

[Empty comment from Monorail migration]

### rs...@chromium.org (2021-10-04)

Thanks for the great write-up!

I'm tentatively tagging this as Medium; it doesn't appear you're able to spoof the UI, so much as cause it to not display properly, but that still represents an interesting edge case here and definitely seems "tamper" worthy.

[Monorail components: UI>Browser>Permissions>Prompts UI>Security>UrlFormatting]

### rs...@chromium.org (2021-10-04)

nasko: Could you help route this? Your name comes up from https://source.chromium.org/chromium/chromium/src/+/413468f8e2196ea59444399c517a3a6b72fa86c3 / https://crbug.com/chromium/899788 , so I'm hoping you may have pointers or thoughts here.

### [Deleted User] (2021-10-04)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-04)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-10-04)

[Empty comment from Monorail migration]

### cr...@chromium.org (2021-10-04)

Thanks for the report.  As https://crbug.com/chromium/1255713#c2 notes, this is more about causing a missing URL or a confusing "about:blank#blocked" URL to show in dialogs, rather than showing an attacker-controlled URL, but in some of the cases it still appears to be an issue in practice.

For this specific approach, maybe there's a way to enforce an identical length limit in the renderer process to avoid failing the FilterURL check, but I'm not sure if that would rule out all the ways FilterURL might rewrite it to about:blank#blocked.

More generally, dialogs probably need to be more robust to about:blank-like URLs (as discussed in https://crbug.com/chromium/1241497 and https://crbug.com/chromium/1228702).

I don't think tab-url-spoof.png and window-url-spoof.png are significant concerns (since the attacker can't put a victim's URL in the address bar), but some of the other screenshots are concerning:
* payment-dialog-custom-title-spoof.png shows no URL, allowing the title to look like a URL.  This is a problem.
* permission-access-denied-spoof.png is confusing if not necessarily dangerous?
* pwa-custom-title-spoof.png at least shows about:blank#blocked, but also allows an attacker-controlled title.  Might be a problem.
* The screen-share images also show a missing and confusing URL.

Origin might be a better thing to display in all these cases?  avi@ / meacer@: Do you have thoughts on how to address this more generally?


[Monorail components: Blink>Payments UI>Browser>MediaCapture]

### na...@chromium.org (2021-10-05)

Removing myself as the owner, since creis@ has triaged the bug. Assigning tentatively to avi@, who has been doing some work recently, though feel free to reassign to more appropriate person.

### av...@chromium.org (2021-10-08)

I had raised the question of formatting URLs, but that doesn’t quite make me someone who has been working on this recently :)

I’m in agreement with https://crbug.com/chromium/1255713#c7 by creis@. The “about:blank#blocked” ones don’t worry me right now. The use of page-controlled titles do. I can bring this to the security UI folks; this seems like a pretty large question about what we want dialogs to look like.



### av...@chromium.org (2021-10-08)

I see the point about the disappearing origins. Let me look into the URL formatters.

### av...@chromium.org (2021-10-08)

We have too many functions for URL formatting (IMO) but I added printfs to them all and none appear to be called for these dialogs. This is concerning; let me dig further.

### av...@chromium.org (2021-10-08)

For the screen sharing dialog, the string comes from DisplayMediaAccessHandler::ProcessQueuedAccessRequest() which tries to do the right thing but hits an antipattern.

They could have done:
   picker_params.app_name = url_formatter::FormatUrlForSecurityDisplay(
       web_contents->GetLastCommittedURL(),
       url_formatter::SchemeDisplay::OMIT_CRYPTOGRAPHIC);

which would say “about:blank#blocked wants to share the contents of your screen”.

They could have done:
   picker_params.app_name = url_formatter::FormatOriginForSecurityDisplay(
       web_contents->GetMainFrame()->GetLastCommittedOrigin(),
       url_formatter::SchemeDisplay::OMIT_CRYPTOGRAPHIC);

which would correctly say “example.com wants to share the contents of your screen”.

But they did:
  picker_params.app_name = url_formatter::FormatOriginForSecurityDisplay(
      url::Origin::Create(web_contents->GetLastCommittedURL()),
      url_formatter::SchemeDisplay::OMIT_CRYPTOGRAPHIC);

and url::Origin::Create() creates a null origin, which url_formatter::FormatOriginForSecurityDisplay turns into an empty string.

Issues here:
1. The fact that “about:blank#blocked” turns into a null Origin isn’t great.
2. `FormatOriginForSecurityDisplay` should probably hard-CHECK if a null Origin is passed to it.
3. Can we do anything about the antipattern of `url::Origin::Create(web_contents->GetLastCommittedURL())`?

### av...@chromium.org (2021-10-08)

Specifically, the antipattern `url::Origin::Create(web_contents->GetLastCommittedURL())` allows a page to launder its origin into an opaque origin unrelated to its URL.

### av...@chromium.org (2021-10-08)

https://source.chromium.org/search?q=Origin::Create.*LastCommittedURL&ss=chromium

It is used more often than it should.

### av...@chromium.org (2021-10-08)

[Empty comment from Monorail migration]

### ma...@google.com (2021-10-08)

[Empty comment from Monorail migration]

### ro...@chromium.org (2021-10-08)

[Empty comment from Monorail migration]

### av...@chromium.org (2021-10-09)

I have https://crrev.com/c/3212580 for the media picker, and https://crrev.com/c/3213747 for the payment picker.

https://crrev.com/c/3213301 makes FormatOriginForSecurityDisplay CHECK for opaque origins, but that is very red for tests. I need to investigate.

The permissions prompts are probably failing due to using URLs rather than origins, but the problem is that Android doesn’t have Origin formatting like our C++ does.

### gi...@appspot.gserviceaccount.com (2021-10-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/6ae36cd32eb7c21fa2a5d4761e37ea5c272adf07

commit 6ae36cd32eb7c21fa2a5d4761e37ea5c272adf07
Author: Avi Drissman <avi@chromium.org>
Date: Mon Oct 11 23:05:56 2021

Add formatOriginForSecurityDisplay to Java

Bug: 1255713
Change-Id: I1ec7c6cb143342c12c31c6bb0d6872a12495fe4f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3216454
Reviewed-by: Ted Choc <tedchoc@chromium.org>
Commit-Queue: Avi Drissman <avi@chromium.org>
Cr-Commit-Position: refs/heads/main@{#930320}

[modify] https://crrev.com/6ae36cd32eb7c21fa2a5d4761e37ea5c272adf07/components/url_formatter/BUILD.gn
[modify] https://crrev.com/6ae36cd32eb7c21fa2a5d4761e37ea5c272adf07/components/url_formatter/android/BUILD.gn
[modify] https://crrev.com/6ae36cd32eb7c21fa2a5d4761e37ea5c272adf07/components/url_formatter/android/java/src/org/chromium/components/url_formatter/UrlFormatter.java
[modify] https://crrev.com/6ae36cd32eb7c21fa2a5d4761e37ea5c272adf07/components/url_formatter/url_formatter_android.cc


### av...@chromium.org (2021-10-13)

I have fixes for payments and screen sharing in the works. The PWA issue is in CustomTabBarView::UpdateContents() and right now it seems beyond my ability to easily fix.

### gi...@appspot.gserviceaccount.com (2021-10-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/84ce1c7414d2d7fce208787f34fedd75a083973e

commit 84ce1c7414d2d7fce208787f34fedd75a083973e
Author: Avi Drissman <avi@chromium.org>
Date: Wed Oct 13 16:36:13 2021

Correctly use FormatOriginForSecurityDisplay in the media access dialog callers

For the display of an origin, FormatOriginForSecurityDisplay is the
correct function to use. Ensure that it is used and used correctly
by the callers of DesktopMediaPicker::Show(), and in other places
where the origin of a tab needs to be displayed.

Bug: 1255713
Change-Id: Iec98e2be6a995fe59c6376516330fa84cb6b8ce4
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3212580
Reviewed-by: Guido Urdaneta <guidou@chromium.org>
Commit-Queue: Avi Drissman <avi@chromium.org>
Cr-Commit-Position: refs/heads/main@{#931084}

[modify] https://crrev.com/84ce1c7414d2d7fce208787f34fedd75a083973e/chrome/browser/ui/views/tab_sharing/tab_sharing_ui_views.cc
[modify] https://crrev.com/84ce1c7414d2d7fce208787f34fedd75a083973e/chrome/browser/ui/tab_sharing/tab_sharing_infobar_delegate_unittest.cc
[modify] https://crrev.com/84ce1c7414d2d7fce208787f34fedd75a083973e/chrome/browser/ui/tab_sharing/tab_sharing_infobar_delegate.cc
[modify] https://crrev.com/84ce1c7414d2d7fce208787f34fedd75a083973e/chrome/browser/media/webrtc/desktop_capture_access_handler.cc
[modify] https://crrev.com/84ce1c7414d2d7fce208787f34fedd75a083973e/chrome/browser/media/webrtc/display_media_access_handler.cc
[modify] https://crrev.com/84ce1c7414d2d7fce208787f34fedd75a083973e/chrome/browser/ui/views/tab_sharing/tab_sharing_ui_views_browsertest.cc


### gi...@appspot.gserviceaccount.com (2021-10-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b0eb49065f24771bf42e534e7be00c958799f27a

commit b0eb49065f24771bf42e534e7be00c958799f27a
Author: Avi Drissman <avi@chromium.org>
Date: Wed Oct 13 18:51:41 2021

Use FormatOriginForSecurityDisplay in the payment dialog

Bug: 1255713
Change-Id: I173a767c5902939c2c7031049c32eec573f2a095
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3213747
Reviewed-by: Liquan (Max) Gu <maxlg@chromium.org>
Commit-Queue: Avi Drissman <avi@chromium.org>
Cr-Commit-Position: refs/heads/main@{#931164}

[modify] https://crrev.com/b0eb49065f24771bf42e534e7be00c958799f27a/chrome/browser/ui/views/payments/payment_handler_web_flow_view_controller.cc


### av...@chromium.org (2021-10-13)

Splitting the Origin antipattern to https://crbug.com/chromium/1259711.

### av...@chromium.org (2021-10-13)

Media sharing is fixed. Payments on desktop is fixed, but payments on Android requires infrastructure for Java Origin that doesn’t yet exist and is being discussed. PWAs show URLs in CustomTabBarView::UpdateContents() but it shares a lot of infrastructure with the omnibox so it’s not clear to me how to fix it.

What else is there to do? Do we want to do a more thorough retrofit of Origin? 

### mf...@chromium.org (2021-10-14)

FWIW I have a patch up to fix the Cast dialog which should land soon.  There may need to be a similar patch for Zenith, I haven't investigated yet.

### [Deleted User] (2021-10-29)

avi: Uh oh! This issue still open and hasn't been updated in the last 15 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### av...@chromium.org (2021-10-29)

What else can be done here?

The immediate issue of missing origins in the dialogs is fixed (at least on desktop). There remain underlying issues: That GURL.GetOrigin returns a GURL (though it’s been renamed), that Origin::Create is still problematic, that the Origin infrastructure on Android is underbuilt and some of the fixes on desktop cannot be made on Android until that happens.

Is this something that we need to assemble a task force to handle, or do we call this bug done?

### [Deleted User] (2021-11-12)

avi: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-15)

[Empty comment from Monorail migration]

### ma...@google.com (2021-11-15)

[Empty comment from Monorail migration]

### sm...@chromium.org (2021-11-16)

Removing Blink>Payments as the payment-part is fixed (thanks avi@!) and this is tripping our SLO metrics for being an open P1 bug.

FWIW, I would agree with closing this as fixed given lack of apparent appetite to do the follow-throughs that you suggested; otherwise I expect it will just lie open forever :/.

[Monorail components: -Blink>Payments]

### av...@chromium.org (2021-11-16)

Closing this now; the Origin work is being tracked in https://crbug.com/chromium/1270878. Thanks, lukasza@!

### [Deleted User] (2021-11-17)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-17)

[Empty comment from Monorail migration]

### am...@google.com (2021-11-24)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-11-24)

Congratulations! The VRP Panel has decided to award you $3000 for this report. Please let us know what name or handle/pseudonym you would like used for acknowledgement of this issue in our release notes. Thank you for reporting this issue and nice work!

In the future, we kindly request that you please attach POCs and other files directly and individually to security bug reports (rather than linking or zip/compressed files). 
Failure to do so may result in a slightly reduced reward amount. Thank you!! 

### st...@gmail.com (2021-11-24)

Hi Amy,
You can use "Thomas Orlita" as the name.
Thanks!

### am...@chromium.org (2021-11-24)

Thanks and thanks for providing it again! I completely missed that you provided that in the original report above.

### am...@chromium.org (2021-11-29)

was sent to finance for VRP reward payment processing on 24 November 2021  

### am...@chromium.org (2022-01-04)

[Empty comment from Monorail migration]

### am...@google.com (2022-01-04)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-24)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-07-29)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1255713?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: UI>Browser>MediaCapture, UI>Browser>Permissions>Prompts, UI>Security>UrlFormatting]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057508)*
