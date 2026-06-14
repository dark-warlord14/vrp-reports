# Heap use after free with malware blocking page

| Field | Value |
|-------|-------|
| **Issue ID** | [40052042](https://issues.chromium.org/issues/40052042) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | UI, UI>Browser>Navigation |
| **Reporter** | ch...@gmail.com |
| **Assignee** | cr...@chromium.org |
| **Created** | 2011-12-12 |
| **Bounty** | $3,133.00 |

## Description

**VULNERABILITY DETAILS**  

Attached reproduction case causes a heap use after free.

**VERSION**  

Chrome Version: [18.0.969.0 (Developer Build 113965 Linux)] + [dev]  

Operating System: [Ubuntu 10.04 64 bit]

**REPRODUCTION CASE**  

1.Open attached test1.html in chrome.  

2. It tries to load <http://www.ianfette.org> in an iframe.  

3. Chrome will display malware blocking page.  

4. Click on reload button of chrome.  

5. Chrome browser will crash.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: [browser]  

Crash State:  

This is what asan has to say

==7837== ERROR: AddressSanitizer heap-use-after-free on address 0x7f586e8c8248 at pc 0x7f589a23adbc bp 0x7fff8d1786b0 sp 0x7fff8d178688  

READ of size 4 at 0x7f586e8c8248 thread T0  

#0 0x7f589a23adbc in \_ZNKSs6\_M\_repEv /usr/lib/gcc/x86\_64-linux-gnu/4.4/../../../../include/c++/4.4/bits/basic\_string.h:272  

#1 0x7f589a23e801 in \_ZNK11TabContents8delegateEv /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/./content/browser/tab\_contents/tab\_contents.h:93  

#2 0x7f589a17d0be in \_ZN14RenderViewHost13OnMsgNavigateERKN3IPC7MessageE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/content/browser/renderer\_host/render\_view\_host.cc:910  

#3 0x7f589a179baa in \_ZN14RenderViewHost17OnMessageReceivedERKN3IPC7MessageE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/content/browser/renderer\_host/render\_view\_host.cc:678  

#4 0x7f589a161abf in \_ZN21RenderProcessHostImpl17OnMessageReceivedERKN3IPC7MessageE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/content/browser/renderer\_host/render\_process\_host\_impl.cc:941  

#5 0x7f589a16210d in \_ZThn8\_N21RenderProcessHostImpl17OnMessageReceivedERKN3IPC7MessageE ???:0  

#6 0x7f58973ca649 in \_ZN3IPC12ChannelProxy7Context17OnDispatchMessageERKNS\_7MessageE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/ipc/ipc\_channel\_proxy.cc:263  

#7 0x7f5895c5a98f in \_ZNK4base8CallbackIFvvEE3RunEv /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/./base/callback.h:274  

#8 0x7f5895c5b226 in \_ZN11MessageLoop21DeferOrRunPendingTaskERKN4base11PendingTaskE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/message\_loop.cc:512  

#9 0x7f5895c5c52f in \_ZN11MessageLoop6DoWorkEv /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/message\_loop.cc:702  

#10 0x7f5895cf99a2 in \_ZN4base15MessagePumpGlib17RunWithDispatcherEPNS\_11MessagePump8DelegateEPNS\_21MessagePumpDispatcherE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/message\_pump\_glib.cc:213  

#11 0x7f5895c5954e in \_ZN11MessageLoop11RunInternalEv /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/message\_loop.cc:460  

#12 0x7f5895c5d112 in ~AutoRunState /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/message\_loop.cc:774  

#13 0x7f5895640e10 in \_ZN22ChromeBrowserMainParts18MainMessageLoopRunEPi /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/chrome/browser/chrome\_browser\_main.cc:2000  

#14 0x7f5899fedcc2 in \_ZN7content15BrowserMainLoop23RunMainMessageLoopPartsEPb /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/content/browser/browser\_main\_loop.cc:392  

#15 0x7f5899feb5e6 in \_Z11BrowserMainRKN7content18MainFunctionParamsE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/content/browser/browser\_main.cc:102  

#16 0x7f5895bae94c in \_ZN12\_GLOBAL\_\_N\_123RunNamedProcessTypeMainERKSsRKN7content18MainFunctionParamsEPNS2\_19ContentMainDelegateE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/content/app/content\_main.cc:264  

#17 0x7f5895bae0e2 in \_ZN7content11ContentMainEiPPKcPNS\_19ContentMainDelegateE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/content/app/content\_main.cc:455  

#18 0x7f58943d4917 in ChromeMain /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/chrome/app/chrome\_main.cc:32  

#19 0x7f58943d483b in main /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/chrome/app/chrome\_exe\_main\_gtk.cc:18  

#20 0x7f588d96ec4d in \_\_libc\_start\_main /build/buildd/eglibc-2.11.1/csu/libc-start.c:258  

#21 0x7f58943d4759 in \_start ??:0  

0x7f586e8c8248 is located 456 bytes inside of 608-byte region [0x7f586e8c8080,0x7f586e8c82e0)  

freed by thread T0 here:  

#0 0x7f589b4c4e19 in \_ZdlPv *asan\_rtl*  

#1 0x7f589a216f11 in \_ZN20NavigationController26RemoveEntryAtIndexInternalEi /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/content/browser/tab\_contents/navigation\_controller.cc:1079  

#2 0x7f589a2164b8 in \_ZN20NavigationController18RemoveEntryAtIndexEiRK4GURL /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/content/browser/tab\_contents/navigation\_controller.cc:468  

#3 0x7f58958288ca in \_ZN24SafeBrowsingBlockingPage11DontProceedEv /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/chrome/browser/safe\_browsing/safe\_browsing\_blocking\_page.cc:582  

#4 0x7f589a20d8c9 in \_ZN16InterstitialPage7ObserveEiRKN7content18NotificationSourceERKNS0\_19NotificationDetailsE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/content/browser/tab\_contents/interstitial\_page.cc:282  

#5 0x7f5894651696 in \_ZN22ChromeInterstitialPage7ObserveEiRKN7content18NotificationSourceERKNS0\_19NotificationDetailsE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/chrome/browser/tab\_contents/chrome\_interstitial\_page.cc:52  

#6 0x7f589a10ec3d in \_ZNK4base7WeakPtrI16ObserverListBaseIN7content20NotificationObserverEEE3getEv /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/./base/memory/weak\_ptr.h:171  

#7 0x7f589a21bd34 in \_ZN20NavigationController30NotifyNavigationEntryCommittedEPN7content20LoadCommittedDetailsE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/content/browser/tab\_contents/navigation\_controller.cc:1202  

#8 0x7f589a218459 in \_ZN20NavigationController19RendererDidNavigateERK32ViewHostMsg\_FrameNavigate\_ParamsPN7content20LoadCommittedDetailsE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/content/browser/tab\_contents/navigation\_controller.cc:637  

#9 0x7f589a23e269 in \_ZN11TabContents11DidNavigateEP14RenderViewHostRK32ViewHostMsg\_FrameNavigate\_Params /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/content/browser/tab\_contents/tab\_contents.cc:1543  

#10 0x7f589a17d0be in \_ZN14RenderViewHost13OnMsgNavigateERKN3IPC7MessageE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/content/browser/renderer\_host/render\_view\_host.cc:910  

#11 0x7f589a179baa in \_ZN14RenderViewHost17OnMessageReceivedERKN3IPC7MessageE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/content/browser/renderer\_host/render\_view\_host.cc:678  

#12 0x7f589a161abf in \_ZN21RenderProcessHostImpl17OnMessageReceivedERKN3IPC7MessageE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/content/browser/renderer\_host/render\_process\_host\_impl.cc:941  

#13 0x7f589a16210d in \_ZThn8\_N21RenderProcessHostImpl17OnMessageReceivedERKN3IPC7MessageE ???:0  

#14 0x7f58973ca649 in \_ZN3IPC12ChannelProxy7Context17OnDispatchMessageERKNS\_7MessageE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/ipc/ipc\_channel\_proxy.cc:263  

#15 0x7f5895c5a98f in \_ZNK4base8CallbackIFvvEE3RunEv /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/./base/callback.h:274  

#16 0x7f5895c5b226 in \_ZN11MessageLoop21DeferOrRunPendingTaskERKN4base11PendingTaskE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/message\_loop.cc:512  

#17 0x7f5895c5c52f in \_ZN11MessageLoop6DoWorkEv /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/message\_loop.cc:702  

#18 0x7f5895cf99a2 in \_ZN4base15MessagePumpGlib17RunWithDispatcherEPNS\_11MessagePump8DelegateEPNS\_21MessagePumpDispatcherE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/message\_pump\_glib.cc:213  

#19 0x7f5895c5954e in \_ZN11MessageLoop11RunInternalEv /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/message\_loop.cc:460  

#20 0x7f5895c5d112 in ~AutoRunState /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/message\_loop.cc:774  

#21 0x7f5895640e10 in \_ZN22ChromeBrowserMainParts18MainMessageLoopRunEPi /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/chrome/browser/chrome\_browser\_main.cc:2000  

#22 0x7f5899fedcc2 in \_ZN7content15BrowserMainLoop23RunMainMessageLoopPartsEPb /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/content/browser/browser\_main\_loop.cc:392  

#23 0x7f5899feb5e6 in \_Z11BrowserMainRKN7content18MainFunctionParamsE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/content/browser/browser\_main.cc:102  

#24 0x7f5895bae94c in \_ZN12\_GLOBAL\_\_N\_123RunNamedProcessTypeMainERKSsRKN7content18MainFunctionParamsEPNS2\_19ContentMainDelegateE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/content/app/content\_main.cc:264  

#25 0x7f5895bae0e2 in \_ZN7content11ContentMainEiPPKcPNS\_19ContentMainDelegateE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/content/app/content\_main.cc:455  

#26 0x7f58943d4917 in ChromeMain /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/chrome/app/chrome\_main.cc:32  

#27 0x7f58943d483b in main /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/chrome/app/chrome\_exe\_main\_gtk.cc:18  

#28 0x7f588d96ec4d in \_\_libc\_start\_main /build/buildd/eglibc-2.11.1/csu/libc-start.c:258  

previously allocated by thread T0 here:  

#0 0x7f589b4c4a93 in \_Znwm *asan\_rtl*  

#1 0x7f589a219bc6 in \_ZN20NavigationController28RendererDidNavigateToNewPageERK32ViewHostMsg\_FrameNavigate\_ParamsPb /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/content/browser/tab\_contents/navigation\_controller.cc:790  

#2 0x7f589a217ed2 in \_ZN20NavigationController19RendererDidNavigateERK32ViewHostMsg\_FrameNavigate\_ParamsPN7content20LoadCommittedDetailsE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/content/browser/tab\_contents/navigation\_controller.cc:585  

#3 0x7f589a23e269 in \_ZN11TabContents11DidNavigateEP14RenderViewHostRK32ViewHostMsg\_FrameNavigate\_Params /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/content/browser/tab\_contents/tab\_contents.cc:1543  

#4 0x7f589a17d0be in \_ZN14RenderViewHost13OnMsgNavigateERKN3IPC7MessageE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/content/browser/renderer\_host/render\_view\_host.cc:910  

#5 0x7f589a179baa in \_ZN14RenderViewHost17OnMessageReceivedERKN3IPC7MessageE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/content/browser/renderer\_host/render\_view\_host.cc:678  

#6 0x7f589a161abf in \_ZN21RenderProcessHostImpl17OnMessageReceivedERKN3IPC7MessageE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/content/browser/renderer\_host/render\_process\_host\_impl.cc:941  

#7 0x7f589a16210d in \_ZThn8\_N21RenderProcessHostImpl17OnMessageReceivedERKN3IPC7MessageE ???:0  

#8 0x7f58973ca649 in \_ZN3IPC12ChannelProxy7Context17OnDispatchMessageERKNS\_7MessageE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/ipc/ipc\_channel\_proxy.cc:263  

#9 0x7f5895c5a98f in \_ZNK4base8CallbackIFvvEE3RunEv /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/./base/callback.h:274  

#10 0x7f5895c5b226 in \_ZN11MessageLoop21DeferOrRunPendingTaskERKN4base11PendingTaskE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/message\_loop.cc:512  

#11 0x7f5895c5c52f in \_ZN11MessageLoop6DoWorkEv /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/message\_loop.cc:702  

#12 0x7f5895cf99a2 in \_ZN4base15MessagePumpGlib17RunWithDispatcherEPNS\_11MessagePump8DelegateEPNS\_21MessagePumpDispatcherE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/message\_pump\_glib.cc:213  

#13 0x7f5895c5954e in \_ZN11MessageLoop11RunInternalEv /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/message\_loop.cc:460  

#14 0x7f5895c5d112 in ~AutoRunState /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/message\_loop.cc:774  

#15 0x7f5895640e10 in \_ZN22ChromeBrowserMainParts18MainMessageLoopRunEPi /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/chrome/browser/chrome\_browser\_main.cc:2000  

#16 0x7f5899fedcc2 in \_ZN7content15BrowserMainLoop23RunMainMessageLoopPartsEPb /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/content/browser/browser\_main\_loop.cc:392  

#17 0x7f5899feb5e6 in \_Z11BrowserMainRKN7content18MainFunctionParamsE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/content/browser/browser\_main.cc:102  

#18 0x7f5895bae94c in \_ZN12\_GLOBAL\_\_N\_123RunNamedProcessTypeMainERKSsRKN7content18MainFunctionParamsEPNS2\_19ContentMainDelegateE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/content/app/content\_main.cc:264  

#19 0x7f5895bae0e2 in \_ZN7content11ContentMainEiPPKcPNS\_19ContentMainDelegateE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/content/app/content\_main.cc:455  

#20 0x7f58943d4917 in ChromeMain /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/chrome/app/chrome\_main.cc:32  

#21 0x7f58943d483b in main /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/chrome/app/chrome\_exe\_main\_gtk.cc:18  

#22 0x7f588d96ec4d in \_\_libc\_start\_main /build/buildd/eglibc-2.11.1/csu/libc-start.c:258  

==7837== ABORTING  

Shadow byte and word:  

0x1feb0dd19049: fd  

0x1feb0dd19048: fd fd fd fd fd fd fd fd  

More shadow bytes:  

0x1feb0dd19028: fd fd fd fd fd fd fd fd  

0x1feb0dd19030: fd fd fd fd fd fd fd fd  

0x1feb0dd19038: fd fd fd fd fd fd fd fd  

0x1feb0dd19040: fd fd fd fd fd fd fd fd  

=>0x1feb0dd19048: fd fd fd fd fd fd fd fd  

0x1feb0dd19050: fd fd fd fd fd fd fd fd  

0x1feb0dd19058: fd fd fd fd fd fd fd fd  

0x1feb0dd19060: fa fa fa fa fa fa fa fa  

0x1feb0dd19068: fa fa fa fa fa fa fa fa

## Attachments

- [test1.html](attachments/test1.html) (text/html; charset=us-ascii, 83 B)
- [version_list.py](attachments/version_list.py) (text/x-java; charset=us-ascii, 5.5 KB)
- [abc2.html](attachments/abc2.html) (application/x-empty; charset=binary, 0 B)
- [abc.html](attachments/abc.html) (text/html; charset=us-ascii, 254 B)

## Timeline

### sk...@chromium.org (2011-12-12)

Thanks for the report + asan details!

Unfortunately, I cannot reproduce on Windows. It may there that there simply is not enough heap activity after any erroneous free to see the effects of the memory corruption without asan. On the other hand, it may be OS-specific (but I see no reason why it would be). Have you tried your PoC against earlier versions on Linux?

Memory corruption in the browser process is obviously bad, but your PoC seems to require certain user interaction that I don't expect is very likely to happen luckily. Let's hope this is related to the refresh button, and doesn't apply to automated page reloads or navigations.

### ch...@gmail.com (2011-12-12)

@skylined
I have tried this poc only with ubuntu 10.04. I don't have any previous linux versions installed now.

Yes. This needs user interaction. I cannot reproduce with automated reloads.

### sk...@chromium.org (2011-12-12)

@chamal: Don't worried, I wanted to ask if you tried earlier versions of Chrome on Linux. The Linux version should not matter in this case.

### ch...@gmail.com (2011-12-12)

[Comment Deleted]

### ch...@gmail.com (2011-12-12)

Yes I tried . But did not reproduce on stable version 15.0.874.121 and developer build 17.0.963.2 dev. 

### sk...@chromium.org (2011-12-12)

Thank you, it probably was 17: you can find this at http://omahaproxy.appspot.com/ or you can use the  attached python script that parses this info into a more readable format. It tells me that linux dev has been 17.0.963.2 since 9 Dec 2011.

### in...@chromium.org (2011-12-14)

Chamal, are you still able this to reproduce this on latest dev channel or new m16 stable ?

### ch...@gmail.com (2011-12-14)

[Comment Deleted]

### ch...@gmail.com (2011-12-14)

Original steps mentioned in report does not work now. 

But these steps work on Chrome stable version 16.0.912.63 and 18.0.971.0 (Developer Build 114373 Linux).

1. Host test1.html in local web server.
2. Open chrome.
3. Visit www.google.com. Any site will do.
4. Visit 127.0.0.1/test1.html.
5. Chrome will display malware blocking page.
6. Click on refresh button.
Browser will crash.

Please let me know if these steps does not reproduce.

### ts...@chromium.org (2011-12-15)

Reproduced on 18.0.967.0 (Developer Build 113815) Linux.

#0  memcpy () at ../sysdeps/x86_64/memcpy.S:161
#1  0x00007f4fed8a38d0 in copy (__n=<optimized out>, __s2=<optimized out>, 
    __s1=<optimized out>)
    at /build/buildd/gcc-4.4-4.4.3/build/x86_64-linux-gnu/libstdc++-v3/include/bits/char_traits.h:275
