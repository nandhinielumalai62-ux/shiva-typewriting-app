const BASIC_DRILL_POOLS = {
  "Junior English Basic": [
    "asdfgf ;lkjhj asdfgf ;lkjhj asdfgf ;lkjhj asdfgf ;lkjhj asdfgf ;lkjhj",
    "ask fad alas asks shad lads flags flask glass jag fag fall hash glad sags galls halls salad jak has jags gaff hall dash flash slash flasks lad sad lash adds gall gash shall lakhs dhalls",
    "awerqfa ;oiupj; awerqfa ;oiupj; awerqfa ;oiupj; awerqfa ;oiupj; awerqfa ;oiupj;",
    "fish kodak ahead larks quail apples reader flukes fiddle dead rails sales agile isles should liquid shower saddle idols jaded sails filed legal folder sledge squall larger grade jails lakes roses rupee squeal fields lulled dislike apple dirks lease equip skill easels dollar poorer require asked forks hedge would grass jokers jailer equals refresh fails usual liked walks peaks orders follow drawls defiles",
    "gftfrf hjyjuj gftfrf hjyjuj gftfrf hjyjuj gftfrf hjyjuj gftfrf hjyjuj",
    "lawyers streaks shipped hillside herewith proposals shekels forward desired loophole jugglers straggles halves figures prepare leathery freehold struggles thought thyself treated youthful although territory freight quarter yodlers further glowbar slippers guileless forfeit pleased goodwill tortuous prepared telegraph laughed bottles whiskers thorough repeated addressed patrols regular equipped liliput etiquette flashlight without waggish laughter lifewall yesterday powerfully typewriter",
    "azsexdcf ;lpokmijn azsexdcf ;lpokmijn azsexdcf ;lpokmijn azsexdcf ;lpokmijn",
    "amazed journal gambols pickling vineyard grizzled except logical jackets failure austrian appeared frequent sieffeld succeed spacing movement joyfully premises daybook lecture western examined accuracy fortress kindled general mutual vocation quantity question executor jingled amulets service produce requires judicious jumbled arrival relative provoked starting cylinder materials swivels fizzed possible somewhat gracious thousand assessment violet regal becoming gracious thousand appearance",
    "abcdefghijklmnopqrstuvwxyz., zyxwvutsrqponmlkjihgfedcba.,",
    "123454 098767 123454 098767 123454 098767 123454 098767",
    "Lost time is never regained. Get up early and do your work. To-day's youth and to-morrow's old. Age is a virtue when wisdom is with it. Measure your word before it goes out of you. Children are innocent and should be guided rightly. Our Land had great sages who knew the eternal truth.",
    "Men live by deeds and not by years. God helps those who help themselves. Honest work always brings its reward. A man without character should not be trusted. Rude language speaks ill of the man who uses it. Never lose courage when faced with difficulties. It is easier to ask questions than to answer them. Pandit Nehru always devoted himself to public affairs. It is essential to use the touch method. The correct degree of touch is an important factor. The touch should be neither too heavy nor too light. High speed is within the capacity of every typist. Astronomy is the oldest science. Young men have a right to be happy. A petty man refuses to admit delay. Man is mortal, but his spirit is immortal. Sivaji fought to keep the real spirit of India alive. Tilak was a great Patriot and also a brilliant scholar. Kindly supply 5 tables (4' x 2') immediately."
  ],
  "Junior Tamil Basic": [
    "யளனக டமத யளனக டமத யளனக டமத யளனக டமத யளனக டமத யளனக",
    "யளனகபக டமதாத யளனகபக டமதாத யளனகபக டமதாத யளனகபக டமதாத",
    "கனம் கனம் மனம் கடன் மடம் கது காய் கபம் மகள் பயன்",
    "தானம் கானம் மாயம் பாடம் மாடம் கடகம் கமகம் வாமம் கள்ளன் தாயம்",
    "கப்பம் பட்டம் தத்தம் பள்ளம் மக்கள் கட்டம் கம்பம் மாதம் தாகம் டப்பாய்",
    "கடமான் தாயகம் கானகம் பாட்டன் மாளயம் பம்பாய் கிட்டம் கர்த்தா கமலான் டாக்டர்",
    "காப்பகம் பட்டாளம் கட்டாயம் பக்கமாய் பக்தனாய் மட்டமாய் காட்டான் பார்த்தூன் காப்பாய் காப்பாளர்"
  ]
};

