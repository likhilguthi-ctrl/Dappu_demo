const fs = require('fs');
const path = require('path');

const samplePath = path.join(__dirname, '..', 'sample.json');
const data = JSON.parse(fs.readFileSync(samplePath, 'utf8'));

const secEducation = data.content_section.find(sec => sec.id === 'sec_education');
if (!secEducation) {
  console.error('sec_education not found');
  process.exit(1);
}

const newItems = [
  {
    random_value: 'item_edu_gogu_shyamala',
    age_rating: 'U/A 13+',
    duration: '48m',
    year: '2024',
    languages_content: [
      {
        language: 'en',
        title: 'The Voice of Madiga Women: Gogu Shyamala',
        description: 'Acclaimed Dalit feminist thinker and author Gogu Shyamala highlights rural Madiga women’s resistance, lived oral narratives, and cultural emancipation.',
        assets: {
          '2_3': './assets/madiga/posters/en/education_1.jpg',
          '16_9': './assets/madiga/banners/en/education_1_banner.jpg'
        }
      },
      {
        language: 'te',
        title: 'మాదిగ మహిళల గొంతుకగా... గోగు శ్యామల పోరాటం',
        description: 'దళిత స్త్రీవాద రచయిత్రి, ఉద్యమ వైతాళికురాలు గోగు శ్యామల మాదిగ మహిళల ఆత్మగౌరవం, సాహిత్యం మరియు హక్కుల పోరాటం.',
        assets: {
          '2_3': './assets/madiga/posters/te/education_1.jpg',
          '16_9': './assets/madiga/banners/te/education_1_banner.jpg'
        }
      }
    ]
  },
  {
    random_value: 'item_edu_endluri_sudhakar',
    age_rating: 'U/A 13+',
    duration: '55m',
    year: '2024',
    languages_content: [
      {
        language: 'en',
        title: 'A New Voice for Dalit Literature: Prof. Endluri Sudhakar',
        description: 'Celebrating the monumental legacy of Prof. Endluri Sudhakar, whose pioneering poetry, research, and voice awakened Dalit consciousness across generations.',
        assets: {
          '2_3': './assets/madiga/posters/en/education_2.jpg',
          '16_9': './assets/madiga/banners/en/education_2_banner.jpg'
        }
      },
      {
        language: 'te',
        title: 'దళిత సాహిత్యానికి కొత్త గొంతుక! ఎండ్లూరి సుధాకర్',
        description: 'దళిత సాహిత్య వైతాళికుడు ప్రొఫెసర్ ఎండ్లూరి సుధాకర్ కవిత్వ సంపుటాలు, చారిత్రక పరిశోధనలు మరియు నూతన సాహిత్య ప్రస్థానం.',
        assets: {
          '2_3': './assets/madiga/posters/te/education_2.jpg',
          '16_9': './assets/madiga/banners/te/education_2_banner.jpg'
        }
      }
    ]
  }
];

// Prepend the new items if not already present
const existingIds = (secEducation.content || []).map(c => c.random_value);
const filteredNew = newItems.filter(item => !existingIds.includes(item.random_value));

secEducation.content = [...filteredNew, ...(secEducation.content || [])];

fs.writeFileSync(samplePath, JSON.stringify(data, null, 2), 'utf8');
console.log('Successfully updated sec_education in sample.json. Total items:', secEducation.content.length);
