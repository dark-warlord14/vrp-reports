# Security: Inserting a Google account to Chrome and stealing user's private data

| Field | Value |
|-------|-------|
| **Issue ID** | [40078433](https://issues.chromium.org/issues/40078433) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Webstore |
| **Reporter** | ja...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2013-11-21 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

An attacker can send a malicious URL to a victim and insert his account to her Google Chrome to sync the victim's private data (history, passwords, etc.) without the victim's knowledge.

**VERSION**  

Chrome Version: [31.0.1650.57] + [stable]  

Operating System: MAC OS X 10.8.5

**REPRODUCTION CASE**  

I attached a simple PoC in PHP.

Change the email and password vars (any Google email and password under your control) and, if needed, change the millisecondsToReplaceWindow.

Sometimes the PoC does not work in the first time because some Google accounts will ask you to add the account to Chrome direct from the Web UI, in that cases you need click on "Skip for now" and reproduce the PoC again (change the millisecondsToReplaceWindow to 60000, click on 'Start the hack!' and click on 'Skip for now'. After change the millisecondsToReplaceWindow to the original value, sign out of the account in the Chrome settings and try again).

This PoC was tested in Chrome instances without other accounts linked, please create a new user if you already have an account linked to your Chrome (just disconnect your account will not solve the problem and the PoC may not work).

FIX  

You need ask the Chrome users if they really want to add an Google account to their Chrome BEFORE actually add the account, with an dialog that attackers can not control or close.

## Attachments

- [Chromiumsync_hack.txt](attachments/Chromiumsync_hack.txt) (text/plain, 3.5 KB)

## Timeline

### ja...@gmail.com (2013-11-21)

PoC attached.

### js...@chromium.org (2013-11-21)

Adding labels so someone so sync and sign-in can take a look.

### bc...@chromium.org (2013-11-21)

Quick look says it signs in and then closes the confirmation (presumably with the "undo" link) before it is seen.

source=5 is a webstore thing.  Assigning to Hui as she worked on that.

### ro...@chromium.org (2013-11-21)

Looking at the php file, the attacker uses /ClientLogin and /IssueAuthToken to mint an uber auth token for a google account they control.  They use this uber auth token with /MergeSession to stuff the cookie jar with credentials of that google account.  Note that this only works if the user is not already signed in to a google account in the content area.  They would have to log out the content area first and then do the merge session, similar to what is already described in 307159.

When the attacker calls /MergeSession, it uses unneeded URL parameters like source=chromiumsync and continue=<chrome-signin-continue-url> to make chrome think this is an attempt to sign in to chrome.  Since all this happens with real gaia URLs and with a valid account/password, chrome accepts this and connects the profile.

Note sure why source=5 is needed.  Needs more investigation.


### js...@chromium.org (2013-11-21)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-11-21)

Fixing impact labels.

### [Deleted User] (2013-11-21)

This is not a webstore specific issue, i was able to repro it for source=2 on local computer with a slightly modified script. Also by adding &sarp=1 to the mergeSession url, an attacker could suppress the Chrome signin promo page thus always succeed, even for the first time.

there are at least two issues here.

first when the untrusted signin confirmation dialog is closed without clicking 'ok, got it', e.g., by clicking the cross icon on the top right corner, or by closing the associated window as in the reported case, Chrome starts sync with default settings instead of canceling the pending signin.

Second, OneClickSigninHelper treats any non-gaia url with a google-account-signin header and a request param of source as an attempt to sign in to chrome. This is only guarded by the untrusted signin confirmation dialog, which in the reported case failed.

A simple fix is to cancel signin when the untrursted confirm dialog is closed without clicking 'ok got it'.  We should also improve our detection of chrome signin attempt, but given the current signin flow will soon be replaced by native inline UI, and the issue would no longer apply, i think we may just implement the simple fix for now.



### [Deleted User] (2013-11-21)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-11-21)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-11-21)

Medium Severity Bugs should not need this label. This is only for high+ severity bugs.

### tm...@chromium.org (2013-11-21)

[Empty comment from Monorail migration]

### ro...@chromium.org (2013-11-22)

Correction to Hui second point in https://crbug.com/chromium/321940#c7:  this comment really refers to https://crbug.com/chromium/307159.

### bu...@chromium.org (2013-11-25)

------------------------------------------------------------------------
r237115 | guohui@chromium.org | 2013-11-25T19:12:18.336520Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/ui/cocoa/one_click_signin_view_controller.mm?r1=237115&r2=237114&pathrev=237115
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/ui/cocoa/one_click_signin_dialog_controller_browsertest.mm?r1=237115&r2=237114&pathrev=237115
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/ui/views/sync/one_click_signin_bubble_view_unittest.cc?r1=237115&r2=237114&pathrev=237115
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/ui/views/sync/one_click_signin_bubble_view.cc?r1=237115&r2=237114&pathrev=237115

Security fix for untrusted signin confirm dialog

When the window associated with the confirm dialog is closed without user clicking 'ok got it', chrome starts sync with default settings. This could be exploited to sign a user's Chrome into an attacker's account, as reported in crbug 321940.

BUG=321940

Review URL: https://codereview.chromium.org/79553004
------------------------------------------------------------------------

### [Deleted User] (2013-11-25)

should we merge the fix to beta?

### tm...@chromium.org (2013-11-25)

We should probably verify it's working in this week's Dev channel, and then merge.

+release-block label for any TPM guidance in the meantime.

### cl...@chromium.org (2013-11-26)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-11-26)

[Empty comment from Monorail migration]

### ka...@google.com (2013-12-02)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-12-02)

------------------------------------------------------------------------
r238138 | rogerta@chromium.org | 2013-12-02T18:44:03.169153Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/1700/src/chrome/browser/ui/cocoa/one_click_signin_dialog_controller_browsertest.mm?r1=238138&r2=238137&pathrev=238138
   M http://src.chromium.org/viewvc/chrome/branches/1700/src/chrome/browser/ui/views/sync/one_click_signin_bubble_view_unittest.cc?r1=238138&r2=238137&pathrev=238138
   M http://src.chromium.org/viewvc/chrome/branches/1700/src/chrome/browser/ui/views/sync/one_click_signin_bubble_view.cc?r1=238138&r2=238137&pathrev=238138
   M http://src.chromium.org/viewvc/chrome/branches/1700/src/chrome/browser/ui/cocoa/one_click_signin_view_controller.mm?r1=238138&r2=238137&pathrev=238138

Merge 237115 "Security fix for untrusted signin confirm dialog"

> Security fix for untrusted signin confirm dialog
> 
> When the window associated with the confirm dialog is closed without user clicking 'ok got it', chrome starts sync with default settings. This could be exploited to sign a user's Chrome into an attacker's account, as reported in crbug 321940.
> 
> BUG=321940
> 
> Review URL: https://codereview.chromium.org/79553004

TBR=guohui@chromium.org

Review URL: https://codereview.chromium.org/99343006
------------------------------------------------------------------------

### ka...@google.com (2013-12-02)

can i close this roger?

### ro...@chromium.org (2013-12-02)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-12-02)

[Empty comment from Monorail migration]

### ja...@gmail.com (2014-01-07)

Hey guys,

Thanks for the quickly fix.

Any news of the security panel?

Cheers,
Joao Lucas Melo Brasio.

### in...@chromium.org (2014-01-08)

[Empty comment from Monorail migration]

### dh...@google.com (2014-01-09)

[Empty comment from Monorail migration]

### ja...@gmail.com (2014-01-13)

Just a note.

The Google Sign In XSRF used here was reported to Google Security Team in the report [#8-7172000002294].

Thanks.

### ja...@gmail.com (2014-01-13)

One doubt.

Why the https://crbug.com/chromium/252062 was classified with Pri-0 and Security_Severity-High and this bug with Pri-1 and Security_Severity-Medium?

What is the difference about these bugs?

Is not all about Chrome Sync?

Thanks.

### mb...@chromium.org (2014-01-13)

Thanks for the report! It qualifies for a $5000 reward. This was a particularly nasty bug, as it could have allowed an attacker to sync extensions of his or her choice to a victim's browser.

As for your concern in https://crbug.com/chromium/321940#c27, this should have been marked as high severity. I've updated it accordingly.

### ja...@gmail.com (2014-01-13)

Thank you guys.

=)

### mb...@chromium.org (2014-01-14)

[Empty comment from Monorail migration]

### ja...@gmail.com (2014-01-16)

[Comment Deleted]

### ja...@gmail.com (2014-01-16)

Please do not release this bug before the fix for the Google Sign In XSRF used in this exploit.

### ti...@chromium.org (2014-02-28)

Hey Joao,

I've moved across from the Web reward program to the Chrome one. Good to know that I'll still get to work with you over here!

As you certainly know, processing via the e-payment system can take a few weeks, but reward should be on its way to you. Thanks again for your help!

Cheers,
Tim


### ja...@gmail.com (2014-03-09)

Hey Tim,

How are you doing?

I am glad because I will have someone I know in Chromium Security Team to work with me.
=)

