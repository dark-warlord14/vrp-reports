# A vulnerability in run-mailcap can lead to code execution on Debian-based Linux distros with certain (nonstandard) desktop environments

| Field | Value |
|-------|-------|
| **Issue ID** | [40080709](https://issues.chromium.org/issues/40080709) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Platforms** | Linux |
| **CVE IDs** | CVE-2014-7209 |
| **Reporter** | ti...@blindspotsecurity.com |
| **Assignee** | jl...@chromium.org |
| **Created** | 2014-10-24 |
| **Bounty** | $500.00 |

## Description

Hi Guys,

I'm sitting on a RCE bug that is triggerable in Chrome and Chromium, but the issue is not in the browser itself. It is in an operating system component that Chrome uses on specific platforms under specific scenarios. I was hoping to find out if you guys would normally reward a bounty for something like this.

**VULNERABILITY DETAILS**  

\* With minimal user interaction, an attacker can execute arbitrary code as the Chrome user. I have a reliable working exploit for this.

\* The vulnerability lies in an OS component that exists only on a specific set of Linux distributions. These distributions are popular, but not all popular distributions are affected.

\* The affected Linux distributions must be configured in a specific, somewhat less common way in order to be rendered vulnerable with Chrome/Chromium.

\* The vulnerability can be exploited through software other than Chrome/Chromium. The configuration requirements that render the software vulnerable varies depending on the context and software being attacked. There are perhaps dozens of potential avenues for attack, but each may affect only a small number of users.

**VERSION**  

Chrome Version: all versions under Linux (?)  

Operating System: Specific Linux distributions

**REPRODUCTION CASE**  

If you guys think this vulnerability would be eligible for a bounty, then I'll happily provide all details.

Thanks!  

tim

## Attachments

- [evil-download.py](attachments/evil-download.py) (text/plain, 1.8 KB)

## Timeline

### in...@chromium.org (2014-10-24)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-10-27)

[Empty comment from Monorail migration]

### wf...@chromium.org (2014-10-28)

The final decision on whether a particular report is eligible to receive a reward is determined by the reward panel once we have fully diagnosed and fixed the bug (or notified third party upstream providers), so we cannot whether a particular bug will be eligible to receive a reward or not in advance of it being disclosed.

That notwithstanding, https://www.google.com/about/appsecurity/chrome-rewards/index.html says explicitly:

"Bugs may be eligible even if they are part of the base operating system and can manifest through Chrome."

However, historically bugs that require a large amount of user interaction or uncommon configurations can offer lower rewards - "Less convincing or more constrained bug submissions will likely qualify for reduced reward amounts, as chosen at the discretion of the reward panel."

We would encourage you to report this bug so we can further protect our users.  Feel free to attach the bug to this report (and we can reopen and rename), or just file a new one.  You could also consider responsibly disclosing the bug via other bounty programs such as Google's "patch rewards" program - https://www.google.com/about/appsecurity/patch-rewards/ or via HackerOne https://hackerone.com/programs

### ti...@blindspotsecurity.com (2014-10-29)

Thanks much for your detailed reply.  I did read the chrome rewards page, but I was just having a hard time figuring out what bounty program to submit to.  None is a great fit.  I'll just post the details here and see what you guys think.  Stay tuned.

### ti...@blindspotsecurity.com (2014-10-29)

Good morning.

A shell metacharacter injection vulnerability lies in the run-mailcap
utility.  This utility executes a command based on the file type
provided.  It is very similar in concept to xdg-open.  More information
on this utility can be found in:
  http://manned.org/run-mailcap.1

run-mailcap is installed under Debian, Ubuntu, and FreeBSD by default.
It likely exists in any Debian-derived distribution.  The vulnerability
has been verified as exploitable in Debian and Ubuntu.

run-mailcap uses configuration files (primarily /etc/mailcap) to
determine which command to run for specific actions on specific
file content types.  The command specified in this configuration file
may optionally contain printf-like escapes that dictate where the
callers file name argument is included.  For instance, under Debian's
configuration, one line may contain (assuming evince is installed):

application/pdf; evince %s; test=test -n "$DISPLAY"


If this line matches based on the content type, then the '%s' will be
replaced with the provided file name and the evince command will be
executed as: 
  evince the_filename_provided_to_run_mailcap.pdf

The most obvious vulnerability in run-mailcap lies in cases where no %s
is provided in the mailcap configuration entry.  Relevant vulnerable
code is provided below.  My annotations are included in #!! comments:

...
        if ($file ne "-") {
            if ($comm =~ m/[^%]%s/) {
#!! This path is taken if a %s exists in the mailcap configuration
#!! Note this next file name validation check, which limits exploitation here
                if (decode(langinfo(CODESET()), $file) =~ m![^[:alnum:],.:/@%^+=_-]!i) {
                    $match =~ m/nametemplate=(.*?)\s*($|;)/;
                    my $prefix = $1;
                    my $linked = 0;
                    while (!$linked) {
                        $tmplink = TempFile($prefix);
                        unlink($tmplink);
                        if ($file =~ m!^/!) {
                            $linked = symlink($file,$tmplink);
                        } else {
                            my $pwd = `/bin/pwd`;
                            chomp($pwd);
                            $linked = symlink("$pwd/$file",$tmplink);
                        }
                    }
                    print STDERR " - filename contains shell meta-characters; aliased to '$tmplink'\n" if $debug;
                    $comm =~ s/([^%])%s/$1$tmplink/g;
                } else {
                    $comm =~ s/([^%])%s/$1$file/g;
                }
            } else {
#!! This path is taken if no %s exists in the configuration
                if ($comm =~ m/\|/) {
                    $comm =~ s/\|/<\Q$file\E \|/;
                } else {
#!! This is the most typical path taken when %s doesn't exist in the configuration
#!! Note how the $file value is quoted using \Q and \E.  Seems safe, right?
                    $comm .= " <\Q$file\E";
                }
                if ($action eq 'edit' || $action eq 'compose') {
                    $comm .= " >\Q$file\E";
                }
            }
        } else {
            if ($comm =~ m/[^%]%s/) {
                $tmpfile = SaveStdin($match);
                $comm =~ s/([^%])%s/$1$tmpfile/g;

                # If needsterminal then redirect stdin to the tty which is
                # on stdout, rather than leaving it as the input data stream
                # which has now been read through to EOF.
                #
                # Some programs such as "more" and "less" already use
                # /dev/tty rather than stdin.  But "vim" on non-tty stdin
                # gives a warning message and then leaves the tty in raw
                # mode on exit.  Or "nvi" refuses to run at all unless both
                # stdin and stdout are the tty.
                #
                # RFC 1524 is silent on exactly what a program with
                # "needsterminal" should expect, but it seems sensible to
                # arrange that both stdin and stdout are the terminal for
                # "needsterminal" with "%s".
                #
                if ($needsterminal) {
                    $comm .= ' <&1';
                }
            } else {
                # no name means same as "-"... read from stdin
            }
        }
#!! This bit is complicated.  What do all of these do?  (BTW- I really hate perl)

        $comm =~ s!([^%])%t!$1$type!g;
        $comm =~ s!([^%])%F!$1!g;
        $comm =~ s!%{(.*?)}!$_="'$ENV{$1}'";s/\`//g;s/\'\'//g;$_!ge;

#!! Uh... WOOH!  What is this all about?  This strips off
#!! the backslash from anything that is already escaped!!!!
        $comm =~ s!\\(.)!$1!g;

#!! ... And then we convert any '' to '??
        $comm =~ s!\'\'!\'!g;

#!! ... AND unquote any semicolon?  Dear god man!
        $comm =~ s!$quotedsemi!;!go;
        $comm =~ s!$quotedprct!%!go;
	print STDERR "comm: $comm\n";
        print STDERR " - executing: $comm\n" if $debug;
	if ($norun) {
	    print $comm,"\n";
	    $res = 0;
	} else {

#!! Kaboom.  Command run, likely without adequate escaping
	    $res = system $comm;
...


Ok, so in the %s case an attacker can't do much because the script
checks for the majority of shell metacharacters.  (Or, rather, it makes
sure the file name contains only characters in a white list.)  If the
file name fails the test, it creates a sanely named symlink to the file
and runs the command on that, eliminating an attacker's control over the
file name.  (BTW, I haven't carefully inspected the tempfile symlink
code to see if it is safe.)  Note that the vast majority of command
templates in the Debian/Ubuntu mailcap configuration all contain %s.
However, one that exists by default that doesn't contain this is:

application/x-troff-man; /usr/bin/nroff -mandoc -Tutf8; copiousoutput; print=/usr/bin/nroff -mandoc -Tutf8 | print text/plain:-

So in this case, it turns out any file provided to run-mailcap with a
".man" extension will trigger this nroff command and allow us to execute
code. Let's try it out:

tim@shannon:~> uname -a
Linux shannon 3.16-1-amd64 #1 SMP Debian 3.16.2-2 (2014-09-08) x86_64 GNU/Linux
tim@shannon:~> touch '/tmp/evil;echo pwned;.man'
tim@shannon:~> run-mailcap '/tmp/evil;echo pwned;.man'
sh: 1: cannot open /tmp/evil: No such file
pwned
sh: 1: .man: not found


As you can see, "/tmp/evil" was all that was provided to nroff, which
didn't exist.  Then the echo ran with our payload, and finally
run-mailcap attempted to execute ".man", but this is not a valid
command.  Clearly there is command injection.


But how do we trigger this from Chrome?  Well this is a little
complicated.  Often when Chrome receives file download, it saves it and
prompts the user to open it by clicking on the button at the bottom of
the window.  When this is clicked under Linux, the xdg-open command is
run on the local file path of where it was saved.  

xdg-open is a fairly complex beast of a shell script.  Upon startup, it
attempts to detect what desktop environment you are using, whether that
be Gnome, KDE, XFCE, or something else.  If xdg-open *cannot* determine
what desktop environment is in use, then it will fall back on some more
basic utilities, including run-mailcap.  Here's that case statement:

...
detectDE

if [ x"$DE" = x"" ]; then
    DE=generic
fi

DEBUG 2 "Selected DE $DE"

# if BROWSER variable is not set, check some well known browsers instead
if [ x"$BROWSER" = x"" ]; then
    BROWSER=www-browser:links2:elinks:links:lynx:w3m
    if [ -n "$DISPLAY" ]; then
        BROWSER=x-www-browser:firefox:seamonkey:mozilla:epiphany:konqueror:chromium-browser:google-chrome:$BROWSER
    fi
fi

case "$DE" in
    kde)
    open_kde "$url"
    ;;

    gnome*)
    open_gnome "$url"
    ;;

    mate)
    open_mate "$url"
    ;;

    xfce)
    open_xfce "$url"
    ;;

    lxde)
    open_lxde "$url"
    ;;

    generic)
    open_generic "$url"
    ;;

    *)
    exit_failure_operation_impossible "no method available for opening '$url'"
    ;;
esac
...


In order to get run-mailcap to run, the attacker needs the "generic"
case to be used.  This is true if the user isn't running X windows (and
is instead somehow causing xdg-open to be run from the text terminal or
a remote shell) or if the user is using X windows without one of the
bloated^W desktop environments listed above.  So long as one of these
cases is true, it is fairly easy to coax xdg-open into using
run-mailcap.  Of course this means any program calling xdg-open or
run-mailcap directly could be vulnerable to attack.  This includes
things like the mutt email client, possibly claws mail, and any number
of other programs.  I'm not yet sure how deep this particular rabbit hole
goes.

An additional limitation on the attack in the case of Chrome or Chromium
is that the browser squashes certain special characters in the file
name.  It either converts these to '_' or removes them.  Unusable
characters include:
  |"\<>?:*

So this does make life a little difficult.  However, I was able to
bootstrap an attack that allows arbitrary shell commands to be run,
regardless of character set.  I'm attaching a small Python script which
acts as a malicious web server.  To test this, do the following:

1. First, set up a Debian or Ubuntu Linux system which runs without a
   desktop environment.  You can do this by disabling gdm and setting up
   xdm with a basic window manager (e.g. fluxbox) through your .Xsession file.  
   Let me know if you are unsure how to do this.
   (If you are lazy and want to skip this step, just edit your xdg-open
   command and put "DE=generic" just before the final case statement.)

2. Next, start up the python script.  It will listen on http://127.0.0.1:8666/

3. Access any page on the malicious webserver with Chrome or Chromium.
   The server will immediately push a file back to the browser with
   Content-Disposition to force a file download.

4. Click on the downloaded file to open it.  This will cause the exploit
   to run immediately. (Note how long the prefix of the filename
   is... it prevents users from easily seeing the ugly shell bit at the
   end of the file name, at least on my system.)

5. Check your home directory.  If successful, a new empty file should
   appear named 'u-been-mailcapped!'


There are other potential attack scenarios than I have described here.
Some I haven't had time yet to explore.  I'll follow up with more info
once you guys have sunk your teeth into these bits.


### ti...@blindspotsecurity.com (2014-11-04)

Hey Guys... any thoughts on this one?  Care to re-open it?

### mb...@chromium.org (2014-11-04)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-11-05)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-11-09)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-11-10)

[Empty comment from Monorail migration]

### ti...@blindspotsecurity.com (2014-11-13)

I'm quite surprised at how long it is taking for someone to get back to me on this.  Seems un-Google-like.  Is this normal?  When can I expect a response?  Thank you.

### cl...@chromium.org (2014-11-14)

[Empty comment from Monorail migration]

### mb...@chromium.org (2014-11-14)

Sorry for the delay here. We definitely messed up with the triage on this one. For next time, it would probably be better to open a new bug with a more descriptive summary, but we should have caught this anyway.

Once this is fixed upstream, the reward panel will consider it.

### cl...@chromium.org (2014-11-14)

cevans@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### ti...@blindspotsecurity.com (2014-11-14)

I suspected it may have been forgotten, but "wfh" did say I could post here.  Seemed like the chain of discussion would have been better preserved that way, so that's why I did it.

Do you guys need help notifying the various distributions?

### ti...@blindspotsecurity.com (2014-11-14)

In case you guys are curious, a similar bug was just posted on FD:
  http://seclists.org/fulldisclosure/2014/Nov/36

I knew about this one as well, but it isn't as serious as the one I have posted here due to the limited sets of systems it affects.  My exploit works for both bugs.  

This bug is different in that it exists in xdg-open, rather than run-mailcap, but the system configuration requirements are very similar (window manager, etc).  While xdg-open exists on most Linux systems, for some reason the bug described in the FD post didn't seem to apply to most of the systems I looked at, except my Debian box.  I hadn't finished researching the xdg-open bug, but planned on filling you in on it once I understood it better.  Anyway, that particular kitten is out of the bag now.

To be clear, the run-mailcap bug is still out there and is still a 0-day AFAIK.


### mb...@chromium.org (2014-11-14)

If you want to notify the affected distributions, that would be helpful.

cevans: Ping. Did you have a chance to look at this bug? Should I try to find another owner?

### ti...@blindspotsecurity.com (2014-11-15)

Ok, I can help with a few of the distributions; namely Debian, Ubuntu, and FreeBSD.  I don't know how to easily check for other distros that may rely on these packages or have forked them.

I'll try to submit some bugs to Debian and Ubuntu this weekend.  Let me know if you notify any distros before me. Thanks!

### ti...@blindspotsecurity.com (2014-11-15)

How should we manage the embargo with the affected distros?  Should we consider using the distros list[1]?

1. http://oss-security.openwall.org/wiki/mailing-lists/distros

### mb...@chromium.org (2014-11-15)

Seems reasonable to me.

### ti...@blindspotsecurity.com (2014-11-17)

Ok, I kind of expected you guys would have had a more standard procedure for this kind of thing.  If not, then I'll plan on notifying Debian, Ubuntu, and FreeBSD directly today via email.  Let me know if you want me to CC any of you.  

After these distros have worked out a patch for the problem, I'll notify the distros mailing list to ensure other distros have a chance to fix it if they also rely on this utility before making it public.

### ti...@blindspotsecurity.com (2014-11-18)

Just emailed security contacts at Debian, Ubuntu and FreeBSD.

Is there any possibility that ChromeOS could be affected?  I noticed a mime-support portage entry for it, but I'm not really familiar with the platform.

### mb...@chromium.org (2014-11-18)

It doesn't seem too likely that this could affect Chrome OS. Jorge, can you confirm?

### jo...@chromium.org (2014-11-18)

There is no run-mailcap in Chrome OS.

### ti...@blindspotsecurity.com (2014-11-18)

Thank you.  I kind of figured as much, but it would be kind of embarrassing if no one bothered to check.

### cl...@chromium.org (2014-11-22)

cevans@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### sc...@gmail.com (2014-11-22)

Not sure why this was assigned to me?

### cl...@chromium.org (2014-11-25)

[Empty comment from Monorail migration]

### ke...@chromium.org (2014-11-27)

Sorry that this bug has been left in limbo for most of the last month. We are usually a lot more prompt in our triage.

I just read the descriptions, and it isn't clear to me what Chromium should be doing with this. The don't know of any precedent where we try to mitigate exploits of OS vulnerabilities by downloaded files, except that we add actual known malware hashes to the safebrowsing blacklist.

jln or mdempsky, do either of you have any thoughts on this?

I am assigning to jln just to have an owner, but I think it should be closed unless there are reasonable actions we can take to mitigate.

### md...@chromium.org (2014-11-27)

Seems like if we wanted to prevent this issue within Chromium, we could extend the download filename character blacklist with more shell metacharacters (e.g., $ ` ; & and maybe more), and perhaps that's a prudent short-term mitigation.  But unless I'm overlooking something, it seems like this is really an issue for xdg-open/run-mailcap to fix, since I'd also expect the impact extends beyond just Chromium.

