export type LangCode =
  | "en"
  | "hi"
  | "or"
  | "bn"
  | "gu"
  | "mr"
  | "kn"
  | "ta"
  | "te"
  | "pa";

export const LANGUAGES: { code: LangCode; native: string; prompt: string }[] = [
  { code: "en", native: "English", prompt: "Choose your language" },
  { code: "hi", native: "हिन्दी", prompt: "अपनी भाषा चुनें" },
  { code: "or", native: "ଓଡ଼ିଆ", prompt: "ଆପଣଙ୍କ ଭାଷା ବାଛନ୍ତୁ" },
  { code: "bn", native: "বাংলা", prompt: "আপনার ভাষা নির্বাচন করুন" },
  { code: "gu", native: "ગુજરાતી", prompt: "તમારી ભાષા પસંદ કરો" },
  { code: "mr", native: "मराठी", prompt: "तुमची भाषा निवडा" },
  { code: "kn", native: "ಕನ್ನಡ", prompt: "ನಿಮ್ಮ ಭಾಷೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ" },
  { code: "ta", native: "தமிழ்", prompt: "உங்கள் மொழியைத் தேர்ந்தெடுக்கவும்" },
  { code: "te", native: "తెలుగు", prompt: "మీ భాషను ఎంచుకోండి" },
  { code: "pa", native: "ਪੰਜਾਬੀ", prompt: "ਆਪਣੀ ਭਾਸ਼ਾ ਚੁਣੋ" },
];

// English source phrase -> translation. Missing keys fall back to English.
type Dict = Record<string, string>;

const hi: Dict = {
  "Flood Intelligence": "बाढ़ इंटेलिजेंस",
  "Your location": "आपका स्थान",
  "Use current location": "वर्तमान स्थान का उपयोग करें",
  Workspace: "कार्यक्षेत्र",
  "Current weather": "वर्तमान मौसम",
  Forecasts: "पूर्वानुमान",
  "Flood map": "बाढ़ मानचित्र",
  Alerts: "चेतावनियाँ",
  "Climate insights": "जलवायु जानकारी",
  "New question": "नया प्रश्न",
  "Grid-based, causal, built for Odisha": "ग्रिड आधारित, कारण-आधारित, ओडिशा के लिए बनाया गया",
  Today: "आज",
  "Want to know your flood risk before it matters? Ask here.":
    "क्या आप समय रहते अपना बाढ़ जोखिम जानना चाहते हैं? यहाँ पूछें।",
  "Rainfall intensifying after 4 PM": "शाम 4 बजे के बाद वर्षा तेज़ होगी",
  "Updated 6 min ago · grid v3 pipeline": "6 मिनट पहले अपडेट · ग्रिड v3 पाइपलाइन",
  "Bhubaneswar, Odisha": "भुवनेश्वर, ओडिशा",
  "Flood risk isn't just rainfall. It's rainfall, saturated soil, and terrain, reasoned together.":
    "बाढ़ का जोखिम केवल वर्षा नहीं है। यह वर्षा, संतृप्त मिट्टी और भू-भाग का संयुक्त विश्लेषण है।",
  Conversation: "बातचीत",
  "Ask about flood risk, safe travel windows, or advisories for any grid cell in Odisha — I'll reason through the causal chain, not just show you a number.":
    "ओडिशा के किसी भी ग्रिड सेल के लिए बाढ़ जोखिम, सुरक्षित यात्रा समय या सलाह पूछें — मैं केवल संख्या नहीं, कारण-श्रृंखला समझाऊँगा।",
  "Ask MausamAI anything about weather and flood risk…":
    "मौसम और बाढ़ जोखिम के बारे में MausamAI से कुछ भी पूछें…",
  Voice: "आवाज़",
  "SHIFT + ENTER FOR NEW LINE": "नई पंक्ति के लिए SHIFT + ENTER",
  "Grid-level forecasts · causal reasoning · plain-language advisories":
    "ग्रिड स्तर पूर्वानुमान · कारण विश्लेषण · सरल भाषा में सलाह",
  "Active alerts": "सक्रिय चेतावनियाँ",
  "Seasonal trends": "मौसमी रुझान",
  "Prediction layer — model signals": "पूर्वानुमान परत — मॉडल संकेत",
  Rainfall: "वर्षा",
  "Soil saturation": "मिट्टी की संतृप्ति",
  High: "उच्च",
  Moderate: "मध्यम",
  Low: "कम",
};

