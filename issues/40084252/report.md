# Chrome For Android Address Bar Spoofing Issue Due To Mishandling Of RTL Characters

| Field | Value |
|-------|-------|
| **Issue ID** | [40084252](https://issues.chromium.org/issues/40084252) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>Omnibox, UI>Internationalization>RTL |
| **Platforms** | Android |
| **Reporter** | rb...@gmail.com |
| **Assignee** | mg...@chromium.org |
| **Created** | 2016-05-06 |
| **Bounty** | $3,000.00 |

## Description

**Device name:**

Browser: Chrome For Android  

Version: 49.0.2623.91  

Phone: Nexus Phone  

**OS:** Android Lollipop

Vulnerability Details:

Due to mishandling of Unicode (RTL characters) such as U+7000, u+8000 etc combined with an IP Address it is possible to spoof  

a URL on Google Chrome. Simply placing these characters in "Filepath" followed by the URL you wish to spoof such as Google.com, the URL provided in file path is shifted towards host name. In order to make the attack more realistic unicode version of padlock can be used in order to demonstrate the presence of SSL.

Reproduction Case:

i) Visit - <http://jsbin.com/vexocufalu/>, <http://jsbin.com/dihujobumi> and click the hyperlink.

ii) You would notice that the page is hosted on 182.176.65.7, However the address bar is pointing towards google.com

The same POC was tested against Chrome For Desktop machine and the POC did not work.

Screenshots are attached as an evidence.

## Attachments

- [chromefordesktop.png](attachments/chromefordesktop.png) (image/png, 17.0 KB)
- [ChromeForAndroid.png](attachments/ChromeForAndroid.png) (image/png, 85.2 KB)
- [unnamed.png](attachments/unnamed.png) (image/png, 51.9 KB)
- [ltr-suggestions.png](attachments/ltr-suggestions.png) (image/png, 98.8 KB)
- [rtl-suggestions.png](attachments/rtl-suggestions.png) (image/png, 104.6 KB)
- [rtl-keyboard-cursor.png](attachments/rtl-keyboard-cursor.png) (image/png, 110.0 KB)
- [bidi-omnibox-english.mp4](attachments/bidi-omnibox-english.mp4) (application/octet-stream, 2.3 MB)
- [bidi-omnibox-hebrew.mp4](attachments/bidi-omnibox-hebrew.mp4) (application/octet-stream, 2.4 MB)

## Timeline

### rb...@gmail.com (2016-05-09)

[Comment Deleted]

### el...@chromium.org (2016-05-16)

[Empty comment from Monorail migration]

[Monorail components: Security>UX UI>Browser>Omnibox]

### mb...@chromium.org (2016-05-16)

[Empty comment from Monorail migration]

### mb...@chromium.org (2016-05-16)

I actually haven't been able to reproduce this in Chrome 50 on M, but applying labels based on the screenshots in the initial report.

mgiuca: You've handled some similar RTL issues in the past. Would you mind taking a look or helping to find an owner for this?

### mg...@chromium.org (2016-05-17)

The links seem to be in a state of expiring which is bad for reproducibility. I'm not sure why jsbin was necessary here; the repro is just the following two URLs:

http://182.176.65.7/%EF%B9%B0http://google.com/test
http://182.176.65.7/%EF%B9%B0%F0%9F%94%92https://google.com/test

This looks like the same root bug as https://crbug.com/chromium/351639, but I'll take a closer look. (I am having trouble reproducing this on Desktop and Android tablet, but I was able to on Android phone so I'm not sure what the difference is.)

### mg...@chromium.org (2016-05-17)

Also I can't repro the %F0%9F%94%92 (U+1F512: LOCK) part of the bug at all (https://crbug.com/chromium/495934). We fixed this in r335870 (Chrome 45) so I'm not sure why this would showing as a lock character in 49. None of the above screenshots, nor any of my devices, show a lock character in the URL.

### mg...@chromium.org (2016-05-17)

%EF%B9%B0 is U+FE70 ARABIC FATHATAN ISOLATED FORM, so it counts as a right-to-left Arabic character.

Looks like this is actually the much simpler case of https://crbug.com/chromium/495933 (which is combining a RTL character with an IP address). This was fixed in r334537 in Views but apparently not in Android. We can fix this without having a full fix for https://crbug.com/chromium/351639.

