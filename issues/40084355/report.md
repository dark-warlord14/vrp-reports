# Credential Phishing via Transparent Authenticating Proxy Vector

| Field | Value |
|-------|-------|
| **Issue ID** | [40084355](https://issues.chromium.org/issues/40084355) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Network>Auth, Internals>Network>Proxy |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | pa...@gmail.com |
| **Assignee** | as...@chromium.org |
| **Created** | 2016-05-20 |
| **Bounty** | $1,000.00 |

## Description

This impacts version Chrome version 50.0.2661.94 for OSX.

It is possible for a networked MitM to establish a transparent authenticating proxy on a network.  When this is done, a user running Chrome on that network will be prompted for entry of credentials as shown in "Screen Shot 2016-05-20 at 11.22.10 AM.png."  Unfortunately the authentication dialog references the destination host, in the case of this example: "https://www.google.com" and not the proxy host.  As a result trust is entirely lost and it is possible to trick users into entering their Google credentials into the authentication dialog as they believe that www.google.com is requesting them.  In reality the credentials are sent to the proxy controlled by the MitM where they are then available in clear text.  Note that as shown in the later 11.42.57 screenshot which is attached, this does not appear to be an OSX platform issue as Safari handles the dialog appropriately.  Note that Firefox also provides an adequate dialog.

## Attachments

- [Screen Shot 2016-05-20 at 11.22.19 AM.png](attachments/Screen Shot 2016-05-20 at 11.22.19 AM.png) (image/png, 62.8 KB)
- [Screen Shot 2016-05-20 at 11.42.57 AM.png](attachments/Screen Shot 2016-05-20 at 11.42.57 AM.png) (image/png, 41.0 KB)
- [wellsfargo_phishing_osx.png](attachments/wellsfargo_phishing_osx.png) (image/png, 104.3 KB)
- [net-internals-log.json.txt](attachments/net-internals-log.json.txt) (text/plain, 785.6 KB)

## Timeline

### lg...@chromium.org (2016-05-20)

Thanks for your report!

I can't quite tell what you mean with "establish a transparent authenticating proxy", and an internet search isn't turning up anything that would make an external proxy show up the prompt fro your fist screenshot. Could you provide more details?

### lg...@chromium.org (2016-05-21)

[Empty comment from Monorail migration]

### me...@chromium.org (2016-05-31)

Not sure how to repro this, but from the screenshots it looks like we might be showing the wrong origin in the auth dialog. Adding Http Auth label since the UI code is shared between HTTP auth and Proxy auth.

davidben: Any thoughts?

[Monorail components: Internals>Network>Auth]

### da...@chromium.org (2016-05-31)

+asanka for auth stuff.

### as...@chromium.org (2016-05-31)

Could you send us a net-internals log? https://sites.google.com/a/chromium.org/dev/for-testers/providing-network-details explains how to do so.

I'd like to understand what the transparent proxy does a bit better.

### cl...@chromium.org (2016-05-31)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-06-02)

[Empty comment from Monorail migration]

### fe...@chromium.org (2016-06-02)

[Empty comment from Monorail migration]

### fe...@chromium.org (2016-06-03)

To the reporter: could you please send a net-internals log as requested in #5? It would help us debug the issue. Thanks.

### cl...@chromium.org (2016-06-05)

[Empty comment from Monorail migration]

### sl...@google.com (2016-06-06)

lgarron: Presumably, WPAD hijacking would be sufficient for this vector.

### fe...@chromium.org (2016-06-06)

cbentzel@, I see that you've worked on some net auth bugs before. Could you PTAL at this one, or help us re-assign?

### as...@chromium.org (2016-06-06)

#11: I was thrown off a bit by the mention of a transparent proxy. We shouldn't be prompting for proxy auth challenges coming from a transparent proxy since the browser should be treating the request as having been sent via DIRECT.

I'm guessing that's not what's going on here.

### sh...@chromium.org (2016-06-07)

cbentzel: Uh oh! This issue still open and hasn't been updated in the last 17 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cb...@chromium.org (2016-06-10)

I think the issue here from screenshot (need to confirm) is that there is explicit proxy auth going on (407) but the origin of the site trying to be accessed is displayed rather than the name of the proxy. 

The screenshot shows "The proxy https://www.google.com requires a username and password."

Looking at LoginPrompt it appears this happens.

### pa...@gmail.com (2016-06-10)

A couple things:

1) Yes, it is showing the wrong origin for the proxy but see #3.
2) This attack vector works whether a user is using an authentication proxy or not.  In other words, as long as they have an autoproxy or proxy config, even if they are using a non-authenticating proxy, an attacker can intercept the HTTP response to the CONNECT and to prompt them for credentials.
3) Even if you show the correct origin, through exploitation of autoproxy configurations the attacker can simply setup the proxy as the name of the site being targeted and do a forced DNS on the network (ergo., evil WiFi vector).
4) 407 is always subject to downgrade.  It supports NTLM & Kerberos, but can be easily downgraded to basic-realm, not to mention NTLM doesn't buy much these days anyway, so that dialog must tell the user that their credentials are not safe.
5) To point #4, many users have no idea what a proxy is because they are using a host configured by their library, their government agency, or their company, therefore I believe that even asking for proxy credentials in this manner is a dubious proposition.  Therefore it would seem this needs some pushing to the OS platform unless you are going to do your own proxy implementation like the Mozilla team.  On this note, Microsoft doesn't appear to support the entry and storage of proxy authentication credentials at the OS level.  I've notified them of this bug and I would hope they are considering implementing something here.
6) This is now being tracked by CERT as VU#905344 aka., FalseCONNECT and the  Opera folks have been pointed your way as they are impacted and using Chromium. 