const or_: Dict = {
  "Flood Intelligence": "ବନ୍ୟା ଇଣ୍ଟେଲିଜେନ୍ସ",
  "Your location": "ଆପଣଙ୍କ ଅବସ୍ଥାନ",
  "Use current location": "ବର୍ତ୍ତମାନ ଅବସ୍ଥାନ ବ୍ୟବହାର କରନ୍ତୁ",
  Workspace: "କାର୍ଯ୍ୟକ୍ଷେତ୍ର",
  "Current weather": "ବର୍ତ୍ତମାନ ପାଣିପାଗ",
  Forecasts: "ପୂର୍ବାନୁମାନ",
  "Flood map": "ବନ୍ୟା ମାନଚିତ୍ର",
  Alerts: "ସତର୍କତା",
  "Climate insights": "ଜଳବାୟୁ ଅନ୍ତର୍ଦୃଷ୍ଟି",
  "New question": "ନୂଆ ପ୍ରଶ୍ନ",
  "Grid-based, causal, built for Odisha": "ଗ୍ରିଡ୍ ଆଧାରିତ, କାରଣମୂଳକ, ଓଡ଼ିଶା ପାଇଁ ନିର୍ମିତ",
  Today: "ଆଜି",
  "Want to know your flood risk before it matters? Ask here.":
    "ବନ୍ୟା ବିପଦ ଆସିବା ପୂର୍ବରୁ ଜାଣିବାକୁ ଚାହୁଁଛନ୍ତି? ଏଠାରେ ପଚାରନ୍ତୁ।",
  "Rainfall intensifying after 4 PM": "ଅପରାହ୍ନ 4ଟା ପରେ ବର୍ଷା ବଢ଼ିବ",
  "Updated 6 min ago · grid v3 pipeline": "6 ମିନିଟ୍ ପୂର୍ବରୁ ଅପଡେଟ୍ · ଗ୍ରିଡ୍ v3 ପାଇପଲାଇନ",
  "Bhubaneswar, Odisha": "ଭୁବନେଶ୍ୱର, ଓଡ଼ିଶା",
  "Flood risk isn't just rainfall. It's rainfall, saturated soil, and terrain, reasoned together.":
    "ବନ୍ୟା ବିପଦ କେବଳ ବର୍ଷା ନୁହେଁ। ଏହା ବର୍ଷା, ସିକ୍ତ ମାଟି ଓ ଭୂମିରୂପର ମିଳିତ ବିଚାର।",
  Conversation: "କଥାବାର୍ତ୍ତା",
  "Ask about flood risk, safe travel windows, or advisories for any grid cell in Odisha — I'll reason through the causal chain, not just show you a number.":
    "ଓଡ଼ିଶାର ଯେକୌଣସି ଗ୍ରିଡ୍ ସେଲ୍ ପାଇଁ ବନ୍ୟା ବିପଦ, ନିରାପଦ ଯାତ୍ରା ସମୟ କିମ୍ବା ପରାମର୍ଶ ପଚାରନ୍ତୁ — ମୁଁ କେବଳ ସଂଖ୍ୟା ନୁହେଁ, କାରଣ ଶୃଙ୍ଖଳା ବୁଝାଇବି।",
  "Ask MausamAI anything about weather and flood risk…":
    "ପାଣିପାଗ ଓ ବନ୍ୟା ବିଷୟରେ MausamAI କୁ ପଚାରନ୍ତୁ…",
  Voice: "ସ୍ୱର",
  "SHIFT + ENTER FOR NEW LINE": "ନୂଆ ଧାଡ଼ି ପାଇଁ SHIFT + ENTER",
  "Grid-level forecasts · causal reasoning · plain-language advisories":
    "ଗ୍ରିଡ୍ ସ୍ତରୀୟ ପୂର୍ବାନୁମାନ · କାରଣ ବିଶ୍ଳେଷଣ · ସରଳ ଭାଷାରେ ପରାମର୍ଶ",
  "Active alerts": "ସକ୍ରିୟ ସତର୍କତା",
  "Seasonal trends": "ଋତୁକାଳୀନ ଧାରା",
  "Prediction layer — model signals": "ପୂର୍ବାନୁମାନ ସ୍ତର — ମଡେଲ ସଙ୍କେତ",
  Rainfall: "ବର୍ଷା",
  "Soil saturation": "ମାଟି ସିକ୍ତତା",
  High: "ଅଧିକ",
  Moderate: "ମଧ୍ୟମ",
  Low: "କମ୍",
};

