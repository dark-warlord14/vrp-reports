# Steal local file contents by abusing liberal CSS parsing

| Field | Value |
|-------|-------|
| **Issue ID** | [40089692](https://issues.chromium.org/issues/40089692) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Loader, Blink>Storage |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | pv...@gmail.com |
| **Assignee** | mk...@chromium.org |
| **Created** | 2017-11-27 |
| **Bounty** | $2,000.00 |

## Description

Resources from file:/// do not define a Content-Type, hence, a malicious page can load any local resource as CSS and it will be interpreted as such, independently of the MIME type. This allows to exfiltrate data from cross-origin local files via a CSS injection. This is a small variation of @filedescriptor's <https://bugs.chromium.org/p/chromium/issues/detail?id=419383> bug.

Chrome seems to use the file extension as a hint for the MIME type and displays warnings when suspects that it's parsing an incorrect resource: "Resource interpreted as Stylesheet but transferred with MIME type text/html". This hint could be used to avoid content sniffing under file:///.

**VULNERABILITY DETAILS**  

The attack requires a victim to render a local malicious HTML page. I don't discuss how this can be done, but there are many ways to trick a user into it (force downloads, redirection from a local PDF, mail attachment, etc.,). Furthermore, I guess this can become specially useful in Android or Electron environments.

I show 3 PoCs exploiting this issue. All of them require 2 things:

- A fixed (or predictable) path to a file with sensitive information.
- Attacker's capability to inject content into that file.

Chrome's SQLite databases meet those 2 requirements and become ideal candidates for this attack. For example:

// Random page on the internet

<script>
document.cookie = "foo{}\\*{--:bar=1337"; // gets written into sqlite db after a few seconds
</script>

// Local file (open by default from ~/Downloads/)

<link rel="stylehseet" href="../Library/Application Support/Chrome/Default/Cookies">
<script>
var leak = getComputedStyle(document.body).getPropertyValue('--');
alert(leak);
</script>

The code above can work sometimes, but with huge files is hard to control the characters appearing before and after the injected payload, some of them breaking the CSS parsing. In order to increase the chance of success we need some kind of "file-massaging".

The PoCs below are not very reliable, but have been successfully tested in Chrome stable 62 and Canary 64 (on both Linux and OSX machines), and illustrate how these attacks can work.

PROBES OF CONCEPT

- PoC 1 - Cross-origin redirection leak:

File: redir.html

Description: The file '~/Library/Application Support/Google/Chrome/Default/Current Session' contains information about the current requests. Two interesting facts are that part of the information is encoded in UTF-16 (with this encoding we can reduce noisy chars breaking parsing), and that iframe's requests are perfectly collocated with the parent requests. Hence, we can iframe a cross-origin page and read the result of the redirection. We only need to ensure that the CSS parser is in a proper state by closing all previous blocks[1], for this we simply append an arbitrary amount of '}])' chars.

- PoC 2 - LocalStorage's SQLite leak (localstorage.html):

File: localstorage.html

Description: In this case we target leveldb files (~/Library/Application Support/Google/Chrome/Default/Local Storage/leveldb/). Since the data is directly stored and we completely control the binary representation, it's easy to encode our payload as UTF-16 and parse the CSS as such. Moreover, the filenames use incremental numeric values, so we can simply bruteforce them until we import the right one containing our injection.

This can leak information stored by other sites and extensions.

- PoC 3 - \*BONUS\* Cookie Monster:

File: cookiemonster.html

Description: As mentioned before, when a page sets a cookie (via JS or header) it is written into the local SQLite database after a few seconds. The table looks like this:

/\*  

creation\_utc INTEGER NOT NULL UNIQUE PRIMARY KEY,  

host\_key TEXT NOT NULL,  

name TEXT NOT NULL,  

value TEXT NOT NULL,  

path TEXT NOT NULL,  

expires\_utc INTEGER NOT NULL,  