I'll keep this issue open since it's a separate case on Android. At this point, not considering the padlock character (since no repro found for that).

### mg...@chromium.org (2016-05-17)

Oh, and the specific nature of the bug is this:

Going to use the simpler exploit URL from https://crbug.com/chromium/495933:
http://127.0.0.1/%D8%A7/example.org

Because the Omnibox truncates the "http://", the displayed string is:
127.0.0.1/‭ا/example.org [logical order]

Because everything before the "ا" is numeric/punctuation, it does not strongly enforce LTR direction. Therefore, the entire URL is treated as RTL (since the first strong character is RTL), and so the URL is right-aligned and the domain is placed on the right.

So it displays as:
example.org/‭ا‬/127.0.0.1 [physical order]

On Views, in r334537, we made a rule that all URLs are LTR in the top-level context. Looks like we need this same rule on Android.

### mg...@chromium.org (2016-05-17)

I can't repro this exact bug on M52. I believe this was inadvertently fixed in r383200 (Chrome 51) by turning on URL fade behaviour (where the path part of the URL fades away after awhile). This seems to change the URL rendering so that it physically splits up the origin and path parts, rendering them separately, which causes an IP address origin to always be rendered LTR.

This actually resolves quite a lot of the weird mixed LTR/RTL behaviour in URLs but it introduces some discrepancies with the desktop version and there are still some weird cases (e.g., https:// URLs always render LTR; http:// URLs sometimes render RTL). I'd like to try and resolve some of these; we probably should make a rule that the Omnibox on Android always renders LTR no matter what (to match what we have on Desktop).

### mg...@chromium.org (2016-05-17)

#9 Never mind, tab fading was removed again in r389560 (https://crbug.com/chromium/521178), which made this bug come back. Investigating.

### cl...@chromium.org (2016-05-17)

[Empty comment from Monorail migration]

### mg...@chromium.org (2016-05-17)

WIP CL to bring Android in line with Views Omnibox: https://codereview.chromium.org/1988553002

### rb...@gmail.com (2016-05-17)

The bug also validates on Chrome on iOS, Chrome version 50.0.2661.95 (released May 3, 2016)

### mg...@chromium.org (2016-05-17)

Screenshots of the WIP CL:

ltr-suggestions and rtl-suggestions show what the URL bar and suggestions look like with the above URL typed in. You can see in both cases that the URL reads correctly from left to right (although in the RTL case it is right-aligned). There is no confusion about what is the domain. In the suggestions, the blue URL is formatted the same way; the search suggestion and page title are the opposite way (as they are normal text, NOT URLs --- this is by design and matches the Desktop omnibox).

rtl-keyboard-cursor shows a weird thing, which is when you are in RTL mode and typing in RTL characters, the input cursor is split across the beginning and end of the text. This is an artifact of the Android text view, because the text direction is set to LTR, so Android applies this special cursor because you are typing RTL characters (mismatching the TextView's text direction). That seems a little bit of a bad experience but it is *technically* correct and I don't think it's possible to change it and still keep the desired behaviour.

### mg...@chromium.org (2016-05-17)

#13 Thanks for letting us know. I think we'll have to do iOS separately (I'm not the right person to do that).

### mg...@chromium.org (2016-05-17)

FWIW this is also a bug on Mac. (I'm also not the right person to do that, and maybe it will go away on its own with Mac Views.)

### te...@chromium.org (2016-05-18)

What happens for entirely RTL URLs?
http://مركز-التسجيل.السعودية/

As far as I can tell, السعودية is the TLD and مركز-التسجيل is the domain.

I "guess" the above is correct since http:// is ltr and the url-y section is RTL and it would make sense to flow <TLD>.<Host>.



### mg...@chromium.org (2016-05-19)

> What happens for entirely RTL URLs?
> http://مركز-التسجيل.السعودية/
>
> As far as I can tell, السعودية is the TLD and مركز-التسجيل is the domain.

In that case, you're right, السعودية is the TLD and مركز-التسجيل is the SLD. My change won't change the way it's rendered (you'll still see the TLD on the left and the SLD on the right). I am only changing the top-level paragraph direction (from "first strong character" to "always LTR"), which only changes the behaviour for mixed bidirectional URLs.

More generally, we aren't sure what to do about URLs such as the above. I've thought and written at length about this topic: https://docs.google.com/document/d/1J6MaltBnAMGkQ7hCeuRzKaxnfgH9Y6fkk6YD9SVmBp8/edit -- we don't have a clear solution to this but I think something is wrong when a single English word can cause the entire URL order to shift around. The current CL is just about fixing an obvious spoofing issue, and bringing Android in line with the desktop browser (where I made this same fix almost a year ago).

### mg...@chromium.org (2016-05-25)

As discussed on code review, I changed it so that the Omnibox is forced LTR when defocused, but normal bidi when focused. This allows a) the user to type a non-URL search, and b) avoids the split insertion point problem.