#2  _M_copy (__n=<optimized out>, __s=<optimized out>, __d=<optimized out>)
    at /build/buildd/gcc-4.4-4.4.3/build/x86_64-linux-gnu/libstdc++-v3/include/bits/basic_string.h:339
#3  _S_copy_chars (__k2=<optimized out>, __k1=<optimized out>, 
    __p=<optimized out>)
    at /build/buildd/gcc-4.4-4.4.3/build/x86_64-linux-gnu/libstdc++-v3/include/bits/basic_string.h:384
#4  std::string::_S_construct<char const*> (
    __beg=0x363636366c6c6c6c <Address 0x363636366c6c6c6c out of bounds>, 
    __end=<optimized out>, __a=<optimized out>)
    at /build/buildd/gcc-4.4-4.4.3/build/x86_64-linux-gnu/libstdc++-v3/include/bits/basic_string.tcc:141
#5  0x00007f4fed8a3aeb in _S_construct_aux<char const*> (__a=<optimized out>, 
    __end=<optimized out>, __beg=<optimized out>)
    at /build/buildd/gcc-4.4-4.4.3/build/x86_64-linux-gnu/libstdc++-v3/include/bits/basic_string.h:1546
#6  _S_construct<char const*> (__a=<optimized out>, __end=<optimized out>, 
    __beg=<optimized out>)
    at /build/buildd/gcc-4.4-4.4.3/build/x86_64-linux-gnu/libstdc++-v3/include/bits/basic_string.h:1562