secure INTEGER NOT NULL,  

httponly INTEGER NOT NULL,  

last\_access\_utc INTEGER NOT NULL,  

has\_expires INTEGER NOT NULL DEFAULT 1,  

persistent INTEGER NOT NULL DEFAULT 1,  

priority INTEGER NOT NULL DEFAULT 1,  

encrypted\_value BLOB DEFAULT '',  

firstpartyonly INTEGER NOT NULL DEFAULT 0  

\*/

The attacker can control the cookie's 'name' and 'path' (the value is encrypted), hence, it's easy to create a cookie with our payload as name and hope to be lucky and leak some cookies. One interesting fact is that new cookies are most of the time written before (from the file's offset perspective) than the old ones. The reason seems to be that SQLite allocates chunks of space to afterwards fill them from bottom to top (at least to some extent). This helps us, since we are interested in leaking the existent cookies (and the CSS parser will go top to bottom).

Unfortunately, special chars break the CSS most of the time, and it's unlikely to leak a whole cookie... We could try again with UTF-16, but to our despair, cookies do not allow NULL bytes :(

The only apparent solution seems to set a cookie with a valid value (ascii printable chars, w/o semicolons, equals or quotes) that when encrypted generates our desired payload. Easy, peasy. Let's invoke the gods of PoC||GTFO :D

Cookies are encrypted using AES-128 with CBC mode, with a fixed IV = 0x20202020202020202020202020202020. In Linux, the key is hardcoded[2] ("peanuts") and for key derivation it uses PBKDF2 with a single iteration and fixed salt ("saltysalt"). In OSX the key is unique and stored in the Keychain, so we'll focus only on Linux from now on.

It turns out that our payload "{}\*{--:(" is exactly 8 bytes long. This means that when encoded in UTF-16 it will occupy 16 bytes (8 + 8 NULL bytes)[3].

Illustration (payload, key, and IV are known and fixed):

```
       \*B0\*              payload               \*B2\*  
   [ 16 bytes ]-       [ 16 bytes ]-       [ 16 bytes]  
        |       |           |       |           |  
        v       |           v       |           v  
key ->(AES)     |   key ->(AES)     |   key ->(AES)  
        |       |           |       |           |  
        v       |           v       |           v  
 IV--->(+)      |--------->(+)      |--------->(+)  
        |                   |                   |  
        v                   v                   v  
       P0                  P1               P2 + padding  

```

We need to find a valid block B0 that when decrypted satisfy:

- P0's bytes are valid chars (this is a restriction of ~2 bits per byte, less than 32 bits of entropy).
- P1's bytes being valid chars. However, since the output of the payload's AES is fixed, we can limit the initial space search of B0 to make P1 = B0 ^ AES(key,payload) a valid plaintext.

We need to find a valid block B2 that when decrypted satisfy:

- P2 = payload ^ AES(key, B2) 's bytes are valid chars.
- P2's last byte = 0x01 (the cheapest valid padding).

Fortunately for us, B0 and B2 are independent. After a couple of minutes (few billions of AES encryptions on a 4 cores Skylake's i5)... We get a valid cookie value that when encrypted and stored in the db will contain our payload in UTF-16 form!

```
document.cookie="whatever=i+GW\*e@afGR]sYo{Wa>7[[[[[[[[[[[[xBLGWAJ|VCX<T\*P;"  

```

(You should set this cookie, via devtools for instance, and load the local HTML file ~40 seconds later)

With the cookie, we are ready to leak part of the cookie's database more reliably, decode the UTF-16, parse the encrypted values (which have a prefix 'v10'), and use the web crypto API to decrypt them. The attached PoC does that.

Note, however, that we only set a single cookie with one payload. That means that the test can fail if the UTF-16 payload is missaligned, or if the CSS parser breaks. An improved attack could set a few cookies with different values (--a, --b, --c) to increase the chance of success. In any case, I also attached an screenshot to show how a successful attacks looks like.

RECOMMENDATIONS

In addition to avoid content-sniffing, adding a random string to the profile's folder name (in a similar way than Firefox), would make these (and similar) attacks much harder.

Also, Firefox's CSS string parser is stricter and will stop after detecting a NULL byte, reducing notably the leakeage.

Seems reasonable (and cheap) to use a unique key per system even in Linux. I suppose that the motivation is that local attackers will find the key as well, but since an attacker can only have partial read access, that could safe some cows...

It's probably not a severe issue, but I had a lot of fun with it, hope you like it :D

[1] <https://www.w3.org/TR/css-syntax-3/#%7B%7D-block-diagram>  

[2] <https://cs.chromium.org/chromium/src/components/os_crypt/os_crypt_posix.cc?l=44>  

[3] It could occupy a few more bytes from the surrounding blocks, since we don't need the 16 bytes for finding a valid block.

## Attachments

- [redir.html](attachments/redir.html) (text/plain, 741 B)
- [localstorage.html](attachments/localstorage.html) (text/plain, 822 B)
- [cookiemonster.html](attachments/cookiemonster.html) (text/plain, 2.2 KB)
- [cookiemonster_screenshot.png](attachments/cookiemonster_screenshot.png) (image/png, 567.2 KB)

## Timeline

### el...@chromium.org (2017-11-28)

+mkwst, who's currently on the warpath against MIME-type issues. Requiring a proper file extension (e.g. treating file-served CSS files as if they have an X-Content-Type-Options: nosniff directive) seems like a reasonable mitigation.

### pa...@chromium.org (2017-11-28)

We should both require the right .css extension before treating it as a file, *and* tighten the CSS parsing. I don't think we should consider this bug fully Fixed until both things have been done.

Whichever is easier should be done ASAP, of course. Probably the file extension requirement.

Making saved local state less predictable on disk is a good mitigation also, but not fundamentally a solution.

Although this bug has lots of mitigating factors, the severity of successful exploitation is High or Critical. I'm marking the severity as Medium due to the many mitigating factors — but note the high quality of the bug report and the PoCs. I think we should consider rewarding this bug as if its severity were at least High.

nainar: Can you please take a look at this, or reassign to someone else who you think is more appropriate? Thank you! It's important to get this bug on the right track ASAP.

[Monorail components: Blink>CSS Blink>Storage]

### el...@chromium.org (2017-11-28)

The proposal in #1 is unfortunately probably not trivial, because the stylesheet code doesn't rely upon //net's Content-Type sniffing (which, for the file:// protocol, sets the MIME type based on the file's extension).

The code in bool CSSStyleSheetResource::CanUseSheet(MIMETypeCheck mime_type_check) notes:

  // Note that we grab the Content-Type header directly because we want to see 
  // what the value is BEFORE content sniffing. Firefox does this by setting a
  // "type hint" on the channel. This implementation should be observationally equivalent.
  //
*******
  // This code defaults to allowing the stylesheet for non-HTTP protocols so
  // folks can use standards mode for local HTML documents.
*******
  if (mime_type_check == MIMETypeCheck::kLax)
    return true;
  AtomicString content_type = HttpContentType();
  return content_type.IsEmpty() ||  // <-----------------------------------------------****
         DeprecatedEqualIgnoringCase(content_type, "text/css") ||
         DeprecatedEqualIgnoringCase(content_type,
                                     "application/x-unknown-content-type");
}

The |HttpContentType| function is literally looking at the |Content-Type| response header, which isn't set for resources from the file:// protocol.

If we do make a change here, we need to watch out for regressions in Android WebView; it turns out that some Android applications are dropping resources and loading them via extensionless file URIs (https://crbug.com/chromium/786150).

### na...@chromium.org (2017-11-29)

[Empty comment from Monorail migration]

### na...@chromium.org (2017-11-29)

Forked a separate bug for the CSS team's responsibility and marked it as blocking this. 

Unfortunately while our behaviour is vulnerable to security violations we are spec compliant, this will hence need some discussion. Also with branch point 2 days away, it seems like the change would be hard to land in M64. So I have marked the bug as M-65. Feel free to change if needed.

With re:to the file extension that is the loading team's purview not ours. So marking this as such. And marking it as Untriaged to add it to their triage rotation.

[Monorail components: -Blink>CSS Blink>Loader]

### na...@chromium.org (2017-11-29)

[Empty comment from Monorail migration]

### pa...@chromium.org (2017-11-29)

#56: We can get security fixes merged back into 64, and we should in this case.

Unfortunately, adding the Blink>Loader component (thanks!) isn't certain to get Loader people visibility into this bug. It's better to add people specifically. japhet, can you please take a look? Thanks!

### mk...@chromium.org (2017-11-29)

I'll poke at this today, since I've been giving this code the evil eye all week. I'll add a file extension requirement, a use counter, and tie it to a feature flag so we can disable it via Finch if it turns out to explode.

### mk...@chromium.org (2017-11-29)

Patch started at https://chromium-review.googlesource.com/c/chromium/src/+/795717. Adding a UseCounter in CSSStyleSheetResource is a bit of a pain but I think we probably need it. So. I'll keep poking at it.

### bu...@chromium.org (2017-11-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/56db65a6d5d214d238ca16a90fea118571d5c8e6

commit 56db65a6d5d214d238ca16a90fea118571d5c8e6
Author: Mike West <mkwst@chromium.org>
Date: Thu Nov 30 18:24:38 2017

Restrict `file:` stylesheets to `.css` extensions.

Bug: 788936
Change-Id: Icd4e22745561d57c691fd0f0e75bb8c3e4a59303
Reviewed-on: https://chromium-review.googlesource.com/795717
Commit-Queue: Mike West <mkwst@chromium.org>
Reviewed-by: nainar <nainar@chromium.org>
Reviewed-by: Jochen Eisinger <jochen@chromium.org>
Cr-Commit-Position: refs/heads/master@{#520610}
[modify] https://crrev.com/56db65a6d5d214d238ca16a90fea118571d5c8e6/content/child/runtime_features.cc
[modify] https://crrev.com/56db65a6d5d214d238ca16a90fea118571d5c8e6/content/public/common/content_features.cc
[modify] https://crrev.com/56db65a6d5d214d238ca16a90fea118571d5c8e6/content/public/common/content_features.h
[add] https://crrev.com/56db65a6d5d214d238ca16a90fea118571d5c8e6/third_party/WebKit/LayoutTests/fast/css/local-file-name-requirements-expected.txt
[add] https://crrev.com/56db65a6d5d214d238ca16a90fea118571d5c8e6/third_party/WebKit/LayoutTests/fast/css/local-file-name-requirements.html
[add] https://crrev.com/56db65a6d5d214d238ca16a90fea118571d5c8e6/third_party/WebKit/LayoutTests/fast/css/resources/red.not-css
[modify] https://crrev.com/56db65a6d5d214d238ca16a90fea118571d5c8e6/third_party/WebKit/LayoutTests/fast/html/imports/rel-style-to-import-expected.txt
[modify] https://crrev.com/56db65a6d5d214d238ca16a90fea118571d5c8e6/third_party/WebKit/Source/core/css/StyleSheetContents.cpp
[modify] https://crrev.com/56db65a6d5d214d238ca16a90fea118571d5c8e6/third_party/WebKit/Source/core/dom/ProcessingInstruction.cpp
[modify] https://crrev.com/56db65a6d5d214d238ca16a90fea118571d5c8e6/third_party/WebKit/Source/core/frame/Deprecation.cpp
[modify] https://crrev.com/56db65a6d5d214d238ca16a90fea118571d5c8e6/third_party/WebKit/Source/core/html/parser/CSSPreloadScanner.cpp
[modify] https://crrev.com/56db65a6d5d214d238ca16a90fea118571d5c8e6/third_party/WebKit/Source/core/inspector/InspectorPageAgent.cpp
[modify] https://crrev.com/56db65a6d5d214d238ca16a90fea118571d5c8e6/third_party/WebKit/Source/core/loader/resource/CSSStyleSheetResource.cpp
[modify] https://crrev.com/56db65a6d5d214d238ca16a90fea118571d5c8e6/third_party/WebKit/Source/core/loader/resource/CSSStyleSheetResource.h
[modify] https://crrev.com/56db65a6d5d214d238ca16a90fea118571d5c8e6/third_party/WebKit/Source/platform/exported/WebRuntimeFeatures.cpp
[modify] https://crrev.com/56db65a6d5d214d238ca16a90fea118571d5c8e6/third_party/WebKit/Source/platform/runtime_enabled_features.json5
[modify] https://crrev.com/56db65a6d5d214d238ca16a90fea118571d5c8e6/third_party/WebKit/public/platform/WebRuntimeFeatures.h
[modify] https://crrev.com/56db65a6d5d214d238ca16a90fea118571d5c8e6/third_party/WebKit/public/platform/web_feature.mojom
[modify] https://crrev.com/56db65a6d5d214d238ca16a90fea118571d5c8e6/tools/metrics/histograms/enums.xml


### mk...@chromium.org (2017-12-01)

+tabatkins@ for context.

### mk...@chromium.org (2017-12-01)

It looks like the `.css` restriction for `file:` landed in time for 64. Let's see if it sticks.

### pa...@chromium.org (2017-12-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-12-15)

mkwst: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2017-12-30)

mkwst: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ra...@chromium.org (2018-01-31)

mkwst: can this be marked fixed now? 

### el...@chromium.org (2018-02-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-07)

[Empty comment from Monorail migration]

### pv...@gmail.com (2018-03-30)

Hey, any updates on this? I'm curious about the current status of mitigations for file:// bugs. Is there any other open issue I can follow?

### sh...@chromium.org (2018-04-18)

[Empty comment from Monorail migration]

### rs...@chromium.org (2018-05-14)

mkwst: Is this fixed by the CL in #10 (don't see an associated revert), or is there more to do?

### sh...@chromium.org (2018-05-30)

[Empty comment from Monorail migration]

### pv...@gmail.com (2018-06-28)

Since the bug seems solved and there has been no recent activity, could the issue be made public?

I also wonder if the bug qualifies for a reward. Thanks.

### aw...@chromium.org (2018-06-28)

Marking as fixed sounds reasonable, and also getting it into the queue of bugs to be considered for reward.  Thanks for the ping!

### sh...@chromium.org (2018-06-29)

[Empty comment from Monorail migration]

### pv...@gmail.com (2018-06-29)

Cool :) Also, just for completness, here is the code I used for generating the right cookie: https://github.com/cgvwzq/aes_bf (yeah, shame on me for this crap)

### sh...@chromium.org (2018-07-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-01)

This bug requires manual review: M68 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), kariahda@(iOS), bhthompson@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cm...@chromium.org (2018-07-03)

 awhalley@ is this fix safe enough to be merged into M68?

