# Cross-origin-read attack by chaining three vulnerabilities

| Field | Value |
|-------|-------|
| **Issue ID** | [40091524](https://issues.chromium.org/issues/40091524) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Downloads |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | he...@gmail.com |
| **Assignee** | dt...@chromium.org |
| **Created** | 2018-05-31 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

By combining three vulnerabilities it's possible to read data from cross-origin websites when an user opens a local HTML file.

The following vulnerabilities are being chained in this attack:

1. Simulating an Alt-Click (click with the alt key pressed) through javascript allows the download of cross-origin resources.
2. Using history.back() allows the download of multiple files without the need to give permission to the page.
3. File urls are considered same-origin amongst themselves, allowing any local resource to be re-downloaded with a new name and extension through the use of the download attribute.

The only requirement to perform this attack is that the targeted website must have an endpoint which contains user-controlled input (this happens in almost any API). For example, <https://issuetracker.google.com> and <https://bugzilla.mozilla.org> are both vulnerable.

The exploit works as follows:

1. Attacker makes an endpoint contain a script tag (in the example displayed in the video, the attacker reports a bug to a HackerOne program with the title <script>...</script>).
2. Later, the attacker sends the malicious page to a triager of the program (someone with access to reported bugs).
3. Triager downloads and opens the malicious HTML file containing the attacker's script.
4. By simulating an alt-click the script downloads <https://hackerone.com/bugs.json> with the default name of "response.json" (note that we can't control the name nor the extension of the downloaded file because it's a cross-origin resource).
5. By using history.back() the attacker re-downloads "response.json". This time from the Downloads folder instead of /bugs.json. We do this because all local files are same-origin resources, permitting the use of the download attribute to change the filename to "injection.html".
6. The script redirects the user to "injection.html" and the script tag that was inserted earlier is now executed, allowing the attacker to exfiltrate the information contained in <https://hackerone.com/bugs.json>.

Because the PoC exfiltrates information from a private program on HackerOne you will not be able to reproduce it. But if needed, I can create another PoC that doesn't use HackerOne.

I have also attached a reproduction case for each individual vulnerability used.

And here is a video simulating the attack:  

<https://www.youtube.com/watch?v=67nWiqIl5bc>

**VERSION**  

Chrome 67.0.3396.62 (Official Build) stable (64-bit)  

Chrome 68.0.3440.7 (Official Build) dev (64-bit)

**REPRODUCTION CASE**  

simulate.html: Downloads cross-origin resources.  

download.html: Bypasses the download limit restriction.  

change.html: Downloads local file with different name and extension.  

bug.html: Full PoC that is used in the video.

## Attachments

- [simulate.html](attachments/simulate.html) (text/plain, 562 B)
- [download.html](attachments/download.html) (text/plain, 378 B)
- [change.html](attachments/change.html) (text/plain, 339 B)
- [bug.html](attachments/bug.html) (text/plain, 1.5 KB)
- [back.html](attachments/back.html) (text/plain, 118 B)

## Timeline

### he...@gmail.com (2018-05-31)

Oops, I missed the back.html file (must be on the same folder as download.html).

### el...@chromium.org (2018-05-31)

Thanks for the report! A working PoC would probably be better for reproducing the issue than a POC that does not work.

Use of a simulated Alt+Click sounds like a circumvention of the protections introduced in https://crbug.com/chromium/608669.

> all local files are same-origin resources

In Chrome, this isn't supposed to be the case, but it sounds like you may have found a case where it is unexpectedly so.

Chrome might also consider blocking local files from triggering "Download" of other local files, which was deemed innocuous in https://crbug.com/chromium/827083.

### he...@gmail.com (2018-05-31)

Hi Eric,

I will be creating a new PoC then.

About local files not being same-origin, I thought that was the case because on m67 we can download local files and use the download attribute to set a new name (which should only be possible between same-origin resources).

### he...@gmail.com (2018-05-31)

Here is the new PoC:
https://lbherrera.github.io/lab/cross-read/start.html

To reproduce it you must click on the click and then open the automatically downloaded HTML file.

Assume that https://bharl.github.io/test/dummy.json is the targeted cross-origin endpoint where the attacker inserted his malicious script tag and wants to steal the information from.

### he...@gmail.com (2018-05-31)

I gave this more thought and realized this vulnerability can also be used to exploit previously "unexploitable" XSSes that would otherwise been blocked by CSP or the XSS Auditor.

Granted this can't be used to steal a user session, but it could be used to exfiltrate CSRF tokens as well as any private information that was rendered in the page at the time of the download.

You can reproduce it here:
https://lbherrera.github.io/lab/cross-read/bypass.html

### me...@chromium.org (2018-06-01)

This bug requires a few preconditions, so assigning medium severity (the site must allow user input and the user needs to open the downloaded file).

I'll split the bugs.

### me...@chromium.org (2018-06-01)

[Empty comment from Monorail migration]

### me...@chromium.org (2018-06-01)

[Empty comment from Monorail migration]

### me...@chromium.org (2018-06-01)

[Empty comment from Monorail migration]

### me...@chromium.org (2018-06-01)

[Empty comment from Monorail migration]

[Monorail components: UI>Browser>Downloads]

### he...@gmail.com (2018-06-01)

Hi meacer,

While it's true that the site must allow user input, the practice is extremely common, even more so for websites that use any kind of API. I feel the severity is closer to high than medium given the user is one click away from having confidential information stolen. Additionally, simply opening a HTML file is not generally seen as an attack vector, even among technical users (no warnings are shown, for example).

I personally feel this hasn't the same severity as https://crbug.com/chromium/608669, which requires the victim not only to open a local HTML file, but also upload it to the attacker's website. Finally, my attack can also exfiltrate information from dozens of websites in only one go, which https://crbug.com/chromium/608669 doesn't allow.

What do you think?

### sh...@chromium.org (2018-06-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-06-01)

[Empty comment from Monorail migration]

### go...@chromium.org (2018-06-01)

+awhalley@ (Security TPM)

### go...@chromium.org (2018-06-01)

[Empty comment from Monorail migration]

### me...@chromium.org (2018-06-01)

> While it's true that the site must allow user input, the practice is extremely common, even more so for websites that use any kind of API. I feel the severity is closer to high than medium given the user is one click away from having confidential information stolen. 

Yes, this is admittedly a low bar. But:

> Additionally, simply opening a HTML file is not generally seen as an attack vector, even among technical users (no warnings are shown, for example).

Quoting asanka from https://bugs.chromium.org/p/chromium/issues/detail?id=780770#c9:

"""
So to address the question in #4, marking all downloads that run JS was in fact what we were doing in the past. But mitigations around treating file:// origins as unique in Chrome was considered sufficient to no longer consider downloaded HTML as being dangerous. Where scripts are not run such mitigations in place (e.g. .js files that could be executed with external script engines) downloads continue to be considered dangerous.

I don't think considering HTML to be dangerous again would help in this case. The chain already requires user interaction unless the user has configured HTML as a file type that opens automatically.
"""

So we consider local HTML files non-dangerous, but the user opening them is still a mitigation. I don't have a strong opinion about the severity though. If anyone disagrees and wants to raise this to high, that's okay with me.

### jo...@chromium.org (2018-06-04)

+rbyers who I recently talked to about site initiated downloads

### he...@gmail.com (2018-06-05)

On the past few days I made two discoveries:

1. A redirect also bypasses the protections introduced in https://crbug.com/chromium/608669, allowing resources to be downloaded cross-origin. Should I file another bug report on this? I don't know if the root cause is the same as the alt+click bypass (If I had to guess I would say they are unrelated).

// redirect.php
<?php
header("Location: ".$_GET["url"], true, 301);
exit;
?>

// index.html
<a href="redirect.php?url=http://google.com" download>Cross-origin download</a>

2. I also created a PoC which can trick users into opening local HTML files (or other files) by abusing a clickjacking vulnerability.

It can be reproduced here (although it will probably be misaligned because I only had my screen resolution in mind):
https://lbherrera.github.io/lab/game-read/

And here's a video simulating the full attack (clickjacking + cross-origin read):
https://www.youtube.com/watch?v=6cz2J6KGVoU

Should I also file another bug report about this?

### jo...@chromium.org (2018-06-05)

1. is https://crbug.com/chromium/831073

### pa...@chromium.org (2018-06-05)

The repro in #5 works for me. I think Medium is the right severity; High is defined (https://chromium.googlesource.com/chromium/src/+/master/docs/security/severity-guidelines.md#High-severity) as "A bug that allows full circumvention of the same origin policy. Universal XSS bugs fall into this category, as they allow script execution in the context of an arbitrary origin".

It's a large value of Medium, though. :)

asanka, you seem to be the main Downloads OWNER, is that right? Can you please see this family of bugs through, and/or help find other people? Thanks.

67 is out the door and this is a complicated suite of bugs, so I'm bumping the Milestone to 68. It'd be great if we could make that.

### pa...@chromium.org (2018-06-05)

[Empty comment from Monorail migration]

### me...@chromium.org (2018-06-05)

[Empty comment from Monorail migration]

### me...@chromium.org (2018-06-05)

Just in case we want to do something about the clickjacking attack in https://crbug.com/chromium/848123#c18, I filed https://crbug.com/chromium/849820. (another variant of it that uses the download shelf is https://crbug.com/chromium/636974)

### he...@gmail.com (2018-06-05)

Is https://crbug.com/chromium/780770 about dropping javascript files inside the Downloads folder? Because reading asanka's quote made me realize that websites that load external javascript from the root folder and are using relative path are also vulnerable to this attack.

Which is relevant because even after all the bugs that I reported are fixed, the attacker will still be able to drop javascript files inside the Downloads folder and when/if an user saves a page to the Downloads folder and opens it, the attacker's script will end up being executed. This might be something worth fixing (if possible at all).

### as...@chromium.org (2018-06-06)

dtrainor@ is the new downloads TL. Passing along to him. I'd be happy to help as well.

### dt...@chromium.org (2018-06-07)

[Empty comment from Monorail migration]

### dt...@chromium.org (2018-06-07)

Taking a look thanks!  Will work to get this in by 68!

### qi...@chromium.org (2018-06-07)

for #24, i think we have to also think about the normal cases.
For example, a lot of crbug reports contain both javascript and html files, if we don't allow the javascript to run when opening the html file after download, then it will put a lot of extra effort to reproduce those issues.



### he...@gmail.com (2018-06-07)

asanka@: About your comment on https://crbug.com/chromium/827083, it seems the behavior you described is only true for m67.

On m68, simply using the download attribute on an anchor tag already redirects the user to the file:// URL instead of downloading it.

The behavior on m68 only changes when the alt+click bypass starts the download, in which the file:/// URL will be downloaded with the new name and extension.

### dt...@chromium.org (2018-06-12)

@29 - Your PoC looks like it simulates an alt click on the download, but I'm not seeing injection.html created in the download folder (instead it navigates to dummy.json like you said in @29).  Is this particular step in the flow fixed or is it still useful in the attack chain?

### he...@gmail.com (2018-06-13)

It seems a change was made on m69 which prevents the alt+click bypass from being able to download cross-origin resources (breaking the attack chain), but I wouldn't know which change did that. Prior to https://crbug.com/chromium/848123#c29 I had only tested on m66, m67 and m68. One thing that I found strange while testing is that non-simulated alt+clicks on anchor tags with the download attribute are still allowed to download cross-origin files with different names/extensions, even on Canary.

### dt...@chromium.org (2018-06-13)

Thanks!  Will try to track down the relevant change.

### dt...@chromium.org (2018-06-19)

[Empty comment from Monorail migration]

### dp...@chromium.org (2018-06-19)

[Empty comment from Monorail migration]

### he...@gmail.com (2018-06-30)

dtrainor@: I did some digging and found the relevant change that broke the attack chain: https://chromium.googlesource.com/chromium/src/+/4379a7fcff8190aa7ba72307b398161c32102c52

### sh...@chromium.org (2018-07-03)

dtrainor: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-07-17)