const FALLBACK_PASSAGE_POOLS = {
  "Junior English Basic": [
    [
      "asdfgf ;lkjhj asdfgf ;lkjhj asdfgf ;lkjhj asdfgf ;lkjhj asdfgf ;lkjhj",
      "ask fad alas asks shad lads flags flask glass jag fag fall hash glad sags galls halls salad jak has jags gaff hall dash flash slash flasks lad sad lash adds gall gash shall lakhs dhalls"
    ],
    [
      "awerqfa ;oiupj; awerqfa ;oiupj; awerqfa ;oiupj; awerqfa ;oiupj; awerqfa ;oiupj;",
      "fish kodak ahead larks quail apples reader flukes fiddle dead rails sales agile isles should liquid shower saddle idols jaded sails filed legal folder sledge squall larger grade jails lakes roses rupee squeal fields lulled dislike apple dirks lease equip skill easels dollar poorer require asked forks hedge would grass jokers jailer equals refresh fails usual liked walks peaks orders follow drawls defiles"
    ],
    [
      "gftfrf hjyjuj gftfrf hjyjuj gftfrf hjyjuj gftfrf hjyjuj gftfrf hjyjuj",
      "lawyers streaks shipped hillside herewith proposals shekels forward desired loophole jugglers straggles halves figures prepare leathery freehold struggles thought thyself treated youthful although territory freight quarter yodlers further glowbar slippers guileless forfeit pleased goodwill tortuous prepared telegraph laughed bottles whiskers thorough repeated addressed patrols regular equipped liliput etiquette flashlight without waggish laughter lifewall yesterday powerfully typewriter"
    ],
    [
      "azsexdcf ;lpokmijn azsexdcf ;lpokmijn azsexdcf ;lpokmijn azsexdcf ;lpokmijn",
      "amazed journal gambols pickling vineyard grizzled except logical jackets failure austrian appeared frequent sieffeld succeed spacing movement joyfully premises daybook lecture western examined accuracy fortress kindled general mutual vocation quantity question executor jingled amulets service produce requires judicious jumbled arrival relative provoked starting cylinder materials swivels fizzed possible somewhat gracious thousand assessment violet regal becoming gracious thousand appearance"
    ],
    [
      "abcdefghijklmnopqrstuvwxyz., zyxwvutsrqponmlkjihgfedcba.,",
      "123454 098767 123454 098767 123454 098767 123454 098767"
    ],
    [
      "Lost time is never regained. Get up early and do your work. To-day's youth and to-morrow's old. Age is a virtue when wisdom is with it. Measure your word before it goes out of you. Children are innocent and should be guided rightly. Our Land had great sages who knew the eternal truth.",
      "Men live by deeds and not by years. God helps those who help themselves. Honest work always brings its reward. A man without character should not be trusted. Rude language speaks ill of the man who uses it. Never lose courage when faced with difficulties. It is easier to ask questions than to answer them. Pandit Nehru always devoted himself to public affairs. It is essential to use the touch method. The correct degree of touch is an important factor. The touch should be neither too heavy nor too light. High speed is within the capacity of every typist. Astronomy is the oldest science. Young men have a right to be happy. A petty man refuses to admit delay. Man is mortal, but his spirit is immortal. Sivaji fought to keep the real spirit of India alive. Tilak was a great Patriot and also a brilliant scholar. Kindly supply 5 tables (4' x 2') immediately."
    ]
  ],
  "Junior English Speed": [
    [
      "The way we travel from our homes to our workplaces shapes the world around us in significant ways. For many years, reliance on private vehicles has been the default choice for millions of people. While this provides comfort and independence, it comes at a cost to our environment and well-being. Rising traffic congestion in cities leads to wasted time and stress, while emissions from cars contribute to the degradation of our air quality.",
      "It is time to rethink our daily habits and consider how small changes in our routine can lead to a cleaner future for everyone. By acknowledging the impact of our individual decisions, we can start a movement toward more sustainable ways of moving through our shared urban spaces. Public transportation systems, when well-managed, offer a highly effective alternative to individual vehicle ownership. Trains, buses, and metro lines provide routes that carry large numbers of passengers, significantly reducing the total volume of traffic on our roads."
    ]
  ],
  "Senior English Speed": [
    [
      "Rural infrastructure plays an important role in the overall development of a country. Villages are the backbone of a nation, and improving rural facilities helps to increase the quality of life of people living in rural areas. Good roads, reliable electricity, clean drinking water, healthcare facilities and communication networks are essential for the progress of villages. Better infrastructure connects rural communities with cities and creates new opportunities for education, employment and economic growth.",
      "Agriculture and rural industries depend greatly on proper infrastructure. Improved transportation facilities help farmers to carry their products to markets quickly and safely. Modern storage facilities and digital services support rural development by reducing losses and increasing income opportunities. Providing better schools, hospitals and skill development centers in villages encourages people to build a better future without leaving their hometowns.",
      "Environmental protection is the responsibility of all citizens. Natural resources such as forests, water, soil and air must be protected for future generations. Rapid development should always be balanced with environmental conservation. Planting trees, reducing pollution, saving water and promoting renewable energy are important steps for protecting nature. A strong economy requires both developed rural areas and growing industries."
    ]
  ],
  "Junior Tamil Basic": [
    [
      "யளனக டமத யளனக டமத யளனக டமத யளனக டமத யளனக டமத யளனக",
      "யளனகபக டமதாத யளனகபக டமதாத யளனகபக டமதாத யளனகபக டமதாத"
    ],
    [
      "கனம் கனம் மனம் கடன் மடம் கது காய் கபம் மகள் பயன்",
      "தானம் கானம் மாயம் பாடம் மாடம் கடகம் கமகம் வாமம் கள்ளன் தாயம்"
    ],
    [
      "கப்பம் பட்டம் தத்தம் பள்ளம் மக்கள் கட்டம் கம்பம் மாதம் தாகம் டப்பாய்",
      "கடமான் தாயகம் கானகம் பாட்டன் மாளயம் பம்பாய் கிட்டம் கர்த்தா கமலான் டாக்டர்"
    ],
    [
      "கடமான் தாயகம் கானகம் பாட்டன் மாளயம் பம்பாய் கிட்டம் கர்த்தா கமலான் டாக்டர்",
      "காப்பகம் பட்டாளம் கட்டாயம் பக்கமாய் பக்தனாய் மட்டமாய் காட்டான் பார்த்தூன் காப்பாய் காப்பாளர்"
    ]
  ],
  "Junior Tamil Speed": [
    [
      "தமிழ் நாட்டில் கைத்தறித் தொழிலுக்கு பெரும் நெருக்கடி ஏற்பட்டுள்ளது, ஏராளமான துணிகள் விற்பனை ஆகாமல் தேங்கிக் கிடக்கின்றன. அது மட்டுமன்றி, கைத்தறி ஆடைகளின் ஏற்றுமதியும் மிகவும் குறைந்துள்ளது. இந்த இரண்டு பிரச்சினைகளுக்கு உடனடியாக கவனம் செலுத்தப்படாவிட்டால் அத்தொழிலின் நிலைமை மேலும் மோசமாகிவிடும். ஏற்கனவே பல கைத்தறிகள் வேலையில்லாமல் இருப்பதாகச் சொல்லப்படுகிறது. விவசாயத்தைப் போலவே ஏராளமான பேருக்கு வேலை வாய்ப்பு அளிக்கின்ற ஒரு தொழில் நசிந்துவிடாமல் பார்த்துக்கொள்ள வேண்டிய பொறுப்பு மத்திய, மாநில அரசுகளுக்கு உண்டு. மாநிலத்திலிருந்து ஏற்றுமதியாகும் கைத்தறி ஆடைகளின் மதிப்பு ஆண்டுதோறும் குறைந்துவிட்டதால் கோடிக்கணக்கான மதிப்புள்ள துணிகள் தேங்கிக் கிடக்கின்றன என்பது கவலை அளிக்கிறது.",
      "இத்தொழிலில் உள்ளவர்கள் விசைத்தறித் துறையில் இருந்தும், மில்கள் துறையில் இருந்தும் கடுமையான போட்டியைச் சமாளிக்க வேண்டியிருக்கிறது. இதனையெல்லாம் கருத்தில் கொண்டுதான் இந்தத் தொழிலின் வளர்ச்சிக்காக சில வகைத் துணிகள் உற்பத்தியைக் கைத்தறிக்கு ஒதுக்குவது என்று சில விசேட நடவடிக்கைகளை மத்திய, மாநில அரசுகள் அவ்வப்போது மேற்கொண்டுள்ளது. அப்படியும் அந்தத் தொழிலுக்கு பிரச்சினைகள் தொடர்ந்து நீடித்துக் கொண்டிருக்கின்றன. எனவே பிரச்சினைகளுக்கு உண்மையான காரணம் என்ன என்பதைக் கண்டறிந்து தகுந்த நடவடிக்கைகளை மேற்கொள்ள வேண்டும். கைத்தறித் துணிகளின் உற்பத்தித் செலவு அதிகரித்துவிட்டது. இப்போதைய நிலைமைக்கு இது முக்கிய ஒரு காரணமாகும். நூல் விலைகள் அசாதாரணமான அளவிற்கு உயர்ந்துவிட்டதால் உற்பத்திச் செலவு அதிகரித்துவிட்டதாக சொல்லப்படுகிறது. இந்த நூல் விலை உயர்வு பற்றி கைத்தறித் துறையிலுள்ளவர்கள் மட்டுமன்றி மாநில அரசினரும் குறை கூறியிருக்கிறார்கள். கைத்தறி ஆடை சம்பந்தமான குறியளவை அடைய வேண்டுமானால் இவற்றின் விலைகள் மற்ற நாட்டுத் துணிகளின் விலைகளுடன் ஒப்பிடும் போது, குறைவாக இல்லாவிட்டாலும் அதிகமாக இருக்கக் கூடாது."
    ]
  ],
  "Senior Tamil Speed": [
    [
      "பொறுமை என்பது மனித வாழ்வில் மிக முக்கியமான ஒரு பண்பு ஆகும். இது ஒரு சிறந்த குணம் என்று போற்றப்படுகிறது. பொறுமை உள்ளவர்கள் எந்த ஒரு செயலையும் நிதானமாக செய்வார்கள். அவசரப்பட மாட்டார்கள். பொறுமை ஒருவரின் மனதை அமைதியாக வைத்திருக்க உதவும். கோபம், பதற்றம் போன்ற எதிர்மறை உணர்வுகளை கட்டுப்படுத்தும் சக்தி பொறுமைக்கு உண்டு. பொறுமை இல்லாதவர்கள் சிறிய விஷயங்களுக்காகவும் சண்டையிடுவார்கள். அவர்கள் தங்கள் முடிவுகளை அவசரமாக எடுப்பார்கள். இதனால் பல தவறுகள் நடக்கும்.",
      "பொறுமை ஒரு மனிதனை சிறப்பான வாழ்க்கைக்கு வழிநடத்தும். வாழ்க்கையில் வெற்றி பெற பொறுமை மிக அவசியம். கடினமான சூழ்நிலைகளில் கூட பொறுமையுடன் செயல்பட வேண்டும். ஒரு மாணவன், கல்வி கற்பதில் பொறுமையுடன் இருக்க வேண்டும். அப்பொழுதுதான் அவன் நன்றாக படித்து தேர்வுகளில் நல்ல மதிப்பெண்கள் பெற முடியும். ஒரு விவசாயி பயிர் வளர்ப்பதில் பொறுமையுடன் இருக்க வேண்டும். விதைத்த உடன் பலன் எதிர்பார்ப்பது சரியல்ல. அறுவடைக்குக் காத்திருக்கும் பொறுமை அவசியமாகும். எந்த ஒரு பெரிய காரியத்தையும் சாதிக்க பொறுமை மிக முக்கியம்.",
      "சமூக உறவுகளில் பொறுமை மிகவும் முக்கியமானது. குடும்ப உறுப்பினர்களிடமும், நண்பர்களிடமும் பொறுமையுடன் பழக வேண்டும். மற்றவர்கள் சொல்லும் கருத்துக்களை பொறுமையுடன் கேட்க வேண்டும். கோபப்படுவது உடனே நல்லதல்ல. பொறுமையுடன் மற்றவர்களின் உணர்வுகளை புரிந்து கொள்ள முயற்சி செய்ய வேண்டும். இது உறவுகளை பலப்படுத்தும். சண்டைகளைத் தவிர்க்கும். எந்த ஒரு பிரச்சனைக்கும் தீர்வு காண பொறுமை உதவும். ஒரு சிக்கலான பிரச்சனையை அணுகும்போது, பொறுமையுடன் அனைத்து அம்சங்களையும் ஆராய வேண்டும்."
    ]
  ]
};

