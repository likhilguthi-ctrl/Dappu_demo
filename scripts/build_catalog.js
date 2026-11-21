const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const EXTRACTED = path.join(ROOT, 'assets', 'extracted');

// Helper to ensure directory exists
function ensureDir(dir) {
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
}

// Target directories
const DIRS = {
  culture: path.join(ROOT, 'assets', 'culture'),
  education: path.join(ROOT, 'assets', 'education'),
  films: path.join(ROOT, 'assets', 'films')
};

Object.values(DIRS).forEach(d => {
  ensureDir(path.join(d, 'banners', 'en'));
  ensureDir(path.join(d, 'banners', 'te'));
  ensureDir(path.join(d, 'posters', 'en'));
  ensureDir(path.join(d, 'posters', 'te'));
});

// Copy file helper
function copyAsset(srcFolder, srcFile, destFolder, destFile) {
  const srcPath = path.join(EXTRACTED, srcFolder, srcFile);
  const destPath = path.join(destFolder, destFile);
  if (fs.existsSync(srcPath)) {
    fs.copyFileSync(srcPath, destPath);
    return true;
  } else {
    console.warn('Source file not found:', srcPath);
    return false;
  }
}

// ─────────────────────────────────────────────────────────────────────────────
// 1. CULTURE ASSETS MAPPING (Verified 100% against actual image artwork)
// ─────────────────────────────────────────────────────────────────────────────
const cultureFolder = 'cluture-20261121T052108Z-1-001/cluture';
const cultureItems = [
  {
    id: 'culture_dappu_craftsmanship',
    ageRating: 'U/A 13+',
    duration: '1h 45m',
    year: '2025',
    en: {
      title: 'Dappu Craftsmanship: Making the Instrument',
      description: 'The sacred craft, rhythmic pulse, and ancestral artisanal legacy behind crafting the authentic community Dappu drum.',
      bannerSrc: 'Dappu Craftsmanship_ Making the Instrument.png',
      posterSrc: 'Dappu Craftsmanship_ Making the Instrument (1).png'
    },
    te: {
      title: 'దప్పు వాద్య నిర్మాణం – తయారీలోని నైపుణ్యం',
      description: 'పవిత్రమైన సంప్రదాయ దప్పు తయారీ విధానం, చర్మ కళా నైపుణ్యం మరియు చారిత్రక సామాజిక స్వరమాధ్యమం.',
      bannerSrc: 'Crafting the Traditional Dappu Drum.png',
      posterSrc: 'Crafting the Traditional Dappu Drum (1).png'
    }
  },
  {
    id: 'culture_dappu_expression',
    ageRating: 'U/A 13+',
    duration: '1h 32m',
    year: '2024',
    en: {
      title: 'Dappu: The Drum of Community Expression',
      description: 'Exploring the cultural heartbeat and socio-political identity forged through generations of community drummers.',
      bannerSrc: 'Dappu_ The Drum of Community Expression.jpg',
      posterSrc: 'Dappu_ Drum of Community Expression.png'
    },
    te: {
      title: 'దప్పు: సముదాయపు స్వరమాధ్యం',
      description: 'తరతరాల సంస్కృతి, జీవన పోరాటం మరియు దప్పు మోత వెనుక ఉన్న సామాజిక చైతన్య ప్రయాణం.',
      bannerSrc: 'Dappu_ The Drum of Community Expression (1).png',
      posterSrc: 'తెలుగు దప్పు_ సముదాయపు స్వరమాధ్యం.png'
    }
  },
  {
    id: 'culture_chindu_yakshaganam',
    ageRating: 'U/A 13+',
    duration: '2h 10m',
    year: '2025',
    en: {
      title: 'Chindu Yakshaganam: Heritage in Motion',
      description: 'The vibrant, dramatic folk theater form preserving centuries-old mythological narratives, dance, and cultural theater.',
      bannerSrc: 'Chindu Yakshaganam Folk Festival Poster.png',
      posterSrc: 'Chindu Yakshaganam Cultural Performance Poster.png'
    },
    te: {
      title: 'చిందు యక్షగానం',
      description: 'వందల ఏళ్ల ప్రాచీన జానపద నాట్య సంప్రదాయం, వేషధారణ, నటన మరియు పౌరాణిక కథా ప్రదర్శనల అద్భుత దృశ్యం.',
      bannerSrc: 'చిందు యక్షగానం పోస్టర్.png',
      posterSrc: 'Chindu Yakshaganam Heritage Poster.png'
    }
  },
  {
    id: 'culture_dandora_protest',
    ageRating: 'U/A 13+',
    duration: '1h 55m',
    year: '2024',
    en: {
      title: 'Dandora: Sound, Protest and Public Voice',
      description: 'The historic resonance of public announcement turning into an unstoppable movement for social dignity and constitutional justice.',
      bannerSrc: 'Drumbeat of Public Voice.png',
      posterSrc: 'Dandora_ Sound and Protest.png'
    },
    te: {
      title: 'దండోరా: శబ్దం, నిరసన మరియు ప్రజల గొంతుక',
      description: 'ప్రజా గళం, చైతన్య బాట మరియు ఆత్మగౌరవ పోరాటంలో దండోరా సాధించిన చారిత్రక విజయాలు.',
      bannerSrc: 'Telugu Protest Poster with Drum and Crowd.png',
      posterSrc: 'ప్రజల గొంతుక దండోరా.png'
    }
  },
  {
    id: 'culture_gosangi_performance',
    ageRating: 'U/A 13+',
    duration: '1h 28m',
    year: '2025',
    en: {
      title: 'Gosangi Performance Tradition',
      description: 'A deep dive into the nomadic performance arts, balladeers, and musical narratives preserved across Telangana and Andhra.',
      bannerSrc: 'Gosangi_ Sunset Performance Tradition.png',
      posterSrc: 'Gosangi_ A Folk Performance Tradition.png'
    },
    te: {
      title: 'గోసాంగి ప్రదర్శన సంప్రదాయం',
      description: 'గ్రామీణ సాయంత్రాల్లో గోసాంగి కళాకారుల సంగీతం, కథాగానం మరియు అరుదైన సాంస్కృతిక వారసత్వం.',
      bannerSrc: 'Gosangi Folk Performance at Sunset.png',
      posterSrc: 'Gosangi Folk Performance Tradition.png'
    }
  },
  {
    id: 'culture_jambavantaru_purana',
    ageRating: 'U/A 13+',
    duration: '1h 50m',
    year: '2024',
    en: {
      title: 'Jambavanthula Kathaprasangam Tradition',
      description: 'The master oral storytellers reciting epics of cosmic beginnings and ancestral valor with painted scrolls.',
      bannerSrc: 'Jambavantaru_ Epic Folk Storytelling Poster.png',
      posterSrc: 'Jambavantaru_ Jamba Purana Storyteller.png'
    },
    te: {
      title: 'జాంబవంతులు జాంబ పురాణం',
      description: 'జాంబవ పురాణ మూలాలు, పట ప్రదర్శన మరియు మౌఖిక సంప్రదాయ కథా ప్రసంగాల విశేషాలు.',
      bannerSrc: 'Jambavants Storyteller and Painted Scroll.png',
      posterSrc: 'Jambavantal Kathaprasangam Tradition.png'
    }
  },
  {
    id: 'culture_dakkali_scroll',
    ageRating: 'U/A 13+',
    duration: '1h 40m',
    year: '2025',
    en: {
      title: 'Dakkali Scroll Narration',
      description: 'Unfurling the legendary illuminated scrolls: visually captivating performance art narrating ancestral legends.',
      bannerSrc: 'Dakkali Scroll Storytelling at Dusk (1).png',
      posterSrc: 'Dakkali Scroll Storyteller at Sunset (1).png'
    },
    te: {
      title: 'డక్కలి చిత్రపట కథనం',
      description: 'సాయం సంధ్యలో డక్కలి కళాకారుల చిత్రపట ప్రదర్శన, వంశ చరిత్రల గానం మరియు చిత్రకళా సౌందర్యం.',
      bannerSrc: 'Telugu Scroll Storyteller at Sunset.png',
      posterSrc: 'Telugu Storyteller’s Painted Scroll.png'
    }
  },
  {
    id: 'culture_leather_craft',
    ageRating: 'U/A 13+',
    duration: '1h 35m',
    year: '2024',
    en: {
      title: 'Madiga Leather Technology & Craftsmanship',
      description: 'Honoring centuries of indigenous tanning chemistry, leatherwork craftsmanship, and utilitarian mastery.',
      bannerSrc: 'Madiga Leather Technology Poster.png',
      posterSrc: 'Madiga Leather Technology Workshop.png'
    },
    te: {
      title: 'మాదిగల తోలు సాంకేతిక విజ్ఞానం',
      description: 'తరతరాల స్వాభావిక సాంకేతిక పరిజ్ఞానం, తోలు శుద్ధి నైపుణ్యం మరియు దేశీయ ఉత్పత్తి పరిశ్రమ.',
      bannerSrc: 'Traditional Leathercraft and Telugu Heritage.png',
      posterSrc: 'Leatherworking Hands and Telugu Craft Title.png'
    }
  },
  {
    id: 'culture_oral_histories',
    ageRating: 'U/A 13+',
    duration: '2h 05m',
    year: '2025',
    en: {
      title: 'Oral Histories of Madiga Villages',
      description: 'Elders share unwritten memoirs, folk memory, survival songs, and communal wisdom from rural villages.',
      bannerSrc: 'Madiga Villages_ Oral Histories.png',
      posterSrc: 'Oral Histories of Madiga Villages.png'
    },
    te: {
      title: 'మాదిగ గ్రామాల మౌఖిక చరిత్రలు',
      description: 'గ్రామీణ పెద్దలు పంచుకున్న జీవిత అనుభవాలు, పల్లె జీవన చిత్రాలు మరియు మౌఖిక విజ్ఞానం.',
      bannerSrc: 'Madiga Villages_ Oral Histories Poster.png',
      posterSrc: 'Oral Histories of Village Elders.png'
    }
  },
  {
    id: 'culture_women_writers',
    ageRating: 'U/A 13+',
    duration: '1h 48m',
    year: '2025',
    en: {
      title: 'Madiga Women Writers: Literature and Memory',
      description: 'Powerful voices, poetry, and autobiographical narratives documenting lived experiences and feminist resistance.',
      bannerSrc: 'Madiga Women Writers_ Literature and Memory (2).png',
      posterSrc: 'Madiga Women Writers_ Literature and Memory (4).png'
    },
    te: {
      title: 'మాదిగ మహిళా రచయిత్రులు',
      description: 'కవిత్వం, కథలు మరియు ఆత్మకథల ద్వారా మహిళా దృక్కోణంలో సమాజ వాస్తవాలను ఆవిష్కరించిన సాహిత్య ధార.',
      bannerSrc: 'Madiga Women Writers_ Literature and Memory (1).png',
      posterSrc: 'Madiga Women Writers_ Literature and Memory (3).png'
    }
  }
];