const bn: Dict = {
  "Flood Intelligence": "বন্যা ইন্টেলিজেন্স",
  "Your location": "আপনার অবস্থান",
  "Use current location": "বর্তমান অবস্থান ব্যবহার করুন",
  Workspace: "কর্মক্ষেত্র",
  "Current weather": "বর্তমান আবহাওয়া",
  Forecasts: "পূর্বাভাস",
  "Flood map": "বন্যা মানচিত্র",
  Alerts: "সতর্কতা",
  "Climate insights": "জলবায়ু অন্তর্দৃষ্টি",
  "New question": "নতুন প্রশ্ন",
  "Grid-based, causal, built for Odisha": "গ্রিড-ভিত্তিক, কারণ-ভিত্তিক, ওড়িশার জন্য তৈরি",
  Today: "আজ",
  "Want to know your flood risk before it matters? Ask here.":
    "সময় থাকতে আপনার বন্যার ঝুঁকি জানতে চান? এখানে জিজ্ঞাসা করুন।",
  "Rainfall intensifying after 4 PM": "বিকেল ৪টার পর বৃষ্টি বাড়বে",
  "Updated 6 min ago · grid v3 pipeline": "৬ মিনিট আগে হালনাগাদ · গ্রিড v3 পাইপলাইন",
  "Bhubaneswar, Odisha": "ভুবনেশ্বর, ওড়িশা",
  "Flood risk isn't just rainfall. It's rainfall, saturated soil, and terrain, reasoned together.":
    "বন্যার ঝুঁকি শুধু বৃষ্টি নয়। এটি বৃষ্টি, সিক্ত মাটি ও ভূ-প্রকৃতির একত্র বিশ্লেষণ।",
  Conversation: "কথোপকথন",
  "Ask about flood risk, safe travel windows, or advisories for any grid cell in Odisha — I'll reason through the causal chain, not just show you a number.":
    "ওড়িশার যেকোনো গ্রিড সেলের বন্যার ঝুঁকি, নিরাপদ ভ্রমণের সময় বা পরামর্শ জিজ্ঞাসা করুন — আমি শুধু সংখ্যা নয়, কার্যকারণ শৃঙ্খল ব্যাখ্যা করব।",
  "Ask MausamAI anything about weather and flood risk…":
    "আবহাওয়া ও বন্যার ঝুঁকি নিয়ে WeatherGPT-কে যেকোনো কিছু জিজ্ঞাসা করুন…",
  Voice: "কণ্ঠস্বর",
  "SHIFT + ENTER FOR NEW LINE": "নতুন লাইনের জন্য SHIFT + ENTER",
  "Grid-level forecasts · causal reasoning · plain-language advisories":
    "গ্রিড-স্তরের পূর্বাভাস · কার্যকারণ বিশ্লেষণ · সহজ ভাষায় পরামর্শ",
  "Active alerts": "সক্রিয় সতর্কতা",
  "Seasonal trends": "ঋতুভিত্তিক প্রবণতা",
  "Prediction layer — model signals": "পূর্বাভাস স্তর — মডেল সংকেত",
  Rainfall: "বৃষ্টিপাত",
  "Soil saturation": "মাটির সিক্ততা",
  High: "উচ্চ",
  Moderate: "মাঝারি",
  Low: "কম",
};

