<template>
  <nav class="navbar">
    <div class="logo">
      <img 
        src="https://scontent.fmnl33-1.fna.fbcdn.net/v/t1.15752-9/474667107_1150394953328908_453092773794161443_n.png?_nc_cat=100&ccb=1-7&_nc_sid=9f807c&_nc_eui2=AeFtTV2Y3K0jKg0_2qV1Ho2xsF94E5Xqu6ewX3gTleq7pyQODnFyHMmvOYxLBKQlWA6rilKeyHQG2zaatLODHo2A&_nc_ohc=rpQ5djOAujEQ7kNvgHIFAZB&_nc_zt=23&_nc_ht=scontent.fmnl33-1.fna&oh=03_Q7cD1gF1ICi8zBFjshzJ24XNdz3oZT7SBQdxXjfFdQZv9Wfp3w&oe=67BFD3DF"
        alt="Rain's Cafe Logo">
    </div>   
  
    <div class="nav-links">
        <a href="/navbarbanner"><b>Home</b></a>
        <a href="#banner"><b>More</b></a>
        <a href="/gallery"><b>Gallery</b></a>
        <a href="/contact"><b>Contact</b></a>
        <div class="dropdown">
            <button class="dropbtn">
                <span class="dropdown-icon">&#x25BC;</span>
            </button>
            <div class="dropdown-content">
                <div class="dropdown-section">
                  <h4 class="dropdown-title">Menu</h4>
                  <a href="#menu1">Coffees</a>
                  <a href="#menu2">Pastries</a>
                  <a href="#menu3">Specials</a>
                </div>
                <div class="dropdown-section">
                  <h4 class="dropdown-title">Contact Us</h4>
                  <a href="#location">Our Location</a>
                  <a href="#support">Customer Support</a>
                </div>
                <div class="dropdown-section">
                  <h4 class="dropdown-title">Social</h4>
                  <a href="#facebook">Facebook</a>
                  <a href="#instagram">Instagram</a>
                  <a href="#twitter">Twitter</a>
                </div>
            </div>
        </div>
    </div> 
  </nav>

  <!-- Banner Section -->
  <header id="banner">
      <div id="banner-content" class="row clearfix">
          <div class="col-38">
              <div class="section-heading">
                  <h1>Steamed & Skilled</h1>
              </div>
          </div>
      </div>
  </header>

<div class="resume-container" data-aos="fade-up">
  <h2 class="tag">From Books to Bytes</h2>
  <div class="card" data-aos="fade-up">
      <i class="fas fa-university school-icon"></i>
      <div class="school-name">Asia Pacific College</div>
      <div class="year">2023-2027 (Ongoing)</div>
      <div class="honors">Honour Student (1st Year)</div>
      <div class="role">Secretariat Officer at Junior Information Systems Security Association</div>
  </div>

  <div class="card" data-aos="fade-up">
      <i class="fas fa-school school-icon"></i>
      <div class="school-name">AMA University</div>
      <div class="year">2022-2023</div>
      <div class="honors">Grade 12 (With High Honours)</div>
  </div>

  <div class="card" data-aos="fade-up">
      <i class="fas fa-graduation-cap school-icon"></i>
      <div class="school-name">FEU High School</div>
      <div class="year">2021-2022</div>
      <div class="honors">Grade 11 (With Honours)</div>
      <div class="role">Member of the Association of Young Accountants</div>
  </div>

  <div class="card" data-aos="fade-up">
      <i class="fas fa-users school-icon"></i>
      <div class="school-name">Starland International School</div>
      <div class="year">2018-2021</div>
      <div class="honors">Grade 8-10 (With High Honours)</div>
      <div class="role">Grade 10 Student Learners' Council President (VisMin Branch)</div>
  </div>

  <div class="card" data-aos="fade-up">
      <i class="fas fa-book school-icon"></i>
      <div class="school-name">Asian Learning Center</div>
      <div class="year">2017-2018</div>
      <div class="honors">Grade 7 (With High Honours)</div>
  </div>
</div>

