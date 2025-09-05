import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Subject, interval, takeUntil } from 'rxjs';
import { NamedMobsService, NamedMob, NamedMobTimer } from '../shared/services/named-mobs.service';

@Component({
  selector: 'app-named-mobs',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './named-mobs.component.html',
  styleUrls: ['./named-mobs.component.scss']
})
export class NamedMobsComponent implements OnInit, OnDestroy {
  private destroy$ = new Subject<void>();

  namedMobs: NamedMob[] = [];
  activeTimers: NamedMobTimer[] = [];
  filteredMobs: NamedMob[] = [];
  
  searchQuery: string = '';
  selectedLevel: number | null = null;
  selectedServer: string = 'default';
  showOnlyActive: boolean = true;
  
  // Level filter options
  levelOptions = Array.from({length: 35}, (_, i) => i + 1);
  
  loading = false;

  constructor(private namedMobsService: NamedMobsService) {}

  ngOnInit() {
    this.loadNamedMobs();
    this.loadActiveTimers();
    
    // Update timers every minute
    interval(60000)
      .pipe(takeUntil(this.destroy$))
      .subscribe(() => {
        this.loadActiveTimers();
        this.updateTimerCountdowns();
      });
  }

  ngOnDestroy() {
    this.destroy$.next();
    this.destroy$.complete();
  }

  async loadNamedMobs() {
    this.loading = true;
    try {
      this.namedMobs = await this.namedMobsService.getAllNamedMobs(this.selectedLevel, this.searchQuery);
      this.filterMobs();
    } catch (error) {
      console.error('Failed to load named mobs:', error);
    } finally {
      this.loading = false;
    }
  }

  async loadActiveTimers() {
    try {
      this.activeTimers = await this.namedMobsService.getActiveTimers(this.selectedServer);
      this.updateTimerCountdowns();
    } catch (error) {
      console.error('Failed to load active timers:', error);
    }
  }

  filterMobs() {
    this.filteredMobs = this.namedMobs.filter(mob => {
      const matchesSearch = !this.searchQuery || 
        mob.name.toLowerCase().includes(this.searchQuery.toLowerCase());
      
      const matchesLevel = !this.selectedLevel || mob.level === this.selectedLevel;
      
      const hasActiveTimer = this.getActiveTimerForMob(mob.id!) !== null;
      const matchesActiveFilter = !this.showOnlyActive || hasActiveTimer;
      
      return matchesSearch && matchesLevel && matchesActiveFilter;
    });
  }

  getActiveTimerForMob(mobId: number): NamedMobTimer | null {
    return this.activeTimers.find(timer => timer.named_mob_id === mobId) || null;
  }

  onSearchChange() {
    this.loadNamedMobs();
  }

  onLevelChange() {
    this.loadNamedMobs();
  }

  onShowActiveChange() {
    this.filterMobs();
  }

  async startTimer(mob: NamedMob) {
    const killedAt = prompt('When was this mob killed? (YYYY-MM-DD HH:MM:SS or leave empty for now)', 
                            this.getCurrentDateTime());
    
    if (killedAt === null) return; // User cancelled
    
    const playerName = prompt('Player name (optional):');
    const notes = prompt('Notes (optional):');
    
    try {
      await this.namedMobsService.startTimer({
        named_mob_id: mob.id!,
        killed_at: killedAt || undefined,
        server: this.selectedServer,
        player_name: playerName || undefined,
        notes: notes || undefined
      });
      
      this.loadActiveTimers();
      this.filterMobs();
    } catch (error) {
      console.error('Failed to start timer:', error);
      alert('Failed to start timer. Please try again.');
    }
  }

  async deleteTimer(timer: NamedMobTimer) {
    if (!confirm(`Delete timer for ${timer.mob_name}?`)) return;
    
    try {
      await this.namedMobsService.deleteTimer(timer.id!);
      this.loadActiveTimers();
      this.filterMobs();
    } catch (error) {
      console.error('Failed to delete timer:', error);
      alert('Failed to delete timer. Please try again.');
    }
  }

  getTimerStatus(timer: NamedMobTimer): string {
    const minutesRemaining = timer.minutes_remaining || 0;
    
    if (minutesRemaining <= 0) {
      return 'SPAWNED';
    } else if (minutesRemaining <= 5) {
      return 'SOON';
    } else {
      return 'WAITING';
    }
  }

  getTimerStatusClass(timer: NamedMobTimer): string {
    const status = this.getTimerStatus(timer);
    return {
      'SPAWNED': 'status-spawned',
      'SOON': 'status-soon', 
      'WAITING': 'status-waiting'
    }[status] || 'status-waiting';
  }

  formatTimeRemaining(timer: NamedMobTimer): string {
    const minutesRemaining = timer.minutes_remaining || 0;
    
    if (minutesRemaining <= 0) {
      return 'READY TO SPAWN';
    }
    
    const hours = Math.floor(minutesRemaining / 60);
    const minutes = minutesRemaining % 60;
    
    if (hours > 0) {
      return `${hours}h ${minutes}m`;
    } else {
      return `${minutes}m`;
    }
  }

  openCodexLink(mob: NamedMob | NamedMobTimer) {
    const url = 'codex_url' in mob ? mob.codex_url : 
                'mob_name' in mob && this.namedMobs.find(m => m.id === mob.named_mob_id)?.codex_url;
    
    if (url) {
      window.open(url, '_blank');
    }
  }

  private getCurrentDateTime(): string {
    return new Date().toISOString().slice(0, 19).replace('T', ' ');
  }

  private updateTimerCountdowns() {
    // This will trigger change detection and update the displayed countdowns
    // The actual calculation is done in the template/methods
  }

  getLevelClass(level: number): string {
    if (level <= 10) return 'level-low';
    if (level <= 20) return 'level-medium';
    if (level <= 30) return 'level-high';
    return 'level-max';
  }

  async importNamedMobs() {
    if (!confirm('Import all named mobs from Ashes Codex? This will update existing data.')) return;
    
    this.loading = true;
    try {
      const result = await this.namedMobsService.importNamedMobs();
      alert(`Successfully imported ${result.imported} named mobs!`);
      this.loadNamedMobs();
    } catch (error) {
      console.error('Failed to import named mobs:', error);
      alert('Failed to import named mobs. Please try again.');
    } finally {
      this.loading = false;
    }
  }
}