#7  std::basic_string<char, std::char_traits<char>, std::allocator<char> >::basic_string (this=0x7fff10aad3a0, __s=0x7f4f9ff0a018 "", __n=<optimized out>, 
    __a=...)
    at /build/buildd/gcc-4.4-4.4.3/build/x86_64-linux-gnu/libstdc++-v3/include/bits/basic_string.tcc:208
#8  0x00007f4ff6536f35 in net::RegistryControlledDomainService::GetDomainAndRegistry (gurl=...) at net/base/registry_controlled_domain.cc:80
#9  0x00007f4ff6537065 in net::RegistryControlledDomainService::SameDomainOrHost (gurl1=..., gurl2=...) at net/base/registry_controlled_domain.cc:99
#10 0x00007f4ff5b6e3a8 in ConstrainedWindowTabHelper::DidNavigateMainFrame (
    this=0x7f4fe088ce80, details=..., params=...)
    at chrome/browser/ui/constrained_window_tab_helper.cc:91
#11 0x00007f4ff840922c in TabContents::DidNavigateMainFramePostCommit (
    this=0x7f4fe15db900, details=..., params=...)
    at content/browser/tab_contents/tab_contents.cc:1310
#12 0x00007f4ff840a0f0 in TabContents::DidNavigate (this=0x7f4fe15db900, rvh=
    0x7f4fd7186000, params=...)
    at content/browser/tab_contents/tab_contents.cc:1580
