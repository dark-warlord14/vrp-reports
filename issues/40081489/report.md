# crash with processing invalid x509-user-cert responses.

| Field | Value |
|-------|-------|
| **Issue ID** | [40081489](https://issues.chromium.org/issues/40081489) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals |
| **Reporter** | in...@chromium.org |
| **Assignee** | [Deleted User] |
| **Created** | 2010-06-09 |
| **Bounty** | $500.00 |

## Description

Steps to reproduce

1. nc -l -p 80 < bug
2  browse to http://localhost:80
3. broswer crashes.

## Attachments

- [bug](attachments/bug) (text/plain; charset=us-ascii, 2.5 KB)

## Timeline

### in...@chromium.org (2010-06-09)

reproduces on v5 stable and latest 6 trunk. looking into it.

### in...@chromium.org (2010-06-09)

Here is the stacktrace.

 	1a98645b()	
>	chrome.dll!CrossSiteResourceHandler::ResumeResponse()  Line 157 + 0x34 bytes	C++
 	chrome.dll!ResourceDispatcherHost::OnClosePageACK(const ViewMsg_ClosePage_Params & params={...})  Line 556	C++
 	chrome.dll!DispatchToMethod<ResourceDispatcherHost,void (__thiscall ResourceDispatcherHost::*)(ViewMsg_ClosePage_Params const &),ViewMsg_ClosePage_Params>(ResourceDispatcherHost * obj=0x09b16240, void (const ViewMsg_ClosePage_Params &)* method=0x033ed920, const Tuple1<ViewMsg_ClosePage_Params> & arg={...})  Line 422 + 0xc bytes	C++
 	chrome.dll!IPC::MessageWithTuple<Tuple1<ViewMsg_ClosePage_Params> >::Dispatch<ResourceDispatcherHost,void (__thiscall ResourceDispatcherHost::*)(ViewMsg_ClosePage_Params const &)>(const IPC::Message * msg=class=32, index=122, ResourceDispatcherHost * obj=0x09b16240, void (const ViewMsg_ClosePage_Params &)* func=0x033ed920)  Line 1020 + 0x11 bytes	C++
 	chrome.dll!ResourceDispatcherHost::OnMessageReceived(const IPC::Message & message=class=32, index=122, ResourceDispatcherHost::Receiver * receiver=0x0b16440c, bool * message_was_ok=0x0adff3f3)  Line 301 + 0x12 bytes	C++
 	chrome.dll!ResourceMessageFilter::OnMessageReceived(const IPC::Message & msg=class=32, index=122)  Line 448 + 0x38 bytes	C++
 	chrome.dll!IPC::ChannelProxy::Context::TryFilters(const IPC::Message & message=class=32, index=122)  Line 65 + 0x2c bytes	C++
 	chrome.dll!IPC::SyncChannel::SyncContext::OnMessageReceived(const IPC::Message & msg=class=32, index=122)  Line 292 + 0xc bytes	C++
 	chrome.dll!IPC::Channel::ChannelImpl::ProcessIncomingMessages(base::MessagePumpForIO::IOContext * context=0x09ba4104, unsigned long bytes_read=36)  Line 302 + 0x19 bytes	C++
 	chrome.dll!IPC::Channel::ChannelImpl::OnIOCompleted(base::MessagePumpForIO::IOContext * context=0x09ba4104, unsigned long bytes_transfered=36, unsigned long error=0)  Line 396 + 0x10 bytes	C++
 	chrome.dll!base::MessagePumpForIO::WaitForIOCompletion(unsigned long timeout=26, base::MessagePumpForIO::IOHandler * filter=0x00000000)  Line 502 + 0x1b bytes	C++
 	chrome.dll!base::MessagePumpForIO::WaitForWork()  Line 482	C++
 	chrome.dll!base::MessagePumpForIO::DoRunLoop()  Line 466 + 0x8 bytes	C++
 	chrome.dll!base::MessagePumpWin::RunWithDispatcher(base::MessagePump::Delegate * delegate=0x0adffd78, base::MessagePumpWin::Dispatcher * dispatcher=0x00000000)  Line 52 + 0xf bytes	C++
 	chrome.dll!base::MessagePumpWin::Run(base::MessagePump::Delegate * delegate=0x0adffd78)  Line 78 + 0x1c bytes	C++
 	chrome.dll!MessageLoop::RunInternal()  Line 204 + 0x2a bytes	C++
 	chrome.dll!MessageLoop::RunHandler()  Line 177	C++
 	chrome.dll!MessageLoop::Run()  Line 155	C++
 	chrome.dll!base::Thread::Run(MessageLoop * message_loop=0x0adffd78)  Line 137	C++
 	chrome.dll!base::Thread::ThreadMain()  Line 160 + 0x16 bytes	C++
 	chrome.dll!`anonymous namespace'::ThreadFunc(void * closure=0x09abf660)  Line 26 + 0xf bytes	C++
 	kernel32.dll!@BaseThreadInitThunk@12()  + 0xe bytes	
 	ntdll.dll!___RtlUserThreadStart@8()  + 0x23 bytes	
 	ntdll.dll!__RtlUserThreadStart@8()  + 0x1b bytes	


### js...@chromium.org (2010-06-09)

After some inspection, it looks like a stale pointer in the browser. Working out the details now, but it doesn't seem like it will be a complicated fix.

### sc...@gmail.com (2010-06-09)

Ugh. Does it affect v5 stable? If so, full steam ahead!

### in...@chromium.org (2010-06-09)

Yes Chris, it does affect v5 stable.

### js...@chromium.org (2010-06-09)

It looks like the problem here is that inside BufferedResourceHandler::CompleteResponseStarted() we see an "application/x-x509-user-cert" content type and call UseAlternateResourceHandler(), which ends up deleting a paused CrossSiteResourceHandler. A stale pointer for the CrossSiteResourceHandler is stored and later used after the request is resumed.

Wan-Teh, You seem like the most qualified one to work out the exact problem and knock out the patch. Do you have time to jump on this?


### in...@chromium.org (2010-06-09)

Adding Rodrigo Marcos (reporter)

### in...@chromium.org (2010-06-09)

ccing Gaurav Shah, who originally wrote this code to process x-x509-user-cert certs.

I had a chat with Wan-Teh on this. Basically, we should ONLY be processing x-x509-user-cert responses that arise from a <keygen> form post request (which is a cert enrollment request). Any others need to be discarded. Wan-Teh is planning to look at it today.

### js...@chromium.org (2010-06-09)

[Empty comment from Monorail migration]

### js...@chromium.org (2010-06-09)

My fear here is that there may be a way to silently trigger the processing of a cert, so we probably want to also clear out the paused CrossSiteResourceHandler.

### js...@chromium.org (2010-06-09)

Still fishing for whoever is most familiar with the relationship between these chunks of code.


### js...@chromium.org (2010-06-09)

Downgrading this because this can only be triggered from a typed/pasted URL. Hyperlink and automated navigation don't trigger the CrossSiteResourceHandler.

Also, wtc@ and brettw@ appear to have worked out a fix.


### js...@chromium.org (2010-06-09)

[Empty comment from Monorail migration]

### [Deleted User] (2010-06-10)

I wrote a changelist at http://codereview.chromium.org/2787005/show

I noticed that the download code also calls UseAlternateResourceHandler,
but when I typed a download URL in the location bar, Chrome didn't crash.
Upon looking into it closer, I found that the download code does one thing
that the x509-user-cert code doesn't do:

    info->set_is_download(true);

And that makes all the difference, because the is_download flag allows
the download code to bypass the problematic code in CrossSiteResourceHandler:

bool CrossSiteResourceHandler::OnResponseStarted(int request_id,
                                                 ResourceResponse* response) {
  ...
  ResourceDispatcherHostRequestInfo* info =
      ResourceDispatcherHost::InfoForRequest(request);

  // If this is a download, just pass the response through without doing a
  // cross-site check.  The renderer will see it is a download and abort the
  // request.
  if (info->is_download()) {
    return next_handler_->OnResponseStarted(request_id, response);  <=== SHORT CIRCUIT
  }

  // Tell the renderer to run the onunload event handler, and wait for the
  // reply.
  StartCrossSiteTransition(request_id, response, global_id);
  return true;
}

If I add the 

    info->set_is_download(true);

call to the x509-user-cert code, it also fixes the crash.

### in...@chromium.org (2010-06-10)

Thanks a lot Wan-Teh and Brett for fixing this quickly.

Looks like bugdroid went down. 
UseAlternateResourceHandler should set the non-owning pointer
to the CrossSiteResourceHandler in the extra request info to
NULL when it deletes the original ResourceHandler chain.

R=brettw,jschuh
BUG=46126
TEST=See bug report.

Committed: http://src.chromium.org/viewvc/chrome?view=rev&revision=49411

### bu...@gmail.com (2010-06-11)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=49411 

------------------------------------------------------------------------
r49411 | wtc@chromium.org | 2010-06-10 09:31:04 -0700 (Thu, 10 Jun 2010) | 8 lines
Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/renderer_host/buffered_resource_handler.cc?r1=49411&r2=49410

UseAlternateResourceHandler should set the non-owning pointer
to the CrossSiteResourceHandler in the extra request info to
NULL when it deletes the original ResourceHandler chain.

R=brettw,jschuh
BUG=46126
TEST=See bug report.
Review URL: http://codereview.chromium.org/2787005
------------------------------------------------------------------------


### bu...@gmail.com (2010-06-11)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=49562 

------------------------------------------------------------------------
r49562 | jschuh@chromium.org | 2010-06-11 11:43:26 -0700 (Fri, 11 Jun 2010) | 11 lines
Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/375/src/chrome/browser/renderer_host/buffered_resource_handler.cc?r1=49562&r2=49561

Merge 49411 - UseAlternateResourceHandler should set the non-owning pointer
to the CrossSiteResourceHandler in the extra request info to
NULL when it deletes the original ResourceHandler chain.

R=brettw,jschuh
BUG=46126
TEST=See bug report.
Review URL: http://codereview.chromium.org/2787005

TBR=wtc@chromium.org
Review URL: http://codereview.chromium.org/2766007
------------------------------------------------------------------------


### js...@chromium.org (2010-06-11)

[Empty comment from Monorail migration]

### [Deleted User] (2010-06-11)

[Empty comment from Monorail migration]

### sc...@gmail.com (2010-06-14)

@secforce.co.uk: thanks for the report! Provisional to giving us a chance to release this to users before disclosure, you've qualified for a $500 Chromium Security Reward.

We'll get this out relatively soon, but I don't have an exact date.

We'd like to credit you in the release notes. What name and optional affiliation should we use?

Feel free to file future Chromium issues directly here (using the Security template) rather than going via security@google.com.

### js...@chromium.org (2010-06-17)

Bulk edit for SecurityNotify Migration.

### sc...@gmail.com (2010-06-25)

Heya Rodrigo. If you e-mail me at cevans@chromium.org, we can start getting you in the system in order to pay your reward :)

### sc...@gmail.com (2010-06-26)

[Empty comment from Monorail migration]

### sc...@gmail.com (2010-08-31)

Payment is in electronic system. Since this is your first reward, please keep an eye out for successful arrival. Allow a few weeks.

Thanks again!

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-10-05)

Batch update.

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/46126?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-02-04)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081489)*
