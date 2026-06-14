# Multiple vulnerabilities in sqlite; Cast is 1 attack vector/target

| Field | Value |
|-------|-------|
| **Issue ID** | [40092919](https://issues.chromium.org/issues/40092919) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Storage>WebSQL, Internals>Cast, Internals>Storage |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **CVE IDs** | CVE-2018-20346 |
| **Reporter** | le...@gmail.com |
| **Assignee** | pw...@chromium.org |
| **Created** | 2018-11-01 |
| **Bounty** | $10,337.00 |

## Description

**This template is ONLY for reporting security bugs. If you are reporting a**  

**Download Protection Bypass bug, please use the "Security - Download**  

**Protection" template. For all other reports, please use a different**  

**template.**

**Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com>**  

**/chromium/src/+/master/docs/security/faq.md**

**Please see the following link for instructions on filing security bugs:**  

**<https://www.chromium.org/Home/chromium-security/reporting-security-bugs>**

**Reports may be eligible for reward payments under the Chrome VRP:**  

**<http://g.co/ChromeBugRewards>**

**NOTE: Security bugs are normally made public once a fix has been widely**  

**deployed.**

**-------------------------**

**VULNERABILITY DETAILS**  

Vulnerabilities in Google Chrome could allow attacker to perform an RCE attack in Google Home (Chromecast) and Google Chrome

Hi,

Our team is now doing security auditing of Google Chrome, during the auditing, we have found that we could use castv2 to let the device to visit a designated webpage. Thus we could use vulnerabilities in Google Chrome to attack the Google Home device.

We have found many vulnerabilities in third-party library SQLite, so we could use the WebSQL to trigger those vulnerabilities.

Those vulnerabilties also affect Chrome, Webview and any Apps or programs that use those 2 products.

The vulnerabilties (defeats) are:

1. \*\*IMPORTANT\*\* The SQLite is using "assert()" to do security check, but Google products are compiling Chrome with NDEBUG defined in Release Build, and the "assert()" turns to "void()", this compiling option disabled almost every key security checks in SQLite. The same thing happens in SQLite Release build too.
2. The "merge" action in fts3 extension could allow an attacker to leak heap data or cause heap buffer overflow.
3. The "match" action (fts3ScanInteriorNode) in fts3 extension is vulnerable to integer overflow, and could allow an attacker to leak memory data or cause heap buffer overflow, but the "match" seems not working in Chrome, so we can only get it triggered only in sqlite shell now.
4. The fts3SegReaderNext in fts3 extension is vulnerable to integer overflow, and could allow an attacker to leak memory data or cause heap buffer overflow.
5. A minor problem for Chrome, wrong primary key constraints will cause Denial of Service of database service (2 places)

We are mainly using the vuln. (1) and (2) to perform the attack.

ATTACK VECTORS FOR GOOGLEHOME

ATTACK REMOTELY:  

The GoogleHome device supports the castv2 protocol. An attacker can create a cast app and push any web page to Google Home for remote attacks.

SPECIFIC STEPS:

1. After the attacker registers as a cast developer, the cast app can be developed and published. The CAST RECEIVER URL can be specified as a web page with a malicious payload. (We have already registered one.)
2. The attacker tricks the victim to visit the CAST SENDER URL, which searches for the Google Home at the victim's home and triggers it to visit the CAST RECEIVER URL;
3. The CAST RECEIVER URL is the malicious page containing the payload for RCE. After visit that web page, the Google Home would be controlled by the attacker.

ATTACK WITHIN THE LAN:  

At the same time, if the attacker and the Google Home are in the same LAN, the attacker can send the castv2 protocol (such as the LAUNCH APP request) to port 8009. This will directly trigger Google Home to access the CAST RECEIVER URL, which triggers RCE.

---

We have succeessfully performed code execution in sqlite3 shell application,

Leaking the base address in Chromium on Ubuntu, Google Home, chromecast, and we are still working for the code execution on those platforms, and it may take some time.

\*\*  

Please check the attachment [Detailed report of vuln 1 to 5.doc] for the detailed report.

In [screenshots.zip]:  

For a victim visit a webpage, then cast the malicious code to Google Home, please check:  

cast.mov

While attacker and the victim in the same network, attacker could do it silently, please check:  

launch\_app.py in [PoCA.zip]

The Screenshot for (2) is :  

2-leaking-Google Home.jpg  

2-leaking-Google Home.mov (Now it is leaking some random bytes, we are still working for a more stable leak. You can try to run leak-02-leaking-random-bytes.html till it leak an address :) )  

2-leaking-chrome72-ubuntu.png  

2-crashing-chrome72-ubuntu.png  

2-leaking-function-addr-sqlite-shell.png  

2-PC-set-to-0x41414140-sqlite-shell.png

The Screenshot for (3) is :  

3-crashing-sqlite-shell.png

The Screenshot for (5) is :  

5-crashing-a-chrome72-ubuntu.png  

5-crashing-b-chrome72-ubuntu.png

Environment of ubuntu machine:  

Chromium 72.0.3589.0 installed on ARM 32bit PC  

Environment of Android machine:  

Chromium 70.0.3538.80 installed on ARM 64bit Android 9.0.0 (Pixel XL)  

\*\*

For detailed advises please also check [Detailed report of vuln 1 to 5.doc].

We are still working for a full PoC, when we have any new discoveries, we will send it to this thread.

Repair Advices(Simplified):

1. Change all assert() to "if (!...) abort();";
2. Prevent user from modifing the built-in tables, such as %\_segdir, %\_segments ...
3. The memory growth algorithm (if n is greater than allocated, then reallocate with a larger size) is copied and modified everywhere amoung the sqlite project, and many are vulnerable to integer overflow (there are several places are using realloc((int)n \* 2) then memcpy with size n. For example if n is 0x80000001, the result in 32bit will be 2, on 64-bit systems, this could lead to a buffer overflow), maybe it is better to encapsule them to one function.

\*\*\*\* We'd like to publish some articles on our medias in recent days to promote the progress that our team has discovered (mostly promoting, not many technology related) if these vuln are confirmed, we will not talk about any detail of the vulnerabilities within 90 days from the day you have confirmed these vulnerabilities, is it sounds OK for you? Or do you need to contact our PR crew to know the details?