// Fixed 10 minutes (600 seconds) for all Junior, Senior & Basic sessions
const PRACTICE_DURATION_SECONDS = 600;

const ENGLISH_KEYBOARD_ROWS = [
  [
    { code: "Backquote", main: "`", shift: "~", qwerty: "`" },
    { code: "Digit1", main: "1", shift: "!", qwerty: "1" },
    { code: "Digit2", main: "2", shift: "@", qwerty: "2" },
    { code: "Digit3", main: "3", shift: "#", qwerty: "3" },
    { code: "Digit4", main: "4", shift: "$", qwerty: "4" },
    { code: "Digit5", main: "5", shift: "%", qwerty: "5" },
    { code: "Digit6", main: "6", shift: "^", qwerty: "6" },
    { code: "Digit7", main: "7", shift: "&", qwerty: "7" },
    { code: "Digit8", main: "8", shift: "*", qwerty: "8" },
    { code: "Digit9", main: "9", shift: "(", qwerty: "9" },
    { code: "Digit0", main: "0", shift: ")", qwerty: "0" },
    { code: "Minus", main: "-", shift: "_", qwerty: "-" },
    { code: "Equal", main: "=", shift: "+", qwerty: "=" },
    { code: "Backspace", main: "Backspace", wide: true }
  ],
  [
    { code: "Tab", main: "Tab", wide: true },
    { code: "KeyQ", main: "q", shift: "Q", qwerty: "q" },
    { code: "KeyW", main: "w", shift: "W", qwerty: "w" },
    { code: "KeyE", main: "e", shift: "E", qwerty: "e" },
    { code: "KeyR", main: "r", shift: "R", qwerty: "r" },
    { code: "KeyT", main: "t", shift: "T", qwerty: "t" },
    { code: "KeyY", main: "y", shift: "Y", qwerty: "y" },
    { code: "KeyU", main: "u", shift: "U", qwerty: "u" },
    { code: "KeyI", main: "i", shift: "I", qwerty: "i" },
    { code: "KeyO", main: "o", shift: "O", qwerty: "o" },
    { code: "KeyP", main: "p", shift: "P", qwerty: "p" },
    { code: "BracketLeft", main: "[", shift: "{", qwerty: "[" },
    { code: "BracketRight", main: "]", shift: "}", qwerty: "]" },
    { code: "Backslash", main: "\\", shift: "|", qwerty: "\\" }
  ],
  [
    { code: "CapsLock", main: "Caps", wide: true },
    { code: "KeyA", main: "a", shift: "A", qwerty: "a", home: true },
    { code: "KeyS", main: "s", shift: "S", qwerty: "s", home: true },
    { code: "KeyD", main: "d", shift: "D", qwerty: "d", home: true },
    { code: "KeyF", main: "f", shift: "F", qwerty: "f", home: true },
    { code: "KeyG", main: "g", shift: "G", qwerty: "g" },
    { code: "KeyH", main: "h", shift: "H", qwerty: "h" },
    { code: "KeyJ", main: "j", shift: "J", qwerty: "j", home: true },
    { code: "KeyK", main: "k", shift: "K", qwerty: "k", home: true },
    { code: "KeyL", main: "l", shift: "L", qwerty: "l", home: true },
    { code: "Semicolon", main: ";", shift: ":", qwerty: ";", home: true },
    { code: "Quote", main: "'", shift: "\"", qwerty: "'" },
    { code: "Enter", main: "Enter", wide: true }
  ],
  [
    { code: "ShiftLeft", main: "Shift", shiftKey: true },
    { code: "KeyZ", main: "z", shift: "Z", qwerty: "z" },
    { code: "KeyX", main: "x", shift: "X", qwerty: "x" },
    { code: "KeyC", main: "c", shift: "C", qwerty: "c" },
    { code: "KeyV", main: "v", shift: "V", qwerty: "v" },
    { code: "KeyB", main: "b", shift: "B", qwerty: "b" },
    { code: "KeyN", main: "n", shift: "N", qwerty: "n" },
    { code: "KeyM", main: "m", shift: "M", qwerty: "m" },
    { code: "Comma", main: ",", shift: "<", qwerty: "," },
    { code: "Period", main: ".", shift: ">", qwerty: "." },
    { code: "Slash", main: "/", shift: "?", qwerty: "/" },
    { code: "ShiftRight", main: "Shift", shiftKey: true }
  ],
  [
    { code: "Space", main: "Space", space: true }
  ]
];