dtrainor: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### he...@gmail.com (2018-07-30)

Can I get access to https://crbug.com/chromium/848531?

### aw...@chromium.org (2018-07-30)

luan.herrera@ - added you to that issue, thanks

### he...@gmail.com (2018-07-31)

awhalley@: Thanks!

Seeing all issues were fixed with exception of https://crbug.com/chromium/849820 I was wondering if this bug can be marked as fixed given https://crbug.com/chromium/849820 isn't really an issue blocking the chain described in this attack but rather just a way to trick the user into opening a local file, which can be achieved in several ways, such as demonstrated in https://crbug.com/chromium/63773 and https://crbug.com/chromium/636974.

### aw...@google.com (2018-07-31)

re https://crbug.com/chromium/848123#c40 - sounds reasonable. Marking as fixed.

### sh...@chromium.org (2018-08-01)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-08-07)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-08-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-08-08)

This bug requires manual review: M69 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: amineer@(Android), kariahda@(iOS), cindyb@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2018-08-08)

awhalley@ (Security TPM) for M69 merge review

### aw...@google.com (2018-08-09)

Tracking any merges in the child bugs, no merges needed for this bug.

### aw...@chromium.org (2018-08-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-08-13)

Hi luan.herrera@! The VRP panel decided to award $2,000 for this report - thanks!