#13 0x00007f4ff839061a in RenderViewHost#0  memcpy () at ../sysdeps/x86_64/memcpy.S:161
#1  0x00007f4fed8a38d0 in copy (__n=<optimized out>, __s2=<optimized out>, 
    __s1=<optimized out>)
    at /build/buildd/gcc-4.4-4.4.3/build/x86_64-linux-gnu/libstdc++-v3/include/bits/char_traits.h:275
#2  _M_copy (__n=<optimized out>, __s=<optimized out>, __d=<optimized out>)
    at /build/buildd/gcc-4.4-4.4.3/build/x86_64-linux-gnu/libstdc++-v3/include/bits/basic_string.h:339
#3  _S_copy_chars (__k2=<optimized out>, __k1=<optimized out>, 
    __p=<optimized out>)
    at /build/buildd/gcc-4.4-4.4.3/build/x86_64-linux-gnu/libstdc++-v3/include/bits/basic_string.h:384
#4  std::string::_S_construct<char const*> (
    __beg=0x363636366c6c6c6c <Address 0x363636366c6c6c6c out of bounds>, 
    __end=<optimized out>, __a=<optimized out>)
    at /build/buildd/gcc-4.4-4.4.3/build/x86_64-linux-gnu/libstdc++-v3/include/bits/basic_string.tcc:141