// Standard Tamil Typewriter (தமிழ் தட்டச்சு / Bamini) keyboard layout
const TAMIL_TYPEWRITER_ROWS = [
  [
    { code: "Backquote", main: "`", shift: "~", qwerty: "`" },
    { code: "Digit1", main: "1", shift: "!", qwerty: "1" },
    { code: "Digit2", main: "2", shift: "@", qwerty: "2" },
    { code: "Digit3", main: "3", shift: "#", qwerty: "3" },
    { code: "Digit4", main: "4", shift: "$", qwerty: "4" },
    { code: "Digit5", main: "5", shift: "%", qwerty: "5" },
    { code: "Digit6", main: "6", shift: "^", qwerty: "6" },
    { code: "Digit7", main: "7", shift: "&", qwerty: "7" },
    { code: "Digit8", main: "8", shift: "*", qwerty: "8" },
    { code: "Digit9", main: "9", shift: "(", qwerty: "9" },
    { code: "Digit0", main: "0", shift: ")", qwerty: "0" },
    { code: "Minus", main: "-", shift: "_", qwerty: "-" },
    { code: "Equal", main: "=", shift: "+", qwerty: "=" },
    { code: "Backspace", main: "Backspace", wide: true }
  ],
  [
    { code: "Tab", main: "Tab", wide: true },
    { code: "KeyQ", main: "ஞ", shift: "ஸ", qwerty: "q" },
    { code: "KeyW", main: "ற", shift: "ஷ", qwerty: "w" },
    { code: "KeyE", main: "ந", shift: "ஜ", qwerty: "e" },
    { code: "KeyR", main: "ச", shift: "ஹ", qwerty: "r" },
    { code: "KeyT", main: "வ", shift: "க்ஷ", qwerty: "t" },
    { code: "KeyY", main: "ல", shift: "ள", qwerty: "y" },
    { code: "KeyU", main: "ர", shift: "ற", qwerty: "u" },
    { code: "KeyI", main: "ை", shift: "ஐ", qwerty: "i" },
    { code: "KeyO", main: "ெ", shift: "ஒ", qwerty: "o" },
    { code: "KeyP", main: "ி", shift: "ீ", qwerty: "p" },
    { code: "BracketLeft", main: "ு", shift: "ூ", qwerty: "[" },
    { code: "BracketRight", main: "ூ", shift: "ௌ", qwerty: "]" },
    { code: "Backslash", main: "\\", shift: "|", qwerty: "\\" }
  ],
  [
    { code: "CapsLock", main: "Caps", wide: true },
    { code: "KeyA", main: "ய", shift: "ஆ", qwerty: "a", home: true },
    { code: "KeyS", main: "ள", shift: "ஸ்ரீ", qwerty: "s", home: true },
    { code: "KeyD", main: "ன", shift: "ண", qwerty: "d", home: true },
    { code: "KeyF", main: "க", shift: "க்", qwerty: "f", home: true },
    { code: "KeyG", main: "ப", shift: "ப்", qwerty: "g" },
    { code: "KeyH", main: "ா", shift: "ஆ", qwerty: "h" },
    { code: "KeyJ", main: "த", shift: "த்", qwerty: "j", home: true },
    { code: "KeyK", main: "ம", shift: "ம்", qwerty: "k", home: true },
    { code: "KeyL", main: "ட", shift: "ட்", qwerty: "l", home: true },
    { code: "Semicolon", main: "்", shift: ":", qwerty: ";", home: true },
    { code: "Quote", main: "'", shift: "\"", qwerty: "'" },
    { code: "Enter", main: "Enter", wide: true }
  ],
  [
    { code: "ShiftLeft", main: "Shift", shiftKey: true },
    { code: "KeyZ", main: "ழ", shift: "ழூ", qwerty: "z" },
    { code: "KeyX", main: "ங", shift: "ஃ", qwerty: "x" },
    { code: "KeyC", main: "ண", shift: "ஒ", qwerty: "c" },
    { code: "KeyV", main: "உ", shift: "ஊ", qwerty: "v" },
    { code: "KeyB", main: "ெ", shift: "எ", qwerty: "b" },
    { code: "KeyN", main: "ே", shift: "ஏ", qwerty: "n" },
    { code: "KeyM", main: "அ", shift: "ஈ", qwerty: "m" },
    { code: "Comma", main: "இ", shift: ",", qwerty: "," },
    { code: "Period", main: "எ", shift: ".", qwerty: "." },
    { code: "Slash", main: "ஏ", shift: "?", qwerty: "/" },
    { code: "ShiftRight", main: "Shift", shiftKey: true }
  ],
  [
    { code: "Space", main: "Space", space: true }
  ]
];