const gu: Dict = {
  "Flood Intelligence": "પૂર ઇન્ટેલિજન્સ",
  "Your location": "તમારું સ્થાન",
  "Use current location": "વર્તમાન સ્થાનનો ઉપયોગ કરો",
  Workspace: "કાર્યક્ષેત્ર",
  "Current weather": "વર્તમાન હવામાન",
  Forecasts: "આગાહી",
  "Flood map": "પૂર નકશો",
  Alerts: "ચેતવણીઓ",
  "Climate insights": "આબોહવા માહિતી",
  "New question": "નવો પ્રશ્ન",
  "Grid-based, causal, built for Odisha": "ગ્રિડ આધારિત, કારણ આધારિત, ઓડિશા માટે બનાવેલ",
  Today: "આજે",
  "Want to know your flood risk before it matters? Ask here.":
    "સમય રહેતાં તમારું પૂરનું જોખમ જાણવું છે? અહીં પૂછો.",
  "Rainfall intensifying after 4 PM": "સાંજે 4 વાગ્યા પછી વરસાદ વધશે",
  "Updated 6 min ago · grid v3 pipeline": "6 મિનિટ પહેલાં અપડેટ · ગ્રિડ v3 પાઇપલાઇન",
  "Bhubaneswar, Odisha": "ભુવનેશ્વર, ઓડિશા",
  "Flood risk isn't just rainfall. It's rainfall, saturated soil, and terrain, reasoned together.":
    "પૂરનું જોખમ માત્ર વરસાદ નથી. તે વરસાદ, ભીની માટી અને ભૂપ્રદેશનું સંયુક્ત વિશ્લેષણ છે.",
  Conversation: "વાતચીત",
  "Ask about flood risk, safe travel windows, or advisories for any grid cell in Odisha — I'll reason through the causal chain, not just show you a number.":
    "ઓડિશાના કોઈપણ ગ્રિડ સેલ માટે પૂરનું જોખમ, સુરક્ષિત મુસાફરીનો સમય કે સલાહ પૂછો — હું માત્ર આંકડો નહીં, કારણ-શૃંખલા સમજાવીશ.",
  "Ask MausamAI anything about weather and flood risk…":
    "હવામાન અને પૂરના જોખમ વિશે MausamAI ને કંઈપણ પૂછો…",
  Voice: "અવાજ",
  "SHIFT + ENTER FOR NEW LINE": "નવી લાઇન માટે SHIFT + ENTER",
  "Grid-level forecasts · causal reasoning · plain-language advisories":
    "ગ્રિડ સ્તરની આગાહી · કારણ વિશ્લેષણ · સરળ ભાષામાં સલાહ",
  "Active alerts": "સક્રિય ચેતવણીઓ",
  "Seasonal trends": "મોસમી વલણો",
  "Prediction layer — model signals": "આગાહી સ્તર — મોડેલ સંકેતો",
  Rainfall: "વરસાદ",
  "Soil saturation": "માટીની ભીનાશ",
  High: "ઊંચું",
  Moderate: "મધ્યમ",
  Low: "ઓછું",
};

const mr: Dict = {
  "Flood Intelligence": "पूर इंटेलिजन्स",
  "Your location": "तुमचे स्थान",
  "Use current location": "सध्याचे स्थान वापरा",
  Workspace: "कार्यक्षेत्र",
  "Current weather": "सध्याचे हवामान",
  Forecasts: "अंदाज",
  "Flood map": "पूर नकाशा",
  Alerts: "सूचना",
  "Climate insights": "हवामान अंतर्दृष्टी",
  "New question": "नवीन प्रश्न",
  "Grid-based, causal, built for Odisha": "ग्रिड आधारित, कारणाधारित, ओडिशासाठी तयार",
  Today: "आज",
  "Want to know your flood risk before it matters? Ask here.":
    "वेळेआधीच तुमचा पुराचा धोका जाणून घ्यायचा आहे? इथे विचारा.",
  "Rainfall intensifying after 4 PM": "दुपारी 4 नंतर पाऊस वाढेल",
  "Updated 6 min ago · grid v3 pipeline": "6 मिनिटांपूर्वी अद्ययावत · ग्रिड v3 पाइपलाइन",
  "Bhubaneswar, Odisha": "भुवनेश्वर, ओडिशा",
  "Flood risk isn't just rainfall. It's rainfall, saturated soil, and terrain, reasoned together.":
    "पुराचा धोका फक्त पाऊस नाही. तो पाऊस, ओलसर माती आणि भूभाग यांचा एकत्रित विचार आहे.",
  Conversation: "संवाद",
  "Ask about flood risk, safe travel windows, or advisories for any grid cell in Odisha — I'll reason through the causal chain, not just show you a number.":
    "ओडिशातील कोणत्याही ग्रिड सेलसाठी पुराचा धोका, सुरक्षित प्रवासाची वेळ किंवा सल्ला विचारा — मी फक्त आकडा नाही, कारणसाखळी समजावून सांगेन.",
  "Ask MausamAI anything about weather and flood risk…":
    "हवामान आणि पुराच्या धोक्याबद्दल MausamAI ला काहीही विचारा…",
  Voice: "आवाज",
  "SHIFT + ENTER FOR NEW LINE": "नवीन ओळीसाठी SHIFT + ENTER",
  "Grid-level forecasts · causal reasoning · plain-language advisories":
    "ग्रिड स्तरावरील अंदाज · कारण विश्लेषण · सोप्या भाषेत सल्ला",
  "Active alerts": "सक्रिय सूचना",
  "Seasonal trends": "हंगामी कल",
  "Prediction layer — model signals": "अंदाज स्तर — मॉडेल संकेत",
  Rainfall: "पाऊस",
  "Soil saturation": "मातीतील ओलावा",
  High: "उच्च",
  Moderate: "मध्यम",
  Low: "कमी",
};

