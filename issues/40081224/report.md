# Adobe Flash Player Out-of-Bound Access Vulnerability

| Field | Value |
|-------|-------|
| **Issue ID** | [40081224](https://issues.chromium.org/issues/40081224) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>Flash |
| **CVE IDs** | CVE-2013-0634, CVE-2014-0559, CVE-2015-0330 |
| **Reporter** | we...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2015-01-20 |
| **Bounty** | $2,000.00 |

## Description


I. Summary
Adobe Flash Player is prone to a vulnerability which leads to Out-of-Bound memory access memory via carefully crafted regular expression. An attacker can exploit this issue to defeat ASLR protection or even execute arbitrary code in the context of affected application (Internet Explorer, EXCEL...).
------------------------------------------------------------------
II. Description
Adobe Flash is a multimedia and software platform used for authoring of vector graphics, animation, games and rich Internet applications (RIAs) that can be viewed, played and executed in Adobe Flash Player. 

When constructing a RegExpObject, most part of memory was applied from the heap. While heap overflow may also happen as it is with CVE-2013-0634, CVE-2014-0559, the matching result is stored on the stack. A fixed size int ovector[99] is defined to store the matching index numbers of the target string. A simple line of ActionScript could lead to a crash caused by reading inaccessable memory:

"Venus".match("(((((((((((((((((((((((((((((((((((((((((((((((((?P<G2>)))))))))))))))))))))))))))))))))))))))))))))))))"); 

For the given regular expression above, ovector[99] will be filled with zeros. Then Flash Player managed to construct an Array containing the matching result recognized by AS3. Since there is a named group G2, the Array will also contain a string index entry (G2) that is filled with substring of the target string. The start address of the substring is calculated as follow: start address of target string + ovector[nameIndex*2]. The length of the substring is calulated as:  ovector[nameIndex*2+1] - ovector[nameIndex*2].

The problem is that nameIndex equals to the number of left brackets inside the given regular expression. As the number of left brackets is fully controlled, ovector[nameIndex*2+1] is able to read values out of the stack memory ovector. Flash took mitigations where it checks if the nameIndex is larger than 49, ignoring the fact that nameIndex can be 49 itself. When nameIndex equals to 49, nameIndex*2+1 equals to 99, ovector[nameIndex*2+1] will point to stack memory out of bound. Normally, ovector[nameIndex*2+1] points to the saved EIP under windows and it is a very large value for length field.

This may result in returning a string with a fake length field with enormous value to the AS3 interface. Advanced Heap Fengshui techniques may even allow an attacker build workable exploit via such string to access arbitrary memory.

Chrome 39.0.2171.99 m with latest version of Adobe Flash Player (16.0.0.257) has been tested under Windows 7.
poc and its source code are attached.
------------------------------------------------------------------
III. Impact
Out-of-Bound Access
------------------------------------------------------------------
IV. Affected
Adobe Flash Player under Windows 7.
Other versions may also be affected.
------------------------------------------------------------------
V. Solution
Fortunately, this vulnerability can actually be patched under binary level. First, locate following code snippets in Adobe Flash Player:

0FBE08           MOVSX ECX,BYTE PTR DS:[EAX]
0FBE50 01        MOVSX EDX,BYTE PTR DS:[EAX+1]
C1E1 08          SHL ECX,8
03CA             ADD ECX,EDX
83F9 31          CMP ECX,31
0F8F B5000000    JG flashpla.0113EA9A

Then, modify the last instruction from JG to JGE.
------------------------------------------------------------------
VI. Credit
Wen Guanxing from Venustech ADLAB is credited for this vulnerability.

## Attachments

- [poc.zip](attachments/poc.zip) (application/zip, 5.4 KB)
- [single.zip](attachments/single.zip) (application/zip, 602.0 KB)

## Timeline

### mb...@chromium.org (2015-01-20)

[Empty comment from Monorail migration]

### ri...@chromium.org (2015-01-20)

Thanks for the detailed report! Leaving the rest of the triage/Adobe stuff to cevans@ and markbrand@.

### cl...@chromium.org (2015-01-21)

[Empty comment from Monorail migration]

### wf...@chromium.org (2015-01-21)

[Empty comment from Monorail migration]

### sc...@gmail.com (2015-01-21)

cc: Peleus directly for a real-time opinion.

### sc...@gmail.com (2015-01-21)

This looks very similar indeed to https://code.google.com/p/chromium/issues/detail?id=442585, but with one minor difference: this bug notes an off-by-one error and the other bug notes an integer signedness error.

### sc...@gmail.com (2015-01-21)

@wengx522: thanks for this great bug!

The PoC doesn't actually crash on my 64-bit Linux build -- probably stack layout differences on 64-bit ?

When your PoC runs successfully, does it just crash or does it actually demonstrate an infoleak? If you can create a PoC that actually demonstrates an infoleak, this would typically bump up the reward levels.

### we...@gmail.com (2015-01-21)

@scarybeast:

The poc is actually tested only under IE with latest version of Adobe Flash (16.0.0.257). 
I simply thought this would crash Chrome either. 

It turns out that Flash.ocx and pepflashplayer.dll has minor differences on this issue. 
The stack size and layout are not exactly the same. 

And this really confuse me at the moment, why and who modify such code snippets? 
They don't relate to the sandbox protection added by Chrome. 
It probably caused by the compiler optimization.

I 'm working on a fully workable exploit but perhaps only for IE.
Hopefully, I could also build up an exploit for Chrome.
It will be submitted once finished.


### sc...@gmail.com (2015-01-21)

Adobe tracking as PSIRT-3247

### sc...@gmail.com (2015-01-21)

@wengx522: yes, different compilers will generate very different code and stack layouts from the same C code.

Feel free to try Chrome on the different OS'es and see if there's one that crashes for you as a more useful starting point :-)
(e.g. Win32, Win64, Mac, Chrome OS ARM, Chrome OS x64, Linux x64) -- lots of options.

