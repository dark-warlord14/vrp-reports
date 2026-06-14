# Renderer crash on very big animated gif image @ WebCore::RGBA32Buffer::setRGBA(unsigned int *,unsigned int,unsigned int,unsigned int,unsigned int)

| Field | Value |
|-------|-------|
| **Issue ID** | [40083056](https://issues.chromium.org/issues/40083056) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | si...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2010-09-04 |
| **Bounty** | $500.00 |

## Description

Chrome Version : 7.0.503.1 (Official Build 57041) dev  

URLs (if applicable) : <http://asset.soup.io/asset/1056/8367_7835_48-square.gif>  

backup: <http://home.arcor.de/slxviper/8367_7835_48-square.gif>  

**Other browsers tested:**  

**Add OK or FAIL after other browsers where you have tested this issue:**  

**Safari 4:**  

Firefox 3.x: FAIL/(ok)  

**IE 7:**  

IE 8: (ok)

**What steps will reproduce the problem?**

1. open above url (animated gif image, actual size 10176x7632 px)
2. observe RAM consumption

**What is the expected result?**  

Image is displayed, browser and OS are continuing to work normally.  

OR: Warning is displayed, allocation of even more RAM is stopped.

**What happens instead?**  

Huge amounts of RAM are consumed, until...  

a) on Windows: some RAM is allocated, "sad tab" is displayed, RAM is freed again  