<section class="skills-section">
    <h2 class="tag" data-aos="fade-up">Barista's Tools</h2>

    <div class="teapot-container" data-aos="fade-up">
      <div class="teapot" :class="{ tilt: isPouring }"></div>
      <div class="liquid" :class="{ pouring: isPouring }"></div>
    </div>

    <button class="pour-button" data-aos="fade-up" @click="restartAnimation">Click Me!</button>

    <div class="progress-wrapper" data-aos="fade-up">
      <div v-for="(skill, index) in skills" :key="index" class="skill-item">
        <div class="skill-category">{{ skill.category }}</div>
        <div class="progress-container">
          <div 
            class="progress-bar" 
            :style="{ width: skill.progress + '%' }"
          ></div>
          <span class="progress-text">{{ skill.progress }}%</span>
        </div>
      </div>
    </div>
  </section>

  <section class="profile-showcase" data-aos="fade-up">
  <h2 class="tag">Skillfolio ☕✨</h2>

  <div class="showcase-card">
  <div class="showcase-card-title">Leadership & Team Collaboration</div>
  <div class="showcase-card-content">
    <ul>
      <li>🔹 <strong>UI/UX Prototyping Lead</strong> – Co-led a team in designing an interactive Figma prototype, ensuring a seamless user experience with intuitive design principles.</li>
    </ul>
  </div>
</div>

<div class="showcase-card">
  <div class="showcase-card-title">Programming, Development, & Problem-Solving</div>
  <div class="showcase-card-content">
    <ul>
      <li>🔹 <strong>Financial Transaction Simulation</strong> – Developed a custom tool for managing deposits, withdrawals, and transfers, improving efficiency and record-keeping.</li>
    </ul>
  </div>
</div>

<div class="showcase-card">
  <div class="showcase-card-title">Content Creation & Digital Presence</div>
  <div class="showcase-card-content">
    <ul>
      <li>🔹 <strong>Client Content Creation</strong> – Produced engaging digital content to establish brand identity, enhancing audience engagement and online reach.</li>
      <li>🔹 <strong>Personal Content Creation</strong> – Growing as a beauty and makeup content creator on TikTok, experimenting with creative strategies to connect with audiences.</li>
    </ul>
  </div>
</div>

<div class="showcase-card">
  <div class="showcase-card-title">Academic & Educational Support</div>
  <div class="showcase-card-content">
    <ul>
      <li>🔹 <strong>Academic Writing & Tutoring</strong> – Skilled in structuring well-researched academic papers for high school and elementary levels. Also provides tutoring, especially in mathematics.</li>
    </ul>
  </div>
</div>

<div class="showcase-card">
  <div class="showcase-card-title">Administrative & Organizational Skills</div>
  <div class="showcase-card-content">
    <ul>
      <li>🔹 <strong>Administrative Support</strong> – Experienced in data entry, file organization, and calendar management to maintain efficient workflows.</li>
    </ul>
  </div>
</div>
</section>

<footer class="footer">
  <div class="footer-content">
    <p> 2025 Rain's Café. All rights reserved.</p>
    <div class="social-icons">
      <a href="#"><i class="fab fa-facebook"></i></a>
      <a href="#"><i class="fab fa-instagram"></i></a>
      <a href="#"><i class="fab fa-twitter"></i></a>
    </div>
  </div>
</footer>

</template>

<script>
export default {
  data() {
    return {
      isPouring: false,
      skills: [
        { category: "Programming (Python, JavaScript)", progress: 0, target: 80 },
        { category: "Web Development (HTML, CSS, Vue.js)", progress: 0, target: 75 },
        { category: "Development Tools (VS Code, GitHub, Vercel)", progress: 0, target: 70 },
        { category: "Databases (MySQL, Supabase, PostgreSQL, XAMPP)", progress: 0, target: 60 },
        { category: "UI/UX & Graphic Design (Canva, Figma)", progress: 0, target: 90 },
        { category: "Productivity Tools (Office 365, Google Suite)", progress: 0, target: 95 }
      ]
    };
  },
  methods: {
    restartAnimation() {
      this.isPouring = false;
      this.skills.forEach(skill => skill.progress = 0);

      setTimeout(() => {
        this.isPouring = true;
        this.fillProgressBars();
      }, 200);
    },

    fillProgressBars() {
      this.skills.forEach((skill, index) => {
        let progress = 0;
        const interval = setInterval(() => {
          if (progress < skill.target) {
            this.skills[index].progress = ++progress;
          } else {
            clearInterval(interval);
          }
        }, 20);
      });
    }
  }
}
</script>

<style></style>