// Tamil99 (தமிழ்99) optional keyboard layout
const TAMIL99_ROWS = [
  ENGLISH_KEYBOARD_ROWS[0],
  [
    { code: "Tab", main: "Tab", wide: true },
    { code: "KeyQ", main: "ஆ", shift: "ஸ", qwerty: "q" },
    { code: "KeyW", main: "ஈ", shift: "ஷ", qwerty: "w" },
    { code: "KeyE", main: "ஊ", shift: "ஜ", qwerty: "e" },
    { code: "KeyR", main: "ஐ", shift: "ஹ", qwerty: "r" },
    { code: "KeyT", main: "ஏ", shift: "க்ஷ", qwerty: "t" },
    { code: "KeyY", main: "ள", shift: "ஸ்ரீ", qwerty: "y" },
    { code: "KeyU", main: "ற", shift: "ற்", qwerty: "u" },
    { code: "KeyI", main: "ன", shift: "ன்", qwerty: "i" },
    { code: "KeyO", main: "ட", shift: "ட்", qwerty: "o" },
    { code: "KeyP", main: "ண", shift: "ண்", qwerty: "p" },
    { code: "BracketLeft", main: "ச", shift: "ச்", qwerty: "[" },
    { code: "BracketRight", main: "ஞ", shift: "ஞ்", qwerty: "]" },
    { code: "Backslash", main: "\\", shift: "|", qwerty: "\\" }
  ],
  [
    { code: "CapsLock", main: "Caps", wide: true },
    { code: "KeyA", main: "அ", shift: "ா", qwerty: "a", home: true },
    { code: "KeyS", main: "இ", shift: "ி", qwerty: "s", home: true },
    { code: "KeyD", main: "உ", shift: "ு", qwerty: "d", home: true },
    { code: "KeyF", main: "்", shift: "ஃ", qwerty: "f", home: true },
    { code: "KeyG", main: "எ", shift: "ெ", qwerty: "g" },
    { code: "KeyH", main: "க", shift: "க்", qwerty: "h" },
    { code: "KeyJ", main: "ப", shift: "ப்", qwerty: "j", home: true },
    { code: "KeyK", main: "ம", shift: "ம்", qwerty: "k", home: true },
    { code: "KeyL", main: "த", shift: "த்", qwerty: "l", home: true },
    { code: "Semicolon", main: "ந", shift: "ந்", qwerty: ";", home: true },
    { code: "Quote", main: "ய", shift: "ய்", qwerty: "'" },
    { code: "Enter", main: "Enter", wide: true }
  ],
  [
    { code: "ShiftLeft", main: "Shift", shiftKey: true },
    { code: "KeyZ", main: "ஔ", shift: "ௌ", qwerty: "z" },
    { code: "KeyX", main: "ஓ", shift: "ோ", qwerty: "x" },
    { code: "KeyC", main: "ஒ", shift: "ொ", qwerty: "c" },
    { code: "KeyV", main: "வ", shift: "வ்", qwerty: "v" },
    { code: "KeyB", main: "ங", shift: "ங்", qwerty: "b" },
    { code: "KeyN", main: "ல", shift: "ல்", qwerty: "n" },
    { code: "KeyM", main: "ர", shift: "ர்", qwerty: "m" },
    { code: "Comma", main: ",", shift: "<", qwerty: "," },
    { code: "Period", main: ".", shift: ">", qwerty: "." },
    { code: "Slash", main: "ழ", shift: "?", qwerty: "/" },
    { code: "ShiftRight", main: "Shift", shiftKey: true }
  ],
  [
    { code: "Space", main: "Space", space: true }
  ]
];

let currentPassage = "";
let currentPracticeNumber = 1;
let availableSessions = [];
let startTime = null;
let timerInterval = null;
let remainingSec = PRACTICE_DURATION_SECONDS;
let sessionFinished = false;
let lastWeakChars = "";

function isTamilCategorySelected() {
  const selectEl = document.getElementById("categorySelect");
  return ((selectEl ? selectEl.value : "") || "").toLowerCase().includes("tamil");
}

function getActiveKeyboardRows() {
  if (!isTamilCategorySelected()) {
    return ENGLISH_KEYBOARD_ROWS;
  }
  const layoutEl = document.getElementById("tamilLayoutSelect");
  return layoutEl && layoutEl.value === "tamil99" ? TAMIL99_ROWS : TAMIL_TYPEWRITER_ROWS;
}

function getAsciiToTamilCharMap() {
  const rows = getActiveKeyboardRows();
  const map = {};
  rows.forEach((row) => {
    row.forEach((k) => {
      if (k.qwerty && k.main) {
        map[k.qwerty.toLowerCase()] = k.main;
        if (k.shift) {
          map[k.qwerty.toUpperCase()] = k.shift;
        }
      }
    });
  });
  return map;
}

