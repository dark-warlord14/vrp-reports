# Picture Capture Camera Prompt On Different Origin - Chrome iOS.

| Field | Value |
|-------|-------|
| **Issue ID** | [349062458](https://issues.chromium.org/issues/349062458) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Mobile>iOSWeb |
| **Platforms** | iOS |
| **Chrome Version** | 124.0.0.0 |
| **Reporter** | ia...@gmail.com |
| **Assignee** | aj...@google.com |
| **Created** | 2024-06-24 |
| **Bounty** | $500.00 |

## Description

# Steps to reproduce the problem

1. Host the attached `cam2.html` file on your server.
2. Open Chrome on an iOS device and navigate to the hosted `cam2.html` file.
3. Click on the "Tap to open camera" button located at the top left of the page.
4. This action will open a new tab with `google.com`. After 2 seconds, it will directly open the camera app, allowing you to take a picture.
5. Return to the previous tab where `cam2.html` is open. The picture you took through the `google.com` window will appear there.

# Problem Description

### Vulnerability Description for Chrome iOS Version 126.0.6478.108 Running iOS 17.5.1

#### Vulnerability Overview

Identified a sequence of actions that demonstrates a potential security vulnerability. By hosting the `cam2.html` file on a server and navigating to it using Chrome on an iOS device, the user can click a "Tap to open camera" button located at the top left of the page. This action opens a new tab with `google.com`, which, after a delay of 2 seconds, directly launches the camera app, allowing the user to take a picture. Upon returning to the previous tab where `cam2.html` is open, the picture taken through the `google.com` window appears displayed there. This behavior could be exploited to manipulate browser tab actions and access device camera functionality.

#### Detailed Description

1. **Hosting Malicious HTML File**: An attacker hosts a specially crafted HTML file (`cam2.html`) on a server.
2. **User Interaction**: The user, while browsing with Chrome on an iOS device, navigates to the hosted `cam2.html` file.
3. **Triggering the Exploit**:
   - The user clicks on a hyperlink labeled "Tap to open camera" located at the top left of the webpage.
   - This action opens a new tab pointing to `google.com`.
   - After a 2-second delay, the browser automatically redirects to the device’s camera application.
4. **Unauthorized Camera Access**:
   - The camera app opens without further user interaction, allowing the user to take a picture.
   - The user takes a picture using the camera app, thinking it is a regular process initiated from `google.com`.
5. **Image Capture by Exploit Code**:
   - The picture taken through the camera app is captured by the exploit code embedded in the original `cam2.html` file.
   - Upon returning to the original tab, the captured image is displayed in the `cam2.html` webpage.

#### Impact

User will assume that the camera app is opened by google.com.

#### Technical Details

- **Browser Version**: Chrome iOS version 126.0.6478.108
- **Operating System**: iOS 17.5.1

#### Steps to Reproduce

1. Host the `cam2.html` file on a web server.
2. Open Chrome on an iOS device running iOS 17.5.1 and navigate to the hosted `cam2.html`.
3. Click the "Tap to open camera" button on the webpage.
4. Observe the new tab opening `google.com`, followed by the automatic redirection to the camera app.
5. Take a picture using the camera app.
6. Return to the original tab to see the captured image displayed.

###POC Video attached.

# Summary

Picture Capture Camera Prompt On Different Origin - Chrome iOS.

# Custom Questions

#### Reporter credit:

Narendra Bhati, Manager - Cyber Security at Suma Soft Pvt. Ltd , Pune - India

# Additional Data

Category: Security   

Chrome Channel: Stable   

Regression: N/A

## Attachments

- [cam2.html](attachments/cam2.html) (text/html, 1.4 KB)
- [Picture Capture Camera Prompt On Different Origin - Chrome iOS..MP4](attachments/Picture Capture Camera Prompt On Different Origin - Chrome iOS..MP4) (video/mp4, 60.9 MB)

## Timeline

### ri...@google.com (2024-06-25)

Thanks for reporting! Can you provide the POC video?

### ia...@gmail.com (2024-06-25)

@ri - Apologise I missed out to uploaded POC Video initially. Please find it attached.

### pe...@google.com (2024-06-25)

Thank you for providing more feedback. Adding the requester to the CC list.

### ia...@gmail.com (2024-06-25)

Can some one please add [ds...@chromium.org](mailto:ds...@chromium.org) into this report?

### el...@chromium.org (2024-06-25)

#5: What is the username of the person you would like CCed? (email addresses are automatically censored by our bug tracker, so don't type the @chromium.org part)

### ia...@gmail.com (2024-06-26)

@el - Apologise, I don't know his/her username and nether have idea how to add them into this report.

I want the same team who is looking at the report <https://issues.chromium.org/issues/339788219> should my this report too!

### el...@chromium.org (2024-06-26)

Done! Here you go, dslee@ :) going to mark this as a provisional Pri-2 Sev-2 security bug.

### ia...@gmail.com (2024-06-26)

@el - Thanks :)

### ia...@gmail.com (2024-06-26)