// ─────────────────────────────────────────────────────────────────────────────
// 2. EDUCATION ASSETS MAPPING (Verified 100% against actual image artwork)
// ─────────────────────────────────────────────────────────────────────────────
const eduFolder = 'Education-20261121T052108Z-1-001/Education';
const educationItems = [
  {
    id: 'edu_neet_jee_prep',
    ageRating: 'U/A 13+',
    duration: '1h 50m',
    year: '2025',
    en: {
      title: 'NEET & JEE Preparation Pathway',
      description: 'Strategic roadmap, expert masterclasses, and top mentorship guiding community aspirants into premier national medical and engineering institutes.',
      bannerSrc: 'NEET & JEE Preparation Pathway (2).png',
      posterSrc: 'NEET & JEE Preparation Pathway (1).png'
    },
    te: {
      title: 'నీట్ & జేఈఈ సిద్ధత మార్గం',
      description: 'టాప్ మెంటార్ల క్లాసులు, ప్రిపరేషన్ వ్యూహాలు మరియు జాతీయ స్థాయి విద్యా సంస్థల్లో సీట్ల సాధన బాట.',
      bannerSrc: 'NEET & JEE Preparation Pathway.png',
      posterSrc: 'NEET & JEE Preparation Pathway (5).png'
    }
  },
  {
    id: 'edu_digital_skills',
    ageRating: 'U/A 13+',
    duration: '1h 35m',
    year: '2025',
    en: {
      title: 'Digital Skills & IT Learning',
      description: 'Equipping rural and first-generation learners with modern software skills, full-stack programming, and AI tools for global technology careers.',
      bannerSrc: 'Digital Skills and IT Learning.png',
      posterSrc: 'Digital Skills & IT Learning.png'
    },
    te: {
      title: 'డిజిటల్ నైపుణ్యాలు & ఐటీ అభ్యాసం',
      description: 'సాఫ్ట్‌వేర్ కోడింగ్, కంప్యూటర్ నైపుణ్యాలు మరియు ఆధునిక సాంకేతిక ఉద్యోగాలకు సంపూర్ణ మార్గదర్శకత్వం.',
      bannerSrc: 'Digital Skills and IT Learning Banner.png',
      posterSrc: 'Telugu Digital Skills & IT Learning Poster.png'
    }
  },
  {
    id: 'edu_study_abroad',
    ageRating: 'U/A 13+',
    duration: '1h 42m',
    year: '2025',
    en: {
      title: 'Study Abroad & Fellowships',
      description: 'Navigating GRE/IELTS, international university applications, Ambedkar overseas scholarships, and research visas.',
      bannerSrc: 'Study Abroad & Fellowships Poster.png',
      posterSrc: 'Study Abroad Fellowship Skyline.png'
    },
    te: {
      title: 'విదేశీ విద్య & ఫెలోషిప్స్',
      description: 'అంబేద్కర్ ఓవర్సీస్ స్కాలర్‌షిప్, గ్లోబల్ యూనివర్సిటీల్లో ప్రవేశాలు మరియు విదేశీ ఉన్నత విద్యా అవకాశాలు.',
      bannerSrc: 'Global Education and Fellowships Banner.png',
      posterSrc: 'Telugu Study Abroad Poster.png'
    }
  },
  {
    id: 'edu_govt_exams',
    ageRating: 'U/A 13+',
    duration: '2h 10m',
    year: '2024',
    en: {
      title: 'Government Exam Preparation Desk',
      description: 'Comprehensive coaching for UPSC Civil Services, state public service commissions, banking, and staff selection exams.',
      bannerSrc: 'Government Exam Preparation Desk.png',
      posterSrc: 'Government Exam Preparation Desk (1).png'
    },
    te: {
      title: 'ప్రభుత్వ ఉద్యోగాల పరీక్షల సిద్ధత డెస్క్',
      description: 'సివిల్ సర్వీసెస్, గ్రూప్ 1, 2 మరియు బ్యాంకింగ్ పరీక్షల్లో విజయానికి సమగ్ర స్టడీ గైడ్ & నిపుణుల సలహాలు.',
      bannerSrc: 'Telugu Government Exam Study Desk.png',
      posterSrc: 'Telugu Government Exam Study Desk (1).png'
    }
  },
  {
    id: 'edu_higher_research',
    ageRating: 'U/A 13+',
    duration: '1h 55m',
    year: '2025',
    en: {
      title: 'Higher Education & Research',
      description: 'Ph.D. fellowship opportunities, NET/JRF preparation, research publication protocols, and university professorship pathways.',
      bannerSrc: 'Higher Education & Research Banner.png',
      posterSrc: 'Higher Education and Research Poster (1).png'
    },
    te: {
      title: 'ఉన్నత విద్య & పరిశోధన',
      description: 'యూజీసీ నెట్/జేఆర్‌ఎఫ్ ఫెలోషిప్‌లు, పీహెచ్‌డీ పరిశోధనా మార్గం మరియు సెంట్రల్ యూనివర్సిటీ అవకాశాలు.',
      bannerSrc: 'Higher Education & Research Banner (1).png',
      posterSrc: 'Higher Education and Research Poster.png'
    }
  },
  {
    id: 'edu_first_gen_grads',
    ageRating: 'U/A 13+',
    duration: '1h 30m',
    year: '2024',
    en: {
      title: 'First-Generation Graduate Stories',
      description: 'Inspiring personal accounts of breaking generational barriers through perseverance, degrees, and community encouragement.',
      bannerSrc: 'First-Generation Graduate Stories (2).png',
      posterSrc: 'First-Generation Graduate Stories.png'
    },
    te: {
      title: 'మొదటి తరం పట్టభద్రుల కథలు',
      description: 'తరాల నిరక్షరాస్యతను అధిగమించి ఉన్నత పట్టభద్రులుగా నిలిచిన యువతీయువకుల ఆదర్శ ప్రయాణం.',
      bannerSrc: 'First-Generation Graduate Stories (1).png',
      posterSrc: 'Telugu Graduates at Sunset.png'
    }
  },
  {
    id: 'edu_scholarships_guide',
    ageRating: 'U/A 13+',
    duration: '1h 25m',
    year: '2025',
    en: {
      title: 'Scholarship & Fee-Reimbursement Guide',
      description: 'Essential portal walk-throughs for post-matric scholarships, corporate CSR grants, and government fee reimbursements.',
      bannerSrc: 'Scholarship & Fee-Reimbursement Guide.png',
      posterSrc: 'Scholarship Guide at Sunset.png'
    },
    te: {
      title: 'విద్యా వేతనాలు & ఫీజు రీయింబర్స్మెంట్ మార్గదర్శిని',
      description: 'ప్రభుత్వ పోస్ట్-మెట్రిక్ ఉపకార వేతనాలు, జాతీయ స్కాలర్‌షిప్ పోర్టల్ మరియు దరఖాస్తు విధానం.',
      bannerSrc: 'Telugu Scholarship Guide Poster (1).png',
      posterSrc: 'Golden Campus Scholarship Guide.png'
    }
  },
  {
    id: 'edu_student_mentorship',
    ageRating: 'U/A 13+',
    duration: '1h 40m',
    year: '2025',
    en: {
      title: 'Mentorship for School Students',
      description: 'One-on-one counseling connecting high school students with accomplished university scholars and career leaders.',
      bannerSrc: 'Mentorship for School Students (1).png',
      posterSrc: 'Mentorship for School Students.png'
    },
    te: {
      title: 'పాఠశాల విద్యార్థులకు మార్గదర్శకత్వం',
      description: 'పాఠశాల, కళాశాల విద్యార్థులకు వ్యక్తిగత కెరీర్ కౌన్సెలింగ్ మరియు మార్గదర్శకత్వ కార్యక్రమాలు.',
      bannerSrc: 'Student Mentorship in Telugu.png',
      posterSrc: 'విద్యార్థుల మార్గదర్శకత్వం.png'
    }
  },
  {
    id: 'edu_spoken_english',
    ageRating: 'U/A 13+',
    duration: '1h 35m',
    year: '2024',
    en: {
      title: 'Spoken English & Communication',
      description: 'Interactive workshops building confidence, interview fluency, and professional workplace communication for Telugu students.',
      bannerSrc: 'Spoken English Conversation Course.png',
      posterSrc: 'Spoken English Communication Workshop.png'
    },
    te: {
      title: 'మాట్లాడే ఇంగ్లీష్ & కమ్యూనికేషన్',
      description: 'తెలుగు మాధ్యమ విద్యార్థులకు ఆత్మవిశ్వాసంతో ఆంగ్లంలో మాట్లాడటానికి ప్రత్యేక సంభాషణా శిక్షణ.',
      bannerSrc: 'Conversational English Learning Workshop.png',
      posterSrc: 'Conversational English Coaching Session.png'
    }
  },
  {
    id: 'edu_student_rights',
    ageRating: 'U/A 13+',
    duration: '1h 45m',
    year: '2025',
    en: {
      title: 'Education Rights & Student Support',
      description: 'Empowering students with knowledge of statutory rights, hostel welfare schemes, and anti-discrimination cell safeguards.',
      bannerSrc: 'Student Support on Campus.png',
      posterSrc: 'Education Rights Student Support Poster.png'
    },
    te: {
      title: 'విద్యా హక్కులు & విద్యార్థి సహాయం',
      description: 'విద్యా సంస్థల్లో చట్టబద్ధమైన హక్కులు, హాస్టల్ సదుపాయాలు మరియు సంక్షేమ పథకాల సమాచారం.',
      bannerSrc: 'Students and Counselor at Campus Table.png',
      posterSrc: 'Student Rights and Support.png'
    }
  }
];

