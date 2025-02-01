import { Component, computed, inject, OnInit, signal } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MapService } from '../shared/services/map.service';
import { FormControl, FormGroup, FormsModule, ReactiveFormsModule, Validators } from '@angular/forms';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatSelectModule } from '@angular/material/select';
import { Rarity } from '../map/enums/rarity.enum';
import { debounceTime, distinctUntilChanged } from 'rxjs';
import { ButtonModule } from 'primeng/button';
import { MultiSelectModule } from 'primeng/multiselect';
import { TreeSelectModule } from 'primeng/treeselect';
import { CommonModule } from '@angular/common';
import { FiltersService } from '../shared/services/filters.service';
import { SidebarModule } from 'primeng/sidebar';
import moment from 'moment';

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

  filtersOpen = signal(true);

  toggleFilters(): void {
    this.filtersOpen.set(!this.filtersOpen());
  }

  initialFormData: any

  // Transform the enum into an array of objects
  // resources = Object.keys(RessourceImageLinks);
  rarities = Object.keys(Rarity);
  resourceOptions = this.#filtersService.getTreeResourceOptions();
  respawns = [0, 15, 30];

  // Liste filtrée des ressources (initialisée avec toutes les ressources)

  // Form group with a multi-select control
  filterForm = new FormGroup({
    selectedResources: new FormControl([]), // Default: no selection
    selectedRarities: new FormControl([]),
    selectedRespawnIn: new FormControl(0)
  });

  ngOnInit() {
    this.initialFormData = this.filterForm.value;
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

  onSubmit(): void {
    const now = moment().unix();
    const selectedResources = this.getSelectedResources();
    const selectedRarities  = this.getSelectedRarities();
    const selectedRespawnIn = this.getSelectedRespawnIn();
    this.initialFormData = this.filterForm.value;
  
    // Filtrer les markers en fonction des ressources et des raretés sélectionnées
    const filteredMarkers = this.#mapService.markers.filter((marker) => {
      const customData = (marker as any).customData;
  
      // Si aucune ressource ou rareté n'est sélectionnée, ignorer ce filtre
      const matchesResource =
        selectedResources.length === 0 || selectedResources.includes(customData.type);
      const matchesRarity =
        selectedRarities.length === 0 || selectedRarities.includes(customData.rarity);

      const respawnIn = customData.alarmAfter - now;
      const isRespawnInRange = respawnIn > 0 && respawnIn < (selectedRespawnIn * 60);
      const matchesRespawnIn =   
        selectedRespawnIn !== 0 && isRespawnInRange; // Converted in seconds

      return customData && matchesResource && matchesRarity && matchesRespawnIn;
    });
  
    // Ajouter les markers filtrés à la carte
    filteredMarkers.forEach((marker) => marker.addTo(this.#mapService.map));
  
    // Retirer les markers non filtrés de la carte
    this.#mapService.markers
      .filter((marker) => !filteredMarkers.includes(marker))
      .forEach((marker) => this.#mapService.map.removeLayer(marker));
  }

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

}