@ds - Apologise for out of context query but it is possible for you or any other iOS team mater to look in this report as well <https://issues.chromium.org/issues/346694918> that report is marked as not-feasible but looks like there is some confusion. I left few comments on that report.

### ds...@chromium.org (2024-06-26)

I removed myself from the assignee so that this issue would be triaged to the right team appropriately.

### il...@chromium.org (2024-06-27)

This doesn't reproduce on windows.

The console shows error:

```
cam2.html:36 File chooser dialog can only be shown with a user activation.

```

So the issue isn't about the camera, it's about the file chooser dialog, which happens to be triggered by a delayed script while another site is being displayed.

It's not exactly a browser vulnerability, but a potentially user deceptive behavior.

It's weird that the behavior is different on iOS and other platforms.

### il...@chromium.org (2024-06-27)

Moved to BLink>Form>File component.

### pe...@google.com (2024-06-27)

Setting milestone because of s2 severity.

### am...@chromium.org (2024-06-28)

thanks for having a look ilnik@ and reassigning to a different component
components don't automatically provide visibility of security bugs to the appropriate team 
assigning / cc'ing to blink>forms>file owners based on past file chooser work 

### tk...@chromium.org (2024-06-30)

iOS Chrome doesn't use Blink now. Please assign someone in iOS team.

### il...@chromium.org (2024-07-01)

> iOS Chrome doesn't use Blink now

Is it using webkit then?

This explains the different behavior.

Moved to chromium > mobile >iosweb. Adding owners to CC.

### il...@chromium.org (2024-07-01)

+cc [ajuma@chromium.org](mailto:ajuma@chromium.org) [gambard@chromium.org](mailto:gambard@chromium.org) [michaeldo@chromium.org](mailto:michaeldo@chromium.org)

### aj...@google.com (2024-07-01)

Thanks for the report! Does this reproduce in Safari on iOS 17.5.1 as well?

### ia...@gmail.com (2024-07-01)

@Ajuma - The issue is reproducible on Chrome for iOS but not on Safari for iOS. However, it works on Safari for MacOS and is not reproducible on Chrome for MacOS.

For Safari for MacOS I have reported it to Apple. Here is the report number OE1984963593214

### aj...@google.com (2024-07-02)

> After a 2-second delay, the browser automatically redirects to the device’s camera application.

In my testing (and also in the provided POC), the delay has to be no longer than 600ms for this to work. IMO that greatly mitigates this, since the user barely has a chance to see the new web page and will only remember interacting with the previous page. Practically speaking, the user will not have read the new origin in the omnibox, and just seeing a flash of content shouldn't be too convincing to the user (e.g., the attacker page can easily draw and flash something that looks like apple.com or google.com).

In Safari on iOS, if the delay is set to 0ms, then we sometimes see a flash of the camera being presented and then hidden. So Safari is likely using some private API to close the camera after the tab switch.

Also, for smaller delays (e.g., 100ms), Firefox on iOS shows the camera, and when the camera is closed you see google.com rather than the attacker page. So the tab switch is happening underneath the camera.

I'll file a WebKit bug asking to close the camera when the originating view is no longer in the view hierarchy.

### aj...@google.com (2024-07-02)

Filed <https://bugs.webkit.org/show_bug.cgi?id=276132>

### pe...@google.com (2024-07-17)

ajuma: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### aj...@google.com (2024-07-17)

This is an external dependency, nags are not helpful.

### ia...@gmail.com (2024-08-06)

Dear Team,

The report which was affecting, Chrome iOS got fixed by Apple but surprisingly its still affecting chrome in new iOS Version!

### aj...@google.com (2024-08-06)

The WebKit bug is still open. Did you see a fix from Apple elsewhere? If Apple fixed this for Safari on macOS, it wouldn't be necessarily be sufficient to fix on iOS, I'd expect different code changes would be needed.

### ia...@gmail.com (2024-08-06)

@Aj- You are correct, looks like the fix is yet to land for iOS. Let wait for the further updates!

### aj...@google.com (2024-10-28)

Fixed in iOS 18.1.

### ia...@gmail.com (2024-10-31)

Thanks Team, finally we can conclude this report now :)

### ia...@gmail.com (2024-11-05)

Dear Team, can we move this report to VRP team now?

### ia...@gmail.com (2024-11-08)

Just A Reminder!

Can we move this report to VRP team now?

### ia...@gmail.com (2024-11-11)

One More Reminder!

Can we move this report to VRP team now?

### am...@chromium.org (2024-11-13)

Hello, thank you, but there's no need for the repeated reminders. This issue has been in the VRP queue since 28 October when it was closed as fixed thanks to our automation (see reward-topanel hotlist).
We apologize for the delay, but there was a week recently since this issue was closed in which we did not have a VRP Panel sessions (I was OOO). Issues are also assessed in order of severity so it will be a few more days until we get to this issue. Thank you for your patience in the meantime.

### sp...@google.com (2024-11-15)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $500.00 for this report.

Rationale for this decision:
report of lower impact security UI spoof 


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-11-15)

Congratulations Narendra! Thank you for your efforts and reporting this issue to us.

### pe...@google.com (2025-02-04)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/349062458)*
