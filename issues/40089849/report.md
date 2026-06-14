# Mac: Add hardening to protect against sandboxed processes calling CTFontManagerRegisterFontsForURL(), tricking LoadFontOnFileThread()

| Field | Value |
|-------|-------|
| **Issue ID** | [40089849](https://issues.chromium.org/issues/40089849) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P4 |
| **Component** | Internals>Sandbox |
| **Platforms** | Mac |
| **Reporter** | ha...@gmail.com |
| **Assignee** | ke...@chromium.org |
| **Created** | 2017-12-08 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:57.0) Gecko/20100101 Firefox/57.0

Steps to reproduce the problem:
I don't think this problem is exploitable, but a small change to one of the Mac sandbox profiles could inadvertently introduce a sandbox bypass for a compromised child process using this problem. Description of the problem and suggested changes below.

--

Description:

LoadFontOnFileThread(), which executes in the main process, opens a font file and makes the contents of the file available to renderer processes via shared memory.

It uses the following code to get the path to a font file on the filesystem for a font with the given name "font_name". The name is provided by the renderer process.

src/content/common/mac/font_loader.mm:
std::unique_ptr<FontLoader::ResultInternal> LoadFontOnFileThread(
    const base::string16& font_name,
    const float font_point_size) {
  ...
  NSFont* font_to_encode =
      [NSFont fontWithName:font_name_ns size:font_point_size];
  ...
  base::scoped_nsobject<NSURL> font_url(
      base::mac::CFToNSCast(base::mac::CFCastStrict<CFURLRef>(
          CTFontCopyAttribute(ct_font, kCTFontURLAttribute))));
  ...
}

The underlying font list used by the OS library call [NSFont fontWithName...] is controllable by a child process with both A) a connection to the font server and B) read/write access to a file on the filesystem. A process can call CTFontManagerRegisterFontsForURL()[1] and provide a file path to register a font that is visible to other processes. I don't think any Chromium child processes run with both A) and B). The renderer process has a connection to the font server, but not both read and write access to a file. It has write access to its log file, but not read access. Utility processes have read/write access to files, but no connection to the font server. In my tests, CTFontManagerRegisterFontsForURL() rejected font file paths the process did not have read access to.

If the renderer process sandbox was changed to allow read/write access to a file, it would be possible for a compromised renderer to

1) call CTFontManagerRegisterFontsForURL(NSURL myURL, kCTFontManagerScopeUser) to register a font where myURL is a file path to a symlink to a valid font named Foo.

2) then change the symlink to refer to a private file /Users/me/private.

3) then request the parent process read the font data for Foo by calling ::SandboxSupport::LoadFont("Foo").

4) access /Users/me/private data in the renderer process.

--

Suggested change:

1) Add the "vnode-type" requirement to the renderer profile to prevent renderers from writing symlinks. For example,

  (allow file-write* 
    (require-all (path (param log-file-path))
                 (vnode-type REGULAR-FILE)))

2) Change LoadFontOnFileThread() to not follow symlinks. This would affect loading of fonts on systems with font managers if the font manager software registers fonts using symlinks and places the link in a non-standard directory.

--

1. https://developer.apple.com/documentation/coretext/1499468-ctfontmanagerregisterfontsforurl?language=objc

What is the expected behavior?
N/A

What went wrong?
N/A

Did this work before? N/A 

Chrome version: 64.0.3275.0  Channel: dev
OS Version: OS X 10.13
Flash Version: Shockwave Flash 27.0 r0

## Timeline

### el...@chromium.org (2017-12-08)

> If the renderer process sandbox was changed to allow read/write access to a file

If a renderer process sandbox had read/write access to arbitrary files, this would itself be a significant vulnerability.

I'll let one of our sandbox experts comment on the proposed hardening.

[Monorail components: Internals>Sandbox]

### ha...@gmail.com (2017-12-08)

>> If the renderer process sandbox was changed to allow
>> read/write access to a file

> If a renderer process sandbox had read/write access to arbitrary
> files, this would itself be a significant vulnerability.

Hi, by "changed to allow read/write access to a file", I meant read/write access to a single file, not arbitrary access to files. For example, the renderer has write access to a log file now. If the sandbox was changed to also allow read access to the log file, that would be sufficient to use CTFontManagerRegisterFontsForURL() to bypass the sandbox read access restrictions. I don't think it's a problem now, but I think it makes sense to protect against. One wouldn't expect that allowing read/write access to a single file in the renderer sandbox rules would have this side effect.

### sh...@chromium.org (2017-12-09)

[Empty comment from Monorail migration]

### rs...@chromium.org (2017-12-14)

Thanks for the report, this is an interesting find!

I agree with your assessment that this isn't exploitable. Generally we don't want to give any file-write access to processes (except through brokered FDs), so I think the risk is low. However, defense-in-depth is a good policy, and this is subtle enough that having extra checks would be beneficial.

I think suggested change (1) is a good idea. We may even want to take it a step further and make it a macro to be used instead of file-write* to ensure that we always only write to regular files.

The concern you raise about (2) is probably going to occur for our users, so I'm less convinced we should make that change.

I've also been thinking that we may want to get rid of the current FontLoader implementation and switch to granting seatbelt extensions for font files (a much larger change than this bug).

Passing this over to Greg who's working on the sandbox policies now for looking at 1 and 2.

### bu...@chromium.org (2017-12-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/411ce7e1c0d06419ebb9174d34560ab7653f4057

commit 411ce7e1c0d06419ebb9174d34560ab7653f4057
Author: Greg Kerr <kerrnel@chromium.org>
Date: Fri Dec 15 18:25:43 2017

macOS V2 Sandbox: Harden sandbox by specifying vnode-type for writes.

This hardens the macOS sandbox by specifying an explicit vnode type for
all writeable files, reducing the risk that an attacker can symlink a
file Chrome has write access to, and modify the filesystem at will.

Bug: 793402
Change-Id: I53bbcc84345e432756eff0d2dc18a505719fd521
Reviewed-on: https://chromium-review.googlesource.com/829877
Reviewed-by: Robert Sesek <rsesek@chromium.org>
Commit-Queue: Greg Kerr <kerrnel@chromium.org>
Cr-Commit-Position: refs/heads/master@{#524413}
[modify] https://crrev.com/411ce7e1c0d06419ebb9174d34560ab7653f4057/services/service_manager/sandbox/mac/common_v2.sb
[modify] https://crrev.com/411ce7e1c0d06419ebb9174d34560ab7653f4057/services/service_manager/sandbox/mac/renderer_v2.sb


### ke...@chromium.org (2018-04-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-04-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-11-12)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-12-03)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-12-03)

Thanks for the report, haik.aftandilian@! The VRP panel has been looking at older bugs with security_impact-None and decided to award $500. A member of our finance team will be in touch to arrange payment. Cheers!

### aw...@google.com (2018-12-03)

[Empty comment from Monorail migration]

### is...@google.com (2018-12-03)

This issue was migrated from crbug.com/chromium/793402?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40089849)*
