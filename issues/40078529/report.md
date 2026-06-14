# Security: Cross-domain bug in password manager

| Field | Value |
|-------|-------|
| **Issue ID** | [40078529](https://issues.chromium.org/issues/40078529) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **CVE IDs** | CVE-2010-0556 |
| **Reporter** | 0a...@gmail.com |
| **Assignee** | ti...@chromium.org |
| **Created** | 2010-01-20 |
| **Bounty** | $500.00 |

## Description

I have not had a lot of time to test various scenarios with this issue.  If
you have trouble reproducing, just let me know and I can try to get a more
precise test case.

In messing around with HTTP digest authentication, I discovered a behavior
where the password manager pre-populates the login form for one domain with
the credentials for *another domain*.  It doesn't submit them
automatically, but does leave the user one click away from sending
credentials to the wrong place.

Here are the steps I followed on Chrome 3.0.195.38 under Windows 7 (release
candidate):

0. Set up an HTML page with the following contents:
   <html><body>
     <img src="http://evil.example.com/image.png" />
   </body></html>

   This page should be hosted at (not protected by any auth):
     http://victim.example.org/test-img.html


1. Next, set up an HTTP digest protected area under the following URL:
   http://victim.example.org/private/


2. Now set up the attacker's server to be digest protected, so 
   that the following URL should prompt for digest auth:
   http://evil.example.com/image.png


3. Log in to a digest-protected area such as: 
   http://victim.example.org/private

   Save the password in the password manager.


4. Now, access the unauthenticated HTML page on the victim's server:
   http://victim.example.org/test-img.html
     
   Since the embedded image requires authentication, you should get a
   password prompt.  

The vulnerability I encountered is that the password manager actually
prepopulates victim.example.org's credentials in this dialog.  In message
board websites, or anywhere that an attacker can post links to images on
third party sites, this could be a serious phishing issue.  No other
browser I tested does this.

With digest authentication, this isn't the end of the world since passwords
aren't that easy to get at, but I would be surprised if basic
authentication prompts don't have the same behavior.

I was doing some general security testing on many browsers when I came
across this issue.  I have some additional observations about security
weaknesses in this area which affect many browsers that I'll be publishing
in a week or so.  I will drop a link somewhere here when I get it out and I
hope some of your devs will have a chance to review it.

thanks!


## Timeline

### sc...@gmail.com (2010-01-21)

Thanks for the report.
Wan-Teh, Eric - any thoughts? I haven't had time to look into this.

Regarding your upcoming report, we'd love to get a pre-release version to see if 
there's anything serious we want to tackle before it goes public.
cc:Ian because I believe he's look at some of the previous password manager studies.

### er...@chromium.org (2010-01-21)

I don't reproduce this.

I just tested in Chrome 4.0.249.64, and 3.0.195.38. In both cases for me, in step (4) the 
auth dialog was prompted as expected, however it was *NOT* pre-filled with the 
password from victim.example.org.

My tests used Windows Vista, and for the digest realms I used apache webservers.

### 0a...@gmail.com (2010-01-21)

[Comment Deleted]

### er...@chromium.org (2010-01-21)

Actually I was able to repro this locally now.

The trick is both realms need to be the same.

### er...@chromium.org (2010-01-21)

[Empty comment from Monorail migration]

### 0a...@gmail.com (2010-01-21)

OK, great, thanks for trying that again.

Typically we (www.vsecurity.com) release advisories for vulnerabilities like this
once a fix is available.  I don't regard this issue as particularly severe, but it is
a problem that I think should be addressed.

Could you just keep me abreast as to when you think a fix will make it in to a stable
release?

In regard to providing a preview of this research paper: I'm honestly very tempted to
post it here, but since some of the issue listed (minor UI security problems) affect
several browsers, I don't think it would be very fair to provide it only to Chrome
developers.  Since the problems aren't severe (and in fact have been pointed out
before by others), I don't think releasing it without any notice is a problem for end
users.  I do hope to have it posted on our website early next week, so I'll drop a
link here to it at that time.

Thanks again!


### er...@chromium.org (2010-01-21)

Ok, so it looks like the problem is in:

  chrome/browser/login/login_prompt.cc

76:  TabContents* parent_contents = handler_->GetTabContentsForLogin();
...
86:  MakeInputForPasswordManager(parent_contents->GetURL(), &v);


So it is using the TAB's URL as the key, rather than the resource's URL.

Inthe GetSignonRealm() function of that same file, it is using this parent URL to form 
the key. Really it should be using |auth_info.host_and_port| to get the authenticating 
domain...

### ti...@chromium.org (2010-01-21)

wtc/eroman: I'm not set up with a repro locally at this point but, do you happen to 
know the values in the AuthChallengeInfo that get presented to CreateLoginPrompt for 
the image resource in this scenario?

### ti...@chromium.org (2010-01-21)

Oh, well I think that answers my question. Looking at this now.

### er...@chromium.org (2010-01-21)

Thanks Tim (both of you!).

> do you happen to know the values in the AuthChallengeInfo that get presented to
> CreateLoginPrompt for the image resource in this scenario?