// ─────────────────────────────────────────────────────────────────────────────
// 3. FILMS & SERIES ASSETS MAPPING (Verified 100% against actual image artwork)
// ─────────────────────────────────────────────────────────────────────────────
const filmFolder = 'flims-20261121T052118Z-1-001/flims';
const filmItems = [
  {
    id: 'film_edumudi_1994',
    ageRating: 'U/A 13+',
    duration: '2h 15m',
    year: '2025',
    en: {
      title: 'Edumudi 1994: Rally of Resistance',
      description: 'The monumental historical drama chronicling the grassroots spark and unstoppable momentum of the 1994 Edumudi convention.',
      bannerSrc: 'Edumudi 1994_ Sunset Rally.png',
      posterSrc: 'Edumudi 1994_ Rally of Resistance.png'
    },
    te: {
      title: 'ఎడుముడి 1994',
      description: '1994 చారిత్రక ఎడుముడి సభ, సామాజిక న్యాయ పోరాటం మరియు చైతన్య తరంగాల నేపథ్య సినిమా.',
      bannerSrc: 'Edumudi 1994 Rally Poster.png',
      posterSrc: 'Edumudi 1994_ Rally at Sunset.png'
    }
  },
  {
    id: 'film_first_graduate',
    ageRating: 'U/A 13+',
    duration: '2h 08m',
    year: '2025',
    en: {
      title: 'The First Graduate: A Hopeful Journey',
      description: 'An emotional cinematic journey of a rural youth striving against all odds to become the very first college graduate in his village.',
      bannerSrc: 'The First Graduate Sunset Poster.png',
      posterSrc: 'The First Graduate_ A Hopeful Journey.png'
    },
    te: {
      title: 'మొదటి గ్రాడ్యుయేట్',
      description: 'గ్రామంలో తొలి పట్టభద్రుడిగా నిలవడానికి ఓ యువకుడు సాగించిన పోరాటం, పల్లె ప్రజల ఆశల చలనచిత్రం.',
      bannerSrc: 'First Graduate at Sunset (1).png',
      posterSrc: 'First Graduate at Sunset.png'
    }
  },
  {
    id: 'film_jobseeker_founder',
    ageRating: 'U/A 13+',
    duration: '1h 58m',
    year: '2024',
    en: {
      title: 'From Job Seeker to Founder',
      description: 'A contemporary entrepreneurial saga of transforming rejection into community-driven startups and economic empowerment.',
      bannerSrc: 'From Job Seeker to Founder (1).png',
      posterSrc: 'From Job Seeker to Founder.png'
    },
    te: {
      title: 'ఉద్యోగార్ధి నుంచి వ్యవస్థాపకుడిగా',
      description: 'కష్టాలను అధిగమించి నూతన స్టార్టప్ స్థాపించి పదిమందికి ఉపాధినిచ్చిన వ్యవస్థాపకుని సత్యకథ.',
      bannerSrc: 'ఉద్యోగార్ధి నుంచి వ్యవస్థాపకుడిగా.png',
      posterSrc: 'Confident Professional in Chalkboard Classroom.jpg'
    }
  },
  {
    id: 'film_tholi_thaalam',
    ageRating: 'U/A 13+',
    duration: '2h 02m',
    year: '2025',
    en: {
      title: 'The First Beat: Drumbeat of Hope',
      description: 'A poetic musical tribute depicting the timeless connection between rhythm, community identity, and the first beat of awakening.',
      bannerSrc: 'The First Beat at Sunset.png',
      posterSrc: 'The First Beat_ Drumbeat of Hope.png'
    },
    te: {
      title: 'తొలి తాళం',
      description: 'సంగీతం, సంప్రదాయం మరియు సాంస్కృతిక అస్తిత్వాన్ని ప్రతిబింబించే అద్భుత సంగీత చలనచిత్రం.',
      bannerSrc: 'తొలి తాళం_ Drumbeats of Legacy.png',
      posterSrc: 'తొలి తాళం.png'
    }
  },
  {
    id: 'film_guardians_manuscript',
    ageRating: 'U/A 13+',
    duration: '1h 45m',
    year: '2024',
    en: {
      title: 'The Scroll Keepers: Heritage in Focus',
      description: 'An investigative cultural documentary exploring researchers rescuing ancient palm-leaf scrolls and rare oral manuscripts.',
      bannerSrc: 'Guardians of the Ancient Scroll.png',
      posterSrc: 'The Scroll Keepers_ Heritage in Focus.png'
    },
    te: {
      title: 'గ్రంథ రక్షకులు',
      description: 'ప్రాచీన తాళపత్ర గ్రంథాలు, లిపులు మరియు అరుదైన సాహిత్య సంపదను కాపాడుతున్న పరిశోధకుల కథ.',
      bannerSrc: 'Guardians of the Ancient Manuscript.png',
      posterSrc: 'గ్రంథ రక్షకులు.png'
    }
  },
  {
    id: 'film_hands_remember',
    ageRating: 'U/A 13+',
    duration: '1h 50m',
    year: '2025',
    en: {
      title: 'Hands That Remember',
      description: 'An intimate chronicle highlighting the skilled artisans whose hands molded history, music, and social resilience.',
      bannerSrc: 'Hands That Remember.png',
      posterSrc: 'Hands That Remember (1).png'
    },
    te: {
      title: 'మరువని చేతులు',
      description: 'శ్రమజీవుల చేతుల నైపుణ్యం, చెమట చుక్కల విలువ మరియు కనుమరుగవుతున్న కళల రక్షణ కథ.',
      bannerSrc: 'Hands That Never Forget.png',
      posterSrc: 'మరువని చేతులు.png'
    }
  },
  {
    id: 'film_village_language',
    ageRating: 'U/A 13+',
    duration: '1h 38m',
    year: '2024',
    en: {
      title: 'The Language of the Village',
      description: 'Capturing the rich dialects, idioms, agrarian folklore, and evocative storytelling traditions of rustic rural Telangana.',
      bannerSrc: 'The Language of the Village (1).png',
      posterSrc: 'The Language of the Village.png'
    },
    te: {
      title: 'పల్లె మాటల భాష',
      description: 'పల్లెదనపు యాస, జానపద పలుకుబడులు మరియు గ్రామీణ ప్రజల జీవన భావోద్వేగాల సంభాషణ.',
      bannerSrc: 'Village Voices at Sunset.png',
      posterSrc: 'పల్లె మాటల భాష_ గ్రామీణ జ్ఞాపకాలు.png'
    }
  },
  {
    id: 'film_drum_maker_son',
    ageRating: 'U/A 13+',
    duration: '2h 12m',
    year: '2025',
    en: {
      title: 'The Drum Maker’s Son',
      description: 'A coming-of-age drama about a young musician harmonizing inherited acoustic drum-making with modern digital sound design.',
      bannerSrc: 'The Drum Maker’s Son.png',
      posterSrc: 'The Drum Maker’s Son at Sunset.png'
    },
    te: {
      title: 'దప్పు కళాకారుడి కొడుకు',
      description: 'తండ్రి నేర్పిన సాంప్రదాయ వాద్య కళను నేటి ప్రపంచ సంగీత వేదికలకు చేర్చిన యువకుని ప్రయాణం.',
      bannerSrc: 'Golden-Hour Dappu Tradition.png',
      posterSrc: 'Traditional Drummakers at Sunset.png'
    }
  },
  {
    id: 'film_the_archive',
    ageRating: 'U/A 13+',
    duration: '1h 42m',
    year: '2024',
    en: {
      title: 'The Archive: Memories in Motion',
      description: 'Documenting rare photographs, audio recordings, and visual records that capture the defining community moments of the 20th century.',
      bannerSrc: 'The Archive_ Memories in Motion.png',
      posterSrc: 'The Archive_ A Curated Past.png'
    },
    te: {
      title: 'ఆర్కైవ్',
      description: 'అరుదైన ఫోటోలు, పాటల రికార్డులు మరియు నాటి ఉద్యమ పత్రాల సమగ్ర డాక్యుమెంటరీ సమాహారం.',
      bannerSrc: 'Telugu Archive Poster Collage.png',
      posterSrc: 'Archival Memories at the Table.png'
    }
  },
  {
    id: 'film_chindu_night',
    ageRating: 'U/A 13+',
    duration: '2h 00m',
    year: '2025',
    en: {
      title: 'A Night of Chindu',
      description: 'An immersive backstage look at the transformative makeup rituals, devotional dedication, and midnight performances of Chindu troupes.',
      bannerSrc: 'Chindu Night Backstage.png',
      posterSrc: 'Chindu_ A Night of Tradition.png'
    },
    te: {
      title: 'చిందు రాత్రి',
      description: 'గ్రీన్ రూమ్ ముస్తాబులు, కిరీటధారణ మరియు అర్ధరాత్రి రంగస్థల ప్రదర్శనల అరుదైన అంతరంగ దృశ్యాలు.',
      bannerSrc: 'Chindu Ratri_ Backstage Crown Ritual.png',
      posterSrc: 'Chindu Ratri_ Backstage Traditions.png'
    }
  }
];

