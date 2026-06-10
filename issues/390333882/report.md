# [Chrome Ios] Blank Address Bar via Blob Null Possible Spoof

| Field | Value |
|-------|-------|
| **Issue ID** | [390333882](https://issues.chromium.org/issues/390333882) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P4 |
| **Component** | UI>Browser>Omnibox |
| **Platforms** | iOS |
| **Reporter** | we...@gmail.com |
| **Assignee** | mi...@google.com |
| **Created** | 2025-01-16 |
| **Bounty** | $500.00 |

## Description


Chrome version: 131.0.6778.154
OS: IOS

##Step To Reproduce:
1. save file and run localhost and etc. (example: redir.php)

```
<?php
header("Content-Security-Policy: sandbox allow-scripts");
header("Content-Type: text/html");

echo "<!DOCTYPE html>
<html lang='en'>
<head>
    <meta charset='UTF-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <title>Redirect to Blob</title>
    <script>
        var text = `<h1>Address blank</h1>`;
        var blob = new Blob([text], { type: 'text/html' });
        var url = URL.createObjectURL(blob);
        location.href = url;
    </script>
</head>
<body>
</body>
</html>";
?>
```
2. copy & paste on chrome ios (example: localhost/redir.php)
3. check the omnibox, it will be empty

What is the expected behavior?
There should be a text “blob://null/12345” inside the address bar like in android. 

What went wrong?
The browser displays an empty URL bar with fake content inside the page.


## Attachments

- [andro_blob.jpeg](attachments/andro_blob.jpeg) (image/jpeg, 19.1 KB)
- [chrome_blobios.mp4](attachments/chrome_blobios.mp4) (video/mp4, 4.5 MB)
- [ios_blob.jpeg](attachments/ios_blob.jpeg) (image/jpeg, 21.3 KB)
- [Thu Jan 16 2025 18:17:29 GMT-0500 (Eastern Standard Time).png](attachments/Thu Jan 16 2025 18_17_29 GMT-0500 (Eastern Standard Time).png) (image/png, 35.8 KB)

## Timeline

### ti...@chromium.org (2025-01-16)

(primary shepherd)

Thanks for the report! I was able to reproduce this. After some discussions about this bug we landed on S3, but if you could demonstrate that you can get the lock icon instead of the warning then maybe it would be more useful for an attacker and it would be S2. However, we don't think this it is possible due blob-untrusted:// always having an untrusted origin.

### ti...@chromium.org (2025-01-16)

marq@, I'm assigning this based off top-level //ios since I'm not quite sure what the right component or owner should be. Can you help route this to the right team? Thanks!

### pe...@google.com (2025-01-17)

Setting Priority to P2 to match Severity s3. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### we...@gmail.com (2025-01-20)

any update ?

### fe...@google.com (2025-01-21)

Reassigning this bug to search pod since this seems to be an issue with the omnibox.

### mi...@google.com (2025-01-21)

I looked into this a bit to try and identify where this was coming from and it looks like it is coming from the omnibox component code.

Inside `LocationBarModelImpl::GetFormattedURL`, the URL is correctly of the `blob:null/<ID>` format. However, there is [code which replaces the URL with only the origin](https://source.chromium.org/chromium/chromium/src/+/main:components/omnibox/browser/location_bar_model_impl.cc;l=100) if it is a blob URL on iOS. When the origin in null, this then returns a URL with spec of an empty string.

(Note that iOS Safari displays a URL of the format "blob:null/7f76f33e-6c8a-48aa-8bc2-2ccf63e47a06" as well.)

### we...@gmail.com (2025-01-24)

any update ?

### mi...@google.com (2025-01-24)

I've uploaded [crrev.com/c/6199465](https://crrev.com/c/6199465) which updates the logic to continue to use the blob url if there is no origin.

### we...@gmail.com (2025-01-25)

I have seen the change in `location_bar_model_impl.cc`. is there any other pending code ?

### mi...@google.com (2025-01-25)

That CL is the only code change related to this bug as far as I'm aware.

### ap...@google.com (2025-01-25)

Project: chromium/src  

Branch: main  

Author: Mike Dougherty <[michaeldo@chromium.org](mailto:michaeldo@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6199465>

[iOS] Show blob URL in omnibox if the URL is `null`

---


Expand for full commit details
```
[iOS] Show blob URL in omnibox if the URL is `null` 
 
Fixed: 390333882 
Change-Id: I33dc7d006c5caa005551520d3b24c2d70dd798ab 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6199465 
Commit-Queue: Mike Dougherty <michaeldo@chromium.org> 
Reviewed-by: Mark Pearson <mpearson@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1411264}

```

---

Files:

- M `components/omnibox/browser/location_bar_model_impl.cc`

---

Hash: 09bb4eb7e85b70b9e4e472abf382c2e82198f5b6  

Date:  Fri Jan 24 20:07:44 2025


---

### we...@gmail.com (2025-01-25)

did this go into the latest update 3 hours ago to version 132.0.6834.100 on chrome ios or not? because I still reproduce on that version.

### we...@gmail.com (2025-01-25)

How long is the reward related info?

### mi...@google.com (2025-01-25)

No, the fix only just landed and it won't be released until 134.\* It won't be released earlier unless it is merged to an earlier version branch. (I was able to reproduce and validated the fix so I am fairly confident in the patch fixing the issue described here.)

The reward info takes a bit longer. I don't process those, but I believe the group that does so only reviews bugs weekly, so please wait until the end of next week at a minimum for an update regarding any potential reward.

You can also see more info about [VRP](https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/vrp-faq.md) and [Life of a Security Issue](https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/life-of-a-security-issue.md) at the respective links.

### we...@gmail.com (2025-01-25)

ohh okay. thanks for the information

### sp...@google.com (2025-01-29)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $500.00 for this report.

Rationale for this decision:
Thank you reward for report of issue that resulted in a security beneficial change for users


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-01-29)

Thank you for this report. We don't generally consider a blank origin a security issue, but incorrect ones definitely are. A security beneficial change was able to be made based on this report, so we did want to acknowledge and thank you for that.

### we...@gmail.com (2025-01-31)

I already set up payment through bugcrowd [comment #17](https://issues.chromium.org/issues/390333882#comment17)

### we...@gmail.com (2025-02-04)

I'm using bugcrowd why do I have to fill in google legacy, can you help explain? [comment #18](https://issues.chromium.org/issues/390333882#comment18)

### am...@chromium.org (2025-02-04)

Please see <https://chromium.googlesource.com/chromium/src/+/main/docs/security/vrp-faq.md#when-will-i-receive-my-reward> and check your Bughunters profile information reflects BugCrowd rather than Legacy.
This would have had to be set in your profile before the reward update in c#17.

### we...@gmail.com (2025-02-11)

hey [comment #21](https://issues.chromium.org/issues/390333882#comment21)

is there anyone who can chat/email regarding the problem of filling out the bank form. the bank I use does not have ABA, I have filled in the swift code. this is too complicated. on any platform it is common to just swift code.

### am...@chromium.org (2025-02-11)

Sorry, we don't handle payments. You'll need to confer with [p2p-vrp@google.com](mailto:p2p-vrp@google.com) about this. They can connect you with a finance team that can assist you based on your locale and banking info

### am...@chromium.org (2025-03-04)

Updating this issue to reflect the earlier assessment in c#18

### we...@gmail.com (2025-04-02)

no cve ?

### am...@chromium.org (2025-04-02)

As mentioned in c#18, we don't consider this a security issue, therefore, we are unable to issue a CVE.

### ch...@google.com (2025-05-04)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/390333882)*
