# 🏛️ বাংলাদেশ আইনি সহায়ক | Bangladesh Legal RAG Assistant

একটি উন্নত AI-চালিত আইনি সহায়ক যা বাংলাদেশের আইনজীবীদের জন্য বিশেষভাবে ডিজাইন করা হয়েছে। এটি Retrieval Augmented Generation (RAG) প্রযুক্তি ব্যবহার করে বাংলাদেশের আইনি নথি থেকে নির্ভুল এবং প্রাসঙ্গিক আইনি পরামর্শ প্রদান করে।

**An advanced AI-powered legal assistant specifically designed for lawyers in Bangladesh. It uses Retrieval Augmented Generation (RAG) technology to provide accurate and contextual legal advice from Bangladesh legal documents.**

---

## ✨ বৈশিষ্ট্যসমূহ | Features

### 🎯 মূল বৈশিষ্ট্য | Core Features
- **🤖 AI-চালিত আইনি পরামর্শ**: Google Gemini 2.5 Flash ব্যবহার করে উন্নত আইনি পরামর্শ
- **📚 বাংলা নথি প্রক্রিয়াকরণ**: বাংলাদেশের আইনি PDF নথি থেকে তথ্য সংগ্রহ
- **🔍 স্মার্ট অনুসন্ধান**: FAISS ভেক্টর ডেটাবেস ব্যবহার করে দ্রুত এবং নির্ভুল অনুসন্ধান
- **⚖️ সিনিয়র এডভোকেট স্টাইল**: অভিজ্ঞ আইনজীবীর মতো ধাপে ধাপে পরামর্শ
- **📄 ডকুমেন্ট জেনারেশন**: আইনি নোটিশ, আবেদনপত্র ইত্যাদি তৈরি
- **🏛️ বাংলাদেশি আইনের রেফারেন্স**: সংবিধান, দণ্ডবিধি, এবং অন্যান্য আইনের সুনির্দিষ্ট উল্লেখ

### 💼 আইনজীবীদের জন্য বিশেষ সুবিধা | Special Features for Lawyers
- **📊 মামলা বিশ্লেষণ**: মামলার শক্তি-দুর্বলতা মূল্যায়ন
- **📋 পদক্ষেপ পরিকল্পনা**: শুরু থেকে শেষ পর্যন্ত মামলার গাইডলাইন
- **🔗 আইনি রেফারেন্স**: প্রতিটি পরামর্শে সুনির্দিষ্ট আইনের ধারা উল্লেখ
- **⏰ দ্রুত সমাধান**: তাৎক্ষণিক এবং বিস্তারিত পরামর্শ

---

## 📁 প্রজেক্ট স্ট্রাকচার | Project Structure

```
বাংলাদেশ-আইনি-সহায়ক/
├── 📄 app.py                    # স্ট্রিমলিট ওয়েব অ্যাপ্লিকেশন
├── 🧠 rag_system.py             # মূল RAG সিস্টেম
├── 🔗 gemini_client.py          # Google Gemini API ক্লায়েন্ট
├── 🗄️ vector_database.py        # FAISS ভেক্টর ডেটাবেস
├── 📋 pdf_processor.py          # PDF প্রক্রিয়াকরণ মডিউল
├── ⚙️ config.py                 # কনফিগারেশন সেটিংস
├── 🚀 setup.py                  # সেটআপ স্ক্রিপ্ট
├── 📦 requirements.txt          # পাইথন ডিপেন্ডেন্সি
├── 📂 data/                     # আইনি PDF ফাইলসমূহ
│   ├── বাংলাদেশের_সংবিধান.pdf
│   ├── দণ্ডবিধি_১৮৬০.pdf
│   └── ... (অন্যান্য আইনি নথি)
├── 🗃️ vector_db/               # ভেক্টর ডেটাবেস স্টোরেজ
└── 📊 logs/                     # লগ ফাইলসমূহ
```

---

## 🚀 ইন্সটলেশন | Installation

