# speech-dispatcher crashes with window.speechSynthesis() 

| Field | Value |
|-------|-------|
| **Issue ID** | [40078530](https://issues.chromium.org/issues/40078530) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Speech |
| **Platforms** | Linux |
| **Reporter** | at...@gmail.com |
| **Assignee** | dm...@chromium.org |
| **Created** | 2013-12-10 |
| **Bounty** | $1,000.00 |

## Description



Tested on:

OS: Ubuntu 12.04 Desktop

Chrome/Chromium: 
   Google Chrome	33.0.1729.3 (Official Build 238910) dev
   Chromium	 ASAN   33.0.1732.0 (Developer Build 239266) 


Repro-file as attachment.

When the repro-file is opened at Chrome, you should hear some stuttering speech.(Note that the window.speechSynthesis is not available on stable-channel Chrome) After few seconds you should see following types of messages in dmesg.

dmesg-output:

[11425.891667] speech-dispatch[30256] general protection ip:7f7379527e20 sp:7f7378e5a930 error:0 in libc-2.15.so[7f73794a9000+1b5000]
[11428.155845] speech-dispatch[30637] general protection ip:7f84d63e56c5 sp:7f84d5d18de0 error:0 in libc-2.15.so[7f84d6366000+1b5000]
[11430.212666] speech-dispatch[30981]: segfault at 940018 ip 00007fb0f3fe2714 sp 00007fb0f3915de0 error 4 in libc-2.15.so[7fb0f3f63000+1b5000]
[11431.452238] speech-dispatch[31190]: segfault at 18 ip 00007f34aa86ee20 sp 00007f34aa1a1930 error 4 in libc-2.15.so[7f34aa7f0000+1b5000]


You might also get apport-dialog about speech-dispatcher crashing with some glibc malloc asserts (double free or corruption).

While the repro-file is running the browser might freeze and/or completely crash. If the browser goes silent you have to "killall speech-dispatcher" few times to get the speech synthesizer back working.

I have checked this issue on Ubuntu 12.04 Desktop version and it is reproducible on two different computers.



## Attachments

- [speech-repro-file.html](attachments/speech-repro-file.html) (text/html, 15.3 KB)
- [speech-repro-file.html](attachments/speech-repro-file_53335748.html) (text/html, 549 B)

## Timeline

### at...@gmail.com (2013-12-10)

There seems to be a lot of different bugs from speech-dispatcher already reported on https://bugs.launchpad.net/ubuntu/+source/speech-dispatcher 

In example https://bugs.launchpad.net/ubuntu/+source/speech-dispatcher/+bug/725765 looks similar to the glibc asserts happening with the repro-file, but there is no activity since 2011-03-22.

### cl...@chromium.org (2013-12-10)

ClusterFuzz is analyzing your testcase. See https://cluster-fuzz.appspot.com/testcase?key=5428057103925248

### cl...@chromium.org (2013-12-13)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-12-13)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-12-13)

tommyw@: Can you please take a look or find someone else to own it.

- Your friendly ClusterFuzz

### cl...@chromium.org (2013-12-13)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-12-13)

Looks like speech synthesis is coming out from behind a flag in M33: https://code.google.com/p/chromium/issues/detail?id=239503

Looks like @dmazzoni is owner; assigning appropriately.

So this is a _really_ interesting case. @attekett: if I read your report correctly, it looks like Chromium is integrating with the system binary "speech-dispatch". And "speech-dispatch" is just generally buggy / suffers bad security?

This means it's technically not a Chromium bug => Security_Severity-None. But it's us exposing a new risk to our users! => ReleaseBlock-Stable. And we're grateful that your report might enable us to better protect users! => reward-topanel

### sc...@gmail.com (2013-12-13)

@jorgelo, @wad: do you happen to know if we've added any system-level components for speech synthesis on Chrome OS? If so, we'd likely flip this over to a Chrome OS security bug and put severity back up to high or critical, depending on sandboxing status?

### sc...@gmail.com (2013-12-13)

@attekett: actually, looks like there may be _even more_ going on here. Can you try and get us a crash ID from chrome://crashes for the browser crash? We can split this out into multiple bugs if necessary but let's collect data here first.

### jo...@chromium.org (2013-12-13)

I don't think we do but Will can confirm.

### sc...@gmail.com (2013-12-13)

[Empty comment from Monorail migration]

### at...@gmail.com (2013-12-13)

@scarybeasts: From my point of view it looks like at least the "speech-dispatch" is buggy, but it is still in default desktop install of Ubuntu.

Also there is some weird UAF and null-pointer segfaults that can be triggered with speech API + some user interactions. So far I haven't been able to make any automated javascript that could trigger those.

I'll try to get the crash ID, I'll let you know how it ends up.

### at...@gmail.com (2013-12-13)

@scarybeasts: Here is one crash ID I got. Crash ID d8d4d71ed7055b80. I can't verify what sort of crash it was, but it dropped the whole browser instead of a sad tab. 

Running the repro-file eventually bricked the whole speechSynthesis from my laptop. I don't get any sound from the speechsynth, even after reboot. :D 

If you want to try to reproduce the UAF that needs user interaction the instructions are:

1. Open two empty tabs in ASAN Chromium.
2. Copy-paste a link to the repro-file into both tabs but do not open the pages yet.
3. Load first tab.
4. Switch to the second tab while speechsynth is working and load the tab.
5. Close the first tab without switching focus into it.(Click the "x")
6. Refresh the second tab.

This UAF is easier to reproduce if you remove the location.reload() setTimeout from the repro-file.

This should drop the whole browser with the following ASAN-report:

==15244==ERROR: AddressSanitizer: heap-use-after-free on address 0x60700045b188 at pc 0x7fc61953c553 bp 0x7fff3a65d2b0 sp 0x7fff3a65d2a8
READ of size 8 at 0x60700045b188 thread T0 (chrome)
    #0 0x7fc61953c552 in Utterance::OnTtsEvent(TtsEventType, int, std::basic_string<char, std::char_traits<char>, std::allocator<char> > const&) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../chrome/browser/speech/tts_controller.cc:98:0
    #1 0x7fc61953cfc0 in TtsController::Stop() /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../chrome/browser/speech/tts_controller.cc:227:0
    #2 0x7fc618e20676 in TtsMessageFilter::OnCancel() /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../chrome/browser/speech/tts_message_filter.cc:108:0
    #3 0x7fc618e1f95b in bool IPC::Message::Dispatch<TtsMessageFilter, TtsMessageFilter>(IPC::Message const*, TtsMessageFilter*, TtsMessageFilter*, void (TtsMessageFilter::*)()) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../ipc/ipc_message.h:147:0
    #4 0x7fc618e1f754 in TtsMessageFilter::OnMessageReceived(IPC::Message const&, bool*) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../chrome/browser/speech/tts_message_filter.cc:45:0
    #5 0x7fc61f6ca007 in content::BrowserMessageFilter::Internal::DispatchMessage(IPC::Message const&) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../content/public/browser/browser_message_filter.cc:82:0
.
.
.


The issue is pretty hard to reproduce, I haven't been able to automate it, and it is normally linked with "speech-dispatch"-process segfault so I thought I would wait until this issue is resolved before reporting it. 

### sc...@gmail.com (2013-12-13)

https://crash.corp.google.com/samples?stbtiq=d8d4d71ed7055b80

Thread 0 CRASHED [SIGABRT @ 0x000003e8000033fd] MAGIC SIGNATURE THREAD
0x00007f8707d65425	[libc-2.15.so -raise.c:64 ]	raise
0x00007f8707d68b8a	[libc-2.15.so -abort.c:91 ]	abort
0x00007f87086b869c	[libstdc++.so.6.0.16 -basic_string.h:1642 ]	std::basic_string<char, std::char_traits<char>, std::allocator<char> >::replace
0x00007f870918fccc	[libpthread-2.15.so + 0x0000eccc ]	
0x00007f87086b6845	[libstdc++.so.6.0.16 -basic_string.h:623 ]	std::basic_string<char, std::char_traits<char>, std::allocator<char> >::end
0x00007f87086b6872	[libstdc++.so.6.0.16 -basic_string.h:631 ]	std::basic_string<char, std::char_traits<char>, std::allocator<char> >::end
0x00007f87086b728e	[libstdc++.so.6.0.16 -basic_string.tcc:318 ]	std::basic_string<char, std::char_traits<char>, std::allocator<char> >::append
0x00007f870eb211aa	[chrome -tts_controller.cc:98 ]	Utterance::OnTtsEvent(TtsEventType, int, std::string const&)
0x00007f870eb21cac	[chrome -tts_controller.cc:228 ]	TtsController::Stop()
0x00007f870e953aa4	[chrome -ipc_message.h:147 ]	TtsMessageFilter::OnMessageReceived(IPC::Message const&, bool*)
0x00007f87110f132b	[chrome -browser_message_filter.cc:82 ]	content::BrowserMessageFilter::Internal::DispatchMessage(IPC::Message const&)

That could easily be a UAF.

At this stage, it's clear there's another bug here aside from the buggy "speech-dispatch" binary on Linux. Could you file a separate issue and I'll keep an eye out for it to triage it? I actually think we may want to fix the browser UAF _first_. If we make the speech-dispatch binary buggy safe, it may stop crashing and in turn that may hide the browser UAF (if a subprocess crash is needed to get the UAF ;-)

### dm...@chromium.org (2013-12-13)

I'll take the tts_controller.cc crash. Thanks for the repro and stack trace!

As for the speech-dispatcher crash:

First, to address https://crbug.com/chromium/327295#c8, this code does not run on Chrome OS. Chrome OS has its own solution for speech synthesis, and it's all sandboxed by NaCl. So this only affects desktop Linux.

Second, we have alternative options for speech on Linux now - we now include Google Network Speech by default (though only on official Google Chrome builds, not Chromium). Users can also install additional speech synthesis options from the web store.

Would it suffice to just make it a command-line flag to enable libspeechd support? Users who really want local speech can assume the risk, and everyone else won't have to worry about potential vulnerabilities on the drive-by web.


### sc...@gmail.com (2013-12-13)

@dmazzoni: yes, that sounds like a decent suggestion to get us out of this spot.
Would it be too much to ask to have you add the new command line flag to the "dangerous command line flags" list? This flag will, after all, expose _critical_ memory corruptions to the drive-by web, so treating it the same way as --no-sandbox, in terms of security impact, seems fair.

### at...@gmail.com (2013-12-13)

So do you guys want me to report a second bug report or do you handle it yourself?

### jo...@chromium.org (2013-12-13)

[Empty comment from Monorail migration]

### dm...@chromium.org (2013-12-13)

OK, I filed crbug.com/328543 for the tts_controller crash, and we'll leave this bug for adding the command-line flag.

"dangerous command line flags" sounds fine.


### sc...@gmail.com (2013-12-13)

Thanks. And an idea from @wad which seems interesting to me: why not ship the Chrome OS extension for desktop Linux?

If for no other reasons, you've gained the advantage of less configurations to test and debug, which is always a boon. But also because it looks like it would solve the security concern: the code in the extension is NaCl'ed.

### at...@gmail.com (2013-12-13)

So did I understand https://crbug.com/chromium/327295#c15 correctly, Chrome should have alternative thingy for speechSynth than "speech-dispatch"? If so, how can I enable it? My fuzzer might find better repro for the uaf if it wouldn't need to handle all the "speech-dispatch" hangs/crashes/unresponsiveness.

At least with official Chrome unstable, the same "speech-dispatch" persists.

### dm...@chromium.org (2013-12-18)

So far unfortunately I can't reproduce the ASAN crash. I can get speech-dispatcher to become unresponsive, but Chrome stays running.

Can you tell me what speech-dispatcher package(s) you have installed? For example, speech-dispatcher-flite, etc. - it seems possible that the bug depends on what speech engine is being used.

If you'd like to try to fuzz without speech-dispatcher being involved, just install one of these extensions:

https://chrome.google.com/webstore/detail/us-english-female-text-to/pkidpnnapnfgjhfhkpmjpbckkbaodldb
https://chrome.google.com/webstore/detail/multilingual-tts-engine/megclklaoidjbomplbhbdgbelkoebbdl
https://chrome.google.com/webstore/detail/tts-engine-using-google-t/heapeepeplnopkplmnehobamjenidpga

In the fuzzed code, make sure that the utterance voice is anything other than "native".

In addition, try an official build of Google Chrome, which includes an extension like one of these by default, that uses Google's speech API.

Finally, some blind users prefer voices they can access via speech-dispatcher over the Chrome OS voices, so I don't want to remove speech-dispatcher support entirely, at least yet. Putting it behind a scary flag is still fine.


### at...@gmail.com (2013-12-18)


I shouldn't have any additional packages installed than the ones that come with official Ubuntu 12.04 Desktop. According to apt-get I don't have anything else than speech-dispatcher installed with search speech-*.

Once you get it to crash first time it is pretty easy to reproduce. Like said in the instruction it needs little bit trickery. :)