### we...@gmail.com (2015-01-22)

@scarybeast:

====Testing Environment====
Single.swf is a workable poc for info leak.
It is currently target the lastest version of flashplayer under Win7 32bit. (http://labsdownload.adobe.com/pub/labs/flashruntimes/flashplayer/flashplayer16_sa_win_32.exe)
If everything goes well, it should print out the dynamic base address of flashplayer.

====Basic ideas====
As demonstrated before, it is likely that RegExpObject match returns a malformed String object to the AS3 interface.
The start address of this malformed String equals to that of the original String to be matched. 
The length field of malformed String equals to the saved EIP because of off-by-one. 

Normally, the memory crash at this point is triggered during the construction of an atom of string object. 
The construction contains instructions (probably calculate the length or transcode the charset, whatever) that will access every byte of the string object.
Anyway, the key point to avoid the crash is that following memory blocks after the string object should be continuous and larger than the fake length field.
Then, with the length field of malformed String object, saved EIP can be retrieved and the based address is calculable.

====Exploitation====
To do so, the poc start by spray many 0x10000-byte blocks via vector.<int>, then free some of them to leak memory holes.
It continues to construct the original String object via a prebuild ByteArray. 
The original String object takes 0x10000-byte exactly and will fall in one of the memory holes.
RegExpObject match returns successfully and it is able to calculate the base address of flashplayer by minus the save EIP with a fixed offset.

====Limitations====
Heap Fengshui layout:
/----FULL----\
|----hole----|
|----FULL----| --> 16M - 90M
|----hole----|
|----FULL----/

|----hole----| obtained by the original string

/----FULL----\
|----FULL----|
|............| --> 100M - 512M
|----FULL----|
\----FULL----/

These holes stands in front part of those 0x10000-byte blocks.
So when one of them is obtained by the oringal string, it should be enough continuous memory blocks left.
Normally, the basic address of stand alone flashplayer.exe is less than 0x10000000 (Win7 or XP), so is the saved EIP.
The value of 90M + saved EIP would fall in 100M-512M, so there will be no memory crash.

But for flashplayer plugin (ocx/dll), the start address will likely larger than 0x10000000 (0x5xxxxxxx most time for me).
The reason why this exploit is not working for plugin is that flash cannot spray that much memory blocks.
Still, if any OS with flashplayer plugin in lower memory address, this exploit idea should work. 

### we...@gmail.com (2015-01-22)

[Comment Deleted]

### sc...@gmail.com (2015-02-04)

[Empty comment from Monorail migration]

### we...@gmail.com (2015-02-07)

@scarybeast

Is CVE-2015-0330 reward related?

### sc...@gmail.com (2015-02-07)

Hi @wengx522 -- yes, we'll consider this for reward soon!

If you look at the labels, you'll see "reward-topanel" which is a label that reminds us to decide the reward.

I'm also marking this bug as fixed, since it is fixed here:
https://helpx.adobe.com/security/products/flash-player/apsb15-04.html
http://googlechromereleases.blogspot.com/2015/02/stable-channel-update.html


### cl...@chromium.org (2015-02-07)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### ti...@google.com (2015-02-17)

Merge not required - see #15.

@wengx522 - we should get back to you this week with a reward amount :)

### we...@gmail.com (2015-03-05)

Where does the reward goes, through paypal? 
Does this reward independent from IBB (hackerone)?

### ti...@google.com (2015-03-05)

This reward is independent from IBB, so you'll very likely get another reward from us.

Sorry it's taken so long here - we've had a lot of bugs to push through the reward panel. I'll put this on the top of the list for this week's panel.

### cl...@chromium.org (2015-05-16)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2015-08-17)

wengx522: We're going to pay an additional $2,000 for this report. We'll be in contact this week to collect payment details. If you don't hear from anyone within a week, please contact me at timwillis@.

### ti...@google.com (2015-08-28)

[Empty comment from Monorail migration]

### ti...@google.com (2015-09-23)

Processing via our e-payment system takes ~7 days, but the reward should be on its way to you. Thanks again for your help!

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/450198?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081224)*