#5  0x00007f4fed8a3aeb in _S_construct_aux<char const*> (__a=<optimized out>, 
    __end=<optimized out>, __beg=<optimized out>)
    at /build/buildd/gcc-4.4-4.4.3/build/x86_64-linux-gnu/libstdc++-v3/include/bits/basic_string.h:1546
#6  _S_construct<char const*> (__a=<optimized out>, __end=<optimized out>, 
    __beg=<optimized out>)
    at /build/buildd/gcc-4.4-4.4.3/build/x86_64-linux-gnu/libstdc++-v3/include/bits/basic_string.h:1562
#7  std::basic_string<char, std::char_traits<char>, std::allocator<char> >::basic_string (this=0x7fff10aad3a0, __s=0x7f4f9ff0a018 "", __n=<optimized out>, 
    __a=...)
    at /build/buildd/gcc-4.4-4.4.3/build/x86_64-linux-gnu/libstdc++-v3/include/bits/basic_string.tcc:208
#8  0x00007f4ff6536f35 in net::RegistryControlledDomainService::GetDomainAndRegistry (gurl=...) at net/base/registry_controlled_domain.cc:80
#9  0x00007f4ff6537065 in net::RegistryControlledDomainService::SameDomainOrHost (gurl1=..., gurl2=...) at net/base/registry_controlled_domain.cc:99
#10 0x00007f4ff5b6e3a8 in ConstrainedWindowTabHelper::DidNavigateMainFrame (
    this=0x7f4fe088ce80, details=..., params=...)
    at chrome/browser/ui/constrained_window_tab_helper.cc:91
#11 0x00007f4ff840922c in TabContents::DidNavigateMainFramePostCommit (
    this=0x7f4fe15db900, details=..., params=...)
    at content/browser/tab_contents/tab_contents.cc:1310
#12 0x00007f4ff840a0f0 in TabContents::DidNavigate (this=0x7f4fe15db900, rvh=
    0x7f4fd7186000, params=...)
    at content/browser/tab_contents/tab_contents.cc:1580
#13 0x00007f4ff839061a in RenderViewHost::OnMsgNavigate (this=0x7f4fd7186000, 
    msg=...) at content/browser/renderer_host/render_view_host.cc:909
