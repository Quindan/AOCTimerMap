import { Component, DestroyRef, inject, OnInit, signal } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MapService } from '../shared/services/map.service';
import { FormControl, FormGroup, FormsModule, ReactiveFormsModule, Validators } from '@angular/forms';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatSelectModule } from '@angular/material/select';
import { Rarity } from '../map/enums/rarity.enum';
import { ButtonModule } from 'primeng/button';
import { MultiSelectModule } from 'primeng/multiselect';
import { TreeSelectModule } from 'primeng/treeselect';
import { CommonModule } from '@angular/common';
import { FiltersService } from '../shared/services/filters.service';
import { SidebarModule } from 'primeng/sidebar';
import { getUnixTime, intervalToDuration } from 'date-fns';
import { interval, tap } from 'rxjs';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';

@Component({
  selector: 'app-map-filters',
  imports: [
    CommonModule,
    FormsModule,
    ReactiveFormsModule,
    MatFormFieldModule,
    MatSelectModule,
    MatIconModule,
    MatButtonModule,
    ButtonModule,
    MultiSelectModule,
    TreeSelectModule,
    SidebarModule
  ],
  templateUrl: './map-filters.component.html',
  styleUrl: './map-filters.component.scss'
})
export class MapFiltersComponent implements OnInit {
  #mapService = inject(MapService);
  #filtersService = inject(FiltersService);
  #destroyRef = inject(DestroyRef);

  filtersOpen = signal(true);

  toggleFilters(): void {
    this.filtersOpen.set(!this.filtersOpen());
  }

  initialFormData: any

  // Transform the enum into an array of objects
  rarities = Object.keys(Rarity);
  resourceOptions = this.#filtersService.getTreeResourceOptions();
  respawns = [0, 15, 30, 60, 120, 180, 240];

  // Form group with a multi-select control
  filterForm = new FormGroup({
    selectedResources: new FormControl([]), // Default: no selection
    selectedRarities: new FormControl([]),
    selectedRespawnIn: new FormControl(0)
  });

  ngOnInit() {
    this.initialFormData = this.filterForm.value;
    this.onFormChanges().subscribe();
  }

  clearMarkers() {
    this.#mapService.clearAllMarkers();
  }

  // Method to get selected resources
  getSelectedResources(): string[] {
    return (this.filterForm.get('selectedResources')?.value || [])
    .map((resource: any) => resource.key);
  }

  getSelectedRarities(): string[] {
    return this.filterForm.get('selectedRarities')?.value || [];
  }

  getSelectedRespawnIn(): number {
    return this.filterForm.get('selectedRespawnIn')?.value || 0;
  }

  /*onSubmit(): void {
    this.#mapService.selectedResources = this.getSelectedResources();
    this.#mapService.selectedRarities  = this.getSelectedRarities();
    this.#mapService.selectedRespawnIn = this.getSelectedRespawnIn();
    this.initialFormData = this.filterForm.value;
  
    this.#mapService.showFilteredMap();
  }*/

  clearAllResources(): void {
    this.filterForm.get('selectedResources')?.setValue([]);
  }

  clearAllFilters(): void {
    this.filterForm.reset()
  }

  hasFormChanged(): boolean {
    //return JSON.stringify(this.filterForm.value) !== JSON.stringify(this.initialFormData);
    return true;
  }

  convertToReadableTime(minutes: number): string {
    const duration = intervalToDuration({ start: 0, end: minutes * 60 * 1000 });
  
    if (duration.hours) return `Moins de ${duration.hours} ${duration.hours > 1 ? 'heures' : 'heure'}`;
    return `Moins de ${minutes} minutes`;
  }

  onFormChanges() {
    return this.filterForm.valueChanges.pipe(
      tap(() => {
        this.#mapService.selectedResources = this.getSelectedResources();
        this.#mapService.selectedRarities  = this.getSelectedRarities();
        this.#mapService.selectedRespawnIn = this.getSelectedRespawnIn();
        this.initialFormData = this.filterForm.value;
      
        this.#mapService.showFilteredMap();
      }),
      takeUntilDestroyed(this.#destroyRef)
    )
  }
}