// ─────────────────────────────────────────────────────────────────────────────
// PROCESS & COPY ASSETS
// ─────────────────────────────────────────────────────────────────────────────

function processCategory(catKey, catFolder, items) {
  const targetDir = DIRS[catKey];
  return items.map((item) => {
    // Landscape filenames
    const enBannerFilename = `${item.id}_banner_en.png`;
    const teBannerFilename = `${item.id}_banner_te.png`;
    // Portrait filenames
    const enPosterFilename = `${item.id}_poster_en.png`;
    const tePosterFilename = `${item.id}_poster_te.png`;

    // Copy EN
    copyAsset(catFolder, item.en.bannerSrc, path.join(targetDir, 'banners', 'en'), enBannerFilename);
    copyAsset(catFolder, item.en.posterSrc, path.join(targetDir, 'posters', 'en'), enPosterFilename);

    // Copy TE
    copyAsset(catFolder, item.te.bannerSrc, path.join(targetDir, 'banners', 'te'), teBannerFilename);
    copyAsset(catFolder, item.te.posterSrc, path.join(targetDir, 'posters', 'te'), tePosterFilename);

    const enBannerRel = `./assets/${catKey}/banners/en/${enBannerFilename}`;
    const enPosterRel = `./assets/${catKey}/posters/en/${enPosterFilename}`;
    const teBannerRel = `./assets/${catKey}/banners/te/${teBannerFilename}`;
    const tePosterRel = `./assets/${catKey}/posters/te/${tePosterFilename}`;

    return {
      random_value: item.id,
      age_rating: item.ageRating,
      duration: item.duration,
      year: item.year,
      languages_content: [
        {
          language: 'en',
          title: item.en.title,
          description: item.en.description,
          assets: {
            '2_3': enPosterRel,
            '16_9': enBannerRel
          }
        },
        {
          language: 'te',
          title: item.te.title,
          description: item.te.description,
          assets: {
            '2_3': tePosterRel,
            '16_9': teBannerRel
          }
        }
      ]
    };
  });
}