### ab...@google.com (2018-07-06)

[Empty comment from Monorail migration]

### cm...@chromium.org (2018-07-11)

Ping!

### pa...@chromium.org (2018-07-11)

awhalley is OOO, and it looks like mkwst is too. I will attempt to answer, but, keep in mind that I am a fool.

Although the patch spans many files, it does not look particularly complicated. I also very much would like the fix to make it into 68. I would guess that if it merges cleanly into 68, then it's safe. But if there are any hiccups with the simple cherry-pick process, I'd say pass on it.

### bu...@chromium.org (2018-07-11)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-07-12)

I'm a little confused over what's to be merged? The change in #10's already out in stable since 64

### ab...@google.com (2018-07-13)

+1 to awhalley's question. 

### cm...@chromium.org (2018-07-17)

If this has to be in M68, then it has to be merged as soon as possible. M68 stable cut is today.

### aw...@google.com (2018-07-18)

We'll pick this up in 69

### aw...@chromium.org (2018-07-23)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-07-23)

Many thanks for the report, pvtolkien@! The VRP panel decided to award $2,000 for this report. How would you like to be credited in release notes?

### aw...@google.com (2018-07-23)

[Empty comment from Monorail migration]

### pv...@gmail.com (2018-07-23)

Thank you. Pepe Vila (@cgvwzq) should be fine.