const kn: Dict = {
  "Flood Intelligence": "ಪ್ರವಾಹ ಇಂಟೆಲಿಜೆನ್ಸ್",
  "Your location": "ನಿಮ್ಮ ಸ್ಥಳ",
  "Use current location": "ಪ್ರಸ್ತುತ ಸ್ಥಳವನ್ನು ಬಳಸಿ",
  Workspace: "ಕಾರ್ಯಕ್ಷೇತ್ರ",
  "Current weather": "ಪ್ರಸ್ತುತ ಹವಾಮಾನ",
  Forecasts: "ಮುನ್ಸೂಚನೆಗಳು",
  "Flood map": "ಪ್ರವಾಹ ನಕ್ಷೆ",
  Alerts: "ಎಚ್ಚರಿಕೆಗಳು",
  "Climate insights": "ಹವಾಮಾನ ಒಳನೋಟಗಳು",
  "New question": "ಹೊಸ ಪ್ರಶ್ನೆ",
  "Grid-based, causal, built for Odisha": "ಗ್ರಿಡ್ ಆಧಾರಿತ, ಕಾರಣಾಧಾರಿತ, ಒಡಿಶಾಗಾಗಿ ನಿರ್ಮಿತ",
  Today: "ಇಂದು",
  "Want to know your flood risk before it matters? Ask here.":
    "ಸಮಯಕ್ಕೆ ಮೊದಲೇ ನಿಮ್ಮ ಪ್ರವಾಹ ಅಪಾಯ ತಿಳಿಯಬೇಕೆ? ಇಲ್ಲಿ ಕೇಳಿ.",
  "Rainfall intensifying after 4 PM": "ಸಂಜೆ 4 ರ ನಂತರ ಮಳೆ ಹೆಚ್ಚಾಗಲಿದೆ",
  "Updated 6 min ago · grid v3 pipeline": "6 ನಿಮಿಷಗಳ ಹಿಂದೆ ನವೀಕರಿಸಲಾಗಿದೆ · ಗ್ರಿಡ್ v3 ಪೈಪ್‌ಲೈನ್",
  "Bhubaneswar, Odisha": "ಭುವನೇಶ್ವರ, ಒಡಿಶಾ",
  "Flood risk isn't just rainfall. It's rainfall, saturated soil, and terrain, reasoned together.":
    "ಪ್ರವಾಹ ಅಪಾಯ ಕೇವಲ ಮಳೆ ಅಲ್ಲ. ಅದು ಮಳೆ, ಒದ್ದೆ ಮಣ್ಣು ಮತ್ತು ಭೂಪ್ರದೇಶಗಳ ಒಟ್ಟಿಗೆ ವಿಶ್ಲೇಷಣೆ.",
  Conversation: "ಸಂಭಾಷಣೆ",
  "Ask about flood risk, safe travel windows, or advisories for any grid cell in Odisha — I'll reason through the causal chain, not just show you a number.":
    "ಒಡಿಶಾದ ಯಾವುದೇ ಗ್ರಿಡ್ ಸೆಲ್‌ಗೆ ಪ್ರವಾಹ ಅಪಾಯ, ಸುರಕ್ಷಿತ ಪ್ರಯಾಣ ಸಮಯ ಅಥವಾ ಸಲಹೆ ಕೇಳಿ — ನಾನು ಕೇವಲ ಸಂಖ್ಯೆ ಅಲ್ಲ, ಕಾರಣ ಸರಪಳಿಯನ್ನು ವಿವರಿಸುತ್ತೇನೆ.",
  "Ask MausamAI anything about weather and flood risk…":
    "ಹವಾಮಾನ ಮತ್ತು ಪ್ರವಾಹ ಅಪಾಯದ ಬಗ್ಗೆ MausamAI ಗೆ ಏನಾದರೂ ಕೇಳಿ…",
  Voice: "ಧ್ವನಿ",
  "SHIFT + ENTER FOR NEW LINE": "ಹೊಸ ಸಾಲಿಗೆ SHIFT + ENTER",
  "Grid-level forecasts · causal reasoning · plain-language advisories":
    "ಗ್ರಿಡ್ ಮಟ್ಟದ ಮುನ್ಸೂಚನೆ · ಕಾರಣ ವಿಶ್ಲೇಷಣೆ · ಸರಳ ಭಾಷೆಯ ಸಲಹೆ",
  "Active alerts": "ಸಕ್ರಿಯ ಎಚ್ಚರಿಕೆಗಳು",
  "Seasonal trends": "ಋತುಮಾನದ ಪ್ರವೃತ್ತಿಗಳು",
  "Prediction layer — model signals": "ಮುನ್ಸೂಚನೆ ಪದರ — ಮಾದರಿ ಸಂಕೇತಗಳು",
  Rainfall: "ಮಳೆ",
  "Soil saturation": "ಮಣ್ಣಿನ ತೇವಾಂಶ",
  High: "ಹೆಚ್ಚು",
  Moderate: "ಮಧ್ಯಮ",
  Low: "ಕಡಿಮೆ",
};

