# Security: a@download feature can be abused to leak sensitive information from third party sites

| Field | Value |
|-------|-------|
| **Issue ID** | [40084219](https://issues.chromium.org/issues/40084219) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Downloads |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | in...@gmail.com |
| **Assignee** | jo...@chromium.org |
| **Created** | 2016-05-03 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**

The a@download attribute can be abused to make someone download sensitive content (csrf tokens, personal info) from a third party website that would appear to come from a server that serves as a proxy.

There is some user interaction involved, but nothing unrealistic: victim would have to download a file (with name and extension of choice) from a server and re-upload it somewhere else.

This happens in quite some real-life situations, for example in a PGP key generator like this one (<https://pgpkeygen.com/>): the user downloads a file and distributes it with its peers.

The issue occurs when a webpage does not throw a 404 error upon loading a non-existing resource on a page that includes sensitive information and CSRF tokens, e.g.

<https://mtouch.facebook.com/events/upcoming/result.pwn>

The page will download as result.pwn. We can hide the source by using a server-side redirect on the attackers server,.

We can also exploit the credibility of the source, e.g. when a JSON response at trustedsite.com/response.json/clickme.bat includes ||{malicious batch code}}|| - so an attacker could make the victim download and execute malicious code from a trusted site. This last issue is perhaps lower risk, but a fix would also get rid of this.

I reported this to facebook initially and they suggested contacting you.

Even though this can be prevented by websites individually, the solution isn't always feasible. Tackling this issue on a higher level would be a better solution.

IMPACT

A successful exploitation can be quite disastrous: Google maps leaks personal data such as e-mail, phone number and GPS location, Facebook leaks messages and CSRF tokens, ...

The user interaction is a mitigating factor, but is not too unrealistic. All the victim has to do is to download a file from a server and upload it to (another) server.

**VERSION**  

Chrome Version: 50.0.2661.94 m stable  

Operating System: Windows

**REPRODUCTION CASE**

I set up a PoC that'd download your Facebook data and CSRF tokens. PoC is very simple but shows a test that'd download your results as a .pwn file. You can then view the .pwn file in an online viewer, but in reality the contents of the file would be transferred to the attacker's server. This is of course just one simple scenario, there are more possibilities.

1. Download your file here (this can be done automatically)  
   
   <http://ceukelai.re/d-ownload/index.php?url=aHR0cHM6Ly9tdG91Y2guZmFjZWJvb2suY29tL2V2ZW50cy91cGNvbWluZy9yZXN1bHQucHdu>

On this page, you'll find the following piece of code:

<a href="./getresult.php?url=aHR0cHM6Ly9tdG91Y2guZmFjZWJvb2suY29tL2V2ZW50cy91cGNvbWluZy9yZXN1bHQucHdu" download="">here</a>

Which is actually

<a href="https://mtouch.facebook.com/events/upcoming/result.pwn">here</a>

2. As you can see, no references are made to facebook. The victim has no clue that in reality the contents of another website are downloaded as a filename and extension of the attackers choice - whatever suits the scenario.

FIX

Firefox refused to a@download content from third parties, IE/Edge looks at the content type. Also, I think it'd be a good idea to prevent a@downloads from following redirects.

## Timeline

### el...@chromium.org (2016-05-09)

Confirmed repro and details above. 

Chrome doesn't make it clear where the downloaded file came from; this effectively is a user-mediated cross-origin-read attack.

Mozilla directly protects against this; discussion is in https://bugzilla.mozilla.org/show_bug.cgi?id=874009 and https://bugzilla.mozilla.org/show_bug.cgi?id=676619.

Edge simply changes the file extension (to e.g. .html), which likely wasn't intended as a mitigation (and it's not very effective).

[Monorail components: UI>Browser>Downloads]

### mb...@chromium.org (2016-05-10)

[Empty comment from Monorail migration]

### mb...@chromium.org (2016-05-10)

[Empty comment from Monorail migration]

### fe...@chromium.org (2016-05-10)

nparker, are people on your team also interested in download shenanigans? 

### np...@chromium.org (2016-05-10)

This reminds me of http://crbug.com/589747 in that the user really has no insight into where downloads come from or how they were transported.  I think this is outside the scope of Safe Browsing.

### sh...@chromium.org (2016-05-11)

[Empty comment from Monorail migration]

### mb...@chromium.org (2016-05-12)

mkwst: Any idea who the right owner for this would be?

### sh...@chromium.org (2016-05-18)

mkwst: Uh oh! This issue still open and hasn't been updated in the last 15 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mk...@chromium.org (2016-05-18)

Hrm. Probably me, I guess, though I don't know who might know how many developers might be relying on the current behavior.

If Mozilla folks have gotten away with restricting `a@download` to same-origin endpoints, perhaps we could do the same. We'd need to carve out an exception for `data:` and ensure that it worked from within a sandboxed frame, which might be a little complicated, but is certainly doable.