We are Tencent Blade Team, which was founded by Tencent Security Platform Department, our team is dedicated in security researches of AI, mobile Internet, IoT, wireless and other cutting-edge technologies. (<https://blade.tencent.com/index_en.html>). For the press related thing, you may also contact our crew via [blade@tencent.com](mailto:blade@tencent.com).

**VERSION**  

Chrome Version: 72.0- (include the newest Webview)  

Operating System: Linux,Android,Windows,OSX

**REPRODUCTION CASE**  

The (1) is a compiling problem, you can see there is no abort() in sqlite part in Chrome release build. If those asserts are present in the Chrome, the exploit won't be successed.  

For (2), please check the attachment POCA.ZIP  

For (3) and (5), please check the attachment POCB.ZIP  

For (4), the (2) has covered its exploiting route, so the POC is inside POCA.ZIP.

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Wenxiang Qian of Tencent Blade Team

## Attachments

- [Detailed report of vuln 1 to 5.docx](attachments/Detailed report of vuln 1 to 5.docx) (application/octet-stream, 223.9 KB)
- [PoCA.zip](attachments/PoCA.zip) (application/octet-stream, 4.5 KB)
- [PoCB.zip](attachments/PoCB.zip) (application/octet-stream, 2.2 KB)
- [hijackpc_in_sqlite3shell(not related to chrome).docx](attachments/hijackpc_in_sqlite3shell(not related to chrome).docx) (application/octet-stream, 309.0 KB)
- [02-heap-buffer-overflow.html](attachments/02-heap-buffer-overflow.html) (text/plain, 1.6 KB)
- [PoC_for_sqlite3.zip](attachments/PoC_for_sqlite3.zip) (application/octet-stream, 2.2 KB)
- [debug.jpg](attachments/debug.jpg) (image/jpeg, 276.0 KB)
- [poc_updated_nov16.zip](attachments/poc_updated_nov16.zip) (application/octet-stream, 146.5 KB)
- [running_result.png](attachments/running_result.png) (image/png, 155.4 KB)
- [crash-03-update.html](attachments/crash-03-update.html) (text/plain, 848 B)
- deleted (application/octet-stream, 0 B)

## Timeline

### le...@gmail.com (2018-11-01)

[Comment Deleted]

### le...@gmail.com (2018-11-01)

[Comment Deleted]

### le...@gmail.com (2018-11-01)

[Comment Deleted]

### le...@gmail.com (2018-11-01)

[Comment Deleted]

### pa...@chromium.org (2018-11-01)

Thanks for your report! In the future, please attach plain text files instead of .docx. Also generally PoCs are more useful to us than screenshots. But this is all good info, so thank you. :)

If I understand correctly, these are all bugs in upstream sqlite. We can mitigate some of them in Chromium by not building with NDEBUG, but ultimately we're going to need to get these things fixed upstream. Have you reported these bugs to sqlite?

jsbell/sqlite crew: Is there some extremely good reason we can't turn off NDEBUG/enable assert? It's too bad that upstream uses assert for safety checks (hopefully they'll fix that), but they are, so we need them.

I am not sure the Cast attack vector is something we can/will fix; it sounds like Cast working as intended, except for the sqlite vulnerabilities. Cast crew: does that sound true to you?

[Monorail components: Blink>Storage>WebSQL Internals>Cast Internals>Storage]

### pa...@chromium.org (2018-11-01)

[Empty comment from Monorail migration]

### ha...@chromium.org (2018-11-01)

+dougsteed.
Yes, Cast is WAI here in the sense that it allows users to load a web page on a Cast device on the same LAN.

### ha...@chromium.org (2018-11-01)

[Empty comment from Monorail migration]

### pw...@chromium.org (2018-11-01)

For better or for worse, I own SQLite these days...

First, SQLite impacts startup performance. Enabling asserts would have to deal with that.

Second, I suspect we'd only be compiling the sqlite .c header with NDEBUG, not every module that depends on sqlite. This means we'll be compiling the .c files with a different set of flags than sqlite3.h file, which makes me worry about ODR-like weirdness. The header looks fine now, but every SQLite upgrade would have to check that the flag mismatch isn't a problem.

I'd strongly prefer that we find a better path. I'll follow up offline to discuss options.

### pa...@chromium.org (2018-11-01)

[Empty comment from Monorail migration]

### le...@gmail.com (2018-11-02)

OK :). Sure next time I will post text files instead. I'd also like to add a new PoC, which I have forgot to upload yesterday. It demonstrates how to overflow a heap buffer of vuln (2). 

The memory leaking and the heap buffer overflow shares the same code path. 

In this PoC, the 8002 part means the size. It is calculated by fts3GetVarint32.
For example, this PoC will copy  8002 (0x100 bytes) data from the byte after 8002 to the buffer, this will often cause the buffer overflow.

If you change the 8002 to 06, means it will only copy 6 bytes after it, and this could leak 6 bytes every time you run the code, you can run it as many times as it doesn't crash. 

  tx.executeSql("update x_segdir set root = x'000431323334020000000101010001010101000101018002';");

We are working for a full PoC to overwrite the handler of fts3 tokenizer object to  control PC register, when we have more discoveries we will reply in this thread.



### le...@gmail.com (2018-11-02)

Have you reported these bugs to sqlite?
---------
Not yet, I couldn't find an email address or some place to contact them, I asked them how to report vulnerabilities to them on their mailing list but I haven't got replied so far. 


### pa...@chromium.org (2018-11-03)

[Empty comment from Monorail migration]

### pw...@chromium.org (2018-11-03)

The above seems to be true. I vaguely remember that SQLite used to have a dedicated address for reporting security bugs, but it seems to have disappeared from their site.

I don't think that having access to the internal FTS3 tables is a security vulnerability in itself. Removing this access will definitely harden us, but SQLite should not have UB if the database gets corrupted on disk. Having user code mess with these tables looks just like corruption.

The other suggestions in the doc look very sensible. Thank you very much,  leonwxqian@!

### pw...@chromium.org (2018-11-03)

Thank you very much for looking into this, Richard!

### dr...@gmail.com (2018-11-03)

Thanks for including me in the report.  Can you also add dan@sqlite.org (or danielk1977@gmail.com) to the access list for this so that he can also see the full report and make replies?

We are all over this and should have a fix (or fixes) for you soon.

One minor point:  SQLite *never* uses assert() for security checking.  At least not deliberately.  If you ever find any way to make an assert() fire in SQLite, that is a bug in and of itself.  We only use assert() to express invariants.  SQLite automatically disables all assert() statements, unless compiled with -DSQLITE_DEBUG.  Because assert() is disabled in release builds, we use assert() in performance critical areas, and performance drops by 3x or more when assert() is enabled.  Our recommendation is that we fix the actual bugs in SQLite (and any assert() failures are an actual bug) rather than turning on assert() in all builds.

