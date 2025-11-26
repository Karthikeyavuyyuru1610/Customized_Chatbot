// TTS helper (browser Web Speech API) with simple UI bindings
(function(){
    // Expose global toggles
    window.chatVoiceEnabled = false;
    window.chatVoiceLang = 'en-US';

    function updateSettingsFromUI(){
        const cb = document.getElementById('voiceToggle');
        const sel = document.getElementById('voiceLang');
        if(cb) window.chatVoiceEnabled = cb.checked;
        if(sel) window.chatVoiceLang = sel.value || 'en-US';
    }

    document.addEventListener('DOMContentLoaded', function(){
        const cb = document.getElementById('voiceToggle');
        const sel = document.getElementById('voiceLang');
        if(cb){
            cb.addEventListener('change', updateSettingsFromUI);
        }
        if(sel){
            sel.addEventListener('change', updateSettingsFromUI);
        }
        // initialize
        updateSettingsFromUI();
    });

    window.speakTextBrowser = function(text, lang){
        try{
            if(!('speechSynthesis' in window)) return false;
            const synth = window.speechSynthesis;
            synth.cancel();
            const utter = new SpeechSynthesisUtterance(text);
            utter.lang = lang || window.chatVoiceLang || 'en-US';
            utter.rate = 1.0;
            utter.pitch = 1.0;
            utter.volume = 1.0;
            // pick a matching voice if available
            const voices = synth.getVoices();
            if(voices && voices.length){
                const locale = (utter.lang || 'en').split('-')[0];
                const matched = voices.find(v => v.lang && v.lang.toLowerCase().startsWith(locale));
                if(matched) utter.voice = matched;
            }
            synth.speak(utter);
            return true;
        }catch(e){
            console.error('speakTextBrowser error', e);
            return false;
        }
    };

    // Optional server TTS fallback placeholder
    window.speakServerFallback = async function(text, lang){
        try{
            const res = await fetch('/api/speak', {
                method: 'POST',
                headers: {'Content-Type':'application/json'},
                body: JSON.stringify({text, lang})
            });
            if(!res.ok) return false;
            const blob = await res.blob();
            const url = URL.createObjectURL(blob);
            const audio = new Audio(url);
            await audio.play();
            return true;
        }catch(e){
            console.error('speakServerFallback error', e);
            return false;
        }
    };

})();