Ok, I can wait, thank you guys again.

Cheers,
Joao Lucas.

### cl...@chromium.org (2014-03-28)

Bulk update: removing view restriction from closed bugs.

### ti...@chromium.org (2014-04-14)

Hey Joao - can you confirm if you've received this payment yet?

### ti...@chromium.org (2014-04-14)

Actually, Finance tells me that payment is due around 29 April, so I answered my own question :)

### [Deleted User] (2016-02-02)

That script is what ya kak? Please explain to me, because I wanted depth. and want to learn



http://www.sewuanblog.tk/2016/01/cara-membuat-plugin-comment-facebook-di.html

### gl...@gmail.com (2016-04-02)

Thanks for your greeting. i have see your profile blog, i very like with your page. but i need much more about your article smile
because your article is so so nice.


http://daftarcaramembuatakunemail.blogspot.com

### we...@gmail.com (2016-07-03)

[Comment Deleted]

### we...@gmail.com (2016-07-03)

This could be dangerous attacker will know your Google account password, Thanks for sharing. 
http://caramembuatmengatasiakun.blogspot.com

### wd...@gmail.com (2016-07-11)

[Comment Deleted]

### wd...@gmail.com (2016-07-11)

should we merge the fix to beta? http://wfdshare.com

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### ba...@gmail.com (2016-10-12)

[Comment Deleted]

### an...@gmail.com (2018-03-27)

it's so dengerous,thank for sharing
https://prediksiangka888.blogspot.com


### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### ob...@gmail.com (2018-11-10)

[Comment Deleted]

### is...@google.com (2018-11-10)

This issue was migrated from crbug.com/chromium/321940?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Services>SignIn, Services>Sync, Webstore]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40078433)*