You can always send vulnerability reports (or any other bug reports) for SQLite to support@sqlite.org.  At any time.

### pw...@chromium.org (2018-11-03)

Adding Dan from SQLite, for more eyes. Thank you very much for your quick response!

### le...@gmail.com (2018-11-04)

Thank you @drhsql @pwnall ! I've repacked those PoC files which you could test in sqlite3 shell, please check the attachment. 

Thank you for your explanations, now I understand why there're asserts() there. Would it be better to change some of asserts in the functions related FTS blob parsing of internal tables (%_segments, %_stats ...), to if (!..) return SQLITE_ERROR? Especially those functions with memory operation such as memcpy().

I think blob parsing in FTS extensions are very tricky and risky -- those binary blobs represent for some data structs in different extensions (BTree Node, RTree Node...), and they are often calling memcpy() to read & copy data from the blob. 

If having access to internal FTS tables are working as designed, with out assert() the internal node could be modified by attackers again and again in Release build to mislead the code.


### dr...@gmail.com (2018-11-04)

@leonwxq: If you want, please try out your PoCs on the latest trunk check-in for SQLite.  I think the major problems have been fixed.

However, we still have a lot more testing to do before we are done.  Also, we intend to implement additional measures for defense-in-depth.  For example, we are planning to make the shadow tables of FTS3 (and all other virtual tables that we control) read-only so that they cannot be changed by ordinary SQL. There are additional plans for other defensive measures.  And, we are planning a new document that summarizes the defensive strategies built into SQLite and how to best employ them.  We will follow-up in a few days once all changes have been implemented and tested.

@pwnall:  I'm assuming you will be wanting all of these changes on a new emergency patch release (version 3.25.3) to occur sometime next week rather than waiting for the next regularly scheduled release in December, right?

### le...@gmail.com (2018-11-05)

Thank you very much for your time and all your work! I will try out the latest trunk code.

### dr...@gmail.com (2018-11-05)

SQLite version 3.25.3, now uploaded on the SQLite website, should close the
specific vulnerabilities identified by this ticket.  Additional hardening of SQLite is underway and will appear in subsequent releases.

### pa...@chromium.org (2018-11-06)

#21: Wonderful, thanks!

pwnall: We can close this bug as Fixed once we've updated the SQLite we ship in Chromium.

### dr...@gmail.com (2018-11-06)

I don't know what your policies are regarding when to close bugs, but perhaps you should consider keeping the bug open until we can get our enhanced defenses into SQLite in the next release.  That way, this bug can serve as a reminder to incorporate and integrate those forthcoming enhancements when they are available.

Or, if you prefer, I can simply send you an out-of-band reminder emails when the enhancements become available.

### pa...@chromium.org (2018-11-06)

#23: Thanks. Our goal is to track latest stable to the greatest extent possible, so in theory we'd pick up your new defenses shortly after they become available. But we'll keep this bug open for now.

### dr...@gmail.com (2018-11-06)

The new defenses we are working on in SQLite cannot be enabled by default, as doing so might break legacy applications.  The new defenses do things like disable "PRAGMA writable_schema=ON" and make the shadow tables of FTS3 (and RTREE and FTS5) read-only to ordinary SQL.  These restrictions prevent ordinary SQL statements from deliberately corrupting the database file, thus reducing the attack surface and making future zero-day exploits less likely.

I think it is probably fine to turn on those restrictions in WebSQL. But for ordinary applications (which is to say, applications that do not accept and run arbitrary SQL from a potential attacker) there are probably a few of them out there that use those features and would break if the new restrictions were suddenly turned on by default. We don't want to break legacy applications, so I think we need to leave the new defenses turned off by default.

Which in turn means that if you want to make use of the new defenses when they become available, it is more than just recompiling with the latest code. You will also need to add either a compile-time option or start-time option to activate the higher level of defense.  (We are still working through the details on exactly how that will be done.)

However this all works out, I will let you know.

### le...@gmail.com (2018-11-07)

Hi, we'd like to publish some articles on our medias in this week to promote the progress that our team has made on security (mostly promotion, we will not talk about any detail of the vulnerabilities now, For example, we will just say we can now successfully leak base address and can almost do code execution in LAN on Google Home), does it sounds OK for you? 

### lc...@chromium.org (2018-11-08)

Hi leonwxqian@,

Thanks again for reporting these vulnerabilities. Regarding publishing your findings, when do you guys plan to publish it? Thanks.

### do...@chromium.org (2018-11-08)

[Empty comment from Monorail migration]

### le...@gmail.com (2018-11-09)

Hi lcwu@,
We are planning to publish an article at later today on Chinese media, in this article, we will not talk about any detail of the vulnerability.

We will only mention that "some vulnerabilities is confirmed and we can now successfully do code execution in LAN on Google Home".

And we are planning to go full disclosure after 104 days (90 days + 2 weeks) from the day you have confirmed those vulnerabilities.

### do...@chromium.org (2018-11-09)

Hi leonwxqian@,

On Nov 7, you said "can almost do code execution in LAN on Google Home" and today you say "can now successfully do code execution in LAN on Google Home". Can you give further details of this ?

### wz...@chromium.org (2018-11-09)

Hi Tencent team,

Thanks for reporting the vulnerabilities.

Reading hijackpc_in_sqlite3shell(not related to chrome).docx, I can see that you are able to modify callback address by heap overflow and so hijack PC.

However, ARM linux supports NX, so even you are able to modify PC and point it to a heap or stack address (data page), it shouldn't be able to execute further.

Have you been able to hijack PC and successfully execute code injection?

Regards,

### wz...@chromium.org (2018-11-09)

Don't get me wrong. Both illegal access to data alone and hijacking PC are already bad enough...

But code injection would bring the threat to another level...

### le...@gmail.com (2018-11-11)

[Comment Deleted]

### le...@gmail.com (2018-11-11)

[Comment Deleted]

### le...@gmail.com (2018-11-11)

[Comment Deleted]

### pw...@chromium.org (2018-11-11)

drhsqlite@: Thank you very much for the quick fixes and for making an emergency release!

(not related to the security bug)
Ideally, all configuration done via a PRAGMA would also have a sqlite3_ API call and/or a compile-time flag to set the default value. This would (eventually) let us disable PRAGMA support altogether, and give us better control over how Chrome features use SQLite. This is not relevant to WebSQL, because we already disallow PRAGMA there, but would help overall code health.