### dm...@chromium.org (2013-12-18)

Guessing that this is the same root cause as 329651


### at...@gmail.com (2014-01-09)

Any luck in reproducing the UAF? I still haven't had any luck on making automatic repro. Not sure if it even is possible.

I played around with the repro-file. 

The attached repro-file is the smallest one I found that can reproduce the speech-dispatch general protection fault.

There seems to be some magic in the utterance text sets.

test8.text="盜砯瘎㇊࢐տ"
test9.text="ݛѫ般牶ᠱ䴾紽赍ᘊၸ譏煣摤珱♮いó㨗梇纽⦩稓眬皺啄路搿橂ᓶ熪腻䤪㌍䒱薍ᣌ劵甔⧌䍗᪆ㆴ溅聛摜"

If you change the value of those into in example same amount of letter "a" the crashing stops.


### dm...@chromium.org (2014-01-09)

I'm pretty sure the UAF in Chrome was fixed in http://crbug.com/329651




### at...@gmail.com (2014-01-09)

I don't have access to that issue. 

Is that patch in the newest lkgr? I could update into newest version and try to reproduce.

### at...@gmail.com (2014-01-09)

I tried with, Chromium 34.0.1777.0 (Developer Build 243865). Can't reproduce the UAF anymore. :) Now the repro-file only causes chrome to hang.

