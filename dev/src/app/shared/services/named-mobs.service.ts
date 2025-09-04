import { Injectable } from '@angular/core';
import { environment } from '../../../environments/environment';

export interface NamedMob {
  id?: number;
  name: string;
  slug: string;
  level: number;
  level_range: string;
  respawn_time: string;
  respawn_minutes: number;
  codex_url: string;
  location_x?: number;
  location_y?: number;
  location_z?: number;
  type: string;
  created_at?: string;
  updated_at?: string;
}

export interface NamedMobTimer {
  id?: number;
  named_mob_id: number;
  marker_id?: number;
  last_killed_at: string;
  respawn_at: string;
  server_name: string;
  notes?: string;
  player_name?: string;
  created_at?: string;
  updated_at?: string;
  
  // Joined fields from named_mobs table
  mob_name?: string;
  level?: number;
  respawn_minutes?: number;
  codex_url?: string;
  location_x?: number;
  location_y?: number;
  minutes_remaining?: number;
}

export interface StartTimerRequest {
  named_mob_id: number;
  killed_at?: string;
  server?: string;
  player_name?: string;
  notes?: string;
}

export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
  total?: number;
  imported?: number;
  timer_id?: number;
  respawn_at?: string;
  minutes_until_respawn?: number;
  server?: string;
}

@Injectable({
  providedIn: 'root'
})
export class NamedMobsService {
  private baseUrl = environment.apiUrl || '';

  constructor() {}

  async getAllNamedMobs(level?: number | null, search?: string): Promise<NamedMob[]> {
    const params = new URLSearchParams();
    if (level) params.append('level', level.toString());
    if (search) params.append('search', search);
    
    const url = `${this.baseUrl}/named_mobs_api.php?${params.toString()}`;
    const response = await fetch(url);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const result: ApiResponse<NamedMob[]> = await response.json();
    
    if (!result.success) {
      throw new Error(result.error || 'Failed to fetch named mobs');
    }
    
    return result.data || [];
  }

  async searchNamedMobs(query: string, level?: number): Promise<NamedMob[]> {
    const params = new URLSearchParams();
    params.append('q', query);
    if (level) params.append('level', level.toString());
    
    const url = `${this.baseUrl}/named_mobs_api.php/search?${params.toString()}`;
    const response = await fetch(url);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const result: ApiResponse<NamedMob[]> = await response.json();
    
    if (!result.success) {
      throw new Error(result.error || 'Failed to search named mobs');
    }
    
    return result.data || [];
  }

  async getNamedMob(id: number | string): Promise<NamedMob> {
    const url = `${this.baseUrl}/named_mobs_api.php/${id}`;
    const response = await fetch(url);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const result: ApiResponse<NamedMob> = await response.json();
    
    if (!result.success) {
      throw new Error(result.error || 'Failed to fetch named mob');
    }
    
    return result.data!;
  }

  async getActiveTimers(server: string = 'default'): Promise<NamedMobTimer[]> {
    const params = new URLSearchParams();
    params.append('server', server);
    
    const url = `${this.baseUrl}/named_mobs_api.php/timers?${params.toString()}`;
    const response = await fetch(url);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const result: ApiResponse<NamedMobTimer[]> = await response.json();
    
    if (!result.success) {
      throw new Error(result.error || 'Failed to fetch active timers');
    }
    
    return result.data || [];
  }

  async startTimer(request: StartTimerRequest): Promise<{
    timer_id: number;
    respawn_at: string;
    minutes_until_respawn: number;
  }> {
    const url = `${this.baseUrl}/named_mobs_api.php/timer`;
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        named_mob_id: request.named_mob_id,
        killed_at: request.killed_at,
        server: request.server || 'default',
        player_name: request.player_name,
        notes: request.notes
      })
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const result: ApiResponse<any> = await response.json();
    
    if (!result.success) {
      throw new Error(result.error || 'Failed to start timer');
    }
    
    return {
      timer_id: result.timer_id!,
      respawn_at: result.respawn_at!,
      minutes_until_respawn: result.minutes_until_respawn!
    };
  }

  async updateTimer(timerId: number, updates: {
    notes?: string;
    player_name?: string;
  }): Promise<void> {
    const url = `${this.baseUrl}/named_mobs_api.php/timer`;
    const response = await fetch(url, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        timer_id: timerId,
        ...updates
      })
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const result: ApiResponse<any> = await response.json();
    
    if (!result.success) {
      throw new Error(result.error || 'Failed to update timer');
    }
  }

  async deleteTimer(timerId: number): Promise<void> {
    const url = `${this.baseUrl}/named_mobs_api.php/timer?timer_id=${timerId}`;
    const response = await fetch(url, {
      method: 'DELETE'
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const result: ApiResponse<any> = await response.json();
    
    if (!result.success) {
      throw new Error(result.error || 'Failed to delete timer');
    }
  }

  async importNamedMobs(): Promise<{
    imported: number;
    total_mobs: number;
    message: string;
  }> {
    const url = `${this.baseUrl}/named_mobs_api.php/import`;
    const response = await fetch(url, {
      method: 'POST'
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const result: ApiResponse<any> = await response.json();
    
    if (!result.success) {
      throw new Error(result.error || 'Failed to import named mobs');
    }
    
    return {
      imported: result.imported!,
      total_mobs: result.total_mobs || 0,
      message: result.message!
    };
  }
}