const ta: Dict = {
  "Flood Intelligence": "வெள்ள நுண்ணறிவு",
  "Your location": "உங்கள் இருப்பிடம்",
  "Use current location": "தற்போதைய இருப்பிடத்தைப் பயன்படுத்து",
  Workspace: "பணியிடம்",
  "Current weather": "தற்போதைய வானிலை",
  Forecasts: "முன்னறிவிப்புகள்",
  "Flood map": "வெள்ள வரைபடம்",
  Alerts: "எச்சரிக்கைகள்",
  "Climate insights": "காலநிலை நுண்ணறிவு",
  "New question": "புதிய கேள்வி",
  "Grid-based, causal, built for Odisha": "கட்டம் சார்ந்த, காரண அடிப்படையிலான, ஒடிசாவுக்காக உருவாக்கப்பட்டது",
  Today: "இன்று",
  "Want to know your flood risk before it matters? Ask here.":
    "நேரம் கடப்பதற்கு முன் உங்கள் வெள்ள ஆபத்தை அறிய வேண்டுமா? இங்கே கேளுங்கள்.",
  "Rainfall intensifying after 4 PM": "மாலை 4 மணிக்குப் பிறகு மழை அதிகரிக்கும்",
  "Updated 6 min ago · grid v3 pipeline": "6 நிமிடங்களுக்கு முன் புதுப்பிக்கப்பட்டது · கட்டம் v3 பைப்லைன்",
  "Bhubaneswar, Odisha": "புவனேசுவர், ஒடிசா",
  "Flood risk isn't just rainfall. It's rainfall, saturated soil, and terrain, reasoned together.":
    "வெள்ள ஆபத்து வெறும் மழை அல்ல. அது மழை, ஈரமான மண் மற்றும் நிலத்தோற்றம் ஆகியவற்றின் ஒருங்கிணைந்த பகுப்பாய்வு.",
  Conversation: "உரையாடல்",
  "Ask about flood risk, safe travel windows, or advisories for any grid cell in Odisha — I'll reason through the causal chain, not just show you a number.":
    "ஒடிசாவின் எந்தக் கட்டத்திற்கும் வெள்ள ஆபத்து, பாதுகாப்பான பயண நேரம் அல்லது ஆலோசனை கேளுங்கள் — நான் வெறும் எண்ணை அல்ல, காரணத் தொடரை விளக்குவேன்.",
  "Ask MausamAI anything about weather and flood risk…":
    "வானிலை மற்றும் வெள்ள ஆபத்து குறித்து WeatherGPT-யிடம் எதையும் கேளுங்கள்…",
  Voice: "குரல்",
  "SHIFT + ENTER FOR NEW LINE": "புதிய வரிக்கு SHIFT + ENTER",
  "Grid-level forecasts · causal reasoning · plain-language advisories":
    "கட்ட அளவிலான முன்னறிவிப்பு · காரண பகுப்பாய்வு · எளிய மொழி ஆலோசனை",
  "Active alerts": "செயலில் உள்ள எச்சரிக்கைகள்",
  "Seasonal trends": "பருவகால போக்குகள்",
  "Prediction layer — model signals": "முன்னறிவிப்பு அடுக்கு — மாதிரி சமிக்ஞைகள்",
  Rainfall: "மழை",
  "Soil saturation": "மண் ஈரப்பதம்",
  High: "அதிகம்",
  Moderate: "மிதமான",
  Low: "குறைவு",
};

