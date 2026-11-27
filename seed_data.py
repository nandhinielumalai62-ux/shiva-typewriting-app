from werkzeug.security import generate_password_hash
from db import get_db

# Complete curated drills & passages aligned with all 6 institute categories
SEED_PASSAGES = [
    # 1. Junior English Basic (Practice 1 .. 6+)
    {
        "category": "Junior English Basic",
        "practice_number": 1,
        "title": "Practice 1 - Home Row Keys & Words",
        "content_type": "word",
        "target_wpm": 20,
        "target_strokes": 400,
        "passage_text": (
            "asdfgf ;lkjhj asdfgf ;lkjhj asdfgf ;lkjhj asdfgf ;lkjhj asdfgf ;lkjhj\n\n"
            "ask fad alas asks shad lads flags flask glass jag fag fall hash glad sags galls halls salad jak has jags gaff hall dash flash slash flasks lad sad lash adds gall gash shall lakhs dhalls"
        ),
    },
    {
        "category": "Junior English Basic",
        "practice_number": 2,
        "title": "Practice 2 - Top Row Keys & Words",
        "content_type": "word",
        "target_wpm": 22,
        "target_strokes": 450,
        "passage_text": (
            "awerqfa ;oiupj; awerqfa ;oiupj; awerqfa ;oiupj; awerqfa ;oiupj; awerqfa ;oiupj;\n\n"
            "fish kodak ahead larks quail apples reader flukes fiddle dead rails sales agile isles should liquid shower saddle idols jaded sails filed legal folder sledge squall larger grade jails lakes roses rupee squeal fields lulled dislike apple dirks lease equip skill easels dollar poorer require asked forks hedge would grass jokers jailer equals refresh fails usual liked walks peaks orders follow drawls defiles"
        ),
    },
    {
        "category": "Junior English Basic",
        "practice_number": 3,
        "title": "Practice 3 - Index Finger Reach & Words",
        "content_type": "word",
        "target_wpm": 24,
        "target_strokes": 500,
        "passage_text": (
            "gftfrf hjyjuj gftfrf hjyjuj gftfrf hjyjuj gftfrf hjyjuj gftfrf hjyjuj\n\n"
            "lawyers streaks shipped hillside herewith proposals shekels forward desired loophole jugglers straggles halves figures prepare leathery freehold struggles thought thyself treated youthful although territory freight quarter yodlers further glowbar slippers guileless forfeit pleased goodwill tortuous prepared telegraph laughed bottles whiskers thorough repeated addressed patrols regular equipped liliput etiquette flashlight without waggish laughter lifewall yesterday powerfully typewriter"
        ),
    },
    {
        "category": "Junior English Basic",
        "practice_number": 4,
        "title": "Practice 4 - Bottom Row Reach & Words",
        "content_type": "word",
        "target_wpm": 25,
        "target_strokes": 550,
        "passage_text": (
            "azsexdcf ;lpokmijn azsexdcf ;lpokmijn azsexdcf ;lpokmijn azsexdcf ;lpokmijn\n\n"
            "amazed journal gambols pickling vineyard grizzled except logical jackets failure austrian appeared frequent sieffeld succeed spacing movement joyfully premises daybook lecture western examined accuracy fortress kindled general mutual vocation quantity question executor jingled amulets service produce requires judicious jumbled arrival relative provoked starting cylinder materials swivels fizzed possible somewhat gracious thousand assessment violet regal becoming gracious thousand appearance"
        ),
    },
    {
        "category": "Junior English Basic",
        "practice_number": 5,
        "title": "Practice 5 - Alphabet & Number Drill",
        "content_type": "word",
        "target_wpm": 25,
        "target_strokes": 400,
        "passage_text": (
            "abcdefghijklmnopqrstuvwxyz., zyxwvutsrqponmlkjihgfedcba.,\n\n"
            "123454 098767 123454 098767 123454 098767 123454 098767"
        ),
    },
    {
        "category": "Junior English Basic",
        "practice_number": 6,
        "title": "Practice 6 - Moral Sentences & Touch Method",
        "content_type": "paragraph",
        "target_wpm": 28,
        "target_strokes": 650,
        "passage_text": (
            "Lost time is never regained. Get up early and do your work. To-day's youth and to-morrow's old. Age is a virtue when wisdom is with it. Measure your word before it goes out of you. Children are innocent and should be guided rightly. Our Land had great sages who knew the eternal truth.\n\n"
            "Men live by deeds and not by years. God helps those who help themselves. Honest work always brings its reward. A man without character should not be trusted. Rude language speaks ill of the man who uses it. Never lose courage when faced with difficulties. It is easier to ask questions than to answer them. Pandit Nehru always devoted himself to public affairs. It is essential to use the touch method. The correct degree of touch is an important factor. The touch should be neither too heavy nor too light. High speed is within the capacity of every typist. Astronomy is the oldest science. Young men have a right to be happy. A petty man refuses to admit delay. Man is mortal, but his spirit is immortal. Sivaji fought to keep the real spirit of India alive. Tilak was a great Patriot and also a brilliant scholar. Kindly supply 5 tables (4' x 2') immediately."
        ),
    },

    # 2. Junior English Speed (Practice 1 .. 3)
    {
        "category": "Junior English Speed",
        "practice_number": 1,
        "title": "Practice 1 - Urban Mobility & Public Transport",
        "content_type": "paragraph",
        "target_wpm": 30,
        "target_strokes": 1500,
        "passage_text": (
            "The way we travel from our homes to our workplaces shapes the world around us in significant ways. For many years, reliance on private vehicles has been the default choice for millions of people. While this provides comfort and independence, it comes at a cost to our environment and well-being. Rising traffic congestion in cities leads to wasted time and stress, while emissions from cars contribute to the degradation of our air quality.\n\n"
            "It is time to rethink our daily habits and consider how small changes in our routine can lead to a cleaner future for everyone. By acknowledging the impact of our individual decisions, we can start a movement toward more sustainable ways of moving through our shared urban spaces. Public transportation systems, when well-managed, offer a highly effective alternative to individual vehicle ownership. Trains, buses, and metro lines provide routes that carry large numbers of passengers, significantly reducing the total volume of traffic on our roads."
        ),
    },
    {
        "category": "Junior English Speed",
        "practice_number": 2,
        "title": "Practice 2 - Discipline & Office Administration",
        "content_type": "paragraph",
        "target_wpm": 30,
        "target_strokes": 1500,
        "passage_text": (
            "Accuracy and speed in commercial typewriting depend upon regular daily practice and proper posture at the desk. Every student should keep both feet flat on the floor and hold the wrists slightly raised above the frame of the machine. Looking at the copy rather than the keyboard builds strong finger memory and prevents unnecessary errors during timed examinations.\n\n"
            "In modern government and corporate offices, clear written communication remains the foundation of efficient administration. Neat formatting, consistent spacing after punctuation marks, and careful proofreading ensure that official letters and statements are ready for immediate dispatch. Developing steady rhythm across ten minutes of continuous typing helps candidates complete Junior Grade speed tests with confidence."
        ),
    },
    {
        "category": "Junior English Speed",
        "practice_number": 3,
        "title": "Practice 3 - Digital Literacy & Skill Development",
        "content_type": "paragraph",
        "target_wpm": 32,
        "target_strokes": 1500,
        "passage_text": (
            "Skill development programs prepare young learners to meet the practical needs of industry and public service. Alongside academic knowledge, vocational training in keyboarding, accounting, and office automation opens reliable avenues of employment across towns and cities. Dedicated institutions guide students step by step from basic finger drills to fluent passage composition.\n\n"
            "Consistent evaluation through timed practice sessions enables learners to identify difficult key combinations and correct them early. When speed improves without sacrificing accuracy, candidates gain both self-assurance and professional readiness. Regular attendance and focused effort over several months always yield lasting mastery."
        ),
    },

    # 3. Senior English Speed (Practice 1 .. 3)
    {
        "category": "Senior English Speed",
        "practice_number": 1,
        "title": "Practice 1 - Rural Infrastructure & Conservation",
        "content_type": "paragraph",
        "target_wpm": 45,
        "target_strokes": 2250,
        "passage_text": (
            "Rural infrastructure plays an important role in the overall development of a country. Villages are the backbone of a nation, and improving rural facilities helps to increase the quality of life of people living in rural areas. Good roads, reliable electricity, clean drinking water, healthcare facilities and communication networks are essential for the progress of villages. Better infrastructure connects rural communities with cities and creates new opportunities for education, employment and economic growth.\n\n"
            "Agriculture and rural industries depend greatly on proper infrastructure. Improved transportation facilities help farmers to carry their products to markets quickly and safely. Modern storage facilities and digital services support rural development by reducing losses and increasing income opportunities. Providing better schools, hospitals and skill development centers in villages encourages people to build a better future without leaving their hometowns.\n\n"
            "Environmental protection is the responsibility of all citizens. Natural resources such as forests, water, soil and air must be protected for future generations. Rapid development should always be balanced with environmental conservation. Planting trees, reducing pollution, saving water and promoting renewable energy are important steps for protecting nature. A strong economy requires both developed rural areas and growing industries."
        ),
    },
    {
        "category": "Senior English Speed",
        "practice_number": 2,
        "title": "Practice 2 - Public Governance & Citizen Services",
        "content_type": "paragraph",
        "target_wpm": 45,
        "target_strokes": 2250,
        "passage_text": (
            "Transparent public administration strengthens trust between citizens and civic institutions. When municipal offices, revenue departments, and educational boards maintain accurate records and timely schedules, everyday services become predictable and fair for every resident. Well-trained clerical staff and stenographers play an indispensable role in drafting notices, recording proceedings, and organizing official correspondence.\n\n"
            "Rapid urbanization requires thoughtful planning in water supply, waste management, and affordable housing. Local bodies must work closely with engineering teams and community representatives to inspect ongoing projects and verify quality standards. Clear reporting and disciplined documentation ensure that public funds are utilized efficiently for long-term community benefit.\n\n"
            "Senior grade candidates are expected to sustain high typing velocity across multi-paragraph passages while keeping typographical mistakes to a minimum. Controlled breathing, relaxed shoulders, and steady keystroke cadence allow experienced typists to handle complex punctuation, capital letters, and numerical figures effortlessly within the allotted ten minutes."
        ),
    },
    {
        "category": "Senior English Speed",
        "practice_number": 3,
        "title": "Practice 3 - Sustainable Energy & Industrial Growth",
        "content_type": "paragraph",
        "target_wpm": 45,
        "target_strokes": 2250,
        "passage_text": (
            "Clean energy transition has become a central priority for economies seeking reliable industrial growth without harming ecological balance. Solar parks, wind turbines, and modernized power grids reduce dependence on imported fuels while creating skilled technical jobs in manufacturing and maintenance. Long-term investment in research encourages engineers to build higher-capacity batteries and energy-saving machinery.\n\n"
            "Small and medium enterprises form a vital part of regional supply chains, turning raw materials into finished goods for domestic and international markets. Access to fair credit, reliable logistics, and vocational training helps entrepreneurs expand production and adopt safer workplace practices. Cooperative efforts between training institutes and local businesses bridge the gap between classroom instruction and real industry needs.\n\n"
            "Every citizen can contribute to resource conservation through mindful consumption in daily life. Turning off unused electrical appliances, harvesting rainwater during monsoon seasons, and minimizing single-use plastics collectively create measurable positive change. Sustainable progress depends equally on forward-looking policies and responsible community participation."
        ),
    },

    # 4. Junior Tamil Basic (Practice 1 .. 4)
    {
        "category": "Junior Tamil Basic",
        "practice_number": 1,
        "title": "Practice 1 - Tamil Home Row Key Drills",
        "content_type": "word",
        "target_wpm": 18,
        "target_strokes": 350,
        "passage_text": (
            "யளனக டமத யளனக டமத யளனக டமத யளனக டமத யளனக டமத யளனக\n\n"
            "யளனகபக டமதாத யளனகபக டமதாத யளனகபக டமதாத யளனகபக டமதாத"
        ),
    },
    {
        "category": "Junior Tamil Basic",
        "practice_number": 2,
        "title": "Practice 2 - Simple Two & Three Letter Tamil Words",
        "content_type": "word",
        "target_wpm": 20,
        "target_strokes": 400,
        "passage_text": (
            "கனம் கனம் மனம் கடன் மடம் கது காய் கபம் மகள் பயன்\n\n"
            "தானம் கானம் மாயம் பாடம் மாடம் கடகம் கமகம் வாமம் கள்ளன் தாயம்"
        ),
    },
    {
        "category": "Junior Tamil Basic",
        "practice_number": 3,
        "title": "Practice 3 - Compound & Vowel-Sign Tamil Words",
        "content_type": "word",
        "target_wpm": 22,
        "target_strokes": 450,
        "passage_text": (
            "கப்பம் பட்டம் தத்தம் பள்ளம் மக்கள் கட்டம் கம்பம் மாதம் தாகம் டப்பாய்\n\n"
            "கடமான் தாயகம் கானகம் பாட்டன் மாளயம் பம்பாய் கிட்டம் கர்த்தா கமலான் டாக்டர்"
        ),
    },
    {
        "category": "Junior Tamil Basic",
        "practice_number": 4,
        "title": "Practice 4 - Advanced Basic Tamil Word Practice",
        "content_type": "word",
        "target_wpm": 24,
        "target_strokes": 500,
        "passage_text": (
            "கடமான் தாயகம் கானகம் பாட்டன் மாளயம் பம்பாய் கிட்டம் கர்த்தா கமலான் டாக்டர்\n\n"
            "காப்பகம் பட்டாளம் கட்டாயம் பக்கமாய் பக்தனாய் மட்டமாய் காட்டான் பார்த்தூன் காப்பாய் காப்பாளர்"
        ),
    },

    # 5. Junior Tamil Speed (Practice 1 .. 3)
    {
        "category": "Junior Tamil Speed",
        "practice_number": 1,
        "title": "Practice 1 - கைத்தறித் தொழில் வளர்ச்சி",
        "content_type": "paragraph",
        "target_wpm": 25,
        "target_strokes": 1250,
        "passage_text": (
            "தமிழ் நாட்டில் கைத்தறித் தொழிலுக்கு பெரும் நெருக்கடி ஏற்பட்டுள்ளது, ஏராளமான துணிகள் விற்பனை ஆகாமல் தேங்கிக் கிடக்கின்றன. அது மட்டுமன்றி, கைத்தறி ஆடைகளின் ஏற்றுமதியும் மிகவும் குறைந்துள்ளது. இந்த இரண்டு பிரச்சினைகளுக்கு உடனடியாக கவனம் செலுத்தப்படாவிட்டால் அத்தொழிலின் நிலைமை மேலும் மோசமாகிவிடும். ஏற்கனவே பல கைத்தறிகள் வேலையில்லாமல் இருப்பதாகச் சொல்லப்படுகிறது. விவசாயத்தைப் போலவே ஏராளமான பேருக்கு வேலை வாய்ப்பு அளிக்கின்ற ஒரு தொழில் நசிந்துவிடாமல் பார்த்துக்கொள்ள வேண்டிய பொறுப்பு மத்திய, மாநில அரசுகளுக்கு உண்டு. மாநிலத்திலிருந்து ஏற்றுமதியாகும் கைத்தறி ஆடைகளின் மதிப்பு ஆண்டுதோறும் குறைந்துவிட்டதால் கோடிக்கணக்கான மதிப்புள்ள துணிகள் தேங்கிக் கிடக்கின்றன என்பது கவலை அளிக்கிறது.\n\n"
            "இத்தொழிலில் உள்ளவர்கள் விசைத்தறித் துறையில் இருந்தும், மில்கள் துறையில் இருந்தும் கடுமையான போட்டியைச் சமாளிக்க வேண்டியிருக்கிறது. இதனையெல்லாம் கருத்தில் கொண்டுதான் இந்தத் தொழிலின் வளர்ச்சிக்காக சில வகைத் துணிகள் உற்பத்தியைக் கைத்தறிக்கு ஒதுக்குவது என்று சில விசேட நடவடிக்கைகளை மத்திய, மாநில அரசுகள் அவ்வப்போது மேற்கொண்டுள்ளது. அப்படியும் அந்தத் தொழிலுக்கு பிரச்சினைகள் தொடர்ந்து நீடித்துக் கொண்டிருக்கின்றன. எனவே பிரச்சினைகளுக்கு உண்மையான காரணம் என்ன என்பதைக் கண்டறிந்து தகுந்த நடவடிக்கைகளை மேற்கொள்ள வேண்டும். கைத்தறித் துணிகளின் உற்பத்தித் செலவு அதிகரித்துவிட்டது. இப்போதைய நிலைமைக்கு இது முக்கிய ஒரு காரணமாகும். நூல் விலைகள் அசாதாரணமான அளவிற்கு உயர்ந்துவிட்டதால் உற்பத்திச் செலவு அதிகரித்துவிட்டதாக சொல்லப்படுகிறது. இந்த நூல் விலை உயர்வு பற்றி கைத்தறித் துறையிலுள்ளவர்கள் மட்டுமன்றி மாநில அரசினரும் குறை கூறியிருக்கிறார்கள். கைத்தறி ஆடை சம்பந்தமான குறியளவை அடைய வேண்டுமானால் இவற்றின் விலைகள் மற்ற நாட்டுத் துணிகளின் விலைகளுடன் ஒப்பிடும் போது, குறைவாக இல்லாவிட்டாலும் அதிகமாக இருக்கக் கூடாது."
        ),
    },
    {
        "category": "Junior Tamil Speed",
        "practice_number": 2,
        "title": "Practice 2 - கல்வி மற்றும் நேர மேலாண்மை",
        "content_type": "paragraph",
        "target_wpm": 25,
        "target_strokes": 1250,
        "passage_text": (
            "மாணவர்கள் தங்கள் அன்றாட வாழ்வில் நேரத்தைத் திட்டமிட்டுப் பயன்படுத்துவது வெற்றிக்கு அடித்தளமாக அமைகிறது. காலையில் எழுந்தது முதல் இரவு உறங்கும் வரை ஒவ்வொரு மணி நேரத்தையும் பயனுள்ள முறையில் செலவிடப் பழக வேண்டும். தட்டச்சுப் பயிற்சியில் வேகமும் துல்லியமும் ஒரே நேரத்தில் வளர வேண்டுமானால் தினமும் குறைந்தது பத்து நிமிடங்கள் தொடர்ந்து தவறின்றிப் பயிற்சி செய்வது மிகவும் அவசியமாகும்.\n\n"
            "நல்ல எழுத்துத் திறனும் மொழி அறிவும் அரசுத் தேர்வுகளிலும் அலுவலகப் பணிகளிலும் உயர்ந்த இடத்தைத் தேடித்தரும். தமிழ் எழுத்துக்களின் மெய்யெழுத்து மற்றும் உயிர்மெய் குறியீடுகளை விரைவாகவும் சரியாகவும் அடிக்கும் பழக்கம் தொடர்ந்து பயிற்சி செய்வதால் மட்டுமே கிடைக்கும். பிழைகளைக் குறைத்து சீரான வேகத்தில் தட்டச்சு செய்யும் மாணவர்கள் தேர்வில் எளிதாக வெற்றி பெறுவார்கள்."
        ),
    },
    {
        "category": "Junior Tamil Speed",
        "practice_number": 3,
        "title": "Practice 3 - கிராமப்புற நூலகங்களும் வாசிப்பும்",
        "content_type": "paragraph",
        "target_wpm": 26,
        "target_strokes": 1250,
        "passage_text": (
            "ஊரகப் பகுதிகளில் அமைந்துள்ள பொது நூலகங்கள் மாணவர்களுக்கும் இளைஞர்களுக்கும் அறிவுக் களஞ்சியங்களாகத் திகழ்கின்றன. செய்தித்தாள்கள், பாடநூல்கள் மற்றும் போட்டித் தேர்வு வழிகாட்டிகள் அனைவருக்கும் எளிதில் கிடைப்பதால் பலர் தங்களின் பொது அறிவை வளர்த்துக் கொள்ள முடிகிறது. வாசிப்புப் பழக்கம் சிந்தனைத் திறனை மேம்படுத்துவதோடு மொழி வளத்தையும் அதிகரிக்கிறது.\n\n"
            "இன்றைய காலத்தில் தொழில்நுட்ப வசதிகள் பெருகியிருந்தாலும் புத்தகங்களைப் படிக்கும் பழக்கம் என்றும் குறையக் கூடாது. நல்ல நூல்களைத் தேர்ந்தெடுத்துப் படிப்பதன் மூலம் சமூகப் பொறுப்புணர்வும் ஒழுக்கமும் வளர்கின்றன. கிராமங்கள் தோறும் நூலகங்களைச் சிறப்பாகப் பராமரிப்பது எதிர்காலத் தலைமுறைக்கு நாம் செய்யும் சிறந்த தொண்டாகும்."
        ),
    },

    # 6. Senior Tamil Speed (Practice 1 .. 3)
    {
        "category": "Senior Tamil Speed",
        "practice_number": 1,
        "title": "Practice 1 - பொறுமை எனும் நற்பண்பு",
        "content_type": "paragraph",
        "target_wpm": 35,
        "target_strokes": 1750,
        "passage_text": (
            "பொறுமை என்பது மனித வாழ்வில் மிக முக்கியமான ஒரு பண்பு ஆகும். இது ஒரு சிறந்த குணம் என்று போற்றப்படுகிறது. பொறுமை உள்ளவர்கள் எந்த ஒரு செயலையும் நிதானமாக செய்வார்கள். அவசரப்பட மாட்டார்கள். பொறுமை ஒருவரின் மனதை அமைதியாக வைத்திருக்க உதவும். கோபம், பதற்றம் போன்ற எதிர்மறை உணர்வுகளை கட்டுப்படுத்தும் சக்தி பொறுமைக்கு உண்டு. பொறுமை இல்லாதவர்கள் சிறிய விஷயங்களுக்காகவும் சண்டையிடுவார்கள். அவர்கள் தங்கள் முடிவுகளை அவசரமாக எடுப்பார்கள். இதனால் பல தவறுகள் நடக்கும்.\n\n"
            "பொறுமை ஒரு மனிதனை சிறப்பான வாழ்க்கைக்கு வழிநடத்தும். வாழ்க்கையில் வெற்றி பெற பொறுமை மிக அவசியம். கடினமான சூழ்நிலைகளில் கூட பொறுமையுடன் செயல்பட வேண்டும். ஒரு மாணவன், கல்வி கற்பதில் பொறுமையுடன் இருக்க வேண்டும். அப்பொழுதுதான் அவன் நன்றாக படித்து தேர்வுகளில் நல்ல மதிப்பெண்கள் பெற முடியும். ஒரு விவசாயி பயிர் வளர்ப்பதில் பொறுமையுடன் இருக்க வேண்டும். விதைத்த உடன் பலன் எதிர்பார்ப்பது சரியல்ல. அறுவடைக்குக் காத்திருக்கும் பொறுமை அவசியமாகும். எந்த ஒரு பெரிய காரியத்தையும் சாதிக்க பொறுமை மிக முக்கியம்.\n\n"
            "சமூக உறவுகளில் பொறுமை மிகவும் முக்கியமானது. குடும்ப உறுப்பினர்களிடமும், நண்பர்களிடமும் பொறுமையுடன் பழக வேண்டும். மற்றவர்கள் சொல்லும் கருத்துக்களை பொறுமையுடன் கேட்க வேண்டும். கோபப்படுவது உடனே நல்லதல்ல. பொறுமையுடன் மற்றவர்களின் உணர்வுகளை புரிந்து கொள்ள முயற்சி செய்ய வேண்டும். இது உறவுகளை பலப்படுத்தும். சண்டைகளைத் தவிர்க்கும். எந்த ஒரு பிரச்சனைக்கும் தீர்வு காண பொறுமை உதவும். ஒரு சிக்கலான பிரச்சனையை அணுகும்போது, பொறுமையுடன் அனைத்து அம்சங்களையும் ஆராய வேண்டும்."
        ),
    },
    {
        "category": "Senior Tamil Speed",
        "practice_number": 2,
        "title": "Practice 2 - வேளாண்மை மற்றும் நீர் மேலாண்மை",
        "content_type": "paragraph",
        "target_wpm": 35,
        "target_strokes": 1750,
        "passage_text": (
            "தமிழகத்தின் பொருளாதார வளர்ச்சியில் வேளாண்மைத் துறை மிக முக்கியப் பங்கு வகிக்கிறது. பருவமழையை நம்பியுள்ள விவசாயிகள் நீரைச் சிக்கனமாகப் பயன்படுத்தி அதிக மகசூல் பெறும் முறைகளைக் கற்றுக் கொள்ள வேண்டும். சொட்டு நீர்ப்பாசனம் மற்றும் தெளிப்பு நீர்ப்பாசனம் போன்ற நவீன நுட்பங்கள் நீரைச் சேமிப்பதுடன் பயிர்களின் வளர்ச்சியையும் மேம்படுத்துகின்றன.\n\n"
            "ஏரிகள், குளங்கள் மற்றும் கால்வாய்களைத் தூர்வாரி மழைநீரைச் சேமிப்பது நமது பாரம்பரிய நீர் மேலாண்மை முறையாகும். கிராம மக்கள் அனைவரும் ஒன்றிணைந்து நீர்நிலைகளைப் பாதுகாப்பதன் மூலம் நிலத்தடி நீர்மட்டம் உயர்ந்து குடிநீர் தட்டுப்பாடு நீங்கும். இயற்கை உரங்களைப் பயன்படுத்துவதால் மண்ணின் வளம் காக்கப்பட்டு நஞ்சில்லா உணவுப் பொருட்கள் கிடைக்கின்றன.\n\n"
            "அரசு மற்றும் வேளாண் பல்கலைக்கழகங்கள் வழங்கும் புதிய விதை வகைகளையும் தொழில்நுட்ப ஆலோசனைகளையும் விவசாயிகள் முறையாகப் பயன்படுத்த வேண்டும். விளைபொருட்களுக்கு நியாயமான விலை கிடைக்கச் சந்தை வசதிகளும் சேமிப்புக் கிடங்குகளும் விரிவுபடுத்தப்பட வேண்டும். வளமான வேளாண்மையே நாட்டின் உணவுப் பாதுகாப்பிற்கு உறுதியான அடித்தளமாகும்."
        ),
    },
    {
        "category": "Senior Tamil Speed",
        "practice_number": 3,
        "title": "Practice 3 - தமிழ் இலக்கியமும் பண்பாடும்",
        "content_type": "paragraph",
        "target_wpm": 35,
        "target_strokes": 1750,
        "passage_text": (
            "உலகின் தொன்மையான செம்மொழிகளில் ஒன்றான தமிழ் மொழி, காலத்தால் அழியாத இலக்கியச் செல்வங்களைத் தன்னகத்தே கொண்டுள்ளது. சங்க இலக்கியங்கள் மனித வாழ்வின் அன்பையும் வீரத்தையும் இயற்கையோடு இணைந்த வாழ்க்கை முறையையும் அழகாக எடுத்துரைக்கின்றன. திருக்குறள் போன்ற அறநூல்கள் உலக மக்கள் அனைவருக்கும் பொதுவான வாழ்வியல் நெறிகளை வழங்குகின்றன.\n\n"
            "மொழியைப் பாதுகாத்து வளர்ப்பதில் கல்வி நிறுவனங்களும் இளைய தலைமுறையினரும் பெரும் பங்கு வகிக்கின்றனர். தூய தமிழ் சொற்களைப் பயன்படுத்திப் பேசுவதும் எழுதுவதும் மொழியின் இனிமையை நிலைநிறுத்தும். கணினி மற்றும் இணைய உலகிலும் தமிழ் தட்டச்சு மற்றும் மென்பொருள் பயன்பாடு வேகமாக வளர்ந்து வருவது பெருமைக்குரிய செய்தியாகும்.\n\n"
            "முதுநிலை தட்டச்சுத் தேர்வில் தேர்ச்சி பெற விரும்பும் மாணவர்கள் பத்து நிமிட நேர வரம்பிற்குள் மூன்று பத்திகளையும் பிழையின்றித் தட்டச்சு செய்யும் திறனைப் பெற வேண்டும். தினசரி பயிற்சியும் கவனக்குவிப்பும் இருந்தால் தமிழ் தட்டச்சில் உயர்ந்த வேகத்தையும் நேர்த்தியையும் எளிதில் அடைய முடியும்."
        ),
    },
]