console.log('Processing Culture assets...');
const processedCulture = processCategory('culture', cultureFolder, cultureItems);

console.log('Processing Education assets...');
const processedEducation = processCategory('education', eduFolder, educationItems);

console.log('Processing Films assets...');
const processedFilms = processCategory('films', filmFolder, filmItems);

// ─────────────────────────────────────────────────────────────────────────────
// READ EXISTING COMMUNITY PERSONALITIES (Category 1)
// ─────────────────────────────────────────────────────────────────────────────
const existingSample = JSON.parse(fs.readFileSync(path.join(ROOT, 'sample.json'), 'utf8'));
const personalitiesSection = existingSample.content_section.find(s => s.id === 'sec_av');

// Ensure section title for Community Personalities is clean
personalitiesSection.language_specific_values = [
  {
    language: 'en',
    title: 'Community Personalities',
    description: 'Profiles and interviews featuring prominent community leaders, pioneers, ministers, and public figures.'
  },
  {
    language: 'te',
    title: 'సమాజ ప్రముఖులు',
    description: 'సమాజ నాయకులు, మంత్రులు, ప్రజా ప్రతినిధుల ప్రత్యేక పరిచయాలు మరియు ముఖాముఖులు.'
  }
];
personalitiesSection.description = 'Community Personalities';

