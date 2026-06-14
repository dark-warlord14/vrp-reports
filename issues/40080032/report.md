# Popups opened from a sandboxed iframe are not themselves sandboxed

| Field | Value |
|-------|-------|
| **Issue ID** | [40080032](https://issues.chromium.org/issues/40080032) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink |
| **Reporter** | bz...@mit.edu |
| **Assignee** | mk...@chromium.org |
| **Created** | 2014-07-12 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:33.0) Gecko/20100101 Firefox/33.0

Steps to reproduce the problem:
1. Download https://bugzilla.mozilla.org/attachment.cgi?id=8454381
2. Untar it
3. Load the iframePage.html file from that tarball.
4. Click the link in the iframe.

What is the expected behavior?
A new tab opens with the text "No JavaScript!".

What went wrong?
The text said "Hello JavaScript!", which means javascript ran even though the content was supposed to be sandboxed.

Did this work before? N/A 

Chrome version: 37.0.2062.3 (Official Build 279868) dev  Channel: n/a
OS Version: OS X 10.9
Flash Version: Shockwave Flash 14.0 r0

See https://bugzilla.mozilla.org/show_bug.cgi?id=1037381#c1 for the spec text on the matter, as well as the reason why the spec text is what it is.

## Timeline

### bz...@mit.edu (2014-07-12)

Oh, and Firefox and IE get this right.

### mb...@chromium.org (2014-07-12)

Adam, could you please take a look at this when you get a chance or help find another owner?

### ab...@chromium.org (2014-07-12)

Hi bzbarsky.  Sorry about this bug.  I think we must have implemented an earlier version of the spec or I didn't understand this part of the spec.  It's important that we fix this issue before sites come to depend on our permissive behavior.  Thanks for filing the bug.

@jww and @mkwst: Feel free to grab this bug if you're interested.  There are a couple tricky parts to the implementation:

1) We need to make sure we get windows created from context menus (e.g., open in new tab).
2) We need to make sure the sandbox bits aren't lost on process swaps.

We have all the plumbing because it's used for Referrer.

### mk...@chromium.org (2014-07-12)

+nasko, who might have some time to work on this, as it's relevant to the oop frames work he's involved in.

### cl...@chromium.org (2014-07-28)

[Empty comment from Monorail migration]

### bz...@mit.edu (2014-10-20)

Just as a note, as sites use sandboxed iframes more some of them are starting to rely on this security bug.  :(  See https://bugzilla.mozilla.org/show_bug.cgi?id=1082846#c3

### js...@chromium.org (2015-02-12)

Anyone know what the status on this is?

### na...@chromium.org (2015-02-12)

[Empty comment from Monorail migration]

### mk...@chromium.org (2015-03-03)

The status is that I thought Nasko was doing it, and then missed you assigning it back to me. :)

Patch up at https://codereview.chromium.org/967423005 for review. This will likely break sites, but I think we need to take the hit.

### bu...@chromium.org (2015-03-05)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=191352

------------------------------------------------------------------
r191352 | mkwst@chromium.org | 2015-03-05T09:18:53.527661Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/page/CreateWindow.cpp?r1=191352&r2=191351&pathrev=191352
   M http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/navigation/new-window-sandboxed-iframe-expected.txt?r1=191352&r2=191351&pathrev=191352
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/resources/post-origin-to-opener.html?r1=191352&r2=191351&pathrev=191352
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/sandbox-inherit-to-blank-document.html?r1=191352&r2=191351&pathrev=191352

<iframe sandbox> should inherit through <a target='_blank'>.

We already do this properly for 'window.open', but we intentionally
dropped targeted anchor navigation in https://crbug.com/353253. This
patch reverts that decision.

https://bugzilla.mozilla.org/show_bug.cgi?id=1037381#c1 walks through
the relevant portions of the HTML spec; we're simply wrong here.

BUG=393401,353253

Review URL: https://codereview.chromium.org/967423005
-----------------------------------------------------------------

### ti...@google.com (2015-03-16)

Any remaining work here or can this issue be marked as Fixed?

### ti...@google.com (2015-04-08)

Bump mkwst - can this be marked as fixed?

### mk...@chromium.org (2015-04-08)

[Empty comment from Monorail migration]

### mk...@chromium.org (2015-04-08)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-04-08)

[Empty comment from Monorail migration]