def seed_initial_data():
    with get_db() as db:
        # 1. Seed default Admin user if no staff exists
        staff_count = db.fetchone("SELECT COUNT(*) AS cnt FROM staff_users")
        if not staff_count or staff_count["cnt"] == 0:
            db.execute(
                """
                INSERT INTO staff_users (username, full_name, role, password_hash, phone)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    "admin",
                    "Principal / Chief Instructor",
                    "admin",
                    generate_password_hash("admin123"),
                    "9876543210",
                ),
            )

        # 2. Initialize sequential student code counter
        counter = db.fetchone(
            "SELECT counter_key FROM institute_counters WHERE counter_key = %s",
            ("student_code",),
        )
        if not counter:
            db.execute(
                "INSERT INTO institute_counters (counter_key, last_number) VALUES (%s, %s)",
                ("student_code", 0),
            )

        # 3. Seed practice passages if missing
        for item in SEED_PASSAGES:
            existing = db.fetchone(
                "SELECT id FROM practice_passages WHERE category = %s AND practice_number = %s",
                (item["category"], item["practice_number"]),
            )
            if not existing:
                db.execute(
                    """
                    INSERT INTO practice_passages
                        (category, practice_number, title, content_type, passage_text, target_wpm, target_strokes)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        item["category"],
                        item["practice_number"],
                        item["title"],
                        item["content_type"],
                        item["passage_text"],
                        item["target_wpm"],
                        item["target_strokes"],
                    ),
                )

        db.commit()
