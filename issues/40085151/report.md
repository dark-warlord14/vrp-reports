# ignored TLS errors propagate from webview to main browser

| Field | Value |
|-------|-------|
| **Issue ID** | [40085151](https://issues.chromium.org/issues/40085151) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Internals>Network>SSL, UI>Browser>Interstitials |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ja...@googlemail.com |
| **Assignee** | es...@chromium.org |
| **Created** | 2016-08-19 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36

Steps to reproduce the problem:
1. Add the attached app to Chrome. Note that it does not request any user-visible permissions.
2. Go to https://37.221.195.125/. You'll see the TLS error screen (because the hostname doesn't match the cert); do *not* click through it.
3. Open the newly installed app. You'll see the TLS error screen again, but this time half-transparent and green because it's coming from inside a webview with CSS styles.
4. Click through the half-transparent TLS error screen.
5. Now try loading https://37.221.195.125/ in the main browser window again.

What is the expected behavior?
The main browser window should still show a TLS error.

What went wrong?
Apparently the state of ignored TLS errors is shared between webviews and normal browser tabs?

I believe that this is a problem because, as shown, an app without any visible permissions can perform clickjacking attacks against TLS error screens.

Did this work before? N/A 

Chrome version: 52.0.2743.116  Channel: stable
OS Version: 
Flash Version: Shockwave Flash 22.0 r0

I guess this is low severity because it only works from app context, it requires user interaction and it's useless without a MITM position on the network?

In case this qualifies for a reward: I'm not sure whether I'm eligible to receive rewards.

## Attachments

- [webview-tls-test.crx](attachments/webview-tls-test.crx) (application/octet-stream, 1.5 KB)
- [webview-tls-test.zip](attachments/webview-tls-test.zip) (application/octet-stream, 1.4 KB)

## Timeline

### ji...@chromium.org (2016-08-19)

Personally, I feel friction is pretty high to make the attack successful. And if an extension/app really did something bad, it will be removed and blocked. Unless the attacker has access to the victim's browser and install the bad app via Developer mode. But if that's the case, much worse things can be done. 

+felt@, what do you think about this one? Should I fold it into https://crbug.com/chromium/392354?

### in...@chromium.org (2016-08-23)

Adrienne, can you please help to triage. Thanks!

### fe...@chromium.org (2016-08-29)

It seems like there are two issues here:

A) Is it OK that we are sharing exception state between the app's WV and the rest of Chrome?

My opinion: this is undesirable, even outside of the clickjacking issue. The context of an app seems different enough to me that I would expect it to have its own state. However, I suspect we do connection pooling etc across apps and regular tabs. 

Adding sleevi and jww to chime in on this issue.

==============

B) Is it OK that an app can modify the appearance and state of an interstitial inside a WebView?

This seems WAI to me in theory. WVs are meant to be controllable by the embedder. However, combined with (A) it does seem like undesirable behavior.

Adding nparker since he's thought about interstitials in WVs in the past.

[Monorail components: Internals>Network>SSL Security>UX]

### fe...@chromium.org (2016-08-29)

In terms of whether this is a security bug, the threshold for making a successful attack is very high. The attacker needs to:

-- Achieve a privileged network position (to accomplish MITM)
-- Trick the user into installing the app
-- Mount this clickjacking attack

Altogether, this doesn't seem like a promising attack vector and I'd say it's low-severity in terms of our triage guidelines. I do agree that there is a problem here though.

### rs...@chromium.org (2016-08-29)

Adrienne: The privileged network connection doesn't seem a very high bar (c.f. http://web.eecs.umich.edu/~zhiyunq/tcp_sequence_number_inference/ ), but I would suggest this represents a larger issue, and is perhaps an unresolved manifestation of https://crbug.com/chromium/291417 that was missed.

### rs...@chromium.org (2016-08-29)

Paper link: http://www.cs.ucr.edu/~zhiyunq/pub/sec16_TCP_pure_offpath.pdf

### fe...@chromium.org (2016-08-30)

