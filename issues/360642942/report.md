# Multiple Vulnerability Address Bar Spoofing to XSS via Recent Search

| Field | Value |
|-------|-------|
| **Issue ID** | [360642942](https://issues.chromium.org/issues/360642942) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Omnibox |
| **Platforms** | Android |
| **Reporter** | gh...@gmail.com |
| **Assignee** | ga...@chromium.org |
| **Created** | 2024-08-18 |
| **Bounty** | $1,000.00 |

## Description

Security Bug

Important: Please do not change the component of this bug manually.

Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/faq.md>

Please see the following link for instructions on filing security bugs: <https://www.chromium.org/Home/chromium-security/reporting-security-bugs>

Reports may be eligible for reward payments under the Chrome VRP: <https://g.co/chrome/vrp>

NOTE: Security bugs are normally made public once a fix has been widely deployed.

---

## VULNERABILITY DETAILS

SOP Bypass leads to Address Bar Spoofing chained to Universal XSS found in the Address bar in Recent Search via search terms (keywords),

This results in all domains opened by the victim being able to trigger XSS, including sites that are used as payload to inject search terms (keywords) which produce Recent Searches, namely Search Engine and other sites that provide search terms (keywords) as titles.

the reason is that search keywords are also displayed in the tab title, likewise if the user only enters a search term, then selecting Recent Search will only display this search term, instead of displaying the full URL

Supposedly Javascript should not be executed when the browser checks the schema and cancels it, aka the Browser should not navigate to it directly but do a search for the term, which is shown in the video I attached in the PoC

## VERSION

Chrome Version: [127.0.6533.103] + [stable]
Operating System: [Android , 13, TECNO KJ6 Build/TP1A.220624.014]

## REPRODUCTION CASE

### Address Bar Spoofing :

- Send Url to Victim

```
https://www.google.com/search?q=evil.com
https://www.google.com/search?q=https://evil.com

```

**Notes :**
When the victim opens the URL above, this search term is saved in Recent Search on the victim's browser. when the victim is in the domain , example: facebook.com

- the victim opens a Recent Search sent by the attacker previously
- The victim was successfully spoofed to the attacker's site/malicious site

### Universal XSS

- Send this Url to Victim

```
https://www.google.com/search?q=javascript%3Aalert%28document.domain%29
https://www.google.com/search?q=javascript%3Aalert%28document.cookie%29

```

**Notes :**
When the victim opens the URL above, this search term is saved in Recent Search on the victim's browser. when the victim is in the domain, example: youtube.com

- the victim opens a Recent Search sent by the attacker previously
- XSS is triggered in any domain the victim opens, **Example:** youtube.com

### Expected results:

URLs with javascript schema: should not be executed.

Browsers should not be allowed to return search terms in the address bar via Recent Search from https -> javascript.

Please note, at this time apart from the location header, I have not tested whether this pattern can be used to load resources in a way that bypasses the SOP. Let me know if you have that information after reproducing this, I'd really like to learn it

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: [tab, browser, etc.]
Crash State: [see link above: stack trace *with symbols*, registers, exception record]
Client ID (if relevant): [see link above]

Reporter credit: Muhammad Zaid Ghifari

## Attachments

- [Universal XSS.mp4](attachments/Universal XSS.mp4) (video/mp4, 16.5 MB)
- [Universal XSS.jpg](attachments/Universal XSS.jpg) (image/jpeg, 359.9 KB)
- [Address Bar Spoof.jpg](attachments/Address Bar Spoof.jpg) (image/jpeg, 335.3 KB)
- [Address Bar Spoof.mp4](attachments/Address Bar Spoof.mp4) (video/mp4, 19.8 MB)
- [Address Bar Spoof 2.jpg](attachments/Address Bar Spoof 2.jpg) (image/jpeg, 338.4 KB)
- [Universal XSS on Google Chrome via Recent Search(2).mp4](attachments/Universal XSS on Google Chrome via Recent Search(2).mp4) (video/mp4, 11.3 MB)
- [Universal XSS on Google Chrome via Recent Search.mp4](attachments/Universal XSS on Google Chrome via Recent Search.mp4) (video/mp4, 17.2 MB)
- [Microsoft Edge.mp4](attachments/Microsoft Edge.mp4) (video/mp4, 17.0 MB)
- [Firefox PoC.mp4](attachments/Firefox PoC.mp4) (video/mp4, 16.5 MB)
- [Opera Browser PoC.mp4](attachments/Opera Browser PoC.mp4) (video/mp4, 12.0 MB)
- Vid 1.mp4 (video/mp4, 7.0 MB)
- Vid 2.mp4 (video/mp4, 11.5 MB)
- Fix By Edge Mobile.mp4 (video/mp4, 30.1 MB)
- Screenshot_2024-08-27-06-22-29-93_40deb401b9ffe8e1df2f1cc5ba480b12.jpg (image/jpeg, 749.4 KB)
- PoC Chrome.mp4 (video/mp4, 17.5 MB)
- VID-20240830-WA0016.mp4 (video/mp4, 7.9 MB)
- WhatsApp Image 2024-09-05 at 02.43.31.jpeg (image/jpeg, 51.9 KB)
- [WhatsApp Image 2024-09-05 at 02.39.30.jpeg](attachments/WhatsApp Image 2024-09-05 at 02.39.30.jpeg) (image/jpeg, 72.9 KB)
- [WhatsApp Image 2024-09-05 at 02.39.29.jpeg](attachments/WhatsApp Image 2024-09-05 at 02.39.29.jpeg) (image/jpeg, 76.1 KB)
- [IOS UXSS.mp4](attachments/IOS UXSS.mp4) (video/mp4, 9.1 MB)
- [Screenshot 2024-09-13 080747.png](attachments/Screenshot 2024-09-13 080747.png) (image/png, 32.8 KB)
- [Screenshot (392).png](attachments/Screenshot (392).png) (image/png, 235.3 KB)

## Timeline

### gh...@gmail.com (2024-08-18)

## Address Bar Spoofing PoC :

[image:https://issues.chromium.org/action/issues/360642942/attachments/58740888?download=false]
[image:https://issues.chromium.org/action/issues/360642942/attachments/58740890?download=false]
[image:https://issues.chromium.org/action/issues/360642942/attachments/58740889?download=true]

## Universal XSS PoC :

[image:https://issues.chromium.org/action/issues/360642942/attachments/58740887?download=false]
[image:https://issues.chromium.org/action/issues/360642942/attachments/58740886?download=true]

### xi...@chromium.org (2024-08-19)

Thanks for the report. This report is similar to <https://crbug.com/360044702>, but with a different attack surface. I suspect both issues are caused by the same underlying code. +ender, could you take a look at this bug too? Thanks!

### pe...@google.com (2024-08-19)

Setting Priority to P2 to match Severity s3. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### gh...@gmail.com (2024-08-19)

thanks for the reply

> This report is similar to <https://crbug.com/360044702>, but with a different attack surface. I suspect both issues are caused by the same underlying code.

I don't know about that, but in the Via Recent Search attack in this report. I managed to reproduce Universal XSS on a large scale across all domains. This is different from <https://crbug.com/360044702> which can only attack the default search engine

### gh...@gmail.com (2024-08-19)

Hi team, I would like to provide additional information that this vulnerability also affects the Apple IOS operating system
PoC is attached below

### en...@google.com (2024-08-19)

sending back to security team.

i can look at this but it is unclear to me what is expected of this. this is a search suggestion coming from Google. Refinement works exactly the same way on all platforms.

"found-in" milestone may be incorrect. this is pretty much how it worked from the day refinements were introduced on any of our supported platforms. is this about detection?

### xi...@chromium.org (2024-08-20)

I guess the expectation is that if the suggestion is a search suggestion from Google, when clicking on it, it should be opened in the search engine. From the recording, Chrome seemed to remove the https part and leave the javascript: part, which causes a script to run instead. Would that make sense?

Re "found-in": We only track issue back to the current extended Stable milestone, so Found-In=126 just means the issue has been introduced for a long time.

### gh...@gmail.com (2024-08-20)

> this is a search suggestion coming from Google. Refinement works exactly the same way on all platforms.

Hi team,

I will answer this statement, due to the fact that almost all browsers other than Chromium base do not work in the same way as Chrome behaves
, Even though search suggestions from Google's Search Engine work on all platforms, other browsers don't treat things the same as Chrome.

Search suggestions taken from the Chrome browser return search terms in the address bar, instead of returning the full URL

Look at the video I attached below. I have tested Firefox, Edge and Opera Android Browsers

Similar vulnerabilities were not found there.

### gh...@gmail.com (2024-08-20)

Also, this vulnerability can not only be reproduced via search suggestions from Search Engine Google, but can be reproduced via search suggestions from Search Engine Bing, DuckDuckgo etc.

### en...@google.com (2024-08-21)

I don't think this is quite right. I think the confusion is with "what a Refine button does", or "what the *Refine action* means".

A refine button is not synonymous to "Search". Refine simply takes a Query from the Suggestion and pastes it Verbatim in the Omnibox, appending it with a space (permitting the user to continue typing right after that query, or, in exact terms, "Refine that query").
The synonym on Desktop is:

1. highlight suggestion
2. deselect text
3. add space at the end

there is no "search match" associated with this, because a Refinement starts a new query. A "Refine" quite literally means that by its term: "Refine Query".
Upon refine, the suggestion used as a source of the query is neither shown nor valid. the refined user input is now considered a brand new input, and the suggestions reflect it. the new input is evaluated to be a valid URL and is opened as such.

So if we consider this a vulnerability, then this is a vulnerability as well:

[image:http://screen/7BogocLfcuuPhTj.png]

Capturing mobile for comparison:

[image:http://screen/58kC4u2huNrFrAx.png]

### gh...@gmail.com (2024-08-21)

> Synonyms on Desktop are:

> 1. highlight suggestions
> 2. deselect text
> 3. add a space at the end

I have to correct the steps

The correct steps for the above are like this:

1. Click the address bar
2. highlight the suggestion (press down arrow)
3. deselect text
4. add a space at the end

[image:https://issues.chromium.org/action/issues/360642942/attachments/58797087?download=true]

in the case of Chrome Desktop, this takes a lot of interaction, it's the same as sticking javascript:alert() in the address bar.

Unlike the case with Chrome Android and iOS, you don't need to add a space at the end. when you click on the "Arrow icon" in Recent Search then XSS is executed.

I also suggest a fix by following Chrome Desktop Behavior.
I have tested this on several desktop browsers, the desktop browser returns "Query" and when the user clicks "Enter / Browse" then it will return again to the URL.

I attached proof for Chrome.

[image:https://issues.chromium.org/action/issues/360642942/attachments/58813656?download=true]

### en...@google.com (2024-08-21)

the reason desktop doesn't have an explicit "refine" button is because typing with physical keyboard is most of the time faster than aligning pointer against a *very wide* and *very narrow* field to click a button whose related content is on the far side of the screen - ergo impractical (read about [Fitt's law](https://www.nngroup.com/articles/fitts-law/) for more information on that topic - the target height is small enough that moving cursor accurately takes longer time than typing the query from start.. and then there's the process we discussed earlier - highlight suggestion and clear focus to refine).

meanwhile, typing on mobile devices is considered high friction, and the objective of the refine button (and pencil button, brought up in another bug) is to simply take a previously entered query back to the omnibox to give you (the user) the chance to make things right.

there are cases (no joke) where typing URL initiates navigation to search results page. this unfortunately happens on all platforms, including mobile. refine and edit buttons have shown benefit significant enough to warrant a default behavior, and we are discussing here a course of action that will likely undo this for all users (because typing `:`, `/` and other special characters is particularly cumbersome on mobile devices, and for every character added, 3 will have to be removed first)

### gh...@gmail.com (2024-08-22)

Just want to ask a little, why not treat it as implemented by the 3 browsers below?

[image:https://issues.chromium.org/action/issues/360642942/attachments/58763952?download=true]
[image:https://issues.chromium.org/action/issues/360642942/attachments/58766659?download=true]
[image:https://issues.chromium.org/action/issues/360642942/attachments/58766660?download=true]

### gh...@gmail.com (2024-08-22)

By the way, can you add IOS to the OS scope? because I have shown that this vulnerability is confirmed to impact the IOS operating system

### en...@google.com (2024-08-22)

- video #1 shows a "refinement" where you are unable to access a query. instead, you are accessing the search url, something that 99% of people don't know or want to refine manually (and subsequently click "clear omnibox" right after). this essentially shows that "refine" in that context is, at best, a mistake. the only reason anyone would want to do this is if they wanted to copy or share the url right after - and we do have two dedicated buttons for that already. IOW the value of this kind of refinement was none.
- video #3 shows something that does make a lot of sense: *strip javascript: scheme and stop supporting javascript in omnibox*. this resonates with me a lot! but to do that i need a signoff from the security team (that's why this is bounced back to them). there may be a situation where javascript: in mobile omnibox is actually needed - they would know. iow - this is not my decision to make :)

ps. sadly buganizer shows links to downloads as broken, possibly as an easy solution to possible security issue (access is set to 'limited visibility'); we can't use them (i'm guessing you may not be able to do that either, but not sure)... if that's no trouble, can you offer links to comments with specific attachments in the future? this would make it a lot easier to find these downloads. thank you!

### gh...@gmail.com (2024-08-22)

Thank you for the reply.

sorry about that, the video I meant was video [comment #9](https://issues.chromium.org/issues/360642942#comment9)
<https://issues.chromium.org/issues/360642942#comment9>

### en...@google.com (2024-08-22)

so circling back to [comment#16](https://issues.chromium.org/issues/360642942#comment16) - question to security team:

Would it be reasonable for us to either strip `javascript:` prefix or break it so that it's no longer a valid URL?

i imagine this could break a few tests internally, e.g. Toolbar color tests, that inject HTML via the means of inline javascript.

if this is not an acceptable solution, please advise how you see this resolved. as is, the vulnerability mentioned here revolves around the fact that "refine" is a "whole new user input based on a formerly executed query" and unlike suggested in previous reply, it does not have a corresponding search suggestion.

if the intention is to retain the `javascript:` scheme support, another thing we could do is alter the default behavior for non-http/https looking schemes so that these do not by default resolve as URLs (i.e. the default behavior for `javascript:` and other similar URLs would be to *search*, but an option to run them would still be accessible from the suggestions list)

### xi...@chromium.org (2024-08-22)

Thanks for sharing the extra details. Would it be feasible/reasonable to avoid showing the query in the suggestion if the query is based on the history of a renderer initiated navigation? I think the level of trust of the query is different between a user typing "javascript:alert" directly in the URL bar vs. opening a link "<https://www.google.com/search?q=javascript%3Aalert>" on a website. In the former case, it is ok to show the script again in the suggestion options. But the latter case is more dangerous because the query can come from any random website.

### en...@google.com (2024-08-23)

> Would it be feasible/reasonable to avoid showing the query in the suggestion if the query is based on the history of a renderer initiated navigation?

refinement is considered a new user input, not a previous query. we have nearly no way of knowing where it came from unless we start recording every single suggestion shown to the user for the entire duraton of the omnibox interaction - this will be both very slow and memory consuming.

> I think the level of trust of the query is different between a user typing "javascript:alert" ...

this is pretty much what refinement is: it's a "new user input", even if based on a previous query. so circling back to the previous statement, the only way to make this proposal safe is if we begin monitoring everything that happened from the moment the refinement is made, otherwise user pressing ^H to remove trailing space would again resolve the `javascript:` as an URL.

Autocomplete subsystem doesn't take "hints" about "what we think the input is" -- instead, it tells us what the input is. `javascript:` looks like a URL to Autocomplete subsystem. The UI simply renders it the way Autocomplete suggests to resolve it. the UI doesn't process the inputs in any way - it's just "the UI".

there are theoretically ways we could forcibly reject all URLs upon query refinement, but i can't really see an elegant way to make it friction-less, e.g.

- say the user refined `javascript:alert()`
- we block the URLs for.. how long? remainder of the omnibox interaction?
  - if we do that, what if the user wants actually to open, say, mdn page for `alert`? we'll never show the url
  - if we don't do that, what if the user cuts + pastes that query into the omnibox? do we change how we behave? or: at what point do we change what suggestions do we show?

i hear your argument that the query can come from any random website, that's a fair observation!

1. i would prefer to keep the UI focus on drawing rectangles and text alone - UI should not decide how to process data
2. i hear there is a legitimate problem with the `javascript:` refinement or editing, because of how it is processed *by default*
3. i question the value of `javascript:` in mobile omnibox, especially its default open behavior which appears to be the problem
4. if we have the reason to keep `javascript:` in mobile omnibox, i *think* we should demote it, so that it requires an explicit user action to invoke - not just when the user refines `javascript:` query, but also when they type it in the omnibox in the first place.

in other words, i think the most reasonable solution may be changing the behavior for non-http/https/chrome/about schemes (such as `content:`, `data:`, `javascript:`, ...) so that these are never resolved by opening them by default (not on mobile devices anyway). this way, pressing "enter" would initiate search, but the ability to open/execute a URL would still be there, just not as a default action (= requires explicit user intent).

[image:http://screen/64S7FUTWQPjQKBC.png]

### ct...@chromium.org (2024-08-26)

It does seem unexpected to me that a previous search could then be repurposed as a URL navigation, regardless of scheme, but the javascript: case is particularly risky (the other cases are just "you got redirected to a random URL" which can feel bad but our top-level security goal is to make it safe for users to click on links). This feels like a sort of type-confusion between "search query" and "URL", where we dynamically guess the type based on the textual contents of what was previously a query, instead of having the user refine the query URL.

The distinction with copy+paste into the Omnibox is a matter of automation to me -- the refinement case is the browser doing this automatically for the user. Is this a huge difference versus the possibility of social-engineering the user to copy a javascript: URL and paste it into the Omnibox themselves? Maybe not, although I think the Omnibox refinement case makes it a lot easier to get opportunistic accidental XSS on other pages (versus convincing the user to copy the URL, go to a different page, then paste).

I don't think we can just block javascript: navigations (bookmarklet support has been enough that we have a specific callout in our Security FAQ [1](https://chromium.googlesource.com/chromium/src/+/main/docs/security/faq.md#Does-executing-JavaScript-from-a-bookmark-or-the-Home-button-mean-there_s-an-XSS-vulnerability)) even if it would be a security positive change.

The idea of adding an explicit user action to invoke javascript: URLs actually sounds like a nice balance here (ideally if we can distinguish bookmark initiated navs separately, maybe via the page transition type?).

### gh...@gmail.com (2024-08-26)

I have provided suggestions in the report <https://issues.chromium.org/issues/360044702> I think the suggestions make more sense, please see the attachment below :

## Steps when Edge Mobile is still vulnerable (before fixing):

the victim opens this url: <https://www.google.com/search?q=javascript%3Aalert%28document.cookie%29&client=ms-android-oppo-rvo2&sca_esv=458fc5d25ecd7a59&sxsrf=ADLYWILWDpWuwhrhq0AqAS-yUpHVERI44A%3A1720836628300&ei=FOKRZoS> BEpeM4-EP3t2oqAk&oq=javascript%3Aalert%28document . cookie%29&gs\_lp=EhNtb2JpbGUtZ3dzLXdpei1zZXJwIiFqYXZhc2NyaXB0OmFsZXJ0KGRvY3VtZW50LmRvbWFpbilI8g1Q2gtY2gtwAXgBkAEAmAF-oAF-qgEDMC4xuAEDyAEA-AEBmAIBoAIZw gIKEAAYsAMY1gQYR5gDAIgGAZAGCJIHATGgBy0&sclient=mobile-gws-wiz-serp#sbfbu=1&pi=javascript:alert%28document.cookie%29

- the victim clicks on the address bar, then enter
- XSS triggered

## Steps when Edge Mobile has done a Fix (on the current Edge version):

the victim opens this url: <https://www.google.com/search?q=javascript%3Aalert%28document.cookie%29&client=ms-android-oppo-rvo2&sca_esv=458fc5d25ecd7a59&sxsrf=ADLYWILWDpWuwhrhq0AqAS-yUpHVERI44A%3A1720836628300&ei=FOKRZoS> BEpeM4-EP3t2oqAk&oq=javascript%3Aalert%28document . cookie%29&gs\_lp=EhNtb2JpbGUtZ3dzLXdpei1zZXJwIiFqYXZhc2NyaXB0OmFsZXJ0KGRvY3VtZW50LmRvbWFpbilI8g1Q2gtY2gtwAXgBkAEAmAF-oAF-qgEDMC4xuAEDyAEA-AEBmAIBoAIZw gIKEAAYsAMY1gQYR5gDAIgGAZAGCJIHATGgBy0&sclient=mobile-gws-wiz-serp#sbfbu=1&pi=javascript:alert%28document.cookie%29

the victim clicks on the address bar, then enter

-XSS is no longer triggered

-For Xss to be triggered add (any text or space)

-then enter

-XSS will be triggered

-in the step after this fix XSS is no longer a threat, because users consciously add words or spaces after "javascript:alert()" in the address bar

Example :

javascript:alert();x

which means the steps the user takes are the same as pasting "javascript:alert()" there

Actually, this is a pretty good suggestion for a report <https://issues.chromium.org/issues/360044702>, but if someone wants to apply something similar to this report, maybe this could be the best reference.

### gh...@gmail.com (2024-08-26)

by the way, can the severity be increased to `S1`?, considering this impact is Universal XSS

### en...@google.com (2024-08-26)

> It does seem unexpected to me that a previous search could then be repurposed as a URL navigation

it is not a "reused search". refinement process starts a whole new user input. that is how it always worked, and that's the idea behind it. we don't keep track of "how we ended up with the current user input", because it is simply too expensive and unclear how to make it "right" (see [comment#20](https://issues.chromium.org/issues/360642942#comment20)).

one clear example of where i use it frequently is when a URL linked to page with localized domain (e.g "interia.pl", "wp.pl", "paypal.pl") or an internal url ("go/X", "who/X") is opened as a search (which happens frequently enough to be a problem). typing on mobile keyboards is not exactly as convenient as typing on physical keyboards, so i think this is still a valid case to be recognized.

> This feels like a sort of type-confusion between "search query" and "URL" where we dynamically guess the type based on the textual contents of what was previously a query, instead of having the user refine the query URL.

not quite. what we're debating here is a suggestion that a "search query based input should be resolved as a search query" -- so, for a sake of presentation, looking at the examples above, "interia.pl" should be resolved as a search, because "interia" is a search. refinement is not a complex process. it allows users to formulate a new input based on something they typed in the past. it's not anchored to anything, because tracking all possible ways of formulating the input (paste via menu, paste via keyboard, keyboard autocomplete, keyboard autocorrect, clear and start over, select all and type over, ...) is just too complicated for a basic feature whose simple purpose is to allow the user to take what they typed in the past and make changes.

In simple terms: i disagree that this scenario should open a search results page:

[image:http://screen/5kbFF4MiiCx9JLK.png]

> I don't think we can just block javascript: navigations

Agreed. I think this should still be accessible

> The idea of adding an explicit user action to invoke javascript: URLs actually sounds like a nice balance here

Do i have your blessing to proceed with this, then?

[image:http://screen/64S7FUTWQPjQKBC.png]

### xi...@chromium.org (2024-08-26)

Thanks everyone for the input. It seems that we have reached an agreement on the mitigation (adding an explicit user action to invoke javascript: URL).

Regarding the severity, I can't find a clear criteria on <https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md> or a precedent bug that looks similar. I need to consult other security members.

### xi...@chromium.org (2024-08-26)

Discussed with the rest of the team and we agreed that the severity should be S2. Although there are multiple mitigations to avoid the UXSS, the consequence is higher than a normal S3 bug.

### gh...@gmail.com (2024-08-26)

Isn't Universal Xss already listed on the High Severity (S1) list?

### xi...@chromium.org (2024-08-26)

It requires additional user interactions and it is potentially hard to trick the user into doing it so the attacker would only get opportunistic success without much control over target origin, so the severity is dropped down by a level.

### en...@google.com (2024-08-27)

[crrev/c/5814284](https://crrev.com/c/5814284) is in CQ. it addresses problems on Android. I pinged Stepan, iOS Chrome Search TL, to help with necessary adjustments needed to adopt the change on iOS. The problem is that there's a ton of tests that rely on `javascript:` or `data:` URLs to simulate dark mode (by injecting html or javascript content and theming the Toolbar).

### ap...@google.com (2024-08-27)

Project: chromium/src
Branch: main

commit 04938340e1a93e5e5588badd5e01600dd3356d52
Author: Tomasz Wiszkowski <ender@google.com>
Date:   Tue Aug 27 00:55:43 2024

    Disallow VerbatimMatches to open non-navigable URLs by default.
    
    This change prevents non-navigable URLs from being opened upon paste,
    refine, autocomplete etc., effectively disallowing accidental execution
    of inline javascript: blocks.
    
    The non-navigable (e.g. executable) URIs will be effectively pushed
    down on the suggestions list, making them still available, but
    moving forward these will require an explicit user action to be
    invoked (i.e. the user now has to intentionally tap these suggestions
    to initiate the corresponding action).
    
    The change removes redundant test that relies on inline page
    injection. This is already covered by another test:
    http://shortn/_NG1M484b41
    
    Bug: b/360642942
    Change-Id: I47abb15e38272355664ac8e2714b04a8dbef11e2
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5814284
    Reviewed-by: Gang Wu <gangwu@chromium.org>
    Commit-Queue: Tomasz Wiszkowski <ender@google.com>
    Cr-Commit-Position: refs/heads/main@{#1347092}

M       chrome/android/javatests/src/org/chromium/chrome/browser/omnibox/UrlBarTest.java
M       components/omnibox/browser/verbatim_match.cc

https://chromium-review.googlesource.com/5814284


### pe...@google.com (2024-08-27)

Setting milestone because of s2 severity.

### en...@google.com (2024-08-27)

Passing this to Stepan. Android portion is addressed, and iOS portion can also be addressed by extending change mentioned in [comment#30](https://issues.chromium.org/issues/360642942#comment30) to include iOS.

i did not do that because i have seen some test failures on iOS linked to theming. on android this was caused by tests injecting html code via `data:` url, i am assuming the same may be true on iOS, but it's also quite possible it was just flakes i ran into.

### gh...@gmail.com (2024-08-27)

Hi team, I would like to provide additional information. that I managed to bypass isolation for reading local files in the browser via this vulnerability.

Steps:

1.) Go to <https://www.google.com/search?q=javascript:window.open%28%27file:///sdcard/%27%29>

2.) open
<https://www.google.com/search?q=view-source:file:///sdcard/> then click the pencil icon and enter

3.) The url bar will look like this
view-source:file:///sdcard/

4.) type j and select search suggestions (recent search) in step 1, then click

5.) Successfully bypass isolation and read local file

PoC : see the video I attached

Currently I am still looking for other points for this attack, if I find them I will notify you as soon as possible

### ap...@google.com (2024-08-27)

Project: chromium/src
Branch: main

commit 1cf57b53c2e9bbae9896025d69bd9e7db43b5a3f
Author: Tomasz Wiszkowski <ender@google.com>
Date:   Tue Aug 27 21:46:13 2024

    Disallow VerbatimMatch to open non-navigable URLs on iOS by default.
    
    This change expands the scope of http://crrev/c/5814284 to include
    the iOS platform. iOS was initially omitted due to intermittent test
    failures, that previously seemed to be possibly related to the fix.
    
    Since these issues have cleared up since yesterday, it makes sense to
    include iOS platform in the fix.
    
    Fixed: b/360642942
    Change-Id: Ie4c0db3efa74be72ee388ba95d052f7a0bef6ae8
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5817737
    Reviewed-by: Patrick Noland <pnoland@chromium.org>
    Auto-Submit: Tomasz Wiszkowski <ender@google.com>
    Commit-Queue: Tomasz Wiszkowski <ender@google.com>
    Cr-Commit-Position: refs/heads/main@{#1347647}

M       components/omnibox/browser/verbatim_match.cc

https://chromium-review.googlesource.com/5817737


### en...@google.com (2024-08-27)

re: [comment#33](https://issues.chromium.org/issues/360642942#comment33) - file:/// urls are not disabled on mobile devices. these are suppressed because `~` expansion was occasionally confusing to users. there was no value in keeping it as a regular entrypoint to file browser, because android has one already built in.

there's no vulnerability revealed in [comment#33](https://issues.chromium.org/issues/360642942#comment33), at least i fail to see one.

### gh...@gmail.com (2024-08-28)

Alright, Thanks for the explanation

### gh...@gmail.com (2024-08-28)

Can I know when the Reward will be decided and awarded?

### pe...@google.com (2024-08-28)

Security Merge Request Consideration: Requesting merge to beta (M129) because latest trunk commit (1347647) appears to be after beta branch point (1343869).
**Merge rejected:** M129 is already shipping to beta and this issue is marked as a Priority:P2,P3 or Type:feature request.

Please contact the milestone owner if you have questions.

**Owners:** govind (Android), govind (iOS), matthewjoseph (ChromeOS), srinivassista (Desktop)
Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [129].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### pe...@google.com (2024-08-29)

Security Merge Request Consideration: Requesting merge to beta (M129) because latest trunk commit (1347647) appears to be after beta branch point (1343869).
Security Merge Request - Manual Review: Merge review required: M129 is already shipping to beta.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [129].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### am...@chromium.org (2024-08-29)

The priority was not in tandem to severity being changed from S3 to S2/medium, so this applies for a potential merge to M129, which is currently in beta

### am...@chromium.org (2024-08-29)

I am reopening this though, because it looks like this fix was reverted on iOS due to a test failure

### am...@chromium.org (2024-08-29)

The fix for Android (<https://crrev.com/c/5814284>) has been on canary since 26 August and there do not appear to be any issues related to this change since it was finally landed and a change for iOS landed separately.
Please merge this fix to M129 / branch 6668 at your earliest convenience so this fix can be included in the next Beta update.

### gh...@gmail.com (2024-08-29)

Hi team, why was the Universal title removed? This report is a real Universal Xss

### st...@google.com (2024-08-30)

I don't actually repro this on iOS 128 Stable.

Address Bar Spoofing :

1. Open <https://www.google.com/search?q=https://evil.com>
2. Navigate to facebook.com
3. open a Recent Search for evil.com

Result: opens google.com/search?q=<https://evil.com>. The address bar shows google.com.
I think this is expected.

Universal XSS

1. Open <https://www.google.com/search?q=javascript%3Aalert%28document.domain%29>
2. Navigate to facebook.com
3. Use the suggestion for the recent search above

Result: opens google.com/search?q=javascript%3Aalert%28document.domain%29 and no alert is shown.
I think this is also expected.

Removing iOS and reassigning to Amy for confirmation; please send back to me if I'm doing something wrong with the repro!

### gh...@gmail.com (2024-08-30)

Hi team, this vulnerability has been confirmed, how can this be removed ?
I have sent the above proof that IOS is affected. I also send the proof again in the attachment below

### gh...@gmail.com (2024-08-30)

Hi team, this vulnerability can be reproduced in version 128.0.6613.92

In version 128.0.6613.98 the vulnerability has been fixed. It seems that there is miscommunication here. my report was already 2 weeks ago

so I don't think it's necessary to remove IOS from the affected OS

### gh...@gmail.com (2024-09-01)

Hi team, Any Update??

### pe...@google.com (2024-09-02)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### gh...@gmail.com (2024-09-02)

Hi can you add IOS to OS? Like this :
`OS:​Android, iOS`

because you tested the vulnerability after the `Fixed` status report and application update

### go...@google.com (2024-09-03)

Please merge your change to M129 by 3:00 PM PT today so we can take it in for this week's M129 beta release.

M129 Branch Details: https://chromiumdash.appspot.com/branches

### pg...@google.com (2024-09-04)

Testing on iOS with Chrome version 128.0.6613.98 - I was also unable to reproduce. This version was [released August 27](https://chromereleases.googleblog.com/2024/08/chrome-stable-for-ios-update_27.html) and the fix for iOS landed also Aug 27 but to version 130, not backmerged to older versions, and reverted soon after.

@reporter, can you confirm the version of Chrome you used in the repro video in [comment#45](https://issues.chromium.org/issues/360642942#comment45)?

### gh...@gmail.com (2024-09-04)

Hi team, I have again attached complete proof below
`Version : 128.0.6613.98`

### pe...@google.com (2024-09-06)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### gh...@gmail.com (2024-09-09)

Hi team, is there a reply to [comment#45](https://issues.chromium.org/issues/360642942#comment45)?

### go...@google.com (2024-09-09)

Please merge your change to M129 latest by 10:00 AM PT tomorrow, Sept 10th so we can take it in for this week's M129 Early Stable release on Wednesday, Sept 11th.

M129 branch Details: https://chromiumdash.appspot.com/branches

### am...@chromium.org (2024-09-09)

Reassigning back to stkhapugin@ so merge to M129 can be completed ASAP / by tomorrow's deadline for M129 Stable RC cut

### am...@chromium.org (2024-09-09)

Assigning to ender@ for merge to be completed

### en...@google.com (2024-09-10)

I'm out of the office this week. I'm not entirely sure what needs to be
done here, but if this is urgent, please pass this to pnoland@

On Mon, Sep 9, 2024, 7:55 PM amyressler <buganizer-system@google.com> wrote:

> Replying to this email means your email address will be shared with the
> team that works on this product.
> https://issues.chromium.org/issues/360642942
>
> *Changed*
>
> *amyressler@chromium.org <amyressler@chromium.org> added comment #57
> <https://issues.chromium.org/issues/360642942#comment57>:*
>
> Assigning to ender@ for merge to be completed
>
> _______________________________
>
> *Reference Info: 360642942 Multiple Vulnerability Address Bar Spoofing to
> XSS via Recent Search*
> component:  Public Trackers > Chromium Public Trackers > Chromium > UI >
> Browser > Omnibox <https://issues.chromium.org/components/1457180>
> status:  Fixed
> reporter:  ghifari898@gmail.com
> assignee:  ender@google.com
> cc:  amyressler@chromium.org, cthomp@chromium.org, ender@google.com, and
> 4 more
> collaborators:  security-notify@chromium.org
> type:  Vulnerability
> access level:  Limited visibility
> priority:  P1
> severity:  S2
> duplicate:  360044702 <https://issues.chromium.org/issues/360044702>
> found in:  126
> hotlist:  external_security_report
> <https://issues.chromium.org/hotlists/5433527>, reward-topanel
> <https://issues.chromium.org/hotlists/5432096>, Security_Impact-Extended
> <https://issues.chromium.org/hotlists/5432548>, Unconfirmed
> <https://issues.chromium.org/hotlists/5437934>, Untriaged
> <https://issues.chromium.org/hotlists/5614589>
> retention:  Component default
> Component Ancestor Tags:  UI, UI>Browser, UI>Browser>Omnibox
> Component Tags:  UI>Browser>Omnibox
> Merge:  Approved-129
> Milestone:  129
> OS:  Android
>
>
> Generated by Google IssueTracker notification system.
>
> You're receiving this email because you are subscribed to updates on
> Google IssueTracker issue 360642942
> <https://issues.chromium.org/issues/360642942> where you have the roles:
> cc, assignee
> Unsubscribe from this issue.
> <https://issues.chromium.org/issues/360642942?unsubscribe=true>
>


### am...@chromium.org (2024-09-10)

Hi pnoland@ can you please merge this fix <https://crrev.com/c/5814284> to M129 / branch 6668 immediately, so this fix can be included in the M129 Stable RC today -- thank you!

### go...@google.com (2024-09-10)

pnloand@ is OOO too

### am...@chromium.org (2024-09-10)

Hi gangwu@ -- it looks like pnoland@ is OOO until tomorrow, can you please merge this change?

### go...@google.com (2024-09-10)

Prepared M129 merge here - https://chromium-review.googlesource.com/c/chromium/src/+/5851277

### ga...@google.com (2024-09-10)

just saw the bug, thank Krishna for the CL, I will review it

### ap...@google.com (2024-09-10)

Project: chromium/src
Branch: refs/branch-heads/6668

commit 4d2cab773589a430dfae515994c3e6cad0eb0270
Author: Tomasz Wiszkowski <ender@google.com>
Date:   Tue Sep 10 17:59:43 2024

    [M129] Disallow VerbatimMatches to open non-navigable URLs by default.
    
    This change prevents non-navigable URLs from being opened upon paste,
    refine, autocomplete etc., effectively disallowing accidental execution
    of inline javascript: blocks.
    
    The non-navigable (e.g. executable) URIs will be effectively pushed
    down on the suggestions list, making them still available, but
    moving forward these will require an explicit user action to be
    invoked (i.e. the user now has to intentionally tap these suggestions
    to initiate the corresponding action).
    
    The change removes redundant test that relies on inline page
    injection. This is already covered by another test:
    http://shortn/_NG1M484b41
    
    (cherry picked from commit 04938340e1a93e5e5588badd5e01600dd3356d52)
    
    Bug: b/360642942
    Change-Id: I47abb15e38272355664ac8e2714b04a8dbef11e2
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5814284
    Reviewed-by: Gang Wu <gangwu@chromium.org>
    Commit-Queue: Tomasz Wiszkowski <ender@google.com>
    Cr-Original-Commit-Position: refs/heads/main@{#1347092}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5851277
    Reviewed-by: Krishna Govind <govind@chromium.org>
    Owners-Override: Krishna Govind <govind@chromium.org>
    Commit-Queue: Krishna Govind <govind@chromium.org>
    Cr-Commit-Position: refs/branch-heads/6668@{#1133}
    Cr-Branched-From: 05bc664984ca075216b7f2198c88b9725bfa1b9b-refs/heads/main@{#1343869}

M       chrome/android/javatests/src/org/chromium/chrome/browser/omnibox/UrlBarTest.java
M       components/omnibox/browser/verbatim_match.cc

https://chromium-review.googlesource.com/5851277


### gh...@gmail.com (2024-09-11)

Hi team, Any update for [comment#45](https://issues.chromium.org/issues/360642942#comment45) and [comment#52](https://issues.chromium.org/issues/360642942#comment52)?

### am...@chromium.org (2024-09-11)

I have also tried to reproduce this on the same version of Chrome for iOS on an iphone 14 and am unable to successfully repro.

### gh...@gmail.com (2024-09-12)

It should be noted that the vulnerability cannot be reproduced if your Chrome iOS is in incognito mode.

### sp...@google.com (2024-09-12)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
$1,000 for report of lower impact, mitigated XSS / web platform privilege escalation


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-09-13)

Congratulations Muhammad! Given how the level of mitigation here in comparison to a standard XSS/UXSS and the preconditions to reasonably convince a user to engage in their search results in this way for an attacker to make use of this XSS in the time that these were still part of the victims search history, we have assessed this issue as of lower impact. But we do thank you for your efforts here and appreciate you reporting this issue to us.

### gh...@gmail.com (2024-09-13)

Thank you for the reply.

but why is the prize I got so small, even though this is Universal XSS

and the reasons given are also inaccurate

> Rationale for this decision:
> $1,000 for report of lower impact, mitigated XSS / web platform privilege escalation

First, this vulnerability is confirmed to impact Android and iOS

Second, this report and [b/360044702](https://issues.chromium.org/issues/360044702) have been combined into 1 report

Third, this XSS not only attacks the Default Search Engine like report [b/360044702](https://issues.chromium.org/issues/360044702) but also attacks the entire web (Universal)

So I don't agree with the current reward, this is very far from my expectations if you look at previous reports, such as:
[b/40082910](https://issues.chromium.org/issues/40082910)
[b/40936265](https://issues.chromium.org/issues/40936265)
[b/40083619](https://issues.chromium.org/issues/40083619)

Even the rewards given are lower than regular Spoofing:
[b/40092386](https://issues.chromium.org/issues/40092386)
[b/40084252](https://issues.chromium.org/issues/40084252)
[b/40056854](https://issues.chromium.org/issues/40056854)

Previously I reported a similar vulnerability on Microsoft Edge Android and (Only attacks the search engine) like report [b/360044702](https://issues.chromium.org/issues/360044702) but I got $3000, why in this report which clearly has 2 attack scenarios from 2 reports combined and can attack all domains/websites not only Default Search Engine, just get lower payout. even on your bounty table Lower Impact Up to $10,000

can we discuss it again? I'm quite disappointed to see this :(

### gh...@gmail.com (2024-09-13)

Take a look at this image, this is proof of the bounty amount in my report on Microsoft Edge a few months ago.

even though this only attacks the Default Search Engine

### gh...@gmail.com (2024-09-13)

> comparison to a standard XSS/UXSS and the preconditions to reliably convince a user to engage in their search results in this way for an attacker to make use of this

In fact, it takes quite a long time or repeated searches for JavaScript to no longer appear in your browsing history. so in my opinion this cannot be considered as a reference for reducing the impact

### am...@chromium.org (2024-09-13)

We're sorry you are disappointed with this reward decision.

> First, this vulnerability is confirmed to impact Android and iOS

We did not dispute this impacts Android. Our team was not at all able to confirm the impact to iOS.
This, however, does not impact the reward amount.

Rewards are strictly based on the impact and potential for user harm, demonstrated impact, and report quality.

> Second, this report and [b/360044702](https://issues.chromium.org/issues/360044702) have been combined into 1 report

Again, this was explained in [crbug.com/360044702](https://crbug.com/360044702), the same root cause with two different ways to exploit the same issue, both with high preconditions to successfully exploit and leverage by an attacker, do not result in a higher severity. But it also does not result in a higher reward in most cases unless there is an exploitation vector that is much more straightforward. Such is not the case here.

In this issue, the attacker must send the URL with the javascript to the victim, who must click / visit it in a way that it will end up in victims search history. It is not not propagated into the victim's search history without some prior handling of it with the search engine. Then the victim must be coerced / convinced to visit that link with the javascript from their search history and before the search results are no longer part of their recent history.

> So I don't agree with the current reward, this is very far from my expectations if you look at previous reports, such as: [b/40082910](https://issues.chromium.org/issues/40082910) [b/40936265](https://issues.chromium.org/issues/40936265) [b/40083619](https://issues.chromium.org/issues/40083619)

Standard, and considered highly severe UXSS via the browser is generally achieved by a victim simply accessing malicious web content directly. This is not the case here, thus this is a very mitigated version of UXSS.

The examples you link here are all cases of UXSS being achieved through 0 to minimal user interaction, directly from malicious web content. These reports also all came with full, functional exploits -- thus the even higher reward amounts.

> Previously I reported a similar vulnerability on Microsoft Edge Android and (Only attacks the search engine) like report [b/360044702](https://issues.chromium.org/issues/360044702) but I got $3000,

Thank you for letting us know. Our programs, however, have different reward structures and criteria.

This all being said, we're happy to take another look at a future VRP Panel session; however, I do want to convey that we discussed this issue very thoroughly today. It was clear your expectations for this issue were very high given the repeated requests for a change in severity. We did review both reports. Other than the $3,000 reward amount from the Edge bounty program, there's no new information for us here to help change the outcome, but I am happy to put it back in the queue for reassessment.

### gh...@gmail.com (2024-09-13)

I hope that this report will be reviewed and receive the fairest possible compensation in accordance with existing policies. considering the severity is S2 so when I saw the reward given, it was very far from my expectations

### gh...@gmail.com (2024-09-13)

Thank you for your reply and understanding

Re : [Comment#73](https://issues.chromium.org/issues/360642942#comment73)

> In this issue, the attacker must send the URL with the javascript to the victim, who must click / visit it in a way that it will end up in victims search history

In this case, the attacker must send a URL with javascript to the victim, who must click/visit it in such a way that it goes into the victim's search history.

This is very reasonable considering that this kind of attack method is normal and usually in CVSS `UI:R`. also the url that the attacker sent is not suspicious because it comes from the Google Search Engine via keywords, compared to report [b/40082910](https://issues.chromium.org/issues/40082910) [b/40936265](https://issues.chromium.org/issues/40936265) the victim must be persuaded by the attacker to open the exploit.html site hosted by the attacker himself.

> It is not not propagated into the victim's search history without some prior handling of it with the search engine. Then the victim must be coerced / convinced to visit that link with the javascript from their search history and before the search results are no longer part of their recent history.

I agree with this, but it should be noted that if the victim has logged into his Google account in the browser then the content will be in the search history (Recent Search) for a long time and will have to do many searches so that the content disappears from the search history (Recent Search) victims

> Standard, and considered highly severe UXSS via the browser is generally achieved by a victim simply accessing malicious web content directly. This is not the case here, thus this is a very mitigated version of UXSS.

Even so it is still called Universal XSS

> The examples you link here are all cases of UXSS being achieved through 0 to minimal user interaction, directly from malicious web content.

If we refer back to report [b/40082910](https://issues.chromium.org/issues/40082910) [b/40936265](https://issues.chromium.org/issues/40936265) don't they need interaction? Even more than 2 times the interaction.

> These reports also all came with full, functional exploits -- thus the even higher reward amounts.

I think this report meets the requirements of a report with a fully functional exploit, because it is clear that I provide all the details starting from functional, simple steps, even with screenshots and reproduction videos.
just because this vulnerability is simple and does not require exploitation steps like an attacker site with exploit.html like this <http://attacker.io/exploit.html> so it doesn't meet the requirements?

I hope you and your team can reconsider the rewards of this report. Sorry if there are any wrong words, it's a pleasure to discuss with you.

Kind regards,
Zaid

### am...@chromium.org (2024-09-18)

Hello Zaid, while we appreciate this report, we have reassessed this issue and have determined that the original reward amount was sufficient based on our threat model and reward structure.

There was no new information in the reassessment request and our original feedback about this issue and reward decision remain.

To counter some of your follow-up points, this is not considered a UXSS, since it's not universal in that there is a dependency to leverage the search engine and the exploitability is limited. There are substantial steps and much convincing of a user to engage in a way that is not standard for a UXSS.

A user being convinced to simply browse to a malicious, attacker-hosted page is standard and expected for XSS; a convincing a user to navigate to a javascript link then re-engage with that link strictly via recent search history results adds considerable friction and user engagement / convincing to exploitability.

### gh...@gmail.com (2024-09-21)

Re : [Comment#76](https://issues.chromium.org/issues/360642942#comment76)

> this is not considered a UXSS, since it's not universal in that there is a dependency to leverage the search engine and the exploitability is limited. There are substantial steps and much convincing of a user to engage in a way that is not standard for a UXSS.

Hi team, although there is a dependency on utilizing search engines and exploitation is limited. but in terms of final impact it remains Universal Xss.
I agree more with your statement above regarding the high complexity of the attack but it doesn't change this vulnerability because this is still Universal XSS

### gh...@gmail.com (2024-09-30)

Hi team, Any update?

### am...@chromium.org (2024-09-30)

Hello, there is no update we have to share since the update in c#76. We previously explained that we considered this a limited XSS and the rationale. Despite, however, the semantics around title / naming convention here, we consider this a lower impact issue with significant preconditions. The categorization of impact (with parameters of preconditions and path to exploitation) are the primary criteria for reward amount, so there is no planned changes or update here as we deemed our latest decision from reassessment conveyed in c#76 to be final, especially given there has been no new technical information or demonstration of this provided to warrant a decision change. Thank you.

### gh...@gmail.com (2024-11-06)

Hi team,

The reasons why this vulnerability should have high severity are:

<https://ik.imagekit.io/zheev/Exploit%20UXSS%20OPPO.html>

1. If you exploit using the CSRF below: then the javascript:url will automatically be saved in the victim's recent search so that the complexity of the attack is low, not high
2. This UXSS attack not only takes advantage of the victim's ignorance, but can be exploited through errors in pressing recent search because javascript:url will be stored for a long time in the victim's browser, especially if the victim is logged in to his Google account in the browser. then this javascript:url can attack across browsers/devices, for example between browsers on different devices

### pe...@google.com (2024-12-17)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### gh...@gmail.com (2024-12-18)

Re :[Comment#80](https://issues.chromium.org/issues/360642942#comment80)

I managed to minimize this vulnerability step, why is there no update? IOS was also affected by this attack, I have attached [comment #6](https://issues.chromium.org/issues/360642942#comment6)
Can you close this report again so that it is not visible to the public? because this vulnerability is in fact not yet resolved

### am...@chromium.org (2024-12-18)

As mentioned in comments above, there were multiple attempts to reproduce this issue on iOS by various members of our team before and after this issue was closed. 
In c#51, we requested you please confirm the version of Chrome on iOS you were able to reproduce this issue on, but received no response with that information from you.

I just attempted to reproduce this issue on Chrome on iOS version 131.0.6778.134 and I was not able to reproduce this issue. 
Based on this, we cannot find a reason to re-restrict this report at this time.


### gh...@gmail.com (2024-12-18)

Steps to Reproduce :

- Navigate to <https://ik.imagekit.io/zheev/Exploit%20UXSS%20OPPO.html>
- the page will change to a google url with the keywords "javascript:alert(document.domain);"
- victim clicks the top left arrow
- XSS triggered

POC :
<https://drive.google.com/file/d/1ihkNMzlS-y3Zl_KQfSsSrsz4J3T3OEGp/view?usp=sharing>

Chrome IOS Version : 131.0.6778.154

### am...@chromium.org (2024-12-18)

Two of us on the team just attempted to reproduce this on Chrome for iOS; following your reproduction this does not reproduce as described. 

By clicking the `submit request` from the poc link, we are presented with the google search of `javascript:alert(document.cookie)`. That does reproduce.
However, in navigating to another page, when using the omnibox to search, the javascript command is not available in the most history or suggested results, the user must explicitly search for `javascipt:` for `javascript:alert(document.cookie)` to be suggested in the history and the user has to explicitly click the arrow to the right of the javascript select it to trigger this. This is essentially the same as the user copying and pasting the javascript into the URL or executing it from a bookmarklet, neither of which are considered security issues. [1][2]

We're going to consider this issue completed closed now. 
Please do not expect further comments or response to this issue. 
Thank you.


[1] https://chromium.googlesource.com/chromium/src/+/main/docs/security/faq.md#does-entering-javascript_urls-in-the-url-bar-or-running-script-in-the-developer-tools-mean-there_s-an-xss-vulnerability
[2] https://chromium.googlesource.com/chromium/src/+/main/docs/security/faq.md#does-executing-javascript-from-a-bookmark-or-the-home-button-mean-there_s-an-xss-vulnerability

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/360642942)*