As far as Chrome is concerned, the fact that this doesn't affect GNOME/KDE/XFCE users seems reassuring at least in terms of impact.  (Though personally as an Xmonad user, it's less so. :P)

### ti...@blindspotsecurity.com (2014-11-28)

Yeah, it's definitely an issue with run-mailcap.  You could blacklist more filename special characters, but you'd need quite a few to fully prevent attacks.

I've been exchanging emails with Debian, Ubuntu, and FreeBSD security contacts, but they are taking their time in analyzing the issue.  As far as I know, nothing is happening.  I don't feel entirely confident in submitting a patch myself, since I don't do much Perl and I'm unsure of the reasoning behind the current script's design.  But if they keep dragging their feet, I'll submit a heavy-handed patch to prevent exploitation and see what they do with it.

As for the set of users affected, it surely is a small minority of Linux desktop users.  However, running a non-GNOME/KDE/XFCE window manager is not as uncommon as some might like to think.  I personally do, and here we have one Xmonad user.  There are a huge number of window managers out there.  Also, after submitting this bug, I was searching around and came across this:
  https://code.google.com/p/chromium/issues/detail?id=182458

This is clearly the same issue, but folks didn't realize it was a vulnerability. So there's at least 3 people affected now. ;-)

### cl...@chromium.org (2014-12-05)