### mm...@chromium.org (2016-05-26)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-05-26)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-01)

mkwst: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ta...@google.com (2016-07-13)

[Empty comment from Monorail migration]

### ta...@google.com (2016-07-13)

[Empty comment from Monorail migration]

### pa...@chromium.org (2016-07-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-07-21)

[Empty comment from Monorail migration]

### ra...@chromium.org (2016-08-02)

Re #9, blocking cross-origin <a download> would also mitigate against https://crbug.com/chromium/587956 which uses the same mechanism. I think it would be a good idea. Any updates on a plan?

### sh...@chromium.org (2016-09-01)

[Empty comment from Monorail migration]

### ke...@chromium.org (2016-09-28)

[Empty comment from Monorail migration]

### el...@chromium.org (2016-09-28)

https://crbug.com/chromium/651043 notes that we prevent cross-origin callers from specifying the suggested filename using the DOWNLOAD attribute:

  suggestedName = (isSameOrigin ? fastGetAttribute(downloadAttr) : nullAtom);

... but as shown in this repro, if the server fails to specify a Content-Disposition header, our GetSuggestedFilenameImpl function falls back to groveling the URL for something that looks like a filename (e.g. result.pwn is the example used here). 

If the server is willing to serve a file using attacker-controlled text after the "true" path (e.g. the "/LITERALLYANYTHINGHERE" in "https://mtouch.facebook.com/events/upcoming/LITERALLYANYTHINGHERE") then the user (this bug) or their operating system (651043) may take unsafe action.

### mk...@chromium.org (2016-09-29)

> Any updates on a plan?

I think the plan is: "This sounds like a good idea. Someone should send an intent-to-make-developers-that-rely-on-this-behavior-sad email to blink-dev@."

Raymes, are you that person? If not, I can probably ask my intern to be that person. Or find someone who's interested in an exciting 20% project.

### mm...@chromium.org (2016-10-11)

Looks like Raymes doesn't want to be that person? Mike, should we find anybody else?

### sh...@chromium.org (2016-10-13)

[Empty comment from Monorail migration]

### ra...@chromium.org (2016-11-28)

Sorry I didn't see this because I wasn't cc'd! I'm not the right person I was just posting as security sheriff previously :(

### sh...@chromium.org (2016-12-02)

[Empty comment from Monorail migration]

### in...@gmail.com (2016-12-15)

[Comment Deleted]

### np...@chromium.org (2017-01-20)

And another Security Sheriff ping.  mkwst -- do you have said intern, or 20%'er you could rope in?  Thanks

### sh...@chromium.org (2017-01-26)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-03-10)

[Empty comment from Monorail migration]

### ji...@chromium.org (2017-03-21)

Friendly ping from Security Sheriff. mkwst, any update?

### me...@chromium.org (2017-04-19)

Since Firefox already blocks cross origin <a download> tags, I assume there wouldn't be a strong opposition to an intent to deprecate them. Does anyone volunteer to send that I2D?

### mk...@chromium.org (2017-04-20)

Sorry! I support the limitation to same-origin endpoints, but I have no bandwidth to poke at this. Removing myself, marking as available.

### sh...@chromium.org (2017-04-20)

[Empty comment from Monorail migration]

### jo...@chromium.org (2017-04-22)

[Empty comment from Monorail migration]

### jo...@chromium.org (2017-04-22)

OWP launch https://crbug.com/chromium/714373

### jo...@chromium.org (2017-05-20)

should we outright block downloads, or just mark them as dangerous?

and if we mark them as dangerous, should we mark them as "maybe dangerous content" or introduce a new danger type?

### dt...@chromium.org (2017-05-23)

+dahlke@.  I'm personally fine with blocking these.  Do we have any idea with how often this happens or if it's a relatively common site behavior?

### jo...@chromium.org (2017-05-23)

I don't know how common that is. Maybe we should for M60 as DOWNLOAD_DANGER_TYPE_DANGEROUS_FILE and add UMA for this, and then decide what to do?

### dt...@chromium.org (2017-05-23)

That sounds good to me as well :).

### da...@chromium.org (2017-05-23)

We are looking into requiring a user prompt (similar to pop up blocking and cross-origin navigations) prior to downloading from a cross-origin frame (downloading would be blocked entirely from sandboxed iframes). Would that meet the need here or do we need to be more restrictive?

### bu...@chromium.org (2017-05-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/99a1d0db25c2b77ad42d216b2289e0bf67c69540

commit 99a1d0db25c2b77ad42d216b2289e0bf67c69540
Author: Jochen Eisinger <jochen@chromium.org>
Date: Fri May 26 14:16:45 2017

cross origin downloads w/o content disposition are dangerous

BUG=714373,608669
R=dtrainor@chromium.org