#14 0x00007f4ff838e49f in RenderViewHost::OnMessageReceived (
    this=0x7f4fd7186000, msg=...)af
 ::OnMsgNavigate (this=0x7f4fd7186000, 
    msg=...) at content/browser/renderer_host/render_view_host.cc:909
#14 0x00007f4ff838e49f in RenderViewHost::OnMessageReceived (
    this=0x7f4fd7186000, msg=...)
in

87 void ConstrainedWindowTabHelper::DidNavigateMainFrame(
88      const content::LoadCommittedDetails& details,
89          const content::FrameNavigateParams& params) {
90            // Close constrained windows if necessary.
91              if (!net::RegistryControlledDomainService::SameDomainOrHost(
92                        details.previous_url, details.entry->url()))
93                            CloseConstrainedWindows();
94                            }


details.entry->url() appears freed


$5 = (const GURL &) @0x7f4fe124b298: {
  spec_ = 
    <error reading variable: Cannot access memory at address 0x363636363636361e\
>, 
  is_valid_ = 54, 
  parsed_ = {
    scheme = {
      begin = 909522486, 
      len = 909522486
    }, 
    username = {
      begin = 909522486, 
      len = 909522486
    }, 
    password = {
      begin = 909522486, 
      len = 909522486
    }, 
    host = {
      begin = 909522486, 
      len = 909522486
    }, 
    port = {
      begin = 909522486, 
      len = 909522486
    }, 
    path = {
      begin = 909522486, 
      len = 909522486
    }, 
    query = {
      begin = 909522486, 
      len = 909522486
    }, 
    ref = {
      begin = 909522486, 
      len = 909522486
    }
  }
}

details.entry is also freed.






 

### ts...@chromium.org (2011-12-15)

NavigationController::GetActiveEntry() is likely the source of the defunct |entry|, possibly from http://src.chromium.org/viewvc/chrome?view=rev&revision=105355.   Charlie, could you take a look?

### ts...@chromium.org (2011-12-15)

[Empty comment from Monorail migration]

### cr...@chromium.org (2011-12-15)

Yes, I'll take a look.

### cr...@chromium.org (2011-12-15)

I don't think this is related to GetActiveEntry().  The problem is that we are trying to reload the page that caused the interstitial page.  That means the current NavigationEntry is being used, but SafeBrowsingBlockingPage::DontProceed is deleting it.

Clearly, that's not the right thing to do.  I can think of a few options:
1) Make InterstitialPage or SafeBrowsingBlockingPage smart enough not to delete the entry if it is in use again.  (Will that leave some unresolved state around?)
2) If an interstitial is showing, treat the reload as a new navigation rather than a reload.  This means we'll use a different NavigationEntry and the previous SafeBrowsingBlockingPage can clean up its state as before.
3) Don't allow reloads when an interstitial page is showing, or do something else, like go back.

Scott, what do you think is the best way forward?

### sk...@chromium.org (2011-12-15)

Jay's knows more about interstitials than I.

### jc...@chromium.org (2011-12-15)

That's tricky...
I think option 3 is not good, as disabling the reload button would not be sufficient (you could simply enter the same URL) and as navigating back would be to my opinion confusing to users.
For option 1 we would probably need to change InterstitialPage::DontProceed() to include a parameter specifying whether we decided not to proceed as part of a reload so that safe_browsing_blocking_page could know not to delete the entry. But as you say we might have to reset some states.
Option 2 seems trickier to me as the navigation controller would have to know that an interstitial page is showing.
So I would think option 1 is probably the best approach.


### cr...@chromium.org (2011-12-16)

Wow, this code is really tricky.

For top-level malware or SSL pages, there's no problem.  The navigation entry with the problem never commits, and InterstitialPage::DontProceed discards the pending entry.

For subresource malware (like this test page), SafeBrowsingBlockingPage::DontProceed assumes it should delete the interstitial page's entry.  This is the right thing to do if DontProceed is called before a new navigation begins (such as if the user clicks the Back button or the button on the interstitial page itself), and it's also the right thing to do if DontProceed is called after a new navigation to a different page commits.

It's only a problem if DontProceed is called after a navigation to the same entry commits.  Unfortunately, SafeBrowsingBlockingPage::DontProceed doesn't have any way to tell if it was called before a new navigation began or after one was just committed.  In fact, I'm kind of surprised we call the same function from both situations, since that requires it to deal with a lot of corner cases like this.