### aw...@google.com (2018-08-13)

[Empty comment from Monorail migration]

### he...@gmail.com (2018-08-14)

Hi again awhalley@!

I started writing down about this attack chain for an upcoming article that I plan to release when the Stable version comes out and I realized that I missed some key points that the panel might have also overlooked.

At first I didn't give too much attention about the bug's ability to re-download local files with different names and extensions, but this essentially also allows an attacker to steal local files if they can somehow inject their malicious javascript code into them.

Knowing this I decided to look which local Chrome files could be remotely altered by the attacker and found a few (there are others but for brevity I will omit them, also, they are not as relevant as the ones below):

/home/user/.config/google-chrome/Default/History
/home/user/.config/google-chrome/Default/Web Data
/home/user/.config/google-chrome/Default/Network Action Predictor

Redirecting an user to "http://example.com/<script>...</script>" for example, would add this URL to their browsing history and consequently to their local Chrome history file, which then could be downloaded by the attacker, renamed to injection.html and forced to be opened by the victim. This would then execute the attacker controlled javascript, allowing all of the user's history to be stolen.

Username/passwords in GET parameters, SSO tokens, CSRF tokens, secret gists/pastebins/videos/images, all this and much more would be leaked.

Also (I imagine you guys already know this, but wasn't mentioned before by me), it's possible to launch this attack from a locally opened pdf instead of a html file. Albeit the technical distinction between these two aren't that big, for a common user, I think opening a pdf file would appear less threatening.

In light of these new discoveries, would be possible for this report to be revaluated by the panel? If a new PoC is deemed necessary I can create and provide one.

Thanks again!

### he...@gmail.com (2018-08-15)

Oops, redirecting the user to "http://example.com/<script>...</script>" would not do the trick because the URL is actually encoded before being saved.

Instead, the attacker would need to create a page, set the title of the page to their payload and then redirect the user to it (the title of the page is saved inside the Chrome history file without being escaped).

Also, I noticed that the Cookies file can also be stolen by this attack. I am not familiar with the details behind it but it seems the cookies are encrypted using the computer's password as a key. I think it would be possible for an attacker to download and bruteforce it offline.

### aw...@google.com (2018-08-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-08-27)

Hi luan.herrera@ - thanks for the additional details. The VRP panel took another look at this, and decided to keep the reward amount at 2k, I'm afraid. Cheers!

### he...@gmail.com (2018-09-04)

Seems this bug is missing in the release notes :(

### aw...@google.com (2018-09-05)

Apologies, this has been fixed.

### he...@gmail.com (2018-09-05)

awhalley@: When would you feel comfortable with me publishing an article about this chain of bugs? Do you think waiting one week for users to update would suffice?

### aw...@google.com (2018-09-05)

Would waiting until the 25th be OK? That's two weeks after the Chrome OS release date.

### he...@gmail.com (2018-09-05)

Sure, no problem.

### aw...@google.com (2018-09-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-11-07)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2018-11-07)

This issue was migrated from crbug.com/chromium/848123?no_tracker_redirect=1

[Monorail blocked-on: crbug.com/chromium/827083, crbug.com/chromium/831073, crbug.com/chromium/848531, crbug.com/chromium/848535, crbug.com/chromium/849820]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091524)*
