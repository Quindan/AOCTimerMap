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

  /*getTreeResourceOptions(): any[] {
    return Object.entries(RESOURCE_CATEGORIES).map(([category, resources]) => ({
      label: this.capitalizeFirstLetter(category), // Convertit 'wood' en 'Wood'
      key: category, 
      selectable: true, // Empêche la sélection des catégories
      children: Object.entries(resources).map(([resourceKey, resourcePath]) => ({
        label: this.formatLabel(resourceKey), // Convertit 'moonbell' en 'Moon Bell'
        key: resourceKey
      }))
    }));
  }*/

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


      /*return [
        {
            "label": "Work",
            "icon": "pi pi-folder",
            "children": [
                {
                    "label": "data.json",
                    "icon": "pi pi-file"
                },
                {
                    "label": "sales.docx",
                    "icon": "pi pi-file"
                },
                {
                    "label": "presentation.pptx",
                    "icon": "pi pi-file"
                }
            ]
        },
        {
            "label": "Home",
            "icon": "pi pi-folder",
            "children": [
                {
                    "label": "grocery.word",
                    "icon": "pi pi-file"
                },
                {
                    "label": "picture.jpeg",
                    "icon": "pi pi-file"
                },
                {
                    "label": "homeplan.png",
                    "icon": "pi pi-file"
                }
            ]
        },
        {
            "label": "Multimedia",
            "icon": "pi pi-folder",
            "children": [
                {
                    "label": "infinity-war.mp4",
                    "icon": "pi pi-file"
                },
                {
                    "label": "you.mp3",
                    "icon": "pi pi-file"
                },
                {
                    "label": "endgame.mp4",
                    "icon": "pi pi-file"
                },
                {
                    "label": "MI.mp4",
                    "icon": "pi pi-file"
                }
            ]
        }
    ];*/

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