I tried avoiding calling RemoveEntryAtIndex if the index is the last committed entry, but that breaks the GoBack case (since we haven't started a new navigation yet).  In fact, RemoveEntryAtIndex has some logic to force a load of a different page if it deletes the current entry.  I don't think that's safe, though, because there's still a period of time when we're showing a deleted entry.

As for option 2 from https://crbug.com/chromium/107182#c14, the NavigationController already knows about interstitial pages and calls DontProceed and CancelForNavigation in a lot of places.  DontProceed isn't what we want on a reload, though, since that will kick us back to the previous page.  CancelForNavigation doesn't fix the bug, because we still end up calling DontProceed after commit, which deletes the current entry.

I'm not comfortable with any of the fix attempts I have so far because of the complexity of SafeBrowsingBlocking Page.  I can look again tomorrow, but Jay, let me know if you see a cleaner way to handle this.

### cr...@chromium.org (2011-12-16)

Ah, I think I see more of the problem.

Unless I'm mistaken, I don't think it's safe to have a NavigationController::RemoveEntryAtIndex call that can delete the current entry.  That function takes in a URL to load in case the current entry is being deleted, but this leaves us with a deleted current entry while an asynchronous and potentially slow navigation takes place.

As it turns out, this function is only used for this case in SafeBrowsingBlockingPage::DontProceed, so this is probably the only place we're running into this memory error.  I think we'll need to find a different way around this and then change RemoveEntryAtIndex to fail if called on the current index.

My current plan is to avoid calling RemoveEntryAtIndex for the current entry and make it so we don't rely on this behavior in the GoBack case.  I'll see if it works.

### cr...@chromium.org (2011-12-17)

CL in progress.  I still need to fix a unit test, but I think it's close.

I've marked the CL private for now since I won't get back to until Monday.
http://codereview.chromium.org/8976014/

### ch...@gmail.com (2011-12-19)

[Comment Deleted]

### ch...@gmail.com (2011-12-19)

Attached another reproduction case which does not need user interaction.
This reproduces only on release build with asan.
Does not reproduce on debug build.

Steps
=====
1. Copy abc.html and abc2.html to same folder and host them on localhost web server.
2. Open chrome web browser.
3. Open abc.html on chrome browser through localhost.
4. Wait about 10 seconds. Browser will crash with a use after free.

### js...@chromium.org (2011-12-19)

Resetting priority based on severity.

### cr...@chromium.org (2011-12-19)

CL posted for review.  In a stock build, I'm not able to repro the bug without user interaction based on https://crbug.com/chromium/107182#c21, since the reload of the document never seems to complete for me.  Regardless, the CL should fix the underlying issue.

### bu...@chromium.org (2011-12-20)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=115189

------------------------------------------------------------------------
r115189 | creis@chromium.org | Tue Dec 20 13:47:12 PST 2011

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/src/content/browser/tab_contents/navigation_controller.cc?r1=115189&r2=115188&pathrev=115189
 M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/safe_browsing/safe_browsing_blocking_page_test.cc?r1=115189&r2=115188&pathrev=115189
 M http://src.chromium.org/viewvc/chrome/trunk/src/content/browser/tab_contents/navigation_controller_unittest.cc?r1=115189&r2=115188&pathrev=115189
 M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/safe_browsing/safe_browsing_blocking_page.cc?r1=115189&r2=115188&pathrev=115189
 M http://src.chromium.org/viewvc/chrome/trunk/src/content/browser/tab_contents/navigation_controller.h?r1=115189&r2=115188&pathrev=115189
 M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/safe_browsing/safe_browsing_blocking_page_unittest.cc?r1=115189&r2=115188&pathrev=115189

Don't delete the current NavigationEntry when leaving an interstitial page.

BUG=107182
TEST=See bug

Review URL: http://codereview.chromium.org/8976014
------------------------------------------------------------------------

### cr...@chromium.org (2011-12-21)

Fixed.  We can verify in tomorrow's canary and then merge to 17 if it looks good.

### js...@chromium.org (2011-12-21)

This is listed as OS Linux, but it doesn't look platform specific. Is there any reason it shouldn't be OS All?

### sc...@gmail.com (2011-12-21)

Charlie, does this really affect stable? It's marked Mstone-17 SecImpacts-Stable which is confusing.

### cr...@chromium.org (2011-12-21)

Yes, it's not Linux specific.  The bug has been there for a long time.  I'm guessing we should merge it to M16 as well.

### ch...@gmail.com (2011-12-21)

Tested on 18.0.978.0 (Developer Build 115243 Linux). Does not reproduce any longer.I think fix works fine.

Yes.This fix needs to be merged to m16, because it still reproduces in stable version 16.0.912.63. 

### in...@chromium.org (2011-12-21)

[Empty comment from Monorail migration]

### cr...@chromium.org (2011-12-22)

kerz@ and laforge@, I'll plan to merge this to M17 and M16 today unless there's a reason not to.

### bu...@chromium.org (2011-12-22)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=115624

------------------------------------------------------------------------
r115624 | creis@chromium.org | Thu Dec 22 14:11:08 PST 2011

Changed paths:
 M http://src.chromium.org/viewvc/chrome/branches/963/src/content/browser/tab_contents/navigation_controller.cc?r1=115624&r2=115623&pathrev=115624
 M http://src.chromium.org/viewvc/chrome/branches/963/src/chrome/browser/safe_browsing/safe_browsing_blocking_page_test.cc?r1=115624&r2=115623&pathrev=115624
 M http://src.chromium.org/viewvc/chrome/branches/963/src/content/browser/tab_contents/navigation_controller_unittest.cc?r1=115624&r2=115623&pathrev=115624
 M http://src.chromium.org/viewvc/chrome/branches/963/src/content/browser/tab_contents/navigation_controller.h?r1=115624&r2=115623&pathrev=115624
 M http://src.chromium.org/viewvc/chrome/branches/963/src/chrome/browser/safe_browsing/safe_browsing_blocking_page.cc?r1=115624&r2=115623&pathrev=115624
 M http://src.chromium.org/viewvc/chrome/branches/963/src/chrome/browser/safe_browsing/safe_browsing_blocking_page_unittest.cc?r1=115624&r2=115623&pathrev=115624

Merge 115189 - Don't delete the current NavigationEntry when leaving an interstitial page.

BUG=107182
TEST=See bug

Review URL: http://codereview.chromium.org/8976014

TBR=creis@chromium.org
Review URL: http://codereview.chromium.org/9023016
------------------------------------------------------------------------

### bu...@chromium.org (2011-12-22)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=115633

------------------------------------------------------------------------
r115633 | creis@chromium.org | Thu Dec 22 15:15:20 PST 2011

Changed paths:
 M http://src.chromium.org/viewvc/chrome/branches/912/src/content/browser/tab_contents/navigation_controller_unittest.cc?r1=115633&r2=115632&pathrev=115633
 M http://src.chromium.org/viewvc/chrome/branches/912/src/content/browser/tab_contents/navigation_controller.h?r1=115633&r2=115632&pathrev=115633
 M http://src.chromium.org/viewvc/chrome/branches/912/src/content/browser/tab_contents/navigation_controller.cc?r1=115633&r2=115632&pathrev=115633
 M http://src.chromium.org/viewvc/chrome/branches/912/src/chrome/browser/safe_browsing/safe_browsing_blocking_page_unittest.cc?r1=115633&r2=115632&pathrev=115633
 M http://src.chromium.org/viewvc/chrome/branches/912/src/chrome/browser/safe_browsing/safe_browsing_blocking_page.cc?r1=115633&r2=115632&pathrev=115633
 M http://src.chromium.org/viewvc/chrome/branches/912/src/chrome/browser/safe_browsing/safe_browsing_blocking_page_test.cc?r1=115633&r2=115632&pathrev=115633

Merge 115189 - Don't delete the current NavigationEntry when leaving an interstitial page.

BUG=107182
TEST=See bug

Review URL: http://codereview.chromium.org/8976014

TBR=creis@chromium.org
Review URL: http://codereview.chromium.org/8958022
------------------------------------------------------------------------

### bu...@chromium.org (2011-12-22)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=115639

------------------------------------------------------------------------
r115639 | creis@chromium.org | Thu Dec 22 15:40:21 PST 2011

Changed paths:
 M http://src.chromium.org/viewvc/chrome/branches/912/src/chrome/browser/safe_browsing/safe_browsing_blocking_page.cc?r1=115639&r2=115638&pathrev=115639

Fix merge error.

Follow-up CL for http://codereview.chromium.org/8958022/.

BUG=107182
TBR=creis@chromium.org
Review URL: http://codereview.chromium.org/8962041
------------------------------------------------------------------------

### bu...@chromium.org (2011-12-22)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=115641

------------------------------------------------------------------------
r115641 | creis@chromium.org | Thu Dec 22 15:45:46 PST 2011

Changed paths:
 M http://src.chromium.org/viewvc/chrome/branches/912/src/chrome/browser/safe_browsing/safe_browsing_blocking_page_test.cc?r1=115641&r2=115640&pathrev=115641

Fix another merge error in test.

BUG=107182
Review URL: http://codereview.chromium.org/9027024
------------------------------------------------------------------------

### in...@chromium.org (2012-01-03)

[Empty comment from Monorail migration]

### ch...@gmail.com (2012-01-05)

Is this issue eligible for a reward? 

### in...@chromium.org (2012-01-05)

Yes it is and that is why, this bug already has the reward-topanel label on it.

### js...@chromium.org (2012-01-19)

[Empty comment from Monorail migration]

### js...@chromium.org (2012-01-19)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-01-20)

@chamal.desilva: thanks for this very interesting bug report! And sorry that the fix was accidentally merged and released earlier than we expected.

Given that this bug causes memory corruption in the browser process, the rewards panel has decided to reward the rarely-seen top $3133.7 level! Congrats :D

### ch...@gmail.com (2012-01-20)

Thank you very much for the higher reward. :)

### sc...@gmail.com (2012-01-24)

Derestricting; actually fixed since a few weeks.

### sc...@gmail.com (2012-01-31)

Payment in system. Congrats again Chamal!

### ch...@gmail.com (2012-02-03)

I received the money today. Thanks a lot again :)

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-14)

[Empty comment from Monorail migration]

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

This issue was migrated from crbug.com/chromium/107182?no_tracker_redirect=1

[Multiple monorail components: UI, UI>Browser>Navigation, UI>Browser>SafeBrowsing]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40052042)*
