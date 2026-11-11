const fs = require('fs');

const data = JSON.parse(fs.readFileSync('./sample.json', 'utf8'));

// 1. Update sec_songs
const secSongs = data.content_section.find(s => s.id === 'sec_songs');
if (secSongs) {
  secSongs.language_specific_values = [
    {
      language: 'en',
      title: 'Songs',
      description: 'Soulful folk melodies, revolutionary songs, and rhythm of the Dappu celebrating Dalit and Madiga heritage.'
    },
    {
      language: 'te',
      title: 'పాటలు',
      description: 'దళిత, మాదిగ సాంస్కృతిక వారసత్వాన్ని, డప్పు దరువులను మరియు పోరాట స్ఫూర్తిని కీర్తించే జానపద, విప్లవ గీతాలు.'
    }
  ];

  secSongs.content = [
    {
      random_value: 'item_song_1',
      age_rating: 'U',
      duration: '4m 12s',
      year: '2024',
      languages_content: [
        {
          language: 'en',
          title: 'Comrade Dappu Ramesh Tribute Song',
          description: 'In memory of Comrade Dappu Ramesh: Iconic JNM & CNM revolutionary folk anthem celebrating people’s resistance and cultural heritage.',
          assets: {
            '2_3': './assets/madiga/posters/en/song_1.jpg',
            '16_9': './assets/madiga/banners/en/song_1_banner.jpg'
          }
        },
        {
          language: 'te',
          title: 'అమరుడు కామ్రేడ్ డప్పు రమేష్ అన్న స్మృతి లో',
          description: 'అమరుడు కామ్రేడ్ డప్పు రమేష్ అన్న స్మృతి లో జేఎన్‌ఎం, సీఎన్‌ఎం సమర్పించిన సుప్రసిద్ధ ప్రజా విప్లవ పోరాట గీతం.',
          assets: {
            '2_3': './assets/madiga/posters/te/song_1.jpg',
            '16_9': './assets/madiga/banners/te/song_1_banner.jpg'
          }
        }
      ]
    },
    {
      random_value: 'item_song_2',
      age_rating: 'U',
      duration: '5m 28s',
      year: '2023',
      languages_content: [
        {
          language: 'en',
          title: 'O Red Flag, Red Salutes to You',
          description: 'A powerful, fiery revolutionary anthem dedicated to the red flag and grassroots martyrs by Janavani cultural wing.',
          assets: {
            '2_3': './assets/madiga/posters/en/song_2.jpg',
            '16_9': './assets/madiga/banners/en/song_2_banner.jpg'
          }
        },
        {
          language: 'te',
          title: 'ఓ అరుణ పతాకమా నీకివిగో రెడ్ సెల్యూట్స్',
          description: 'రక్తసిక్త ఎర్రజెండాకు, ఉద్యమ అమరవీరులకు సమర్పించిన ఉద్వేగభరిత విప్లవ నివాళి గీతం.',
          assets: {
            '2_3': './assets/madiga/posters/te/song_2.jpg',
            '16_9': './assets/madiga/banners/te/song_2_banner.jpg'
          }
        }
      ]
    },
    {
      random_value: 'item_song_3',
      age_rating: 'U',
      duration: '3m 45s',
      year: '2024',
      languages_content: [
        {
          language: 'en',
          title: 'Madiga Dandora Cultural Troupe',
          description: 'The roaring rhythm of Dappu and Daruvu: vibrant community celebration of indigenous folk drums and Telangana rhythms.',
          assets: {
            '2_3': './assets/madiga/posters/en/song_3.jpg',
            '16_9': './assets/madiga/banners/en/song_3_banner.jpg'
          }
        },
        {
          language: 'te',
          title: 'మాదిగ దండోరా దళం - డప్పు, దరువు, సప్పుడు',
          description: 'మాదిగ దండోరా కళాకారుల డప్పు దరువు, శ్రామిక జన చప్పుడు మరియు సంస్కృతి ఉత్సవం.',
          assets: {
            '2_3': './assets/madiga/posters/te/song_3.jpg',
            '16_9': './assets/madiga/banners/te/song_3_banner.jpg'
          }
        }
      ]
    },
    {
      random_value: 'item_song_4',
      age_rating: 'U',
      duration: '4m 50s',
      year: '2024',
      languages_content: [
        {
          language: 'en',
          title: 'Aadudam Dappulo Daruveyyara',
          description: 'High-energy folk dance track bringing the stage alive with the thunderous resonance of Telangana daph drums.',
          assets: {
            '2_3': './assets/madiga/posters/en/song_4.jpg',
            '16_9': './assets/madiga/banners/en/song_4_banner.jpg'
          }
        },
        {
          language: 'te',
          title: 'ఆడుదాం డప్పులో దరువెయ్యరా... (జానపద గీతం)',
          description: 'వేదికను హోరెత్తించే డప్పు దరువుల జానపద నృత్య గీతం, శ్రామిక జన ఉత్సాహం.',
          assets: {
            '2_3': './assets/madiga/posters/te/song_4.jpg',
            '16_9': './assets/madiga/banners/te/song_4_banner.jpg'
          }
        }
      ]
    },
    {
      random_value: 'item_song_5',
      age_rating: 'U/A 13+',
      duration: '5m 15s',
      year: '2024',
      languages_content: [
        {
          language: 'en',
          title: 'Dalitha Pululamma - Tigers of Resistance',
          description: 'Martyrs memorial anthem honoring the brave souls of the Dalit resistance movement at Rudhirakshetram.',
          assets: {
            '2_3': './assets/madiga/posters/en/song_5.jpg',
            '16_9': './assets/madiga/banners/en/song_5_banner.jpg'
          }
        },
        {
          language: 'te',
          title: 'దళిత పులులమ్మా (రుధిరక్షేత్రం స్మృతి గీతం)',
          description: 'రుధిరక్షేత్రం అమరుల స్మృతిలో దళిత ప్రతిఘటన పోరాట వీరులను స్మరించుకునే స్ఫూర్తిదాయక గీతం.',
          assets: {
            '2_3': './assets/madiga/posters/te/song_5.jpg',
            '16_9': './assets/madiga/banners/te/song_5_banner.jpg'
          }
        }
      ]
    }
  ];
}

