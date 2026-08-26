import os
import random
import pandas as pd

# ============================================================
# Multilingual Weather Intent Dataset Generator
# ============================================================

OUTPUT_DIR = r"C:\Users\KIIT\Weather\training\data\intent"

random.seed(42)

# ------------------------------------------------------------
# Intent examples
# ------------------------------------------------------------

examples = {

    "weather_current": {
        "en": [
            "What is the weather in {city} today?",
            "How is the weather in {city} right now?",
            "What is the weather like in {city}?",
            "Tell me the current weather in {city}.",
            "How is the weather today in {city}?",
        ],
        "hi": [
            "{city_hi} में आज मौसम कैसा है?",
            "{city_hi} में अभी मौसम कैसा है?",
            "{city_hi} का वर्तमान मौसम बताओ।",
            "आज {city_hi} में मौसम कैसा रहेगा?",
        ],
        "bn": [
            "{city_bn} এ আজ আবহাওয়া কেমন?",
            "{city_bn} এর বর্তমান আবহাওয়া কেমন?",
            "আজ {city_bn} এর আবহাওয়া কেমন?",
            "{city_bn} এর আবহাওয়া আমাকে বলুন।",
        ],
        "or": [
            "{city_or}ରେ ଆଜି ପାଗ କେମିତି ଅଛି?",
            "{city_or}ର ବର୍ତ୍ତମାନ ପାଗ କେମିତି?",
            "ଆଜି {city_or}ର ପାଗ କେମିତି?",
            "{city_or}ର ପାଗ ବିଷୟରେ କୁହନ୍ତୁ।",
        ],
        "mr": [
            "{city_mr} मध्ये आज हवामान कसे आहे?",
            "{city_mr} मधील सध्याचे हवामान कसे आहे?",
            "आज {city_mr} चे हवामान कसे आहे?",
        ],
        "gu": [
            "{city_gu}માં આજે હવામાન કેવું છે?",
            "{city_gu}નું હાલનું હવામાન કેવું છે?",
            "આજે {city_gu}માં હવામાન કેવું છે?",
        ],
        "pa": [
            "{city_pa} ਵਿੱਚ ਅੱਜ ਮੌਸਮ ਕਿਹੋ ਜਿਹਾ ਹੈ?",
            "{city_pa} ਵਿੱਚ ਇਸ ਵੇਲੇ ਮੌਸਮ ਕਿਹੋ ਜਿਹਾ ਹੈ?",
            "ਅੱਜ {city_pa} ਦਾ ਮੌਸਮ ਕਿਹੋ ਜਿਹਾ ਹੈ?",
        ],
        "ta": [
            "{city_ta}வில் இன்று வானிலை எப்படி இருக்கிறது?",
            "{city_ta}வில் தற்போதைய வானிலை எப்படி உள்ளது?",
            "இன்று {city_ta}வில் வானிலை எப்படி இருக்கும்?",
        ],
        "te": [
            "{city_te}లో ఈ రోజు వాతావరణం ఎలా ఉంది?",
            "{city_te}లో ప్రస్తుత వాతావరణం ఎలా ఉంది?",
            "ఈ రోజు {city_te}లో వాతావరణం ఎలా ఉంటుంది?",
        ],
        "kn": [
            "{city_kn}ನಲ್ಲಿ ಇಂದು ಹವಾಮಾನ ಹೇಗಿದೆ?",
            "{city_kn}ನಲ್ಲಿ ಪ್ರಸ್ತುತ ಹವಾಮಾನ ಹೇಗಿದೆ?",
            "ಇಂದು {city_kn}ನಲ್ಲಿ ಹವಾಮಾನ ಹೇಗಿರುತ್ತದೆ?",
        ],
    },

    "weather_forecast": {
        "en": [
            "What will the weather be like in {city} tomorrow?",
            "What is the weather forecast for {city}?",
            "How will the weather be in {city} this weekend?",
            "Give me the weather forecast for {city}.",
            "What weather can I expect in {city} tomorrow?",
        ],
        "hi": [
            "कल {city_hi} में मौसम कैसा रहेगा?",
            "{city_hi} का मौसम पूर्वानुमान बताओ।",
            "इस सप्ताह के अंत में {city_hi} में मौसम कैसा रहेगा?",
        ],
        "bn": [
            "আগামীকাল {city_bn} এর আবহাওয়া কেমন থাকবে?",
            "{city_bn} এর আবহাওয়ার পূর্বাভাস কী?",
            "এই সপ্তাহান্তে {city_bn} এর আবহাওয়া কেমন হবে?",
        ],
        "or": [
            "ଆସନ୍ତାକାଲି {city_or}ରେ ପାଗ କେମିତି ରହିବ?",
            "{city_or}ର ପାଗ ପୂର୍ବାନୁମାନ କଣ?",
            "ଏହି ସପ୍ତାହ ଶେଷରେ {city_or}ର ପାଗ କେମିତି ରହିବ?",
        ],
        "mr": [
            "उद्या {city_mr} मध्ये हवामान कसे असेल?",
            "{city_mr} चे हवामान अंदाज सांगा.",
            "या आठवड्याच्या शेवटी {city_mr} मध्ये हवामान कसे असेल?",
        ],
        "gu": [
            "કાલે {city_gu}માં હવામાન કેવું રહેશે?",
            "{city_gu}નું હવામાન અનુમાન શું છે?",
            "આ સપ્તાહના અંતે {city_gu}માં હવામાન કેવું રહેશે?",
        ],
        "pa": [
            "ਕੱਲ੍ਹ {city_pa} ਵਿੱਚ ਮੌਸਮ ਕਿਹੋ ਜਿਹਾ ਰਹੇਗਾ?",
            "{city_pa} ਦਾ ਮੌਸਮ ਪੂਰਵ ਅਨੁਮਾਨ ਕੀ ਹੈ?",
            "ਇਸ ਹਫ਼ਤੇ ਦੇ ਅੰਤ ਵਿੱਚ {city_pa} ਵਿੱਚ ਮੌਸਮ ਕਿਹੋ ਜਿਹਾ ਰਹੇਗਾ?",
        ],
        "ta": [
            "நாளை {city_ta}வில் வானிலை எப்படி இருக்கும்?",
            "{city_ta} வானிலை முன்னறிவிப்பு என்ன?",
            "இந்த வார இறுதியில் {city_ta}வில் வானிலை எப்படி இருக்கும்?",
        ],
        "te": [
            "రేపు {city_te}లో వాతావరణం ఎలా ఉంటుంది?",
            "{city_te} వాతావరణ సూచన ఏమిటి?",
            "ఈ వారాంతంలో {city_te}లో వాతావరణం ఎలా ఉంటుంది?",
        ],
        "kn": [
            "ನಾಳೆ {city_kn}ನಲ್ಲಿ ಹವಾಮಾನ ಹೇಗಿರುತ್ತದೆ?",
            "{city_kn} ಹವಾಮಾನ ಮುನ್ಸೂಚನೆ ಏನು?",
            "ಈ ವಾರಾಂತ್ಯದಲ್ಲಿ {city_kn}ನಲ್ಲಿ ಹವಾಮಾನ ಹೇಗಿರುತ್ತದೆ?",
        ],
    },

    "temperature": {
        "en": [
            "What is the temperature in {city}?",
            "How hot is it in {city}?",
            "What will the temperature be in {city} tomorrow?",
            "Tell me the temperature in {city}.",
            "How cold is it in {city}?",
        ],
        "hi": [
            "{city_hi} में तापमान कितना है?",
            "{city_hi} में कितनी गर्मी है?",
            "कल {city_hi} में तापमान कितना रहेगा?",
        ],
        "bn": [
            "{city_bn} এর তাপমাত্রা কত?",
            "{city_bn} এ কতটা গরম?",
            "আগামীকাল {city_bn} এর তাপমাত্রা কত থাকবে?",
        ],
        "or": [
            "{city_or}ରେ ତାପମାତ୍ରା କେତେ?",
            "{city_or}ରେ କେତେ ଗରମ ଅଛି?",
            "ଆସନ୍ତାକାଲି {city_or}ର ତାପମାତ୍ରା କେତେ ରହିବ?",
        ],
        "mr": [
            "{city_mr} मध्ये तापमान किती आहे?",
            "{city_mr} मध्ये किती उष्णता आहे?",
            "उद्या {city_mr} मध्ये तापमान किती असेल?",
        ],
        "gu": [
            "{city_gu}માં તાપમાન કેટલું છે?",
            "{city_gu}માં કેટલી ગરમી છે?",
            "કાલે {city_gu}માં તાપમાન કેટલું રહેશે?",
        ],
        "pa": [
            "{city_pa} ਵਿੱਚ ਤਾਪਮਾਨ ਕਿੰਨਾ ਹੈ?",
            "{city_pa} ਵਿੱਚ ਕਿੰਨੀ ਗਰਮੀ ਹੈ?",
            "ਕੱਲ੍ਹ {city_pa} ਵਿੱਚ ਤਾਪਮਾਨ ਕਿੰਨਾ ਰਹੇਗਾ?",
        ],
        "ta": [
            "{city_ta}வில் வெப்பநிலை எவ்வளவு?",
            "{city_ta}வில் எவ்வளவு வெப்பமாக உள்ளது?",
            "நாளை {city_ta}வில் வெப்பநிலை எவ்வளவு இருக்கும்?",
        ],
        "te": [
            "{city_te}లో ఉష్ణోగ్రత ఎంత?",
            "{city_te}లో ఎంత వేడిగా ఉంది?",
            "రేపు {city_te}లో ఉష్ణోగ్రత ఎంత ఉంటుంది?",
        ],
        "kn": [
            "{city_kn}ನಲ್ಲಿ ತಾಪಮಾನ ಎಷ್ಟು?",
            "{city_kn}ನಲ್ಲಿ ಎಷ್ಟು ಬಿಸಿಯಾಗಿದೆ?",
            "ನಾಳೆ {city_kn}ನಲ್ಲಿ ತಾಪಮಾನ ಎಷ್ಟು ಇರುತ್ತದೆ?",
        ],
    },

    "rain": {
        "en": [
            "Will it rain in {city} today?",
            "Is there a chance of rain in {city}?",
            "Will it rain tomorrow in {city}?",
            "Is rain expected in {city}?",
            "What is the chance of rain in {city}?",
        ],
        "hi": [
            "क्या आज {city_hi} में बारिश होगी?",
            "{city_hi} में बारिश की संभावना है?",
            "क्या कल {city_hi} में बारिश होगी?",
        ],
        "bn": [
            "আজ কি {city_bn} এ বৃষ্টি হবে?",
            "{city_bn} এ বৃষ্টির সম্ভাবনা আছে কি?",
            "আগামীকাল কি {city_bn} এ বৃষ্টি হবে?",
        ],
        "or": [
            "ଆଜି {city_or}ରେ ବର୍ଷା ହେବ କି?",
            "{city_or}ରେ ବର୍ଷା ହେବାର ସମ୍ଭାବନା ଅଛି କି?",
            "ଆସନ୍ତାକାଲି {city_or}ରେ ବର୍ଷା ହେବ କି?",
        ],
        "mr": [
            "आज {city_mr} मध्ये पाऊस पडेल का?",
            "{city_mr} मध्ये पावसाची शक्यता आहे का?",
            "उद्या {city_mr} मध्ये पाऊस पडेल का?",
        ],
        "gu": [
            "આજે {city_gu}માં વરસાદ પડશે?",
            "{city_gu}માં વરસાદની શક્યતા છે?",
            "કાલે {city_gu}માં વરસાદ પડશે?",
        ],
        "pa": [
            "ਕੀ ਅੱਜ {city_pa} ਵਿੱਚ ਮੀਂਹ ਪਵੇਗਾ?",
            "{city_pa} ਵਿੱਚ ਮੀਂਹ ਦੀ ਸੰਭਾਵਨਾ ਹੈ?",
            "ਕੀ ਕੱਲ੍ਹ {city_pa} ਵਿੱਚ ਮੀਂਹ ਪਵੇਗਾ?",
        ],
        "ta": [
            "இன்று {city_ta}வில் மழை பெய்யுமா?",
            "{city_ta}வில் மழைக்கு வாய்ப்பு உள்ளதா?",
            "நாளை {city_ta}வில் மழை பெய்யுமா?",
        ],
        "te": [
            "ఈ రోజు {city_te}లో వర్షం పడుతుందా?",
            "{city_te}లో వర్షం పడే అవకాశం ఉందా?",
            "రేపు {city_te}లో వర్షం పడుతుందా?",
        ],
        "kn": [
            "ಇಂದು {city_kn}ನಲ್ಲಿ ಮಳೆ ಬೀಳುತ್ತದೆಯೇ?",
            "{city_kn}ನಲ್ಲಿ ಮಳೆಯ ಸಾಧ್ಯತೆ ಇದೆಯೇ?",
            "ನಾಳೆ {city_kn}ನಲ್ಲಿ ಮಳೆ ಬೀಳುತ್ತದೆಯೇ?",
        ],
    },

    "humidity": {
        "en": [
            "What is the humidity in {city}?",
            "How humid is it in {city}?",
            "What will the humidity be in {city}?",
        ],
        "hi": [
            "{city_hi} में नमी कितनी है?",
            "{city_hi} में आर्द्रता कितनी है?",
            "आज {city_hi} में नमी कितनी रहेगी?",
        ],
        "bn": [
            "{city_bn} এর আর্দ্রতা কত?",
            "{city_bn} এ কতটা আর্দ্র?",
            "আজ {city_bn} এর আর্দ্রতা কত থাকবে?",
        ],
        "or": [
            "{city_or}ରେ ଆର୍ଦ୍ରତା କେତେ?",
            "{city_or}ରେ କେତେ ଆର୍ଦ୍ରତା ଅଛି?",
            "ଆଜି {city_or}ର ଆର୍ଦ୍ରତା କେତେ ରହିବ?",
        ],
        "mr": [
            "{city_mr} मध्ये आर्द्रता किती आहे?",
            "{city_mr} मध्ये किती दमट आहे?",
            "आज {city_mr} मध्ये आर्द्रता किती असेल?",
        ],
        "gu": [
            "{city_gu}માં ભેજ કેટલો છે?",
            "{city_gu}માં કેટલી ભેજ છે?",
            "આજે {city_gu}માં ભેજ કેટલો રહેશે?",
        ],
        "pa": [
            "{city_pa} ਵਿੱਚ ਨਮੀ ਕਿੰਨੀ ਹੈ?",
            "{city_pa} ਵਿੱਚ ਕਿੰਨੀ ਨਮੀ ਹੈ?",
            "ਅੱਜ {city_pa} ਵਿੱਚ ਨਮੀ ਕਿੰਨੀ ਰਹੇਗੀ?",
        ],
        "ta": [
            "{city_ta}வில் ஈரப்பதம் எவ்வளவு?",
            "{city_ta}வில் எவ்வளவு ஈரப்பதமாக உள்ளது?",
            "இன்று {city_ta}வில் ஈரப்பதம் எவ்வளவு இருக்கும்?",
        ],
        "te": [
            "{city_te}లో తేమ ఎంత?",
            "{city_te}లో ఎంత తేమ ఉంది?",
            "ఈ రోజు {city_te}లో తేమ ఎంత ఉంటుంది?",
        ],
        "kn": [
            "{city_kn}ನಲ್ಲಿ ತೇವಾಂಶ ಎಷ್ಟು?",
            "{city_kn}ನಲ್ಲಿ ಎಷ್ಟು ತೇವಾಂಶ ಇದೆ?",
            "ಇಂದು {city_kn}ನಲ್ಲಿ ತೇವಾಂಶ ಎಷ್ಟು ಇರುತ್ತದೆ?",
        ],
    },

    "wind": {
        "en": [
            "How strong is the wind in {city}?",
            "What is the wind speed in {city}?",
            "How windy is it in {city}?",
        ],
        "hi": [
            "{city_hi} में हवा की गति कितनी है?",
            "{city_hi} में हवा कितनी तेज है?",
        ],
        "bn": [
            "{city_bn} এ বাতাসের গতি কত?",
            "{city_bn} এ বাতাস কতটা জোরে বইছে?",
        ],
        "or": [
            "{city_or}ରେ ପବନର ବେଗ କେତେ?",
            "{city_or}ରେ ପବନ କେତେ ଜୋରରେ ବହୁଛି?",
        ],
        "mr": [
            "{city_mr} मध्ये वाऱ्याचा वेग किती आहे?",
            "{city_mr} मध्ये वारा किती जोरात आहे?",
        ],
        "gu": [
            "{city_gu}માં પવનની ઝડપ કેટલી છે?",
            "{city_gu}માં પવન કેટલો ઝડપી છે?",
        ],
        "pa": [
            "{city_pa} ਵਿੱਚ ਹਵਾ ਦੀ ਰਫ਼ਤਾਰ ਕਿੰਨੀ ਹੈ?",
            "{city_pa} ਵਿੱਚ ਹਵਾ ਕਿੰਨੀ ਤੇਜ਼ ਹੈ?",
        ],
        "ta": [
            "{city_ta}வில் காற்றின் வேகம் எவ்வளவு?",
            "{city_ta}வில் காற்று எவ்வளவு வேகமாக வீசுகிறது?",
        ],
        "te": [
            "{city_te}లో గాలి వేగం ఎంత?",
            "{city_te}లో గాలి ఎంత వేగంగా వీస్తోంది?",
        ],
        "kn": [
            "{city_kn}ನಲ್ಲಿ ಗಾಳಿಯ ವೇಗ ಎಷ್ಟು?",
            "{city_kn}ನಲ್ಲಿ ಗಾಳಿ ಎಷ್ಟು ವೇಗವಾಗಿ ಬೀಸುತ್ತಿದೆ?",
        ],
    },

    "air_quality": {
        "en": [
            "What is the air quality in {city}?",
            "How is the air quality in {city}?",
            "What is the AQI in {city}?",
        ],
        "hi": [
            "{city_hi} में हवा की गुणवत्ता कैसी है?",
            "{city_hi} का AQI कितना है?",
        ],
        "bn": [
            "{city_bn} এর বায়ুর মান কেমন?",
            "{city_bn} এর AQI কত?",
        ],
        "or": [
            "{city_or}ରେ ବାୟୁର ଗୁଣବତ୍ତା କେମିତି?",
            "{city_or}ର AQI କେତେ?",
        ],
        "mr": [
            "{city_mr} मध्ये हवेची गुणवत्ता कशी आहे?",
            "{city_mr} चा AQI किती आहे?",
        ],
        "gu": [
            "{city_gu}માં હવાની ગુણવત્તા કેવી છે?",
            "{city_gu}નો AQI કેટલો છે?",
        ],
        "pa": [
            "{city_pa} ਵਿੱਚ ਹਵਾ ਦੀ ਗੁਣਵੱਤਾ ਕਿਹੋ ਜਿਹੀ ਹੈ?",
            "{city_pa} ਦਾ AQI ਕਿੰਨਾ ਹੈ?",
        ],
        "ta": [
            "{city_ta}வில் காற்றின் தரம் எப்படி உள்ளது?",
            "{city_ta}வின் AQI எவ்வளவு?",
        ],
        "te": [
            "{city_te}లో గాలి నాణ్యత ఎలా ఉంది?",
            "{city_te} AQI ఎంత?",
        ],
        "kn": [
            "{city_kn}ನಲ್ಲಿ ಗಾಳಿಯ ಗುಣಮಟ್ಟ ಹೇಗಿದೆ?",
            "{city_kn}ನ AQI ಎಷ್ಟು?",
        ],
    },

    "sunrise_sunset": {
        "en": [
            "What time is sunrise in {city}?",
            "When is sunset in {city}?",
            "What time does the sun rise in {city}?",
        ],
        "hi": [
            "{city_hi} में सूर्योदय कितने बजे होगा?",
            "{city_hi} में सूर्यास्त कितने बजे होगा?",
        ],
        "bn": [
            "{city_bn} এ সূর্যোদয় কখন?",
            "{city_bn} এ সূর্যাস্ত কখন?",
        ],
        "or": [
            "{city_or}ରେ ସୂର୍ଯ୍ୟୋଦୟ କେତେବେଳେ?",
            "{city_or}ରେ ସୂର୍ଯ୍ୟାସ୍ତ କେତେବେଳେ?",
        ],
        "mr": [
            "{city_mr} मध्ये सूर्योदय किती वाजता होतो?",
            "{city_mr} मध्ये सूर्यास्त किती वाजता होतो?",
        ],
        "gu": [
            "{city_gu}માં સૂર્યોદય કેટલા વાગ્યે થાય છે?",
            "{city_gu}માં સૂર્યાસ્ત કેટલા વાગ્યે થાય છે?",
        ],
        "pa": [
            "{city_pa} ਵਿੱਚ ਸੂਰਜ ਕਿੰਨੇ ਵਜੇ ਚੜ੍ਹਦਾ ਹੈ?",
            "{city_pa} ਵਿੱਚ ਸੂਰਜ ਕਿੰਨੇ ਵਜੇ ਡੁੱਬਦਾ ਹੈ?",
        ],
        "ta": [
            "{city_ta}வில் சூரிய உதயம் எப்போது?",
            "{city_ta}வில் சூரிய அஸ்தமனம் எப்போது?",
        ],
        "te": [
            "{city_te}లో సూర్యోదయం ఎప్పుడు?",
            "{city_te}లో సూర్యాస్తమయం ఎప్పుడు?",
        ],
        "kn": [
            "{city_kn}ನಲ್ಲಿ ಸೂರ್ಯೋದಯ ಯಾವಾಗ?",
            "{city_kn}ನಲ್ಲಿ ಸೂರ್ಯಾಸ್ತ ಯಾವಾಗ?",
        ],
    },

    "weather_alert": {
        "en": [
            "Are there any weather alerts for {city}?",
            "Is there a weather warning for {city}?",
            "Are there any severe weather warnings in {city}?",
        ],
        "hi": [
            "{city_hi} के लिए कोई मौसम चेतावनी है?",
            "{city_hi} में मौसम की कोई चेतावनी है?",
        ],
        "bn": [
            "{city_bn} এর জন্য কোনো আবহাওয়া সতর্কতা আছে?",
            "{city_bn} এ কোনো আবহাওয়া সতর্কতা জারি হয়েছে?",
        ],
        "or": [
            "{city_or} ପାଇଁ କୌଣସି ପାଣିପାଗ ସତର୍କତା ଅଛି କି?",
            "{city_or}ରେ କୌଣସି ପାଗ ସତର୍କତା ଅଛି କି?",
        ],
        "mr": [
            "{city_mr} साठी हवामानाची कोणतीही चेतावणी आहे का?",
            "{city_mr} मध्ये हवामानाचा इशारा आहे का?",
        ],
        "gu": [
            "{city_gu} માટે કોઈ હવામાન ચેતવણી છે?",
            "{city_gu}માં હવામાનની કોઈ ચેતવણી છે?",
        ],
        "pa": [
            "{city_pa} ਲਈ ਕੋਈ ਮੌਸਮ ਚੇਤਾਵਨੀ ਹੈ?",
            "{city_pa} ਵਿੱਚ ਮੌਸਮ ਦੀ ਕੋਈ ਚੇਤਾਵਨੀ ਹੈ?",
        ],
        "ta": [
            "{city_ta}க்கு வானிலை எச்சரிக்கை உள்ளதா?",
            "{city_ta}வில் ஏதேனும் வானிலை எச்சரிக்கை உள்ளதா?",
        ],
        "te": [
            "{city_te}కి వాతావరణ హెచ్చరికలు ఏమైనా ఉన్నాయా?",
            "{city_te}లో వాతావరణ హెచ్చరిక ఉందా?",
        ],
        "kn": [
            "{city_kn}ಗೆ ಯಾವುದೇ ಹವಾಮಾನ ಎಚ್ಚರಿಕೆ ಇದೆಯೇ?",
            "{city_kn}ನಲ್ಲಿ ಹವಾಮಾನ ಎಚ್ಚರಿಕೆ ಇದೆಯೇ?",
        ],
    },

    "weather_comparison": {
        "en": [
            "Which city is colder, {city1} or {city2}?",
            "Compare the weather in {city1} and {city2}.",
            "Which is hotter, {city1} or {city2}?",
        ],
        "hi": [
            "{city1_hi} और {city2_hi} में किसका मौसम बेहतर है?",
            "{city1_hi} और {city2_hi} के मौसम की तुलना करो।",
        ],
        "bn": [
            "{city1_bn} এবং {city2_bn} এর আবহাওয়ার তুলনা করুন।",
            "{city1_bn} না {city2_bn}, কোনটি বেশি ঠান্ডা?",
        ],
        "or": [
            "{city1_or} ଏବଂ {city2_or}ର ପାଗ ତୁଳନା କରନ୍ତୁ।",
            "{city1_or} ନା {city2_or}, କେଉଁଠି ଅଧିକ ଥଣ୍ଡା?",
        ],
        "mr": [
            "{city1_mr} आणि {city2_mr} मधील हवामानाची तुलना करा.",
            "{city1_mr} आणि {city2_mr} पैकी कोणते शहर थंड आहे?",
        ],
        "gu": [
            "{city1_gu} અને {city2_gu}ના હવામાનની તુલના કરો.",
            "{city1_gu} અને {city2_gu}માંથી કયું વધુ ઠંડું છે?",
        ],
        "pa": [
            "{city1_pa} ਅਤੇ {city2_pa} ਦੇ ਮੌਸਮ ਦੀ ਤੁਲਨਾ ਕਰੋ।",
            "{city1_pa} ਅਤੇ {city2_pa} ਵਿੱਚੋਂ ਕਿਹੜਾ ਠੰਡਾ ਹੈ?",
        ],
        "ta": [
            "{city1_ta} மற்றும் {city2_ta} வானிலையை ஒப்பிடுங்கள்.",
            "{city1_ta} அல்லது {city2_ta}, எது குளிராக உள்ளது?",
        ],
        "te": [
            "{city1_te} మరియు {city2_te} వాతావరణాన్ని పోల్చండి.",
            "{city1_te} లేదా {city2_te}, ఏది చల్లగా ఉంది?",
        ],
        "kn": [
            "{city1_kn} ಮತ್ತು {city2_kn} ಹವಾಮಾನವನ್ನು ಹೋಲಿಸಿ.",
            "{city1_kn} ಅಥವಾ {city2_kn}, ಯಾವುದು ಹೆಚ್ಚು ತಂಪಾಗಿದೆ?",
        ],
    },
}


