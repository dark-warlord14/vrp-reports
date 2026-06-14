# Security: spell checking dictionaries are fetched over HTTP, and large responses lead to a crash

| Field | Value |
|-------|-------|
| **Issue ID** | [40081904](https://issues.chromium.org/issues/40081904) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>Language>Spellcheck |
| **CVE IDs** | CVE-2015-1288 |
| **Reporter** | [Deleted User] |
| **Assignee** | gr...@chromium.org |
| **Created** | 2015-04-21 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**

This bug is very similar (but different) to another that was worked recently, <https://code.google.com/p/chromium/issues/detail?id=477680>

This time the insecure URL is used when downloading spell checking dictionaries.

The code that needs to be updated to use HTTPS is: <https://code.google.com/p/chromium/codesearch#chromium/src/chrome/browser/spellchecker/spellcheck_hunspell_dictionary.cc&l=217>

An example insecure URL that is used is: <http://cache.pack.google.com/edgedl/chrome/dict/en-us-4-0.bdic>

The problem is that the insecure requests can be tampered with by an active network attacker to respond with a large response body which causes the Chrome process to allocate large amounts of memory and/or crash with SIGABRT.

Here is an example of what happens on the command line when subject to an active network attack:

> google-chrome --incognito  
> 
> [5989:5989:0421/090853:ERROR:url\_pattern\_set.cc(240)] Invalid url pattern: chrome://print/\*  
> 
> [5989:5989:0421/090854:ERROR:extension\_downloader.cc(695)] Invalid URL: '' for extension gmlllbghnfkpflemihljekbapjopfjik  
> 
> tcmalloc: large alloc 1073741824 bytes == 0x3cf8eed0000 @  
> 
> [5989:6024:0421/090915:FATAL:memory\_linux.cc(43)] Out of memory.  
> 
> Aborted (core dumped)

**VERSION**  

Chrome Version: 42.0.2311.90 stable  

Operating System: Ubuntu 14.04.2 LTS

**REPRODUCTION CASE**

1. simulate needing to download a new language by removing existing dictionaries: rm -rf ~/.config/google-chrome/Dictionaries
2. perform an active network attack that makes the request to <http://cache.pack.google.com/edgedl/chrome/dict/en-us-4-0.bdic> respond with a 1GB response (I generated a test file with: dd if=/dev/zero of=gig bs=1M count=1024).
3. now cause the browser to attempt to download the language. there are a few ways of achieving this. the most generic that i found was to:  
   
   a) navigate to <https://www.google.com/>  
   
   b) right click the mouse in the main search entry text box. doing so notices that the language needs to be downloaded and causes a crash. my intuition says that this occurs because of a need to populate the spelling portion of the context menu, although i did not verify that.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: entire browser sig abort  

Crash State: see screen shot and description above

## Attachments

- [spell-check-downloader-crash.png](attachments/spell-check-downloader-crash.png) (image/png, 146.6 KB)

## Timeline

### fe...@chromium.org (2015-04-21)

As far as you can tell, is the dictionary checked in any other way (eg hash verification), or could the attacker also provide you with incorrect spelling suggestions?

### [Deleted User] (2015-04-21)

There are some sanity checks on structure of the dictionary. But, I did not see any cryptographic signature checks. So, given a little playing around learning that file format, it may be possible to suggest incorrect spellings. These are the areas of the code that makes me think it's possible:

https://code.google.com/p/chromium/codesearch#chromium/src/chrome/browser/spellchecker/spellcheck_hunspell_dictionary.cc&l=180

https://code.google.com/p/chromium/codesearch#chromium/src/third_party/hunspell/google/bdict.cc

### [Deleted User] (2015-04-21)

I was able to inject the Afrikaans (af-ZA-3-0.bdic) dictionary in place of the US English one (en-US-4-0.bdic) and cause my spelling suggestions to be totally off.
I could probably create my own dictionary also as the only check looks like a md5sum of the a big part of the bdic file. But, that's not a signature which would require a signing key, just a md5 to verify the integrity of the file. So, yes, an injected response can change the suggestions.

### mb...@chromium.org (2015-04-21)

Adding OWNERS for spellchecker. Could one of you please take a look at this?

### rl...@chromium.org (2015-04-21)

[Empty comment from Monorail migration]

### gr...@chromium.org (2015-04-21)

