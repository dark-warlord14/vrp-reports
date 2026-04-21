# Security: URL spoofing using 'very-long-hostname' URL in the Suggestion box

| Field | Value |
|-------|-------|
| **Issue ID** | [40052009](https://issues.chromium.org/issues/40052009) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>Omnibox |
| **Platforms** | iOS |
| **Reporter** | ra...@gmail.com |
| **Assignee** | jd...@chromium.org |
| **Created** | 2020-04-13 |
| **Bounty** | $500.00 |

## Description

While 'very-long-hostname' is fixed in the iOS version and shows correctly in the omnibox, but it needs to be fixed in the suggestion box since it states the link that you copied is 'google.com/fake/fake/fake' However, it should be shown as '...attack.com'

URL for the experiment:

https://google.com.mail.accounts.fake.fake.fake.fake.fake.fake.fake.fake.fake.fake.fake.fake.fake.fake.fake.fake.fake.fake.fake.fake.fake.fake.fake.fake.fake.fake.fake.fake.fake.fake.fake.attack.com/

## Attachments

- [URL spoofing in the suggestion box.jpg](attachments/URL spoofing in the suggestion box.jpg) (image/jpeg, 27.6 KB)
- [Shown correctly in omni box.jpg](attachments/Shown correctly in omni box.jpg) (image/jpeg, 27.9 KB)
- [Suggested.jpeg](attachments/Suggested.jpeg) (image/jpeg, 42.9 KB)
- [Before fix.jpg](attachments/Before fix.jpg) (image/jpeg, 27.6 KB)
- [After fix.jpg](attachments/After fix.jpg) (image/jpeg, 40.0 KB)

## Timeline

### xi...@chromium.org (2020-04-13)

Thanks for the report. Not sure if this can be attacked since when users click on the link in the suggestion box, the link will be displayed in the omnibox. +jdonnelly@, could you take a look? Thanks!

[Monorail components: UI>Browser>Omnibox UI>Security>UrlFormatting]

### ra...@gmail.com (2020-04-14)

Given that the clipboard suggestions are a means of direct navigation to a site via arbitrary text from some unknown application, therefore, Google Security team confirmed that suggestions are considered a security surface.

### ra...@gmail.com (2020-04-14)

Okay, one more update: very long url hostname isn't fixed in windows (talking about omni box here - so this could be another issue)

### jd...@chromium.org (2020-04-14)

Hi, I have a quick question:

> Given that the clipboard suggestions are a means of direct navigation to a site via arbitrary text from some unknown application, therefore, Google Security team confirmed that suggestions are considered a security surface.

The Security team confirmed this where? In an email thread? I ask because we (omnibox team) have always consider the suggestions to *not* be a security surface. Because Chrome can make no guarantees about what will happen after initial navigation. For example, any legitimate site could be compromised and redirect the user to attack.com. Our security focus is on the display of URLs in the omnibox itself, where we *can* guarantee that the displayed origin is the source of the information in the content area (assuming HTTPS, etc.).


### ra...@gmail.com (2020-04-14)

>The Security team confirmed this where?

You can find it in https://crbug.com/chromium/1070399#c21 and https://crbug.com/chromium/1070399#c22 in the https://crbug.com/chromium/712919

### [Deleted User] (2020-04-14)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jd...@chromium.org (2020-04-14)

rayyanh12: Thanks. Also lol that I'm one of the people who said that. I guess I have to argue with myself now. :)

I maintain that, despite my earlier statement in https://crbug.com/chromium/712919, suggestions are not a security surface. We can make no guarantees about where the user ends up after choosing one so there's little to be gained in trying to carefully format them. This principle is reflected in other design decisions, such as that we don't bother to display the protocol (http:// or https://) on suggestion URLs. (Consider also that if an attacker got the user to copy this URL to the clipboard and thus put it in a suggestion, they could have just as easily gotten the user to click on a link to that URL.) The right place to defend users is in the steady-state omnibox, which *can* guarantee the relationship between the URL and the content, and in the content area, where SafeSearch can trigger.

That said, I think it'd be nice-to-have if you could see the 'attack.com' part of the URL in this case. The problem is that you don't want to just show the trailing part of the URL, either, because then the spoofable surface becomes the path of the URL. To get to a better place here you'd need to make sure to specifically show the most-significant part of the domain. Which is actually rather difficult to do because of the possible presence of bi-directional text in URLs.

Given the two points above, I'm going to leave this open but reduce the priority.

### jd...@chromium.org (2020-04-14)

[Empty comment from Monorail migration]

### jd...@chromium.org (2020-04-14)

[Empty comment from Monorail migration]

### jd...@chromium.org (2020-04-14)

See the two issues I just merged for other cases where the most-significant part of the domain isn't displayed. All 3 cases share the same desire of applying smart logic or heuristics to what part of the URL to display in a suggestion.

### ra...@gmail.com (2020-04-14)

Well, just because these bugs lie on the same suggestion box doesn't mean they all are same issues. According to this logic, Every issue of URL spoofing which lies in the omni box should be duped to that one central issue "All cases of URL Spoofing in the omni box". If this is the case, I will be reporting the cases of url spoofing in the suggestion box one by one after making sure the previous one got fixed first.  Simple as that :))

### jd...@chromium.org (2020-04-14)

The logic isn't that all similar outcomes should be deduped to the same issue. The logic is that all issues with the same root cause should be deduped. If and when we made a change to address this, the one change would fix each of the issues you've reported. Hope that helps clarify my intent.

### jd...@chromium.org (2020-04-14)

That said, there's definitely no harm in you reporting multiple issues! Your thoughtful reports on each of the different cases is helpful and is why I made a note in https://crbug.com/chromium/1070399#c10 referring back to the other two reports.

### ra...@gmail.com (2020-04-14)

This would be my last comment on this 'particular argument'. I hope it could yield some fruit towards deciding more justified decision regarding it. 

> the one change would fix each of the issues you've reported

If one change could fix each of the issues, these issues won't be there now because you're already made that 'one' change by fixing the https://crbug.com/chromium/712919. How is 'not showing space in code' in the suggestion box is related to 'RTL Mishandling' and how these two are related in terms of fixture of 'very long hostname URL' problem. Obviously, they all need different fixtures. For eg: blacklisting 'space' (to show it in  code) wouldn't solve the problem of 'very long hostname URL' and solving both the issues won't solve RTL mishandling problem. These issues need to be addressed separately without merging into each other. Thanks.



### jd...@chromium.org (2020-04-14)

Sorry, I don't know what you're referring to in regards to "showing space in code". I don't see space mentioned in any of these issues (this one, https://crbug.com/chromium/1058333, https://crbug.com/chromium/1068422, or https://crbug.com/chromium/712919). The fix for https://crbug.com/chromium/712919 didn't fix the current set of issues because it's in a different part of the code than the logic that produces these "Link that you copied" suggestions. Fixing that logic would address all 3 of these issues.

### mp...@chromium.org (2020-04-14)

rayyanh12@ note that https://crbug.com/chromium/712919 was not duped into this issue. We appreciate your detailed reports, and please note that the VRP will give larger rewards to well-written reports that detail multiple different attacks. It's a bit easier to see all this extra info if the attacks are all listed in one report. Please see https://www.google.com/about/appsecurity/chrome-rewards/ for more information.

In this case, the bugs you've reported are all due to the same underlying bug, and are really separate attack methods taking advantage of the underlying bug.

It's fair to report new attacks if the fix for your first report isn't sufficient to prevent other attacks. But it's in your interest to report all attacks for a single underlying bug into a single report, as you will end up with a higher reward for a higher quality report.

### ra...@gmail.com (2020-04-14)

I'm sorry, I wasn't clear regarding "Showing space in code" - I meant https://crbug.com/chromium/1068422 (In this issue the invisible character is the space character; space character should be shown as %20 in the suggestion box too i.e 'Link that you copied' area). the https://crbug.com/chromium/712919  was literally created to show the correct URL in the 'Link that you copied'  area because before the fixture it was showing a spoofed URL in that area - just like these issues. Refer to https://crbug.com/chromium/1070399#c19 ( https://bugs.chromium.org/p/chromium/issues/detail?id=708981#c19 ) because  https://crbug.com/chromium/712919  was created based on this comment. Therefore, all these issues;  https://crbug.com/chromium/1058333,  https://crbug.com/chromium/1068422, https://crbug.com/chromium/712919 including the https://crbug.com/chromium/712919 were created because they were showing spoofed URL in the 'Link that you copied' area. I hope I made some sense here. (It's 4.43AM here - and I'm quite tired too :P)

### ra...@gmail.com (2020-04-14)

https://crbug.com/chromium/1070399#c16: https://crbug.com/chromium/712919 was created and fixed in 2017  - How can it be duped to the bug created in 2020? :P - Plus, I've given all my "valid" points here, obviously you guys are the actual boss here. I'm happy in whatever your decision is. Thank you :) 

### [Deleted User] (2020-04-15)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ra...@gmail.com (2020-05-09)

Why URL in the suggestion box is important? Answer: https://crbug.com/chromium/1080905 - Although the address bar shows spoofed URL but still user can see it's the evilzone.org.

### ra...@gmail.com (2020-10-26)

Friendly ping: Any update on this? 

### [Deleted User] (2020-10-30)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-11)

[Empty comment from Monorail migration]

### zh...@google.com (2021-03-17)

[Empty comment from Monorail migration]

### ra...@gmail.com (2021-03-23)

Can you guys update its status as fixed since this bug along with other bugs related to this has been fixed.

### ra...@gmail.com (2021-04-20)

friendly ping: Please mark this bug as fixed. thank you

### jd...@chromium.org (2021-04-29)

rayyanh12: Can you specify where you think this has been fixed? I know there were multiple issues here so I might be missing it but I'm not aware of a specific fix for this case.

### ra...@gmail.com (2021-04-29)

There were multiple bugs in this:
1) https://crbug.com/chromium/1070399 
2) https://crbug.com/chromium/1068422 
3) https://crbug.com/chromium/1058333
4) https://crbug.com/chromium/1080395 ( this reproduced in suggestion box ) 

