import { Injectable } from '@angular/core';
import { RESOURCE_CATEGORIES } from '../../map/enums/ressources.enum';

@Injectable({
  providedIn: 'root'
})
export class RessourcesService {

  constructor() { }

  getResourceIcon(resourceName: string): string | null {
    for (const category of Object.values(RESOURCE_CATEGORIES)) {
      if (resourceName in category) {
        return category[resourceName];
      }
    }
    return null; // Retourne null si la ressource n'existe pas
  }

  getAllResources(): string[] {
    return Object.values(RESOURCE_CATEGORIES)
      .flatMap(category => Object.keys(category));
  }
}
