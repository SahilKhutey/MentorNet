const { faker } = require("@faker-js/faker");
const fs = require("fs");

const NUM_MENTORS = 10000;
const NUM_STUDENTS = 10000;

// -------------------- DATA POOLS --------------------

const domains = [
  "Software Engineering",
  "Data Science",
  "AI/ML",
  "Product Management",
  "UI/UX Design",
  "Finance",
  "Marketing",
  "Cybersecurity",
  "HR",
];

const skillsMap = {
  "Software Engineering": ["React", "Node.js", "System Design", "Java", "AWS"],
  "Data Science": ["Python", "Pandas", "ML", "Statistics"],
  "AI/ML": ["Deep Learning", "NLP", "Transformers", "TensorFlow"],
  "Product Management": ["Roadmaps", "Analytics", "Agile", "UX"],
  "UI/UX Design": ["Figma", "Wireframing", "User Research"],
  Finance: ["Stocks", "Valuation", "Excel"],
  Marketing: ["SEO", "Content", "Ads"],
  Cybersecurity: ["Ethical Hacking", "Network Security"],
  HR: ["Recruitment", "Soft Skills"],
};

const companies = [
  "Google",
  "Amazon",
  "Microsoft",
  "Flipkart",
  "Zomato",
  "Infosys",
  "TCS",
  "Startup",
];

const education = [
  "B.Tech IIT",
  "M.Tech IIT",
  "MBA IIM",
  "B.Des NID",
  "B.Tech NIT",
  "Self-Taught",
];

const availabilityOptions = ["Weekends", "Evenings", "Flexible"];

const languagesList = ["English", "Hindi", "English,Hindi"];

// -------------------- HELPERS --------------------

function getRandom(arr) {
  return arr[Math.floor(Math.random() * arr.length)];
}

function getSkills(domain) {
  return skillsMap[domain]
    .sort(() => 0.5 - Math.random())
    .slice(0, 3)
    .join("|"); // Using pipe to avoid CSV confusion
}

// -------------------- GENERATORS --------------------

function generateMentor(id) {
  const domain = getRandom(domains);

  return {
    id,
    name: faker.person.fullName(),
    role: "Mentor",
    experience_years: faker.number.int({ min: 3, max: 20 }),
    domain,
    skills: getSkills(domain),
    company: getRandom(companies),
    designation: faker.person.jobTitle(),
    location: faker.location.city(),
    country: "India",
    education: getRandom(education),
    availability: getRandom(availabilityOptions),
    price_per_hour: faker.number.int({ min: 15, max: 120 }),
    rating: (Math.random() * (5 - 4.2) + 4.2).toFixed(1),
    total_sessions: faker.number.int({ min: 20, max: 500 }),
    languages: getRandom(languagesList),
    bio: faker.lorem.sentence(),
    linkedin: `https://linkedin.com/in/${faker.internet.username()}`,
    verified: Math.random() > 0.3,
    profile_image: `https://i.pravatar.cc/150?img=${id % 70}`,
  };
}

function generateStudent(id) {
  const domain = getRandom(domains);

  return {
    id,
    name: faker.person.fullName(),
    role: "Student",
    current_level: getRandom(["Beginner", "Intermediate", "Advanced"]),
    target_domain: domain,
    interests: getSkills(domain),
    current_skills: getSkills(domain),
    experience_years: faker.number.int({ min: 0, max: 5 }),
    education: getRandom(["B.Tech", "BCA", "MBA", "Student"]),
    location: faker.location.city(),
    country: "India",
    goals: faker.lorem.sentence(),
    preferred_availability: getRandom(availabilityOptions),
    budget_per_hour: faker.number.int({ min: 5, max: 50 }),
    languages: getRandom(languagesList),
    linkedin: `https://linkedin.com/in/${faker.internet.username()}`,
    profile_image: `https://i.pravatar.cc/150?img=${(id + 30) % 70}`,
  };
}

// -------------------- CSV WRITER --------------------

function toCSV(data) {
  const headers = Object.keys(data[0]);
  const rows = data.map((obj) =>
    headers.map((h) => `"${String(obj[h]).replace(/"/g, '""')}"`).join(","),
  );
  return [headers.join(","), ...rows].join("\n");
}

// -------------------- GENERATE DATA --------------------

console.log("Generating mentors...");
const mentors = Array.from({ length: NUM_MENTORS }, (_, i) =>
  generateMentor(i + 1),
);

console.log("Generating students...");
const students = Array.from({ length: NUM_STUDENTS }, (_, i) =>
  generateStudent(i + 1),
);

// -------------------- SAVE FILES --------------------

fs.writeFileSync("mentors.csv", toCSV(mentors));
fs.writeFileSync("students.csv", toCSV(students));

console.log("✅ Data generated:");
console.log("mentors.csv (10K)");
console.log("students.csv (10K)");