### aw...@google.com (2018-08-16)

[Empty comment from Monorail migration]

### pv...@gmail.com (2018-08-27)

Hi, sorry for bothering you again, but after re-reading the comments I'm as confused as some of you. The merge was actually done in 64, so not sure why it has been marked as M68 and then M69. Is this due to another similar bug that's really being fixed in 69 or just some misunderstanding?

If it's the later, can we please make the ticket public? :)

Cheers,

### aw...@chromium.org (2018-09-04)

[Empty comment from Monorail migration]

### aw...@google.com (2018-09-04)

Looks like it was the latter - opening the bug. Pardon the confusion!

### bu...@chromium.org (2018-11-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/d913f72b4875cf0814fc3f03ad7c00642097c4a4

commit d913f72b4875cf0814fc3f03ad7c00642097c4a4
Author: Dave Tapuska <dtapuska@chromium.org>
Date: Mon Nov 12 21:08:29 2018

Remove RequireCSSExtensionForFile runtime enabled flag.

The feature has long since been stable (since M64) and doesn't seem
to be a need for this flag.

BUG=788936

Change-Id: I666390b869289c328acb4a2daa5bf4154e1702c0
Reviewed-on: https://chromium-review.googlesource.com/c/1324143
Reviewed-by: Mike West <mkwst@chromium.org>
Reviewed-by: Camille Lamy <clamy@chromium.org>
Commit-Queue: Dave Tapuska <dtapuska@chromium.org>
Cr-Commit-Position: refs/heads/master@{#607329}
[modify] https://crrev.com/d913f72b4875cf0814fc3f03ad7c00642097c4a4/content/child/runtime_features.cc
[modify] https://crrev.com/d913f72b4875cf0814fc3f03ad7c00642097c4a4/content/public/common/content_features.cc
[modify] https://crrev.com/d913f72b4875cf0814fc3f03ad7c00642097c4a4/content/public/common/content_features.h
[modify] https://crrev.com/d913f72b4875cf0814fc3f03ad7c00642097c4a4/third_party/blink/public/platform/web_runtime_features.h
[modify] https://crrev.com/d913f72b4875cf0814fc3f03ad7c00642097c4a4/third_party/blink/renderer/core/loader/resource/css_style_sheet_resource.cc
[modify] https://crrev.com/d913f72b4875cf0814fc3f03ad7c00642097c4a4/third_party/blink/renderer/platform/exported/web_runtime_features.cc
[modify] https://crrev.com/d913f72b4875cf0814fc3f03ad7c00642097c4a4/third_party/blink/renderer/platform/runtime_enabled_features.json5


### er...@microsoft.com (2019-06-18)

Observation: When Chrome saves a page (CTRL+S), it does not enforce that referenced stylesheets have their filename extension as .css. 

The CL landed in #10 means that reopening the page will result in the those stylesheet references getting ignored.

### aw...@chromium.org (2019-06-27)

[Empty comment from Monorail migration]

### is...@google.com (2019-06-27)

This issue was migrated from crbug.com/chromium/788936?no_tracker_redirect=1

[Multiple monorail components: Blink>Loader, Blink>Storage]
[Monorail blocked-on: crbug.com/chromium/789346]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40089692)*
