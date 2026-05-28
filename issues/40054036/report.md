# Security: Self-XSS in Google Chrome mobile browser

| Field | Value |
|-------|-------|
| **Issue ID** | [40054036](https://issues.chromium.org/issues/40054036) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P4 |
| **Component** | UI>Browser>Omnibox |
| **Platforms** | Android |
| **Reporter** | bu...@gmail.com |
| **Assignee** | ga...@chromium.org |
| **Created** | 2020-12-01 |
| **Bounty** | $500.00 |

## Description

Dear team,

This issue has been reported to Android Security Team with reference (issue #174157709, <https://issuetracker.google.com/174157709>)). The Android Security Team forwarded this issue for you. Here, we submit the issue for you with further details just in case you haven't received it from Android Security Team.

**VULNERABILITY DETAILS**

We identified a potential self-XSS issue in Chrome Android mobile browser. The self-XSS vulnerability can be executed from the browser address bar. We're aware that the current practice you follow is to trim "javascript:" when users paste a script from the clipboard.

However, if a user pastes a script with "javascript:" from the keyboard clipboard, the trimming will not apply and the script will be executed. The keyboard clipboard is supported on all Android devices and available in the keyboard. It can be accessed from the Android keyboard by clicking on the clipboard icon.

Please check the supplied demo video for further details.

Please refer to this older issue and the following URL for further info about self-XSS

[1] <https://bugzilla.mozilla.org/show_bug.cgi?id=1422643>  

[2] <https://en.m.wikipedia.org/wiki/Self-XSS#:~:text=Self-XSS%20operates%20by%20tricking,to%20hack%20another%20user's%20>

**VERSION**

Chrome Version: [86.0.4240.198] + [stable]  

Operating System: Android 10, Security patch level Sep 2020.

**REPRODUCTION CASE**

Please check the supplied demo video..  

1.Copy the javascript URL ~ javascript:alert("Self XSS on @ "+document.cookie);  

2.Open Chrome browser and access any web page (email, bank, social messages websites..etc).  

3.Click on the keyboard clipboard and choose the copied URL to paste it.  

4.Click on the link or Go from the keyboard and the code will be executed.

MITIGATION

1.We believe removing the support of "javascript:" might be best to avoid any self-XSS. This is already implemented in Firefox mobile browser, Safari, Desktop Chrome and Desktop MS Edge.  

2.Intercept the keyboard clipboard "paste" action and trim the "javascript:" from the pasted text.  

3.Add a handler to the address bar EditText to clear the "javascript:" string from the inserted text.

**CREDIT INFORMATION**  

University of Birmingham  

Abdulla Aldoseri {[axa1170@student.bham.ac.uk](mailto:axa1170@student.bham.ac.uk)}  

David Oswald {[d.f.oswald@bham.ac.uk](mailto:d.f.oswald@bham.ac.uk)}

## Attachments

- [Chome_PoC.mp4](attachments/Chome_PoC.mp4) (video/mp4, 3.4 MB)
- [poc_patch.mp4](attachments/poc_patch.mp4) (video/mp4, 475.6 KB)

## Timeline

### [Deleted User] (2020-12-01)

[Empty comment from Monorail migration]

### es...@chromium.org (2020-12-01)

twellington@, would you be able to help triage this security bug? Maybe someone familiar with the Android omnibox could take a look?

I'm triaging as Low severity because of the user interaction required.

### es...@chromium.org (2020-12-01)

[Empty comment from Monorail migration]

[Monorail components: UI>Browser>Mobile UI>Browser>Omnibox]

### es...@chromium.org (2020-12-01)

[Empty comment from Monorail migration]

### tw...@chromium.org (2020-12-01)

Sending to Filip for omnibox triage.

At quick glance, it looks like we do have some code that's intended to sanitize text for paste, that ultimately relies on cross-platform //component/omnibox/ code: https://source.chromium.org/chromium/chromium/src/+/master:components/omnibox/browser/omnibox_view.cc;drc=d81c5852498699fe3cd812e78d31c77c28e29281;l=83

Perhaps that's not getting called when pasting from the keyboard.

[Monorail components: -UI>Browser>Mobile]

### [Deleted User] (2020-12-02)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### fg...@chromium.org (2020-12-04)

Most likely I'll be taking care of this bug.
If I cannot get this resolved quickly, I'll dispatch.

### bu...@gmail.com (2020-12-04)

Dears,

If you are using a webview for Android chromium, maybe you can interecpt the url before loading the page by overiding shouldOverrideUrlLoading method. see the example

// Code example
 mWebView.setWebViewClient(new WebViewClient() {
            @Override
            public boolean shouldOverrideUrlLoading(WebView webView, String url) {

                //todo: strip the Javascript: prefix from the url 

                webView.loadUrl(url);

                return true;
            }
        });


Hopefully this will be helpful for you.

Regards,
Abdulla Aldoseri

### bu...@gmail.com (2021-01-14)

Hi, 

I was looking in chromium code. I think this might help you to solve the issue quickly.

Here are the links to where the current practice strip the javascript scheme from the url:

1. Fetching the clipboard text and sanitize it before paste it using this method (sanitizeTextForPaste)
https://github.com/chromium/chromium/blob/99314be8152e688bafbbf9a615536bdbb289ea87/chrome/android/java/src/org/chromium/chrome/browser/omnibox/UrlBarMediator.java#L279

2.The method (sanitizeTextForPaste) will call (StripJavascriptSchemas) function from ominbox to strip the javascript scheme at this line
https://github.com/chromium/chromium/blob/99314be8152e688bafbbf9a615536bdbb289ea87/components/omnibox/browser/omnibox_view.cc#L151

Regards,
Abdulla Aldoseri

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-11)

[Empty comment from Monorail migration]

### zh...@google.com (2021-03-17)

[Empty comment from Monorail migration]

### bu...@gmail.com (2021-06-15)

Dears,

Any update about the issue?
 
We kindly ask if possible to assign a CVE for this issue as we would like to disclose the issue if possibile.

Regards,
Abdulla

### fg...@chromium.org (2021-08-02)

The way Desktop handles the problem is by stripping the leading "javascript:" from the clipboard content when pasting.

If we type in directly "javacsript:alert(document.cookie);" we still get the scrip executed.
We won't be addressing that part as part of this issue, given it is not clipboard related.

### fg...@chromium.org (2021-08-02)

Nikita, Zak,

Would you know who is the best person to look into this?
Since regular pasting from the clipboard, or offering a clipboard suggestion doesn't trigger a negative response, I suspect when Google Keyboard performs a past the characters are typed in verbatim? Can you confirm that?

Is there a chance we could treat a leading "javascript:" in a special way to prevent script execution from the clipboard past triggered from the keyboard app?

/Filip

### fg...@chromium.org (2021-08-02)

I took a liberty of testing this with mobile Firefox and it appears that there is many ways to paste the unwanted script into their omnibox equivalent. (I did that to see if Keyboard negatively affects other browsers, but it looks like there is plenty of ways they are not there yet WRT preventing this issue.)

### [Deleted User] (2021-08-05)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### fg...@chromium.org (2021-08-06)

Adding suzhe@ from GBoard team. I am also sending an email separately to get visibility into this.

### fg...@chromium.org (2021-08-09)

I got response back from the Gboard folks (suzhe@):

> Unfortunately, I don't think it's something that should be fixed in Gboard. Even if we can fix this bug in Gboard somehow, we can't fix every 3rd-party IMEs which have the similar copy/paste functionality. This bug should definitely be fixed in Chrome.

> I'm wondering why Chrome needs to support executing javascript in the omnibox? Can't we just remove this capability? If we do need to keep this capability for some strong reason, then can we show some alert UI to the user asking for a confirmation before executing the script?

It is also confirmed that GBoard is acting as if the user was typing in the whole message while pasting. Chrome currently allows the input starting from "javascript:" and executes the string directly (On Android and desktop at least).

We have 4-ish options:
1. Ignore the problem (the user can see what is in the clipboard before they choose to paste it) -- GBoard has multiple ways of showing the clipboard content before the user "pastes" it.
2. Impede the capability to execute scripts typed into Omnibox by hand. (e.g. one extra confirmation dialog) -- Covers other IMEs with similar paste mechanics.
3. Remove the capability to execute scripts typed into Omnibox by hand. (never run, e.g. sanitize input to remove javascript: before execution).
4. Keep pushing for a fix on GBoard side -- unlikely per suzhe@ (see above) and doesn't cover other keyboard.

Adding Adrian to me reason through the options above, please.

### ad...@google.com (2021-08-09)

Is this a valid fifth option?

5. Recognize when there's a single atomic input of MANY characters from the IDE, and then sanitize that to remove 'javascript:' just as we do for pastes?

I don't know if this can be done via timing (IME typing faster than a human can realistically do) or any other signals.

Even if that were possible, I don't know which of 1-5 is best, so I'm going to bring in some others to comment.

### rs...@chromium.org (2021-08-10)

> It is also confirmed that GBoard is acting as if the user was typing in the whole message while pasting.

I did some testing in the debugger and I think we can distinguish between key events and IME-committed text changes. The GBoard paste chip does not go through dispatchKeyEvent() [1], but only through onTextChanged(). And because onTextChanged() is called via super.dispatchkeyEvent(), we could set a flag to determine if the new text was the result of actual keyed entry or text composition.

[1] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/android/omnibox/java/src/org/chromium/chrome/browser/omnibox/AutocompleteEditTextModel.java;l=497;drc=385121b715b153153f7626baf728cbd588250ff7
[2] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/android/omnibox/java/src/org/chromium/chrome/browser/omnibox/AutocompleteEditText.java;l=189;drc=385121b715b153153f7626baf728cbd588250ff7

### su...@chromium.org (2021-08-10)

Re #23: determining if an input is a paste action in the keyboard via timing is not 100% reliable. For example the user may store a piece of javascript in the keyboard's personal dictionary with a shortcut associated to it, and then the javascript snippet can be typed into the app at once by typing the associated shortcut instead. The user can also input a piece of javascript snippet and store it as a clip item in the keyboard, and then the user can input it into the app at once with a single click. If you really want to support javascript execution in the omnibox, then these two cases shouldn't be prevented, because the javascript snippet was typed into the keyboard by the user deliberately.

Re #24: dispatchKeyEvent() won't be called when typing on an on-screen keyboard, so this approach won't work.

IMO, option 1, 2, 3 listed in #22 are reasonable to me.



### rs...@chromium.org (2021-08-10)

> Re #24: dispatchKeyEvent() won't be called when typing on an on-screen keyboard, so this approach won't work.

Ah, you’re right. I suppose we could check onTextChanged() lengthBefore/lengthAfter?

Otherwise, I’m inclined to do #1 or #3.

### su...@chromium.org (2021-08-10)

Re #26: I think the key issue is that even if we can detect bulk input vs. char by char input somehow, there is no way to know if the user wants to execute the javascript code intentionally or not.

I'd personally vote for option 3, unless we have some mandatory use cases to support.

### ad...@chromium.org (2021-08-11)

I suspect option 3 would be unpopular - bookmarklets are somewhat widely used - https://en.wikipedia.org/wiki/Bookmarklet - obviously they're mostly used via bookmarks but presumably it's therefore pretty common to type javascript: URIs during their development/testing/etc. I'm not sure whether that really applies on Android, but maybe.

Before we considered option 3 I think we should reach out to DevRel folks. (e.g. kinlan@)? cc mkwst too, because although this isn't really web platform compatibility, he is Wise on such matters.

### fg...@chromium.org (2021-08-12)

[Empty comment from Monorail migration]

### fg...@chromium.org (2021-08-12)

Adding reporter of the issue resolved as duplicate for visibility.

### fg...@chromium.org (2021-08-12)

[Empty comment from Monorail migration]

### mk...@chromium.org (2021-08-16)

Unfortunately, I'm not feeling terribly Wise this morning. :)

On desktop platforms, we did pretty explicitly carve out bookmarklets in places like CSP to allow them to continue working and making users happy. I do think that's a use case the product would benefit from continuing to support on desktop. I don't have much insight into usage on Android, but it's also not clear to me that they would run through the same code path. On desktop, they're implemented as a directly browser-initiated navigation, not as typing something into the omnibox. The same seems to be true on Android?

If that's the case, I'd be comfortable preventing folks from typing `javascript:` URLs into the omnibox entirely (on desktop and mobile). We have devtools for folks who choose to poke at pages innards to do so. Unless our friends in devrel agree (cc paulkinlan@ and merewood@), option 3 seems like a fine way way to go.

### [Deleted User] (2021-08-16)

[Empty comment from Monorail migration]

### fg...@chromium.org (2021-08-16)

Adding Gang in case we need to make changes specific to clipboard handling on Android.

### fg...@chromium.org (2021-08-18)

Gang will work on prototyping option 3 on Android/Desktop and confirm the bookmarklet works when direct input is disabled. -> we need to consider when to drop the leading "javascript:" e.g. during typing, after break in typing or upon execution attempt?

My understanding of bookmarklet is that we have a bookmark URL set to "javascript:..." at this point.

We won't be exploring options 5 for now, although if we wanted to leave the "javascript:..." capability to be typed in by hand we could limit ourselves to only the first input (on empty omnibox), that way follow up changes would be consider totally conscious by the user. (this is a hybrid between #5 and #1).

### bu...@gmail.com (2021-09-26)

Hi, 

I think you can solve the issue similar to what adetaylor@google.com proposed (option #5) but without timing. 

You can distinguish between paste event of IMEs and single key event.
The commit of IME works differently based on the number of characters of the string (N) according to [1]
(N=1): It sends a key char event like an actual keypress.
(N>1): It sends a special key with all the strings (text-pasting case)

You simply need to override the OntextChanged method of omnibox/AutocompleteEditText[2] class as follow:
```

bool flag; 
// if flag is true, then it is a multiple character paste. 

public void onTextChanged(CharSequence s, int lengthBefore, int lengthAfter) {
    if(lengthBefore == 0 && (lengthAfter>1) && s.toString().toLowerCase().startsWith("java:"))
        flag = true;
        // It need to be from the start(lengthBefore=0),more than a single character (lengthAfter>1) and begins with Java prefix
    else
        flag = false;
}

```

Later on, it is possible to strip the java: prefix in afterTextChanged method like this: 
```
public void afterTextChanged(Editable s) {
    String query = s.toString();
    if(flag) {
      //strip the java prefix from autoCompleteEditText
    }
}

```

attached to you a PoC demo video

[1] https://android.googlesource.com/platform/frameworks/base/+/56a2301/core/java/android/view/inputmethod/BaseInputConnection.java#529
[2] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/android/omnibox/java/src/org/chromium/chrome/browser/omnibox/AutocompleteEditText.java;l=189;drc=385121b715b153153f7626baf728cbd588250ff7


### bu...@gmail.com (2022-01-27)

Dears,

Any update ?

Regards,
Abdulla Aldoseri

### en...@google.com (2022-01-27)

I am not sure I understand this right.
so the bug is about the user being allowed to execute javascript from the omnibox, which is generally valid..
and it argues that explicitly typing a malicious javascript code is dangerous to the user..

extrapolating this: would it also be considered a security bug that the user can type a malicious website URL? why/why not?

### bu...@gmail.com (2022-01-27)

It is about pasting a Javascript in the address bar. 

The default case is, if a user uses the context menu for pasting the malicious javascript, Omnibox will trim the javascript prefix, preventing it from executing it.

While here, in this issue, if the user uses the GBoard clipboard to paste the malicious javascript, Omnibox will not trim the Javascript assuming the user enters the text manually.

### bu...@gmail.com (2022-02-11)

Dears,

The issue reported a year ago back in Dec 1, 2020. It already exceed the 90-day disclosure deadline accroding to [1]
Kindly, I would like to process the disclosure plan as soon as possibile. May you assign a CVE to this issue please.


[1] https://about.google/appsecurity/

Thank you,
Abdulla Aldoseri

### ad...@chromium.org (2022-02-11)

Thanks. This has been assessed as a Low severity bug, and we don't have any defined time duration for when we fix low severity bugs - please see our guidelines here:
https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/severity-guidelines.md

I'm sorry, I know that's frustrating!

We will assign a CVE when we fix it.

It is your report, so if you wish to disclose it publicly, you're totally free to do that. It will, of course, disqualify you from receiving any VRP reward when we fix this. Please let us know what you decide!

### bu...@gmail.com (2022-02-11)

[Comment Deleted]

### bu...@gmail.com (2022-02-11)

So, If I disclose it, I will not get the VRP reward. right?

But can I still get the CVE afterwards?

Regards.
Abdulla Aldoseri

### fg...@chromium.org (2022-02-14)

Hey, we will try applying approach from https://crbug.com/chromium/1154353#c36 for M101 (next week).
We are currently busy with M100 work.

### ad...@chromium.org (2022-02-15)

Thanks fgorski@!
And to answer https://crbug.com/chromium/1154353#c43, yes, irrespective of reward status we will assign a CVE when we fix the bug or sooner if it is discussed in public.

### bu...@gmail.com (2022-02-22)

Thanks fgorski@ @fgor...@chromium.org.

Sounds like you close to work on it. I guess I can wait then for a month at least.
Hopfully you can manage to make it work soon.

Also, if you have a question or a query about the solution in https://crbug.com/chromium/1154353#c36. Please feel free to ask.
I'm really happy to help

Regards,
Abdulla Aldoseri

### ga...@chromium.org (2022-02-25)

Hi, I am a little busy this week with M100 bugs, will make a prototype for this next week.

Thanks,
Gang

### bu...@gmail.com (2022-03-07)

All the best gangwu@chromium.org.

Dears,

Regarding the disclosure, is there any thing need to be done from my side (send you the disclosure document .. etc?).
I'm planinig to publish on MadWeb 2022, that will be held on Thursday, April 28, 2022. (approximately 2 months from now).

In the meantime, I will be available if help is needed. Thank you all.

Regards,
Abdulla Khalifa Aldoseri

### ga...@chromium.org (2022-03-07)

Thanks, Abdulla Aldoseri, I have a prototype for the issue, and working on the tests. https://chromium-review.googlesource.com/c/chromium/src/+/3504788
I think you did a great job for finding the bug and reporting it, and I think you are good for now. I will post the update here once the bug is fixed.

### ga...@chromium.org (2022-03-10)

The CL is ready to review, I will update once the CL is landed.

### gi...@appspot.gserviceaccount.com (2022-03-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/81e2250b60d4a6d863864249cc2f1da97669f03d

commit 81e2250b60d4a6d863864249cc2f1da97669f03d
Author: Gang Wu <gangwu@chromium.org>
Date: Tue Mar 22 20:34:07 2022

[Omnibox] Disallow pasting of javascript in the Omnibox

Currently, if a user copy-and-paste javascript to Omnibox by ctrl+C or
long press and then select "Paste", the "javascript:" will be striped
from the text by OmniboxView::SanitizeTextForPaste. This sanitizing text
is for the all platforms.

But on Android, some IME, like GBoard may paste the text as user's
typing, not from system clipboard. To handle this case, we need to
specially handle the case.

In this CL, AutocompleteEditText will count a user's input as the paste
if AutocompleteEditText receive a lot of text in a single call, and then
sanitize the text.

Bug:1154353


Change-Id: Iaea24911fea0e1a92c9ee4938fa2dd442e698647
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3504788
Reviewed-by: Tomasz Wiszkowski <ender@google.com>
Reviewed-by: Filip Gorski <fgorski@chromium.org>
Commit-Queue: Gang Wu <gangwu@chromium.org>
Cr-Commit-Position: refs/heads/main@{#984000}

[modify] https://crrev.com/81e2250b60d4a6d863864249cc2f1da97669f03d/chrome/browser/ui/android/omnibox/java/src/org/chromium/chrome/browser/omnibox/AutocompleteEditTextTest.java
[modify] https://crrev.com/81e2250b60d4a6d863864249cc2f1da97669f03d/chrome/browser/ui/android/omnibox/java/src/org/chromium/chrome/browser/omnibox/LocationBarCoordinator.java
[modify] https://crrev.com/81e2250b60d4a6d863864249cc2f1da97669f03d/chrome/browser/ui/android/omnibox/java/src/org/chromium/chrome/browser/omnibox/AutocompleteEditText.java
[modify] https://crrev.com/81e2250b60d4a6d863864249cc2f1da97669f03d/chrome/browser/ui/android/omnibox/java/src/org/chromium/chrome/browser/omnibox/UrlBarCoordinator.java


### ga...@chromium.org (2022-03-22)

[Empty comment from Monorail migration]

### ga...@chromium.org (2022-03-22)

[Empty comment from Monorail migration]

### ad...@chromium.org (2022-03-22)

Please mark bugs as Fixed before requesting merges, thanks!

Also - as this is a Low severity bug, we (from the security team) wouldn't be requesting merge. Given that this change is a little delicate (assessing single call vs lots of calls) I think we should wait for this to organically trickle through head, beta and stable before release. Is that OK with you?

### za...@google.com (2022-03-22)

[Empty comment from Monorail migration]

### ga...@chromium.org (2022-03-22)

Yes, it is ok with us. merge request removed.

### [Deleted User] (2022-03-23)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-23)

[Empty comment from Monorail migration]

### bu...@gmail.com (2022-03-24)

Hi all,
Thanks on fixing the issue and well done.

Since the issue is fixed, is there any information reqiured from my side for the reward?

Regards,
Abdulla Aldoseri


### ad...@chromium.org (2022-03-24)

No information needed! This will go to the VRP panel who will assess whether this attracts a reward and will get in touch with you. I should warn you that they unfortunately have a bit of a backlog right now, so it may take a few weeks!

Also, once this ships, we will assign a CVE. Per https://crbug.com/chromium/1154353#c54 that will take a while for it to trickle through all the branches. I think this will probably ship in Chrome 102 in late May.

Thanks for the report!

### am...@google.com (2022-03-31)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-03-31)

Thank you for this report. While we don't consider this to be a security issue that is in our direct threat model, we do appreciate this report and that it enable us to make a rather large functional change that could impact the user security workflow/experience. The Chrome VRP would like to extend a $500 thank you for this report. A member of our finance team will be in touch to arrange payment. Thank you for your efforts and reporting this issue to us and we appreciate your patience during the time between reporting to the fix. 

### am...@google.com (2022-04-01)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-05-24)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-29)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@gmail.com (2022-10-06)

Dears, 

Any update about assigning a CVE for this issue ?

Regards,
Abdulla

### ad...@chromium.org (2022-10-06)

Thanks for getting in touch. Please see https://crbug.com/chromium/1154353#c62: this was not deemed to be a security vulnerability, so it won't be receiving a CVE.

### is...@google.com (2022-10-06)

This issue was migrated from crbug.com/chromium/1154353?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1154338, crbug.com/chromium/1237595]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40054036)*