### pa...@gmail.com (2016-06-11)

In addition to the items covered previously, just to make sure everyone is on the same page:

7) The context of the authentication ask is within HTTPS.
8) This was trivial to exploit without DNS or WPAD tricks although WPAD is effective for those using autoproxy settings to get them to the point this vector works.  The UI misidentifies the ask within a trusted realm.
9) The result is that if the user inputs their credentials for what they believe to be a trusted HTTPS connection, they are in fact sent in clear text to an attacker.
10) Several million people are at least impacted.
11) This vector is transparent (ergo silent) for users not utilizing proxies, as such it can be setup in public areas (airports, coffee shops, hotel networks) and only target those.
12) This impacts other projects like Opera.

Please see the latest screenshot of exploitation on OSX.


### as...@chromium.org (2016-06-13)

Could you please send a net-internal log as requested in #5?

In the meantime I'll look into this.

### pa...@gmail.com (2016-06-13)

Interesting.  I responded on June 5th with the net-internal log via e-mail.  Here it is again.  It's from one of my older 32-bit machines.

### wf...@chromium.org (2016-06-13)

[Empty comment from Monorail migration]

### sl...@google.com (2016-06-13)

[Empty comment from Monorail migration]

[Monorail components: Internals>Network>Proxy]

### er...@chromium.org (2016-06-13)

I agree that attributing the authentication prompt to the target server if a 407 is received before the tunnel completion is a bug, and that UI should certainly be fixed.


As a side comment though, unfortunately I don't believe that along will solve the general problem with HTTP auth UI. If a user was fooled by this phishing attempt, they may just as easily be fooled by the modified string:

   The proxy "http://www.wellsfargo.com" requires a username and password.

Or for that matter simply painting a similar looking dialog on another webpage.

There isn't the ordinary lock icon UI to guide user's understanding here, and auth UI is not generally something users are trained to understand, nor for that matter one easily distinguished as originating from the browser. Proxy auth UI in particular is a disaster in terms of user expectations as it can pop up at completely unexpected times and not as the result of direct user action.

### pa...@gmail.com (2016-06-13)

Spot on!

Because this is an authentication ask within a security (HTTPS) realm it will always be a vector for phishing if only minor tweaks are made to the wording.  As such I believe the only way to properly handle this is to direct the user to their proxy settings where they must enter their credentials in the proxy setup.  This may not be so hard for iOS, OSX, Android, and ChromeOS, however, Windows could pose some challenges as the last time I checked it doesn't support the entry of proxy authentication credentials in their proxy setup.  Microsoft has been notified as IE, Edge, and their Windows apps are impacted but have yet to engage in a conversation with me about this vector.

### er...@chromium.org (2016-06-13)

RE https://crbug.com/chromium/613626#c23 -- Ah, I see that is your proposal in https://crbug.com/chromium/613626#c16. Apologies I had not quite digested that when I first read it :)