I've attached two videos of the full flow: one with the surrounding UI language set to English, and one in Hebrew. Both cases end up working the same way, which is that the text is left-aligned and LTR when defocused (and no spoofing is possible because 127.0.0.1 is always on the left). The text is right-aligned and RTL when focused. It's a bit disconcerting to have it jump from left to right all the time but that's consistent with the current behaviour. We can change that if needed; it's independently controllable from the text direction.

### mg...@chromium.org (2016-05-26)

+rolfe@: Maybe you can look at those videos from the UX perspective and comment on whether it's OK.

I think the proposed fix makes sense from a security perspective (it aligns with our Desktop Omnibox), but not clear on whether the jumping back and forth from left to right is good.

### sh...@chromium.org (2016-05-26)

[Empty comment from Monorail migration]

### ro...@chromium.org (2016-05-31)

I think this looks okay but I'm not a LTR reader and just want to check with someone who is. mgiuca - do you read Hebrew and this makes sense to you? Otherwise I can ask a friend.

Seems like there's not a ton we can do to avoid the jumping considering it's consistent with current behavior. Some sort of slide transition would be nice but I'm sure it would slow things down. We could log a separate polish bug for cross-platform thinking on that possibly.

### mg...@chromium.org (2016-06-01)

#22: I don't read Hebrew but we don't really need Hebrew readers advice here, as we are not changing the rendering of the text itself (other than fixing the special case of non-https IP address, to make it behave like the exceedingly common ASCII domain case). And we have already made the decision to do that on desktop a year ago, this is just syncing up Android.

If you do know someone who is fluent in English and Hebrew, I would like to talk with them about the much scarier unknown https://crbug.com/chromium/351639 (context: https://docs.google.com/document/d/1J6MaltBnAMGkQ7hCeuRzKaxnfgH9Y6fkk6YD9SVmBp8/edit).

We could avoid jumping by changing the alignment rules. For example, we could have a rule that says "any URL whose first strong character is RTL will always be right aligned" (that is, URLs never change alignment when being selected/deselected; URLs requiring this special treatment will always be right-aligned even when their content is rendered LTR). Or, we could just have the jumping behaviour, which means we consistently left-align LTR URLs and right-align RTL URLs.

### ro...@chromium.org (2016-06-01)

Looking at the doc you're talking to roozbeh@, which is the best place to start. Talo@ I believe is fluent in English and Hebrew if you need additional thoughts from general outsiders though.

I rather keep the jumping behavior if it's consistent with other platforms. How would the rule you propose mess us up? Sounds useful to me. Don't meant to derail things but if there's a way to make the experience better as a whole we should totally do that! I'm a bit out of my league when it comes to readability of that though, were we to root to one spot (might mess people up yeah? which is why we jump to begin with?) It's also not a huge deal - I anticipate few users getting into this state.

### mg...@chromium.org (2016-06-02)

#24: The jumping isn't consistent with other platforms. On desktop, the URL bar is always aligned in the user's language direction (if your language is Hebrew, it's always right-aligned no matter what its contents are), which is a lot more sensible to me. For some reason, on Android, it jumps around based on its contents.