Change-Id: I170ad3a3bec4afe64897a16c98c25e8a152c15ed
Reviewed-on: https://chromium-review.googlesource.com/513923
Commit-Queue: Jochen Eisinger <jochen@chromium.org>
Reviewed-by: David Trainor <dtrainor@chromium.org>
Cr-Commit-Position: refs/heads/master@{#475000}
[modify] https://crrev.com/99a1d0db25c2b77ad42d216b2289e0bf67c69540/chrome/browser/download/download_browsertest.cc
[modify] https://crrev.com/99a1d0db25c2b77ad42d216b2289e0bf67c69540/chrome/browser/download/download_browsertest.h
[modify] https://crrev.com/99a1d0db25c2b77ad42d216b2289e0bf67c69540/chrome/browser/extensions/api/web_navigation/web_navigation_apitest.cc
[modify] https://crrev.com/99a1d0db25c2b77ad42d216b2289e0bf67c69540/chrome/browser/loader/chrome_resource_dispatcher_host_delegate_browsertest.cc
[modify] https://crrev.com/99a1d0db25c2b77ad42d216b2289e0bf67c69540/content/browser/download/download_browsertest.cc
[modify] https://crrev.com/99a1d0db25c2b77ad42d216b2289e0bf67c69540/content/browser/download/download_create_info.h
[modify] https://crrev.com/99a1d0db25c2b77ad42d216b2289e0bf67c69540/content/browser/download/download_item_impl.cc
[modify] https://crrev.com/99a1d0db25c2b77ad42d216b2289e0bf67c69540/content/browser/download/download_item_impl.h
[modify] https://crrev.com/99a1d0db25c2b77ad42d216b2289e0bf67c69540/content/browser/download/download_item_impl_unittest.cc
[modify] https://crrev.com/99a1d0db25c2b77ad42d216b2289e0bf67c69540/content/browser/download/download_request_core.cc
[modify] https://crrev.com/99a1d0db25c2b77ad42d216b2289e0bf67c69540/content/browser/download/download_stats.h
[modify] https://crrev.com/99a1d0db25c2b77ad42d216b2289e0bf67c69540/tools/metrics/histograms/enums.xml


### jo...@chromium.org (2017-05-26)

I'd argue that we shouldn't merge this back, but rather have it roll to stable in the regular way, as this might break CDNs that don't correctly send the content disposition header.

### sh...@chromium.org (2017-05-27)

[Empty comment from Monorail migration]

### jo...@chromium.org (2017-05-30)

that appears to break too much :/

### jo...@chromium.org (2017-07-31)

[Empty comment from Monorail migration]

### as...@chromium.org (2017-09-08)

The commit in https://crbug.com/chromium/608669#c41 was reverted on May 30. jochen@ what are the next steps needed for this bug?

### jo...@chromium.org (2017-09-11)

Still trying to figure out a way to implement this w/o breaking the web. The reason for the revert was that we ended up blocking about 5% of the downloads which is way more than what was expected.

### jo...@chromium.org (2017-10-25)

bumping up (even though I'm not sure we'll get that in M64 either)

### mm...@chromium.org (2017-11-15)

Another ping in case anyone got an idea on how to avoid breaking the web.

### jo...@chromium.org (2017-11-15)

i have a wip CL to implement Firefox' navigation behavior, however, that won't land before the non-PlzNavigate code is gone.

### pa...@chromium.org (2017-12-04)

Calling it Started based on #50. :)

### jo...@chromium.org (2018-01-02)

looks like we'll actually make m65

### jo...@chromium.org (2018-01-15)

landed as https://chromium.googlesource.com/chromium/src/+/2a6afcb26ba6cd2324ddaa366b11968237e304a3

### mm...@chromium.org (2018-01-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-01-22)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-01-22)

Thanks for the report, the VRP panel decided to award $500 for this. By the way, how would you like to be credited in your release notes?

### aw...@chromium.org (2018-01-22)

[Empty comment from Monorail migration]

### in...@gmail.com (2018-01-22)

Hi, thank you for the reward. You can credit me as Inti De Ceukelaire, if we can add a URL: intigriti.com



### aw...@google.com (2018-01-22)

Thanks, we will credit you as: Inti De Ceukelaire (intigriti.com)

### sh...@chromium.org (2018-02-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-02-09)

This bug requires manual review: M65 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), bhthompson@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2018-02-09)

[Bulk Edit]

+awhalley@ (Security TPM) for M65 merge review

### aw...@google.com (2018-02-09)

Already in 65

### aw...@chromium.org (2018-03-06)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-03-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-04-23)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### aw...@google.com (2018-11-14)

[Empty comment from Monorail migration]

### is...@google.com (2018-11-14)

This issue was migrated from crbug.com/chromium/608669?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/651043]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084219)*