// 2. Update sec_podcast
const secPodcast = data.content_section.find(s => s.id === 'sec_podcast');
if (secPodcast) {
  secPodcast.language_specific_values = [
    {
      language: 'en',
      title: 'Podcasts & Interviews',
      description: 'Exclusive in-depth studio podcast conversations with key architects and leaders of the Madiga movement.'
    },
    {
      language: 'te',
      title: 'పాడ్‌కాస్ట్‌లు & ముఖాముఖులు',
      description: 'ఎమ్మార్పీఎస్ ఉద్యమ నిర్మాతలు, దళిత నాయకులతో ప్రత్యేక సమగ్ర స్టూడియో సంభాషణలు మరియు ముఖాముఖులు.'
    }
  ];

  secPodcast.content = [
    {
      random_value: 'item_podcast_1',
      age_rating: 'U',
      duration: '42m 18s',
      year: '2024',
      languages_content: [
        {
          language: 'en',
          title: '1994 – The Genesis of MRPS | Dandu Veerayya Madiga',
          description: 'In-depth historical discussion with Dandu Veerayya Madiga on the seminal founding moments, ideology, and launch of MRPS in 1994.',
          assets: {
            '2_3': './assets/madiga/posters/en/podcast_1.jpg',
            '16_9': './assets/madiga/banners/en/podcast_1_banner.jpg'
          }
        },
        {
          language: 'te',
          title: '1994 – ఎమ్మార్పీఎస్ ఆవిర్భావం! | దండు వీరయ్య మాదిగ',
          description: '1994లో ఎమ్మార్పీఎస్ చారిత్రక ఆవిర్భావం, సైద్ధాంతిక పునాదులు మరియు తొలి ఉద్యమ ప్రస్థానంపై దండు వీరయ్య మాదిగతో సమగ్ర సంభాషణ.',
          assets: {
            '2_3': './assets/madiga/posters/te/podcast_1.jpg',
            '16_9': './assets/madiga/banners/te/podcast_1_banner.jpg'
          }
        }
      ]
    },
    {
      random_value: 'item_podcast_2',
      age_rating: 'U',
      duration: '38m 45s',
      year: '2024',
      languages_content: [
        {
          language: 'en',
          title: 'The Untold Story Behind Madiga Corporation | Kommuri Kanakarao Madiga',
          description: 'Kommuri Kanakarao Madiga takes us backstage through the policy battles, administrative negotiations, and vision that established the Madiga Corporation.',
          assets: {
            '2_3': './assets/madiga/posters/en/podcast_2.jpg',
            '16_9': './assets/madiga/banners/en/podcast_2_banner.jpg'
          }
        },
        {
          language: 'te',
          title: 'మాదిగ కార్పొరేషన్ వెనుక అసలు కథ! | కొమ్మూరి కనకారావు మాదిగ',
          description: 'మాదిగ కార్పొరేషన్ ఏర్పాటు వెనుక జరిగిన తెరవెనుక పోరాటాలు, విధాన నిర్ణయాలు మరియు కార్యాచరణపై కొమ్మూరి కనకారావు మాదిగ ప్రత్యేక విశ్లేషణ.',
          assets: {
            '2_3': './assets/madiga/posters/te/podcast_2.jpg',
            '16_9': './assets/madiga/banners/te/podcast_2_banner.jpg'
          }
        }
      ]
    },
    {
      random_value: 'item_podcast_3',
      age_rating: 'U',
      duration: '45m 10s',
      year: '2024',
      languages_content: [
        {
          language: 'en',
          title: 'How Was MRPS Formed in 1994? | Krupakar Madiga',
          description: 'Founding recollections, crucial mobilization rallies, and grassroots organizing secrets revealed by leader Krupakar Madiga.',
          assets: {
            '2_3': './assets/madiga/posters/en/podcast_3.jpg',
            '16_9': './assets/madiga/banners/en/podcast_3_banner.jpg'
          }
        },
        {
          language: 'te',
          title: '1994లో ఎమ్మార్పీఎస్ ఎలా ఏర్పడింది? | కృపాకర్ మాదిగ',
          description: '1994లో ఉద్యమ పునాది పడిన రోజులు, సభలు, ప్రజల్లోకి ఉద్యమాన్ని తీసుకువెళ్లిన వ్యూహాలపై కృపాకర్ మాదిగ ప్రత్యక్ష అనుభవాలు.',
          assets: {
            '2_3': './assets/madiga/posters/te/podcast_3.jpg',
            '16_9': './assets/madiga/banners/te/podcast_3_banner.jpg'
          }
        }
      ]
    },
    {
      random_value: 'item_podcast_4',
      age_rating: 'U',
      duration: '51m 30s',
      year: '2024',
      languages_content: [
        {
          language: 'en',
          title: 'A Movement\'s History in Song | Dappu Ramesh',
          description: 'Legendary cultural pioneer Dappu Ramesh shares how song, rhythm, and poetry sustained the heartbeat of the people\'s struggle for generations.',
          assets: {
            '2_3': './assets/madiga/posters/en/podcast_4.jpg',
            '16_9': './assets/madiga/banners/en/podcast_4_banner.jpg'
          }
        },
        {
          language: 'te',
          title: 'ఆ పాటలో ఒక ఉద్యమ చరిత్ర ఉంది! | డప్పు రమేష్',
          description: 'సంగీతం, కవిత్వం, డప్పు దరువు ఎలా ఉద్యమానికి జీవనాడిగా నిలిచాయో వివరించిన ప్రముఖ సాంస్కృతిక సారథి డప్పు రమేష్ అంతరంగం.',
          assets: {
            '2_3': './assets/madiga/posters/te/podcast_4.jpg',
            '16_9': './assets/madiga/banners/te/podcast_4_banner.jpg'
          }
        }
      ]
    },
    {
      random_value: 'item_podcast_5',
      age_rating: 'U',
      duration: '58m 20s',
      year: '2024',
      languages_content: [
        {
          language: 'en',
          title: 'The Relentless Struggle for Rights | Manda Krishna Madiga',
          description: 'A flagship exclusive interview with Manda Krishna Madiga on three decades of mobilization, SC classification battles, and future vision.',
          assets: {
            '2_3': './assets/madiga/posters/en/podcast_5.jpg',
            '16_9': './assets/madiga/banners/en/podcast_5_banner.jpg'
          }
        },
        {
          language: 'te',
          title: 'మాదిగల హక్కుల కోసం అలుపెరగని పోరాటం! | మంద కృష్ణ మాదిగ',
          description: 'మూడు దశాబ్దాల ఉద్యమ ప్రస్థానం, ఎస్సీ వర్గీకరణ పోరు మరియు జాతి ఆత్మగౌరవ దిశపై మంద కృష్ణ మాదిగతో ప్రత్యేక ముఖాముఖి.',
          assets: {
            '2_3': './assets/madiga/posters/te/podcast_5.jpg',
            '16_9': './assets/madiga/banners/te/podcast_5_banner.jpg'
          }
        }
      ]
    }
  ];
}

fs.writeFileSync('./sample.json', JSON.stringify(data, null, 2), 'utf8');
console.log('sample.json updated successfully with 5 Songs and 5 Podcasts!');