# ------------------------------------------------------------
# City names
# ------------------------------------------------------------

cities = [
    {
        "en": "Delhi", "hi": "दिल्ली", "bn": "দিল্লি", "or": "ଦିଲ୍ଲୀ",
        "mr": "दिल्ली", "gu": "દિલ્હી", "pa": "ਦਿੱਲੀ",
        "ta": "டெல்லி", "te": "ఢిల్లీ", "kn": "ದೆಹಲಿ"
    },
    {
        "en": "Mumbai", "hi": "मुंबई", "bn": "মুম্বাই", "or": "ମୁମ୍ବାଇ",
        "mr": "मुंबई", "gu": "મુંબઈ", "pa": "ਮੁੰਬਈ",
        "ta": "மும்பை", "te": "ముంబై", "kn": "ಮುಂಬೈ"
    },
    {
        "en": "Chennai", "hi": "चेन्नई", "bn": "চেন্নাই", "or": "ଚେନ୍ନାଇ",
        "mr": "चेन्नई", "gu": "ચેન્નાઈ", "pa": "ਚੇਨਈ",
        "ta": "சென்னை", "te": "చెన్నై", "kn": "ಚೆನ್ನೈ"
    },
    {
        "en": "Kolkata", "hi": "कोलकाता", "bn": "কলকাতা", "or": "କୋଲକାତା",
        "mr": "कोलकाता", "gu": "કોલકાતા", "pa": "ਕੋਲਕਾਤਾ",
        "ta": "கொல்கத்தா", "te": "కోల్‌కతా", "kn": "ಕೊಲ್ಕತ್ತಾ"
    },
    {
        "en": "Bengaluru", "hi": "बेंगलुरु", "bn": "বেঙ্গালুরু", "or": "ବେଙ୍ଗାଲୁରୁ",
        "mr": "बेंगळुरू", "gu": "બેંગલુરુ", "pa": "ਬੈਂਗਲੁਰੂ",
        "ta": "பெங்களூரு", "te": "బెంగళూరు", "kn": "ಬೆಂಗಳೂರು"
    },
    {
        "en": "Hyderabad", "hi": "हैदराबाद", "bn": "হায়দ্রাবাদ", "or": "ହାଇଦ୍ରାବାଦ",
        "mr": "हैदराबाद", "gu": "હૈદરાબાદ", "pa": "ਹੈਦਰਾਬਾਦ",
        "ta": "ஹைதராபாத்", "te": "హైదరాబాద్", "kn": "ಹೈದರಾಬಾದ್"
    },
    {
        "en": "Pune", "hi": "पुणे", "bn": "পুনে", "or": "ପୁଣେ",
        "mr": "पुणे", "gu": "પુણે", "pa": "ਪੁਣੇ",
        "ta": "புனே", "te": "పుణె", "kn": "ಪುಣೆ"
    },
    {
        "en": "Bhubaneswar", "hi": "भुवनेश्वर", "bn": "ভুবনেশ্বর", "or": "ଭୁବନେଶ୍ୱର",
        "mr": "भुवनेश्वर", "gu": "ભુવનેશ્વર", "pa": "ਭੁਵਨੇਸ਼ਵਰ",
        "ta": "புவனேஸ்வர்", "te": "భువనేశ్వర్", "kn": "ಭುವನೇಶ್ವರ"
    },
]


