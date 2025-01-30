import { Injectable } from '@angular/core';
import { RESOURCE_CATEGORIES } from '../../map/enums/ressources';

@Injectable({
  providedIn: 'root'
})
export class FiltersService {

  constructor() { }

  getRessourceOptions() {
    return Object.entries(RESOURCE_CATEGORIES).map(([category, resources]) => ({
      label: category,
      items: Object.entries(resources).map(([key, value]) => ({
        label: key,
        value: value
      }))
    }));
  }

  getTreeResourceOptions(): any[] {
    return Object.entries(RESOURCE_CATEGORIES).map(([category, resources]) => ({
      label: this.capitalizeFirstLetter(category), // Convertit 'wood' en 'Wood'
      key: category, 
      selectable: false, // Empêche la sélection des catégories
      children: Object.entries(resources).map(([resourceKey, resourcePath]) => ({
        label: this.formatLabel(resourceKey), // Convertit 'moonbell' en 'Moon Bell'
        key: resourceKey
      }))
    }));
  }
  
  /**
   * Capitalise la première lettre d'un mot (ex: "wood" -> "Wood")
   */
  capitalizeFirstLetter(str: string): string {
    return str.charAt(0).toUpperCase() + str.slice(1);
  }
  
  /**
   * Remplace les underscores par des espaces et capitalise (ex: "moonbell" -> "Moon Bell")
   */
  formatLabel(str: string): string {
    return str.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
  }

  
}
