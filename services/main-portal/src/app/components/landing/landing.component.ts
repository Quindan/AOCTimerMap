import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

interface ServiceCard {
  title: string;
  description: string;
  icon: string;
  route: string;
  external?: boolean;
  status: 'active' | 'development' | 'planned';
  color: string;
}

@Component({
  selector: 'app-landing',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './landing.component.html',
  styleUrls: ['./landing.component.scss']
})
export class LandingComponent {
  currentYear = new Date().getFullYear();
  
  services: ServiceCard[] = [
    {
      title: 'AOC Timer Map',
      description: 'Interactive resource map with named mob timers. Track spawns, resources, and optimize your farming routes.',
      icon: 'fas fa-map-marked-alt',
      route: '/map',
      external: true,
      status: 'active',
      color: '#3b82f6'
    },
    {
      title: 'Guild Sheets',
      description: 'Comprehensive guild management. Member rosters, raid planning, resource tracking, and performance analytics.',
      icon: 'fas fa-users',
      route: '/guild',
      external: true,
      status: 'development',
      color: '#10b981'
    },
    {
      title: 'Vendor Trash Optimizer',
      description: 'Maximize your profits with real-time vendor pricing data. Calculate optimal trade routes and item values.',
      icon: 'fas fa-coins',
      route: '/vendor',
      external: true,
      status: 'planned',
      color: '#f59e0b'
    },
    {
      title: 'API Documentation',
      description: 'Complete API documentation for all InvictaWeb services. Integration guides and endpoint references.',
      icon: 'fas fa-code',
      route: '/api-docs',
      external: false,
      status: 'active',
      color: '#8b5cf6'
    }
  ];

  navigateTo(service: ServiceCard): void {
    if (service.external) {
      // These will be handled by nginx routing in production
      window.location.href = service.route;
    }
  }

  getStatusText(status: string): string {
    switch (status) {
      case 'active': return 'Live';
      case 'development': return 'Beta';
      case 'planned': return 'Coming Soon';
      default: return '';
    }
  }

  getStatusColor(status: string): string {
    switch (status) {
      case 'active': return '#10b981';
      case 'development': return '#f59e0b';
      case 'planned': return '#6b7280';
      default: return '#6b7280';
    }
  }
}
