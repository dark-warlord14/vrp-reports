# XSS in 1993 history handling

| Field | Value |
|-------|-------|
| **Issue ID** | [40076846](https://issues.chromium.org/issues/40076846) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals |
| **Reporter** | js...@chromium.org |
| **Assignee** | [Deleted User] |
| **Created** | 2013-01-19 |
| **Bounty** | $500.00 |

## Description

From an external report:

Hi,

There is a strang bug in the latest Chrome Beta 25.0.1364.36 beta-m (Windows)

It looks like that Google Search is much more integrated in the latest version, but unfortunately there is a XSS vulnerability inside.

Steps to reproduce:

1. Open Chrome with new user 
2. Search for "><img src=x <img src=x onerror=prompt(7)>=<img src=x onerror=prompt(7)>(1)> via browser search bar
3. Okay, nothing happen...
4. Search again for "<img src=x onerror=prompt(7)>" 

Screenshot:
https://docs.google.com/file/d/0BwS7P2UORGoocTc0MHc1WEhWVnc/edit

## Timeline

### js...@chromium.org (2013-01-19)

First order of business is to figure out where the script is actually executing. I can't trigger the 1993 interface, so I don't know if this is executing in google.com or in webui. Both are equally bad (for different reasons), but if it's getting injected into google.com then I'm very confused how, and if it's in webui then I don't understand why we don't have CSP blocking it. Regardless, this kind of trivially detectable XSS means we should probably postpone the experiment until the feature is closer to ready.

### [Deleted User] (2013-01-19)

Uh oh. Justin, how can we help investigate this? You can enable 1993 by flipping "Enable Instant Extended API" in about:flags on Windows Beta.

### jo...@chromium.org (2013-01-19)

My understanding of 1993 makes me believe that this should be executing in google.com, but I might be wrong. I'm on my phone in Sausalito but I can test this when I get back tonight.

### ke...@google.com (2013-01-19)

I'd like a fix for the next beta, or we should disable it.

### [Deleted User] (2013-01-20)

+cc a bunch of 1993 engineers so they can see the bug.

### [Deleted User] (2013-01-20)

This executes in the context of the google.com page.

However, I don't consider this an XSS. The *user* has to type this into the omnibox to get it to execute in the context of the google.com page. How's it any different from the user executing such scripts through say the JS console or just plainly typing [javascript:alert(7)] into the omnibox when on a google.com page?

Of course, if random history entries are able to achieve the same type of XSS, that would indeed be a major worry. Because then, the user could be tricked into visiting a URL that has some payload, which could get sent through to the page as a history match entry, appropriately shadow DOM'ed but perhaps still causing an XSS.

### sc...@gmail.com (2013-01-20)

@sreeram: the correct classification of this is "XSS, requiring user interaction". I've lowered the severity a notch.

This was discovered by an external security researcher. We should fix it promptly to avoid e.g. embarrassment via press article.

### js...@chromium.org (2013-01-20)

Most people refer to these things as self XSS (if that's the only vector). Sadly, it's a legitimate problem and the reason we had to disable pasting javascript: URLs into the omnibox. Simply put, many people will paste anything into the omnibox and assume it's entirely safe.

### [Deleted User] (2013-01-20)

Ah, very interesting. So what's the correct behavior here, then? Will we in 1993 be making it extremely difficult for people to search for things that look like they could be executable pieces of JS (because we won't have the searchbox on the page)? I guess they'd just have to go to google.com.

Guidance from security folks about the correct behavior of the omnibox here, in terms of these types of input strings, would be hugely appreciated. We'll fix it ASAP.

+cc pkasting

### sc...@gmail.com (2013-01-20)

"Will we in 1993 be making it extremely difficult for people to search for things that look like they could be executable pieces of JS"

Wait, wut? No, we should just need to exercise correct HTML escaping!

### [Deleted User] (2013-01-20)

@jschuh, please review https://chromiumcodereview.appspot.com/12039002/ which contain Chrome side fixes.

Questions:

1. Is there an existing escapeHTML() type function I can reuse? A quick grep through the code didn't find anything. I modelled my variation on htmlUnescape() from chrome/browser/resources/file_manager/js/util.js.

2. Seems like GetFont() is another vector for injection. I could fix it in the same CL, but could somebody tell me the definitive list of characters I should escape for CSS attribute strings (see where GetFont() is being inserted), and how?

@gideonwald: I believe fixes may be needed on the google.com side as well. Please file a bug internally.

### js...@chromium.org (2013-01-20)

There are other people CC'd who can provide better expertise HTML entity handling and XSS mitigation here. Broadly speaking though, I'm a bit confused. What context is this executing in (domui or www.google.com)? That's important for us to understand the broader implications. Also, why would we need server-side changes, since by design we should never be executing or directly rendering any content from the server?

### [Deleted User] (2013-01-20)

As you type in the omnibox, the omnibox text along with local history suggestions are fed to a google.com page through a JS API (encapsulated in the file searchbox_api.js). So, the injection happens in the context of google.com.

The history suggestions are rendered using shadow DOM. My CL above makes sure that searchbox_api.js escapes the suggestions correctly. In addition, google.com can access other raw content through the API, e.g.: chrome.searchBox.value (which is the omnibox text) or chrome.searchBox.font (the omnibox dropdown font), so if it doesn't escape them correctly before rendering them, it could also have an injection vector. That's why I said google.com also needs to be checked carefully.

If google.com is unreachable, we use a local fallback page, whose URL is chrome://local-omnibox-popup/local-omnibox-popup.html. The resources for these are in chrome/browser/resources/local_omnibox_popup/local_omnibox_popup.*. As far as I could tell, that page doesn't insert any unescaped text, so I don't see an injection possibility there.

### [Deleted User] (2013-01-22)

[Empty comment from Monorail migration]

### jo...@chromium.org (2013-01-22)

I've pinged evn@ to see if we can reuse escaping code. He's also cc'd in this bug.

### pa...@chromium.org (2013-01-22)

FWIW, it reproduces on Linux but requires significant user interaction (I have to add and remove the trailing ">" in a search for

    "> <img src=x onerror=prompt(1)>

I haven't tried Windows yet; does it require less interaction?

### ad...@google.com (2013-01-22)

NOTE: As discussed with Chrome Security folks, adding external (i.e. non-Google) bug reporter to the bug.

### ev...@google.com (2013-01-22)

@sreeram, your escapeHTML function LGTM, perhaps add " and ' to the chars to escape as well in case someone reuses this function for inside-attribute escaping.

Did 1993 get a security review?


### jo...@chromium.org (2013-01-22)

Re: c#18 yes, the 1993 team has been working closely with the Security Team.

### ni...@gmail.com (2013-01-22)

Just a note to the issue, it's much easier to exploit.

Open this URL: http://xhtml.im/chromexss.html

Then open a new tab, search for x. If you don't get a prompt(), just click in the big white area under the instant result.

### ma...@chromium.org (2013-01-22)

I can also see interesting blinking in the suggest box for this entry... ;-)

### [Deleted User] (2013-01-22)

@18: Done. I've updated the patch at https://codereview.chromium.org/12039002/.

I've also verified that the injection attempt (as described in #20) succeeds without the patch, and fails with the patch.

### ev...@google.com (2013-01-22)

last time I talked with the shadowdom people, they specifically mentioned it should not be used for hiding content from the parent page as it can't offer such guaranteed.

isn't this doing this now?

### ev...@google.com (2013-01-22)

s/guaranteed/guarantees/

### jo...@chromium.org (2013-01-22)

Shadow DOM is supposed to prevent Most Visited sites to be accessible by the search engine when it builds the New Tab page. Gideon, 1993 engineers, did you get confirmation from the Shadow DOM team that this is a reasonable expectation?

### [Deleted User] (2013-01-22)

Yes, we are indeed using Shadow DOM to hide content from the page. Even if it's not guaranteed, I think it's a reasonable barrier.

The Shadow DOM'ed content is only made available to the default search provider, and only if it supports Instant. We (Google) must explicitly hardcode the instant_url for any such search provider in the Chrome builds we distribute. So, if a search provider tries to get around the barrier, we can not only remove them from the "supported" list, we can also name and shame them.

### ev...@google.com (2013-01-22)

There are several things to take into consideration:

1. XSS in google.com happens. Before it wasn't the case that most-visited sites were available to people with an XSS in google.com (we moved history.google.com off-www for that specific reason, this seems to be a step back).
2. Maybe we should add a comment around the code that guards instant so mention that any domain we add there will effectively be able to read part of the user's navigation history.

### [Deleted User] (2013-01-22)

I think we should take that part of the discussion off this bug to email, unless you guys think it's the same issue - I'd like to keep this focused on how to best resolve the XSS exploit in question (which it looks like Sreeram's patch does - thanks Sreeram!).

I'll start an email thread with the folks who have chimed in so far.

### bu...@chromium.org (2013-01-23)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=178247

------------------------------------------------------------------------
r178247 | sreeram@chromium.org | 2013-01-23T04:40:51.440438Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/renderer/resources/extensions/searchbox_api.js?r1=178247&r2=178246&pathrev=178247

Escape HTML to avoid injection attacks.

BUG=171134
R=jschuh@chromium.org
TEST=No more XSS (server side fixes also necessary).


Review URL: https://chromiumcodereview.appspot.com/12039002
------------------------------------------------------------------------

### js...@chromium.org (2013-01-23)

High-severity seems more appropriate based on the repro in https://crbug.com/chromium/171134#c20.

### jo...@chromium.org (2013-01-23)

And we want to merge to 25, right?

### bu...@chromium.org (2013-01-23)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=178315

------------------------------------------------------------------------
r178315 | sreeram@chromium.org | 2013-01-23T17:19:02.458345Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/1364/src/chrome/renderer/resources/extensions/searchbox_api.js?r1=178315&r2=178314&pathrev=178315

Merge 178247
> Escape HTML to avoid injection attacks.
> 
> BUG=171134
> R=jschuh@chromium.org
> TEST=No more XSS (server side fixes also necessary).
> 
> 
> Review URL: https://chromiumcodereview.appspot.com/12039002

TBR=sreeram@chromium.org
Review URL: https://codereview.chromium.org/12047052
------------------------------------------------------------------------

### [Deleted User] (2013-01-23)

[Empty comment from Monorail migration]

### [Deleted User] (2013-01-23)

We did indeed want to merge it to M25 - but just to be sure, Jason, you're okay taking this? :)

### jo...@chromium.org (2013-01-23)

Security team has Merge-Approved powers for important, very localized security fixes =)

### [Deleted User] (2013-01-23)

Aha! Makes sense - thanks for educating me :).

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### js...@chromium.org (2013-04-11)

Bulk edit for SecurityNotify.

### pa...@chromium.org (2013-04-25)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-05-03)

@nils: thanks! $500 Chromium Security Reward.

### pa...@chromium.org (2013-05-28)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-06-07)

Processing via our e-payment system can take a few weeks, but reward should be on its way to you. Thanks again for your help!

### js...@chromium.org (2013-11-18)

Bulk release of old security bug reports.


### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/171134?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40076846)*