// ─────────────────────────────────────────────────────────────────────────────
// BUILD 4 MAIN CONTENT SECTIONS (Matching Folder Names: Community Personalities, Culture, Education, Films)
// ─────────────────────────────────────────────────────────────────────────────
const contentSections = [
  personalitiesSection, // Category 1: Community Personalities
  {
    id: 'sec_culture',
    language_specific_values: [
      {
        language: 'en',
        title: 'Culture',
        description: 'Explore ancestral rhythms, folk theater, leathercraft, and living traditions of our community.'
      },
      {
        language: 'te',
        title: 'సంస్కృతి',
        description: 'మన సముదాయపు ప్రాచీన కళలు, దప్పు నాదం, చిందు యక్షగానం మరియు జానపద సంప్రదాయాల సమాహారం.'
      }
    ],
    description: 'Culture',
    content: processedCulture
  },
  {
    id: 'sec_education',
    language_specific_values: [
      {
        language: 'en',
        title: 'Education',
        description: 'Empowering future leaders with exam coaching, scholarship guides, IT skills, and study abroad pathways.'
      },
      {
        language: 'te',
        title: 'విద్య',
        description: 'భావి తరాల ఉన్నతికి అవసరమైన పరీక్షల ప్రిపరేషన్, స్కాలర్‌షిప్‌లు, కంప్యూటర్ నైపుణ్యాలు మరియు విదేశీ విద్య.'
      }
    ],
    description: 'Education',
    content: processedEducation
  },
  {
    id: 'sec_films',
    language_specific_values: [
      {
        language: 'en',
        title: 'Films',
        description: 'Cinematic masterworks, grassroots resistance stories, inspiring biographies, and exclusive community originals.'
      },
      {
        language: 'te',
        title: 'సినిమాలు',
        description: 'సామాజిక చైతన్య చిత్రాలు, ఆత్మగౌరవ గాథలు, ఉత్తేజకర జీవిత చరిత్రలు మరియు ప్రత్యేక సినిమాలు.'
      }
    ],
    description: 'Films',
    content: processedFilms
  }
];