function renderOnScreenKeyboard() {
  const container = document.getElementById("virtualKeyboard");
  const badge = document.getElementById("keyboardLangBadge");
  const tamilControls = document.getElementById("tamilControlsGroup");
  if (!container) return;

  const isTamil = isTamilCategorySelected();
  if (badge) {
    badge.innerHTML = isTamil
      ? '<i class="bi bi-keyboard me-1"></i> TAMIL KEYBOARD (தமிழ் விசைப்பலகை)'
      : '<i class="bi bi-keyboard me-1"></i> ENGLISH KEYBOARD (QWERTY)';
    badge.className = isTamil
      ? "badge bg-info text-dark fw-bold px-3 py-2"
      : "badge bg-warning text-dark fw-bold px-3 py-2";
  }
  if (tamilControls) {
    tamilControls.classList.toggle("d-none", !isTamil);
  }

  const rows = getActiveKeyboardRows();
  container.innerHTML = "";

  rows.forEach((row) => {
    const rowDiv = document.createElement("div");
    rowDiv.className = "kb-row";
    row.forEach((keyDef) => {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "kb-key";
      btn.dataset.code = keyDef.code;
      if (keyDef.main) btn.dataset.main = keyDef.main;
      if (keyDef.shift) btn.dataset.shift = keyDef.shift;
      if (keyDef.qwerty) btn.dataset.qwerty = keyDef.qwerty;

      if (keyDef.wide) btn.classList.add("kb-key-wide");
      if (keyDef.shiftKey) btn.classList.add("kb-key-shift");
      if (keyDef.space) btn.classList.add("kb-key-space");
      if (keyDef.home) btn.classList.add("key-home");

      const mainSpan = document.createElement("span");
      mainSpan.className = "kb-key-main";
      mainSpan.textContent = keyDef.main;
      btn.appendChild(mainSpan);

      if (isTamil && keyDef.qwerty) {
        const subSpan = document.createElement("span");
        subSpan.className = "kb-key-sub";
        subSpan.textContent = keyDef.shift
          ? `${keyDef.qwerty.toUpperCase()} / ${keyDef.shift}`
          : keyDef.qwerty.toUpperCase();
        btn.appendChild(subSpan);
      } else if (!isTamil && keyDef.shift && keyDef.shift.length === 1 && keyDef.shift !== keyDef.main.toUpperCase()) {
        const subSpan = document.createElement("span");
        subSpan.className = "kb-key-sub";
        subSpan.textContent = keyDef.shift;
        btn.appendChild(subSpan);
      }

      btn.addEventListener("click", () => handleVirtualKeyClick(keyDef));
      rowDiv.appendChild(btn);
    });
    container.appendChild(rowDiv);
  });

  highlightNextExpectedKey();
}

function handleVirtualKeyClick(keyDef) {
  const inputEl = document.getElementById("typingInput");
  if (!inputEl || inputEl.disabled) return;
  inputEl.focus();

  if (keyDef.code === "Backspace") {
    inputEl.value = inputEl.value.slice(0, -1);
  } else if (keyDef.code === "Enter") {
    inputEl.value += "\n";
  } else if (keyDef.code === "Space") {
    inputEl.value += " ";
  } else if (keyDef.code === "Tab" || keyDef.code === "CapsLock" || keyDef.shiftKey) {
    return;
  } else if (keyDef.main) {
    inputEl.value += keyDef.main;
  }
  updateStats();
}

function highlightNextExpectedKey() {
  const container = document.getElementById("virtualKeyboard");
  const inputEl = document.getElementById("typingInput");
  if (!container) return;

  container.querySelectorAll(".kb-key.key-next").forEach((el) => el.classList.remove("key-next"));
  if (!currentPassage) return;

  const typedLen = inputEl ? inputEl.value.length : 0;
  const nextChar = currentPassage[typedLen];
  if (!nextChar) return;

  if (nextChar === " ") {
    container.querySelector('[data-code="Space"]')?.classList.add("key-next");
    return;
  }
  if (nextChar === "\n") {
    container.querySelector('[data-code="Enter"]')?.classList.add("key-next");
    return;
  }

  let needsShift = false;
  const keys = container.querySelectorAll(".kb-key");
  for (const el of keys) {
    if (el.dataset.main === nextChar) {
      el.classList.add("key-next");
      break;
    }
    if (el.dataset.shift === nextChar) {
      el.classList.add("key-next");
      needsShift = true;
      break;
    }
  }

  if (needsShift) {
    container.querySelector('[data-code="ShiftLeft"]')?.classList.add("key-next");
    container.querySelector('[data-code="ShiftRight"]')?.classList.add("key-next");
  }
}

function toggleKeyboardVisibility(btn) {
  const vk = document.getElementById("virtualKeyboard");
  if (!vk) return;
  const hidden = vk.classList.toggle("d-none");
  if (btn) btn.textContent = hidden ? "Show Keyboard" : "Hide Keyboard";
}

function flashPressedKey(code) {
  const container = document.getElementById("virtualKeyboard");
  if (!container || !code) return;
  const btn = container.querySelector(`[data-code="${code}"]`);
  if (!btn) return;
  btn.classList.add("key-pressed");
  setTimeout(() => btn.classList.remove("key-pressed"), 140);
}

function formatClock(sec) {
  const safe = Math.max(0, sec);
  const mm = String(Math.floor(safe / 60)).padStart(2, "0");
  const ss = String(safe % 60).padStart(2, "0");
  return `${mm}:${ss}`;
}

function getRequiredParagraphCount(category) {
  return (category || "").toLowerCase().includes("senior") ? 3 : 2;
}

function segmentGraphemes(text) {
  if (typeof Intl !== "undefined" && Intl.Segmenter) {
    const segmenter = new Intl.Segmenter("ta", { granularity: "grapheme" });
    return Array.from(segmenter.segment(text), (s) => s.segment);
  }
  return Array.from(text);
}

function renderSampleWithHighlights(sampleEl, passage, typed) {
  if (!sampleEl) return;
  if (!typed) {
    sampleEl.textContent = passage;
    return;
  }

  const passageUnits = segmentGraphemes(passage);
  const typedUnits = segmentGraphemes(typed);
  const frag = document.createDocumentFragment();

  for (let i = 0; i < passageUnits.length; i++) {
    const ch = passageUnits[i];
    if (i < typedUnits.length) {
      const span = document.createElement("span");
      span.textContent = ch;
      span.className = typedUnits[i] === ch ? "char-correct" : "char-wrong";
      frag.appendChild(span);
    } else if (i === typedUnits.length) {
      const span = document.createElement("span");
      span.textContent = ch;
      span.className = "char-current";
      frag.appendChild(span);
    } else {
      frag.appendChild(document.createTextNode(ch));
    }
  }
  sampleEl.innerHTML = "";
  sampleEl.appendChild(frag);
}

function populatePracticeSelector(sessions, preferredPracticeNumber) {
  const practiceSelect = document.getElementById("practiceSelect");
  if (!practiceSelect) return;

  practiceSelect.innerHTML = "";
  sessions.forEach((sess) => {
    const opt = document.createElement("option");
    opt.value = String(sess.practice_number);
    opt.textContent = sess.title || `Practice ${sess.practice_number}`;
    practiceSelect.appendChild(opt);
  });

  const targetVal = String(preferredPracticeNumber || "1");
  const exists = Array.from(practiceSelect.options).some((o) => o.value === targetVal);
  practiceSelect.value = exists ? targetVal : (practiceSelect.options[0]?.value || "1");
}