### dm...@chromium.org (2014-01-09)

The fix landed in trunk on r241887 on 2013-12-19 and was merged to M33 just a few days ago.


### js...@chromium.org (2014-02-02)

Issue cleanup.

### cl...@chromium.org (2014-02-03)

[Empty comment from Monorail migration]

### at...@gmail.com (2014-02-03)

The UAF was a dupe but the speech-dispatch issue is still not fixed. Repro-file from https://crbug.com/chromium/327295#c25 still crashes the speech-dispatch with Chromium 34.0.1814.0 (Developer Build 247920).

dmesg-snippet after running chrome --no-sandbox speech-repro-file.html

[73612.880165] speech-dispatch[7618] general protection ip:7f6755529e20 sp:7f6754e5c930 error:0 in libc-2.15.so[7f67554ab000+1b5000]
[73616.765628] speech-dispatch[7718] general protection ip:7f34ea90ee20 sp:7f34ea241930 error:0 in libc-2.15.so[7f34ea890000+1b5000]
[73617.429394] speech-dispatch[7732] general protection ip:7fb50bbe6e20 sp:7fb50b519930 error:0 in libc-2.15.so[7fb50bb68000+1b5000]
[73618.495725] speech-dispatch[7760] general protection ip:7f68930376c5 sp:7f689296ade0 error:0 in libc-2.15.so[7f6892fb8000+1b5000]