const te: Dict = {
  "Flood Intelligence": "వరద ఇంటెలిజెన్స్",
  "Your location": "మీ ప్రదేశం",
  "Use current location": "ప్రస్తుత ప్రదేశాన్ని ఉపయోగించండి",
  Workspace: "కార్యక్షేత్రం",
  "Current weather": "ప్రస్తుత వాతావరణం",
  Forecasts: "అంచనాలు",
  "Flood map": "వరద పటం",
  Alerts: "హెచ్చరికలు",
  "Climate insights": "వాతావరణ విశ్లేషణలు",
  "New question": "కొత్త ప్రశ్న",
  "Grid-based, causal, built for Odisha": "గ్రిడ్ ఆధారిత, కారణ ఆధారిత, ఒడిశా కోసం నిర్మించబడింది",
  Today: "ఈరోజు",
  "Want to know your flood risk before it matters? Ask here.":
    "సమయం మించకముందే మీ వరద ప్రమాదాన్ని తెలుసుకోవాలా? ఇక్కడ అడగండి.",
  "Rainfall intensifying after 4 PM": "సాయంత్రం 4 తర్వాత వర్షం పెరుగుతుంది",
  "Updated 6 min ago · grid v3 pipeline": "6 నిమిషాల క్రితం నవీకరించబడింది · గ్రిడ్ v3 పైప్‌లైన్",
  "Bhubaneswar, Odisha": "భువనేశ్వర్, ఒడిశా",
  "Flood risk isn't just rainfall. It's rainfall, saturated soil, and terrain, reasoned together.":
    "వరద ప్రమాదం కేవలం వర్షం కాదు. అది వర్షం, తడిసిన నేల మరియు భూస్వరూపాల కలిపిన విశ్లేషణ.",
  Conversation: "సంభాషణ",
  "Ask about flood risk, safe travel windows, or advisories for any grid cell in Odisha — I'll reason through the causal chain, not just show you a number.":
    "ఒడిశాలోని ఏ గ్రిడ్ సెల్‌కైనా వరద ప్రమాదం, సురక్షిత ప్రయాణ సమయం లేదా సలహా అడగండి — నేను కేవలం సంఖ్య కాదు, కారణ గొలుసును వివరిస్తాను.",
  "Ask MausamAI anything about weather and flood risk…":
    "వాతావరణం మరియు వరద ప్రమాదం గురించి MausamAI ని ఏదైనా అడగండి…",
  Voice: "వాయిస్",
  "SHIFT + ENTER FOR NEW LINE": "కొత్త లైన్ కోసం SHIFT + ENTER",
  "Grid-level forecasts · causal reasoning · plain-language advisories":
    "గ్రిడ్ స్థాయి అంచనాలు · కారణ విశ్లేషణ · సరళ భాషలో సలహాలు",
  "Active alerts": "క్రియాశీల హెచ్చరికలు",
  "Seasonal trends": "కాలానుగుణ ధోరణులు",
  "Prediction layer — model signals": "అంచనా పొర — మోడల్ సంకేతాలు",
  Rainfall: "వర్షపాతం",
  "Soil saturation": "నేల తడి",
  High: "అధికం",
  Moderate: "మధ్యస్థం",
  Low: "తక్కువ",
};