I think there is merit to the idea (i.e. basically have the password manager be solely responsible for filling those in), but that is probably a separate discussion to be had.

Cheers.

### pa...@gmail.com (2016-06-14)

I'm talking with the Apple folks tomorrow and will be doubling down on the recommendation.  I've notified Microsoft of a bunch of FalseCONNECT related issues in their products and have given them a heads up on what I'd like to see.  Google keeps pointing me to your team.  If we are going to get this tackled, now is the time to lay that foundation.  The idea may not be helpful for this round of patching but certainly is something we need to do a better job at in the future.  The key here is that these dialogs, in the context of an https:// request and lock tend to imply trust.  Without turfing to the system proxy settings I believe the only rational thing to do in the near term is to implement a scull and crossbones approach where you do a red strike-through of the address, remove the lock, and pop a really scary dialog which reads:

"You are being asked to enter your proxy authentication credentials to proceed, if you don't know why this is happening, don't continue.  The credentials you enter here will not be transmitted securely."

For the win, put a shadow of skulls and crossbones as a watermark behind it.

However, in all seriousness.  This is really is the only situation I'm aware of where an authentication dialog like this can be controlled by an attacker through a clear-text vector which has implications within the security context of a request so it really is unprecedented.

### as...@chromium.org (2016-06-14)

I'll address the login prompt behavior regarding proxies which is a bad regression that went undetected since M49.

I think we can mitigate the UI issue somewhat using our login interstitial by overriding the omnibox URL in addition to hardening the login prompt string.


### as...@chromium.org (2016-06-14)

[Empty comment from Monorail migration]

### as...@chromium.org (2016-06-14)

[Empty comment from Monorail migration]

### as...@chromium.org (2016-06-16)

https://codereview.chromium.org/2067933002 for those wondering.

### me...@chromium.org (2016-06-16)

Updating OS labels.

### bu...@chromium.org (2016-06-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/098c009df7a4ddc5c23d4d3c9dccf5eff1f24c98

commit 098c009df7a4ddc5c23d4d3c9dccf5eff1f24c98
Author: asanka <asanka@chromium.org>
Date: Thu Jun 16 20:18:43 2016

Use correct origin when prompting for proxy authentication.

Since M49, Chrome has been prompting for proxy authentication
credentials using the target origin instead of the origin of the proxy
server. Even if the proxy origin was displayed correctly, a mischievous
network operator could still spoof the proxy server origin. To mitigate
these problems, this CL:

* Fixes the origin used in the proxy authentication login prompt to use
  the origin of the proxy server.

* Indicate if the proxy server connection is insecure.

* Always throw up an interstitial and clear the omnibox when showing a
  proxy auth prompt.

* Use the correct origin when saving proxy authentication credentials.

BUG=613626, 620737