### in...@chromium.org (2014-02-07)

reopening based on c#32.

### la...@google.com (2014-02-14)

Hey Dominic, could you take another look at this issue?

### dx...@chromium.org (2014-02-20)

[Empty comment from Monorail migration]

### mb...@chromium.org (2014-03-11)

Any updates on this? Fixing severity and impact based on c#32.

### cl...@chromium.org (2014-03-11)

You have far exceeded the 60-day deadline for fixing this high severity security vulnerability.

We commit ourselves to this deadline and appreciate your utmost priority on this issue.

If you are unable to look into this soon, please find someone else to own this.

- Your friendly ClusterFuzz

### dx...@google.com (2014-03-15)

Punting this to m35.

### js...@chromium.org (2014-03-15)

We definitely want to get this in for m34, and it looks like there's still a window for the first release, so resetting flags.

### dx...@chromium.org (2014-03-17)

[Empty comment from Monorail migration]

### rs...@chromium.org (2014-03-19)

[Empty comment from Monorail migration]

### dx...@google.com (2014-03-21)

andre, maybe let's merge in your change.  

### dm...@chromium.org (2014-03-21)

Did you post this on the wrong bug?

### dm...@chromium.org (2014-03-22)

[Empty comment from Monorail migration]

### dm...@chromium.org (2014-03-22)