# ------------------------------------------------------------
# Generate rows
# ------------------------------------------------------------

rows = []

for intent, languages in examples.items():

    for lang, templates in languages.items():

        for city in cities:

            for template in templates:

                if "{city1" in template:
                    city2 = random.choice([c for c in cities if c != city])

                    text = template.format(
                        city1=city["en"],
                        city2=city2["en"],
                        city1_hi=city["hi"],
                        city2_hi=city2["hi"],
                        city1_bn=city["bn"],
                        city2_bn=city2["bn"],
                        city1_or=city["or"],
                        city2_or=city2["or"],
                        city1_mr=city["mr"],
                        city2_mr=city2["mr"],
                        city1_gu=city["gu"],
                        city2_gu=city2["gu"],
                        city1_pa=city["pa"],
                        city2_pa=city2["pa"],
                        city1_ta=city["ta"],
                        city2_ta=city2["ta"],
                        city1_te=city["te"],
                        city2_te=city2["te"],
                        city1_kn=city["kn"],
                        city2_kn=city2["kn"],
                    )

                else:
                    text = template.format(
                        city=city["en"],
                        city_hi=city["hi"],
                        city_bn=city["bn"],
                        city_or=city["or"],
                        city_mr=city["mr"],
                        city_gu=city["gu"],
                        city_pa=city["pa"],
                        city_ta=city["ta"],
                        city_te=city["te"],
                        city_kn=city["kn"],
                    )

                rows.append({
                    "text": text,
                    "label": intent,
                    "language": lang
                })


