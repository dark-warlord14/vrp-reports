# On Chrome 130.0.6723.73 on Android: there is a way website A can automatically opens chrome://chrome-urls well via Redirect blocked function

| Field | Value |
|-------|-------|
| **Issue ID** | [375550814](https://issues.chromium.org/issues/375550814) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>Navigation |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | du...@gmail.com |
| **Assignee** | cr...@chromium.org |
| **Created** | 2024-10-25 |
| **Bounty** | $1,000.00 |

## Description

Security Bug

Important: Please do not change the component of this bug manually.

Please READ THIS FAQ before filing a bug: https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/faq.md

Please see the following link for instructions on filing security bugs: https://www.chromium.org/Home/chromium-security/reporting-security-bugs

Reports may be eligible for reward payments under the Chrome VRP: https://g.co/chrome/vrp

NOTE: Security bugs are normally made public once a fix has been widely deployed.

-------------------------

VULNERABILITY DETAILS
On Chrome 130.0.6723.73 on Android: there is a way website A can automatically opens chrome://chrome-urls well via Redirect blocked function.

VERSION
Chrome Version: 130.0.6723.73 + [stable]
Operating System: [Android 14]

REPRODUCTION CASE
Please include a demonstration of the security bug, such as an attached HTML or binary file that reproduces the bug when loaded in Chrome. PLEASE make the file as small as possible and remove any content not required to demonstrate the bug, or any personal or confidential information.

Please attach files directly, not in zip or other archive formats, and if you've created a demonstration site please also attach the files needed to reproduce the demonstration locally.

Open the local .html file (attached), allow in the Redirect blocked notification, the URL chrome://chrome-urls can be opened well after that from the local .html file via Redirect blocked function.

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: [tab, browser, etc.]
Crash State: [see link above: stack trace *with symbols*, registers, exception record]
Client ID (if relevant): [see link above]

CREDIT INFORMATION
Externally reported security bugs may appear in Chrome release notes. If this bug is included, how would you like to be credited?
Reporter credit: Khiem Tran

## Attachments

- [f.html](attachments/f.html) (text/html, 80 B)
- [k.html](attachments/k.html) (text/html, 69 B)
- [Screenrecorder-2024-10-25-19-09-37-151.mp4](attachments/Screenrecorder-2024-10-25-19-09-37-151.mp4) (video/mp4, 6.1 MB)

## Timeline

### du...@gmail.com (2024-10-25)

The iframe's code (attached):

<script>
 window.top.location = "chrome://chrome-urls";
</script>

The video of demonstration is attached below, too.

### ke...@chromium.org (2024-10-25)

Thanks for the report. I have confirmed this on Canary and Stable. The iframe is navigating the top-level frame to a chrome: URL. The redirect blocker is a minor mitigation but I don't believe this is supposed to be possible at all.

creis@: Can you comment and/or recommend an owner? Note that this is Android only.

### ke...@chromium.org (2024-10-25)

Assigning to creis@ which I meant to do in comment 3.

### cr...@chromium.org (2024-10-26)

Thanks for the report! I'm not sure that "automatically" is accurate, given that the user has to choose to bypass the "Redirect blocked" dialog? That seems like a pretty large mitigating factor to me.

Still, I tend to agree that we should not offer an option to follow the redirect anyway, at least for URLs that web renderer processes are not allowed to navigate to (e.g., chrome://, file://, etc). twellington@, do you know who is familiar with the "Redirect blocked" dialog on Android, and whether this can be made stricter?

In some local testing, I can confirm that the user can proceed to navigate to any chrome:// URL (e.g., also chrome://version), as well as data: URLs (which should not be allowed in the main frame). It doesn't seem to work for javascript: URLs, which is good.

My local repro steps for quickly experimenting with it:

1. Visit <http://csreis.github.io/tests/cross-site-iframe.html>
2. In the address bar, carefully type the following without hitting enter:
   `javascript:navFrame('data:text/html,<script>top.location="chrome://version";</script>');`
3. Do not press enter (which does a search), but instead choose the second suggestion in the address bar (which navigates).
4. Observe the "Redirect blocked" dialog, and that you can proceed through it.

### ke...@chromium.org (2024-10-26)

creis@: Am I right in thinking that the redirect warning is an unrelated protection which happens to be a mitigation here? My understanding is that that exists to limit iframes from navigating their ancestors, but shouldn't relate at all to whether the page can navigate to a chrome:// URL.

On desktop you still get the redirect warning, but if you allow it in this case, nothing happens because the navigation is blocked.

### cr...@chromium.org (2024-10-26)

Oh! I didn't test it on desktop, and hadn't been aware we had a redirect blocker like this. At least on ChromeOS 129.0.6668.110, the steps in comment 5 behave the same on desktop as in Android-- when I click on the "Redirect blocked" notice in the omnibox and then on the chrome://version link, it works. (Ken, do you see something different?)

That seems like something we should tighten across desktop and Android. I'm still not familiar with the redirect blocker, but after some digging I think it might be the framebusting intervention from <https://crbug.com/40534787>? After <https://chromium-review.googlesource.com/c/chromium/src/+/3733094>, at least the Android part of it might live in FramebustBlockedMessageDelegate. (I'm not sure where the desktop equivalent is.)

That code appears to unsafely call OpenURL on the blocked\_url\_, treating it as a browser-initiated navigation and thus elevating privileges so that it can navigate to chrome:// (or other off-limits) URLs:
<https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/android/framebust_intervention/framebust_blocked_delegate_android.cc;drc=0d795c6e8be398088fdd747cb4fa4b7c7e366878;l=120>

```
  GetWebContents().OpenURL(
      content::OpenURLParams(blocked_url_, content::Referrer(),
                             WindowOpenDisposition::CURRENT_TAB,
                             ui::PAGE_TRANSITION_LINK, false),
                                                       ^^^^^

```

dgn@: Are you familiar with this from <https://crbug.com/40534787>, and do you know where the desktop-equivalent code is? Could you help to update it so that we don't allow proceeding to URLs that the renderer wouldn't have been able to navigate to on its own? We can chat more about how to limit those if passing "true" for OpenURLParams's `is_renderer_initiated` isn't sufficient.

### du...@gmail.com (2024-10-26)

Sorry for disturbing with this added comment from the external reporter (me
^^):

In Chrome on Android, Chrome only allows the chrome:// URLs appearing after
the users entered the chrome:// URLs directly into the omnibox, other ways
will be blocked by Chrome.

So, seeing this behavior (mentioned in this report), I guess the allowing
opening chrome:// URLs well from websites should be had a look at.

On Sat, Oct 26, 2024, 11:14 AM <buganizer-system@google.com> wrote:

> Replying to this email means your email address will be shared with the
> team that works on this product.
> https://issues.chromium.org/issues/375550814
>
> *Changed*
> assignee:  tw...@chromium.org → dg...@chromium.org
>
> *cr...@chromium.org <cr...@chromium.org> added comment #7
> <https://issues.chromium.org/issues/375550814#comment7>:*
>
> Oh! I didn't test it on desktop, and hadn't been aware we had a redirect
> blocker like this. At least on ChromeOS 129.0.6668.110, the steps in
> comment 5 behave the same on desktop as in Android-- when I click on the
> "Redirect blocked" notice in the omnibox and then on the chrome://version
> link, it works. (Ken, do you see something different?)
>
> That seems like something we should tighten across desktop and Android.
> I'm still not familiar with the redirect blocker, but after some digging I
> think it might be the framebusting intervention from
> https://crbug.com/40534787? After
> https://chromium-review.googlesource.com/c/chromium/src/+/3733094, at
> least the Android part of it might live in FramebustBlockedMessageDelegate.
> (I'm not sure where the desktop equivalent is.)
>
> That code appears to unsafely call OpenURL on the blocked_url_, treating
> it as a browser-initiated navigation and thus elevating privileges so that
> it can navigate to chrome:// (or other off-limits) URLs:
> https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/android/framebust_intervention/framebust_blocked_delegate_android.cc;drc=0d795c6e8be398088fdd747cb4fa4b7c7e366878;l=120
>
>   GetWebContents().OpenURL(
>       content::OpenURLParams(blocked_url_, content::Referrer(),
>                              WindowOpenDisposition::CURRENT_TAB,
>                              ui::PAGE_TRANSITION_LINK, false),
>                                                        ^^^^^
>
> dgn@: Are you familiar with this from https://crbug.com/40534787, and do
> you know where the desktop-equivalent code is? Could you help to update it
> so that we don't allow proceeding to URLs that the renderer wouldn't have
> been able to navigate to on its own? We can chat more about how to limit
> those if passing "true" for OpenURLParams's is_renderer_initiated isn't
> sufficient.
>
> _______________________________
>
> *Reference Info: 375550814 On Chrome 130.0.6723.73 on Android: there is a
> way website A can automatically opens chrome://chrome-urls well via
> Redirect blocked function*
> component:  Public Trackers > 1362134 > Chromium > UI > Browser >
> Navigation <https://issues.chromium.org/components/1457065>
> status:  Assigned
> reporter:  duckhiem@gmail.com
> assignee:  dg...@chromium.org
> cc:  cr...@chromium.org, duckhiem@gmail.com, ke...@chromium.org, and 1
> more
> collaborators:  se...@chromium.org
> type:  Vulnerability
> access level:  Limited visibility
> priority:  P4
> severity:  S2
> found in:  130
> hotlist:  external_security_report
> <https://issues.chromium.org/hotlists/5433527>, Security_Impact-Extended
> <https://issues.chromium.org/hotlists/5432548>, Unconfirmed
> <https://issues.chromium.org/hotlists/5437934>
> retention:  Component default
> Component Ancestor Tags:  UI, UI>Browser, UI>Browser>Navigation
> Component Tags:  UI>Browser>Navigation
> OS:  Android
>
>
> Generated by Google IssueTracker notification system.
>
> You're receiving this email because you are subscribed to updates on
> Google IssueTracker issue 375550814
> <https://issues.chromium.org/issues/375550814> where you have the roles:
> reporter, cc
> Unsubscribe from this issue.
> <https://issues.chromium.org/issues/375550814?unsubscribe=true>
>


### pe...@google.com (2024-10-26)

Setting milestone because of s2 severity.

### pe...@google.com (2024-10-26)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### dg...@chromium.org (2024-10-28)

Sorry I don't have any context on this. I think this 2017 bug was only about some UI changes. The blocking detection logic was done in [issue 40084719](https://issues.chromium.org/issues/40084719), maybe some of the folks from that bug would know? japhet@ could you please help triaging this?

### ke...@chromium.org (2024-10-28)

For the question in comment 7:
Yes, I see different behaviour. On Windows, Mac and Linux I can allow popups and redirects, and the navigation to a chrome:// URL does not happen.

### tw...@chromium.org (2024-10-28)

cc'ing lbrady@ and shivanisha@ who's team did some work on this code a couple of years ago

### ke...@chromium.org (2024-10-28)

One more update on behaviour, because I had been a bit confused by the different UI on Android vs desktop:
- On both, when popups and redirects are always allowed for the site, then the navigation to the chrome:// URL fails.
- When there is no explicit allow or block, it prompts the user.
- On Android, selecting "Allow" causes the navigation to succeed.
- On desktop you have to click the chip in the omnibox. Clicking "always allow" does not cause the navigation to happen, but clicking on the link to the URL target does succeed.

All of which confirm's creis@'s analysis in comment 7.

### cr...@chromium.org (2024-10-28)

Thanks kenrb@! I can confirm that the bug doesn't happen if popups and redirects are allowed on the site in question (on either desktop or Android).

The bug appears specific to the use of OpenURL, which treats the URL in question as browser-initiated and allows privileged URLs. Because the URL comes from the renderer, it should be filtered first. Thanks to dgn@'s link to <https://crbug.com/40084719>, I discovered the browser-side implementation as well.

- Android: [FramebustBlockedMessageDelegate::HandleOpenLink()](https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/android/framebust_intervention/framebust_blocked_delegate_android.cc;drc=0d795c6e8be398088fdd747cb4fa4b7c7e366878;l=120)
- Desktop: [FramebustBlockTabHelper::OnBlockedUrlClicked()](https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/blocked_content/framebust_block_tab_helper.cc;drc=0d795c6e8be398088fdd747cb4fa4b7c7e366878;l=32)

It looks like I was wrong in [comment #7](https://issues.chromium.org/issues/375550814#comment7) and we can't solely set is\_renderer\_initiated to true, since that also requires setting an initiator origin. Thanks to some suggestions from nasko@ and alexmos@, the fix might involve some combination of:

- Using FilterURL on any URLs passed from the renderer. (This can probably be done quickly.)
- Preserving initiator origin (and any other relevant parameters) in the dialog, supposedly similar to what the popup blocker does, and then treating it as renderer-initiated. (This is probably worth doing, possibly as a followup.)
- Optionally preserving more of the navigation context.

I think we may have also previously discussed changing the OpenURL / LoadURL APIs so that they don't allow privileged URLs by default, although this would be a larger overhaul.

Anyway, now that I know where both the desktop and Android code live (and we've confirmed what the bug is across both platforms), I can probably help with the fix.

### cr...@chromium.org (2024-10-28)

Interestingly, there seems to be a test for this case already in [FramebustBlockBrowserTest.ModelAllowsRedirection](https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/content_settings/framebust_block_browsertest.cc;drc=73cb98534375506288904ac3eb7ab6e35e94f0e0;l=153) from <https://chromium-review.googlesource.com/c/chromium/src/+/755523>, but it verifies that you *can* click through to the chrome:// URLs. I'm guessing that was just an oversight of the risk, without realizing web renderers aren't allowed to trigger navigations to chrome:// URLs (even indirectly).

pmonette@: Can you confirm it's ok to change that test to expect that the user can't proceed to chrome:// URLs, and can only proceed to blocked URLs the renderer would have already been able to navigate to in other circumstances?

### cr...@chromium.org (2024-10-28)

I'm working on a first fix in <https://chromium-review.googlesource.com/c/chromium/src/+/5973403>, by adding FilterURL calls. It looks like that should address both the Android and desktop cases, since they both appear to go through RenderFrameHostImpl::DidBlockNavigation before reaching the respective dialogs.

There's additional cleanup we land after that, but this first CL should resolve the main security concern.

### cr...@chromium.org (2024-10-31)

[Navigation triage]

Just adding the Available hotlist to remove this from the untriaged list. The fix is just waiting for owners approval before it can land.

### ap...@google.com (2024-11-04)

Project: chromium/src  

Branch: main  

Author: Charlie Reis <[creis@chromium.org](mailto:creis@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/5973403>

Filter any URLs passed to the "redirect blocked" dialogs.

---


Expand for full commit details
```
Filter any URLs passed to the "redirect blocked" dialogs. 
 
The framebusting mitigation from https://crbug.com/40084719 can block 
subframes from navigating the main frame cross-origin without a user 
gesture. However, the dialog allows the user to manually proceed to the 
URL if desired. 
 
This URL was not adequately filtered before, allowing chrome:// and 
other privileged URLs to be used even if the renderer could not nomrally 
navigate to them.  This CL adds the necessary filtering, which should 
apply to both the desktop and Android dialogs. 
 
Bug: 375550814 
Change-Id: Icd518a869a06ad982767386d5d7a1528e6179e6c 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5973403 
Reviewed-by: Patrick Monette <pmonette@chromium.org> 
Reviewed-by: Nate Chapin <japhet@chromium.org> 
Reviewed-by: Andy Paicu <andypaicu@chromium.org> 
Reviewed-by: Liam Brady <lbrady@google.com> 
Auto-Submit: Charlie Reis <creis@chromium.org> 
Commit-Queue: Charlie Reis <creis@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1377807}

```

---

Files:

- M `chrome/browser/ui/content_settings/framebust_block_browsertest.cc`
- M `content/browser/renderer_host/render_frame_host_impl.cc`

---

Hash: 27dc50bbbf4264d20c2b42d0b2aafc9ebd63fbec  

Date:  Mon Nov 04 19:31:22 2024


---

### cr...@chromium.org (2024-11-04)

Since <https://chromium-review.googlesource.com/5973403> should resolve the security aspects of this report, I'll mark this as fixed. I've filed <https://crbug.com/377339178> to track some followup work to make similar issues less likely.

In terms of severity, I looked for examples of similar bugs that allowed navigation to chrome:// and file:// URLs. In general this type of navigation is disallowed because it can be used as a stepping stone for privilege escalation, though no direct harm is likely to happen as a result. In that sense, it's similar to <https://crbug.com/40083873>, which was considered Low (S3) (even when not requiring a user to click through a warning dialog, like this report). I'll adjust to this to S3 accordingly.

There are some other similar bugs with higher severity, but I think they had larger consequences. For example, <https://crbug.com/40092668> was Medium (S2), but it didn't require user interaction and could lead to leaking file contents via extension APIs. In another example, <https://crbug.com/40087849> was High (S1) because it allowed loading the file in the initiator's process as well, where it could be leaked. I don't think this bug has the same risks as those, but I'm happy to revise the severity if there are examples where the content might be leaked to the attacker.

### du...@gmail.com (2024-11-05)

For beloved panel people who will decide the final reward for this 2024's reported security-labelled bug ^^:

In 2015, from a .PDF file, it has a link, it links to a chrome:// link, it needs users to click on the link, and it can open the chrome:// link in a new tab after users clicked on the link on the .PDF file, the same to my report: a website opened, it opens a redirect blocked notification, users click on a click on the notification, it opens the chrome:// link well.

And the report in 2015 is rewarded 4,000 (https://issues.chromium.org/issues/40082800?pli=1).

### du...@gmail.com (2024-11-05)

And open the website and click on the notification is familiar to users than open the .PDF file and click on the link on the .PDF file, I mean in my report, the scenario is easier to happen to users.

### du...@gmail.com (2024-11-05)

At the first look, the attacker's website can only trick the users click a click on the redirect blocked notification (to allow) to quit the browser by opening the chrome://quit link.

### du...@gmail.com (2024-11-05)

From a deeper look to find a way to get user information, it

### du...@gmail.com (2024-11-05)

I've also filed https://issues.chromium.org/issues/377440449 to report the fix https://issues.chromium.org/issues/375550814#comment20 does not work on my end. Is it practicable I can file a new report for the fix's problem after the status Fixed?

### ke...@chromium.org (2024-11-05)

Re comment #25: Yes, that's fine. The current shepherd will have a look and respond on the new bug.

### cr...@chromium.org (2024-11-05)

Thanks for spotting <https://crbug.com/40082800> as another example, rated Medium (S2). It's possible the reward panel could decide this should be Medium, though I'll mention a few considerations there:

- I would say that clicking through a "Redirect Blocked" notification (which warns the user that something may be wrong) is more of a mitigation than clicking a normal link in a PDF. In the PDF case, there are no warnings to the user that something is wrong, and the chrome:// or file:// URL was opened directly.
- That bug was raised from Low to Medium when it was found it affected more cases than just the one reported ([here](https://issues.chromium.org/u/1/issues/40082800#comment16)). I'm not sure whether the raise in severity was fully justified there or not, but the broader impact did play into it.
- The reward was actually $2000, and the total amount was only $4000 because it was donated to charity and so Google [matched it](https://issues.chromium.org/u/1/issues/40082800#comment34).

Regarding <https://crbug.com/377440449>, I think you might be testing in a version that doesn't have the fix yet (currently just 132.0.6820.0 and higher)?

Regarding [comment #24](https://issues.chromium.org/issues/375550814#comment24), it sounds like you might be looking for ways to leak user information via the bug, which would be super helpful if you found something. The comment cut off at "From a deeper look to find a way to get user information, it", though. Is there any more you can share?

Thanks!

### du...@gmail.com (2024-11-06)

The Redirect blocked notification is just to tell a new tab will be opened and the notification appears just because the Redirect blocking function is turned on in Settings of the browser Chrome on Android.

Base on it, the scenario in my report is that a user is familiar with the blocking redirect function and the notification as know it is as described as above. This user easily tend to click on to allow the redirect.

But I totally agree with all the things explained in the comment #27 and hope the panel will issue the reward notification soon ^^ (shy).

The my own funny explaining in here for the maximum bounty I can have (^^) is:

Now in 2024 the chrome:// link complex is more complex than before so that there are many exploits if I can find one to prove, yeah, if there is a chrome:// link on the chrome:// link complex can do something harmful for users by just loading it successfully, yeah, it is the case that we can discuss about.

I will share details if there is one convinced and proved one can be shared ^^.





### du...@gmail.com (2024-11-08)

So the impact only is:

Trick users click allow on the redirect blocked notification on the website's content.

Trick users click to config something on the opened well chrome:// link by content on the website, too.

Or quit the browser by opening chrome://quit (needs users click to allow on the redirect blocked notification).

I hope the reward will be 500 USD or 1,000 USD ^^.



### du...@gmail.com (2024-11-09)

For comment #27 about the 2,000 USD reward for the bug https://crbug.com/40082800, I also want my report is rewarded 2,000 USD so I would compare that: 

In the .PDF file case, users can see the URL via status bar or other functions and need to click on for the URL to be opened.

In my report, the website can automatically sends the URL (this is the key part) to the redirect blocked notification to show to users, users click on because the redirect blocked notification just tells the current website is moving to this URL.

### du...@gmail.com (2024-11-09)

^^

### du...@gmail.com (2024-11-11)

In the .PDF file case at https://crbug.com/40082800, users can't see the link, and in my report, because the iframe navigates to the link, users can't know.

I will find a way to mask the link in the redirect blocked notification, if so, users can't know the link and tend to click to allow the redirect to happen.

### du...@gmail.com (2024-11-13)

Hi, I'd ask for the panel decision status for the reward ^^.

### du...@gmail.com (2024-11-13)

Thanks!

### du...@gmail.com (2024-11-14)

The key point of the security issue from what I know/understand from Google Chrome's bug bounty program's rules is that: Opening chrome:// not from users directly will end up being about:blank#blocked, so, all the reports pointed to ways to open chrome:// successfully not from users' inputs will be rewarded as security bugs' reports.

### du...@gmail.com (2024-11-14)

The 2,000 USD rewarded report: Open PDF file/website contains PDF, click a click on the link. Users can see the chrome:// link via right click/context menu which is the key point for easier to trick users unknowningly click on. But because it needs users to click on a link a link from the website, users take the risk of clicking on the links that users know it.

My report: Open website, click on the Redirect blocked notification one click to allow. Users can see the chrome;// link on the Redirect blocked notification.

### du...@gmail.com (2024-11-14)

I reported my report because it only needs users clicking on the allowing option from the redirect blocked notification which is a trusted feature of Chrome. This also easily tricks users believe to click allow (this blocking function will block for me all the URL Chrome thinks should be blocked because not from my intention because I didn't enter directly into Chrome's address bar/omibox.

And my reports also is the stating point for the security team to figure out in #comment 14 in desktop version, the Redirect blocked notification has an additional function/option allows users to click on as a link to open the chrome:// link. So I hope, personally, in this time of the world's reality (many appears, that I need enough money to buy a new phone and a new laptop to nurture the knowledge for the bounty program ^^), I will have a maximum at your convenience for the bounty reward (even it's a 500 reward, but it's a maximum bounty reward decided for the report of mine, it's fine ^^).

### sp...@google.com (2024-11-22)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
baseline quality report of web platform privilege escalation | exploitation mitigation bypass 


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-11-22)

Thank you for the report, Khiem. We appreciate your efforts and reporting this issue to us. In the future, it would much more helpful if your reports were clear and concise explanations of the security issue and impact to a user, following feedback we have conveyed in other bug reports and over email.

### du...@gmail.com (2024-11-23)

Thank you, Amy. This reward will help me have a better tool to learn more
deeply for more helpful and the important is, having valid reports security
bugs ^^, thank you, Any, thank you, again.

On Sat, Nov 23, 2024, 4:58 AM <buganizer-system@google.com> wrote:

> Replying to this email means your email address will be shared with the
> team that works on this product.
> https://issues.chromium.org/issues/375550814
>
> *Changed*
>
> *am...@chromium.org <am...@chromium.org> added comment #39
> <https://issues.chromium.org/issues/375550814#comment39>:*
>
> Thank you for the report, Khiem. We appreciate your efforts and reporting
> this issue to us. In the future, it would much more helpful if your reports
> were clear and concise explanations of the security issue and impact to a
> user, following feedback we have conveyed in other bug reports and over
> email.
>
> _______________________________
>
> *Reference Info: 375550814 On Chrome 130.0.6723.73 on Android: there is a
> way website A can automatically opens chrome://chrome-urls well via
> Redirect blocked function*
> component:  Public Trackers > 1362134 > Chromium > UI > Browser >
> Navigation <https://issues.chromium.org/components/1457065>
> status:  Fixed
> reporter:  duckhiem@gmail.com
> assignee:  cr...@chromium.org
> cc:  al...@chromium.org, an...@chromium.org, cr...@chromium.org, and 10
> more
> collaborators:  se...@chromium.org
> type:  Vulnerability
> access level:  Limited visibility
> priority:  P1
> severity:  S3
> duplicate:  377440449 <https://issues.chromium.org/issues/377440449>
> found in:  130
> hotlist:  Available <https://issues.chromium.org/hotlists/5438642>,
> external_security_report <https://issues.chromium.org/hotlists/5433527>,
> Security_Impact-Extended <https://issues.chromium.org/hotlists/5432548>
> retention:  Component default
> Component Ancestor Tags:  UI, UI>Browser, UI>Browser>Navigation
> Component Tags:  UI>Browser>Navigation
> Milestone:  131
> OS:  Android, Linux, Mac, Windows, ChromeOS
> vrp-reward:  1000
>
>
> Generated by Google IssueTracker notification system.
>
> You're receiving this email because you are subscribed to updates on
> Google IssueTracker issue 375550814
> <https://issues.chromium.org/issues/375550814> where you have the roles:
> reporter, starred, cc
> Unsubscribe from this issue.
> <https://issues.chromium.org/issues/375550814?unsubscribe=true>
>


### pe...@google.com (2025-02-11)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/375550814)*