jln@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### ti...@blindspotsecurity.com (2014-12-11)

After some sabre rattling and such, I've got the Debian folks to start making progress on this.  They've assigned this CVE:

CVE-2014-7209 run-mailcap shell command injection

Hopefully they'll have a fix ready soon.

### cl...@chromium.org (2014-12-12)

jln@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-12-18)

jln@: Uh oh! This issue is still open and hasn't been updated in the last 20 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-12-19)

jln@: Uh oh! This issue is still open and hasn't been updated in the last 20 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### ti...@blindspotsecurity.com (2015-01-05)

Closing the loop on this: The issue has been fixed and published.  For more info, see:

https://www.debian.org/security/2014/dsa-3114
http://www.openwall.com/lists/oss-security/2014/12/31/8



### cl...@chromium.org (2015-01-09)

jln@: Uh oh! This issue is still open and hasn't been updated in the last 42 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### ti...@blindspotsecurity.com (2015-01-10)

Could someone close this bug out and send it over to the reward panel?  Thanks much.


### in...@chromium.org (2015-01-10)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-01-10)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### in...@chromium.org (2015-01-25)

Julien, is any merge to be done here ? If yes, lets do it for m41 since this is sec-medium bug.

### pe...@google.com (2015-01-25)

[Automated comment] No bugdroid (commit) comments found, couldn't auto-approve, needs manual review.

