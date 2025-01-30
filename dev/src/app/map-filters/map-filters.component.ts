import { Component, inject, OnInit } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MapService } from '../shared/services/map.service';
import { FormControl, FormGroup, FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatSelectModule } from '@angular/material/select';
import { Rarity } from '../map/enums/rarity.enum';
import { debounceTime, distinctUntilChanged } from 'rxjs';
import { ButtonModule } from 'primeng/button';
import { MultiSelectModule } from 'primeng/multiselect';
import { TreeSelectModule } from 'primeng/treeselect';
import { CommonModule } from '@angular/common';
import { FiltersService } from '../shared/services/filters.service';
import { ResourceType } from '../map/enums/ressources';

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
    TreeSelectModule
  ],
  templateUrl: './map-filters.component.html',
  styleUrl: './map-filters.component.scss'
})
export class MapFiltersComponent implements OnInit {
  #mapService = inject(MapService);
  #filtersService = inject(FiltersService)
  initialFormData: any

  // Transform the enum into an array of objects
  // resources = Object.keys(RessourceImageLinks);
  rarities = Object.keys(Rarity);
  resourceOptions = this.#filtersService.getTreeResourceOptions();

  // Liste filtrée des ressources (initialisée avec toutes les ressources)

  // Form group with a multi-select control
  filterForm = new FormGroup({
    selectedResources: new FormControl([]), // Default: no selection
    selectedRarities: new FormControl([])
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

  onSubmit(): void {
    const selectedResources = this.getSelectedResources();
    const selectedRarities = this.getSelectedRarities();
    this.initialFormData = this.filterForm.value;
  
    // Filtrer les markers en fonction des ressources et des raretés sélectionnées
    const filteredMarkers = this.#mapService.markers.filter((marker) => {
      const customData = (marker as any).customData;
  
      // Si aucune ressource ou rareté n'est sélectionnée, ignorer ce filtre
      const matchesResource =
        selectedResources.length === 0 || selectedResources.includes(customData.type);
      const matchesRarity =
        selectedRarities.length === 0 || selectedRarities.includes(customData.rarity);
  
      return customData && matchesResource && matchesRarity;
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
