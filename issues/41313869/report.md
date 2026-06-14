# RTL URLs show up in the wrong order in the Omnibox suggestions on iOS

| Field | Value |
|-------|-------|
| **Issue ID** | [41313869](https://issues.chromium.org/issues/41313869) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>Omnibox |
| **Platforms** | iOS |
| **Reporter** | mg...@chromium.org |
| **Assignee** | jd...@chromium.org |
| **Created** | 2017-04-19 |
| **Bounty** | $500.00 |

## Description

Chrome Version: 57.0.2987.137  

OS: IOS 10.2.1

Reported on <https://crbug.com/708981#c19> by user rayyanh12.

**What steps will reproduce the problem?**  

I'm not an iOS user so I'm just guessing how to repro this from the screenshot.  

**(1)** Copy the following URL: 127.0.0.1/ا/<http://attack.com>  

**(2)** Open the Omnibox suggestions, maybe try typing "127.0.0.1".

The idea is to get that URL to show up as a suggested result "Link that you copied". May also try visiting that URL and having it in your history, then searching for it.

**What is the expected result?**  

The BLUE URL shown in the suggestions should read:  

‪127.0.0.1/ا/[http://attack.com‬](http://attack.com%E2%80%AC)

(the IP address part should be on the left).

Note: The black text there is plain text (not a URL) so we shouldn't mess with it (it should continue to show "<http://attack.com>" on the left).

**What happens instead?**  

See screenshot. The BLUE URL shows the text flipped:  

‫127.0.0.1/ا/[http://attack.com‬](http://attack.com%E2%80%AC)

Rationale:  

On contexts that we \*know\* are URLs (such as the blue suggested text in those suggestion rows), we should apply the correct ordering (i.e., it should behave as if there is a U+200E LRM at the beginning of the URL). This should be as simple as literally adding a U+200E LRM character to the front of those blue URLs, which we already do in the Omnibox proper for URLs.

I'm marking this as security, because it involves URL spoofing. Note: This is just a precaution, as I don't think this has any real security impact (the blue suggestion text is not a security surface that users are expected to base decisions on -- they should always look in the Omnibox proper \*after\* navigation to decide whether they trust a site).

See <https://crbug.com/624214> for how this was fixed in the Omnibox on iOS.

## Attachments

- [IMG_7871.PNG](attachments/IMG_7871.PNG) (image/png, 111.4 KB)
- [Current situation.jpg](attachments/Current situation.jpg) (image/jpeg, 35.3 KB)
- [Suggested Fixture - google chrome (Windows 10).png](attachments/Suggested Fixture - google chrome (Windows 10).png) (image/png, 8.1 KB)
- [IMG_7885.JPG](attachments/IMG_7885.JPG) (image/jpeg, 97.9 KB)
- [Screen Shot 2017-05-01 at 2.56.38 PM.png](attachments/Screen Shot 2017-05-01 at 2.56.38 PM.png) (image/png, 64.1 KB)
- [Screen Shot 2017-05-01 at 2.33.03 PM.png](attachments/Screen Shot 2017-05-01 at 2.33.03 PM.png) (image/png, 48.4 KB)
- [PoC.mp4](attachments/PoC.mp4) (video/mp4, 1.1 MB)

## Timeline

### me...@chromium.org (2017-04-20)

[Empty comment from Monorail migration]

### mg...@chromium.org (2017-04-20)

meacer: I don't mean to have this unnecessarily show up in the security queue. Feel free to remove the security tags if you think the URLs in the suggestions are not security-identifiers.

### ra...@gmail.com (2017-04-20)

Since both, Plain text and URL are all working in the same security indicator (Omni Box) Don't you think we should actually look into this? Specifically, when this type of plain text appears in the address bar, we should rather show the ip address  first? Because obviously, user will be convinced what he has been shown in the omni box? 

I'm saying this because, the Omnibox shows the correct URL (Ip address first) but only after executing the URL. Before executing it, It shows the Spoofed URL and even after executing it, when user click on the address bar (For instance, to edit the URL), it again shows the spoofed URL which can make the user confused. Most probably, the user will be convinced that the spoofed URL is the real URL since this bug is every where eg: Facebook (great source of traffic) and also google chrome is showing the spoofed URL as the correct URL (I just described how). In this way, the attacker is already have been successful in making the user go to this link (which is spoofed URL) - Which can have malicious script code running. Moreover, I can replace attack.com with google.com to make the user more convinced. In this way, I don't need to find Xss vulnerability on google, but instead of using this behavior, I can enjoy xss vulnerability on every google URL.    


My suggested fixture for this is: If you don't want to change the way it displays the URL as a plain text ("http://attack.com" on the left) - Then because Omni box is mostly used for the URL instead of search, I think we should give the priority to show the BLUE URL first instead of plain text - In this way, The users will be more cautioned. Moreover, The OmniBox should show the logical order (Ip address first) and the plain text should show in the drop down suggestions (which is already showing but here, I'm talking about omni box) - JUST LIKE I've attached the screenshot of chrome in windows 


I’ve attached two screenshots, which shows the bug (Current situation of the mobile browsers) and the fixture of the bug: In google chrome (Windows 10) The omni box shows the logical order of the URL (Ip address first). Plus, It is giving more priority to  the URL instead of plain search. In this way, I'm more likely to say that yes I'm visiting the IP address instead of attack.com, Therefore, same implementation should be appiled to mobile browsers -

After describing the details and impact of this bug, I think this should be considered as the security bug. Hope you get it. Thanks!


### mg...@chromium.org (2017-04-21)

#3: Those screenshots are not comparable: in the iOS one, there is only one row of suggestion (just a direct navigation to the URL), and no Google Search option. Not sure why that is, but there you go. Each suggestion on iOS has two lines -- the black text which is the page title (in this case, the page title is the same as the URL; see https://crbug.com/chromium/708981) and the blue text which is the URL.

In the Windows one, there are two suggestions -- the URL and the Google Search. Normally in Windows, the page title shows up in grey to the left of the URL but I guess your machine hasn't cached the page title yet so it shows nothing.

Anyway, the correct solution is to change the blue URL text to have the 127.0.0.1 on the left. That is, insert a U+200E LRM character at the start of the URL, as I suggested in the initial report.

### ra...@gmail.com (2017-04-21)

[Comment Deleted]

### ra...@gmail.com (2017-04-21)

I know the ss are not comparable.. I was just trying to give you guys the idea of the fixture.. but anyway, If I’m not wrong you yourself said that users should see the Omni Box whether they are going on trusted URL or not, Right? But As you can see in the screenshot 
(Current Situation) that Omni box it self is showing the Spoofed URL. Can you decide by looking at the screenshot that you’re going on ipadress instead of attack.com? This is what I’m saying SINCE THEN regarding the one of the fixtures that Omni Box should show the logical order of URL (ip address first). Anyway, I think the bug has been patched because now, I cannot reproduce the bug shown in the (current situation) screenshot. Now, The omni box is showing the logical order of the URL. (Screenshot attached) Thanks!

### jd...@chromium.org (2017-04-21)

I'll take a look at this. There are a couple different situations where we show something that we know is a URL in the suggestions list. In those cases, I agree that we should clearly apply the same layout as the omnibox does when showing the URL current page.

### eu...@chromium.org (2017-04-21)

[Empty comment from Monorail migration]

### jd...@chromium.org (2017-05-02)

I have a fix in https://codereview.chromium.org/2854893002.

Attached are two screenshots showing the result. In both, 127.0.0.1/ا/http://attack.com is laid out LTR when it's treated as a URL (blue text). The first is a clipboard URL suggestion. The second is a what-you-typed URL suggestion. In this one, the first line of the first suggestion is still RTL because it's treated as the title, not a URL and the text of the second suggestion is RTL because that will not navigate to the offending URL, it will execute a query for that text.

### ra...@gmail.com (2017-05-02)

[Comment Deleted]

### ra...@gmail.com (2017-05-02)

[Comment Deleted]

### ra...@gmail.com (2017-05-02)

Hi, There's actually one more thing to be fixed; When you try to hide the URL with 1 arabic letter, the omni box does show the logical order when clicked on it to edit the URL, however, when you try to hide the URL with multiple arabic letter, The omni box shows the spoofed URL when clicked on it which can make the user confused, However, The user might think that its the technical bug (that it shows the ip address first) upon executing the URL, since, from the user being redirected to, the editing of URL, it shows the evil.com as the URL. Note that this problem doesn't arises when URL is being tried to hidden with 1 arabic letter, therefore, same behaviour should be applied to the URL when multiple arabic letters are there.

### ra...@gmail.com (2017-05-02)

from the user being redirected, to, the editing of URL*

### mg...@chromium.org (2017-05-03)

#12: That bug is totally unrelated to this one (which is about the Omnibox suggestions view). I have filed a new bug and given some commentary there: https://crbug.com/chromium/717868. Please file separate bugs for separate issues. Otherwise it's too hard to keep track of them.

### jd...@chromium.org (2017-05-03)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-05-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/902fe23a4f224a6b8b17769670943fd5f28e2f3b

commit 902fe23a4f224a6b8b17769670943fd5f28e2f3b
Author: jdonnelly <jdonnelly@chromium.org>
Date: Wed May 03 17:50:47 2017

Force URLs in omnibox suggestions to layout LTR.

This treats URLs the same way they are treated in the omnibox text field:
https://cs.chromium.org/chromium/src/ios/chrome/browser/ui/omnibox/omnibox_text_field_ios.mm?l=528&rcl=5bd9e2fd296b774e34d04cddfb09893525a79c04

BUG=712919

Review-Url: https://codereview.chromium.org/2854893002
Cr-Commit-Position: refs/heads/master@{#469029}

[modify] https://crrev.com/902fe23a4f224a6b8b17769670943fd5f28e2f3b/ios/chrome/browser/ui/omnibox/omnibox_popup_material_view_controller.mm
[modify] https://crrev.com/902fe23a4f224a6b8b17769670943fd5f28e2f3b/ios/chrome/browser/ui/omnibox/truncating_attributed_label.h
[modify] https://crrev.com/902fe23a4f224a6b8b17769670943fd5f28e2f3b/ios/chrome/browser/ui/omnibox/truncating_attributed_label.mm


### jd...@chromium.org (2017-05-03)

[Empty comment from Monorail migration]

### ra...@gmail.com (2017-05-03)

Does it qualify for a bounty or Kudos points?

### mg...@chromium.org (2017-05-04)

#18: I am checking now, but I think this does not qualify for a bounty because it is not a security vulnerability (since the Omnibox *suggestions* are not considered a security indicator).

### sh...@chromium.org (2017-05-04)

[Empty comment from Monorail migration]

### jd...@chromium.org (2017-05-04)

Given that the clipboard suggestions are a means of direct navigation to a site via arbitrary text from some unknown application, I think that ought to be considered a security surface.

### mg...@chromium.org (2017-05-05)

Yep, Security team confirmed that suggestions are considered a security surface.

### ra...@gmail.com (2017-05-05)

I've confirmed that this bug does not work in Android, Can you guys confirm it in other OS such as linux/mac?

### ra...@gmail.com (2017-05-05)

[Comment Deleted]

### ra...@gmail.com (2017-05-05)

[Comment Deleted]

### mg...@chromium.org (2017-05-08)

#23 It doesn't repro in Windows/Linux/Chrome OS (Views). Important: If you look in the Omnibox after pasting this link you will see two items:
1. The URL with the IP address on the left (correct). This is the direct link to the page, and
2. The URL with the IP address on the right (incorrect). This is a Google Search for that text; it is DELIBERATELY not formatted as a URL because it is considered plain text in that context.

IIRC Mac behaves the same way.

### ra...@gmail.com (2017-08-04)

Any update for this bug? 

### mg...@chromium.org (2017-08-08)

I'm not sure why the automated process for looking at bug bounties hasn't kicked in. Adding the panel tag.

### aw...@chromium.org (2017-08-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2017-08-09)

The VRP panel decided to award $500 for this report, many thanks! A member of our finance team will be in touch to arrange for payment.

### aw...@chromium.org (2017-08-09)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-08-10)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2017-08-10)

This issue was migrated from crbug.com/chromium/712919?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/708981]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/41313869)*