The UAF was fixed in the other bug. This adds a switch so that speech-dispatcher won't be loaded by default. https://codereview.chromium.org/209393004/


### dm...@chromium.org (2014-03-22)

[Empty comment from Monorail migration]

### dm...@chromium.org (2014-03-24)

[Empty comment from Monorail migration]

### dm...@chromium.org (2014-03-25)

This was committed as r259109, requesting merge.



### dx...@chromium.org (2014-03-25)

[Empty comment from Monorail migration]

### dm...@chromium.org (2014-03-25)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-03-28)

dmazzoni@ - can you please merge to M34?

### dm...@chromium.org (2014-03-31)

This was merged to the M34 branch as r259248. I don't understand why this bug wasn't auto-updated, the committed change had this bug number in its change description.


### in...@chromium.org (2014-03-31)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-04-01)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-04-04)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-04-05)

[Comment Deleted]

### ti...@chromium.org (2014-04-05)

[Comment Deleted]

### ti...@chromium.org (2014-04-05)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-04-14)

Thanks for the report - $1000 for this one. I'll start the payment process today.

### ti...@chromium.org (2014-04-15)

[Empty comment from Monorail migration]

### at...@gmail.com (2014-04-15)

I think there has been a small misunderstanding, because there is actually two bugs going on in this report.

The UAF presented in https://crbug.com/chromium/327295#c13 and the crash of Ubuntu system binary "speech-dispatch" presented in comments #1 and #32.  

I think that the $1k reward doesn't cover that nasty looking crash on system binary that is far outside the sandbox. :)

