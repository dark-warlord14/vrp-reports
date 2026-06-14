# Heap-use-after-free in content::PluginURLFetcher::OnReceivedData

| Field | Value |
|-------|-------|
| **Issue ID** | [40078208](https://issues.chromium.org/issues/40078208) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Plugins |
| **Reporter** | at...@gmail.com |
| **Assignee** | bb...@chromium.org |
| **Created** | 2013-10-07 |
| **Bounty** | $500.00 |

## Description


Tested on:

OS: Ubuntu 12.04

Chromium: ASAN 32.0.1664.0 (Developer Build 227246)

I'm not quite sure if this is kind of false-positive, or a bug on flash, or actual Chromium bug, because you have to have flash (package: flashplugin-installer) installed to reproduce this issue. I haven't been able to reproduce the issue with other plugins so far. 

Repro-file:

<iframe src="data:text/html;charset=utf-8,%3Cembed%20src%3D%22data%3Aapplication/x-shockwave-flash%2CFWS%2505dt%2500%2589%2506%pluginspage%3D%22http%3A//www.macromedia.com/go/getflashplayer%22%20type%3D%22application/x-shockwave-flash%22%2022%3E%3C/object%3E%0A"></iframe>

ASAN-report:

==4958==ERROR: AddressSanitizer: heap-use-after-free on address 0x61300000a608 at pc 0x7f17835b2d1a bp 0x7fff001c40d0 sp 0x7fff001c40c8
READ of size 8 at 0x61300000a608 thread T0 (chrome)
    #0 0x7f17835b2d19 in content::PluginURLFetcher::OnReceivedData(char const*, int, int) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../content/child/npapi/plugin_url_fetcher.cc:289:0
    #1 0x7f17835d5e3c in content::ResourceDispatcher::OnReceivedData(int, int, int, int) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../content/child/resource_dispatcher.cc:433:0
    #2 0x7f17835d817a in bool ResourceMsg_DataReceived::Dispatch<content::ResourceDispatcher, content::ResourceDispatcher, void (content::ResourceDispatcher::*)(int, int, int, int)>(IPC::Message const*, content::ResourceDispatcher*, content::ResourceDispatcher*, void (content::ResourceDispatcher::*)(int, int, int, int)) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../content/common/resource_messages.h:252:0
    #3 0x7f17835d4813 in content::ResourceDispatcher::DispatchMessage(IPC::Message const&) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../content/child/resource_dispatcher.cc:647:0
    #4 0x7f17835d3ab8 in content::ResourceDispatcher::OnMessageReceived(IPC::Message const&) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../content/child/resource_dispatcher.cc:313:0
    #5 0x7f1783562e3d in content::ChildThread::OnMessageReceived(IPC::Message const&) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../content/child/child_thread.cc:354:0
.
.
.
freed by thread T0 (chrome) here:
    #0 0x7f177c825104 in operator delete(void*) _asan_rtl_:0
    #1 0x7f17835b0c8a in content::PluginStreamUrl::~PluginStreamUrl() /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../content/child/npapi/plugin_stream_url.cc:168:0
    #2 0x7f17835b0b6d in content::PluginStreamUrl::~PluginStreamUrl() /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../content/child/npapi/plugin_stream_url.cc:164:0
    #3 0x7f17835b039c in content::PluginStreamUrl::DidReceiveData(char const*, int, int) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../content/child/npapi/plugin_stream_url.cc:130:0
    #4 0x7f17835b2cae in content::PluginURLFetcher::OnReceivedData(char const*, int, int) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../content/child/npapi/plugin_url_fetcher.cc:288:0
    #5 0x7f17835d5e3c in content::ResourceDispatcher::OnReceivedData(int, int, int, int) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../content/child/resource_dispatcher.cc:433:0
.
.
.




## Timeline

### cl...@chromium.org (2013-10-07)

ClusterFuzz is now working on this testcase. See https://cluster-fuzz.appspot.com/testcase?key=5264986129563648

### ke...@chromium.org (2013-10-07)

attekett:

We are having trouble reproducing this, although we're not clear what you are getting from the flashplugin-installer package.

Can you do a flash version check and see what you get?
http://helpx.adobe.com/flash-player/kb/find-version-flash-player.html

### at...@gmail.com (2013-10-07)


My Flash version is 11.2.202.310. ASAN-builds don't have the built-in flash-player. The flashplugin-installer installs that version. Previously flashplugin-installer was in Chromium build dependencies, not sure if it is anymore. 

Without that package, with the repro-file, Chromium will just notify that you need to install flash.

### in...@chromium.org (2013-10-07)

[Empty comment from Monorail migration]

### ae...@chromium.org (2013-10-08)

The UaF reproduces for me after working around another bug:

==16275==ERROR: AddressSanitizer: attempting free on address which was not malloc()-ed: 0x555566766030 in thread T0 (chrome)
    #0 0x555556c78634 (/usr/local/google/home/aedla/chromium/src/out/Release/chrome+0x1724634)
    #1 0x7ffff78dd6a8 (/usr/lib/x86_64-linux-gnu/libX11.so.6+0x406a8)

Like attekett, I'm running flash 11.2.202.310 from flashplugin-installer, chrome 32.0.1664.0 and ubuntu 12.04.

### ae...@chromium.org (2013-10-08)

[Empty comment from Monorail migration]

### ae...@chromium.org (2013-10-08)

Both PluginURLFetcher and PluginStreamUrl are deleted by this call path:

PluginURLFetcher::OnReceivedData
  PluginStreamUrl::DidReceiveData
    PluginStream::Write
      PluginStream::WriteToPlugin
        PluginStream::TryWriteToPlugin
          PluginStreamUrl::Close
            PluginInstance::RemoveStream

So that's not good since both PluginStreamUrl and PluginURLFetcher are still executing. There is a protection in PluginStreamUrl::DidReceiveData:

  // Protect the stream against it being destroyed or the whole plugin instance
  // being destroyed within the write handlers
  scoped_refptr<PluginStream> protect(this);

But there's no such protection in PluginURLFetcher::OnReceivedData, which tries to access its field:

    data_offset_ += data_length;


### ae...@chromium.org (2013-10-08)

I think a UaF in an unsandboxed process triggered by a webpage would normally be high or critical severity. This one shouldn't be exploitable though, since use happens right after free. I'll mark it as medium severity.

### bb...@chromium.org (2013-10-08)

Thanks for the analysis. I've uploaded a CL to fix this particular crash, by doing all member accesses before calling PluginStreamURL / PluginStream methods.
https://codereview.chromium.org/26526002/

### bb...@chromium.org (2013-10-08)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-10-08)

Fixing impact labels.

### in...@chromium.org (2013-10-08)

We need to be careful about milestones. Looks like this should affect m30.

### cl...@chromium.org (2013-10-08)

Fixing impact labels.

### ja...@chromium.org (2013-10-08)

This code path didn't get turned on until r226031, to wait until M32. 

### in...@chromium.org (2013-10-08)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-10-08)

This medium+ severity security issue is a regression on trunk.

Please fix this asap. If you are unable to look into this soon, please revert your change.

Adding ReleaseBlock-Stable label.

- Your friendly ClusterFuzz

### bu...@chromium.org (2013-10-09)

------------------------------------------------------------------------
r227661 | bbudge@chromium.org | 2013-10-09T03:56:51.164568Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/content/child/npapi/plugin_url_fetcher.cc?r1=227661&r2=227660&pathrev=227661

Modify PluginURLFetcher to avoid accessing members after calling PluginStream methods.
Calling PluginStream methods may cause the instance to be deleted, causing a UAF.
Modify the code to update members before calling PluginStream methods.

BUG=304787

Review URL: https://codereview.chromium.org/26526002
------------------------------------------------------------------------

### in...@chromium.org (2013-10-09)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-10-09)

[Empty comment from Monorail migration]

### mb...@chromium.org (2013-12-10)

Thanks for the report! This one qualifies for a $500 reward. Since the use happens right after the free, we think that this would be difficult to exploit.

### pa...@chromium.org (2013-12-18)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-02-06)

Bulk update: removing view restriction from closed bugs.

### ti...@chromium.org (2014-02-28)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-22)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/304787?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40078208)*