Here is the approximate callstack with relevant values:

> chrome.dll!GetSignonRealm(
        url="http://good.com/test-img.html",
        auth_info={host_and_port="evil.com:80", scheme="digest"})
  chrome.dll!LoginDialogTask::MakeInputForPasswordManager(
        origin_url="http://good.com/test-img.html", ... )
  chrome.dll!LoginDialogTask::Run()

The main thing is there is a disconnect between the origin of the challenge ("evil.com:80"), and the URL which is used for lookups 
(the tab's URL, "http://good.com/test-img.html").

### ti...@chromium.org (2010-01-21)

I'm trying to recall why the heck we special case proxy there and use host_and_port in 
that case.  I remember there being a difference, but that was 2 years ago.  Maybe the 
way the AuthChallengeInfo is supplied changed..

### ti...@chromium.org (2010-01-22)

Committed fix in http://src.chromium.org/viewvc/chrome?view=rev&revision=36829.

### ti...@chromium.org (2010-01-22)

Oh, and thanks Tim & Eric & Wan-Teh for the help!

### sc...@gmail.com (2010-01-22)

Tim - the @sentinelchicken.org one - for responsibly disclosed vulnerabilities such as 
this, we're delighted to give credit in the form of <name> of <optional affiliation>. 
Let us know what you want us to use. If you could hold off mentioning this until we 
get a patch out, it would be appreciated. I'll have on ETA on the patch early next 
week.

### 0a...@gmail.com (2010-01-22)

scarybeasts:  Yes, don't worry, I won't mention this specific issue until you have a
patch or fixed version available.  In fact, if you like, I can test a release
candidate if you want to verify it's fixed based on my test cases, though I'm sure
you've probably got it under control.  In any case, I won't release an advisory until
the day of or a few days after your fix.  I'll be traveling overseas starting in the
middle of next week, so I'll probably be too busy to write up an advisory right away
anyway. ;-)

As for credit, please associate me (Timothy D. Morgan) with "VSR
(www.vsecurity.com)".  While I've released advisories on my personal site in the
past, this work is associated with my company.  Thanks!


### sc...@gmail.com (2010-01-26)

Merged to 249 (r37073) and 249s (r37074).

### 0a...@gmail.com (2010-01-26)

Hi again,

I just published the paper I was working on when I ran across this bug.  Once again,
it doesn't include details about this specific vulnerability. See:
  http://www.vsecurity.com/download/papers/WeaningTheWebOffOfSessionCookies.pdf

However, it does include details about UI weaknesses and password manager weaknesses
that affect the top 5 browsers.  I will try to find the time over the next few days
to log separate bugs for each major item identified in Chrome.  I'll be trying to
notify all of the browser dev teams though, and I'm flying overseas in 2 days, so I'm
hellishly busy.  Feel free to log separate bugs based on this paper yourselves.

I hope you also take the time to look over the arguments for HTTP authentication and
how I propose to fix it.  In particular, I'd be interested in hearing feedback on my
proposed change to 401 response handling.  I'll be pressuring other browser vendors
to do the same.

Thanks much for the quick response to the initial vulnerability notification.
tim


### 0a...@gmail.com (2010-01-27)

BTW, any ETA on the fix for this issue?

### sc...@gmail.com (2010-01-27)

I merged the fix over to our release branch. Something like Tuesday perhaps?

### 0a...@gmail.com (2010-01-28)

Tuesday, February 2nd?  Yeah, that's perfectly fine.  I don't mean to rush you, I
just want to plan my time since I'll be overseas for the next two weeks.  I'll start
getting the advisory put together.

### sc...@gmail.com (2010-01-28)

No promises, BTW. There are various dependencies such as QA.

### er...@chromium.org (2010-02-03)

Verified on build 4.0.249.86, running on Windows Vista.

### 0a...@gmail.com (2010-02-05)

eroman: You mean the fix is verified or the bug still exists on that version?



### er...@chromium.org (2010-02-05)

> eroman: You mean the fix is verified or the bug still exists on that version?

I confirmed that it is fixed in 4.0.249.86, which is the upcoming version for the stable 
channel.

### 0a...@gmail.com (2010-02-09)

Ah, great, thanks!

BTW, I did obtain a CVE number for this issue: CVE-2010-0556

### 0a...@gmail.com (2010-02-14)

Hello again.  I see that version 4.0.249.86 has been released.  I've drafted an
advisory which is available here:
  http://www.vsecurity.com/advisory/20100215-1.txt

(It's not publicly linked to yet.)  

I plan on announcing this tomorrow afternoon (US Pacific time) unless anyone has any
objections.  Let me know if you notice any inaccuracies in the document. Thanks.

### sc...@gmail.com (2010-02-16)

[Empty comment from Monorail migration]

### sc...@gmail.com (2010-02-23)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-10-05)

Batch update.

### fr...@thefrozenfire.com (2011-12-09)

Fix may cause regression - Issue #107009

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### sc...@gmail.com (2012-10-28)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-11)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/32718?no_tracker_redirect=1

### pe...@google.com (2024-02-04)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40078529)*
