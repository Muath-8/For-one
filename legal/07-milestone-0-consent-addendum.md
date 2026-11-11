# Milestone 0 consent addendum

> **Draft for counsel. Not legal advice.** The addendum ADR-24.16 requires for the 15 Milestone 0 pilot learners, in two parts per ADR-24.B10, in the plain style of [milestone-0/02-consent.md](../milestone-0/02-consent.md). **Part 1 (vendor tests) must be signed before any pilot clip goes to a vendor. Part 2 (the bridge, re-onboarding, fixtures and import) by 2026-12-15** (register A9, ADR-24.B28). Anyone who does not sign Part 2 keeps the original promise: all pilot data deleted by 2026-12-31. **Counsel must confirm:** how to handle clips that may already have reached vendors the pilot consent did not name (pack A-10, item 1); whether de-identified text and voice fixtures need consent (they are pseudonymized, not anonymous, so we assume yes); the fixture retention date.

**How to send it (for Muath; delete before sending).**
- Two Google Forms, like the pilot consent: English with the Arabic under each part, each box its own optional question, so the form records who agreed to what and when. For a learner whose message language is neither, add a machine translation and say it is one; the English text counts.
- **Send Part 1 now.** No pilot clip goes to any vendor for a learner until that learner has ticked Part 1's box. Send Part 2 so every box is answered by **2026-12-15** (ADR-24.B28). Then delete, by 2026-12-31, the pilot data of anyone who did not sign, and the material each signer did not tick, as the pilot consent promised.
- **Before sending Part 1, fill in its facts truthfully:** which vendors received pilot clips, on which dates, and whether each has confirmed deletion. If no clip has left yet, use the "not yet" wording and delete the other.
- Every box is optional; not answering means no. Anyone who does not tick Part 2 box 1 gets no bridge episodes (offer the full refund instead, register A15); anyone who does not tick box 2 is not invited to the end-to-end run in the last build week; anyone who does not tick box 4 or 5 has none of that material in fixtures. Record the answers in the Roster tab.
- **Never** put a pilot learner's text or voice, de-identified or not, in the public repository. The handbook says the repository is public today ([engineering/09 §6](../engineering/09-data-handling.md)).
- If the build imports pilot learner files into the new system (01 §10 #11), keep Part 2 box 3; if it doesn't, delete it.

---

## Part 1: testing speech services with your clips (sign before any clip leaves)

### English

**For one pilot: one question about your voice clips**

Thank you again for the pilot. We're now building the real For one, and there's one thing we want to do with your pilot clips that wasn't in the consent you signed. It needs a separate yes from you. It's optional, and saying no changes nothing else: your pilot data is still deleted by 31 December 2026, unless you chose to keep your recordings.

**What we'd do.** To choose which speech-to-text and pronunciation services the new app uses, we play the same real learner clips through several services and compare how well each one keeps what was actually said. The services: `[list, e.g. Soniox, Deepgram, AssemblyAI, ElevenLabs Scribe, Speechace]`, most of them in the US. Each one processes the clips only to return a transcript or a score, under its business terms, with storage and training switched off where the service allows. We'd use up to `[N]` short clips of your calls.

`[If no clip has been sent yet:]` We have not sent any of your clips to these services. We will only send yours if you tick the box below.

`[If clips were already sent:]` Between `[date]` and `[date]` we sent `[N]` of your clips to `[services]` before asking you, because we thought the pilot consent covered it. It did not name these services, and we're sorry. We have asked them to delete the clips, and `[which]` have confirmed. If you don't tick the box, we send nothing more and remove your clips from the test results.

**Your rights stay the same.** Ask for a copy, a correction or deletion at any time with one message on WhatsApp; we act within 7 days. You also have the rights the data protection law where you live gives you.

- (Optional) You may use up to `[N]` of my clips to test speech services, as described above.

Name: ________  Date: ________

### Arabic (draft for Muath's read)

**تجربة For one: سؤال واحد عن مقاطع صوتك**

شكراً لك مرة أخرى على المشاركة في التجربة. نحن الآن نبني النسخة الحقيقية من For one، وهناك أمر واحد نريد أن نفعله بمقاطع صوتك من التجربة لم يكن في الموافقة التي وقّعتها، ويحتاج موافقة منفصلة منك. الموافقة اختيارية، والرفض لا يغيّر شيئاً آخر: بيانات التجربة تُحذف في موعد أقصاه ٣١ ديسمبر ٢٠٢٦، إلا إذا اخترت أن نحتفظ بتسجيلاتك.

**ماذا سنفعل.** لنختار خدمات تحويل الكلام إلى نص وتقييم النطق التي سيستخدمها التطبيق الجديد، نشغّل مقاطع حقيقية من المتعلمين على عدة خدمات ونقارن أيها يحافظ أكثر على ما قيل فعلاً. الخدمات: `[القائمة]`، وأغلبها في أمريكا. كل خدمة تعالج المقاطع فقط لتعيد نصاً أو تقييماً، وفق شروطها التجارية، مع إيقاف الحفظ والتدريب حيث تسمح الخدمة. سنستخدم ما لا يزيد على `[N]` مقاطع قصيرة من مكالماتك.

`[إذا لم يُرسل أي مقطع بعد:]` لم نرسل أي مقطع من مقاطعك إلى هذه الخدمات، ولن نرسلها إلا إذا وافقت على الخانة أدناه.

`[إذا أُرسلت مقاطع:]` بين `[تاريخ]` و`[تاريخ]` أرسلنا `[N]` من مقاطعك إلى `[الخدمات]` قبل أن نسألك، لأننا ظننا أن موافقة التجربة تشملها. لم تكن تذكر هذه الخدمات، ونعتذر لك. طلبنا منها حذف المقاطع، وأكدت `[أي منها]` الحذف. إذا لم توافق على الخانة فلن نرسل شيئاً آخر وسنحذف مقاطعك من نتائج الاختبار.

**حقوقك كما هي.** اطلب نسخة من بياناتك أو تصحيحها أو حذفها في أي وقت برسالة واحدة على الواتساب، ونتصرف خلال ٧ أيام. ولك أيضاً الحقوق التي يعطيك إياها قانون حماية البيانات في البلد الذي تعيش فيه.

- ☐ **(اختياري)** أوافق على استخدام ما لا يزيد على `[N]` من مقاطعي لاختبار خدمات تحويل الكلام، كما هو موضح أعلاه.

الاسم: ________  التاريخ: ________

---

## Part 2: the bridge, the new app and quality tests (by 2026-12-15)

### English

**For one pilot: a few more things we'd like to ask you (please answer by 15 December 2026)**

The new For one now opens on **17 March 2027**, not 23 December. A few things we want to do before then were not in the consent you signed, and each needs a separate yes. Every box is optional. If you don't tick a box, we keep our original promise for that material: everything from the pilot is deleted by 31 December 2026, unless you chose to keep your recordings.

**1. The bridge (only if you pre-paid).** Until the new app opens on 17 March 2027, we'd keep making you episodes by hand, two a week (without calls), the way we did in the pilot, with the same services and the same people as before. It costs you nothing extra: your first paid month still starts on 17 March 2027, and your founding price is locked from then. To do this we need to keep your pilot file (your interests, the facts you told us, what we were working on, your scripts and messages) past 31 December 2026, until the new app opens. If you'd rather not, we refund your pre-payment in full now.

**2. Try the new app before anyone else (`[about 2 to 12 March 2027]`).** We'd like you to set up the new For one on your phone and use it for a few days, so we can test it end to end before the first paying learners arrive on 17 March 2027. It's free. You'd create an account and talk with the producer and the hosts again, as a new learner would. This new account follows the new app's privacy notice ([link]): your data is stored in the European Union (Frankfurt), some AI services process it in the US, recordings are kept only if you choose, and you can delete everything at any time. After the test you can keep your account and continue into the beta, or delete it.

**3. Bring your pilot file into the new app.** `[Only if the build imports pilot files.]` So the show continues where we left off, we'd copy what the show learned about you in the pilot into your new account. This means keeping your pilot file past 31 December 2026 until the copy is made; then the pilot copy is deleted.

**4. Use your pilot material, with your name removed, to test the show's quality.** We'd like to keep copies of your pilot episode scripts, transcripts and the notes about what you were working on, with your name, the names of people you mentioned, and your contact details removed and replaced by a code (like "L07"). We would use them to check that new versions of the show still write natural English and still notice the right mistakes. They would be stored privately, read only by the For one team and one paid English reviewer who has signed a confidentiality agreement, never published, never sold, and never used to train anyone's AI. Kept until `[2027-12-31]`, or until you ask us to remove them, whichever is first. We remove them within 7 days of your request.

**5. The same for your voice clips.** Some of these tests need real voices, because a recording tells us things a transcript can't. We'd like to keep up to `[N]` short clips of your calls under the same rules as box 4. A voice can be recognized even without a name, which is why this is a separate question.

**Your rights stay the same.** Ask for a copy, a correction or deletion at any time with one message on WhatsApp; we act within 7 days. You also have the rights the data protection law where you live gives you.

**Boxes (all optional; please answer by 15 December 2026):**
- (Optional) 1. I pre-paid and want the bridge: keep making me episodes by hand until 17 March 2027, and keep my pilot file until then.
- (Optional) 2. I'd like to try the new app from `[2 to 12 March 2027]`, under its own privacy notice.
- (Optional) 3. Bring what the show learned about me in the pilot into my new account. `[Only if the build imports pilot files.]`
- (Optional) 4. You may keep my pilot scripts, transcripts and notes, with my name removed, to test the show's quality, until `[2027-12-31]`.
- (Optional) 5. You may also keep up to `[N]` short clips of my voice for those tests, under the same rules.

Name: ________  Date: ________

### Arabic (draft for Muath's read)

**تجربة For one: أمور أخرى نطلب موافقتك عليها (نرجو الرد قبل ١٥ ديسمبر ٢٠٢٦)**

سيفتح For one الجديد في **١٧ مارس ٢٠٢٧** وليس في ٢٣ ديسمبر. هناك أمور نريد أن نفعلها قبل ذلك لم تكن في الموافقة التي وقّعتها، وكل منها يحتاج موافقة منفصلة. كل الخانات اختيارية. إذا لم توافق على خانة، نلتزم بوعدنا الأصلي في ما يخصها: نحذف كل بيانات التجربة في موعد أقصاه ٣١ ديسمبر ٢٠٢٦، إلا إذا اخترت أن نحتفظ بتسجيلاتك.

**١. الجسر (فقط إذا دفعت مقدماً).** حتى يفتح التطبيق الجديد في ١٧ مارس ٢٠٢٧، نستمر في صنع حلقاتك يدوياً كما في التجربة، بالخدمات نفسها والأشخاص أنفسهم. لا يكلّفك هذا شيئاً إضافياً: شهرك المدفوع الأول يبدأ في ١٧ مارس ٢٠٢٧، وسعرك كعضو مؤسس يُثبَّت من ذلك اليوم. ولنفعل ذلك نحتاج أن نحتفظ بملفك في التجربة (اهتماماتك، والمعلومات التي أخبرتنا بها، وما كنا نعمل عليه، والنصوص والرسائل) بعد ٣١ ديسمبر ٢٠٢٦ حتى يفتح التطبيق الجديد. إذا كنت لا تريد ذلك، نعيد لك المبلغ الذي دفعته كاملاً الآن.

**٢. جرّب التطبيق الجديد قبل الجميع (`[من ٢ إلى ١٢ مارس ٢٠٢٧ تقريباً]`).** نودّ أن تثبّت For one الجديد على جوالك وتستخدمه بضعة أيام، لنختبره كاملاً قبل وصول أول المشتركين في ١٧ مارس ٢٠٢٧. التجربة مجانية. ستنشئ حساباً وتتحدث مع المنتجة والمقدّمَين من جديد، كأي متعلّم جديد. هذا الحساب الجديد تحكمه سياسة الخصوصية الخاصة بالتطبيق الجديد ([الرابط]): بياناتك تُحفظ في الاتحاد الأوروبي (فرانكفورت)، وبعض خدمات الذكاء الاصطناعي تعالجها في أمريكا، والتسجيلات لا تُحفظ إلا إذا اخترت ذلك، وتستطيع حذف كل شيء في أي وقت. بعد الاختبار تستطيع أن تحتفظ بحسابك وتكمل في النسخة التجريبية المدفوعة، أو تحذفه.

**٣. نقل ملفك من التجربة إلى التطبيق الجديد.** `[فقط إذا كان البناء ينقل ملفات التجربة.]` ليكمل البرنامج من حيث توقفنا، ننسخ ما عرفه البرنامج عنك في التجربة إلى حسابك الجديد. وهذا يعني الاحتفاظ بملفك بعد ٣١ ديسمبر ٢٠٢٦ حتى يتم النسخ، ثم نحذف نسخة التجربة.

**٤. استخدام مواد تجربتك، بعد حذف اسمك، لاختبار جودة البرنامج.** نودّ أن نحتفظ بنسخ من نصوص حلقاتك ونصوص مكالماتك وملاحظات ما كنا نعمل عليه معك، بعد حذف اسمك وأسماء من ذكرتهم وبيانات تواصلك ووضع رمز مكانها (مثل "L07"). نستخدمها لنتأكد أن النسخ الجديدة من البرنامج ما زالت تكتب إنجليزية طبيعية وتلاحظ الأخطاء الصحيحة. تُحفظ في مكان خاص، ولا يقرأها إلا فريق For one ومراجع لغة إنجليزية واحد مدفوع الأجر وقّع اتفاقية سرية، ولا تُنشر ولا تُباع ولا تُستخدم لتدريب أي ذكاء اصطناعي. نحتفظ بها حتى `[٣١ ديسمبر ٢٠٢٧]` أو حتى تطلب حذفها، أيهما أقرب، ونحذفها خلال ٧ أيام من طلبك.

**٥. الأمر نفسه لمقاطع صوتك.** بعض هذه الاختبارات يحتاج أصواتاً حقيقية، لأن التسجيل يخبرنا بأشياء لا يخبرنا بها النص. نودّ أن نحتفظ بما لا يزيد على `[N]` مقاطع قصيرة من مكالماتك بالشروط نفسها في الخانة ٤. الصوت قد يُعرف حتى بدون اسم، ولهذا هو سؤال منفصل.

**حقوقك كما هي.** اطلب نسخة من بياناتك أو تصحيحها أو حذفها في أي وقت برسالة واحدة على الواتساب، ونتصرف خلال ٧ أيام. ولك أيضاً الحقوق التي يعطيك إياها قانون حماية البيانات في البلد الذي تعيش فيه.

**الخانات (كلها اختيارية؛ نرجو الرد قبل ١٥ ديسمبر ٢٠٢٦):**
- ☐ **(اختياري)** ١. دفعت مقدماً وأريد الجسر: استمروا في صنع حلقاتي يدوياً حتى ١٧ مارس ٢٠٢٧، واحتفظوا بملفي في التجربة حتى ذلك الوقت.
- ☐ **(اختياري)** ٢. أودّ تجربة التطبيق الجديد من `[٢ إلى ١٢ مارس ٢٠٢٧]`، وفق سياسة الخصوصية الخاصة به.
- ☐ **(اختياري)** ٣. انقلوا ما عرفه البرنامج عني في التجربة إلى حسابي الجديد. `[فقط إذا كان البناء ينقل ملفات التجربة.]`
- ☐ **(اختياري)** ٤. أوافق على أن تحتفظوا بنصوص حلقاتي ومكالماتي وملاحظاتي من التجربة، بعد حذف اسمي، لاختبار جودة البرنامج حتى `[٣١ ديسمبر ٢٠٢٧]`.
- ☐ **(اختياري)** ٥. وأوافق أيضاً على أن تحتفظوا بما لا يزيد على `[N]` مقاطع قصيرة من صوتي لهذه الاختبارات، بالشروط نفسها.

الاسم: ________  التاريخ: ________