However, all got fixed because, before the fixture of this bug - Suggestion box stated "Link that you copied - 'google.com/fake/fake/fake' "- Like link used to appear in the suggestion box. After the fixture of this bug, the suggestion box throws whole responsibility to the user "Paste the link you copied" without displaying the link the user actually copied. Here are the before and after fixture pictures.

### jd...@chromium.org (2021-06-01)

Thanks, yes, it does appear that the change to no longer show clipboard contents[1] addresses this issue.

[1] https://source.chromium.org/chromium/chromium/src/+/master:components/omnibox/browser/clipboard_provider.cc;l=177-180;drc=d977f61598c26ff907ef0bc1bdbb877867fbaa04

### [Deleted User] (2021-06-02)

[Empty comment from Monorail migration]

### [Deleted User] (2021-06-02)

[Empty comment from Monorail migration]

### am...@google.com (2021-06-23)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-06-23)

The VRP Panel has decided to award you $500 for this report. Thank you for reporting this issue to us. 

### am...@google.com (2021-06-30)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-08)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2021-09-08)

This issue was migrated from crbug.com/chromium/1070399?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: UI>Browser>Omnibox, UI>Security>UrlFormatting]
[Monorail mergedwith: crbug.com/chromium/1058333, crbug.com/chromium/1068422]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40052009)*
