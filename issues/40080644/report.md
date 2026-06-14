# Security: Race condition in Flash workers may cause an exploitable double free

| Field | Value |
|-------|-------|
| **Issue ID** | [40080644](https://issues.chromium.org/issues/40080644) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>Flash |
| **CVE IDs** | CVE-2014-0574 |
| **Reporter** | bi...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2014-10-15 |
| **Bounty** | $7,500.00 |

## Description

**VULNERABILITY DETAILS**  

The issue occurs while sharing a bytearray between two workers. If both call bytearray.clear() at the same time, Flash does not correctly handle the race and may double free the array.

**VERSION**  

Chrome Version: [38.0.2125.104] + [stable]  

Operating System: [Win 7 SP1 x64 FR]

**REPRODUCTION CASE**  

Use a VM with 2 cores to get a reliable crash, I can't manage to crash a 1-cored VM.  

Put exploit/clear\_xpl.swf along with exploit/calc\_chrome.bin on a web server and run the browser with the --no-sandbox flag to get the calc.  

Put poc/poc.swf and browse to in order to crash Chrome, IE or anything.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: crash with calc as a side effect  

Crash State: not good

## Attachments

- [flash-clear-rc.rar](attachments/flash-clear-rc.rar) (application/octet-stream, 23.9 KB)
- [bug423703.zip](attachments/bug423703.zip) (application/zip, 25.3 KB)
- [DoubleFreeArray.as](attachments/DoubleFreeArray.as) (application/octet-stream, 2.4 KB)
- [DoubleFreeArray.zip](attachments/DoubleFreeArray.zip) (application/zip, 10.5 KB)

## Timeline

### in...@chromium.org (2014-10-15)

[Empty comment from Monorail migration]

### sc...@gmail.com (2014-10-15)

Yes, I'll deal with this one, thanks @inferno :-)


### sc...@gmail.com (2014-10-15)

Re-attaching as .zip.

@biloulehibou: .rar is a pain to work with (and a dirty hacker tool :P )
I've re-uploaded as .zip; .zip preferred in future reports.

### sc...@gmail.com (2014-10-15)

Also pasting notes.txt as a convenience:

---
Race condition in workers may cause an exploitable double free
Tested: Chrome Stable 38.0.2125.104 (pepflashplayer.dll 15.0.0.189 32BIT) on Windows 7 SP1 x64

The issue occurs while sharing a bytearray between two workers. If both call bytearray.clear() at the same time, Flash does not correctly handle the race and may double free the array.
The idea of the exploit is to free first the bytearray, allocate a vector instead and use the double free to free the vector. Its length should then be overwritten by a pointer which is enough to execute arbitrary code.



From pepflashplayer.dll, base at 0x10000000, poc.swf most of the time causes a crash at 0x1056EF3B attempting to write at a null location.

.text:1056EF32 loc_1056EF32:
.text:1056EF32                 mov     eax, [ecx+0Ch]
.text:1056EF35                 mov     edx, [ecx+10h]
.text:1056EF38                 push    [ebp+arg_4]
.text:1056EF3B                 mov     [eax+10h], edx       ; crash here
.text:1056EF3E                 mov     eax, [ecx+10h]
.text:1056EF41                 mov     edx, [ecx+0Ch]
.text:1056EF44                 mov     [eax+0Ch], edx
.text:1056EF47                 and     dword ptr [ecx+0Ch], 0
.text:1056EF4B                 and     dword ptr [ecx+10h], 0


Put exploit/clear_xpl.swf along with exploit/calc_chrome.bin on a web server and run the browser with the --no-sandbox flag to get the calc.
Use a VM with 2 cores to get a reliable crash, I can't manage to crash a 1-cored VM.
Put poc/poc.swf and browse to in order to crash Chrome.


Compile both .fla with Flash CS 5.5. poc.txt and clear_xpl.txt show the content of poc.fla and clear_xpl.fla.


### sc...@gmail.com (2014-10-15)

Confirm calc.exe in a VM! Chrome Stable 38.0.2125.104 32-bit.

I had to rename calc_chrome.BIN to calc_chrome.bin because my webserver is case sensitive.

### sc...@gmail.com (2014-10-15)

@biloulehibou: great report!

Can you help me with a couple of things?
1) poc/poc.txt is empty. Did you mean to have something in that file?

2) Standalone .as files.
Would you be able to provide standalone .as files instead of .fla files? Not everyone has access to the software needed to compile .fla files.
Ideally, the exploit and the PoC would be in .as files (plus support files like .bin, explicitly loaded by the .as file as necessary).
And the .as files should be compilable by the freely downloadable Flex compiler:
http://www.adobe.com/devnet/flex/flex-sdk-download.html
e.g. mxmlc -target-player 14.0 -swf-version 25 DoubleFreeArray.as
(The flags are needed because you've used APIs newer than the default compile version of 11.1 or so. You'll also need to install a new playerglobal.swc file to get this compiler flag to work, I grabbed it from here: http://helpx.adobe.com/flash-player/kb/archived-flash-player-versions.html#playerglobal)

### sc...@gmail.com (2014-10-15)

@biloulehibou: I've attached my attempt to get the PoC down to a single .as file. It compiles (using flex and the command line above) but it doesn't work. Any chance you can help me fix it? :P
(I don't really know what I'm doing with these worker APIs and I had to comment out the call to .stop() to get it to compile so I've probably done something stupid.)

### bi...@gmail.com (2014-10-16)

I'm reposting a "zip", with a "bin", no "fla" and an updated "poc.txt". DoubleFreeMain.swf is the exploit.

@scarybeasts The issue came from loaderInfo, not sure why flex doesnt like it.

Tell me if you need anything else.

### sc...@gmail.com (2014-10-16)

Adobe is tracking as PSIRT-3089.

### sc...@gmail.com (2014-11-08)

Should be fixed in next week's patch tuesday, with CVE-2014-0574.

### sc...@gmail.com (2014-11-12)

http://helpx.adobe.com/security/products/flash-player/apsb14-24.html

### cl...@chromium.org (2014-11-13)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### mb...@chromium.org (2014-11-17)

Thanks for the report! This qualified for a $7500 reward.

### ti...@google.com (2014-12-08)

Payment in progress

### ti...@google.com (2014-12-09)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-12-15)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-12-15)

[Empty comment from Monorail migration]

### ti...@google.com (2015-02-12)

Payment on its way to you (the first time takes the longest due to the supplier registration). You should see it in your account in about 4 weeks from today. If you don't, please contact me directly to chase.

### cl...@chromium.org (2015-02-19)

Bulk update: removing view restriction from closed bugs.

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

### sh...@chromium.org (2018-07-29)

[Empty comment from Monorail migration]

### is...@google.com (2018-07-29)

This issue was migrated from crbug.com/chromium/423703?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080644)*
