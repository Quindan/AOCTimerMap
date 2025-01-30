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
      label: this.capitalizeFirstLetter(category), 
      key: category, 
      selectable: true, 
      icon: `tree-custom-icon my-icon-${category}`, 
      children: Object.entries(resources).map(([resourceKey, resourcePath]) => ({          
        icon: `tree-custom-icon my-icon-${resourceKey.replaceAll('_', '-')}`,
        label: this.formatLabel(resourceKey),
        key: resourceKey,
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