I thought we had an MD5 signature check... Ah, yes: https://code.google.com/p/chromium/codesearch#chromium/src/third_party/hunspell/google/bdict_reader.cc&l=728

felt@: Yes, I'm aware of the security shortcomings around that MD5 check. Can we do a sec-audit of this whole area at some point?



### [Deleted User] (2015-04-22)

The MD5 would only assure integrity (of part of the bdic file), not authenticity. Basically, it only assures that what is sent/injected is what is received. The quick fix to get authenticity is to change the scheme to HTTPS in the URL at https://code.google.com/p/chromium/codesearch#chromium/src/chrome/browser/spellchecker/spellcheck_hunspell_dictionary.cc&l=217
Doing that would prevent being able to inject a tampered response to either crash the browser or alter the spelling suggestions.

### gr...@chromium.org (2015-04-22)

Sorry, misread your comment to imply there's no integrity check. Lack of coffee. As said above, I'm aware of the security issues only checking integrity.

While https sounds simple, it's not that easy in actuality. Currently pinging top people to find out how we can get there. TOP. PEOPLE ;) (https://www.youtube.com/watch?v=yoy4_h7Pb3M)


### gr...@chromium.org (2015-04-23)

[Empty comment from Monorail migration]

### bu...@chromium.org (2015-04-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/6703b5a51cedaa0ead73047d969f8c04362f51f1

commit 6703b5a51cedaa0ead73047d969f8c04362f51f1
Author: groby <groby@chromium.org>
Date: Sat Apr 25 02:46:16 2015

[Spellcheck] Switch to https download

Download dictionaries via https instead of http, preventing MITM
attacks against dicts. Plus, HTTPS 4 LYFE!

BUG=479162

Review URL: https://codereview.chromium.org/1056103005

Cr-Commit-Position: refs/heads/master@{#326954}

[modify] http://crrev.com/6703b5a51cedaa0ead73047d969f8c04362f51f1/chrome/browser/spellchecker/spellcheck_hunspell_dictionary.cc


### gr...@chromium.org (2015-04-25)

Top people have replied with top solutions. We should be done. 

### cl...@chromium.org (2015-04-25)

[Empty comment from Monorail migration]

### [Deleted User] (2015-04-26)

Top o' the mornin' to ya :)
Thanks for making the quick update. Do you think this will be eligible for a bounty for the report and/or location of the probable fix?

### fe...@chromium.org (2015-04-27)

[Empty comment from Monorail migration]

### ti...@google.com (2015-05-08)

Hey Mike - we'll take a look at this in our next panel round, though a reward is unlikely based purely on the low severity. Nevertheless, we'll take a look.

### ti...@google.com (2015-05-16)

[Empty comment from Monorail migration]

### ti...@google.com (2015-05-19)

Congratulations - $500 for this report!

Reward Panel notes: "attack surface of malformed dictonary files is significant enough for a reward".

The payments team will be in contact within two weeks and I'll update this bug with a CVE later on this evening, though keep in mind that this won't be made public until after M44.

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an established charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### [Deleted User] (2015-05-19)

Thanks for the reward and for the feedback on why it qualified. That helps guide direction of further research.

### [Deleted User] (2015-06-02)

Hi, I haven't heard from payments on this one yet.

### ti...@google.com (2015-06-08)

Yikes - thanks for the reminder. I'll chase this.

### ti...@google.com (2015-06-25)

[Empty comment from Monorail migration]

### [Deleted User] (2015-07-21)

Hi, just checking on this because I haven't seen the CVE assigned or the reward come through yet.

### ti...@google.com (2015-07-24)

Processing via our e-payment system can take up to two weeks, but the reward should be on its way to you. Thanks again for your help!

(Note: sorry for the delay here - it turns out in the new payment system, these payments were waiting for a second approval from me).

### ti...@google.com (2015-07-24)

@mbarbella - can you please help Mike out with a CVE?

### mb...@chromium.org (2015-07-24)

Assigning CVE-2015-1288 to this bug.

### cl...@chromium.org (2015-08-01)

Bulk update: removing view restriction from closed bugs.

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### la...@chromium.org (2017-04-27)

[Empty comment from Monorail migration]

[Monorail components: -UI>Browser>Spellcheck UI>Browser>Language>Spellcheck]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-28)

[Empty comment from Monorail migration]

### is...@google.com (2018-07-28)

This issue was migrated from crbug.com/chromium/479162?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081904)*