### pe...@chromium.org (2015-01-26)

If you're still wanting an M41 merge for this, could somebody point me at a trunk CL with the required fixes?

### pe...@chromium.org (2015-01-29)

Bump.  Can someone point me to a CL, if a merge it still needed?

### jo...@chromium.org (2015-01-29)

There's no CLs on the Chrome side, this was fixed in the mime-support package.

### pe...@chromium.org (2015-01-29)

Thank you!  Done.

### ti...@blindspotsecurity.com (2015-02-13)

Has this been reviewed by the reward panel yet?  The fix isn't dependent on a new Chrome release, and it's already public.  It's been over a month since the issue was resolved.

### mb...@chromium.org (2015-02-13)

Not yet. Since this is tagged with M-41, it will likely be reviewed shortly before the Chrome 41 release.

Even though it's not a perfect fit, I'm adding the Release-0-M41 label here to ensure that we don't forget about it.

### ti...@google.com (2015-03-05)

Just letting you know that the reward panel reviewed this bug and decided to award you $500 for making us aware of this issue (noting that there was no fix on the chrome side).

Someone from our finance area should be in contact in a week or two. If that doesn't happen, please contact me directly or update this bug and I'll reach out.

Congratulations!

### ti...@google.com (2015-03-06)

[Empty comment from Monorail migration]

### ti...@google.com (2015-04-02)

Processing via our e-payment system can take up to six weeks, but the reward should be on its way to you. Thanks again for your help!


### cl...@chromium.org (2015-04-18)

Bulk update: removing view restriction from closed bugs.

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/426890?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080709)*