function buildFallbackSessionsForCategory(category) {
  const pools = FALLBACK_PASSAGE_POOLS[category] || FALLBACK_PASSAGE_POOLS["Junior Tamil Speed"];
  return pools.map((pair, idx) => ({
    practice_number: idx + 1,
    title: `Practice ${idx + 1}`,
    content_type: category.toLowerCase().includes("basic") ? "word" : "paragraph",
    paragraphs: pair.slice(0, getRequiredParagraphCount(category)),
    passage_text: pair.slice(0, getRequiredParagraphCount(category)).join("\n\n"),
    target_wpm: category.toLowerCase().includes("senior") ? 40 : 30,
    target_strokes: category.toLowerCase().includes("senior") ? 1750 : 1200
  }));
}

async function loadCategoryLessons(preferredPractice) {
  const selectEl = document.getElementById("categorySelect");
  const modeEl = document.getElementById("modeSelect");
  const category = selectEl ? selectEl.value : "Junior Tamil Basic";
  const mode = modeEl ? modeEl.value : "all";

  let sessions = [];
  try {
    const query = `/api/practice-passages?category=${encodeURIComponent(category)}${
      mode !== "all" ? `&type=${encodeURIComponent(mode)}` : ""
    }`;
    const resp = await fetch(query);
    if (resp.ok) {
      const data = await resp.json();
      if (Array.isArray(data.sessions) && data.sessions.length > 0) {
        sessions = data.sessions;
      }
    }
  } catch (e) {
    // Fallback below if offline
  }

  if (sessions.length === 0) {
    sessions = buildFallbackSessionsForCategory(category);
  }

  availableSessions = sessions;
  populatePracticeSelector(availableSessions, preferredPractice || "1");
  applySelectedPractice();
}

function applySelectedPractice() {
  const practiceSelect = document.getElementById("practiceSelect");
  const selectEl = document.getElementById("categorySelect");
  const sampleEl = document.getElementById("sampleText");
  const inputEl = document.getElementById("typingInput");
  const titleEl = document.getElementById("activePracticeTitle");

  const category = selectEl ? selectEl.value : "Junior Tamil Basic";
  const chosenNum = parseInt(practiceSelect ? practiceSelect.value : "1", 10) || 1;
  currentPracticeNumber = chosenNum;

  let chosen = availableSessions.find((s) => Number(s.practice_number) === chosenNum);
  if (!chosen && availableSessions.length > 0) {
    chosen = availableSessions[0];
    currentPracticeNumber = Number(chosen.practice_number) || 1;
  }

  if (chosen) {
    const requiredCount = getRequiredParagraphCount(category);
    const paras = Array.isArray(chosen.paragraphs) && chosen.paragraphs.length > 0
      ? chosen.paragraphs.slice(0, requiredCount)
      : [chosen.passage_text || ""];
    currentPassage = paras.join("\n\n");
    if (titleEl) {
      titleEl.textContent = `${category} — ${chosen.title || `Practice ${currentPracticeNumber}`}`;
    }
  } else {
    currentPassage = "";
  }

  if (sampleEl) {
    sampleEl.textContent = currentPassage;
  }
  if (inputEl) {
    inputEl.value = "";
    inputEl.disabled = false;
  }

  resetStats();
  renderOnScreenKeyboard();
}

function resetStats() {
  clearInterval(timerInterval);
  timerInterval = null;
  startTime = null;
  remainingSec = PRACTICE_DURATION_SECONDS;
  sessionFinished = false;
  lastWeakChars = "";

  const timerEl = document.getElementById("timerDisplay");
  const wpmEl = document.getElementById("wpmDisplay");
  const accEl = document.getElementById("accDisplay");
  const errEl = document.getElementById("errDisplay");
  const strokesEl = document.getElementById("strokesDisplay");
  const progBar = document.getElementById("progressBar");
  const progText = document.getElementById("progressText");
  const weakText = document.getElementById("weakCharsText");
  const saveStatus = document.getElementById("saveStatusText");
  const sampleEl = document.getElementById("sampleText");

  if (timerEl) {
    timerEl.textContent = formatClock(PRACTICE_DURATION_SECONDS);
    timerEl.classList.remove("timer-urgent");
  }
  if (wpmEl) wpmEl.textContent = "0";
  if (accEl) accEl.textContent = "100%";
  if (errEl) errEl.textContent = "0";
  if (strokesEl) strokesEl.textContent = "0";
  if (progBar) progBar.style.width = "0%";
  if (progText) progText.textContent = "0%";
  if (weakText) weakText.textContent = "No mistyped characters yet.";
  if (saveStatus) saveStatus.textContent = "10:00 countdown starts automatically when you type the first key.";
  if (sampleEl && currentPassage) sampleEl.textContent = currentPassage;
}

function updateStats() {
  if (sessionFinished) return;
  const inputEl = document.getElementById("typingInput");
  const sampleEl = document.getElementById("sampleText");
  if (!inputEl) return;

  const typed = inputEl.value;
  if (!startTime && typed.length > 0) {
    startTime = Date.now();
    timerInterval = setInterval(tickCountdown, 500);
  }

  const elapsedSec = startTime
    ? Math.min(PRACTICE_DURATION_SECONDS, Math.floor((Date.now() - startTime) / 1000))
    : 0;
  remainingSec = Math.max(0, PRACTICE_DURATION_SECONDS - elapsedSec);

  const timerEl = document.getElementById("timerDisplay");
  if (timerEl) {
    timerEl.textContent = formatClock(remainingSec);
    if (remainingSec <= 60 && startTime) {
      timerEl.classList.add("timer-urgent");
    } else {
      timerEl.classList.remove("timer-urgent");
    }
  }

  renderSampleWithHighlights(sampleEl, currentPassage, typed);

  const passageUnits = segmentGraphemes(currentPassage);
  const typedUnits = segmentGraphemes(typed);

  let errors = 0;
  const missedFreq = {};
  for (let i = 0; i < typedUnits.length; i++) {
    if (typedUnits[i] !== passageUnits[i]) {
      errors++;
      const expected = passageUnits[i];
      if (expected && expected.trim()) {
        missedFreq[expected] = (missedFreq[expected] || 0) + 1;
      }
    }
  }

  const sortedMissed = Object.entries(missedFreq)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 6)
    .map(([ch, cnt]) => `'${ch}' (${cnt})`);
  lastWeakChars = sortedMissed.join(", ");

  const weakText = document.getElementById("weakCharsText");
  if (weakText) {
    weakText.textContent = lastWeakChars
      ? `Focus keys: ${lastWeakChars}`
      : "Clean typing so far — no mistyped characters.";
  }

  const pct = currentPassage.length > 0
    ? Math.min(100, Math.round((typed.length / currentPassage.length) * 100))
    : 0;
  const progBar = document.getElementById("progressBar");
  const progText = document.getElementById("progressText");
  if (progBar) progBar.style.width = `${pct}%`;
  if (progText) progText.textContent = `${pct}%`;

  const correctChars = Math.max(0, typedUnits.length - errors);
  const accuracy = typedUnits.length > 0 ? Math.round((correctChars / typedUnits.length) * 100) : 100;
  const minutes = elapsedSec > 0 ? elapsedSec / 60 : 1 / 60;
  const wpm = Math.round((correctChars / 5) / minutes);

  const wpmEl = document.getElementById("wpmDisplay");
  const accEl = document.getElementById("accDisplay");
  const errEl = document.getElementById("errDisplay");
  const strokesEl = document.getElementById("strokesDisplay");
  if (wpmEl) wpmEl.textContent = String(wpm);
  if (accEl) accEl.textContent = `${accuracy}%`;
  if (errEl) errEl.textContent = String(errors);
  if (strokesEl) strokesEl.textContent = String(typed.length);
  highlightNextExpectedKey();
}

