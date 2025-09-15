import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

interface ApiEndpoint {
  method: string;
  path: string;
  description: string;
  parameters?: string[];
  example?: string;
  response?: string;
}

interface ApiService {
  name: string;
  description: string;
  baseUrl: string;
  endpoints: ApiEndpoint[];
}

@Component({
  selector: 'app-api-docs',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './api-docs.component.html',
  styleUrls: ['./api-docs.component.scss']
})
export class ApiDocsComponent {
  services: ApiService[] = [
    {
      name: 'AOC Timer Map API',
      description: 'Manage resource markers and named mob timers',
      baseUrl: '/api/map',
      endpoints: [
        {
          method: 'GET',
          path: '/api.php',
          description: 'Get all resource markers',
          example: 'curl -u user:pass /api.php',
          response: '{"markers": [{"id": 1, "x": 100, "y": 200, "type": "iron"}]}'
        },
        {
          method: 'POST',
          path: '/api.php',
          description: 'Create new resource marker',
          parameters: ['x (number)', 'y (number)', 'type (string)', 'respawn_time (number)'],
          example: 'curl -X POST -u user:pass -d "x=100&y=200&type=iron" /api.php'
        },
        {
          method: 'GET',
          path: '/named_mobs_api.php',
          description: 'Get all named mob timers',
          example: 'curl -u user:pass /named_mobs_api.php',
          response: '{"success": true, "data": [{"id": 1, "name": "Boss Name", "next_spawn": "2024-01-01T12:00:00Z"}]}'
        },
        {
          method: 'POST',
          path: '/named_mobs_api.php',
          description: 'Create named mob timer',
          parameters: ['mob_id (number)', 'killed_at (string)', 'notes (string)'],
          example: 'curl -X POST -u user:pass -d "mob_id=1&killed_at=now" /named_mobs_api.php'
        }
      ]
    },
    {
      name: 'Guild Sheets API',
      description: 'Guild management and member data',
      baseUrl: '/api/guild',
      endpoints: [
        {
          method: 'GET',
          path: '/members',
          description: 'Get guild member roster',
          example: 'curl -u user:pass /api/guild/members',
          response: '{"members": [{"id": 1, "name": "Player", "rank": "Officer", "level": 50}]}'
        },
        {
          method: 'GET',
          path: '/raids',
          description: 'Get upcoming raids',
          example: 'curl -u user:pass /api/guild/raids'
        }
      ]
    },
    {
      name: 'Vendor Trash API',
      description: 'Item pricing and vendor optimization',
      baseUrl: '/api/vendor',
      endpoints: [
        {
          method: 'GET',
          path: '/prices',
          description: 'Get current item prices',
          example: 'curl -u user:pass /api/vendor/prices'
        },
        {
          method: 'POST',
          path: '/calculate',
          description: 'Calculate optimal vendor route',
          parameters: ['items (array)', 'location (string)'],
          example: 'curl -X POST -u user:pass -d "items=[1,2,3]" /api/vendor/calculate'
        }
      ]
    }
  ];

  getMethodColor(method: string): string {
    switch (method.toUpperCase()) {
      case 'GET': return '#10b981';
      case 'POST': return '#3b82f6';
      case 'PUT': return '#f59e0b';
      case 'DELETE': return '#ef4444';
      default: return '#6b7280';
    }
  }

  goBack(): void {
    window.history.back();
  }
}