# ------------------------------------------------------------
# Shuffle
# ------------------------------------------------------------

random.shuffle(rows)

df = pd.DataFrame(rows)

# Remove accidental duplicates
df = df.drop_duplicates(subset=["text"]).reset_index(drop=True)

# ------------------------------------------------------------
# Increase dataset size
# ------------------------------------------------------------

# We want around 5000 examples.
target_size = 5000

if len(df) < target_size:
    extra = df.sample(
        target_size - len(df),
        replace=True,
        random_state=42
    )

    df = pd.concat([df, extra], ignore_index=True)

df = df.sample(frac=1, random_state=42).reset_index(drop=True)

# ------------------------------------------------------------
# Train / validation / test split
# ------------------------------------------------------------

train_size = int(len(df) * 0.80)
val_size = int(len(df) * 0.10)

train_df = df.iloc[:train_size]
val_df = df.iloc[train_size:train_size + val_size]
test_df = df.iloc[train_size + val_size:]

# ------------------------------------------------------------
# Save
# ------------------------------------------------------------

os.makedirs(OUTPUT_DIR, exist_ok=True)

train_df.to_csv(
    os.path.join(OUTPUT_DIR, "train.csv"),
    index=False,
    encoding="utf-8-sig"
)

val_df.to_csv(
    os.path.join(OUTPUT_DIR, "validation.csv"),
    index=False,
    encoding="utf-8-sig"
)

test_df.to_csv(
    os.path.join(OUTPUT_DIR, "test.csv"),
    index=False,
    encoding="utf-8-sig"
)

df.to_csv(
    os.path.join(OUTPUT_DIR, "intent_full.csv"),
    index=False,
    encoding="utf-8-sig"
)

# ------------------------------------------------------------
# Report
# ------------------------------------------------------------

print("\n========================================")
print("INTENT DATASET CREATED")
print("========================================")

print(f"Total examples: {len(df)}")
print(f"Training:       {len(train_df)}")
print(f"Validation:     {len(val_df)}")
print(f"Test:           {len(test_df)}")

print("\nIntent distribution:")
print(df["label"].value_counts())

print("\nLanguage distribution:")
print(df["language"].value_counts())

print("\nFiles saved to:")
print(OUTPUT_DIR)

print("\n========================================")
print("DONE")
print("========================================")