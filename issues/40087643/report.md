# Security: Whole-script confusable domain label spoofing (Greek)

| Field | Value |
|-------|-------|
| **Issue ID** | [40087643](https://issues.chromium.org/issues/40087643) |
| **Status** | Assigned |
| **Severity** | Unknown |
| **Priority** | P2 |
| **Component** | UI>Browser>Omnibox, UI>Internationalization |
| **Reporter** | ra...@gmail.com |
| **Assignee** | js...@chromium.org |
| **Created** | 2017-05-14 |
| **Bounty** | $500.00 |

## Description

http://νυ.com ( http://xn--yxaq.com/ ) --> When combined with normal letters; it does convert it into punnycode and when purely written in this form, it doesn't convert it.

## Timeline

### ra...@gmail.com (2017-05-14)

[Comment Deleted]

### ra...@gmail.com (2017-05-14)

"This is U+0B3D GREEK SMALL LETTER NU + U+03C5 GREEK SMALL LETTER UPSILON.

This is an example of a whole-script confusable as discussed in   https://crbug.com/chromium/683314  . That one was Cyrillic, this one is Greek."

I opened a new issue regarding this instead of discussing in  https://crbug.com/chromium/683314  for two reasons: 

-) That issue is public and this issue is not fixed.

-) To keep the track of it. 

Although, mgicua@chromium.org has asked a reason that why the fix has not been implemented in greek letters in: 

https://bugs.chromium.org/p/chromium/issues/detail?id=720538#c5 - but since that issue has been closed, I filed a new report regarding this. However, If there's any major reason you guys can eventually close this issue.

### aa...@google.com (2017-05-15)

[Empty comment from Monorail migration]

[Monorail components: UI>Browser>Omnibox UI>Internationalization UI>Security>UrlFormatting]

### mg...@chromium.org (2017-05-15)

Thanks. I've made a high-level https://crbug.com/chromium/722167 to track all of these because I think there's little valid in having a separate bug for each example domain or even each script pair.

### na...@google.com (2020-03-03)

[Empty comment from Monorail migration]

### [Deleted User] (2020-03-04)

[Empty comment from Monorail migration]

### na...@google.com (2020-03-04)

[Empty comment from Monorail migration]

### na...@google.com (2020-03-05)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-03-05)

Congrats! The Panel decided to award $500 for this report! 

### na...@google.com (2020-03-05)

[Empty comment from Monorail migration]

### ra...@gmail.com (2020-03-05)

[Comment Deleted]

### [Deleted User] (2020-06-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2020-06-02)

This issue was migrated from crbug.com/chromium/722125?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: UI>Browser>Omnibox, UI>Internationalization, UI>Security>UrlFormatting]
[Monorail mergedinto: crbug.com/chromium/722167]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40087643)*