function tickCountdown() {
  updateStats();
  if (remainingSec <= 0 && !sessionFinished) {
    finishSession(true);
  }
}

async function finishSession(autoExpired = false) {
  if (sessionFinished) return;
  sessionFinished = true;

  const inputEl = document.getElementById("typingInput");
  const selectEl = document.getElementById("categorySelect");
  const modeEl = document.getElementById("modeSelect");
  const saveStatus = document.getElementById("saveStatusText");

  clearInterval(timerInterval);
  timerInterval = null;
  if (inputEl && autoExpired) {
    inputEl.disabled = true;
  }

  const elapsedSec = startTime
    ? Math.min(PRACTICE_DURATION_SECONDS, Math.floor((Date.now() - startTime) / 1000))
    : 0;
  const wpm = parseInt(document.getElementById("wpmDisplay")?.textContent || "0", 10);
  const accText = document.getElementById("accDisplay")?.textContent || "100%";
  const accuracyPct = parseInt(accText.replace("%", ""), 10) || 100;
  const errors = parseInt(document.getElementById("errDisplay")?.textContent || "0", 10);
  const strokes = inputEl ? inputEl.value.length : 0;
  const category = selectEl ? selectEl.value : "Junior Tamil Basic";
  const contentType = modeEl && modeEl.value !== "all"
    ? modeEl.value
    : (category.toLowerCase().includes("basic") ? "word" : "paragraph");

  let targetMsg = "";
  try {
    const resp = await fetch("/api/practice-sessions", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        category,
        practice_number: currentPracticeNumber,
        content_type: contentType,
        duration_sec: elapsedSec,
        strokes,
        wpm,
        accuracy_pct: accuracyPct,
        errors,
        weak_chars: lastWeakChars
      })
    });
    if (resp.ok) {
      const resData = await resp.json();
      targetMsg = resData.target_met
        ? `Target Met (${resData.target_wpm} WPM benchmark) & saved!`
        : `Saved! Target benchmark: ${resData.target_wpm} WPM / ${resData.target_strokes} strokes.`;
      if (saveStatus) saveStatus.textContent = targetMsg;
    }
  } catch (e) {
    if (saveStatus) saveStatus.textContent = "Saved locally for this session.";
  }

  const headerMsg = autoExpired
    ? "10-Minute Practice Time Up! Session Auto-Submitted."
    : `Practice ${currentPracticeNumber} Session Complete!`;

  alert(
    `${headerMsg}\n` +
    `Category: ${category} (Practice ${currentPracticeNumber})\n` +
    `Time Used: ${formatClock(elapsedSec)} / 10:00\n` +
    `Strokes Typed: ${strokes}\n` +
    `Speed: ${wpm} WPM\n` +
    `Accuracy: ${accuracyPct}%\n` +
    `Errors: ${errors}` +
    (targetMsg ? `\n${targetMsg}` : "")
  );
}

function nextPracticeSession() {
  const practiceSelect = document.getElementById("practiceSelect");
  if (!practiceSelect || practiceSelect.options.length === 0) return;
  const nextIdx = (practiceSelect.selectedIndex + 1) % practiceSelect.options.length;
  practiceSelect.selectedIndex = nextIdx;
  applySelectedPractice();
}

document.addEventListener("DOMContentLoaded", () => {
  const inputEl = document.getElementById("typingInput");
  const categorySelect = document.getElementById("categorySelect");
  const modeSelect = document.getElementById("modeSelect");
  const practiceSelect = document.getElementById("practiceSelect");
  const tamilLayoutSelect = document.getElementById("tamilLayoutSelect");
  const tamilAutoToggle = document.getElementById("tamilAutoInputToggle");

  if (!inputEl || !categorySelect) return;

  inputEl.addEventListener("input", updateStats);
  inputEl.addEventListener("keydown", (e) => {
    flashPressedKey(e.code);

    if (
      isTamilCategorySelected() &&
      tamilAutoToggle &&
      tamilAutoToggle.checked &&
      !e.ctrlKey &&
      !e.altKey &&
      !e.metaKey &&
      e.key.length === 1
    ) {
      const map = getAsciiToTamilCharMap();
      const mapped = map[e.key];
      if (mapped) {
        e.preventDefault();
        const start = inputEl.selectionStart;
        const end = inputEl.selectionEnd;
        const val = inputEl.value;
        inputEl.value = val.slice(0, start) + mapped + val.slice(end);
        inputEl.selectionStart = inputEl.selectionEnd = start + mapped.length;
        updateStats();
      }
    }
  });

  categorySelect.addEventListener("change", () => {
    renderOnScreenKeyboard();
    loadCategoryLessons("1");
  });
  if (tamilLayoutSelect) {
    tamilLayoutSelect.addEventListener("change", renderOnScreenKeyboard);
  }
  if (modeSelect) {
    modeSelect.addEventListener("change", () => loadCategoryLessons("1"));
  }
  if (practiceSelect) {
    practiceSelect.addEventListener("change", applySelectedPractice);
  }

  const initialPractice = practiceSelect?.dataset.initialPractice || "1";
  renderOnScreenKeyboard();
  loadCategoryLessons(initialPractice);
});
