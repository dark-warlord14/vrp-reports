# Security: Print Preview allows spoofing on other tab

| Field | Value |
|-------|-------|
| **Issue ID** | [40087257](https://issues.chromium.org/issues/40087257) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>PrintPreview |
| **Platforms** | Windows |
| **Reporter** | ch...@gmail.com |
| **Assignee** | th...@chromium.org |
| **Created** | 2017-04-05 |
| **Bounty** | $500.00 |

## Description

Chrome Version: 57.0.2987.133 stable  

Operating System: Windows 7

**REPRODUCTION CASE**  

Print preview can appears over the different origin and that's produces "spoofing", the address bar shows google.com but the print preview shows the content that used by document.write() in the PoC.

## Attachments

- [screenshot.png](attachments/screenshot.png) (image/png, 98.9 KB)
- [PoC.html](attachments/PoC.html) (text/plain, 282 B)
- [print_preview_with_source.png](attachments/print_preview_with_source.png) (image/png, 20.4 KB)

## Timeline

### el...@chromium.org (2017-04-05)

[Empty comment from Monorail migration]

[Monorail components: UI>Browser>PrintPreview]

### do...@chromium.org (2017-04-07)

I'm going to put a low severity on this because print preview doesn't leak any information back to the site, and users can't interact with anything on that page.

+thestig to determine if there is anything more to do here.

### sh...@chromium.org (2017-04-07)

[Empty comment from Monorail migration]

### th...@chromium.org (2017-04-11)

I believe it's always been possible for the URL in the Omnibox to not reflect the source of printing. e.g. a page on foo.com has a cross-origin iframe to bar.com, and one tries to print only the iframe. e.g. via window.print() from within the iframe. In this case, the Omnibox still shows foo.com.

It feels weird to me for the Omnibox to change to reflect what's printed in the iframe. Maybe Print Preview should have its own indicator to clarify what URL is being printed? Though some web apps print from generated URLs that are not user friendly, so showing those raw URLs may not be a great UX.

One place where print preview does show a URL is in the footer if one flips on that setting. There, for the bar.com iframe case, it still shows foo.com.

Similarly, the PoC ends up showing google.com in the footer. Maybe we should fix that, but the note about generated URLs above applies here too.

### th...@chromium.org (2017-04-11)

+estark to discuss security UX.

### th...@chromium.org (2017-04-11)

For fixing the footer URL, in PrintPreviewHandler::HandleGetPreview(), we would change:

content::NavigationEntry* entry =
    initiator->GetController().GetLastCommittedEntry();
...
url = entry->GetVirtualURL().ReplaceComponents(url_sanitizer).spec();

to something like:

url = initiator->GetFocusedFrame()->GetLastCommittedURL().ReplaceComponents(url_sanitizer).spec();

### th...@chromium.org (2017-04-21)

[Empty comment from Monorail migration]

### me...@chromium.org (2017-04-21)

Instead of the full URL of the page being printed, can we use the origin? E.g. the "Print" on the top left of the dialog could say "Print a page from www.printed.com" or something similar.

### th...@chromium.org (2017-04-22)

meacer: https://crbug.com/chromium/708595#c8 is regarding the idea in https://crbug.com/chromium/708595#c4 where Print Preview should have its own indicator, right? I think that's doable. Let me try really quick locally and generate a screen shot. Any thoughts on https://crbug.com/chromium/708595#c6?

+hwi FYI.

### me...@chromium.org (2017-04-22)

thestig: Yes, that was my idea. Re https://crbug.com/chromium/708595#c6: Is it possible that the printed frame is not the focused one? In that case it would show the wrong URL in the footer it seems. But if not, your change looks reasonable to me.

### th...@chromium.org (2017-04-25)

Forgot to get back to this earlier. Here's my mock w.r.t. https://crbug.com/chromium/708595#c9.

### me...@chromium.org (2017-04-26)

That looks great to my non-designer eyes. You might also want to test it with
- RTL domains
- Very long domains
- IDNs


### ch...@gmail.com (2017-07-02)

This seems like fixed on Canary and Stable.

### mm...@chromium.org (2019-04-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-09-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-23)

[Empty comment from Monorail migration]

### me...@chromium.org (2019-10-30)

thestig: Can you please confirm https://crbug.com/chromium/708595#c13 when you have a chance?

### me...@chromium.org (2019-11-09)

This indeed looks fixed, but I can't pinpoint the CL (when I bisect, the opening tab crashes). 

### me...@chromium.org (2019-11-26)

Marking as fixed even though we don't have a CL to point to.

### sh...@chromium.org (2019-11-27)

[Empty comment from Monorail migration]

### na...@google.com (2019-12-02)

[Empty comment from Monorail migration]

### na...@google.com (2019-12-05)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-12-05)

Congrats! The Panel decided to reward $500 for this report!

### na...@google.com (2019-12-05)

[Empty comment from Monorail migration]

### ad...@google.com (2019-12-05)

Declaring as fixed in M79 for the purposes of release notes though it was probably fixed earlier.

### ad...@chromium.org (2019-12-06)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-12-10)

[Empty comment from Monorail migration]

### ad...@google.com (2020-03-04)

[Empty comment from Monorail migration]

### [Deleted User] (2020-03-04)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/708595?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40087257)*