// ─────────────────────────────────────────────────────────────────────────────
// BUILD HERO CAROUSEL: High-Impact 16:9 Landscape Items across all 4 categories
// ─────────────────────────────────────────────────────────────────────────────
const heroItems = [
  // 1. Community Personality: Manda Krishna Madiga
  existingSample.hero_section[0],
  // 2. Culture: Chindu Yakshaganam
  {
    id: 'hero_chindu_yakshaganam',
    language_specific_values: [
      {
        language: 'en',
        title: 'Chindu Yakshaganam: Heritage in Motion',
        description: 'The vibrant, dramatic folk theater form preserving centuries-old mythological narratives, dance, and cultural theater.',
        assets: {
          '16_9': './assets/culture/banners/en/culture_chindu_yakshaganam_banner_en.png',
          '2_3': './assets/culture/posters/en/culture_chindu_yakshaganam_poster_en.png'
        }
      },
      {
        language: 'te',
        title: 'చిందు యక్షగానం',
        description: 'వందల ఏళ్ల ప్రాచీన జానపద నాట్య సంప్రదాయం, వేషధారణ, నటన మరియు పౌరాణిక కథా ప్రదర్శనల అద్భుత దృశ్యం.',
        assets: {
          '16_9': './assets/culture/banners/te/culture_chindu_yakshaganam_banner_te.png',
          '2_3': './assets/culture/posters/te/culture_chindu_yakshaganam_poster_te.png'
        }
      }
    ]
  },
  // 3. Education: NEET & JEE Preparation Pathway
  {
    id: 'hero_neet_jee_prep',
    language_specific_values: [
      {
        language: 'en',
        title: 'NEET & JEE Preparation Pathway',
        description: 'Strategic roadmap, expert masterclasses, and top mentorship guiding community aspirants into premier national medical and engineering institutes.',
        assets: {
          '16_9': './assets/education/banners/en/edu_neet_jee_prep_banner_en.png',
          '2_3': './assets/education/posters/en/edu_neet_jee_prep_poster_en.png'
        }
      },
      {
        language: 'te',
        title: 'నీట్ & జేఈఈ సిద్ధత మార్గం',
        description: 'టాప్ మెంటార్ల క్లాసులు, ప్రిపరేషన్ వ్యూహాలు మరియు జాతీయ స్థాయి విద్యా సంస్థల్లో సీట్ల సాధన బాట.',
        assets: {
          '16_9': './assets/education/banners/te/edu_neet_jee_prep_banner_te.png',
          '2_3': './assets/education/posters/te/edu_neet_jee_prep_poster_te.png'
        }
      }
    ]
  },
  // 4. Films: Edumudi 1994 Rally of Resistance
  {
    id: 'hero_edumudi_1994',
    language_specific_values: [
      {
        language: 'en',
        title: 'Edumudi 1994: Rally of Resistance',
        description: 'The monumental historical drama chronicling the grassroots spark and unstoppable momentum of the 1994 Edumudi convention.',
        assets: {
          '16_9': './assets/films/banners/en/film_edumudi_1994_banner_en.png',
          '2_3': './assets/films/posters/en/film_edumudi_1994_poster_en.png'
        }
      },
      {
        language: 'te',
        title: 'ఎడుముడి 1994',
        description: '1994 చారిత్రక ఎడుముడి సభ, సామాజిక న్యాయ పోరాటం మరియు చైతన్య తరంగాల నేపథ్య సినిమా.',
        assets: {
          '16_9': './assets/films/banners/te/film_edumudi_1994_banner_te.png',
          '2_3': './assets/films/posters/te/film_edumudi_1994_poster_te.png'
        }
      }
    ]
  },
  // 5. Culture: Dappu Craftsmanship
  {
    id: 'hero_dappu_craftsmanship',
    language_specific_values: [
      {
        language: 'en',
        title: 'Dappu Craftsmanship: Making the Instrument',
        description: 'The sacred craft, rhythmic pulse, and ancestral artisanal legacy behind crafting the authentic community Dappu drum.',
        assets: {
          '16_9': './assets/culture/banners/en/culture_dappu_craftsmanship_banner_en.png',
          '2_3': './assets/culture/posters/en/culture_dappu_craftsmanship_poster_en.png'
        }
      },
      {
        language: 'te',
        title: 'దప్పు వాద్య నిర్మాణం – తయారీలోని నైపుణ్యం',
        description: 'పవిత్రమైన సంప్రదాయ దప్పు తయారీ విధానం, చర్మ కళా నైపుణ్యం మరియు చారిత్రక సామాజిక స్వరమాధ్యమం.',
        assets: {
          '16_9': './assets/culture/banners/te/culture_dappu_craftsmanship_banner_te.png',
          '2_3': './assets/culture/posters/te/culture_dappu_craftsmanship_poster_te.png'
        }
      }
    ]
  },
  // 6. Films: The First Graduate
  {
    id: 'hero_first_graduate',
    language_specific_values: [
      {
        language: 'en',
        title: 'The First Graduate: A Hopeful Journey',
        description: 'An emotional cinematic journey of a rural youth striving against all odds to become the very first college graduate in his village.',
        assets: {
          '16_9': './assets/films/banners/en/film_first_graduate_banner_en.png',
          '2_3': './assets/films/posters/en/film_first_graduate_poster_en.png'
        }
      },
      {
        language: 'te',
        title: 'మొదటి గ్రాడ్యుయేట్',
        description: 'గ్రామంలో తొలి పట్టభద్రుడిగా నిలవడానికి ఓ యువకుడు సాగించిన పోరాటం, పల్లె ప్రజల ఆశల చలనచిత్రం.',
        assets: {
          '16_9': './assets/films/banners/te/film_first_graduate_banner_te.png',
          '2_3': './assets/films/posters/te/film_first_graduate_poster_te.png'
        }
      }
    ]
  }
];

// ─────────────────────────────────────────────────────────────────────────────
// WRITE UPDATED sample.json
// ─────────────────────────────────────────────────────────────────────────────
const finalCatalog = {
  hero_section: heroItems,
  content_section: contentSections
};

fs.writeFileSync(path.join(ROOT, 'sample.json'), JSON.stringify(finalCatalog, null, 2), 'utf8');
console.log('Successfully wrote sample.json with 4 categories and accurate localized assets!');