+nharper, since it seems like this is related to https://crbug.com/chromium/291417

### wf...@chromium.org (2016-09-07)

[Empty comment from Monorail migration]

### fe...@chromium.org (2016-09-09)

nharper, ptal?

### rs...@chromium.org (2016-09-09)

I'm not sure why Nick got added - this is not caused by https://crbug.com/chromium/291417, just yet another manifestation of holding //net wrong. Nick's investigation was prompted by reducing Channel ID mismatches, but the //net team isn't a good owner for this - this is well beyond our ken and about how people are holding //net.

I'm moving this back to Untriaged, because it's unclear who the subject-matter experts are (aka: who owns WebView). I don't even know the right component label for webview-in-Chrome, but wjmaclean@ may know.

### rs...@chromium.org (2016-09-09)

[Empty comment from Monorail migration]

### fe...@chromium.org (2016-09-12)

fsamuel, are you still working on WebView? If so, could you help handle or triage this bug with how WV is interacting with //net?

### wj...@chromium.org (2016-09-12)

I'll take a look ...

### el...@chromium.org (2016-09-21)

589150 asks for a WebView API to allow Apps to ignore HTTPS errors programmatically.

### lg...@chromium.org (2016-11-22)

[Empty comment from Monorail migration]

[Monorail components: -Security>UX UI>Browser>Interstitials]

### es...@chromium.org (2017-11-10)

[Empty comment from Monorail migration]

### es...@chromium.org (2018-02-18)

[Empty comment from Monorail migration]

### mm...@chromium.org (2019-04-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-09-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-12-11)

[Empty comment from Monorail migration]

### es...@chromium.org (2019-12-16)

[Empty comment from Monorail migration]

### es...@chromium.org (2019-12-16)

Taking a look at this old bug... Looks like the underlying problem is that ChromeSSLHostStateDelegate remembers certificate exceptions per-profile. The net-stack state seems to be isolated as expected (different socket pools for the app and the main browser), but clicking through a cert error in the app gets stored in ChromeSSLHostStateDelegate state that is associated with the profile and notably not segregate by StoragePartition.

I'm not totally sure how to fix this. One possibility might be to key the certificate exceptions by StoragePartition path or some such... Another option might be to move the SSLHostStateDelegate into StoragePartition.

### es...@chromium.org (2019-12-17)

Upon further reflection, keying off StoragePartition is probably not the way to go here. That's too fine-grained, as we generally want certificate error clickthroughs to allow loading resources from that host in a third-party context. I'm investigating another solution which would be to separate clickthroughs in a <webview> from the state for normal web browsing. That feels a little hacky/special-casey though; I'm worried there might be other cases where keying the state on the Profile is too coarse-grained...

### rs...@chromium.org (2019-12-17)

estark: StoragePartition would be associated with profiles; NetworkIsolationKey separates the third-party context. Wouldn't having <webview> be isolated from the hosting Chrome App/Chrome Profile be the right thing?

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-12-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/05b0dc3a708df2b3e5758fa509163d29fed02d46

commit 05b0dc3a708df2b3e5758fa509163d29fed02d46
Author: Emily Stark <estark@google.com>
Date: Fri Dec 20 00:07:34 2019

Isolate cert decisions for non-default storage partition

Currently, all cert error decisions (i.e., when a user clicks through
a certificate error) are stored in ContentSettings, associated with a
Profile. This means that if a user clicks through a certificate error
in a <webview> in a Chrome App, that decisions propagates to normal
browsing. Persisting decisions within a <webview> is undesirable on
its own (because there's no UI to remind the user that they've done so
and to allow them to revoke the decision), and it's especially
undesirable for that decision to affect normal browsing. Therefore,
this CL isolates cert error decisions by storage partition. Decisions
made for the default storage partition are remembered in the normal
way (ContentSettings for the Profile); decisions for other storage
partitions are remembered in memory only.

