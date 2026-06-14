# Security: XSS in the bookmark button

| Field | Value |
|-------|-------|
| **Issue ID** | [40081929](https://issues.chromium.org/issues/40081929) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>Bookmarks |
| **CVE IDs** | CVE-2015-1264 |
| **Reporter** | fe...@chromium.org |
| **Assignee** | rf...@chromium.org |
| **Created** | 2015-04-24 |
| **Bounty** | $500.00 |

## Description

[Reported via e-mail from FB eng]

**VULNERABILITY DETAILS**

1. Go to <http://sandboxing.me/poc/0ab1dceb8c7f70ce936cdd826f9145ba4874dcb273fddf70a2e4e826cbd6eeda505a128eedf4f8c1ef9d69ad6bfe8e2f96dc5a68b676082f243e35cdc74dd236.html>
2. Open dev tools
3. Bookmark the page
4. Notice that JS executes a console.log statement

**VERSION**  

Chrome Version: 42+  

Operating System: Tested on Mac, guess it probably affects other OSes too

**REPRODUCTION CASE**  

See attached. It boils down to the meta property:

<meta property="og:description" content="&quot;&gt;&lt;img src=x onerror=console.log(&quot;hello&quot;)&gt;" />

## Attachments

- [poc.html](attachments/poc.html) (text/html, 215 B)

## Timeline

### fe...@chromium.org (2015-04-24)

This seems like a bug in that I don't think the META tag is supposed to be invoked when you add the bookmark.

I'm not sure how to actually turn it into an attack because it seems to execute in the context of the page that defined the META tag to begin with.

### ne...@meta.com (2015-04-24)

This was originally surfaced to me via Facebook's bug bounty program. The problem is that the og:description for a page can sometimes reflect user-controlled content.

The attack scenario would be similar to self-XSS, where someone browses to a page and then is asked to bookmark it, except it might be less obvious of an attack.

### fe...@chromium.org (2015-04-24)

dbeam@, are you working on bookmarks? I see a bunch of fixed bookmarks bugs in your history. :) any thoughts on this one?

### ne...@meta.com (2015-04-24)

PoC that runs an external script, hence arbitrary, unlimited JS (unclear how feasible it would be to craft this against an actual site): http://sandboxing.me/poc/7b12c469190291944d684866b1561d297c2693e3d4251a181657a533c5fed60a65a5044a4bfcaa8cf5354cd6a6c5cd447587a8e0e83352490da8728b6948c7a8.html

Maybe a red herring, but <img> appears to be the only tag I can get working here.

### db...@chromium.org (2015-04-24)

this is a stars issue.  you see my name for the old chrome://bookmarks.  that's not to say I can't help, but I don't have as much experience with this code as some other folks (cc'ing).

### da...@chromium.org (2015-04-24)

[Empty comment from Monorail migration]

### mb...@chromium.org (2015-04-24)

[Empty comment from Monorail migration]

### mb...@chromium.org (2015-04-24)

VRP note: If it ends up mattering, https://crbug.com/chromium/480954 was reported before this was opened. I duped it into this bug since there was already some activity here.

### k0...@gmail.com (2015-04-24)

Anything I can help?

### mc...@chromium.org (2015-04-24)

This code actually lives outside of Chromium, so b/20555599 for tracking internal code changes.

### mc...@chromium.org (2015-04-24)

To be clear, this is only XSS-like.  While bad and needs to be immediately fixed (this is a P0 internally), this would only execute code on the site providing the injection.  This means you can execute JS on the bad site with only the same credentials currently available on that site (i.e. there is no way to access any other site's data).

### ne...@meta.com (2015-04-24)

Yes, but if og:description is user-controlled that attack can be launched against others as well. This is closer to self-XSS than UXSS. :-)

### mc...@chromium.org (2015-04-24)

Touche! :-)

### mb...@chromium.org (2015-04-27)

[Empty comment from Monorail migration]

### rf...@chromium.org (2015-04-27)

Extension with fix is being pushed now, users should get the next version when Chrome updates the component extension (version 2.2015.427.xxxxx).

### cl...@chromium.org (2015-04-28)

[Empty comment from Monorail migration]

### ti...@google.com (2015-05-16)

[Empty comment from Monorail migration]

### ti...@google.com (2015-05-16)

[Empty comment from Monorail migration]

### ti...@google.com (2015-05-19)

Hey K0r3Ph1L - we decided to pay $500 for this report!

Someone from our payments team will be in contact within two weeks to collect your details. 

We'll credit you in our release notes as "K0r3Ph1L" - please update if you'd like to use another name. I'll also assign a CVE for this bug and provide it shortly.

@neal - do you want me to list you/FB as a co-credit? If so, let me know what name you want to use. 

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an established charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************



### ne...@meta.com (2015-05-19)

> @neal - do you want me to list you/FB as a co-credit? If so, let me know what name you want to use. 

Nope! This was surfaced to us via FB's bug bounty program, not discovered by us, so no credit is required/deserved. ;-)

### ti...@google.com (2015-05-19)

Thanks for the quick response!

### k0...@gmail.com (2015-05-19)

> Hey K0r3Ph1L - we decided to pay $500 for this report!
Someone from our payments team will be in contact within two weeks to collect your details. 

We'll credit you in our release notes as "K0r3Ph1L" - please update if you'd like to use another name. I'll also assign a CVE for this bug and provide it shortly.
 -


@tim
Thanks for the reward! I will be waiting for that, extend my thanks also to your devs/chromium project who acknowledged this bug. I'm fine with the "K0r3ph1l". I will be waiting for more updates to come with the CVE. 

btw, to 

@neal I'm the one who reported it in FB's bbp, I personally thank you for pointing out where the problem is. I'm also reading your blog and an avid follower of your blog that publishes web security issues. once again thank you so much. :))

### ti...@google.com (2015-05-28)

CVE is CVE-2015-1264 and release notes are here: http://googlechromereleases.blogspot.com/2015/05/stable-channel-update_19.html

Someone from our finance team will be in contact within two weeks to collect payment details. Please email me at timwillis@ if that doesn't happen so that I can chase.

Congrats again!

### k0...@gmail.com (2015-05-28)

CVE is CVE-2015-1264 and release notes are here: http://googlechromereleases.blogspot.com/2015/05/stable-channel-update_19.html

Someone from our finance team will be in contact within two weeks to collect payment details. Please email me at timwillis@ if that doesn't happen so that I can chase.

Congrats again!

- 
@tim
Thanks for the everything! Appreciated that. It's been almost 2weeks, but I'm still waiting for someone who will contact me. no worries!

Can I share it to public about this bug? possibly publishing it to infosec news website.


### ti...@google.com (2015-05-28)

If you don't mind waiting a few weeks until a larger percentage of users make it to M43, that would be preferred (and is the default). 

That said, if there's a presentation/something else where there's time pressure to make this issue public early, let me know.

### k0...@gmail.com (2015-05-28)

@tim
Everything is fine for now. I'll just wait an update. 

### ti...@google.com (2015-06-25)

[Empty comment from Monorail migration]

### ti...@google.com (2015-07-24)

Processing via our e-payment system can take up to two weeks, but the reward should be on its way to you. Thanks again for your help!

(Note: sorry for the delay here - it turns out in the new payment system, these payments were waiting for a second approval from me).

### k0...@gmail.com (2015-08-01)

You're welcome, No problem at all.

### cl...@chromium.org (2015-08-03)

Bulk update: removing view restriction from closed bugs.

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-28)

[Empty comment from Monorail migration]

### is...@google.com (2018-07-28)

This issue was migrated from crbug.com/chromium/481015?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/480954]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081929)*