Review-Url: https://codereview.chromium.org/2067933002
Cr-Commit-Position: refs/heads/master@{#400247}

[modify] https://crrev.com/098c009df7a4ddc5c23d4d3c9dccf5eff1f24c98/chrome/browser/ui/login/login_handler.cc
[modify] https://crrev.com/098c009df7a4ddc5c23d4d3c9dccf5eff1f24c98/chrome/browser/ui/login/login_handler.h
[modify] https://crrev.com/098c009df7a4ddc5c23d4d3c9dccf5eff1f24c98/chrome/browser/ui/login/login_handler_unittest.cc
[modify] https://crrev.com/098c009df7a4ddc5c23d4d3c9dccf5eff1f24c98/content/shell/browser/shell_login_dialog.cc
[modify] https://crrev.com/098c009df7a4ddc5c23d4d3c9dccf5eff1f24c98/net/base/auth.cc
[modify] https://crrev.com/098c009df7a4ddc5c23d4d3c9dccf5eff1f24c98/net/base/auth.h
[modify] https://crrev.com/098c009df7a4ddc5c23d4d3c9dccf5eff1f24c98/net/http/http_auth_controller.cc
[modify] https://crrev.com/098c009df7a4ddc5c23d4d3c9dccf5eff1f24c98/net/http/http_network_transaction_unittest.cc
[modify] https://crrev.com/098c009df7a4ddc5c23d4d3c9dccf5eff1f24c98/net/url_request/url_request_ftp_job.cc


### as...@chromium.org (2016-06-16)

Marking as Fixed for now. I didn't make any string changes in #31 due to complications that can arise when we consider this change for merge.

I'll follow up with a change for the strings after any required merges are complete.

### cl...@chromium.org (2016-06-17)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Request-XX label, where XX is the Chrome milestone.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### sh...@chromium.org (2016-06-17)

[Empty comment from Monorail migration]

### pa...@gmail.com (2016-06-17)

Please make sure you coordinate with CERT for VU#905344 or myself on the embargo.  A lot of vendors were impacted and public release needs coordinated.

### as...@chromium.org (2016-06-20)

Requesting merge into M52.

See #31 for description of issue and how the fix addresses them. The change has baked on Canary and hasn't caused problems. No string changes are being made for the change that is the subject of the merge request.

### ti...@google.com (2016-06-20)

Your change meets the bar and is auto-approved for M52 (branch: 2743)

### as...@chromium.org (2016-06-20)

Re-opening for merge.

### bu...@chromium.org (2016-06-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/8c8b7cc66aa395a12b7a25f59d9cd4d1eb71f1a4

commit 8c8b7cc66aa395a12b7a25f59d9cd4d1eb71f1a4
Author: Asanka Herath <asanka@chromium.org>
Date: Mon Jun 20 14:53:42 2016

[Merge M52] Use correct origin when prompting for proxy authentication.

Since M49, Chrome has been prompting for proxy authentication
credentials using the target origin instead of the origin of the proxy
server. Even if the proxy origin was displayed correctly, a mischievous
network operator could still spoof the proxy server origin. To mitigate
these problems, this CL:

* Fixes the origin used in the proxy authentication login prompt to use
  the origin of the proxy server.

* Indicate if the proxy server connection is insecure.

* Always throw up an interstitial and clear the omnibox when showing a
  proxy auth prompt.

* Use the correct origin when saving proxy authentication credentials.

BUG=613626, 620737

Review-Url: https://codereview.chromium.org/2067933002
Cr-Commit-Position: refs/heads/master@{#400247}
(cherry picked from commit 098c009df7a4ddc5c23d4d3c9dccf5eff1f24c98)

Review URL: https://codereview.chromium.org/2082513003 .

Cr-Commit-Position: refs/branch-heads/2743@{#397}
Cr-Branched-From: 2b3ae3b8090361f8af5a611712fc1a5ab2de53cb-refs/heads/master@{#394939}

[modify] https://crrev.com/8c8b7cc66aa395a12b7a25f59d9cd4d1eb71f1a4/chrome/browser/ui/login/login_handler.cc
[modify] https://crrev.com/8c8b7cc66aa395a12b7a25f59d9cd4d1eb71f1a4/chrome/browser/ui/login/login_handler.h
[modify] https://crrev.com/8c8b7cc66aa395a12b7a25f59d9cd4d1eb71f1a4/chrome/browser/ui/login/login_handler_unittest.cc
[modify] https://crrev.com/8c8b7cc66aa395a12b7a25f59d9cd4d1eb71f1a4/content/shell/browser/shell_login_dialog.cc
[modify] https://crrev.com/8c8b7cc66aa395a12b7a25f59d9cd4d1eb71f1a4/net/base/auth.cc
[modify] https://crrev.com/8c8b7cc66aa395a12b7a25f59d9cd4d1eb71f1a4/net/base/auth.h
[modify] https://crrev.com/8c8b7cc66aa395a12b7a25f59d9cd4d1eb71f1a4/net/http/http_auth_controller.cc
[modify] https://crrev.com/8c8b7cc66aa395a12b7a25f59d9cd4d1eb71f1a4/net/http/http_network_transaction_unittest.cc
[modify] https://crrev.com/8c8b7cc66aa395a12b7a25f59d9cd4d1eb71f1a4/net/url_request/url_request_ftp_job.cc


### as...@chromium.org (2016-06-20)

Let's wait a bit before touching M51.

### aw...@chromium.org (2016-07-13)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-14)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-19)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-20)

Congratulations! Our panel has reward $1,000 for this bug.  A member of our finance team will be in touch shortly.

### aw...@chromium.org (2016-07-25)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-08-04)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-08-12)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-09-27)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-12)

[Comment Deleted]

### aw...@chromium.org (2017-01-14)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/613626?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Internals>Network>Auth, Internals>Network>Proxy]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084355)*