const pa: Dict = {
  "Flood Intelligence": "ਹੜ੍ਹ ਇੰਟੈਲੀਜੈਂਸ",
  "Your location": "ਤੁਹਾਡਾ ਟਿਕਾਣਾ",
  "Use current location": "ਮੌਜੂਦਾ ਟਿਕਾਣਾ ਵਰਤੋ",
  Workspace: "ਕਾਰਜ ਖੇਤਰ",
  "Current weather": "ਮੌਜੂਦਾ ਮੌਸਮ",
  Forecasts: "ਪੂਰਵ-ਅਨੁਮਾਨ",
  "Flood map": "ਹੜ੍ਹ ਨਕਸ਼ਾ",
  Alerts: "ਚੇਤਾਵਨੀਆਂ",
  "Climate insights": "ਜਲਵਾਯੂ ਜਾਣਕਾਰੀ",
  "New question": "ਨਵਾਂ ਸਵਾਲ",
  "Grid-based, causal, built for Odisha": "ਗਰਿੱਡ ਆਧਾਰਿਤ, ਕਾਰਨ ਆਧਾਰਿਤ, ਓਡੀਸ਼ਾ ਲਈ ਬਣਾਇਆ",
  Today: "ਅੱਜ",
  "Want to know your flood risk before it matters? Ask here.":
    "ਸਮਾਂ ਰਹਿੰਦੇ ਆਪਣਾ ਹੜ੍ਹ ਦਾ ਖ਼ਤਰਾ ਜਾਣਨਾ ਚਾਹੁੰਦੇ ਹੋ? ਇੱਥੇ ਪੁੱਛੋ।",
  "Rainfall intensifying after 4 PM": "ਸ਼ਾਮ 4 ਵਜੇ ਤੋਂ ਬਾਅਦ ਮੀਂਹ ਤੇਜ਼ ਹੋਵੇਗਾ",
  "Updated 6 min ago · grid v3 pipeline": "6 ਮਿੰਟ ਪਹਿਲਾਂ ਅੱਪਡੇਟ · ਗਰਿੱਡ v3 ਪਾਈਪਲਾਈਨ",
  "Bhubaneswar, Odisha": "ਭੁਵਨੇਸ਼ਵਰ, ਓਡੀਸ਼ਾ",
  "Flood risk isn't just rainfall. It's rainfall, saturated soil, and terrain, reasoned together.":
    "ਹੜ੍ਹ ਦਾ ਖ਼ਤਰਾ ਸਿਰਫ਼ ਮੀਂਹ ਨਹੀਂ ਹੈ। ਇਹ ਮੀਂਹ, ਗਿੱਲੀ ਮਿੱਟੀ ਅਤੇ ਭੂ-ਭਾਗ ਦਾ ਸਾਂਝਾ ਵਿਸ਼ਲੇਸ਼ਣ ਹੈ।",
  Conversation: "ਗੱਲਬਾਤ",
  "Ask about flood risk, safe travel windows, or advisories for any grid cell in Odisha — I'll reason through the causal chain, not just show you a number.":
    "ਓਡੀਸ਼ਾ ਦੇ ਕਿਸੇ ਵੀ ਗਰਿੱਡ ਸੈੱਲ ਲਈ ਹੜ੍ਹ ਦਾ ਖ਼ਤਰਾ, ਸੁਰੱਖਿਅਤ ਸਫ਼ਰ ਦਾ ਸਮਾਂ ਜਾਂ ਸਲਾਹ ਪੁੱਛੋ — ਮੈਂ ਸਿਰਫ਼ ਅੰਕੜਾ ਨਹੀਂ, ਕਾਰਨ-ਲੜੀ ਸਮਝਾਵਾਂਗਾ।",
  "Ask MausamAI anything about weather and flood risk…":
    "ਮੌਸਮ ਅਤੇ ਹੜ੍ਹ ਦੇ ਖ਼ਤਰੇ ਬਾਰੇ MausamAI ਨੂੰ ਕੁਝ ਵੀ ਪੁੱਛੋ…",
  Voice: "ਆਵਾਜ਼",
  "SHIFT + ENTER FOR NEW LINE": "ਨਵੀਂ ਲਾਈਨ ਲਈ SHIFT + ENTER",
  "Grid-level forecasts · causal reasoning · plain-language advisories":
    "ਗਰਿੱਡ ਪੱਧਰੀ ਪੂਰਵ-ਅਨੁਮਾਨ · ਕਾਰਨ ਵਿਸ਼ਲੇਸ਼ਣ · ਸਰਲ ਭਾਸ਼ਾ ਵਿੱਚ ਸਲਾਹ",
  "Active alerts": "ਸਰਗਰਮ ਚੇਤਾਵਨੀਆਂ",
  "Seasonal trends": "ਮੌਸਮੀ ਰੁਝਾਨ",
  "Prediction layer — model signals": "ਪੂਰਵ-ਅਨੁਮਾਨ ਪਰਤ — ਮਾਡਲ ਸੰਕੇਤ",
  Rainfall: "ਮੀਂਹ",
  "Soil saturation": "ਮਿੱਟੀ ਦੀ ਨਮੀ",
  High: "ਉੱਚਾ",
  Moderate: "ਦਰਮਿਆਨਾ",
  Low: "ਘੱਟ",
};

export const DICTS: Record<LangCode, Dict> = {
  en: {},
  hi,
  or: or_,
  bn,
  gu,
  mr,
  kn,
  ta,
  te,
  pa,
};

/** Replace English source phrases in an HTML string with the chosen language. */
export function translateHtml(html: string, lang: LangCode): string {
  const dict = DICTS[lang];
  const keys = Object.keys(dict).sort((a, b) => b.length - a.length);
  let out = html;
  for (const key of keys) {
    out = out.split(key).join(dict[key]);
  }
  return out;
}