I haven't had the bandwidth to do this work, so I don't know which of the PRAGMAs we currently use have the needed API support. I'm sharing this thought because you mentioned you're deciding how to expose FTS3 hardening.

### le...@gmail.com (2018-11-12)

[Comment Deleted]

### lc...@chromium.org (2018-11-12)

[Empty comment from Monorail migration]

### le...@gmail.com (2018-11-13)

[Comment Deleted]

### le...@gmail.com (2018-11-16)

Update the Poc of https://crbug.com/chromium/900910#c33.

Removed all send() socket()... APIs in shellcode, which is generated automatically by software before.

We've replaced them with 1. modify RO navigator.appName 2. repair the stack/heap data after the exploit 3. use fetch() in the callback, to send the reqeust to attacker.

The offset for chrome 69 can be modified in conf.py.
**
Chrome version:
66.0.3359.120

### bu...@chromium.org (2018-11-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/a74f8ccd14cd7b02cda48cf4b46942739ef840eb

commit a74f8ccd14cd7b02cda48cf4b46942739ef840eb
Author: Max Moroz <mmoroz@chromium.org>
Date: Fri Nov 16 17:40:38 2018

SQLite: define SQLITE_DEBUG if (is_debug || dcheck_always_on).

We use this flag on OSS-Fuzz and trigger various asserts with fuzzing:
https://bugs.chromium.org/p/oss-fuzz/issues/list?can=1&q=label%3AProj-sqlite3&colspec=ID+Type+Component+Status+Proj+Reported+Owner+Summary&cells=ids


R=palmer@chromium.org, pwnall@chromium.org