After consideration, I think I should do the rule I proposed (otherwise I'll end up left-aligning ALL URLs). Ideally I think Android should follow desktop and set the alignment based on the language, not the text, but that's outside the scope of this bug.

### ro...@chromium.org (2016-06-02)

Works for me! Would you log a bug for Android in general or is there a different process to pursue that?

### mg...@chromium.org (2016-06-03)

[Empty comment from Monorail migration]

### mg...@chromium.org (2016-06-03)

#26: Done: https://crbug.com/chromium/616702.

### bu...@chromium.org (2016-06-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/3bd33fee094e863e5496ac24714c558bd58d28ef

commit 3bd33fee094e863e5496ac24714c558bd58d28ef
Author: mgiuca <mgiuca@chromium.org>
Date: Fri Jun 17 04:53:04 2016

Android omnibox: Force paragraph direction to LTR.

This means that URLs will always be displayed in a left-to-right
context. Right-to-left runs are still rendered as RTL, but will not
cause the whole URL to flip around.

This fixes several spoofing concerns and makes Android's omnibox
consistent with the Views omnibox.

BUG=609680

Review-Url: https://codereview.chromium.org/1988553002
Cr-Commit-Position: refs/heads/master@{#400359}

[modify] https://crrev.com/3bd33fee094e863e5496ac24714c558bd58d28ef/chrome/android/java/src/org/chromium/chrome/browser/omnibox/SuggestionView.java
[modify] https://crrev.com/3bd33fee094e863e5496ac24714c558bd58d28ef/chrome/android/java/src/org/chromium/chrome/browser/omnibox/UrlBar.java


### aw...@chromium.org (2016-06-28)

[Empty comment from Monorail migration]

### rb...@gmail.com (2016-06-28)

Does it qualify for a bounty?

### mg...@chromium.org (2016-06-29)

Thanks for following up. I think it's eligible for a bounty but it isn't my decision. Adding reward-topanel which should put this in the queue.

Some things to consider: This was an already-known and fixed issue on Windows, Linux and Chrome OS. However, we didn't realise it was also a problem on Android (which rbsoulhunder brought to our attention), so I think that qualifies for an additional bounty. We've also been alerted to the fact that this vulnerability exists separately on iOS and Mac (yay for having FOUR separate implementations of the Omnibox) which I will file bugs for, and don't anticipate further bounties for each of those.

Filed https://crbug.com/chromium/624213 and https://crbug.com/chromium/624214 for Mac and iOS, respectively.

### rb...@gmail.com (2016-06-29)

Thanks, 

I am okay with whatever the panel decides.

Regards,

Rafay 

### pa...@chromium.org (2016-06-29)

Note that our sheriffbot automatically picks up fixed security bugs for consideration for the bug bounty, so we would not have missed it. But manually adding reward-topanel is also good. :) And yes I agree this is definitely worth consideration at the rewards panel meeting. Thank you, Rafay! :)

### sh...@chromium.org (2016-06-29)

[Empty comment from Monorail migration]

### ro...@chromium.org (2016-07-05)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-20)

Congratulations!  The panel has chosen a reward of $3,000 for this bug!  A member of our finance team will be in touch shortly.

Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an established charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

### rb...@gmail.com (2016-07-20)

Thank you very much. Please let me know when can i publish the details about android bug specifically? 

### mg...@chromium.org (2016-07-20)

To be sure, you should wait until the Restricted field on this bug disappears (then the bug is public and there is no risk of "early public disclosure"). That should happen when this fix in M53 rolls out to stable, which should happen in September.

In the mean time, as discussed, you may discuss the details of this vulnerability in general, or with regards to the platforms on which it has already been fixed (Windows, Linux, Chrome OS).

### sh...@chromium.org (2016-07-21)

[Empty comment from Monorail migration]

### am...@chromium.org (2016-07-22)

Approved for M53 branch 2785.

### mg...@chromium.org (2016-07-25)

This is bizarre... I don't know why sheriffbot automatically applied Merge-Request-53 here. The only CL in this bug landed before M53 branch point. There is nothing to merge. I will follow up.

### mg...@chromium.org (2016-08-03)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-08-04)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-08-10)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-09-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-05)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### la...@chromium.org (2016-12-09)

Security>UX component is deprecated in favor of the Team-Security-UX label

[Monorail components: -Security>UX]

### lg...@chromium.org (2017-05-03)

[Empty comment from Monorail migration]

[Monorail components: UI>Internationalization>RTL UI>Security>UrlFormatting]

### ro...@chromium.org (2017-05-03)

[Empty comment from Monorail migration]

### pa...@google.com (2017-05-03)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-05-04)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/609680?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: UI>Browser>Omnibox, UI>Internationalization>RTL, UI>Security>UrlFormatting]
[Monorail blocked-on: crbug.com/chromium/495933]
[Monorail mergedwith: crbug.com/chromium/612207, crbug.com/chromium/633638]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084252)*
