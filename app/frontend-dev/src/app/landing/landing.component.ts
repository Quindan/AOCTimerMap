import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-landing',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="landing-container">
      <div class="container">
        <div class="header">
          <div class="logo-container">
            <img src="/assets/invicta-logo.png" alt="Invicta" class="invicta-logo" onerror="this.style.display='none'">
          </div>
          <h1>InvictaWeb - AOC Tools Hub</h1>
          <p>Comprehensive tools and resources for Ashes of Creation</p>
        </div>
        
        <div class="services-grid">
          <div class="service-card" (click)="goToMap()">
            <div class="service-icon">🗺️</div>
            <h3>AOC Timer Map</h3>
            <p>Interactive map with resource timers and named mob tracking</p>
            <div class="service-status">Active</div>
          </div>
          
          <div class="service-card" onclick="window.open('/bookstack', '_blank')">
            <div class="service-icon">📚</div>
            <h3>Wiki (BookStack)</h3>
            <p>Comprehensive guild knowledge base and documentation</p>
            <div class="service-status">Active</div>
          </div>
          
          <div class="service-card" onclick="window.open('https://docs.google.com/spreadsheets/d/1tFqrMoKayhYch5iZAhDSYn57Q94J85n0RCL4gYFbrbo/edit?gid=1293001695#gid=1293001695', '_blank')">
            <div class="service-icon">📊</div>
            <h3>Guild Sheet</h3>
            <p>Guild management and member tracking spreadsheet</p>
            <div class="service-status">External</div>
          </div>
          
          <div class="service-card" (click)="goToNamedMobs()">
            <div class="service-icon">⚔️</div>
            <h3>Named Mobs</h3>
            <p>Detailed named mob database with timers and drops</p>
            <div class="service-status">Active</div>
          </div>
        </div>
        
        <div class="footer">
          <p>Default Login: <strong>invicta / invicta</strong></p>
          <p>Version 0.6.2 | Powered by Invicta</p>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .landing-container {
      font-family: 'Roboto', sans-serif;
      background: linear-gradient(135deg, #2C1810 0%, #4A2C17 25%, #1A0F0A 50%, #2C1810 75%, #4A2C17 100%);
      background-size: 400% 400%;
      animation: gradientShift 15s ease infinite;
      min-height: 100vh;
      color: #E8E8E8;
      overflow-x: hidden;
    }
    
    @keyframes gradientShift {
      0% { background-position: 0% 50%; }
      50% { background-position: 100% 50%; }
      100% { background-position: 0% 50%; }
    }
    
    .container {
      max-width: 1200px;
      margin: 0 auto;
      padding: 20px;
    }
    
    .header {
      text-align: center;
      margin-bottom: 50px;
      padding-top: 50px;
    }
    
    .logo-container {
      margin-bottom: 20px;
    }
    
    .invicta-logo {
      max-width: 200px;
      height: auto;
      filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.3));
    }
    
    .header h1 {
      font-size: 3rem;
      font-weight: 700;
      background: linear-gradient(45deg, #C0C0C0, #E8E8E8);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
      text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
      margin-bottom: 10px;
    }
    
    .header p {
      font-size: 1.2rem;
      color: #B8B8B8;
      margin-bottom: 30px;
    }
    
    .services-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
      gap: 30px;
      margin-bottom: 50px;
    }
    
    .service-card {
      background: linear-gradient(145deg, rgba(139, 0, 0, 0.2), rgba(220, 20, 60, 0.1));
      border: 2px solid rgba(139, 0, 0, 0.3);
      border-radius: 15px;
      padding: 30px;
      text-align: center;
      transition: all 0.3s ease;
      backdrop-filter: blur(10px);
      cursor: pointer;
      position: relative;
      overflow: hidden;
    }
    
    .service-card:hover {
      transform: translateY(-10px);
      border-color: rgba(139, 0, 0, 0.6);
      background: linear-gradient(145deg, rgba(139, 0, 0, 0.3), rgba(220, 20, 60, 0.2));
    }
    
    .service-icon {
      font-size: 3rem;
      margin-bottom: 20px;
      filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.3));
    }
    
    .service-card h3 {
      font-size: 1.5rem;
      font-weight: 600;
      margin-bottom: 15px;
      color: #E8E8E8;
    }
    
    .service-card p {
      color: #B8B8B8;
      line-height: 1.6;
      margin-bottom: 20px;
    }
    
    .service-status {
      display: inline-block;
      padding: 5px 15px;
      border-radius: 20px;
      font-size: 0.9rem;
      font-weight: 500;
      background: rgba(0, 255, 0, 0.2);
      color: #90EE90;
      border: 1px solid rgba(0, 255, 0, 0.3);
    }
    
    .footer {
      text-align: center;
      padding: 30px 0;
      border-top: 1px solid rgba(139, 0, 0, 0.3);
      color: #B8B8B8;
    }
    
    .footer p {
      margin-bottom: 10px;
    }
  `]
})
export class LandingComponent {
  constructor(private router: Router) {}
  
  goToMap() {
    this.router.navigate(['/map']);
  }
  
  goToNamedMobs() {
    this.router.navigate(['/named-mobs']);
  }
}