Bug: 900910
Change-Id: I223ad95a9626e016c99ed5cecbf6f084cba8f331
Reviewed-on: https://chromium-review.googlesource.com/c/1315959
Commit-Queue: Max Moroz <mmoroz@chromium.org>
Reviewed-by: Chris Palmer <palmer@chromium.org>
Reviewed-by: Victor Costan <pwnall@chromium.org>
Cr-Commit-Position: refs/heads/master@{#608840}
[modify] https://crrev.com/a74f8ccd14cd7b02cda48cf4b46942739ef840eb/third_party/sqlite/BUILD.gn


### pw...@chromium.org (2018-11-17)

[Empty comment from Monorail migration]

### pw...@chromium.org (2018-11-17)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-11-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/ece6d6a2e2c3ef560debfa026dc00d8b56e80ec7

commit ece6d6a2e2c3ef560debfa026dc00d8b56e80ec7
Author: Victor Costan <pwnall@chromium.org>
Date: Thu Nov 22 10:22:57 2018

sqlite: Re-enable ENABLE_SQLITE_API_ARMOR outside fuzzers.

https://crrev.com/c/1315959 and https://crrev.com/c/1341921 made it
possible to use SQLITE_DEBUG for SQLite fuzzers, which has uncovered
bugs. Unfortunately, the CLs unintentionally removed
ENABLE_SQLITE_API_ARMOR from non-fuzzing builds, reducing our ability to
catch API misuse.

This CL re-instates ENABLE_SQLITE_API_ARMOR for non-fuzzing builds, for
the reasons described above. It also removes
-Wno-implicit-function-declaration in return for a less intrusive
workaround in sqlite3_shim.c.

Bug: 900910
Change-Id: I6327fdcee173c384da0b3b62c1414b7b6126473f
Reviewed-on: https://chromium-review.googlesource.com/c/1345649
Commit-Queue: Victor Costan <pwnall@chromium.org>
Reviewed-by: Max Moroz <mmoroz@chromium.org>
Cr-Commit-Position: refs/heads/master@{#610362}
[modify] https://crrev.com/ece6d6a2e2c3ef560debfa026dc00d8b56e80ec7/third_party/sqlite/BUILD.gn
[modify] https://crrev.com/ece6d6a2e2c3ef560debfa026dc00d8b56e80ec7/third_party/sqlite/sqlite3_shim.c


### pw...@chromium.org (2018-11-26)

I think we have a SQLite release (3.25.3 + one patch) that mitigates the security issues described here and doesn't crash.

drhsqlite@, danielk1977@: Thank you very much for your help in tracking down the crashers!

palmer@: We're in good shape for M72, but I think the disclosure window is going to overlap with M71 as well. The safest option I see is to land one CL on M71 that includes all the SQLite changes (upgrade, build flag changes, patch) in M72. The only alternative I can think of is fast-tracking M72 so it gets deployed before the disclosure.

Can you help us reason about this?

### pa...@chromium.org (2018-11-27)

+mpdenton FYI
+awhalley to see if I'm wrong about my response to #45

#45: We don't generally fast-track releases for the sake of a single security bug. Therefore I'd say your idea of landing the 1 CL in the 71 branch is the way to go.

### aw...@google.com (2018-11-27)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-11-27)

This bug requires manual review: We are only 6 days from stable.
Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), kbleicher@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@google.com (2018-11-27)

[Empty comment from Monorail migration]

### aw...@google.com (2018-11-27)

thanks palmer@

I agree this will be good to try and squeeze into M71. The changes in 41 and 44 have both been release in a Dev release, and been on Canary for 5 and 11 days, so a change that bring 71 into the same state sounds good to me. Thanks!

### go...@chromium.org (2018-11-27)

Approving merge to M71 branch 3578 based on comments #45, #46, #50 and per offline chat with  awhalley@. Pls merge ASAP. Thank you.

### bu...@chromium.org (2018-11-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/c368e30ae55600a1c3c9cb1710a54f9c55de786e

commit c368e30ae55600a1c3c9cb1710a54f9c55de786e
Author: Victor Costan <pwnall@chromium.org>
Date: Wed Nov 28 01:16:41 2018

sqlite: Upgrade to the 3.25.3 code in M72.

This CL pulls //third_party/sqlite from M72. The original sources in
//third_party/sqlite/sqlite-src-* were not changed, to avoid making the
diff even bigger than it already is.

This CL also pulls changes to //sql and //third_party/blink from the
following commits that landed in M72:

c6d3a866083891cf6cd935091ea877fa507d14a2
9a6c08e6e8436b8e1bae14a736a5db684287f939

The changes above are needed by the SQLite upgrade.

Tested: full debug build (compilation errors in tests were in unrelated
files), ran browser_tests, content_unittests, sql_unittests and the
LayoutTests in storage/websql/

TBR=cmumford

Bug: 900910
Change-Id: I562b92883101d9cdfba89a28295d1b176ad48138
Reviewed-on: https://chromium-review.googlesource.com/c/1352694
Reviewed-by: Victor Costan <pwnall@chromium.org>
Cr-Commit-Position: refs/branch-heads/3578@{#835}
Cr-Branched-From: 4226ddf99103e493d7afb23a4c7902ee496108b6-refs/heads/master@{#599034}
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/sql/database.cc
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/WebKit/LayoutTests/storage/websql/test-authorizer-expected.txt
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/WebKit/LayoutTests/storage/websql/test-authorizer.js
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/blink/renderer/modules/webdatabase/database_authorizer.cc
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/blink/renderer/modules/webdatabase/sqlite/sqlite_file_system.cc
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/BUILD.gn
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/README.chromium
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/amalgamation/rename_exports.h
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/amalgamation/shell/shell.c
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/amalgamation/sqlite3.c
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/amalgamation/sqlite3.h
[delete] https://crrev.com/9f3cc28b53360f25187d30e9908d92d7d8abdd5c/third_party/sqlite/fuzz/ossfuzz.c
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/fuzz/sql.dict
[delete] https://crrev.com/9f3cc28b53360f25187d30e9908d92d7d8abdd5c/third_party/sqlite/fuzz/sqlite3_prepare_v2_fuzzer.cc
[delete] https://crrev.com/9f3cc28b53360f25187d30e9908d92d7d8abdd5c/third_party/sqlite/fuzz/sqlite3_prepare_v2_fuzzer.dict
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/patches/0001-test-SQLite-tests-compiling-on-Linux.patch
[rename] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/patches/0002-Modify-default-VFS-to-support-WebDatabase.patch
[delete] https://crrev.com/9f3cc28b53360f25187d30e9908d92d7d8abdd5c/third_party/sqlite/patches/0002-Use-seperate-page-cache-pools-for-each-sqlite-connec.patch
[rename] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/patches/0003-Virtual-table-supporting-recovery-of-corrupted-datab.patch
[rename] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/patches/0004-Custom-shell.c-helpers-to-load-Chromium-s-ICU-data.patch
[rename] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/patches/0005-fts3-Disable-fts3_tokenizer-and-fts4.patch
[add] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/patches/0006-fts3-Fix-uninit-variable-in-fts3EvalDeferredPhrase.patch
[rename] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/patches/0007-Allow-auto-vacuum-to-work-with-chunks.patch
[delete] https://crrev.com/9f3cc28b53360f25187d30e9908d92d7d8abdd5c/third_party/sqlite/patches/0007-fts3-Interior-node-corruption-detection.patch
[delete] https://crrev.com/9f3cc28b53360f25187d30e9908d92d7d8abdd5c/third_party/sqlite/patches/0008-fts3-Fix-uninit-variable-in-fts3EvalDeferredPhrase.patch
[rename] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/patches/0008-fuchsia-Use-dot-file-locking-for-sqlite.patch
[add] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/patches/0009-Fix-ossfuzz.c-to-compile-and-run-with-our-config.patch
[add] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/patches/0010-Backport-Windows-VFS-mmap-fix.patch
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/scripts/generate_amalgamation.sh
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/sqlite3_shim.c
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/Makefile.in
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/Makefile.msc
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/README.md
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/VERSION
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/autoconf/Makefile.am
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/autoconf/Makefile.msc
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/autoconf/configure.ac
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/configure
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/configure.ac
[add] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/doc/F2FS.txt
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/ext/expert/expert1.test
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/ext/fts3/fts3.c
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/ext/fts3/fts3Int.h
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/ext/fts3/fts3_write.c
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/ext/fts3/unicode/mkunicode.tcl
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/ext/fts3/unicode/parseunicode.tcl
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/ext/fts5/fts5.h
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/ext/fts5/fts5Int.h
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/ext/fts5/fts5_expr.c
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/ext/fts5/fts5_index.c
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/ext/fts5/fts5_main.c
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/ext/fts5/fts5_tokenize.c
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/ext/fts5/fts5_unicode2.c
[add] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/ext/fts5/test/fts5cat.test
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/ext/fts5/test/fts5rank.test
[add] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/ext/fts5/test/fts5unicode4.test
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/ext/lsm1/lsm-test/lsmtest1.c
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/ext/lsm1/lsm-test/lsmtest_tdb3.c
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/ext/lsm1/lsm_sorted.c
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/ext/misc/completion.c
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/ext/misc/dbdump.c
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/ext/misc/fileio.c
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/ext/misc/json1.c
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/ext/misc/normalize.c
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/ext/rbu/rbu.c
[add] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/ext/rtree/geopoly.c
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/ext/rtree/rtree.c
[add] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/ext/rtree/util/randomshape.tcl
[add] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/ext/rtree/visual01.txt
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/ext/userauth/userauth.c
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/main.mk
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/manifest
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/manifest.uuid
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/src/alter.c
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/src/analyze.c
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/src/attach.c
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/src/auth.c
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/src/backup.c
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/src/btree.c
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/src/btree.h
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/src/build.c
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/src/ctime.c
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/src/dbpage.c
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/src/delete.c
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/src/expr.c
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/src/fkey.c
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/src/func.c
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/src/insert.c
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/src/loadext.c
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/src/main.c
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/src/memdb.c
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/src/os.c
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/src/os_unix.c
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/src/os_win.c
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/src/pager.c
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/src/pager.h
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/src/parse.y
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/src/pcache1.c
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/src/pragma.c
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/src/pragma.h
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/src/prepare.c
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/src/printf.c
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/src/resolve.c
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/src/rowset.c
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/src/select.c
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/src/shell.c.in
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/src/sqlite.h.in
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/src/sqlite3ext.h
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/src/sqliteInt.h
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/src/tclsqlite.c
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/src/test1.c
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/src/test3.c
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/src/test_config.c
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/src/test_tclsh.c
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/src/test_vfs.c
[add] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/src/test_window.c
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/src/tokenize.c
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/src/treeview.c
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/src/trigger.c
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/src/update.c
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/src/upsert.c
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/src/vacuum.c
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/src/vdbe.c
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/src/vdbe.h
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/src/vdbeInt.h
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/src/vdbeapi.c
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/src/vdbeaux.c
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/src/vdbemem.c
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/src/vdbesort.c
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/src/vtab.c
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/src/wal.c
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/src/wal.h
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/src/walker.c
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/src/where.c
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/src/whereInt.h
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/src/wherecode.c
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/src/whereexpr.c
[add] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/src/window.c
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/test/aggnested.test
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/test/all.test
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/test/alter.test
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/test/alter4.test
[add] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/test/alterauth.test
[add] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/test/altercol.test
[add] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/test/alterlegacy.test
[add] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/test/altermalloc2.test
[add] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/test/altertab.test
[add] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/test/altertab2.test
[add] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/test/atomic2.test
[add] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/test/atrc.c
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/test/auth.test
[add] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/test/bestindex6.test
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/test/btree02.test
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/test/corrupt2.test
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/test/corrupt3.test
[add] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/test/countofview.test
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/test/cursorhint2.test
[add] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/test/dataversion1.test
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/test/e_createtable.test
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/test/e_select.test
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/test/eqp.test
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/test/fkey2.test
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/test/fts3ao.test
[add] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/test/fts3corrupt4.test
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/test/fuzzcheck.c
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/test/fuzzdata2.db
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/test/fuzzdata4.db
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/test/fuzzdata5.db
[add] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/test/in6.test
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/test/insert.test
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/test/json103.test
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/test/like3.test
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/test/limit2.test
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/test/lookaside.test
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/test/mmap1.test
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/test/normalize.test
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/test/orderby5.test
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/test/ossfuzz.c
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/test/permutations.test
[add] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/test/pg_common.tcl
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/test/releasetest.tcl
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/test/resetdb.test
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/test/rowvalue.test
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/test/rowvalue4.test
[add] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/test/schemafault.test
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/test/select5.test
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/test/selectD.test
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/test/server1.test
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/test/shell1.test
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/test/skipscan1.test
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/test/snapshot.test
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/test/snapshot2.test
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/test/snapshot3.test
[add] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/test/snapshot4.test
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/test/snapshot_fault.test
[add] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/test/snapshot_up.test
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/test/tclsqlite.test
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/test/tester.tcl
[add] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/test/tkt-c694113d5.test
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/test/trigger7.test
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/test/upsert1.test
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/test/view.test
[add] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/test/walprotocol2.test
[modify] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/test/where.test
[add] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/test/whereL.test
[add] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/test/window1.test
[add] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/test/window2.tcl
[add] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/test/window2.test
[add] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/test/window3.tcl
[add] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqlite/src/test/window3.test
[add] https://crrev.com/c368e30ae55600a1c3c9cb1710a54f9c55de786e/third_party/sqli

### cr...@appspot.gserviceaccount.com (2018-11-28)

The following revision refers to this bug: 
https://chromium.googlesource.com/chromium/src.git/+/c368e30ae55600a1c3c9cb1710a54f9c55de786e

Commit: c368e30ae55600a1c3c9cb1710a54f9c55de786e
Author: pwnall@chromium.org
Commiter: pwnall@chromium.org
Date: 2018-11-28 01:16:41 +0000 UTC

sqlite: Upgrade to the 3.25.3 code in M72.

This CL pulls //third_party/sqlite from M72. The original sources in
//third_party/sqlite/sqlite-src-* were not changed, to avoid making the
diff even bigger than it already is.

This CL also pulls changes to //sql and //third_party/blink from the
following commits that landed in M72:

c6d3a866083891cf6cd935091ea877fa507d14a2
9a6c08e6e8436b8e1bae14a736a5db684287f939

The changes above are needed by the SQLite upgrade.

Tested: full debug build (compilation errors in tests were in unrelated
files), ran browser_tests, content_unittests, sql_unittests and the
LayoutTests in storage/websql/

TBR=cmumford

Bug: 900910
Change-Id: I562b92883101d9cdfba89a28295d1b176ad48138
Reviewed-on: https://chromium-review.googlesource.com/c/1352694
Reviewed-by: Victor Costan <pwnall@chromium.org>
Cr-Commit-Position: refs/branch-heads/3578@{#835}
Cr-Branched-From: 4226ddf99103e493d7afb23a4c7902ee496108b6-refs/heads/master@{#599034}

### sh...@chromium.org (2018-11-28)

[Empty comment from Monorail migration]

### wz...@chromium.org (2018-11-28)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-11-28)

[Empty comment from Monorail migration]

### aw...@google.com (2018-12-03)

[Empty comment from Monorail migration]

### le...@gmail.com (2018-12-06)

Hi, will there be multiple CVEs assigned for this thread, and by the way, the bounty will cover  multiple issues that affects Chrome, right? 

### mp...@chromium.org (2018-12-07)

[Comment Deleted]

### aw...@google.com (2018-12-07)

Hi leonwxqian@! Thanks for your questions. The bug came in front of the VRP panel but we pended it until next week as we needed more time than we had in that meeting to ensure we understood the different bugs properly. mpdenton@ very kindly did the analysis in #59, so we'll take a look at the panel next week. Our intent is to reward as if they'd been submitted as separate bugs.

On the CVE front, dan@sqlite.org - have you allocated CVEs for these?  If not, would you like to, or should we?

### le...@gmail.com (2018-12-11)

Hi, I have some update for FTS3  "match":
-------------------------
The PoC is in original report (the docx file), but it only works on sql_shell, and may not be exploitable in Chrome.
-------------------------
We have found the poc we've provided is not correct, we updated it again, and it can work in Chrome.

### le...@gmail.com (2018-12-11)

Original file is : crash-03(won't working in chrome).html
Only this poc file is wrong, the vuln is correct though.

### mp...@chromium.org (2018-12-11)

Thanks leonwxqian@! I deleted my comment above and here is the updated summary:
Summary of bugs:
1. FTS3 "merge" action trusts data stored in special internal tables, but sqlite3 allows the modification of these internal tables from normal SQL statements, allowing untrusted user input into the tables. There are a couple sub-bugs:
(a) Chrome should not allow a user to modify internal FTS3 tables. SQLite has added the SQLITE_DBCONFIG_DEFENSIVE option, which we will be enabling. This config disables modification of internal tables, including internal FTS3 table and the internal SQLite master table.
(b) When using an FTS3 table, the user can trick SQLite into running FTS4 code by adding tables that are internal to FTS4 but not FTS3. I do not know the plan for dealing with this, or if the SQLITE_DBCONFIG_DEFENSIVE flag will prevent this.
(c) Sqlite does not check the size of the memcpy is less or equal to the the size of the allocation, which it should for defense-in-depth.

The PoC is in https://crbug.com/chromium/900910#c11 (https://bugs.chromium.org/p/chromium/issues/attachmentText?aid=365794). A more detailed writeup of the Chrome/cast-specific exploit is in https://crbug.com/chromium/900910#c33. Most of the exploit is attached in https://crbug.com/chromium/900910#c40.


2. FTS3 "match" action is vulnerable to integer overflow. Also requires access to internal FTS3 tables, these will be mitigated by SQLITE_DBCONFIG_DEFENSIVE.

sqlite_shell PoC is in original report (the docx file). Chrome-specific PoC is in https://crbug.com/chromium/900910#c61.


3. Integer overflow in the FTS3 module. Exploitable in Chrome in a similar fashion to #1. Also mitigated by SQLITE_DBCONFIG_DEFENSIVE.


4. Can crash SQLite with garbage primary constraint. Only a DoS bug. Chrome does not consider these security bugs.


Not a bug/WAI:
1. Per https://crbug.com/chromium/900910#c16, SQLite never uses ASSERT for security checks. Any assertion failures should be reported as bugs, no matter the SQL input.
2. Per https://crbug.com/chromium/900910#c7, Cast is WAI because it is supposed to load an HTML page at the behest of a local network request.

### je...@chromium.org (2018-12-12)

I'm looking into backporting this fix to all currently supported versions of Electron, (2.x, 3.x and 4.x, which are based on Chromium 61, 66 and 69 respectively). Upgrading SQLite to 3.25.3 in all those versions of Chromium is going to be quite a challenge, and we were thinking that it might be easier for us to instead backport the SQLite changes that mitigate this issue to the versions of SQLite depended on by those Chromium versions (3.20.patched, 3.22.0, and 3.24.0 respectively).

We found the following commits in SQLite related to the SQLITE_DBCONFIG_DEFENSIVE flag and it would be great to get some confirmation that these are indeed all the needed commits for an effective mitigation, or if not, what we missed:

https://sqlite.org/src/info/4b370c74ae0f2515
https://sqlite.org/src/info/11d98414eac467af
https://sqlite.org/src/info/1309c84ad36b6ac6
https://sqlite.org/src/info/940f2adc8541a838

Thanks in advance!

### dr...@gmail.com (2018-12-12)

Why would upgrading the SQLite in older versions of Chromium be a challenge? Is it more than simply replacing the older "sqlite3.c" and "sqlite3.h" files with the newer ones?  Does chromium do something special that requires extra work with each SQLite release?

The latest release of SQLite (3.26.0) should be a drop-in replacement for whatever older version of SQLite you are using.  And 3.26.0 has the advantage that is has been extensively tested.  If you try to patch an older version, your patched version probably will not have been tested as carefully.  It seems safer to go with an officially supported and tested release, does it not?

Correct me if I am wrong, but I believe the vulnerabilities described here require that the attacker be able to submit arbitrary SQL using the WebSQL interface.  Does that ever happen in an Electron app?

If you want to do a patch, the key check-in for the "multiple vulnerabilities" described here is https://www.sqlite.org/src/info/d44318f59044162e.  That check-in fixes the error.  The SQLITE_DBCONFIG_DEFENSIVE is some extra security we put in place to prevent similar kinds of attacks in the future.  It is defense-in-depth, and is not strictly necessary to fix the problems reported here. Also, SQLITE_DBCONFIG_DEFENSIVE is off by default (for backwards compatibility) and hence requires changes in Chromium to enable it.  So I am not sure how much value there is in including the SQLITE_DBCONFIG_DEFENSIVE patch.

### mp...@chromium.org (2018-12-12)

Indeed, we have a build process that takes the base sqlite source, then applies our patches, and then creates the amalgamation from the patched source. We would like to get rid of our patches, for sure, partially for this reason.

For Electron, though, you can probably just grab the patched version from the Chrome source tree and use that as a drop in replacement--it would likely be much easier than backporting individual patches. If for some reason you don't want to do that, I would actually recommend backporting SQLITE_DBCONFIG_DEFENSIVE more than I would recommend backporting the individual patches, as editing the internal FTS3 tables is a very juicy attack surface and will protect you from having to backport more patches for any further vulnerabilities in this area. As Dr. Hipp mentioned, you will have to enable it, but that shouldn't be too hard.

### je...@chromium.org (2018-12-13)

Thanks! We've decided to do as you suggest and just take the patched version from Chromium. I see that SQLITE_DBCONFIG_DEFENSIVE isn't yet enabled in Chromium--is there a particular reason it hasn't yet been enabled?

Thanks again for all your help!

### mp...@google.com (2018-12-13)

I believe we will enable it soon, after we're sure the upgrade to 3.26 has spent enough time in production, so that we can make large changes one at a time. All the particular bugs from this issue have been fixed in 3.26, but when we enable SQLITE_DBCONFIG_DEFENSIVE, you should probably backport that patch.

### aw...@google.com (2018-12-14)

[Empty comment from Monorail migration]

### ch...@apple.com (2018-12-15)

Hi! Could someone confirm that chrome on iOS and macOS doesn't have a dependency on the system (mac / ios) sqlite? AFAICT you bundle your own - but just double checking.

### mp...@chromium.org (2018-12-15)

We bundle our own, yes.

### in...@chromium.org (2018-12-15)

[Empty comment from Monorail migration]

### pw...@chromium.org (2018-12-15)

Was this disclosed early? https://www.zdnet.com/google-amp/article/sqlite-bug-impacts-thousands-of-apps-including-all-chromium-based-browsers/

The bug description promised 90 days from the day we confirmed, which I think is Nov 1. I think this means the vulnerability shouldn't have been disclosed until Feb 1st.

### in...@chromium.org (2018-12-15)

looks like they did in https://blade.tencent.com/magellan/index_en.html

### in...@chromium.org (2018-12-15)

90-day is usually considered a disclosure deadline, so if we hadn't fixed it in 90 days, they could do the full disclosure. Since it is fixed in Chromium, looks like they did an early disclosure. I would let down talk to the other affected parties, looks like Apple and Mozilla are cced here now.

### pw...@chromium.org (2018-12-15)

I don't think 71 is fully rolled out, so some of users are still exposed to this.

### pw...@chromium.org (2018-12-15)

[Empty comment from Monorail migration]

### le...@gmail.com (2018-12-15)

[Comment Deleted]

### le...@gmail.com (2018-12-15)

Hi, thank you for your concern. I'd like to clearify, now we only have this page(https://blade.tencent.com/magellan/index_en.html) and its corresponding Chinese version (https://blade.tencent.com/magellan/index.html). 

The content of page is based on the publicly available information, they are edited from Dec 2018 release announcement (https://chromereleases.googleblog.com/2018/12/stable-channel-update-for-desktop.html?m=1) -- "High -- Multiple issues in SQLite via WebSQL", and the title of this issue "cast is a vector".

We published the version number of Chromium and SQLite and we think everyone can get those information from the official website. We release this page with newest software version, to urge Chinese manufacturers to quickly upgrade their products.

We also noticed that someone rewrote the PoC (https://worthdoingbadly.com/sqlitebug/) by backtracking SQLite commits at https://www.sqlite.org/src/info/940f2adc8541a838, and extracted the information from the test case. We want to declare that we have nothing to do with this person. We were unaware of this before and we did not give any information to this person.

If you have any questions, please no hesitate contact me again. Thank you.

### pw...@chromium.org (2018-12-15)

leonwxqian@: Thank you very much for explanation!

### pw...@chromium.org (2018-12-15)

jeremya@: I suggest disabling WebSQL for Electron. Electron apps can use SQLite via a node.js package, which can bring in a newer library.

Electron builds seem to be around forever (compared to browsers), for example the December release of VS Code still uses Electron 2.0 / Chrome 61, released in September 2017. Decoupling the app-visible SQLite version from Electron seems like a reasonable way to combat the lack of upgrading, at least for this class of bugs.

### aw...@google.com (2018-12-15)

[Empty comment from Monorail migration]

### aw...@google.com (2018-12-17)

[Empty comment from Monorail migration]

### aw...@google.com (2018-12-18)

leonwxqian@ - thanks the details in https://crbug.com/chromium/900910#c79. As other users of sqlite are still working on patching, do you have a date you're correctly targeting for disclosure that they can work towards?

drhsqlite@gmail.com or dan@sqlite.org - see question in #60 about CVE assignment. Thanks!

### om...@google.com (2018-12-18)

[Empty comment from Monorail migration]

### le...@gmail.com (2018-12-19)

awhalley@ 
Hi, we will go full disclosure after 90 days from this issue is assigned, which is 1st Feb 2019.

We will not release any details about this issue before 1st Feb 2019, but we might want to update our website with new information which is available to public, such as new CVE number assigned. Does this sound OK to you?


### aw...@google.com (2018-12-19)

leonwxqian@ - sounds great, thanks!

### na...@google.com (2018-12-19)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### na...@google.com (2018-12-20)

Thanks for your report. The panel has decided to reward $10,000 + $1,337 bonus :) 

Since you are a new reporter a member of our finance will be in touch. 




### le...@gmail.com (2018-12-20)

Thank you very much! :)

And thank you again for the quick fix.


-- 

BTW, should the label be  reward-11337 instead of  reward-10337 ?

### na...@google.com (2018-12-20)

Apologies - I had a typo. The panel decided to reward $10,337. 

### na...@google.com (2018-12-20)

[Empty comment from Monorail migration]

### le...@gmail.com (2018-12-22)

Still great, thank you :)

### le...@gmail.com (2018-12-27)

[Comment Deleted]

### le...@gmail.com (2018-12-27)

Seems like CVE-2018-20346 has been assigned for this.

http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2018-20346

### bu...@chromium.org (2019-01-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/a06c5187775536a68f035f16cdb8bc47b9bfad24

commit a06c5187775536a68f035f16cdb8bc47b9bfad24
Author: Victor Costan <pwnall@chromium.org>
Date: Tue Jan 15 05:53:46 2019

websql: Enable SQLite's defensive mode for WebSQL databases.

The SQLITE_DBCONFIG_DEFENSIVE flag [1] was added in SQLite 3.26 for
applications that run untrusted SQL queries.

[1] https://www.sqlite.org/c3ref/c_dbconfig_defensive.html

Bug: 900910, 910906
Change-Id: Ia749be52b4e03c18df3b25bcb963c7a916fc671a
Reviewed-on: https://chromium-review.googlesource.com/c/1407544
Commit-Queue: Victor Costan <pwnall@chromium.org>
Reviewed-by: Joshua Bell <jsbell@chromium.org>
Cr-Commit-Position: refs/heads/master@{#622754}
[modify] https://crrev.com/a06c5187775536a68f035f16cdb8bc47b9bfad24/third_party/blink/renderer/modules/webdatabase/sqlite/sqlite_database.cc
[modify] https://crrev.com/a06c5187775536a68f035f16cdb8bc47b9bfad24/third_party/blink/web_tests/storage/websql/fts-crash-703507.html
[add] https://crrev.com/a06c5187775536a68f035f16cdb8bc47b9bfad24/third_party/blink/web_tests/storage/websql/fts-internal-table-access.html


### le...@gmail.com (2019-01-23)

Hi drhsql@ pwnall@ I'd like to inform you that we will release an online page which can check if the user's browser is vulnerable to this issue after 1st Feb 2019 12:00(UTC+8).

The webpage will contain 2 simple PoC which will crash the render process, if they choose to check their web browser and have not upgraded to the newest version of Chrome.


If you have any concern please contact me. Thank you! 

### pw...@chromium.org (2019-01-23)

leonwxqian@ - Thank you very much for checking with us! awhalley@ can speak about timing on behalf of Chrome. I think you have our approval, per https://crbug.com/chromium/900910#c87

### le...@gmail.com (2019-01-24)

Got it, thank you. :)

### aw...@google.com (2019-02-01)

Yep, all set - thanks! Out of interest, what's the URL of the tool?

### sh...@chromium.org (2019-03-06)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pw...@chromium.org (2019-04-26)

[Empty comment from Monorail migration]

### pw...@chromium.org (2019-05-03)

[Empty comment from Monorail migration]

### ad...@google.com (2019-06-06)

[Empty comment from Monorail migration]

### le...@gmail.com (2019-08-05)

Hi lcwu@, pwnall@,
I have sent an email to your @chromium.org mail address at 31th July. (Email title: Question about the contact info of Goolge PR team)
Could you please check the email and get in touch with us as soon as possible?
Thank you very much!

### aw...@google.com (2019-08-05)

Hi leonwxqian@, you can also ready me at awhalley@google.com if I can also help?

### le...@gmail.com (2019-08-05)

Of course, thank you for reply! I will forward that email to you.

### ad...@chromium.org (2019-11-23)

[Empty comment from Monorail migration]

### is...@google.com (2019-11-23)

This issue was migrated from crbug.com/chromium/900910?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>Storage>WebSQL, Internals>Cast, Internals>Storage]
[Monorail blocked-on: crbug.com/chromium/897576]
[Monorail mergedwith: crbug.com/chromium/956392, crbug.com/chromium/959148]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092919)*