When I tried it last(time of https://crbug.com/chromium/327295#c32). I verified the speech-dispatch crash on three laptops running Ubuntu 12.04 Desktop, so I don't think there is any special configurations and/or packets involved. 

The repro-file from https://crbug.com/chromium/327295#c25 reproduces the speech-dispatch crash, when I use it together with the flag introduced by patch from https://crbug.com/chromium/327295#c45, so the UAF and the speech-dispatch crash are not related.


Tested:

Chromium: 36.0.1937.0 (Developer Build 263419) aura

Command Line:	/home/attekett/Downloads/chrome/chrome --no-sandbox --incognito --enable-speech-dispatcher --flag-switches-begin --flag-switches-end ./Downloads/speech-repro-file.html

Result:

[29028.762326] traps: speech-dispatch[23268] general protection ip:7f0400fe86c5 sp:7f040091ede0 error:0 in libc-2.15.so[7f0400f69000+1b5000]
[29029.851264] traps: speech-dispatch[23298] general protection ip:7f6eee9136c5 sp:7f6eee249de0 error:0 in libc-2.15.so[7f6eee894000+1b5000]
[29030.929711] traps: speech-dispatch[23341] general protection ip:7f37423756c5 sp:7f3741cabde0 error:0 in libc-2.15.so[7f37422f6000+1b5000]


### ti...@chromium.org (2014-04-23)

+ inferno@ for https://crbug.com/chromium/327295#c61

### in...@chromium.org (2014-04-23)

Yes, lets redo on the reward nominations for this one Tim

### ti...@chromium.org (2014-04-23)

Sounds good to me - I'll readd it to the next reward panel.

### jo...@chromium.org (2014-04-25)

I don't think rewarding for bugs in speech-dispatcher (an Ubuntu system binary) is in-scope for the Chromium VRP. The UaF has already been rewarded.

### at...@gmail.com (2014-04-25)

FWIW, From my point of view, the situation is similar to graphics-driver bug etc. Chromium integrates with a system binary that has vulnerability in it. The integration was mitigated with a new switch in patch from c#45. So the reward actually wouldn't be for the speech-dispatcher bug. As far as I know the speech-dispatcher bug still exists, but can not be triggered via Chromium without the flag. 

### sc...@gmail.com (2014-04-25)

@jorgelo: I don't think your comment in https://crbug.com/chromium/327295#c65 is correct.

At the abstract level, we reward for any bug or information which leads to us taking a concrete action that increases the security of our users. In this instance, the concrete action is noted as a CL at https://code.google.com/p/chromium/issues/detail?id=327295#c45.

Thanks to @attekett's report, we took a web-accessible critical vulnerability off the default attack surface.

The closest precedent I can think of is https://code.google.com/p/chromium/issues/detail?id=146254, where we rewarded $5000 for a report in the Windows kernel. I don't think Windows kernel was in scope at the time, but the report enabled us to land a change to OTS in Chrome to take the vulnerability of the web-accessible attack surface.

### ti...@chromium.org (2014-04-30)

Update: We've sent payment for the $1000 reward already, but I'll leave the "in-process" label on this bug until we formally reconsider the reward amount for the issue mentioned in c#61.

### at...@gmail.com (2014-08-27)

This issue has been without any change for some time now. Any progress?

### dm...@chromium.org (2014-08-27)

I thought this was fixed? The UAF is fixed, and the speech-dispatcher crashes are no longer an issue because they require a command-line flag to enable.


### at...@gmail.com (2014-08-27)

Sorry for the confusion, the bug is fixed. I was talking about the https://crbug.com/chromium/327295#c68.

### in...@chromium.org (2014-08-27)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-02-02)

[Empty comment from Monorail migration]

### dm...@chromium.org (2016-03-10)

+landell@opera.com


### dm...@chromium.org (2016-03-10)

@inferno, okay to remove restrictions on this now?


### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### aw...@google.com (2018-10-04)

[Empty comment from Monorail migration]

### aw...@google.com (2018-10-04)

[Empty comment from Monorail migration]

### aw...@google.com (2018-10-15)

Hi attekett@, the VRP panel look a look at the second part of the report and I'm afraid they declined to reward. Not because of how long ago it was, but since the "fix" was to keep the functionality behind a flag. The panel thought you might want to look at the Patch Reward Program (https://www.google.com/about/appsecurity/patch-rewards/) if there's a fix you can make upstream.

### aw...@google.com (2018-10-15)

[Empty comment from Monorail migration]

### is...@google.com (2018-10-15)

This issue was migrated from crbug.com/chromium/327295?no_tracker_redirect=1

[Monorail blocked-on: crbug.com/chromium/329651]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40078530)*