b) on Linux: all available RAM ist allocated, everything hangs until killing that chrome process (which isn't that easy in this situation...)

**Please provide any additional information below. Attach a screenshot if**  

**possible.**  

IE8 consumes about 110MB overall, FF 3.6.8 on Linux crashes as well, FF 3.6 on Windows needs about 360MB overall. Some image viewers crash as well.

This bug was reported to soup.io as well, since the image should be only 48x48 px, so there seems to be a bug on their side as well.

## Timeline

### [Deleted User] (2010-09-07)

Thanks for the report.

Stack Trace
------------
Thread 0 *CRASHED* ( EXCEPTION_ACCESS_VIOLATION_WRITE @ 0x00000098 )

0x022cdebd	 [chrome.dll	 - imagedecoder.h:167]	WebCore::RGBA32Buffer::setRGBA(unsigned int *,unsigned int,unsigned int,unsigned int,unsigned int)
0x022cde10	 [chrome.dll	 - imagedecoder.h:132]	WebCore::RGBA32Buffer::setRGBA(int,int,unsigned int,unsigned int,unsigned int,unsigned int)
0x022cf542	 [chrome.dll	 - gifimagedecoder.cpp:228]	WebCore::GIFImageDecoder::haveDecodedRow(unsigned int,unsigned char *,unsigned char *,unsigned int,unsigned int,bool)
0x022d5faf	 [chrome.dll	 - gifimagereader.cpp:164]	GIFImageReader::output_row()
0x022d624b	 [chrome.dll	 - gifimagereader.cpp:356]	GIFImageReader::do_lzw(unsigned char const *)
0x022d63b7	 [chrome.dll	 - gifimagereader.cpp:446]	GIFImageReader::read(unsigned char const *,unsigned int,WebCore::GIFImageDecoder::GIFQuery,unsigned int)
0x022cf6bf	 [chrome.dll	 - gifimagedecoder.cpp:313]	WebCore::GIFImageDecoder::decode(unsigned int,WebCore::GIFImageDecoder::GIFQuery)
0x022cf316	 [chrome.dll	 - gifimagedecoder.cpp:124]	WebCore::GIFImageDecoder::frameBufferAtIndex(unsigned int)
0x0226e297	 [chrome.dll	 - imagesource.cpp:132]	WebCore::ImageSource::createFrameAtIndex(unsigned int)
0x02251254	 [chrome.dll	 - bitmapimage.cpp:121]	WebCore::BitmapImage::cacheFrame(unsigned int)
0x02251447	 [chrome.dll	 - bitmapimage.cpp:224]	WebCore::BitmapImage::frameIsCompleteAtIndex(unsigned int)
0x02251691	 [chrome.dll	 - bitmapimage.cpp:336]	WebCore::BitmapImage::startAnimation(bool)
0x021c32c2	 [chrome.dll	 - imageskia.cpp:460]	WebCore::BitmapImage::draw(WebCore::GraphicsContext *,WebCore::FloatRect const &,WebCore::FloatRect const &,WebCore::ColorSpace,WebCore::CompositeOperator)
0x0212bbbf	 [chrome.dll	 - graphicscontext.cpp:410]	WebCore::GraphicsContext::drawImage(WebCore::Image *,WebCore::ColorSpace,WebCore::FloatRect const &,WebCore::FloatRect const &,WebCore::CompositeOperator,bool)
0x0212b77f	 [chrome.dll	 - graphicscontext.cpp:329]	WebCore::GraphicsContext::drawImage(WebCore::Image *,WebCore::ColorSpace,WebCore::IntRect const &,WebCore::IntRect const &,WebCore::CompositeOperator,bool)
0x0212b745	 [chrome.dll	 - graphicscontext.cpp:319]	WebCore::GraphicsContext::drawImage(WebCore::Image *,WebCore::ColorSpace,WebCore::IntRect const &,WebCore::CompositeOperator,bool)
0x021bbbe4	 [chrome.dll	 - renderimage.cpp:349]	WebCore::RenderImage::paintIntoRect(WebCore::GraphicsContext *,WebCore::IntRect const &)
0x021bb6b2	 [chrome.dll	 - renderimage.cpp:288]	WebCore::RenderImage::paintReplaced(WebCore::PaintInfo &,int,int)
0x021ccc9b	 [chrome.dll	 - renderreplaced.cpp:145]	WebCore::RenderReplaced::paint(WebCore::PaintInfo &,int,int)
0x021bb9b8	 [chrome.dll	 - renderimage.cpp:294]	WebCore::RenderImage::paint(WebCore::PaintInfo &,int,int)
0x02164d6e	 [chrome.dll	 - inlinebox.cpp:180]	WebCore::InlineBox::paint(WebCore::PaintInfo &,int,int)
0x021611fa	 [chrome.dll	 - inlineflowbox.cpp:696]	WebCore::InlineFlowBox::paint(WebCore::PaintInfo &,int,int)
0x0215f1a8	 [chrome.dll	 - rootinlinebox.cpp:166]	WebCore::RootInlineBox::paint(WebCore::PaintInfo &,int,int)
0x021ca141	 [chrome.dll	 - renderlineboxlist.cpp:220]	WebCore::RenderLineBoxList::paint(WebCore::RenderBoxModelObject *,WebCore::PaintInfo &,int,int)
0x021b35ca	 [chrome.dll	 - renderblock.cpp:2094]	WebCore::RenderBlock::paintContents(WebCore::PaintInfo &,int,int)
0x021b3a12	 [chrome.dll	 - renderblock.cpp:2204]	WebCore::RenderBlock::paintObject(WebCore::PaintInfo &,int,int)
0x021b3208	 [chrome.dll	 - renderblock.cpp:1985]	WebCore::RenderBlock::paint(WebCore::PaintInfo &,int,int)
0x021b37be	 [chrome.dll	 - renderblock.cpp:2137]	WebCore::RenderBlock::paintChildren(WebCore::PaintInfo &,int,int)
0x021b35d1	 [chrome.dll	 - renderblock.cpp:2096]	WebCore::RenderBlock::paintContents(WebCore::PaintInfo &,int,int)
0x021b3a12	 [chrome.dll	 - renderblock.cpp:2204]	WebCore::RenderBlock::paintObject(WebCore::PaintInfo &,int,int)
...... (11 stack frames dropped.)
0x01d5679f	 [chrome.dll	 - render_widget.cc:531]	RenderWidget::DoDeferredUpdate()
0x01d5652f	 [chrome.dll	 - render_widget.cc:456]	RenderWidget::CallDoDeferredUpdate()
0x01d58217	 [chrome.dll	 - ipc_message.h:135]	IPC::Message::Dispatch<RenderView>(IPC::Message const *,RenderView *,void ( RenderView::*)(void))
0x01d55db1	 [chrome.dll	 - render_widget.cc:167]	RenderWidget::OnMessageReceived(IPC::Message const &)
0x01d2247b	 [chrome.dll	 - render_view.cc:810]	RenderView::OnMessageReceived(IPC::Message const &)
0x0202f8fa	 [chrome.dll	 - message_router.cc:40]	MessageRouter::RouteMessage(IPC::Message const &)
0x0202f8d4	 [chrome.dll	 - message_router.cc:31]	MessageRouter::OnMessageReceived(IPC::Message const &)
0x0202229f	 [chrome.dll	 - child_thread.cc:163]	ChildThread::OnMessageReceived(IPC::Message const &)
0x025ff875	 [chrome.dll	 - task.h:327]	RunnableMethod<CancelableRequest<CallbackRunner<Tuple1<std::map<GURL,std::basic_string<wchar_t,std::char_traits<wchar_t>,std::allocator<wchar_t> >,std::less<GURL>,std::allocator<std::pair<GURL const ,std::basic_string<wchar_t,std::char_traits<wchar_t>,std::allocator<wchar_t> > > > > > > >,void ( CancelableRequest<CallbackRunner<Tuple1<std::map<GURL,std::basic_string<wchar_t,std::char_traits<wchar_t>,std::allocator<wchar_t> >,std::less<GURL>,std::allocator<std::pair<GURL const ,std::basic_string<wchar_t,std::char_traits<wchar_t>,std::allocator<wchar_t> > > > > > > >::*)(Tuple1<std::map<GURL,std::basic_string<wchar_t,std::char_traits<wchar_t>,std::allocator<wchar_t> >,std::less<GURL>,std::allocator<std::pair<GURL const ,std::basic_string<wchar_t,std::char_traits<wchar_t>,std::allocator<wchar_t> > > > > > const &),Tuple1<Tuple1<std::map<GURL,std::basic_string<wchar_t,std::char_traits<wchar_t>,std::allocator<wchar_t> >,std::less<GURL>,std::allocator<std::pair<GURL const ,std::basic_string<wchar_t,std::char_traits<wchar_t>,std::allocator<wchar_t> > > > > > > >::Run()
0x01cf2187	 [chrome.dll	 - message_loop.cc:408]	MessageLoop::RunTask(Task *)
0x01cf2213	 [chrome.dll	 - message_loop.cc:417]	MessageLoop::DeferOrRunPendingTask(MessageLoop::PendingTask const &)
0x01cf23a9	 [chrome.dll	 - message_loop.cc:524]	MessageLoop::DoWork()
0x01d05c60	 [chrome.dll	 - message_pump_default.cc:50]	base::MessagePumpDefault::Run(base::MessagePump::Delegate *)
0x01cf1f36	 [chrome.dll	 - message_loop.cc:256]	MessageLoop::RunInternal()
0x01cf1ebb	 [chrome.dll	 - message_loop.cc:228]	MessageLoop::RunHandler()
0x01cf1e69	 [chrome.dll	 - message_loop.cc:206]	MessageLoop::Run()
0x01d19b51	 [chrome.dll	 - renderer_main.cc:294]	RendererMain(MainFunctionParams const &)
0x01c33b1c	 [chrome.dll	 - chrome_dll_main.cc:807]	ChromeMain
0x004039fc	 [chrome.exe	 - client_util.cc:247]	MainDllLoader::Launch(HINSTANCE__ *,sandbox::SandboxInterfaceInfo *)
0x00403ff7	 [chrome.exe	 - chrome_exe_main.cc:46]	wWinMain

Full report @ http://crash/reportdetail?reportid=dd043a662fffdaf9

This is happening with 5.0, 6.0 and 7.0.518.0
Might be related to https://crbug.com/chromium/6062. Marking as private for now.

### pk...@chromium.org (2010-09-07)

[Empty comment from Monorail migration]

### pk...@chromium.org (2010-09-24)

This one is easy (and not a regression); filed upstream as https://bugs.webkit.org/show_bug.cgi?id=46437 , to be patched shortly.

### pk...@chromium.org (2010-09-28)

Fixed upstream in http://trac.webkit.org/changeset/68446

### sc...@gmail.com (2010-09-28)

Upon analysis, this is a security bug. We'll merge it to M7.

Although the pointer written to is always based on NULL, the attacker can write to semi-arbitrary offsets by using a frame that has a non-zero x,y offset into the destination canvas.

### in...@chromium.org (2010-10-01)

[Empty comment from Monorail migration]

### in...@chromium.org (2010-10-04)

Merged in r69027 to 517.

### sc...@gmail.com (2010-10-14)

@sixviper: thanks for your help finding this. I'll credit you in our release notes as "sixviper", unless you wanted to give a different name?

### si...@gmail.com (2010-10-14)

Thanks for the credit. You could use my full name, Simon Schaak, for the release notes.

### sc...@gmail.com (2010-10-15)

@slxviper: congratulations! Your report was very useful and enabled us to correct a security bug. Therefore, you've qualified for a provisional $500 under the Chromium Security Rewards program.
----
Boilerplate text: please do NOT publicly disclose details until a fix has been
released to all our users. Public disclosure may cancel the provisional reward.
----

### si...@gmail.com (2010-10-16)

Nice to hear, I accecpt. Please contact me by (google)mail for further information.

### js...@chromium.org (2010-10-17)

[Empty comment from Monorail migration]

### sc...@gmail.com (2010-11-03)

[Empty comment from Monorail migration]

### sc...@gmail.com (2010-11-21)

Payment is in the electronic system.

### la...@chromium.org (2011-03-19)

Chrome Version : 7.0.503.1 (Official Build 57041) dev  

URLs (if applicable) : <http://asset.soup.io/asset/1056/8367_7835_48-square.gif>  

backup: <http://home.arcor.de/slxviper/8367_7835_48-square.gif>  

**Other browsers tested:**  

**Add OK or FAIL after other browsers where you have tested this issue:**  

**Safari 4:**  

Firefox 3.x: FAIL/(ok)  

**IE 7:**  

IE 8: (ok)

**What steps will reproduce the problem?**

1. open above url (animated gif image, actual size 10176x7632 px)
2. observe RAM consumption

**What is the expected result?**  

Image is displayed, browser and OS are continuing to work normally.  

OR: Warning is displayed, allocation of even more RAM is stopped.

**What happens instead?**  

Huge amounts of RAM are consumed, until...  

a) on Windows: some RAM is allocated, "sad tab" is displayed, RAM is freed again  

b) on Linux: all available RAM ist allocated, everything hangs until killing that chrome process (which isn't that easy in this situation...)

**Please provide any additional information below. Attach a screenshot if**  

**possible.**  

IE8 consumes about 110MB overall, FF 3.6.8 on Linux crashes as well, FF 3.6 on Windows needs about 360MB overall. Some image viewers crash as well.

This bug was reported to soup.io as well, since the image should be only 48x48 px, so there seems to be a bug on their side as well.

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-10-05)

Batch update.

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

### bu...@chromium.org (2013-04-06)

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

This issue was migrated from crbug.com/chromium/54500?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083056)*
