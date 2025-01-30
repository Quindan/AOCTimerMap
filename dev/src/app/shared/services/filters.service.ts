import { Injectable } from '@angular/core';
import { RESOURCE_CATEGORIES } from '../../map/enums/ressources.enum';

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

  
}