### ti...@google.com (2015-05-16)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-07-15)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2015-10-09)

In doing a sweep for old unpaid issues, we took this to our reward panel and decided to award you $500 for reporting this issue to us. Congratulations!

Someone from our finance team will be in contact within a week to collect payment details. If that doesn't happen, please reach out to me at timwillis@ or update this bug.

Thanks!

### ti...@google.com (2015-10-16)

[Empty comment from Monorail migration]

### ti...@google.com (2015-10-29)

Payment is on its way - should arrive in ~7 days. Thanks again for your report!

### bz...@mit.edu (2016-01-08)

This still look broken to me.  The minimal testcase I attached works, but if I replace the URL in linkPage.html with "https://www.google.com" I get working script in there.

### ba...@gmail.com (2016-01-08)

I'm concerned that all this does is make sandboxed iframes useless for development purposes.

If I have a site that I'd like to display user content on, one of the easiest and safest ways to do so is to display it in a sandboxed iframe with JS off. If that content has hyperlinks in it, what this ensures is that if the user clicks on a link, that new tab has scripts disabled, which on the modern web just breaks the linked-to site. In short, developers can't use sandboxed iframes in these kinds of situations, which to my mind are exactly the kind of situations for which they were designed.

I'm also missing the security argument. If JS is off, it means the only way that link would be clicked is if a user clicked it. So what's the security problem?

### ba...@gmail.com (2016-01-08)

To clarify, I'm not disputing the spec interpretation, just that it makes this feature almost useless and confusing as hell to users if it is used.

### bz...@mit.edu (2016-01-09)

> So what's the security problem?

The security problem is that you loaded this thing with script off, but it can just link to itself, and if the user clicks it and the result is not sandboxed, suddenly its running script.  Which is what you were trying to avoid in the first place.

### bz...@mit.edu (2016-01-09)

But note that a sandbox flag is being added to allow you to opt in to not sandboxing popups opened from the sandboxed content.  As long as you realize that this means on user click that sandboxed content can run arbitrary script (so it's not really suitable for user content hosted on your site, unless you really are OK with that content running arbitrary script).

### mk...@chromium.org (2016-01-09)

I'll take a look on Monday, Boris. Thanks for the report. Just for clarity, do you see working script _only_ on `www.google.com`? Or do you see it on any page that's loaded? I'd be pretty surprised if we were special-casing that page anywhere in Blink. (Nasko, are we doing any out-of-process experiments on `google.com`?)

bart.c.butler: As Boris noted, `allow-popups-to-escape-sandbox` (https://html.spec.whatwg.org/#attr-iframe-sandbox-allow-popups-to-escape-sandbox) is potentially what you're looking for. That's shipping in Chrome today. I'm not sure about its status in other browsers.

### bz...@mit.edu (2016-01-09)

> Just for clarity, do you see working script _only_ on `www.google.com`?

Of the pages I've tested so far, yes.  I haven't tried all possible URLs, obviously, but I don't get working script on gmail, web.mit.edu, or a few other pages I've tried.

### mk...@chromium.org (2016-01-11)

Boris: I haven't yet replicated the results you've produced. `https://www.google.com/` is sending me an `X-Frame-Options: SAMEORIGIN` header, which prevents framing it, and the first page I found that didn't (`https://www.google.com/intl/en/policies/privacy/?fg=1`) seems to correctly block script. This is the HTML I'm using:

```
    <iframe src="https://www.google.com/intl/en/policies/privacy/?fg=1" sandbox>
    </iframe>
```

Could you help me reproduce the results you've found?

### mk...@chromium.org (2016-01-11)

Ah, I misunderstood. You're talking about the popup. Sorry. I can reproduce the error you're talking about using the following code in tip-of-tree Chromium:

```
    <meta http-equiv="Content-Security-Policy"
          content="sandbox allow-popups allow-same-origin">                                      

    <a href="https://google.com/" target="_blank">Google!</a>
```

That's a regression I don't understand, and we should fix it. Filed https://crbug.com/576204

### al...@chromium.org (2016-01-11)

I gave an update on https://crbug.com/chromium/576204, but basically this is indeed due to google.com ending up in a different process, and we don't support inheriting sandbox flags for cross-process popups yet.  This should be fixed by https://crbug.com/chromium/483584, which I'm currently working on.

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/393401?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080032)*
