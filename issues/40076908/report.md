# New search UI (1993) could lead to self-XSS

| Field | Value |
|-------|-------|
| **Issue ID** | [40076908](https://issues.chromium.org/issues/40076908) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | UI, UI>Browser>Instant>Extended |
| **Reporter** | ni...@gmail.com |
| **Assignee** | je...@chromium.org |
| **Created** | 2013-01-31 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.22 (KHTML, like Gecko) Chrome/25.0.1364.58 Safari/537.22

Steps to reproduce the problem:
https://www.google.com/search?q=javascript:alert(1)&rlz=1C1CHNR_deDE453DE453&aq=f&aqs=chrome.0.57j60l2j61.312&sourceid=chrome&espv=1&ie=UTF-8

javascript:alert(1) is displayed as search query in the URL bar. A reload loads the search query again.. 

A click into the URL bar followed by a "enter" will lead to a self-XSS and not a search query.

What is the expected behavior?

What went wrong?
It's now to easy to trick user into self-XSS.

Did this work before? N/A 

Chrome version: 25.0.1364.58  Channel: beta
OS Version: 6.1 (Windows 7, Windows Server 2008 R2)

## Attachments

- [Screen Shot 2013-05-01 at 3.33.08 PM.png](attachments/Screen Shot 2013-05-01 at 3.33.08 PM.png) (image/png; charset=binary, 183.5 KB)

## Timeline

### jo...@chromium.org (2013-01-31)

[Empty comment from Monorail migration]

### js...@chromium.org (2013-01-31)

This is not instilling confidence. Perhaps it's time to revisit some of the architectural decisions here?

### js...@chromium.org (2013-01-31)

[Empty comment from Monorail migration]

### [Deleted User] (2013-01-31)

I think the problem isn't architectural so much as, we still don't have a good coherent design around what we want to do in this case.

In non-1993, if the user hits Enter in the omnibox while it contained the text 'javascript:alert(1)', it alerts. Is it unexpected that it would do the same thing here? Or is the point of contention the fact that we do search term replacement in this case? Perhaps this is another type of string for which we bail out of 1993 and show the full URL in the omnibox instead of just the search terms, like with URL queries.

### th...@chromium.org (2013-01-31)

+ other 1993 folks.

### [Deleted User] (2013-01-31)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-02-01)

[Empty comment from Monorail migration]

### js...@chromium.org (2013-02-01)

@gideon - My point about architectural decisions is that we consistently expressed strong reservations with this design because it mixes www.google.com and Chrome in ways that significantly increase the attack surface on both sides. However, the consensus was to let the experiment move forward and we'd see how things worked out. This is the second trivial XSS issue introduced into www.google.com, and the experiment has barely started. So, I'm sure you can appreciate that I'm a bit worried.

As for this specific case, the current behavior is unambiguously wrong. A web site must *never* be able to put a javascript: URL in the omnibox. Ignoring the simple social engineering attack, it hits on our process and history management, which has historically been fertile ground for spoofing attacks, UXSS and sandbox escapes.

Maybe it would be best to just chat in person, so I can better convey the larger concerns?


### [Deleted User] (2013-02-01)

Yeah, let's discuss in person. Tomorrow if we can find the time, else on Monday. Thanks, Justin.

### in...@chromium.org (2013-02-11)

[Empty comment from Monorail migration]

### gr...@chromium.org (2013-02-14)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-02-18)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=183128

------------------------------------------------------------------------
r183128 | grt@chromium.org | 2013-02-18T16:15:40.600119Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/ui/toolbar/toolbar_model_unittest.cc?r1=183128&r2=183127&pathrev=183128
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/ui/toolbar/toolbar_model_impl.cc?r1=183128&r2=183127&pathrev=183128
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/ui/toolbar/toolbar_model_impl.h?r1=183128&r2=183127&pathrev=183128

Don't extract search terms that the omnbox would treat as a navigation.

Doing so might confuse users into believing that the search terms were
the URL of the current page, and could cause problems if users hit enter
in the omnibox expecting to reload the page.  This also covers the case
of javascript: URLs.

BUG=163192,173483
TEST=With instant extended API enabled, paste the following URL into the omnibox and note that the whole URL is visible in the omnibox as the search results are shown. https://www.google.ca/webhp?sourceid=chrome-instant&espv=1&ie=UTF-8#hl=en&sugexp=les%3B&gs_rn=0&gs_ri=hp&cp=4&gs_id=0&xhr=t&q=http://www.shadybank.com/&pf=p&tbo=d&espv=1&output=search&sclient=chrome-search&oq=spam&gs_l=&pbx=1&bav=on.2,or.r_gc.r_pw.r_qf.&bvm=bv.41642243,d.aWc&fp=ba0fd5791f5165d1&biw=0&bih=0

Review URL: https://chromiumcodereview.appspot.com/12086058
------------------------------------------------------------------------

### gr...@chromium.org (2013-02-19)

Fixed in 26.0.1417.0.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### js...@chromium.org (2013-04-11)

Bulk edit for SecurityNotify.

### pa...@chromium.org (2013-04-25)

Hey Nils,

Thanks for the report. I'm not sure if this will meet our bar for a reward, but we'll review in Chrome's reward panel.

### pa...@chromium.org (2013-05-01)

Nils' original scenario still works. Screenshot attached; I'm on Chrome Canary: Version 28.0.1495.0 canary.

### pa...@chromium.org (2013-05-01)

[Comment Deleted]

### pa...@chromium.org (2013-05-01)

Oops, here's the screenshot, FWIW.

### [Deleted User] (2013-05-01)

The bug here is that if we are showing query terms (whether prominent or not) and the user focuses the omnibox and hits Enter, we should enforce that it's treated as a search (i.e., don't classify the text and try to navigate to it).