Bug: 639173
Change-Id: If1cca181c80f8d07f5411fbb0d3707cf3755c5a2
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1974698
Reviewed-by: Mustafa Emre Acer <meacer@chromium.org>
Reviewed-by: Bo <boliu@chromium.org>
Reviewed-by: Alex Moshchuk <alexmos@chromium.org>
Commit-Queue: Emily Stark <estark@chromium.org>
Cr-Commit-Position: refs/heads/master@{#726607}

[modify] https://crrev.com/05b0dc3a708df2b3e5758fa509163d29fed02d46/android_webview/browser/aw_ssl_host_state_delegate.cc
[modify] https://crrev.com/05b0dc3a708df2b3e5758fa509163d29fed02d46/android_webview/browser/aw_ssl_host_state_delegate.h
[modify] https://crrev.com/05b0dc3a708df2b3e5758fa509163d29fed02d46/chrome/browser/ssl/chrome_ssl_host_state_delegate.cc
[modify] https://crrev.com/05b0dc3a708df2b3e5758fa509163d29fed02d46/chrome/browser/ssl/chrome_ssl_host_state_delegate.h
[modify] https://crrev.com/05b0dc3a708df2b3e5758fa509163d29fed02d46/chrome/browser/ssl/chrome_ssl_host_state_delegate_test.cc
[modify] https://crrev.com/05b0dc3a708df2b3e5758fa509163d29fed02d46/chrome/browser/ssl/ssl_browsertest.cc
[modify] https://crrev.com/05b0dc3a708df2b3e5758fa509163d29fed02d46/chrome/browser/ssl/ssl_error_controller_client.cc
[modify] https://crrev.com/05b0dc3a708df2b3e5758fa509163d29fed02d46/chrome/browser/ui/page_info/page_info.cc
[modify] https://crrev.com/05b0dc3a708df2b3e5758fa509163d29fed02d46/chrome/browser/ui/page_info/page_info_unittest.cc
[modify] https://crrev.com/05b0dc3a708df2b3e5758fa509163d29fed02d46/content/browser/ssl/ssl_manager.cc
[modify] https://crrev.com/05b0dc3a708df2b3e5758fa509163d29fed02d46/content/public/browser/ssl_host_state_delegate.h
[modify] https://crrev.com/05b0dc3a708df2b3e5758fa509163d29fed02d46/content/test/mock_ssl_host_state_delegate.cc
[modify] https://crrev.com/05b0dc3a708df2b3e5758fa509163d29fed02d46/content/test/mock_ssl_host_state_delegate.h
[modify] https://crrev.com/05b0dc3a708df2b3e5758fa509163d29fed02d46/weblayer/browser/ssl_error_controller_client.cc
[modify] https://crrev.com/05b0dc3a708df2b3e5758fa509163d29fed02d46/weblayer/browser/ssl_host_state_delegate_impl.cc
[modify] https://crrev.com/05b0dc3a708df2b3e5758fa509163d29fed02d46/weblayer/browser/ssl_host_state_delegate_impl.h


### es...@chromium.org (2019-12-20)

Update: storage partitions are indeed the right way to isolate this; as of https://crbug.com/chromium/639173#c23 I was under the mistaken impression that StoragePartitions correspond with SiteInstances, but that's not right. So cert error decisions are now isolated by StoragePartition.

### sh...@chromium.org (2019-12-20)

[Empty comment from Monorail migration]

### na...@google.com (2020-01-06)

[Empty comment from Monorail migration]

### na...@google.com (2020-01-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-01-09)

Congrats! The Panel decided to reward $500 for this report!

### na...@google.com (2020-01-09)

[Empty comment from Monorail migration]

### ad...@google.com (2020-03-13)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-03-13)

[Empty comment from Monorail migration]

### ad...@google.com (2020-03-13)

[Empty comment from Monorail migration]

### [Deleted User] (2020-03-27)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@chromium.org (2020-04-14)

[Empty comment from Monorail migration]

### ad...@google.com (2020-09-03)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/639173?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Internals>Network>SSL, UI>Browser>Interstitials]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40085151)*
