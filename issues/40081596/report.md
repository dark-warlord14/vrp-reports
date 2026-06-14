# Security: On Android, it's possible to inject text and icons to the page info bubble using crafted URL fragments

| Field | Value |
|-------|-------|
| **Issue ID** | [40081596](https://issues.chromium.org/issues/40081596) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Platforms** | Android |
| **Reporter** | ju...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2015-03-11 |
| **Bounty** | $500.00 |

## Description

The fragment part of the URL is not escaped in any way when displayed in the page info bubble, meaning that it's possible use it to inject arbitrary text and even emoji icons to a security-critical part of the browser UI. This could be used for phishing, or to convince the user that an HTTPS connection is secure when it actually isn't.

**VERSION**  

Chrome Version: 40.0.2214.109 + stable  

Operating System: Android 4.4.2

**REPRODUCTION CASE**

1. Go to <http://jsfiddle.net/877tqfk4/>
2. Tap on the link
3. Press down on the address bar to open the page info bubble
4. See the injected message and icons

## Attachments

- [Screenshot_2015-03-11-23-35-23.png](attachments/Screenshot_2015-03-11-23-35-23.png) (image/png, 54.7 KB)
- [Screenshot_2015-03-13-17-33-20.png](attachments/Screenshot_2015-03-13-17-33-20.png) (image/png, 103.7 KB)
- [Screenshot_2015-03-13-17-18-17.png](attachments/Screenshot_2015-03-13-17-18-17.png) (image/png, 126.1 KB)
- [Screenshot_2015-04-09-11-45-09.png](attachments/Screenshot_2015-04-09-11-45-09.png) (image/png, 106.6 KB)

## Timeline

### wf...@chromium.org (2015-03-13)

felt can you take a look at this since I know you're working on the page info bubble at the moment.

### fe...@chromium.org (2015-03-13)

tsergeant@, can you please take a look at this as the newly minted owner of PageInfo on Clank? I am treating this as a high-severity security vulnerability.

### ts...@chromium.org (2015-03-13)

It seems to me like part of the problem is that the newline/whitespace characters make it look like the message isn't part of the URL. Stripping or urlencoding these characters might help.  

### fe...@chromium.org (2015-03-13)

[Empty comment from Monorail migration]

### be...@chromium.org (2015-03-13)

+sashab, +tedchoc

The newlines are coming from &nbsp in the url. We should be escaping these (and anything else that might be interpreted) or settup up the UI to not intepret markup (if possible without breaking coloring).

### ju...@gmail.com (2015-03-13)

Look closer, there's a literal non-breaking space in the URL; I only used &nbsp; in the HTML because it was easier for me to type and for you to notice. And the nbsp isn't actually causing the newlines; it's just basic word wrapping. What the nbsp does is prevents the spaces from being collapsed together so that you get two newlines instead of just one. 

### me...@chromium.org (2015-03-13)

[Comment Deleted]

### me...@chromium.org (2015-03-13)

I think we should reconsider the severity for this bug given that an explicit user action is required. The severity guidelines state that an "unusual" interaction should downgrade severity to medium (http://www.chromium.org/developers/severity-guidelines).
That said, felt@ and I have differing opinions about what "unusual" means. My interpretation is that the user interaction requirement prevents the bug from being exploited by driveby web, but there are good counter examples (e.g. a bug allowing a tab to change chrome://settings UI would probably be considered high even if the user had to go visit chrome://settings).

### me...@chromium.org (2015-03-13)

(didn't mean to change the label yet, so I've set it back to high)

### ju...@gmail.com (2015-03-13)

The severity guidelines give an example of an unusual action: "such as terminating a tab's process while in full-screen mode". Are you saying that opening the page info bubble is comparable to that? No other user action is required here. 

### me...@chromium.org (2015-03-13)

The requirement to tap the omnibox to see the connection info prevents the bug from being exploited on a mass scale, and the historical interpretation of this has been to consider the bug as medium severity (example: crbug.com/346135).

### ts...@chromium.org (2015-03-13)

In M40, this only requires one action (opening the page info popup). In M42 beta (possibly in M41, I don't have a build handy), it requires two actions (opening the page info popup and expanding the URL).

### ts...@chromium.org (2015-03-14)

Digging into this a bit, there's nothing really fancy about the internals of how the URL is displayed. The url string is essentially untouched before it gets colored, and there's not a lot we can do from the Android TextView side to change how it is displayed.

So, I think the best solution may be to simply replace all spaces with %20. Spaces don't really have any place in a URL anyway, so it's not unexpected for users to see them occasionally. It fixes this attack by pushing the message down and making it much more difficult to read. 

Another solution is to collapse down whitespace into a single space when we display the URL. This kind of works, but still clearly displays the text. 

Does anyone have any ideas about the potential security implications of these ideas?

### ju...@gmail.com (2015-03-14)

> The requirement to tap the omnibox to see the connection info prevents the bug from being exploited on a mass scale

I'm sure you've all seen those 'add this to homescreen' bubbles that have gotten so popular in mobile web apps lately. Using something similar themed to look like a part of the browser UI it would be fairly easy to trick someone into opening the page info bubble. 

> it requires two actions (opening the page info popup and expanding the URL).

I did some testing, and even in M42 you still have two rows at your disposal. You can still inject a message like 'Error! Expand for details.' 

Re: potential fixes, I think the best solution would be to disable wrapping and constrain the URL to a single line, possibly with horizontal scrolling. That way you wouldn't have to make any changes to the actual URL. 

### lg...@chromium.org (2015-03-14)

Any reason we couldn't show the same URL (with URL encoding for anything but a subset of ASCII characters) that we'd show on desktop?

### ju...@gmail.com (2015-03-14)

@15 Where on the desktop? I don't think any characters in the fragment are escaped anywhere. 

### ju...@gmail.com (2015-03-14)

Related issue: In M40, a URL with a space in it doesn't get colored correctly. Try "https://example.com/" vs "https://example.com/# .". This is fixed in M42, though. 

### te...@chromium.org (2015-03-16)

@#15, desktop only shows the host.  I don't know why it's different on Android, but I find this screen to be one of the few places where you have the potential to easily see the full URL at once (without needing to scroll the omnibox).

Desktop code for what gets shown:
https://code.google.com/p/chromium/codesearch#chromium/src/chrome/browser/ui/website_settings/website_settings.cc&q=website_settings.cc&sq=package:chromium&l=749

@#13 - We should probably use whatever logic is done when showing the URL in the omnibox as I suspect it does what we want here (ToolbarModelImpl::GetFormattedURL).  Probably can just use net::FormatUrl directly if we do not need all the fancy logic contained in that model's code.


### ts...@chromium.org (2015-03-16)

@#18 - I'm not sure how this will help? The Omnibox still contains all of the spacing and phishing text, you just can't see it because it's all on a single line.

### te...@chromium.org (2015-03-16)

Well, well, well, you are indeed absolutely right.  I expected it to be escaped in the omnibox in some manner, but it isn't.  Yeah, no help there...sorry for the noise.

### ts...@chromium.org (2015-03-18)

@ #14 - I don't think we can restrict the URL to be displayed on a single line as this will obscure the origin in some cases (there's some special logic in the page info popup to make sure the entire origin is always visible).

Thinking more about my idea from #13, replacing only space characters with %20s isn't going to work because there are a whole range of other Unicode whitespace characters which can do the job (http://www.unicode.org/charts/PDF/U2000.pdf).

So, I'm leaning more towards a version of lgarron@'s suggestion from #15

### ju...@gmail.com (2015-03-19)

@#21 - Suggestion from #15, as in 'escape everything' or 'show the same thing as on the desktop'?

I think simply removing the URL fragment entirely (but leaving everything else as-is) could also be an option. 

### ts...@chromium.org (2015-03-19)

@#22 - Specifically, escaping illegal characters in the url. There's a CL for this at crrev.com/1011383005. 

I think that with a co-operating server, the attack doesn't need the use the fragment using the path or query component, so we'd need hide everything but the origin to avoid this. I like having a place where the entire URL is shown, so escaping is still my preferred solution.

### ju...@gmail.com (2015-03-19)

Actually, shouldn't this be fixed at the level of not allowing illegal characters in URLs in the first place, instead of just escaping them in the popup? RFC 3986 is very explicit on what should be allowed, and the JavaScript location API already seems to be doing some escaping; it's just that the fragment should be automatically escaped when *navigating* to a page.

URL fragments containing weird characters could also be a risk wrt DOM XSS. 

### ts...@chromium.org (2015-03-20)

Okay, I've looked into this some more...

Chrome percent-encodes everything *except* the URL fragment, which stays as UTF-8 (see url/gurl.h:81). The URL spec (https://url.spec.whatwg.org/#url-writing) agrees with this. (And, indeed, this is what happens with the Javascript location API and everything else in Chrome). As a result, it's not a good idea to start encoding the fragment here.

### ts...@chromium.org (2015-03-20)

I think the best solution might be to percent encode the fragment that we display, but have the copy button copy the original URL (which will have the original unencoded fragment). This will obscure the phishing message while ensuring that the URL that is copied out is still valid. felt@, do you think that this is an acceptable solution?

### ju...@gmail.com (2015-03-20)

> Chrome percent-encodes everything *except* the URL fragment, which stays as UTF-8

Okay, this is what I originally thought. I guess IETF and WHATWG don't quite agree on what a URL should look like. This being the case, though, I think my suggestion in #22 would be the best option: just don't display the fragment.

To me, adding an extra layer of encoding just for displaying the URL doesn't sound right. After all, it's not the original URL anymore when you make changes to it. It could also turn out to be very confusing to developers who are relying on using some special characters (say, the pipe symbol "|") in the fragment.

> there's some special logic in the page info popup to make sure the entire origin is always visible

Another option that comes to mind is changing this logic slightly: make everything after the first line collapse like long URLs do in M41 and M42, except for the origin part. Currently the limit seems to be at two lines. As an additional precaution, you could start the collapsing at the first unicode code point outside a certain range, so that you wouldn't show, for example, emoji without the user explicitly expanding the URL.

### be...@chromium.org (2015-03-24)

felt: do you have an opinion?

I think consistency is important, so I'd suggest we always show the fragment and just encode it to hide spaces and any other characters we deem unsafe. The copy should copy the fragment without encoding.

### bu...@chromium.org (2015-03-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/b1130cfc5dca2d5f01edafd7d50f795f391ab904

commit b1130cfc5dca2d5f01edafd7d50f795f391ab904
Author: tsergeant <tsergeant@chromium.org>
Date: Thu Mar 26 01:56:54 2015

Percent-encode illegal characters in Android page info popup URL

This prevents whitespace and non-ASCII characters from being displayed in
the url, stopping attacks where a carefully crafted URL can be used
to display a message in the popup.

BUG=466351

Review URL: https://codereview.chromium.org/1011383005

Cr-Commit-Position: refs/heads/master@{#322296}

[modify] http://crrev.com/b1130cfc5dca2d5f01edafd7d50f795f391ab904/chrome/android/java/src/org/chromium/chrome/browser/WebsiteSettingsPopup.java
[add] http://crrev.com/b1130cfc5dca2d5f01edafd7d50f795f391ab904/chrome/android/javatests/src/org/chromium/chrome/browser/WebsiteSettingsPopupTest.java


### ju...@gmail.com (2015-03-26)

Sorry, I totally missed the code review. The patch is still missing some whitespace characters. Here's a nice list: https://www.cs.tut.fi/~jkorpela/chars/spaces.html

### ts...@chromium.org (2015-04-02)

I've filed a follow-up CL at http://crrev.com/1056743002/. This one uses Character.isSpaceChar(), which matches all of the characters in the "Separator, Space" category (http://www.fileformat.info/info/unicode/category/Zs/list.htm). This is pretty much just the list from https://www.cs.tut.fi/~jkorpela/chars/spaces.html, excluding any zero-space characters.

### ju...@gmail.com (2015-04-02)

Still missing at least U+2420 and U+2422. They're listed at the bottom of Korpela's spaces document as "visible spaces", but at least on my Android they're rendered as just white space.

And I don't even know if that's everything. 

### ju...@gmail.com (2015-04-02)

Actually, now that I think about it, blacklisting is probably a pretty bad idea in the first place, considering the sheer number of unicode characters and all the inconsistencies in rendering them. 

### fe...@chromium.org (2015-04-02)

[Empty comment from Monorail migration]

### pa...@chromium.org (2015-04-02)

I'm imagining a normalizing map function, in which the domain is distinct Unicode character classes, and the image is a single good representation. E.g.:

Character normalizeCharacter(Character c) {
    if (Character.isSpaceChar(c)) return " ";
    if (Character.isISOControl(c)) return "";
    // ... And so on
}

Additionally, we should think about surrogate pairs and combining characters. I suspect there is some function in some Unicode library that already normalizes all such sequences into a single Unicode code point (which we could then subject to |normalizeCharacter|)? I don't know Unicode APIs as well as I should, and java.lang.Character seems strangely impoverished on first glance...

Additionally some more, we should think about what parts of the URL are appropriate to show at all in various contexts. E.g. in the screenshot in the original bug, one could argue that the fragment shouldn't be shown at all? Maybe. Maybe not. Likely depends on context. (Obviously, the COPY URL button must always copy the exact bytes of the URL, without transformation. I am speaking only of display.)

### ju...@gmail.com (2015-04-03)

> one could argue that the fragment shouldn't be shown at all

This. See #22.

tedchoc@ argued that the page info bubble is the only place where you can easily see the full URL, but I think that's a different issue entirely; it's not what the page info bubble is there for anyway. Instead, the omnibox should be made easier to read, for example by making it possible to scroll the URL horizontally even when it's not focused.

But like I said, that's outside the scope of this ticket. 

### cl...@chromium.org (2015-04-03)

[Empty comment from Monorail migration]

### be...@chromium.org (2015-04-07)

The two approaches we have now are (1) escape out spaces, but this is hard as we have to catch them all or (2) don't show the fragment, but that is bad as we're hiding information that we would ideally show.

I wonder if there is a different approach. The problem is basically that it isn't clear that the url / fragment is not chrome UI. It's a weird form of content that users might think is actually chrome.

Could we leave it unescaped / still show it but make it clearer that this is part of the URL? E.g. we could show a box around the URL, or use a different colored background, or put a title or something. We'd only need to do this when the URL is expanded.

### ti...@google.com (2015-04-08)

[Empty comment from Monorail migration]

### ts...@chromium.org (2015-04-09)

How about limiting the amount of fragment which we show: If the URL has a long fragment, truncate it at the end of the line *after* the # symbol -- meaning that there's at most 2 lines of fragment visible. This is enough space to show the entire fragment for lots of legitimate use-cases, but not enough space to inject a message which looks like it's separate from the URL.

### be...@chromium.org (2015-04-09)

I just realised we have no UX super star on this bug to help us!

+rolfe to correct the omission.

Rebecca, any ideas? Sorry about the long thread...

### ro...@chromium.org (2015-04-10)

I could swear there was a bug somewhere sashab@ had going where we discussed having an ellipsis at the second line of any long URLs but I can't find it now. I think in the end we decided it was really hard to break the URLs appropriately (via some Android standard) so for the time being we would show everything. But I am fully in support of a hard stop after some minimum amount, even if the site isn't injecting its own mumbo jumbo (because the legitimate jumbo can be mumbo enough!)

Truncating after # works for me. Thanks!

### be...@chromium.org (2015-04-13)

rolfe: your memory is correct, you're not imagining things :)

We do put an elipsis at the end of the first line (I think it is the first) if the URL is too long to fit. The full URL is shown if the user clicks on this (or long clicks or something).

### ju...@gmail.com (2015-04-13)

benwells@: second line, actually. 

### ro...@chromium.org (2015-04-13)

Ok great. Basically we'd 1) truncate after #, and 2) disable the click to expand the full link. I'm OK with that if security is, as the origin is the key info here.

### fe...@chromium.org (2015-04-13)

I'm OK with it, as the origin is the only thing security-relevant. As long as the origin doesn't get truncated, it's fine.

### ts...@chromium.org (2015-04-15)

I confirmed with rolfe@ off-thread that the solution from #40 of truncating expanded URLs if they have a long fragment is suitable from a UX perspective. This doesn't affect the original behaviour of how the origin is displayed.

There's a CL up for this at https://codereview.chromium.org/1077483002/

### sa...@chromium.org (2015-04-15)

[Empty comment from Monorail migration]

### bu...@chromium.org (2015-04-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/5bf8a2dccf4777c5f065d918d1d9a2bbaa013f9f

commit 5bf8a2dccf4777c5f065d918d1d9a2bbaa013f9f
Author: tsergeant <tsergeant@chromium.org>
Date: Thu Apr 16 00:36:17 2015

Truncate long URL fragments in Android page info popup

This replaces percent-encoding whitespace as a method to combat the use
of crafted URL fragments to inject messages into the page info popup. By
truncating the URL so that at most two lines of the fragment are shown,
we prevent lengthy messages from being injected while minimising the
effect on most URLs.

BUG=466351

Review URL: https://codereview.chromium.org/1077483002

Cr-Commit-Position: refs/heads/master@{#325358}

[modify] http://crrev.com/5bf8a2dccf4777c5f065d918d1d9a2bbaa013f9f/chrome/android/java/src/org/chromium/chrome/browser/WebsiteSettingsPopup.java
[delete] http://crrev.com/151364e2372c690bd50a24c89454e3255fe95d40/chrome/android/javatests/src/org/chromium/chrome/browser/WebsiteSettingsPopupTest.java


### ts...@chromium.org (2015-04-20)

Marking this as fixed after that follow-up patch.

felt@, any opinion on merging this? The original half-working patch (#29) is in M43, the follow-up patch (#49) is not. Is it sufficient to merge #49 to M43?

### cl...@chromium.org (2015-04-20)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### fe...@chromium.org (2015-04-21)

Per earlier discussion with meacer I'm downgrading this to a Medium, but it should still be merged to both 42 and 43. Do you see any conflicts that would make this difficult?

### ti...@google.com (2015-04-21)

Merging to M43 SGTM though I would hesitate in requesting a merge to M42. M42 is already on stable channel and the TPMs that manage chrome milestones usually steer clear of any non-critical UI changes in patch releases. Combined with the security downgrade to medium, it's not likely this issue will be accepted into M42 if you request a merge. 

That said, if you *really* want this in M42, there's no harm in asking. Just be prepared for a "no" :)

(also bumping down to medium based on #52)

### fe...@chromium.org (2015-04-21)

I'd like to go ahead and ask for a merge to 42 anyway. It's a high-ish medium. It lets an attacker control what appears in trusted browser UI. The fix looks fairly low-risk, although I'll let Tim speak to that when he requests the merge.

### ti...@google.com (2015-04-21)

No worries - let's get this into M43 first.

Merge-Requested for M43 (branch 2357). Note that the only CL requiring merge is #49.

### ts...@chromium.org (2015-04-21)

felt@: Sounds good to me

### la...@google.com (2015-04-21)

Approved for M43 (branch: 2357)

### la...@google.com (2015-04-21)

[Automated comment] Request affecting a post-stable build (M42), manual review required.

### bu...@chromium.org (2015-04-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/5aba40cebe8c915c114f3d6ffd10a0c29f0f77d8

commit 5aba40cebe8c915c114f3d6ffd10a0c29f0f77d8
Author: Ben Wells <benwells@chromium.org>
Date: Tue Apr 21 04:00:34 2015

Truncate long URL fragments in Android page info popup

This replaces percent-encoding whitespace as a method to combat the use
of crafted URL fragments to inject messages into the page info popup. By
truncating the URL so that at most two lines of the fragment are shown,
we prevent lengthy messages from being injected while minimising the
effect on most URLs.

BUG=466351

Review URL: https://codereview.chromium.org/1077483002

Merged from trunk.
TBR=tedchoc@chromium.org

Cr-Commit-Position: refs/heads/master@{#325358}
(cherry picked from commit 5bf8a2dccf4777c5f065d918d1d9a2bbaa013f9f)

Review URL: https://codereview.chromium.org/1061533006

Cr-Commit-Position: refs/branch-heads/2357@{#175}
Cr-Branched-From: 59d4494849b405682265ed5d3f5164573b9a939b-refs/heads/master@{#323860}

[modify] http://crrev.com/5aba40cebe8c915c114f3d6ffd10a0c29f0f77d8/chrome/android/java/src/org/chromium/chrome/browser/WebsiteSettingsPopup.java
[delete] http://crrev.com/2fb57e2b1cb54c8bcbb33936ec9f3c5552cf0376/chrome/android/javatests/src/org/chromium/chrome/browser/WebsiteSettingsPopupTest.java


### ti...@google.com (2015-04-21)

@kerz: what's the likelihood that you'll take this for M42?

### ke...@google.com (2015-04-22)

I appreciate the concerns here, however we're done for Android unless it's a critical issue, and we would only take those at this point, so I have to say it waits for 43. Sorry :\

### bu...@chromium.org (2015-04-24)

The following revision refers to this bug:
  https://chrome-internal.googlesource.com/bling/chromium.git/+/5aba40cebe8c915c114f3d6ffd10a0c29f0f77d8

commit 5aba40cebe8c915c114f3d6ffd10a0c29f0f77d8
Author: Ben Wells <benwells@chromium.org>
Date: Tue Apr 21 04:00:34 2015


### ti...@google.com (2015-04-27)

[Empty comment from Monorail migration]

### ju...@gmail.com (2015-05-04)

I guess M-43 is due soon? Does this issue qualify for the vulnerability reward program?

### fe...@chromium.org (2015-05-04)

[Empty comment from Monorail migration]

### ti...@google.com (2015-05-19)

Congratulations - $500 for this report!

Someone from our payments team should be in contact to collect your details in the next two weeks.

We'll credit you in our release notes as "juhonurm" - please let me know if you'd prefer to use a different name.

I'll also assign a CVE for this bug provide it for your reference shortly. Good times.


*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an established charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### ju...@gmail.com (2015-05-19)

Hey, great. Please use my full name, Juho Nurminen.

### ju...@gmail.com (2015-06-14)

Hey, regarding the reward--it's been quite a while but nobody from payments has contacted me yet. They should have my details already from before, but I don't see anything on my bank account either. Could you check what's up?

### ti...@google.com (2015-06-14)

Thanks for letting me know Juho - I'll chase it down this week.

### ju...@gmail.com (2015-06-25)

Sorry to bug you like this, but I still haven't heard from anyone. Did you find out what the holdup is? 

### ti...@google.com (2015-06-25)

I did - the holdup was actually me incorrectly submitting the payment paperwork. I just confirmed that it's gone through with high priority, so you should receive an email within 2 days. Contact me at timwillis@ if it hasn't (or just update this issue).

### ti...@google.com (2015-07-24)

Processing via our e-payment system can take up to two weeks, but the reward should be on its way to you. Thanks again for your help!

### cl...@chromium.org (2015-07-27)

Bulk update: removing view restriction from closed bugs.

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### la...@chromium.org (2016-12-09)

Security>UX component is deprecated in favor of the Team-Security-UX label

[Monorail components: -Security>UX]

### is...@google.com (2016-12-09)

This issue was migrated from crbug.com/chromium/466351?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081596)*