+cc @sail, @beaudoin: Hopefully one of you can pick this up.

### pa...@chromium.org (2013-05-01)

I'm bumping the priority due to the age of the bug.

### [Deleted User] (2013-05-01)

Sail, can you take this one? Would be awesome to get this into M28 - I know that's a tough ask :/.

### pa...@chromium.org (2013-05-02)

+jered FYI

### in...@chromium.org (2013-05-02)

Please do read Mark's email titled "Calling a Code 28 for Security Bugs" on chrome-team mailing list.

### [Deleted User] (2013-05-06)

[Empty comment from Monorail migration]

### [Deleted User] (2013-05-06)

[Empty comment from Monorail migration]

### js...@chromium.org (2013-05-09)

Adding a release block label because this really needs to be fixed if we plan on letting this ship in m28.

### je...@chromium.org (2013-05-09)

[Empty comment from Monorail migration]

### sa...@chromium.org (2013-05-09)

Jered is cooking up a fix.

### [Deleted User] (2013-05-09)

Sail was looking at this so check with him to make sure you're not duplicating work!

### [Deleted User] (2013-05-09)

Sail hasn't worked on it yet, so it'd be awesome if you could grab it, Jered!

### je...@chromium.org (2013-05-10)

A fix is out for review in 14752021.

### in...@chromium.org (2013-05-14)

Lets hope this lands by EOD Thursday. We really want the security queue under control for Security Code 28.

### je...@chromium.org (2013-05-14)

inferno@, feel free to ping my reviewers and let them know that. I'm waiting for jschuh@ and pkasting@.

### bu...@chromium.org (2013-05-17)

------------------------------------------------------------------------
r200904 | jered@chromium.org | 2013-05-17T22:26:45.736278Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/ui/search/instant_extended_interactive_uitest.cc?r1=200904&r2=200903&pathrev=200904
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/policy/policy_browsertest.cc?r1=200904&r2=200903&pathrev=200904
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/ui/browser_commands.cc?r1=200904&r2=200903&pathrev=200904
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/ui/search/instant_controller.h?r1=200904&r2=200903&pathrev=200904
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/ui/omnibox/omnibox_edit_model.cc?r1=200904&r2=200903&pathrev=200904

InstantExtended: Reload when re-accepting search terms.

Previously when focusing in the omnibox and pressing enter while it
showed search results, we would re-classify the match based on the
query terms. Instead, we should refresh the search page. Not doing so
is a potential security problem and is inconsistent UI behavior, because
something that says "Search" should really do a search.

TEST=Manually and browsertest
BUG=173483,226841

Review URL: https://chromiumcodereview.appspot.com/14752021
------------------------------------------------------------------------

### in...@chromium.org (2013-05-17)

[Empty comment from Monorail migration]

### je...@chromium.org (2013-05-17)

(Will merge once this works in canary.)

### sc...@gmail.com (2013-06-07)

@jered: can you merge?

### je...@chromium.org (2013-06-07)

I did. r201095

### sc...@gmail.com (2013-06-07)

Thanks for rocking!

### sc...@gmail.com (2013-06-26)

Just checking our old notes, and this was awarded a $500 Chromium Security Reward! Thanks :D

### pa...@chromium.org (2013-08-20)

[Empty comment from Monorail migration]

### js...@chromium.org (2013-11-18)

Bulk release of old security bug reports.


### mu...@chromium.org (2013-12-04)


Browse https://www.google.com/search?q=javascript:alert(1)&rlz=1C1CHNR_deDE453DE453&aq=f&aqs=chrome.0.57j60l2j61.312&sourceid=chrome&espv=1&ie=UTF-8

click into the URL bar and hit "enter" . SRP is refreshing which is expected

Marking the bug as verified



### ti...@chromium.org (2014-02-28)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/173483?no_tracker_redirect=1

[Multiple monorail components: UI, UI>Browser>Instant>Extended]
[Monorail mergedwith: crbug.com/chromium/226841]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40076908)*