### পূর্বশর্ত | Prerequisites
- **Python 3.8+** ইন্সটল করা থাকতে হবে
- **Git** ইন্সটল করা থাকতে হবে
- **Google AI Studio API Key** প্রয়োজন ([এখানে পান](https://makersuite.google.com/app/apikey))

### ধাপ ১: প্রজেক্ট ক্লোন করুন | Step 1: Clone the Project
```bash
git clone https://github.com/your-username/bangladesh-legal-assistant.git
cd bangladesh-legal-assistant
```

### ধাপ ২: অটো সেটআপ চালান | Step 2: Run Auto Setup
```bash
python setup.py
```

### অথবা ম্যানুয়াল সেটআপ | Or Manual Setup

#### ভার্চুয়াল এনভায়রনমেন্ট তৈরি করুন:
```bash
python -m venv legal_assistant_env

# Windows এ:
legal_assistant_env\Scripts\activate

# Linux/Mac এ:
source legal_assistant_env/bin/activate
```

#### ডিপেন্ডেন্সি ইন্সটল করুন:
```bash
pip install -r requirements.txt
```

---

## ⚙️ কনফিগারেশন | Configuration

### API Key সেটআপ | API Key Setup

**বিকল্প ১: এনভায়রনমেন্ট ভেরিয়েবল (সুপারিশকৃত)**
```bash
export GOOGLE_API_KEY="your_api_key_here"
```

**বিকল্প ২: config.py ফাইলে সরাসরি**
```python
# config.py ফাইলে
GOOGLE_API_KEY = "your_api_key_here"
```

**বিকল্প ৩: অ্যাপ্লিকেশনে সরাসরি এন্ট্রি**
- অ্যাপ চালানোর পর সাইডবারে API Key দিন

### Google API Key কিভাবে পাবেন | How to Get Google API Key

1. [Google AI Studio](https://makersuite.google.com/app/apikey) এ যান
2. আপনার Google অ্যাকাউন্ট দিয়ে সাইন ইন করুন
3. "Create API Key" বাটনে ক্লিক করুন
4. API Key কপি করুন এবং সংরক্ষণ করুন

---

## 🖥️ ব্যবহারবিধি | Usage

### অ্যাপ্লিকেশন চালান | Run the Application
```bash
streamlit run app.py
```

### প্রাথমিক সেটআপ | Initial Setup
1. **ব্রাউজারে অ্যাপ খুলুন**: `http://localhost:8501`
2. **API Key দিন**: সাইডবারে আপনার Google API Key পেস্ট করুন
3. **সিস্টেম চালু করুন**: "সিস্টেম চালু করুন" বাটনে ক্লিক করুন
4. **অপেক্ষা করুন**: প্রথমবার সিস্টেম PDF প্রক্রিয়া করতে ২-৫ মিনিট সময় নিতে পারে

### ব্যবহারের উদাহরণ | Usage Examples

#### 🤖 আইনি পরামর্শ নিন
```
প্রশ্ন: "একজন তার স্ত্রীর দেয়া মিথ্যা নারী নির্যাতন মামলার সম্মুখীন। আমি একজন এডভোকেট হিসাবে কিভাবে তার মামলা সমাধান করবো?"

উত্তর: সিস্টেম বাংলাদেশের সংবিধান ও আইনের রেফারেন্স সহ ধাপে ধাপে সমাধান প্রদান করবে।
```

#### 📄 আইনি নোটিশ তৈরি করুন
- "ডকুমেন্ট তৈরি" ট্যাবে যান
- প্রয়োজনীয় তথ্য পূরণ করুন
- সিস্টেম স্বয়ংক্রিয়ভাবে আইনি নোটিশ তৈরি করবে

#### 🔍 আইনি নথি খুঁজুন
- "নথি খোঁজ" ট্যাবে যান
- বিষয় অনুযায়ী অনুসন্ধান করুন
- প্রাসঙ্গিক আইনি ধারা এবং তথ্য পান

---

## 📚 উপলব্ধ নথি | Available Documents

সিস্টেমে নিম্নলিখিত বাংলাদেশের আইনি নথি রয়েছে:

- 🏛️ **বাংলাদেশের সংবিধান**
- ⚖️ **মুসলিম পারিবারিক আইন অধ্যাদেশ, ১৯৬১**
- 🏠 **পারিবারিক আদালত অধ্যাদেশ, ১৯৮৫**
- 💰 **তালাক ও খোরপোশ আইন**
- 🏘️ **বাড়ী ভাড়া নিয়ন্ত্রণ আইন, ১৯৯১**
- 📋 **মামলা দায়ের, আদালতের রীতি ও কার্যপদ্ধতি**
- 📄 **লিগ্যাল নোটিশ গাইড**

---

## 🛠️ উন্নত ব্যবহার | Advanced Usage

### নতুন PDF যোগ করুন | Add New PDFs
1. `data/` ফোল্ডারে নতুন বাংলা PDF ফাইল যোগ করুন
2. সাইডবারে "Rebuild Database" অপশন ব্যবহার করুন
3. সিস্টেম নতুন নথি প্রক্রিয়া করবে

### টেস্ট ফাংশন চালান | Run Test Functions
```bash
# সম্পূর্ণ সিস্টেম টেস্ট
python rag_system.py

# PDF প্রক্রিয়াকরণ টেস্ট
python pdf_processor.py

# ভেক্টর ডেটাবেস টেস্ট
python vector_database.py

# Gemini API টেস্ট
python gemini_client.py
```

---

## 🎨 UI বৈশিষ্ট্য | UI Features

### 🌐 বহুভাষিক সাপোর্ট
- পূর্ণ বাংলা ইন্টারফেস
- বাংলা ফন্ট অপটিমাইজেশন
- ইংরেজি সাপোর্ট

### 📱 রেসপন্সিভ ডিজাইন
- মোবাইল-বান্ধব ইন্টারফেস
- ট্যাবলেট সাপোর্ট
- ডেস্কটপ অপটিমাইজেশন

### 🎯 ব্যবহারকারী-বান্ধব
- সহজ নেভিগেশন
- স্পষ্ট নির্দেশনা
- তাৎক্ষণিক ফিডব্যাক

---

## 🔧 ট্রাবলশুটিং | Troubleshooting

### সাধারণ সমস্যা | Common Issues

#### ❌ "API Key Invalid" ত্রুটি
```
সমাধান:
1. API Key আবার চেক করুন
2. https://makersuite.google.com/app/apikey থেকে নতুন key নিন
3. Billing সক্রিয় আছে কিনা চেক করুন
```

#### ❌ PDF প্রক্রিয়াকরণ ব্যর্থ
```
সমাধান:
1. PDF ফাইল corrupted কিনা চেক করুন
2. ফাইলের নাম ইংরেজিতে রাখুন
3. ফাইল সাইজ 50MB এর কম রাখুন
```

#### ❌ "Module not found" ত্রুটি
```
সমাধান:
1. pip install -r requirements.txt চালান
2. Virtual environment activate করুন
3. Python 3.8+ ব্যবহার করুন
```

### লগ চেক করুন | Check Logs
```bash
# লগ ফাইল দেখুন
cat logs/system.log

# রিয়েল-টাইম লগ
tail -f logs/system.log
```

---

## 🤝 অবদান | Contributing

### কিভাবে অবদান রাখবেন | How to Contribute

1. **Fork** করুন এই রিপোজিটরি
2. **নতুন ব্রাঞ্চ** তৈরি করুন (`git checkout -b feature/amazing-feature`)
3. **পরিবর্তন কমিট** করুন (`git commit -m 'Add amazing feature'`)
4. **ব্রাঞ্চ Push** করুন (`git push origin feature/amazing-feature`)
5. **Pull Request** তৈরি করুন

### অবদানের ক্ষেত্র | Areas for Contribution
- 📄 নতুন আইনি নথি যোগ
- 🐛 বাগ ফিক্স
- ✨ নতুন ফিচার
- 🌐 ভাষা সাপোর্ট
- 📖 ডকুমেন্টেশন উন্নতি

---

## 📄 লাইসেন্স | License

এই প্রজেক্ট **MIT License** এর অধীনে লাইসেন্সপ্রাপ্ত। বিস্তারিত জানতে [LICENSE](LICENSE) ফাইল দেখুন।

---

## 👥 সাপোর্ট | Support

### 📞 যোগাযোগ | Contact
- **ইমেইল**: support@bangladesh-legal-assistant.com
- **ওয়েবসাইট**: https://bangladesh-legal-assistant.com
- **গিটহাব ইস্যু**: [Issues](https://github.com/your-username/bangladesh-legal-assistant/issues)

### 📚 ডকুমেন্টেশন | Documentation
- [User Guide](docs/user-guide.md)
- [Developer Guide](docs/developer-guide.md)
- [API Reference](docs/api-reference.md)

---

## 🙏 স্বীকৃতি | Acknowledgments

- **Google AI Studio** - Gemini API প্রদানের জন্য
- **FAISS** - ভেক্টর সার্চ ইঞ্জিনের জন্য
- **Streamlit** - ওয়েব ইন্টারফেসের জন্য
- **বাংলাদেশ সরকার** - আইনি নথি প্রকাশের জন্য

---

## ⚠️ আইনি সতর্কতা | Legal Disclaimer

এই সিস্টেম শুধুমাত্র **তথ্যগত উদ্দেশ্যে** তৈরি। এটি পেশাদার আইনি পরামর্শের বিকল্প নয়। গুরুত্বপূর্ণ আইনি বিষয়ে সর্বদা যোগ্য আইনজীবীর পরামর্শ নিন।

**This system is for informational purposes only and is not a substitute for professional legal advice. Always consult qualified lawyers for important legal matters.**

---

<div align="center">

### 🌟 আমাদের সাথে যুক্ত হন | Join Us

**⭐ Star this repository if you find it helpful!**

**🔄 Share with fellow lawyers and legal professionals**

**🤝 Contribute to make it better**

---

**Made with ❤️ for Bangladesh Legal Community**

</div> 